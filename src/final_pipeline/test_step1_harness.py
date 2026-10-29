"""
Step 1 verification & unit-test suite for `src/final_pipeline/`.
Runs completely offline inside the workspace sandbox (0 API calls) and saves the
held-out hybrid routing diagnostics table (`outputs/final/tables/t_rq1_hybrid_routing_diagnostics.csv`).
"""

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
if os.path.join(ROOT, "src") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "src"))

from final_pipeline.common_llm import FINAL_DATA_DIR, FINAL_TABLE_DIR  # noqa: E402
from final_pipeline.metrics import (  # noqa: E402
    compute_exemplar_leakage,
    compute_slot_f1,
    dual_judge_reliability,
    factorial_anova,
    holm_pairwise,
    rm_anova,
)
from final_pipeline.routing import REFINED_ARCHETYPES, RefinedArchetypeRouter  # noqa: E402
from rule_engine import DeclarativeRuleEngine  # noqa: E402


def main():
    print("1. Testing RefinedArchetypeRouter and FAISS sub-indices...")
    router = RefinedArchetypeRouter()
    diag_df = router.routing_diagnostics_table()
    diag_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_rq1_hybrid_routing_diagnostics.csv"), index=False)
    print(diag_df.round(4).to_string(index=False))

    assert (diag_df["routing_kappa"] > 0.35).all(), "Expected held-out routing kappa > .35 at all M >= 3"
    assert diag_df.loc[diag_df.user_messages_m == 5, "routing_accuracy"].iloc[0] > 0.68

    # Test retrieval on a held-out dialogue
    test_did = router.df[router.df.partition == "test"].dialogue_id.iloc[0]
    ret = router.route_and_retrieve(test_did, m_user_msgs=5, k_shot=3)
    assert ret["routed_archetype"] in REFINED_ARCHETYPES
    assert len(ret["cluster_exemplar_ids"]) == 3
    assert test_did not in ret["cluster_exemplar_ids"]
    print(f"Sample retrieval on {test_did}: target={ret['target_archetype']}, routed={ret['routed_archetype']}, "
          f"cluster_sim={ret['cluster_sim_mean']:.3f}")

    print("\n2. Testing compute_slot_f1 and compute_exemplar_leakage...")
    s_res = compute_slot_f1(
        "I have a 5-star package to Paris departing August 12 for $1,800 for 2 adults.",
        expected_slots={"destination": "Paris", "tier": "5-star", "date": "August 12", "price": "1800"},
    )
    assert abs(s_res["f1"] - 1.0) < 1e-6, f"Unexpected slot F1: {s_res}"

    l_res = compute_exemplar_leakage(
        "We can fly you from Gotham to Atlantis for $1200, or check the Cancun resort from $950.",
        exemplar_entities=["Cancun", "950", "Tokyo"],
        dialogue_entities=["Gotham", "Atlantis", "1200"],
    )
    assert l_res["has_leakage"] is True and "cancun" in l_res["leaked_entities"]
    print(f"Slot F1 check: {s_res}, Leakage check: {l_res}")

    print("\n3. Testing statistical functions (RM-ANOVA, Holm, 2x2 Factorial ANOVA, Dual-Judge kappa)...")
    rng = np.random.default_rng(42)
    Y = np.column_stack([rng.normal(0.5, 0.1, 33), rng.normal(0.6, 0.1, 33), rng.normal(0.75, 0.1, 33)])
    rm = rm_anova(Y)
    hp = holm_pairwise(Y, ["Zero-Shot", "Static", "Cluster-Adaptive"])
    assert rm["p_gg"] < 0.001 and (hp["p_holm"] < 0.05).all()

    df_fac = pd.DataFrame({
        "rules": np.repeat(["Off", "Active"], 72),
        "prompt": np.tile(np.repeat(["Zero-Shot", "Cluster-Adaptive"], 36), 2),
        "score": np.concatenate([
            rng.normal(0.65, 0.08, 36),
            rng.normal(0.72, 0.08, 36),
            rng.normal(0.92, 0.05, 36),
            rng.normal(0.96, 0.04, 36),
        ]),
    })
    fa = factorial_anova(df_fac, "score", "rules", "prompt")
    assert fa["effects"]["rules"]["p_hc3"] < 0.001

    rel = dual_judge_reliability([1, 1, 0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 0, 1, 1, 1])
    assert rel["cohen_kappa"] > 0.6

    print("\n4. Testing DeclarativeRuleEngine (14 boundary cases)...")
    engine = DeclarativeRuleEngine(os.path.join(ROOT, "rules", "rules_enterprise.yaml"))
    ok, viol = engine.evaluate_booking_state(
        dict(is_international=True, departure_lead_days=10, passport_expiry_months=4,
             traveler_count_adults=10, package_type="FIT", discount_applied_percentage=20.0, budget_amount=400)
    )
    assert not ok and len(viol) == 5

    summary_out = dict(
        step1_tests_passed=True,
        routing_diagnostics=diag_df.to_dict("records"),
    )
    with open(os.path.join(FINAL_DATA_DIR, "step1_harness_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary_out, f, indent=2)
    print("\nStep 1 harness verification complete: ALL TESTS PASSED.")


if __name__ == "__main__":
    main()

