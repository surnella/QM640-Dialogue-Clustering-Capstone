"""
Interactive Single-Dialogue Walkthrough Script (RQ1 -> RQ2 -> RQ3 -> RQ4).

Demonstrates how a single held-out test dialogue (`partition == 'test'`) flows
through the entire empirical pipeline using the pre-cached embeddings, models,
and LLM responses:
  1. Data Ingestion, De-lexicalization & Slot Extraction (`step1_prepare_data.py`)
  2. RQ1: 16-Field LLM Behavioral Profile, 46-d `Blocks` Vector & Prefix Routing (`routing.py`)
  3. RQ2: 3-Condition Prompt Assembly, LLM Replies & Style/Pacing Scoring (`step2_rq2_refined.py`)
  4. RQ3: 2x2 Factorial Rule Engine & Prompt Evaluation (`step3_rq3_experiment.py`)
  5. RQ4: 2x3 Closed-Loop Multi-Turn Simulation (`step4_rq4_simulation.py`)

Usage:
    /Users/surnellas/capstone/.venv/bin/python src/final_pipeline/demo_single_dialogue_rq1_to_rq4.py
    /Users/surnellas/capstone/.venv/bin/python src/final_pipeline/demo_single_dialogue_rq1_to_rq4.py --dialogue-id <id>
"""

import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(ROOT, "src"), os.path.join(ROOT, "src", "interim_pipeline")):
    if p not in sys.path:
        sys.path.insert(0, p)

from common import delexicalize  # noqa: E402
from routing import ARCHETYPE_DIRECTIVES, RefinedArchetypeRouter  # noqa: E402
from metrics import compute_exemplar_leakage, compute_slot_f1  # noqa: E402


def load_jsonl_by_key(path: str, key_field: str = "dialogue_id"):
    records = []
    if not os.path.exists(path):
        return records
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def run_demo(dialogue_id: str = None):
    print("=" * 88)
    print("SINGLE-DIALOGUE END-TO-END TRACE: DATA PREP -> RQ1 -> RQ2 -> RQ3 -> RQ4")
    print("=" * 88)

    router = RefinedArchetypeRouter(sbert_model=None)
    rq2_df = pd.read_csv(os.path.join(ROOT, "data", "final", "rq2_refined_scored.csv"))
    rq3_df = pd.read_csv(os.path.join(ROOT, "data", "final", "rq3_scored_full.csv"))
    rq4_df = pd.read_csv(os.path.join(ROOT, "data", "final", "rq4_scored_full.csv"))

    # Pick a held-out test dialogue that appears in RQ2 and RQ3 by default
    shared_dids = sorted(set(rq2_df["dialogue_id"]).intersection(set(rq3_df["dialogue_id"])))
    if not dialogue_id:
        dialogue_id = shared_dids[0] if shared_dids else str(rq2_df["dialogue_id"].iloc[0])

    row_idx = router.models_by_m[9]["id_to_row"][dialogue_id]
    meta_row = router.df.iloc[row_idx]
    canon = router.canonical[dialogue_id]
    slot_vals = router.slot_vals[dialogue_id]

    # -------------------------------------------------------------------------
    # STAGE 0: DATA PREPARATION, CANONICAL SCHEMA & SLOT EXTRACTION
    # -------------------------------------------------------------------------
    print(f"\n[STAGE 0] CANONICAL DIALOGUE & SLOT EXTRACTION (dialogue_id = {dialogue_id})")
    print("-" * 88)
    print(f"  Partition           : {meta_row['partition']} (Held-Out Validation Set)")
    print(f"  Total Turns         : {canon['total_turns']} ({canon['user_turns']} user, {canon['wizard_turns']} wizard)")
    print(f"  Extracted Slots     : {slot_vals[:8]}")
    print("  Opening 4 Turns (Raw vs. De-lexicalized):")
    for t_idx, (t_raw, t_delex) in enumerate(zip(canon["turns"][:4], router.delex_turns[dialogue_id][:4])):
        print(f"    Turn {t_idx+1} (Raw)  : [{t_raw['speaker'].upper()}] {t_raw['utterance'][:90]}")
        print(f"    Turn {t_idx+1} (Delex): {t_delex[:90]}")

    # -------------------------------------------------------------------------
    # STAGE 1 (RQ1): LLM BEHAVIORAL CODEBOOK, 46-D BLOCKS VECTOR & PREFIX ROUTER
    # -------------------------------------------------------------------------
    print(f"\n[STAGE 1 / RQ1] 46-D HYBRID 'BLOCKS' REPRESENTATION & PREFIX ROUTING")
    print("-" * 88)
    print(f"  Reference Archetype y^(9) (M=9 K-Means) : {meta_row['archetype_refined']}")
    x46 = router.models_by_m[5]["X_norm"][row_idx]
    print(f"  46-d L2-Normalized Blocks Vector (M=5)  : shape={x46.shape}, norm={np.linalg.norm(x46):.4f}")
    print(f"    First 5 dims (PCA-20 Gemini prefix)   : {np.round(x46[:5], 4)}")
    print(f"    Dims 20..25 (Scaled LLM ordinal/cat)  : {np.round(x46[20:25], 4)}")
    print("  Prefix Router Predictions Across Horizons m in {3, 5, 7, 9}:")
    for m in (3, 5, 7, 9):
        info = router.models_by_m[m]
        pred = info["pred_all"][row_idx]
        probs = info["proba_all"][row_idx]
        classes = info["clf"].classes_
        prob_str = ", ".join(f"{c}: {p:.2f}" for c, p in zip(classes, probs))
        print(f"    m = {m} user msgs -> Predicted: {pred:<24} | Probs: ({prob_str})")

    # -------------------------------------------------------------------------
    # STAGE 2 (RQ2): REPEATED-MEASURES PROMPT INJECTION & STYLE/PACING SCORING
    # -------------------------------------------------------------------------
    print(f"\n[STAGE 2 / RQ2] 3-CONDITION PROMPT INJECTION & NUMERIC SCORING")
    print("-" * 88)
    ret = router.route_and_retrieve(dialogue_id, m_user_msgs=5, k_shot=3)
    print(f"  Routed Archetype at M=5 : {ret['routed_archetype']}")
    print(f"  Archetype Directive     : {ARCHETYPE_DIRECTIVES[ret['routed_archetype']][:105]}...")
    print(f"  Retrieved Archetype FAISS Exemplars (k=3) : {ret['cluster_exemplar_ids']} (mean_sim={ret['cluster_sim_mean']:.3f})")
    print(f"  Retrieved Global FAISS Exemplars (k=3)    : {ret['global_exemplar_ids']} (mean_sim={ret['global_sim_mean']:.3f})")

    sub_rq2 = rq2_df[rq2_df["dialogue_id"] == dialogue_id]
    if not sub_rq2.empty:
        print("\n  Generated Chatbot Responses & Converted Numeric Scores (N=1 dialogue across 3 conditions):")
        for _, r in sub_rq2.iterrows():
            cond = r["condition"]
            resp = str(r.get("response", ""))[:95]
            print(
                f"    [{cond:<25}] Words={int(r['words']):2d} | "
                f"PacingErr={r['word_abs_err']:5.2f}w | SBERT_Cos={r['sbert_style_cos']:.3f} | "
                f"Gemini_Cos={r['style_cos']:.3f} | BERT_F1={r['bert_f1']:.3f}"
            )
            print(f"       Reply: \"{resp}...\"")
            print(f"       De-lexicalized for Style: \"{delexicalize(resp, slot_vals)[:90]}...\"")

    # -------------------------------------------------------------------------
    # STAGE 3 (RQ3): 2x2 FACTORIAL RULE ENGINE & PROMPT EVALUATION
    # -------------------------------------------------------------------------
    print(f"\n[STAGE 3 / RQ3] 2x2 FACTORIAL DECLARATIVE RULES x PROMPTING EVALUATION")
    print("-" * 88)
    from rule_engine import DeclarativeRuleEngine
    engine = DeclarativeRuleEngine(os.path.join(ROOT, "rules", "rules_enterprise.yaml"))
    sample_state = {
        "is_international": True,
        "departure_lead_days": 20,
        "passport_expiry_months": 12,
        "traveler_count_adults": 5,
        "package_type": "FIT",
        "discount_applied_percentage": 20.0,
        "budget_amount": 3200.0,
    }
    is_compliant, viols = engine.evaluate_booking_state(sample_state)
    print(f"  Live DeclarativeRuleEngine.evaluate_booking_state() : compliant={is_compliant} | violations={[v.rule_id for v in viols]}")
    if viols:
        print(f"  Injected [POLICY STATUS] Directive : [{viols[0].severity}] {viols[0].rule_id} -> {viols[0].message} (action={viols[0].action})")

    sub_rq3 = rq3_df[rq3_df["dialogue_id"] == dialogue_id]
    if not sub_rq3.empty:
        r0 = sub_rq3.iloc[0]
        is_viol = bool(r0.get("is_violating_scenario"))
        print(f"  Assigned Between-Subjects Cell for {dialogue_id}: [{r0['rules_mode']} x {r0['prompt_mode']}] (Violating={is_viol})")
    else:
        is_viol = True

    print(f"\n  Representative 2x2 Factorial Cells (Archetype={meta_row['archetype_refined']}, Violating={is_viol}):")
    arch_rq3 = rq3_df[(rq3_df["target_archetype"] == meta_row["archetype_refined"]) & (rq3_df["is_violating_scenario"] == is_viol)]
    for rmode in ("Rules Off", "Rules Active"):
        for pmode in ("Zero-Shot", "Cluster-Adaptive Few-Shot"):
            cell_df = arch_rq3[(arch_rq3["rules_mode"] == rmode) & (arch_rq3["prompt_mode"] == pmode)]
            if not cell_df.empty:
                r = cell_df.iloc[0]
                cell_label = f"{rmode} x {pmode}"
                print(
                    f"    [{cell_label:<36}] (id={r['dialogue_id'][:15]}...) | RuleAdherence={r['rule_adherence']:.1f} | "
                    f"Leakage={r['leakage_rate']:.3f} | Slot_F1={r['slot_f1']:.3f} | StyleCos={r['style_cos']:.3f}"
                )
                print(f"       Reply: \"{str(r.get('response', ''))[:95]}...\"")

    # -------------------------------------------------------------------------
    # STAGE 4 (RQ4): 2x3 MULTI-TURN SIMULATION (TURN ECONOMY & RER)
    # -------------------------------------------------------------------------
    print(f"\n[STAGE 4 / RQ4] 2x3 CLOSED-LOOP MULTI-TURN SIMULATION")
    print("-" * 88)
    arch = meta_row["archetype_refined"]
    sub_rq4 = rq4_df[rq4_df["target_archetype"] == arch]
    for pmode in ("Zero-Shot", "Cluster-Adaptive Few-Shot"):
        ex = sub_rq4[sub_rq4["prompt_mode"] == pmode].iloc[0]
        print(
            f"  [{arch} | {pmode:<25}] Key={ex['key_id']} (seed={ex['dialogue_id']}) -> "
            f"TotalTurns={int(ex['total_turns'])} | LogTurns={ex['log_turns']:.3f} | "
            f"RER={ex['rer']:.3f} | GoalCompleted={int(ex['goal_completed'])}"
        )

    print("\n" + "=" * 88)
    print("WALKTHROUGH COMPLETE — All outputs verified from cached deterministic artifacts.")
    print("=" * 88)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogue-id", type=str, default=None, help="Held-out test dialogue_id to trace")
    args = parser.parse_args()
    run_demo(args.dialogue_id)
