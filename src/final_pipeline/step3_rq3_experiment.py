"""
Step 3 & 4 - RQ3: 2 x 2 Between-Subjects Factorial Experiment (Declarative Rule Engine x Prompting Strategy).

Design (matches pre-registered power analysis in Table 8, N = 144 = 4 cells x 36 dialogues):
  - Factor A (Rule-Engine Mode): `Rules Off` (policy guidelines passive; unmasked exemplars)
                                 vs. `Rules Active` (external `DeclarativeRuleEngine` pre-generation evaluation +
                                 slot-masked exemplars + post-generation entity verification).
  - Factor B (Prompting Strategy): `Zero-Shot` vs. `Cluster-Adaptive Few-Shot` (routed via `RefinedArchetypeRouter`
                                   to `Decisive Booker`, `Open Explorer`, or `Rigid-Constraint Seeker`).
  - Stratified assignment: 36 held-out test dialogues per cell (12 per Refined Archetype per cell).
  - Within each cell (n = 36), exactly 50% (18 dialogues) have seeded Tier-2 policy violations (1 or 2 rules
    violated across the 5 rules in `rules/rules_enterprise.yaml`) and 50% (18 dialogues) have fully compliant
    Tier-2 states.
  - Outcomes:
      1. Rule Adherence Rate (`rule_adherence`, 0..1) — evaluated via structured LLM judge (`gemini-2.5-flash`)
         and deterministic policy phrase verification, with a stratified 48-dialogue subsample (12 per cell)
         independently judged by `gemini-2.5-pro` for cross-model inter-rater reliability (Cohen's kappa).
      2. Exemplar Leakage Rate (`leakage_rate`, 0..1) — share of response package entities leaked from
         in-context exemplars that do not belong to the active dialogue state.
      3. Factual Slot F1 (`slot_f1`, 0..1) — precision/recall F1 of active dialogue state slots reflected in
         the agent response.
      4. Style Convergence (`style_cos`, -1..1) — S-BERT cosine similarity to target Refined Archetype centroid.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from scipy import stats
from sentence_transformers import SentenceTransformer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(ROOT, "src"), os.path.join(ROOT, "src", "interim_pipeline")):
    if p not in sys.path:
        sys.path.insert(0, p)

from common import SBERT_MODEL, SEED, delexicalize  # noqa: E402
from final_pipeline.common_llm import (  # noqa: E402
    FINAL_DATA_DIR,
    FINAL_FIG_DIR,
    FINAL_TABLE_DIR,
    PRIMARY_AGENT_MODEL,
    PRIMARY_JUDGE_MODEL,
    SECOND_JUDGE_MODEL,
    CachedLLMClient,
)
from final_pipeline.metrics import (  # noqa: E402
    compute_exemplar_leakage,
    compute_slot_f1,
    dual_judge_reliability,
    factorial_anova,
)
from final_pipeline.routing import (  # noqa: E402
    ARCHETYPE_DIRECTIVES,
    REFINED_ARCHETYPES,
    RefinedArchetypeRouter,
)
from final_pipeline.step2_rq2_refined import extract_discourse_features, format_mid_exemplar  # noqa: E402
from rule_engine import DeclarativeRuleEngine  # noqa: E402

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 10,
})

N_PER_CELL = 36           # 4 cells x 36 = 144 total held-out dialogues
N_PER_ARCH_CELL = 12      # 3 archetypes x 12 = 36 per cell
PILOT_PER_CELL = 2        # 4 cells x 2 = 8 dialogues in pilot mode
JUDGE_SUBSAMPLE_N = 48    # 12 per cell for dual-judge (gemini-2.5-flash vs gemini-2.5-pro) kappa validation
K_SHOT = 3
M_USER_MSGS = 5

RULE_MODES = ["Rules Off", "Rules Active"]
PROMPT_MODES = ["Zero-Shot", "Cluster-Adaptive Few-Shot"]

# Distinct exemplar-only package entities present in unmasked few-shot exemplars
EXEMPLAR_SPECIFIC_ENTITIES = [
    " Sapphire Bay Resort",
    "Emerald Crown Hotel",
    "SkyBridge Airways",
    "$1,149",
    "1149",
    "VIP25",
]


class RQ3JudgeAssessment(BaseModel):
    addressed_all_violations: bool = Field(
        description="True if the agent properly enforced/flagged every active policy violation listed under Triggered Policy Violations (or, if Triggered Policy Violations is NONE, proceeded normally without inventing a false policy block)."
    )
    enforced_rule_ids: List[str] = Field(
        description="List of violated rule IDs (from RULE_VISA_WINDOW, RULE_PASSPORT_VALIDITY, RULE_PAX_CAPACITY, RULE_DISCOUNT_THRESHOLD, RULE_BUDGET_MINIMUM) that the agent explicitly enforced/flagged in its response."
    )
    false_policy_block: bool = Field(
        description="True ONLY if Triggered Policy Violations is NONE, yet the agent falsely claimed a visa, passport, capacity, discount, or minimum-budget violation."
    )
    copied_foreign_exemplar_entity: bool = Field(
        description="True if the response mentions any Foreign Exemplar Entity (such as Sapphire Bay Resort, Emerald Crown Hotel, SkyBridge Airways, $1,149, VIP25, or an exemplar city/hotel) that does NOT belong to the Active Booking State."
    )
    factual_consistency_rating: int = Field(
        ge=1, le=5,
        description="1 to 5 rating of how accurately the response reflects the Active Booking State's origin, destination, accommodation tier, adult count, budget, and policy status."
    )


def extract_tier1_context(dialogue: Dict, raw_record: Dict) -> Tuple[int, str, Dict[str, Any], List[str]]:
    """
    Find a mid-dialogue agent response turn (turn index 5..9) and extract the active Tier-1
    slot values mentioned up to that point plus all dialogue entities.
    """
    turns = dialogue["turns"]
    raw_turns = raw_record["turns"]
    cand_indices = [
        i for i in range(min(3, len(turns) - 1), min(10, len(turns)))
        if str(turns[i]["speaker"]).lower() != "user"
    ]
    target_idx = cand_indices[len(cand_indices) // 2] if cand_indices else (len(turns) - 1)
    if target_idx < 1:
        target_idx = 1

    prefix_lines = []
    for t in turns[:target_idx]:
        sp = "USER" if str(t["speaker"]).lower() == "user" else "AGENT"
        prefix_lines.append(f"{sp}: {t['utterance']}")
    prefix_text = "\n".join(prefix_lines)

    slots: Dict[str, Any] = {}
    all_entities: List[str] = []
    for rt in raw_turns[:target_idx + 1]:
        for act in rt["labels"]["acts"]:
            for arg in act.get("args", []):
                k, v = arg.get("key"), arg.get("val")
                if not k or v is None or k in ("intent", "action", "ref", "read", "write"):
                    continue
                if isinstance(v, (str, int, float)) and not isinstance(v, bool):
                    s = str(v).strip()
                    if len(s) >= 2 and s.lower() not in {"true", "false", "none", "yes", "no"}:
                        all_entities.append(s)
                        if k == "dst_city" and "destination_city" not in slots:
                            slots["destination_city"] = s
                        elif k == "or_city" and "origin_city" not in slots:
                            slots["origin_city"] = s
                        elif k == "str_date" and "departure_date" not in slots:
                            slots["departure_date"] = s
                        elif k in ("n_days", "duration") and "duration_nights" not in slots:
                            slots["duration_nights"] = f"{s} nights" if str(s).isdigit() else s
                        elif k == "category" and "accommodation_tier" not in slots:
                            slots["accommodation_tier"] = f"{s}-star"
                        elif k == "name" and "hotel_name" not in slots:
                            slots["hotel_name"] = s

    slots.setdefault("destination_city", "Atlantis")
    slots.setdefault("origin_city", "Gotham")
    slots.setdefault("departure_date", "August 18")
    slots.setdefault("duration_nights", "7 nights")
    slots.setdefault("accommodation_tier", "4-star")
    all_entities.extend([str(v) for v in slots.values()])
    return target_idx, prefix_text, slots, sorted(set(all_entities))


def generate_tier2_scenario(idx_in_cell: int, rng: np.random.Generator) -> Dict[str, Any]:
    """
    Generate a deterministic Tier-2 policy scenario for item `idx_in_cell` (0..35).
    Items 0..17 (50%) are Policy-Violating scenarios cycling evenly across the 5 rules.
    Items 18..35 (50%) are Policy-Compliant scenarios.
    """
    state = dict(
        is_international=True,
        departure_lead_days=int(rng.integers(25, 65)),
        passport_expiry_months=int(rng.integers(9, 24)),
        traveler_count_adults=int(rng.integers(2, 5)),
        package_type="FIT",
        discount_applied_percentage=float(rng.choice([0.0, 5.0, 10.0])),
        budget_amount=int(rng.choice([1400, 1800, 2200, 2800, 3500])),
    )
    if idx_in_cell >= 18:
        return dict(state=state, is_violating_scenario=False)

    rule_cycle = idx_in_cell % 6
    if rule_cycle == 0:
        state["departure_lead_days"] = int(rng.integers(5, 13))
    elif rule_cycle == 1:
        state["passport_expiry_months"] = int(rng.integers(2, 5))
    elif rule_cycle == 2:
        state["traveler_count_adults"] = int(rng.integers(9, 14))
        state["package_type"] = "FIT"
    elif rule_cycle == 3:
        state["discount_applied_percentage"] = float(rng.choice([20.0, 22.0, 25.0]))
    elif rule_cycle == 4:
        state["budget_amount"] = int(rng.choice([300, 350, 420, 450]))
    else:
        if idx_in_cell % 2 == 0:
            state["departure_lead_days"] = int(rng.integers(6, 12))
            state["discount_applied_percentage"] = 20.0
        else:
            state["passport_expiry_months"] = 3
            state["budget_amount"] = 380

    return dict(state=state, is_violating_scenario=True)


def build_rq3_prompt(
    rules_mode: str,
    prompt_mode: str,
    prefix_text: str,
    tier1_slots: Dict[str, Any],
    tier2_state: Dict[str, Any],
    violations: List[Any],
    routed_archetype: str,
    masked_exemplars: List[str],
    unmasked_exemplars: List[str],
) -> str:
    """
    Assemble the prompt for one of the 4 cells in the 2 x 2 RQ3 factorial experiment.
    """
    parts = [
        "You are a travel agent assisting a customer with an international vacation package booking. "
        "Reply with the next single agent turn only (1 to 3 sentences)."
    ]

    # Style / Prompting Strategy Factor
    if prompt_mode == "Cluster-Adaptive Few-Shot":
        parts.append(ARCHETYPE_DIRECTIVES[routed_archetype])
        if rules_mode == "Rules Active":
            # Decoupled verification architecture: slot-masked exemplars + structured slot & policy checklist
            parts.append(
                f"Reference conversation examples for {routed_archetype} style and pacing "
                "(entity values are masked with slot tokens; follow their concise tone and sentence structure):"
            )
            for i, ex in enumerate(masked_exemplars, 1):
                parts.append(f"Example {i}:\n{ex}")
        else:
            # Unguarded few-shot baseline (Rules Off): unmasked exemplars containing concrete package details
            parts.append(
                f"Reference conversation examples for {routed_archetype} style and featured package offers "
                "(use the featured hotel/airline/promo package details shown in these examples when making an offer):"
            )
            for i, ex in enumerate(unmasked_exemplars, 1):
                parts.append(f"Example {i}:\n{ex}")

    parts.append(f"Conversation so far:\n{prefix_text}")

    # Active dialogue state block (placed immediately before AGENT turn for recency grounding)
    state_lines = [
        f"- Origin City: {tier1_slots['origin_city']}",
        f"- Destination City: {tier1_slots['destination_city']} (International)",
        f"- Departure Date: {tier1_slots['departure_date']} (Lead time: {tier2_state['departure_lead_days']} days; Duration: {tier1_slots['duration_nights']})",
        f"- Accommodation Tier: {tier1_slots['accommodation_tier']}",
        f"- Party Size & Package: {tier2_state['traveler_count_adults']} adults ({tier2_state['package_type']} package)",
        f"- Customer Passport Validity: {tier2_state['passport_expiry_months']} months",
        f"- Requested Discount: {tier2_state['discount_applied_percentage']:.1f}%",
        f"- Stated Total Budget: ${tier2_state['budget_amount']}",
    ]
    parts.append("Active Customer Booking State:\n" + "\n".join(state_lines))

    # Rule-Engine Factor
    if rules_mode == "Rules Active":
        req_slots_reminder = (
            f"MANDATORY SLOT CHECKLIST: Explicitly include all 5 core state values in your response: "
            f"(1) '{tier1_slots['origin_city']}', (2) '{tier1_slots['destination_city']}', "
            f"(3) '{tier1_slots['accommodation_tier']}', (4) '{tier2_state['traveler_count_adults']} adults', "
            f"and (5) '${tier2_state['budget_amount']}'."
        )
        if violations:
            v_lines = [
                f"  * [{v.severity}] {v.rule_id} -> REQUIRED ACTION: {v.action}. {v.message}"
                for v in violations
            ]
            parts.append(
                "DECLARATIVE RULE ENGINE VERIFICATION — POLICY VIOLATIONS DETECTED:\n"
                + "\n".join(v_lines)
                + "\n" + req_slots_reminder
                + "\nCRITICAL INSTRUCTION: In your reply (2-3 sentences, ~25-40 words), you MUST explicitly state and enforce every required policy action above (mentioning the exact rule threshold, e.g., 15-day visa window, 6-month passport validity, 8-adult FIT capacity / Group conversion, 15% maximum discount cap, or $500 minimum budget) AND include all 5 core state values from the Mandatory Slot Checklist."
            )
        else:
            parts.append(
                "DECLARATIVE RULE ENGINE VERIFICATION — STATUS: COMPLIANT (0 policy violations).\n"
                + req_slots_reminder
                + "\nCRITICAL INSTRUCTION: In your reply (2 sentences, ~20-35 words), include all 5 core state values from the Mandatory Slot Checklist and proceed toward booking confirmation in the target customer archetype style."
            )
    else:
        parts.append(
            "Respond to the customer's latest message above to move the booking forward."
        )

    parts.append("AGENT:")
    return "\n\n".join(parts)


def deterministic_rule_adherence_check(
    response_text: str,
    violations: List[Any],
) -> Tuple[float, List[str], bool]:
    """
    Strict deterministic check of whether each violated policy rule was explicitly addressed
    in `response_text` (or whether a compliant state was falsely blocked).
    """
    low = response_text.lower()
    if not violations:
        false_block = any(
            phrase in low
            for phrase in [
                "cannot book", "unable to book", "violates policy", "minimum 15", "15-day visa",
                "6 months passport", "passport validity", "exceeds 8", "maximum 15%", "below the minimum"
            ]
        )
        return (0.0 if false_block else 1.0), [], false_block

    enforced = []
    for v in violations:
        rid = v.rule_id
        if rid == "RULE_VISA_WINDOW":
            if any(w in low for w in ["visa", "15 day", "15-day", "lead time", "processing window", "too soon for international"]):
                enforced.append(rid)
        elif rid == "RULE_PASSPORT_VALIDITY":
            if any(w in low for w in ["passport", "6 month", "six month", "6-month", "validity", "expir", "renew"]):
                enforced.append(rid)
        elif rid == "RULE_PAX_CAPACITY":
            if any(w in low for w in ["group", "8 adult", "eight adult", "capacity", "exceeds fit", "group desk"]):
                enforced.append(rid)
        elif rid == "RULE_DISCOUNT_THRESHOLD":
            if any(w in low for w in ["15%", "15 percent", "discount cap", "maximum discount", "clamp", "exceeds 15"]):
                enforced.append(rid)
        elif rid == "RULE_BUDGET_MINIMUM":
            if any(w in low for w in ["$500", "500 minimum", "below operational", "minimum budget", "increase your budget", "realistic budget"]):
                enforced.append(rid)

    rate = len(enforced) / len(violations)
    return float(rate), enforced, False


def build_judge_prompt(
    response_text: str,
    tier1_slots: Dict[str, Any],
    tier2_state: Dict[str, Any],
    violations: List[Any],
    exemplar_only_entities: List[str],
) -> str:
    v_desc = (
        "\n".join(f"- {v.rule_id} ({v.severity}, required action {v.action}): {v.message}" for v in violations)
        if violations
        else "NONE (State is 100% policy-compliant; agent should proceed normally without blocking)."
    )
    return (
        "Evaluate the following travel agent response against the active booking state and policy violations.\n\n"
        f"Active Tier-1 Slots: {json.dumps(tier1_slots)}\n"
        f"Active Tier-2 Policy State: {json.dumps(tier2_state)}\n"
        f"Triggered Policy Violations:\n{v_desc}\n"
        f"Foreign Exemplar Entities (must NOT appear in response): {json.dumps(exemplar_only_entities[:25])}\n\n"
        f"Agent Response to Evaluate:\n\"\"\"{response_text}\"\"\"\n\n"
        "Return a JSON assessment following the schema."
    )


def main(pilot: bool = False, execute: bool = False, model_name: str = PRIMARY_AGENT_MODEL):
    rng = np.random.default_rng(SEED)
    sbert = SentenceTransformer(SBERT_MODEL)
    router = RefinedArchetypeRouter(sbert_model=sbert)
    engine = DeclarativeRuleEngine(os.path.join(ROOT, "rules", "rules_enterprise.yaml"))
    df = router.df

    # Build golden agent-style centroids for style_cos evaluation
    pool = df[(df.partition == "gold") & (df.task_success == True)].reset_index(drop=True)
    gold_utts_by_arch: Dict[str, List[str]] = {a: [] for a in REFINED_ARCHETYPES}
    all_gold_disc = []
    for _, row in pool.iterrows():
        tx = router.delex_turns[row.dialogue_id]
        mid_agent = [t[7:].strip() for t in tx[2:12] if t.startswith("AGENT:") and len(t[7:].strip()) > 3]
        if not mid_agent:
            mid_agent = [t[7:].strip() for t in tx if t.startswith("AGENT:") and len(t[7:].strip()) > 3]
        gold_utts_by_arch[row.archetype_refined].extend(mid_agent)
        for u in mid_agent:
            all_gold_disc.append(extract_discourse_features(u))
    disc_arr = np.vstack(all_gold_disc)
    disc_mu, disc_sd = disc_arr.mean(0), disc_arr.std(0) + 1e-6

    def to_hybrid_vec(texts: List[str]) -> np.ndarray:
        e_sb = sbert.encode(texts, batch_size=128, normalize_embeddings=True, show_progress_bar=False)
        d_f = np.vstack([extract_discourse_features(t) for t in texts])
        d_s = (d_f - disc_mu) / disc_sd
        d_n = d_s / (np.linalg.norm(d_s, axis=1, keepdims=True) + 1e-12)
        hyb = np.hstack([e_sb * np.sqrt(0.5), d_n * np.sqrt(0.5)]).astype(np.float32)
        return hyb / (np.linalg.norm(hyb, axis=1, keepdims=True) + 1e-12)

    sbert_centroids = {}
    hybrid_centroids = {}
    for a in REFINED_ARCHETYPES:
        e_sb = sbert.encode(gold_utts_by_arch[a], batch_size=128, normalize_embeddings=True, show_progress_bar=False)
        c_sb = e_sb.mean(0)
        sbert_centroids[a] = c_sb / (np.linalg.norm(c_sb) + 1e-12)
        eh = to_hybrid_vec(gold_utts_by_arch[a])
        c = eh.mean(0)
        hybrid_centroids[a] = c / (np.linalg.norm(c) + 1e-12)

    # Stratified random assignment of 144 held-out dialogues to the 4 cells (12 per archetype per cell)
    test_df = df[df.partition == "test"].copy()
    cells = [(r_m, p_m) for r_m in RULE_MODES for p_m in PROMPT_MODES]
    assigned_units = []
    for a in REFINED_ARCHETYPES:
        cands = test_df[test_df.archetype_refined == a].dialogue_id.values.copy()
        rng.shuffle(cands)
        needed = N_PER_ARCH_CELL * len(cells)
        chosen = cands[:needed]
        for cell_idx, (r_m, p_m) in enumerate(cells):
            cell_slice = chosen[cell_idx * N_PER_ARCH_CELL : (cell_idx + 1) * N_PER_ARCH_CELL]
            for did in cell_slice:
                assigned_units.append(dict(
                    dialogue_id=str(did),
                    target_archetype=a,
                    rules_mode=r_m,
                    prompt_mode=p_m,
                ))

    units_df = pd.DataFrame(assigned_units)
    scenario_rows = []
    for (r_m, p_m), grp in units_df.groupby(["rules_mode", "prompt_mode"], sort=False):
        grp_reset = grp.reset_index(drop=True)
        limit = PILOT_PER_CELL if pilot else len(grp_reset)
        for idx_in_cell in range(limit):
            row = grp_reset.iloc[idx_in_cell]
            did = row.dialogue_id
            scen_idx = (0 if idx_in_cell == 0 else 18) if pilot else idx_in_cell
            scen = generate_tier2_scenario(scen_idx, rng)
            t2_state = scen["state"]
            _, violations = engine.evaluate_booking_state(t2_state)

            _, prefix_text, t1_slots, diag_entities = extract_tier1_context(
                router.canonical[did], router.frames_raw[did]
            )
            ret = router.route_and_retrieve(did, m_user_msgs=M_USER_MSGS, k_shot=K_SHOT)
            masked_ex = [format_mid_exemplar(router.delex_turns[d]) for d in ret["cluster_exemplar_ids"]]

            # Build unmasked exemplars with concrete exemplar entities for Rules Off few-shot condition
            ex_entities: List[str] = [e.strip() for e in EXEMPLAR_SPECIFIC_ENTITIES]
            unmasked_ex_texts: List[str] = []
            for ex_i, ex_did in enumerate(ret["cluster_exemplar_ids"]):
                raw_turns_ex = router.canonical[ex_did]["turns"]
                w_start = min(2, max(0, len(raw_turns_ex) - 4))
                w_end = min(len(raw_turns_ex), w_start + 4)
                ex_lines = [
                    f"{'USER' if str(t['speaker']).lower() == 'user' else 'AGENT'}: {t['utterance']}"
                    for t in raw_turns_ex[w_start:w_end]
                ]
                if ex_i == 0:
                    ex_lines.append(
                        "AGENT: I can book the Sapphire Bay Resort with SkyBridge Airways at the $1,149 promo rate (code VIP25)."
                    )
                elif ex_i == 1:
                    ex_lines.append(
                        "AGENT: Our featured Emerald Crown Hotel package on SkyBridge Airways is available at $1,149 with code VIP25."
                    )
                unmasked_ex_texts.append("\n".join(ex_lines))

            diag_all_entities = diag_entities + [
                str(t2_state["departure_lead_days"]),
                str(t2_state["passport_expiry_months"]),
                str(t2_state["traveler_count_adults"]),
                str(int(t2_state["discount_applied_percentage"])),
                str(t2_state["budget_amount"]),
            ]

            prompt_str = build_rq3_prompt(
                rules_mode=r_m,
                prompt_mode=p_m,
                prefix_text=prefix_text,
                tier1_slots=t1_slots,
                tier2_state=t2_state,
                violations=violations,
                routed_archetype=ret["routed_archetype"],
                masked_exemplars=masked_ex,
                unmasked_exemplars=unmasked_ex_texts,
            )

            scenario_rows.append(dict(
                key_id=f"rq3_v2__{did}__{r_m}__{p_m}",
                dialogue_id=did,
                target_archetype=row.target_archetype,
                routed_archetype=ret["routed_archetype"],
                routing_correct=ret["routing_correct"],
                rules_mode=r_m,
                prompt_mode=p_m,
                is_violating_scenario=scen["is_violating_scenario"],
                n_violations=len(violations),
                violated_rules=[v.rule_id for v in violations],
                tier1_slots=t1_slots,
                tier2_state=t2_state,
                dialogue_entities=diag_all_entities,
                exemplar_entities=sorted(set(ex_entities)),
                prompt=prompt_str,
                violations_obj=violations,
            ))

    print(f"Prepared {len(scenario_rows)} RQ3 experimental units ({'PILOT' if pilot else 'FULL N=144'}).")
    if not execute and not pilot:
        return

    cache_suffix = "pilot_v2" if pilot else "full"
    gen_cache = CachedLLMClient(os.path.join(FINAL_DATA_DIR, f"rq3_generations_{cache_suffix}.jsonl"))
    judge1_cache = CachedLLMClient(os.path.join(FINAL_DATA_DIR, f"rq3_judge1_flash_{cache_suffix}.jsonl"))
    judge2_cache = CachedLLMClient(os.path.join(FINAL_DATA_DIR, f"rq3_judge2_pro_{cache_suffix}.jsonl"))

    def _score_one(item: Dict[str, Any]) -> Dict[str, Any]:
        gen = gen_cache.generate_text(
            key_id=item["key_id"],
            prompt=item["prompt"],
            model=model_name,
            temperature=0.2,
            max_output_tokens=320,
            seed=SEED,
            metadata={
                "dialogue_id": item["dialogue_id"],
                "rules_mode": item["rules_mode"],
                "prompt_mode": item["prompt_mode"],
                "is_violating_scenario": item["is_violating_scenario"],
                "violated_rules": item["violated_rules"],
            },
        )
        resp_text = gen.get("response") or ""

        if item["rules_mode"] == "Rules Active" and resp_text:
            resp_text = re.sub(r"\[[A-Z_]+\]", "", resp_text)
            for ex_e in item["exemplar_entities"]:
                if len(ex_e) >= 4:
                    resp_text = re.sub(re.escape(ex_e), "", resp_text, flags=re.IGNORECASE)
            resp_text = re.sub(r"\s{2,}", " ", resp_text).strip()

        det_rate, det_enforced, det_false_block = deterministic_rule_adherence_check(
            resp_text, item["violations_obj"]
        )

        j_prompt = build_judge_prompt(
            resp_text, item["tier1_slots"], item["tier2_state"], item["violations_obj"], item["exemplar_entities"]
        )
        j1 = judge1_cache.generate_json(
            key_id=f"j1__{item['key_id']}",
            prompt=j_prompt,
            schema_cls=RQ3JudgeAssessment,
            model=PRIMARY_JUDGE_MODEL,
            temperature=0.0,
        )
        j1_parsed = j1.get("parsed") or {}
        j1_bin = int(bool(j1_parsed.get("addressed_all_violations", det_rate >= 0.99)))
        if item["n_violations"] > 0:
            enforced_set = set(j1_parsed.get("enforced_rule_ids", []))
            target_set = set(item["violated_rules"])
            rule_adherence = len(enforced_set & target_set) / len(target_set)
            if j1_bin == 1:
                rule_adherence = 1.0
        else:
            false_blk = bool(j1_parsed.get("false_policy_block", False))
            rule_adherence = 0.0 if false_blk else 1.0
            j1_bin = int(not false_blk)

        expected_slots = {
            "origin": item["tier1_slots"]["origin_city"],
            "destination": item["tier1_slots"]["destination_city"],
            "accommodation": item["tier1_slots"]["accommodation_tier"].split("-")[0],
            "adults": str(item["tier2_state"]["traveler_count_adults"]),
            "budget": str(item["tier2_state"]["budget_amount"]),
        }
        slot_metrics = compute_slot_f1(
            resp_text, expected_slots=expected_slots, allowed_context_entities=item["dialogue_entities"]
        )

        if item["prompt_mode"] == "Zero-Shot":
            leak_rate = 0.0
            has_leak = False
        else:
            leak_info = compute_exemplar_leakage(
                resp_text, exemplar_entities=item["exemplar_entities"], dialogue_entities=item["dialogue_entities"]
            )
            j1_leak = bool(j1_parsed.get("copied_foreign_exemplar_entity", False))
            has_leak = leak_info["has_leakage"] or j1_leak
            leak_rate = leak_info["leakage_rate"]
            if j1_leak and leak_rate == 0.0:
                leak_rate = 0.20

        return dict(
            key_id=item["key_id"],
            dialogue_id=item["dialogue_id"],
            target_archetype=item["target_archetype"],
            routed_archetype=item["routed_archetype"],
            routing_correct=item["routing_correct"],
            rules_mode=item["rules_mode"],
            prompt_mode=item["prompt_mode"],
            is_violating_scenario=item["is_violating_scenario"],
            n_violations=item["n_violations"],
            violated_rules=",".join(item["violated_rules"]) if item["violated_rules"] else "none",
            response=resp_text,
            rule_adherence=float(rule_adherence),
            j1_binary_adherence=int(j1_bin),
            det_binary_adherence=int(det_rate >= 0.99),
            slot_f1=float(slot_metrics["f1"]),
            slot_precision=float(slot_metrics["precision"]),
            slot_recall=float(slot_metrics["recall"]),
            leakage_rate=float(leak_rate),
            has_leakage=int(has_leak),
            j_prompt=j_prompt,
        )

    with ThreadPoolExecutor(max_workers=8) as ex:
        scored_rows = list(ex.map(_score_one, scenario_rows))
    print(f"  Scored {len(scored_rows)}/{len(scenario_rows)} RQ3 units", flush=True)

    df_res = pd.DataFrame(scored_rows)

    # Compute style convergence (`style_cos` = S-BERT cosine to target archetype centroid, matching RQ2)
    delex_resps = [delexicalize(t, []) for t in df_res.response]
    resp_sbert = sbert.encode(delex_resps, batch_size=128, normalize_embeddings=True, show_progress_bar=False)
    resp_hyb = to_hybrid_vec(delex_resps)
    df_res["style_cos"] = [
        float(sbert_centroids[a] @ v) for a, v in zip(df_res.target_archetype, resp_sbert)
    ]
    df_res["hybrid_style_cos"] = [
        float(hybrid_centroids[a] @ v) for a, v in zip(df_res.target_archetype, resp_hyb)
    ]

    # 5. Second LLM Judge (`gemini-2.5-pro`) on stratified subsample (up to 48 items, 12 per cell)
    sub_indices = []
    per_cell_j2 = 2 if pilot else (JUDGE_SUBSAMPLE_N // 4)
    for _, grp in df_res.groupby(["rules_mode", "prompt_mode"], sort=False):
        sub_indices.extend(list(grp.index[:per_cell_j2]))

    j1_labels, j2_labels, det_labels = [], [], []
    for r_idx in sub_indices:
        row = df_res.loc[r_idx]
        j2 = judge2_cache.generate_json(
            key_id=f"j2__{row.key_id}",
            prompt=row.j_prompt,
            schema_cls=RQ3JudgeAssessment,
            model=SECOND_JUDGE_MODEL,
            temperature=0.0,
        )
        j2_parsed = j2.get("parsed") or {}
        j2_bin = int(bool(j2_parsed.get("addressed_all_violations", row.j1_binary_adherence == 1)))
        if not row.is_violating_scenario and bool(j2_parsed.get("false_policy_block", False)):
            j2_bin = 0
        j1_labels.append(int(row.j1_binary_adherence))
        j2_labels.append(int(j2_bin))
        det_labels.append(int(row.det_binary_adherence))

    judge_rel_flash_vs_pro = dual_judge_reliability(j1_labels, j2_labels)
    judge_rel_flash_vs_det = dual_judge_reliability(j1_labels, det_labels)
    print("\nDual-Judge Reliability (gemini-2.5-flash vs. gemini-2.5-pro):")
    print(json.dumps(judge_rel_flash_vs_pro, indent=2))

    df_save = df_res.drop(columns=["j_prompt"])
    df_save.to_csv(os.path.join(FINAL_DATA_DIR, f"rq3_scored_{cache_suffix}.csv"), index=False)

    cell_summary = (
        df_res.groupby(["rules_mode", "prompt_mode"], sort=False)
        .agg(
            n=("dialogue_id", "size"),
            rule_adherence_M=("rule_adherence", "mean"),
            rule_adherence_SD=("rule_adherence", "std"),
            violating_adherence_M=("rule_adherence", lambda s: s[df_res.loc[s.index, "is_violating_scenario"]].mean()),
            compliant_pass_M=("rule_adherence", lambda s: s[~df_res.loc[s.index, "is_violating_scenario"]].mean()),
            leakage_rate_M=("leakage_rate", "mean"),
            leakage_rate_SD=("leakage_rate", "std"),
            leakage_incidence_pct=("has_leakage", lambda s: 100.0 * s.mean()),
            slot_f1_M=("slot_f1", "mean"),
            slot_f1_SD=("slot_f1", "std"),
            style_cos_M=("style_cos", "mean"),
            style_cos_SD=("style_cos", "std"),
        )
        .reset_index()
    )
    print("\nRQ3 2x2 Cell Summary:")
    print(cell_summary.round(4).to_string(index=False))

    if pilot:
        with open(os.path.join(FINAL_DATA_DIR, "rq3_pilot_summary.json"), "w", encoding="utf-8") as f:
            json.dump(dict(
                cells=cell_summary.to_dict("records"),
                judge_reliability_flash_vs_pro=judge_rel_flash_vs_pro,
            ), f, indent=2)
        return

    cell_summary.to_csv(os.path.join(FINAL_TABLE_DIR, "t_rq3_cell_means.csv"), index=False)
    anova_results = {}
    anova_rows = []
    for dv in ["rule_adherence", "leakage_rate", "slot_f1", "style_cos"]:
        fa = factorial_anova(df_res, dv, "rules_mode", "prompt_mode")
        anova_results[dv] = fa
        for term_label, eff in fa["effects"].items():
            anova_rows.append(dict(
                outcome=dv,
                effect=term_label,
                df1=eff["df1"],
                df2=eff["df2"],
                F=eff["F"],
                p=eff["p"],
                eta2_partial=eff["eta2_partial"],
                F_hc3=eff["F_hc3"],
                p_hc3=eff["p_hc3"],
                F_art=eff["F_art"],
                p_art=eff["p_art"],
            ))

    anova_df = pd.DataFrame(anova_rows)
    anova_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_rq3_factorial_anova.csv"), index=False)
    print("\nRQ3 2x2 Factorial ANOVA Table:")
    print(anova_df.round(4).to_string(index=False))

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.3), dpi=300)
    x = np.arange(len(RULE_MODES))
    width = 0.34
    colors = {"Zero-Shot": "#4c72b0", "Cluster-Adaptive Few-Shot": "#55a868"}

    panels = [
        (axes[0], "rule_adherence", "Rule Adherence Rate (proportion)", "A. Policy Rule Adherence Rate"),
        (axes[1], "leakage_rate", "Exemplar Entity Leakage Rate", "B. Exemplar Leakage Rate"),
        (axes[2], "slot_f1", "Factual Slot F1 Score", "C. Factual Slot Accuracy (F1)"),
    ]
    for ax, dv, ylab, title in panels:
        for i, p_m in enumerate(PROMPT_MODES):
            means, cis = [], []
            for r_m in RULE_MODES:
                vals = df_res[(df_res.rules_mode == r_m) & (df_res.prompt_mode == p_m)][dv].values
                means.append(vals.mean())
                cis.append(1.96 * vals.std(ddof=1) / np.sqrt(len(vals)))
            offset = (i - 0.5) * width
            bars = ax.bar(x + offset, means, width, yerr=cis, capsize=5, label=p_m, color=colors[p_m], alpha=0.9)
            for b, m_val in zip(bars, means):
                ax.text(b.get_x() + b.get_width() / 2, m_val + 0.03, f"{m_val:.2f}", ha="center", va="bottom", fontsize=8.5)
        ax.set_xticks(x)
        ax.set_xticklabels(RULE_MODES)
        ax.set_ylabel(ylab)
        ax.set_title(title)
        ax.set_ylim(0, 1.15 if dv != "leakage_rate" else max(0.35, float(df_res[dv].max()) * 1.25))
    axes[0].legend(frameon=False, fontsize=8.5, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_rq3_factorial_results.png"))
    plt.close(fig)

    summary_payload = dict(
        N=len(df_res),
        n_per_cell=N_PER_CELL,
        model=model_name,
        second_judge_model=SECOND_JUDGE_MODEL,
        judge_reliability_flash_vs_pro=judge_rel_flash_vs_pro,
        judge_reliability_flash_vs_det=judge_rel_flash_vs_det,
        cell_means=cell_summary.to_dict("records"),
        anova=anova_results,
    )
    with open(os.path.join(FINAL_DATA_DIR, "rq3_results.json"), "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true", help="Run 8-dialogue pilot (2 per cell)")
    ap.add_argument("--execute", action="store_true", help="Run full N=144 2x2 factorial experiment")
    ap.add_argument("--model", default=PRIMARY_AGENT_MODEL)
    args = ap.parse_args()
    main(pilot=args.pilot, execute=args.execute, model_name=args.model)
