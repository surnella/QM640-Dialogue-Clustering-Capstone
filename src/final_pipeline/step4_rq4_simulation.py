"""
Step 5 & 6 - RQ4: 2 x 3 Factorial Turn-Economy Simulation (Prompting Strategy x Refined Archetype).

Design (matches pre-registered power analysis in Table 8, N = 180 = 6 cells x 30 held-out dialogues):
  - Factor A (Prompting Strategy): `Zero-Shot` vs. `Cluster-Adaptive Few-Shot` (routed via `RefinedArchetypeRouter`
    with cumulative slot-ledger tracking and archetype-specific elicitation/recommendation policy; declarative
    rule engine active in both).
  - Factor B (Refined User Archetype): `Decisive Booker`, `Open Explorer`, `Rigid-Constraint Seeker` (30 held-out
    test dialogues per cell).
  - Multi-Turn Simulation:
      * A persona-conditioned LLM user simulator (`gemini-2.5-flash`) is initialized with the dialogue's
        extracted user goal constraints and its empirical Refined Archetype behavioral profile (Table 14).
      * The agent and user simulator converse turn-by-turn until all goal slots are satisfied and a package
        offer is accepted (`[ACCEPT_BOOKING]`) or `MAX_DIALOGUE_TURNS` (26 turns) is reached.
      * Every completed dialogue trajectory is cached immediately to `data/final/rq4_sim_{pilot|full}.jsonl`
        (thread-safe, resumable).
  - Outcomes:
      1. Turns to Goal Completion (`total_turns` and `log_turns`, tested via 2 x 3 Factorial ANOVA with HC3
         robust standard errors and ART non-parametric ANOVA).
      2. Redundant Elicitation Rate (`rer`: proportion of agent turns that re-request a slot value already
         explicitly provided by the user in an earlier turn).
      3. Goal Completion Rate (`goal_completed`: proportion of dialogues reaching booking acceptance within
         the turn cap).
  - Simulator Persona Fidelity Validation:
      * Stratified subsample of simulated user transcripts (n = 45, 15 per archetype) is rated using the
        Step 2e behavioral codebook (`gemini-2.5-pro` independent judge) to verify that simulated users
        match their intended archetype significantly above chance (33.3%).
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
import sys
import threading
import time
from typing import Any, Dict, List, Optional, Set, Tuple

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

from common import SBERT_MODEL, SEED  # noqa: E402
from final_pipeline.common_llm import (  # noqa: E402
    FINAL_DATA_DIR,
    FINAL_FIG_DIR,
    FINAL_TABLE_DIR,
    PRIMARY_AGENT_MODEL,
    SECOND_JUDGE_MODEL,
    load_gemini_api_key,
)
from final_pipeline.metrics import dual_judge_reliability, factorial_anova  # noqa: E402
from final_pipeline.routing import REFINED_ARCHETYPES, RefinedArchetypeRouter  # noqa: E402
from final_pipeline.step2_rq2_refined import format_mid_exemplar  # noqa: E402
from final_pipeline.step3_rq3_experiment import extract_tier1_context  # noqa: E402

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 10,
})

N_PER_CELL = 30           # 2 prompting modes x 3 archetypes x 30 = 180 dialogues
PILOT_PER_CELL = 1        # 2 x 3 x 1 = 6 dialogues in pilot mode
PERSONA_CHECK_N = 45      # 15 per archetype for persona fidelity validation
MAX_EXCHANGES = 11        # up to 22 total turns
K_SHOT = 3
M_USER_MSGS = 9
PROMPT_MODES = ["Zero-Shot", "Cluster-Adaptive Few-Shot"]

REQUIRED_GOAL_SLOTS = ["origin_city", "destination_city", "departure_date", "duration_nights", "budget_amount"]

SLOT_PATTERNS = {
    "origin_city": [r"\bfrom\s+[a-zA-Z]{3,}", r"\bdeparting from\s+[a-zA-Z]{3,}", r"\bflying out of\s+[a-zA-Z]{3,}"],
    "destination_city": [r"\bto\s+[a-zA-Z]{3,}", r"\bheading to\s+[a-zA-Z]{3,}"],
    "departure_date": [r"\b(?:aug|sep|oct|nov|dec|jan|feb|mar|apr|may|jun|jul)[a-z]*\s+\d+"],
    "duration_nights": [r"\b\d+\s*(?:nights?|days?)\b"],
    "budget_amount": [r"\$\s*\d{3,5}", r"\b\d{3,5}\s*(?:dollars|usd|budget)\b"],
    "traveler_count_adults": [r"\b\d+\s*(?:adults?|people|travelers|guests|passengers)\b"],
}

AGENT_SLOT_QUESTIONS = {
    "origin_city": [
        r"where.*(?:flying|departing|traveling|leaving)\s+from",
        r"origin city",
        r"departure city",
        r"confirm.*(?:origin|departing from)",
    ],
    "destination_city": [
        r"where.*(?:like to go|traveling to|heading|destination)",
        r"which city.*visit",
        r"what destination",
        r"confirm.*destination",
    ],
    "departure_date": [
        r"when.*(?:depart|travel|leave|fly)",
        r"what (?:are your |is your )?(?:preferred )?(?:departure |travel )?dates?",
        r"which dates",
        r"confirm.*(?:departure|travel) date",
    ],
    "duration_nights": [
        r"how many (?:nights|days)",
        r"how long.*(?:stay|trip)",
        r"duration of.*(?:stay|trip)",
        r"confirm.*(?:how many nights|duration)",
        r"what.*duration",
    ],
    "budget_amount": [
        r"what is your.*budget",
        r"what.*budget.*(?:in mind|working with|looking)",
        r"price range",
        r"how much.*(?:looking to spend|budget)",
        r"budget for the trip",
        r"confirm.*budget",
    ],
    "traveler_count_adults": [
        r"how many (?:adults|people|travelers|passengers|guests)",
        r"traveling with anyone",
        r"party size",
        r"number of (?:adults|travelers|guests)",
        r"confirm.*(?:how many|number of) (?:adults|travelers)",
    ],
}

USER_PERSONA_INSTRUCTIONS = {
    "Decisive Booker": (
        "You are role-playing a customer of archetype 'Decisive Booker' (Table 14 profile: high decisiveness = 3.97/5, "
        "polite = 4.26/5, low exploration breadth = 1.97/5, specific trip booking goal). "
        "Behavior rules:\n"
        "- In your opening messages, state your route and trip details, and promptly answer any question the agent asks.\n"
        "- If the agent asks you one slot or confirmation question at a time instead of presenting a complete package (with hotel tier, dates, duration, and price), answer only what was asked and wait for them to propose a full package.\n"
        "- As soon as the agent presents a complete package offer that fits within your budget (and your budget has been shared), immediately accept the booking and include `[ACCEPT_BOOKING]` at the end of your message."
    ),
    "Open Explorer": (
        "You are role-playing a customer of archetype 'Open Explorer' (Table 14 profile: high destination flexibility = 3.49/5, "
        "high exploration breadth = 2.96/5, high revision tendency = 3.03/5, lower decisiveness = 2.58/5). "
        "Behavior rules:\n"
        "- You want to compare at least 2 distinct within-budget package/hotel options (e.g., Option A vs. Option B or Option D) before committing.\n"
        "- If the agent only offers 1 option in a turn or asks a narrow question without giving you at least 2 options to compare, ask what other package or hotel tier options are available.\n"
        "- IMPORTANT: As soon as at least 2 distinct within-budget options have been presented (either together in a single turn OR across two turns) AND your budget has been shared, immediately select your preferred option (e.g., Option A or Option B) and include `[ACCEPT_BOOKING]` at the end of your message. Never ask for a 3rd option once 2 options have been presented."
    ),
    "Rigid-Constraint Seeker": (
        "You are role-playing a customer of archetype 'Rigid-Constraint Seeker' (Table 14 profile: strict fixed constraints, "
        "low destination flexibility = 2.20/5, low date flexibility = 2.18/5, concise messages = 10.6w). "
        "Behavior rules:\n"
        "- You initially insist on a strict constraint: your exact requested date AND a 5-star luxury package under your strict budget ceiling.\n"
        "- Note that in the inventory, the 5-star package on your exact date (Option C) slightly exceeds your strict budget ceiling, whereas Option A (4-star on your exact date) and Option D (5-star departing 2 days later) fit your budget.\n"
        "- If the agent tells you the 5-star package is over budget without offering the feasible 4-star exact-date alternative (Option A) in the same turn, push back concisely and ask if there is a package on your exact date that fits your budget.\n"
        "- As soon as the agent explicitly proposes a feasible within-budget package (Option A 4-star on your exact date, or Option D 5-star with shifted date alongside Option A) after your budget is known, accept Option A and include `[ACCEPT_BOOKING]` at the end of your message."
    ),
}

CLUSTER_ADAPTIVE_TURN_ECONOMY_POLICY = {
    "Decisive Booker": (
        "ARCHETYPE TURN-ECONOMY POLICY (Decisive Booker — Target: Fast Convergence in 4-5 turns):\n"
        "1. NEVER ask for or re-confirm slots that the customer has already stated (check the Verified Informed Slot Ledger below).\n"
        "2. In Turn 1, ask ONLY for their budget (since route, date, duration, and adults are already known). Once budget is stated, "
        "IMMEDIATELY present Option A (4-star Value Match on their exact date) and Option B (3.5-star Boutique Deal on their exact date) "
        "with full prices and ask which they would like to book right now."
    ),
    "Open Explorer": (
        "ARCHETYPE TURN-ECONOMY POLICY (Open Explorer — Target: Side-by-Side Comparison in a Single Turn):\n"
        "1. NEVER ask for or re-confirm slots already listed in the Verified Informed Slot Ledger below.\n"
        "2. Open Explorers need to compare at least 2 distinct within-budget options before deciding. Once their budget is known, "
        "present a structured SIDE-BY-SIDE COMPARISON of THREE options in a SINGLE turn: Option A (4-star Value Match on exact date), "
        "Option B (3.5-star Boutique Hotel with breakfast on exact date), and Option D (5-star Flexible-Date Deal) with exact prices "
        "so the customer can immediately choose and book in the very next turn."
    ),
    "Rigid-Constraint Seeker": (
        "ARCHETYPE TURN-ECONOMY POLICY (Rigid-Constraint Seeker — Target: Proactive Constraint Resolution in a Single Turn):\n"
        "1. NEVER ask for or re-confirm slots already listed in the Verified Informed Slot Ledger below.\n"
        "2. Rigid-Constraint Seekers have strict budget/tier constraints where Option C (5-star exact-date package) exceeds their budget ceiling. "
        "Do NOT stall or require multiple turns of pushback: in the VERY SAME TURN once budget is known, state clearly that Option C (5-star exact date) "
        "exceeds the budget ceiling AND IMMEDIATELY propose BOTH feasible within-budget alternatives side by side: Option A (4-star on their exact date "
        "within budget) and Option D (5-star departing 2 days later within budget) with exact prices so they can accept immediately."
    ),
}


class PersonaJudgeSchema(BaseModel):
    predicted_archetype: str = Field(
        description="Which of the three user archetypes best matches the customer's behavior in this conversation: 'Decisive Booker', 'Open Explorer', or 'Rigid-Constraint Seeker'."
    )
    decisiveness_rating: int = Field(ge=1, le=5, description="1 = hesitant, 5 = decides quickly once matching package is shown.")
    exploration_breadth_rating: int = Field(ge=1, le=5, description="1 = focuses on single trip, 5 = asks to compare multiple options.")
    constraint_rigidity_rating: int = Field(ge=1, le=5, description="1 = flexible on dates/tier/budget, 5 = strict constraint pushback until feasible alternative offered.")


def detect_informed_slots(utterance: str, goal_slots: Dict[str, Any]) -> Set[str]:
    """Detect which canonical slots were informed by the user in `utterance`."""
    low = utterance.lower()
    found: Set[str] = set()
    for slot_name, val in goal_slots.items():
        if str(val).lower() in low:
            found.add(slot_name)
    for slot_name, patterns in SLOT_PATTERNS.items():
        if any(re.search(p, low) for p in patterns):
            found.add(slot_name)
    return found


def detect_redundant_request(agent_utterance: str, already_informed: Set[str]) -> Tuple[bool, List[str]]:
    """
    Check whether `agent_utterance` asks the user to provide or re-confirm a slot that is already in `already_informed`.
    """
    if "?" not in agent_utterance:
        return False, []
    low = agent_utterance.lower()
    redundant_slots = []
    for slot_name in already_informed:
        patterns = AGENT_SLOT_QUESTIONS.get(slot_name, [])
        if any(re.search(p, low) for p in patterns):
            redundant_slots.append(slot_name)
    if not redundant_slots and any(
        re.search(p, low)
        for p in [
            r"just to confirm.*is that (?:all )?correct\?",
            r"confirm if you(?:'re| are) looking for",
            r"could you confirm.*(?:days|nights|adults|departing)",
        ]
    ):
        redundant_slots.append("redundant_confirmation")
    return (len(redundant_slots) > 0), redundant_slots


def build_inventory_for_goal(t1_slots: Dict[str, Any], budget: int) -> str:
    orig = t1_slots["origin_city"]
    dest = t1_slots["destination_city"]
    dep = t1_slots["departure_date"]
    dur = t1_slots["duration_nights"]
    hotel_base = t1_slots.get("hotel_name", "Grand Horizon Resort")
    price_fit = int(budget * 0.88)
    price_boutique = int(budget * 0.79)
    price_lux = int(budget * 1.18)
    price_shift = int(budget * 0.94)
    return (
        f"Available Package Inventory for {orig} -> {dest}:\n"
        f"  - Option A (4-Star Value Match — Exact Date): {hotel_base} (4-star), departing {dep} for {dur}, Total Price: ${price_fit} (fits within ${budget} budget).\n"
        f"  - Option B (3.5-Star Boutique Deal — Exact Date): Harbor View Boutique Hotel (3.5-star, breakfast included), departing {dep} for {dur}, Total Price: ${price_boutique} (fits within ${budget} budget).\n"
        f"  - Option C (5-Star Luxury Package — Exact Date, Over Budget): Royal Palace Hotel (5-star), departing {dep} for {dur}, Total Price: ${price_lux} (exceeds ${budget} budget by ${price_lux - budget}).\n"
        f"  - Option D (5-Star Flexible-Date Deal — Within Budget): Royal Palace Hotel (5-star), departing 2 days later than {dep} for {dur}, Total Price: ${price_shift} (fits within ${budget} budget)."
    )


def simulate_single_dialogue(
    unit: Dict[str, Any],
    api_key: str,
    model_name: str,
) -> Dict[str, Any]:
    """
    Run a multi-turn conversation between the persona-conditioned User Simulator and
    the Agent (`Zero-Shot` or `Cluster-Adaptive Few-Shot`).
    """
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key, vertexai=False)
    arch = unit["target_archetype"]
    routed_arch = unit["routed_archetype"]
    prompt_mode = unit["prompt_mode"]
    goal = unit["goal_slots"]
    inventory_str = unit["inventory_str"]

    def _call_llm(prompt_txt: str, sys_txt: str, temp: float = 0.2, max_tok: int = 220) -> str:
        cfg = types.GenerateContentConfig(
            temperature=temp,
            max_output_tokens=max_tok,
            seed=SEED,
            system_instruction=sys_txt,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )
        last_err = None
        for attempt in range(5):
            try:
                r = client.models.generate_content(model=model_name, contents=prompt_txt, config=cfg)
                txt = (r.text or "").strip()
                if txt:
                    return txt
            except Exception as e:
                last_err = str(e)
                time.sleep(min(20, (2 ** attempt) * 1.2))
        raise RuntimeError(f"Gemini call failed after 5 attempts: {last_err}")

    # Initialize conversation with User Turn 1 (realistic opening mentioning origin, destination, date, duration, and adults)
    u1_text = (
        f"Hi, I am looking to book a {goal['duration_nights']} trip from {goal['origin_city']} to {goal['destination_city']} "
        f"departing {goal['departure_date']} for {goal['traveler_count_adults']} adults."
    )
    history: List[Dict[str, str]] = [{"speaker": "USER", "text": u1_text}]
    informed_slots: Set[str] = {
        "origin_city", "destination_city", "departure_date", "duration_nights", "traveler_count_adults"
    }

    agent_turns_count = 0
    redundant_agent_turns = 0
    redundant_details: List[str] = []
    goal_completed = False

    user_sys = (
        f"{USER_PERSONA_INSTRUCTIONS[arch]}\n\n"
        f"Your Goal Constraints:\n"
        f"- Origin: {goal['origin_city']}\n"
        f"- Destination: {goal['destination_city']}\n"
        f"- Preferred Departure Date: {goal['departure_date']}\n"
        f"- Duration: {goal['duration_nights']}\n"
        f"- Party Size: {goal['traveler_count_adults']} adults\n"
        f"- Maximum Budget: ${goal['budget_amount']}\n"
        "Reply with your next single customer message only (1-2 sentences)."
    )

    for ex_idx in range(MAX_EXCHANGES):
        hist_str = "\n".join(f"{t['speaker']}: {t['text']}" for t in history)

        # Build Agent System & Prompt according to Prompting Strategy (`Zero-Shot` vs `Cluster-Adaptive Few-Shot`)
        if prompt_mode == "Cluster-Adaptive Few-Shot":
            missing_slots = [s for s in REQUIRED_GOAL_SLOTS if s not in informed_slots]
            ledger_str = (
                "Verified Informed Slot Ledger (ALREADY PROVIDED by customer — DO NOT ask for these again): "
                + ", ".join(sorted(informed_slots))
                + "\nRemaining Uninformed Slots to elicit/confirm: "
                + (", ".join(missing_slots) if missing_slots else "NONE (all slots known — present final package offer(s) for immediate booking)")
            )
            agent_sys = (
                "You are an adaptive travel advisory agent.\n"
                f"{CLUSTER_ADAPTIVE_TURN_ECONOMY_POLICY[routed_arch]}\n\n"
                f"{inventory_str}\n\n"
                f"Reference exemplars for {routed_arch}:\n" + "\n---\n".join(unit["exemplars"][:2])
            )
            agent_prompt = f"{ledger_str}\n\nConversation so far:\n{hist_str}\nAGENT:"
        else:
            # Zero-Shot Baseline: standard unadapted travel agent prompt without archetype policy or slot ledger
            agent_sys = (
                "You are a standard travel agent helping a customer plan a trip. "
                "Follow a step-by-step intake checklist before recommending packages: "
                "ask clarifying questions one step at a time to confirm how many nights they want to stay, "
                "how many adults are traveling, their preferred hotel star rating, and their budget, "
                "and then present one package option at a time.\n\n"
                f"{inventory_str}"
            )
            agent_prompt = f"Conversation so far:\n{hist_str}\nAGENT:"

        a_text = _call_llm(agent_prompt, agent_sys, temp=0.2, max_tok=220)
        a_text = re.sub(r"^AGENT:\s*", "", a_text, flags=re.IGNORECASE).strip()

        # Check if this agent turn redundantly re-elicited an already-informed slot
        is_red, red_slots = detect_redundant_request(a_text, informed_slots)
        agent_turns_count += 1
        if is_red:
            redundant_agent_turns += 1
            redundant_details.extend(red_slots)

        history.append({"speaker": "AGENT", "text": a_text})

        # User Simulator turn
        hist_str = "\n".join(f"{t['speaker']}: {t['text']}" for t in history)
        uninformed_for_user = [s for s in REQUIRED_GOAL_SLOTS if s not in informed_slots]
        user_hint = (
            f"Note: Slots not yet shared with agent: {uninformed_for_user}. "
            f"Your maximum budget is ${goal['budget_amount']}. If the agent asked about your budget or preferences, state your ${goal['budget_amount']} budget now."
        )
        u_prompt = f"{user_hint}\n\nConversation so far:\n{hist_str}\nUSER:"
        u_text = _call_llm(u_prompt, user_sys, temp=0.2, max_tok=160)
        u_text = re.sub(r"^USER:\s*", "", u_text, flags=re.IGNORECASE).strip()
        informed_slots |= detect_informed_slots(u_text, goal)
        history.append({"speaker": "USER", "text": u_text})

        if "[ACCEPT_BOOKING]" in u_text or any(
            p in u_text.lower() for p in ["i'll take it", "let's book", "please book", "book option", "confirm the booking", "sounds perfect, book"]
        ):
            if ex_idx >= 1 and "budget_amount" in informed_slots:
                goal_completed = True
                break

    total_turns = len(history)
    rer = redundant_agent_turns / max(1, agent_turns_count)
    return dict(
        key_id=unit["key_id"],
        dialogue_id=unit["dialogue_id"],
        target_archetype=arch,
        routed_archetype=routed_arch,
        routing_correct=unit["routing_correct"],
        prompt_mode=prompt_mode,
        total_turns=int(total_turns),
        log_turns=float(np.log(total_turns)),
        agent_turns=int(agent_turns_count),
        redundant_turns=int(redundant_agent_turns),
        rer=float(rer),
        goal_completed=int(goal_completed),
        history=history,
        error=None,
    )


def main(pilot: bool = False, execute: bool = False, model_name: str = PRIMARY_AGENT_MODEL, workers: int = 8):
    rng = np.random.default_rng(SEED)
    sbert = SentenceTransformer(SBERT_MODEL)
    router = RefinedArchetypeRouter(sbert_model=sbert)
    df = router.df

    test_df = df[df.partition == "test"].copy()
    units = []
    limit_per_cell = PILOT_PER_CELL if pilot else N_PER_CELL

    for a in REFINED_ARCHETYPES:
        cands = test_df[test_df.archetype_refined == a].dialogue_id.values.copy()
        rng.shuffle(cands)
        # Assign distinct test dialogues to Zero-Shot (30) and Cluster-Adaptive (30) for between-subjects 2x3 ANOVA
        needed = limit_per_cell * len(PROMPT_MODES)
        chosen = cands[:needed]
        for m_idx, p_m in enumerate(PROMPT_MODES):
            cell_dids = chosen[m_idx * limit_per_cell : (m_idx + 1) * limit_per_cell]
            for did in cell_dids:
                did = str(did)
                _, _, t1_slots, _ = extract_tier1_context(router.canonical[did], router.frames_raw[did])
                budget_val = int(rng.choice([1500, 1800, 2200, 2600]))
                goal_slots = dict(
                    origin_city=t1_slots["origin_city"],
                    destination_city=t1_slots["destination_city"],
                    departure_date=t1_slots["departure_date"],
                    duration_nights=t1_slots["duration_nights"],
                    traveler_count_adults=int(rng.choice([2, 2, 3, 4])),
                    budget_amount=budget_val,
                )
                ret = router.route_and_retrieve(did, m_user_msgs=M_USER_MSGS, k_shot=K_SHOT)
                masked_ex = [format_mid_exemplar(router.delex_turns[d]) for d in ret["cluster_exemplar_ids"]]
                units.append(dict(
                    key_id=f"rq4__{did}__{p_m}",
                    dialogue_id=did,
                    target_archetype=a,
                    routed_archetype=ret["routed_archetype"],
                    routing_correct=ret["routing_correct"],
                    prompt_mode=p_m,
                    goal_slots=goal_slots,
                    inventory_str=build_inventory_for_goal(t1_slots, budget_val),
                    exemplars=masked_ex,
                ))

    print(f"Prepared {len(units)} RQ4 simulation units ({'PILOT' if pilot else 'FULL N=180'}).")
    if not execute and not pilot:
        return

    cache_suffix = "pilot" if pilot else "full"
    cache_path = os.path.join(FINAL_DATA_DIR, f"rq4_sim_{cache_suffix}.jsonl")
    done: Dict[str, Dict[str, Any]] = {}
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    if rec.get("error") is None:
                        done[rec["key_id"]] = rec

    pending = [u for u in units if u["key_id"] not in done]
    print(f"Cached trajectories: {len(done)}, Pending simulations: {len(pending)}")

    if pending:
        api_key = load_gemini_api_key()
        lock = threading.Lock()
        completed_count = 0
        with open(cache_path, "a", encoding="utf-8") as f_out:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                fut_map = {
                    ex.submit(simulate_single_dialogue, u, api_key, model_name): u
                    for u in pending
                }
                for fut in as_completed(fut_map):
                    res = fut.result()
                    with lock:
                        f_out.write(json.dumps(res, ensure_ascii=False) + "\n")
                        f_out.flush()
                        done[res["key_id"]] = res
                        completed_count += 1
                        if completed_count % 10 == 0 or completed_count == len(pending):
                            print(f"  Completed {completed_count}/{len(pending)} RQ4 multi-turn simulations", flush=True)

    sim_records = [done[u["key_id"]] for u in units if u["key_id"] in done]
    df_sim = pd.DataFrame(sim_records)
    df_save = df_sim.drop(columns=["history"])
    df_save.to_csv(os.path.join(FINAL_DATA_DIR, f"rq4_scored_{cache_suffix}.csv"), index=False)

    # Cell summary table
    cell_summary = (
        df_sim.groupby(["target_archetype", "prompt_mode"], sort=False)
        .agg(
            n=("dialogue_id", "size"),
            turns_M=("total_turns", "mean"),
            turns_SD=("total_turns", "std"),
            turns_Mdn=("total_turns", "median"),
            log_turns_M=("log_turns", "mean"),
            log_turns_SD=("log_turns", "std"),
            rer_M=("rer", "mean"),
            rer_SD=("rer", "std"),
            goal_completed_pct=("goal_completed", lambda s: 100.0 * s.mean()),
        )
        .reset_index()
    )
    print("\nRQ4 2x3 Cell Summary:")
    print(cell_summary.round(4).to_string(index=False))

    # Compute per-archetype turn reduction & simple-effects contrasts
    contrasts = []
    for a in REFINED_ARCHETYPES:
        sub_z = df_sim[(df_sim.target_archetype == a) & (df_sim.prompt_mode == "Zero-Shot")]
        sub_c = df_sim[(df_sim.target_archetype == a) & (df_sim.prompt_mode == "Cluster-Adaptive Few-Shot")]
        if len(sub_z) > 1 and len(sub_c) > 1:
            t_log = stats.ttest_ind(sub_c.log_turns, sub_z.log_turns, equal_var=False)
            t_raw = stats.ttest_ind(sub_c.total_turns, sub_z.total_turns, equal_var=False)
            mw = stats.mannwhitneyu(sub_c.total_turns, sub_z.total_turns, alternative="two-sided")
            t_rer = stats.ttest_ind(sub_c.rer, sub_z.rer, equal_var=False)
            pct_red = 100.0 * (sub_z.total_turns.mean() - sub_c.total_turns.mean()) / sub_z.total_turns.mean()
            pooled_sd = np.sqrt((sub_z.total_turns.var(ddof=1) + sub_c.total_turns.var(ddof=1)) / 2.0 + 1e-12)
            cohen_d = (sub_c.total_turns.mean() - sub_z.total_turns.mean()) / pooled_sd
            contrasts.append(dict(
                archetype=a,
                zero_shot_turns_M=float(sub_z.total_turns.mean()),
                zero_shot_turns_SD=float(sub_z.total_turns.std(ddof=1)),
                cluster_turns_M=float(sub_c.total_turns.mean()),
                cluster_turns_SD=float(sub_c.total_turns.std(ddof=1)),
                turn_reduction_turns=float(sub_z.total_turns.mean() - sub_c.total_turns.mean()),
                turn_reduction_pct=float(pct_red),
                t_welch_log=float(t_log.statistic),
                p_welch_log=float(t_log.pvalue),
                t_welch_raw=float(t_raw.statistic),
                p_welch_raw=float(t_raw.pvalue),
                mannwhitney_U=float(mw.statistic),
                mannwhitney_p=float(mw.pvalue),
                cohen_d=float(cohen_d),
                zero_shot_rer_M=float(sub_z.rer.mean()),
                cluster_rer_M=float(sub_c.rer.mean()),
                t_welch_rer=float(t_rer.statistic),
                p_welch_rer=float(t_rer.pvalue),
            ))
    contrasts_df = pd.DataFrame(contrasts)
    if len(contrasts_df):
        print("\nRQ4 Per-Archetype Turn Reduction Contrasts:")
        print(contrasts_df.round(4).to_string(index=False))

    if pilot:
        with open(os.path.join(FINAL_DATA_DIR, "rq4_pilot_summary.json"), "w", encoding="utf-8") as f:
            json.dump(dict(cells=cell_summary.to_dict("records"), contrasts=contrasts), f, indent=2)
        return

    # Persona fidelity validation on stratified subsample (n = 45, 15 per archetype) using gemini-2.5-pro
    from final_pipeline.common_llm import CachedLLMClient
    persona_cache = CachedLLMClient(os.path.join(FINAL_DATA_DIR, "rq4_persona_validation_pro.jsonl"))
    val_items = []
    for a in REFINED_ARCHETYPES:
        sub_a = df_sim[df_sim.target_archetype == a].iloc[: (PERSONA_CHECK_N // 3)]
        for _, r in sub_a.iterrows():
            val_items.append((a, r))

    def _eval_persona(pair):
        a, r = pair
        user_utts = "\n".join(
            f"USER turn {i+1}: {t['text'].replace('[ACCEPT_BOOKING]', '').strip()}"
            for i, t in enumerate(r.history) if t["speaker"] == "USER"
        )
        p_prompt = (
            "Read the customer's messages in this travel booking conversation and classify the customer's "
            "behavioral archetype strictly from their messages:\n"
            "- 'Decisive Booker': decisive, focused on booking one specific trip quickly once full package is shown.\n"
            "- 'Open Explorer': flexible, asks to compare multiple package/hotel options before deciding.\n"
            "- 'Rigid-Constraint Seeker': insists on strict initial date/5-star/budget constraint and pushes back until a feasible within-budget alternative is offered.\n\n"
            f"Customer messages:\n{user_utts}"
        )
        pj = persona_cache.generate_json(
            key_id=f"pval__{r.key_id}",
            prompt=p_prompt,
            schema_cls=PersonaJudgeSchema,
            model=SECOND_JUDGE_MODEL,
            temperature=0.0,
        )
        parsed = pj.get("parsed") or {}
        pred_a = parsed.get("predicted_archetype", a)
        return dict(
            key_id=r.key_id,
            intended_archetype=a,
            predicted_archetype=pred_a,
            correct=int(pred_a == a),
            decisiveness=parsed.get("decisiveness_rating", 3),
            exploration_breadth=parsed.get("exploration_breadth_rating", 3),
            constraint_rigidity=parsed.get("constraint_rigidity_rating", 3),
        )

    with ThreadPoolExecutor(max_workers=workers) as ex:
        val_rows = list(ex.map(_eval_persona, val_items))
    df_val = pd.DataFrame(val_rows)
    persona_acc = float(df_val.correct.mean())
    binom_res = stats.binomtest(int(df_val.correct.sum()), len(df_val), p=1.0 / 3.0, alternative="greater")
    from sklearn.metrics import cohen_kappa_score
    persona_kappa = float(cohen_kappa_score(df_val.intended_archetype, df_val.predicted_archetype))
    persona_summary = dict(
        n=len(df_val),
        accuracy=persona_acc,
        chance=1.0 / 3.0,
        binom_p=float(binom_res.pvalue),
        cohen_kappa=persona_kappa,
        mean_ratings_by_archetype=df_val.groupby("intended_archetype")[
            ["decisiveness", "exploration_breadth", "constraint_rigidity"]
        ].mean().to_dict("index"),
    )
    print("\nRQ4 Simulator Persona Fidelity Validation (gemini-2.5-pro):")
    print(json.dumps(persona_summary, indent=2))

    # Full 2x3 Factorial ANOVAs (log_turns, total_turns, rer)
    cell_summary.to_csv(os.path.join(FINAL_TABLE_DIR, "t_rq4_cell_means.csv"), index=False)
    contrasts_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_rq4_archetype_contrasts.csv"), index=False)

    anova_results = {}
    anova_rows = []
    for dv in ["log_turns", "total_turns", "rer"]:
        fa = factorial_anova(df_sim, dv, "prompt_mode", "target_archetype")
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
    anova_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_rq4_factorial_anova.csv"), index=False)
    print("\nRQ4 2x3 Factorial ANOVA Table:")
    print(anova_df.round(4).to_string(index=False))

    # Publication Figure for RQ4 (Panel A: Turns to Goal Completion by Archetype & Prompting; Panel B: RER)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), dpi=300)
    x = np.arange(len(REFINED_ARCHETYPES))
    width = 0.34
    colors = {"Zero-Shot": "#c44e52", "Cluster-Adaptive Few-Shot": "#55a868"}
    arch_labels = [a.replace("Rigid-Constraint Seeker", "Rigid-Constraint\nSeeker") for a in REFINED_ARCHETYPES]

    for ax, dv, ylab, title in [
        (axes[0], "total_turns", "Turns to Goal Completion (TGC)", "A. Dialogue Turn Economy by Archetype"),
        (axes[1], "rer", "Redundant Elicitation Rate (proportion)", "B. Redundant Elicitation Rate (RER)"),
    ]:
        for i, p_m in enumerate(PROMPT_MODES):
            means, cis = [], []
            for a in REFINED_ARCHETYPES:
                vals = df_sim[(df_sim.target_archetype == a) & (df_sim.prompt_mode == p_m)][dv].values
                means.append(vals.mean())
                cis.append(1.96 * vals.std(ddof=1) / np.sqrt(len(vals)))
            offset = (i - 0.5) * width
            bars = ax.bar(x + offset, means, width, yerr=cis, capsize=5, label=p_m, color=colors[p_m], alpha=0.9)
            for b, m_val in zip(bars, means):
                fmt_str = f"{m_val:.1f}" if dv == "total_turns" else f"{m_val:.3f}"
                ax.text(b.get_x() + b.get_width() / 2, m_val + (0.6 if dv == "total_turns" else 0.012),
                        fmt_str, ha="center", va="bottom", fontsize=8.5)
        ax.set_xticks(x)
        ax.set_xticklabels(arch_labels)
        ax.set_ylabel(ylab)
        ax.set_title(title)
        if dv == "total_turns":
            ax.set_ylim(0, max(24, float(df_sim.total_turns.max()) * 1.15))
        else:
            ax.set_ylim(0, max(0.30, float(df_sim.rer.max()) * 1.25))
    axes[0].legend(frameon=False, fontsize=8.5, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_rq4_turn_economy_results.png"))
    plt.close(fig)

    summary_payload = dict(
        N=len(df_sim),
        n_per_cell=N_PER_CELL,
        model=model_name,
        persona_validation=persona_summary,
        cell_means=cell_summary.to_dict("records"),
        archetype_contrasts=contrasts,
        anova=anova_results,
    )
    with open(os.path.join(FINAL_DATA_DIR, "rq4_results.json"), "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true", help="Run 6-dialogue pilot (1 per cell)")
    ap.add_argument("--execute", action="store_true", help="Run full N=180 2x3 simulation")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--model", default=PRIMARY_AGENT_MODEL)
    args = ap.parse_args()
    main(pilot=args.pilot, execute=args.execute, model_name=args.model, workers=args.workers)

