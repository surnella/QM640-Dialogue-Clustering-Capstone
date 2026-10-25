"""
Step 4 - Groundwork for RQ3 (rules vs. prompting ablation) and RQ4 (turn economy).

RQ3 groundwork
  * Deterministic verification of the declarative rule engine (boundary test cases).
  * Corpus audit: how often Frames dialogue states trigger the rules that the public
    annotations can support, and which policy slots are entirely missing.
RQ4 groundwork
  * Human (Wizard-of-Oz) baseline of turn economy and a redundant-elicitation proxy
    by archetype, computed from Frames act annotations.
  * Observed dispersion of turns, compared with the planning value used in the synopsis.
"""

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from common import FIG_DIR, ROOT, TABLE_DIR, WORK_DIR, load_frames_raw

sys.path.insert(0, os.path.join(ROOT, "src"))
from rule_engine import DeclarativeRuleEngine  # noqa: E402

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                     "font.size": 11})


def to_float(v):
    try:
        return float(str(v).replace(",", "").replace("$", ""))
    except Exception:
        return None


def main():
    engine = DeclarativeRuleEngine(os.path.join(ROOT, "rules", "rules_enterprise.yaml"))
    rules = pd.DataFrame([dict(rule_id=r["id"], name=r["name"], condition=r["condition"], action=r["action"],
                               severity=r["severity"]) for r in engine.rules])
    rules.to_csv(os.path.join(TABLE_DIR, "t_rq3_rules.csv"), index=False)

    # Boundary test cases: (state, rule expected to fire or None)
    base = dict(is_international=True, departure_lead_days=30, passport_expiry_months=12,
                traveler_count_adults=2, package_type="FIT", discount_applied_percentage=0.0, budget_amount=2000)
    cases = [({}, None),
             ({"departure_lead_days": 14}, "RULE_VISA_WINDOW"), ({"departure_lead_days": 15}, None),
             ({"departure_lead_days": 5, "is_international": False}, None),
             ({"passport_expiry_months": 5}, "RULE_PASSPORT_VALIDITY"), ({"passport_expiry_months": 6}, None),
             ({"traveler_count_adults": 9}, "RULE_PAX_CAPACITY"), ({"traveler_count_adults": 8}, None),
             ({"traveler_count_adults": 12, "package_type": "Group"}, None),
             ({"discount_applied_percentage": 15.5}, "RULE_DISCOUNT_THRESHOLD"),
             ({"discount_applied_percentage": 15.0}, None),
             ({"budget_amount": 499}, "RULE_BUDGET_MINIMUM"), ({"budget_amount": 500}, None),
             ({"budget_amount": 300, "is_international": False}, None)]
    trows = []
    for delta, expected in cases:
        st = dict(base, **delta)
        ok, viol = engine.evaluate_booking_state(st)
        fired = sorted(v.rule_id for v in viol)
        passed = (fired == ([expected] if expected else []))
        trows.append(dict(case=json.dumps(delta), expected=expected or "none", fired=",".join(fired) or "none",
                          passed=passed))
    dtests = pd.DataFrame(trows)
    dtests.to_csv(os.path.join(TABLE_DIR, "t_rq3_rule_tests.csv"), index=False)

    # Corpus audit on Frames (observed user-informed values only)
    frames_raw = load_frames_raw()
    arch = pd.read_csv(os.path.join(WORK_DIR, "frames_archetypes.csv"))
    audit = []
    for did in arch.dialogue_id:
        adults, budgets = [], []
        for t in frames_raw[did]["turns"]:
            if t["author"] != "user":
                continue
            for a in t["labels"]["acts"]:
                for arg in a.get("args", []):
                    if arg.get("key") == "n_adults":
                        v = to_float(arg.get("val"));  adults.append(v) if v is not None else None
                    if arg.get("key") == "budget":
                        v = to_float(arg.get("val"));  budgets.append(v) if v is not None else None
        st = dict(is_international=True, traveler_count_adults=max(adults) if adults else None,
                  budget_amount=min(budgets) if budgets else None, package_type="FIT",
                  departure_lead_days=None, passport_expiry_months=None, discount_applied_percentage=None)
        _, viol = engine.evaluate_booking_state(st)
        ids = {v.rule_id for v in viol}
        audit.append(dict(dialogue_id=did, has_adults=bool(adults), has_budget=bool(budgets),
                          pax_trigger="RULE_PAX_CAPACITY" in ids, budget_trigger="RULE_BUDGET_MINIMUM" in ids))
    da = pd.DataFrame(audit)
    n = len(da)
    corpus_audit = pd.DataFrame([
        dict(rule="RULE_PAX_CAPACITY", required_slot="traveler_count_adults", slot_observed_pct=100 * da.has_adults.mean(),
             trigger_n=int(da.pax_trigger.sum()), trigger_pct=100 * da.pax_trigger.mean()),
        dict(rule="RULE_BUDGET_MINIMUM", required_slot="budget_amount", slot_observed_pct=100 * da.has_budget.mean(),
             trigger_n=int(da.budget_trigger.sum()), trigger_pct=100 * da.budget_trigger.mean()),
        dict(rule="RULE_VISA_WINDOW", required_slot="visa_processing_window_days", slot_observed_pct=0.0,
             trigger_n=0, trigger_pct=0.0),
        dict(rule="RULE_PASSPORT_VALIDITY", required_slot="passport_expiry_months", slot_observed_pct=0.0,
             trigger_n=0, trigger_pct=0.0),
        dict(rule="RULE_DISCOUNT_THRESHOLD", required_slot="discount_applied_percentage", slot_observed_pct=0.0,
             trigger_n=0, trigger_pct=0.0)])
    corpus_audit.to_csv(os.path.join(TABLE_DIR, "t_rq3_corpus_audit.csv"), index=False)

    # RQ4 human baseline by archetype
    names = json.load(open(os.path.join(WORK_DIR, "archetypes.json")))
    order = [names[k] for k in sorted(names, key=int)]
    base_tab = arch.groupby("archetype").agg(n=("dialogue_id", "size"), turns_M=("total_turns", "mean"),
                                             turns_SD=("total_turns", "std"), rer_M=("rer_proxy", "mean"),
                                             rer_SD=("rer_proxy", "std"),
                                             req_turns_M=("agent_request_turns", "mean")).reindex(order).reset_index()
    base_tab.to_csv(os.path.join(TABLE_DIR, "t_rq4_baseline.csv"), index=False)
    g_turns = [np.log(arch.loc[arch.archetype == a, "total_turns"]) for a in order]
    g_rer = [arch.loc[arch.archetype == a, "rer_proxy"].dropna() for a in order]
    lev = stats.levene(*g_turns, center="median")
    kw_turns, kw_rer = stats.kruskal(*g_turns), stats.kruskal(*g_rer)
    f_turns = stats.f_oneway(*g_turns)
    pooled_sd = float(np.sqrt(np.average(base_tab.turns_SD ** 2, weights=base_tab.n - 1)))

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=300)
    lab = [a.replace(" ", "\n") for a in order]
    axes[0].boxplot([arch.loc[arch.archetype == a, "total_turns"] for a in order], labels=lab, showmeans=True)
    axes[0].set_ylabel("Turns to dialogue end (human baseline)")
    axes[0].set_title("A. Turn economy by archetype")
    ci = 1.96 * base_tab.rer_SD / np.sqrt(base_tab.n)
    axes[1].bar(range(3), base_tab.rer_M, yerr=ci, capsize=6, color=["#4c72b0", "#dd8452", "#55a868"])
    axes[1].set_ylim(bottom=0)
    axes[1].set_xticks(range(3)); axes[1].set_xticklabels(lab)
    axes[1].set_ylabel("Redundant elicitation proxy (share of agent turns)")
    axes[1].set_title("B. Redundant elicitation by archetype")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_rq4_baseline.png"))
    plt.close(fig)

    summary = dict(rule_tests_passed=int(dtests.passed.sum()), rule_tests_total=len(dtests),
                   frames_n=n, levene_log_turns=dict(W=float(lev.statistic), p=float(lev.pvalue)),
                   anova_log_turns=dict(F=float(f_turns.statistic), p=float(f_turns.pvalue)),
                   kruskal_turns=dict(H=float(kw_turns.statistic), p=float(kw_turns.pvalue)),
                   kruskal_rer=dict(H=float(kw_rer.statistic), p=float(kw_rer.pvalue)),
                   pooled_turns_sd=pooled_sd, overall_turns_sd=float(arch.total_turns.std()),
                   overall_rer_M=float(arch.rer_proxy.mean()))
    with open(os.path.join(WORK_DIR, "rq34_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
    print(dtests.to_string(index=False))
    print(corpus_audit.round(2).to_string(index=False))
    print(base_tab.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
