"""
Step 2i - Name and describe the refined archetypes used in RQ2-RQ4, and recompute the RQ4 human
baseline with them.

Input: data/interim/frames_archetypes_truncation_winner.csv (step 2g: Gemini user-side embedding +
Gemini behavioural profile of the first 9 user messages, K-Means k = 3, selected by the pre-declared
rule) and the step 2e annotations of the same opening (llm_user_annotations_u9.jsonl).

Fixed naming rule (written before the profiles were labelled):
  * Open Explorer           = the cluster with the highest mean destination flexibility
  * Decisive Booker         = of the remaining two, the cluster with the higher mean decisiveness
  * Rigid-Constraint Seeker = the remaining cluster

Outputs
  data/interim/frames_archetypes_refined.csv
  data/interim/rq1_refined_summary.json
  outputs/interim/tables/t_rq1_refined_profile.csv, t_rq1_refined_vs_primary.csv, t_rq4_baseline_refined.csv
  outputs/interim/figures/fig_rq4_baseline_refined.png, fig_rq1_truncation_2x2.png (step 2g grid replotted
  as a 2 x 2 panel for the report; no refitting)
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import adjusted_rand_score

from common import FIG_DIR, TABLE_DIR, WORK_DIR
from step2b_rq1_representation import cramers_v
from step2f_rq1_llm_hybrid import ORD, load_ann

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                     "font.size": 10})
ORDER = ["Decisive Booker", "Open Explorer", "Rigid-Constraint Seeker"]


def plot_truncation_grid():
    grid = pd.read_csv(os.path.join(TABLE_DIR, "t_rq1_truncation_grid.csv"))
    grid["M"] = grid.M.astype(str)
    ms = ["3", "5", "7", "9", "whole"]
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.6), dpi=300)
    panels = [("stability_ari", "A. Stability (ARI)"), ("core_pct", "B. Core members (%)"),
              ("kappa_N5", "C. Routing \u03ba after five turns"), ("outcome_v", "D. Association with outcome (V)")]
    cols = plt.cm.viridis(np.linspace(0, 0.9, 6))
    for ax, (col, title) in zip(axes.ravel(), panels):
        for k, c in zip(range(3, 9), cols):
            g = grid[grid.k == k].set_index("M").reindex(ms)
            ax.plot(range(len(ms)), g[col], marker="o", color=c, lw=2.2 if k == 3 else 1.2, label=f"k = {k}")
        if col == "stability_ari":
            ax.axhline(0.60, ls=":", color="k", lw=1)
        ax.set_xticks(range(len(ms)))
        ax.set_xticklabels(ms)
        ax.set_xlabel("User messages used")
        ax.set_title(title)
    axes[0, 0].legend(ncol=2, fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_rq1_truncation_2x2.png"))
    plt.close(fig)


def main():
    win = pd.read_csv(os.path.join(WORK_DIR, "frames_archetypes_truncation_winner.csv"))
    prim = pd.read_csv(os.path.join(WORK_DIR, "frames_archetypes.csv"))
    df = prim.merge(win[["dialogue_id", "cluster"]].rename(columns={"cluster": "refined_cluster"}), on="dialogue_id")
    assert len(df) == len(win) == len(prim)
    a9 = load_ann(os.path.join(WORK_DIR, "llm_user_annotations_u9.jsonl")).loc[df.dialogue_id]
    full = load_ann(os.path.join(WORK_DIR, "llm_user_annotations.jsonl")).loc[df.dialogue_id]
    for c in ORD:
        df[c] = a9[c].astype(float).values
    df["goal9"] = a9.primary_goal.values
    df["outcome_full"] = full.outcome.values

    # ---- fixed naming rule ------------------------------------------------------------------------
    m = df.groupby("refined_cluster")[ORD].mean()
    names = {}
    explorer = int(m.destination_flexibility.idxmax())
    names[explorer] = "Open Explorer"
    rest = m.drop(index=explorer)
    booker = int(rest.decisiveness.idxmax())
    names[booker] = "Decisive Booker"
    names[int(rest.drop(index=booker).index[0])] = "Rigid-Constraint Seeker"
    df["archetype_refined"] = df.refined_cluster.map(names)
    df = df.rename(columns={"archetype": "archetype_primary"})

    out_cols = ["dialogue_id", "partition", "archetype_refined", "archetype_primary", "total_turns", "user_turns",
                "rer_proxy", "agent_request_turns", "task_success"]
    df[out_cols].to_csv(os.path.join(WORK_DIR, "frames_archetypes_refined.csv"), index=False)

    # ---- profile (golden partition) --------------------------------------------------------------
    g = df[df.partition == "gold"]
    prof = g.groupby("archetype_refined").agg(n=("dialogue_id", "size"), turns_M=("total_turns", "mean"),
                                              turns_SD=("total_turns", "std"), user_turns_M=("user_turns", "mean"),
                                              **{c: (c, "mean") for c in ORD})
    prof["pct"] = 100 * prof.n / prof.n.sum()
    prof["goal_explore_pct"] = g.groupby("archetype_refined").goal9.apply(
        lambda s: 100 * (s == "explore_destinations").mean())
    prof["goal_booking_pct"] = g.groupby("archetype_refined").goal9.apply(
        lambda s: 100 * (s == "specific_trip_booking").mean())
    prof["booked_pct"] = g.groupby("archetype_refined").outcome_full.apply(lambda s: 100 * (s == "booked").mean())
    prof["no_option_pct"] = g.groupby("archetype_refined").outcome_full.apply(
        lambda s: 100 * (s == "no_suitable_option").mean())
    prof["success_pct"] = g.groupby("archetype_refined").task_success.apply(lambda s: 100 * s.astype(float).mean())
    prof = prof.reindex(ORDER)
    prof.reset_index().to_csv(os.path.join(TABLE_DIR, "t_rq1_refined_profile.csv"), index=False)

    # ---- relation to the primary archetypes --------------------------------------------------------
    ct = pd.crosstab(df.archetype_primary, df.archetype_refined).reindex(columns=ORDER)
    ct.reset_index().to_csv(os.path.join(TABLE_DIR, "t_rq1_refined_vs_primary.csv"), index=False)
    ari_prim = adjusted_rand_score(df.archetype_primary, df.archetype_refined)
    v_prim = cramers_v(df.archetype_primary.values, df.archetype_refined.values)
    v_success = cramers_v(df.archetype_refined.values, df.task_success.astype(str).values)

    # ---- held-out generalization -------------------------------------------------------------------
    gc = df[df.partition == "gold"].archetype_refined.value_counts().reindex(ORDER)
    tc = df[df.partition == "test"].archetype_refined.value_counts().reindex(ORDER)
    chi = stats.chisquare(tc.values, gc.values / gc.sum() * tc.sum())

    # ---- RQ4 human baseline by refined archetype (all Frames dialogues) ---------------------------
    base = df.groupby("archetype_refined").agg(n=("dialogue_id", "size"), turns_M=("total_turns", "mean"),
                                               turns_SD=("total_turns", "std"), rer_M=("rer_proxy", "mean"),
                                               rer_SD=("rer_proxy", "std"),
                                               req_turns_M=("agent_request_turns", "mean")).reindex(ORDER)
    base.reset_index().to_csv(os.path.join(TABLE_DIR, "t_rq4_baseline_refined.csv"), index=False)
    g_turns = [np.log(df.loc[df.archetype_refined == a, "total_turns"]) for a in ORDER]
    g_rer = [df.loc[df.archetype_refined == a, "rer_proxy"].dropna() for a in ORDER]
    lev = stats.levene(*g_turns, center="median")
    kw_t, kw_r = stats.kruskal(*g_turns), stats.kruskal(*g_rer)
    pooled_sd = float(np.sqrt(np.average(base.turns_SD ** 2, weights=base.n - 1)))

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=300)
    lab = [a.replace(" ", "\n").replace("Rigid-Constraint", "Rigid-\nConstraint") for a in ORDER]
    axes[0].boxplot([df.loc[df.archetype_refined == a, "total_turns"] for a in ORDER], labels=lab, showmeans=True)
    axes[0].set_ylabel("Turns to dialogue end (human baseline)")
    axes[0].set_title("A. Turn economy by archetype")
    ci = 1.96 * base.rer_SD / np.sqrt(base.n)
    axes[1].bar(range(3), base.rer_M, yerr=ci, capsize=6, color=["#4c72b0", "#dd8452", "#55a868"])
    axes[1].set_ylim(bottom=0)
    axes[1].set_xticks(range(3))
    axes[1].set_xticklabels(lab)
    axes[1].set_ylabel("Redundant elicitation proxy (share of agent turns)")
    axes[1].set_title("B. Redundant elicitation by archetype")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_rq4_baseline_refined.png"))
    plt.close(fig)

    summary = dict(names={str(k): v for k, v in names.items()}, order=ORDER,
                   ari_vs_primary=float(ari_prim), cramers_v_vs_primary=float(v_prim),
                   cramers_v_task_success=float(v_success),
                   gold_counts=gc.astype(int).to_dict(), test_counts=tc.astype(int).to_dict(),
                   chi_gold_test=dict(chi2=float(chi.statistic), p=float(chi.pvalue), df=len(ORDER) - 1,
                                      N=int(tc.sum())),
                   rq4=dict(n=int(len(df)), levene_log_turns=dict(W=float(lev.statistic), p=float(lev.pvalue)),
                            kruskal_turns=dict(H=float(kw_t.statistic), p=float(kw_t.pvalue)),
                            kruskal_rer=dict(H=float(kw_r.statistic), p=float(kw_r.pvalue)),
                            pooled_turns_sd=pooled_sd, overall_rer_M=float(df.rer_proxy.mean())))
    with open(os.path.join(WORK_DIR, "rq1_refined_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
    print(prof.round(2).T.to_string())
    print(ct.to_string())
    print(base.round(3).to_string())


if __name__ == "__main__":
    plot_truncation_grid()
    main()
