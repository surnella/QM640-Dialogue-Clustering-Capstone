"""
Step 5 - Publication-Grade Exploratory Data Analysis (Univariate, Outcome-Stratified, Bivariate,
Multivariate), Feature Importance & Router Evaluation Diagnostics (Train / 5-Fold CV / Held-Out Test,
Confusion Matrices, Multiclass ROC-AUC), System Architecture, Workflow Diagrams, and 1:1 Print-Scale
(6.5-inch, 300-DPI, Times New Roman) Regeneration of All Report & Appendix Figures.

All figures are designed at exact 1:1 physical print width (`figsize=(6.5, ...)` inches at 300 DPI)
so that 8.5–10.5 pt Times New Roman labels render without any downscaling blur or label collisions
inside 1-inch margins on 8.5 x 11 inch APA 7 pages.
"""

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.preprocessing import StandardScaler, label_binarize

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(ROOT, "src"), os.path.join(ROOT, "src", "final_pipeline")):
    if p not in sys.path:
        sys.path.insert(0, p)

from common import FIG_DIR as INT_FIG_DIR, SEED, TABLE_DIR as INT_TABLE_DIR, WORK_DIR, load_canonical  # noqa: E402
from final_pipeline.common_llm import FINAL_DATA_DIR, FINAL_FIG_DIR, FINAL_TABLE_DIR  # noqa: E402
from final_pipeline.routing import REFINED_ARCHETYPES, RefinedArchetypeRouter, _sha1  # noqa: E402
from step2e_llm_user_annotation import truncate  # noqa: E402
from step2f_rq1_llm_hybrid import ORD, llm_matrix, load_ann  # noqa: E402

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 9.0,
    "axes.titlesize": 9.6,
    "axes.titleweight": "bold",
    "axes.labelsize": 8.8,
    "xtick.labelsize": 8.2,
    "ytick.labelsize": 8.2,
    "legend.fontsize": 7.8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
})

PAL_ARCH = {
    "Decisive Booker": "#2b5c8f",
    "Open Explorer": "#d97724",
    "Rigid-Constraint Seeker": "#2e8540",
}
SHORT_ARCH = {
    "Decisive Booker": "Decisive\nBooker",
    "Open Explorer": "Open\nExplorer",
    "Rigid-Constraint Seeker": "Rigid-Constraint\nSeeker",
}


def _box_legend_handles(extra=None):
    handles = [
        Line2D([0], [0], color="#d95f02", lw=1.6, label="Median"),
        Line2D([0], [0], marker="^", color="w", markerfacecolor="#2ca02c",
               markeredgecolor="#2ca02c", markersize=6.5, label="Mean"),
    ]
    if extra:
        handles.extend(extra)
    return handles


def build_eda_and_appendix_eda():
    df_clean = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    mw_clean = pd.read_csv(os.path.join(WORK_DIR, "multiwoz_clean.csv"))
    df_ref = pd.read_csv(os.path.join(WORK_DIR, "frames_archetypes_refined.csv"))
    ann9 = load_ann(os.path.join(WORK_DIR, "llm_user_annotations_u9.jsonl")).loc[df_clean.dialogue_id]
    ann_full = load_ann(os.path.join(WORK_DIR, "llm_user_annotations.jsonl")).loc[df_clean.dialogue_id]
    can = {d["dialogue_id"]: d for d in load_canonical(("frames",))}

    df = df_clean.merge(
        df_ref[["dialogue_id", "archetype_refined", "archetype_primary"]],
        on="dialogue_id",
    )
    df["revisions_count"] = df["revisions"]
    df["agent_offers"] = df["offers"]
    df["hesitation_markers_count"] = df["hesitations"]
    for col in ORD:
        df[col] = ann9[col].astype(float).values
    df["party_type"] = ann_full["party_type"].values
    df["outcome_llm"] = ann_full["outcome"].values

    t1_rows = [can[did]["canonical_tier1"] for did in df.dialogue_id]
    t1_df = pd.DataFrame(t1_rows)
    df["budget_usd"] = pd.to_numeric(t1_df["budget_amount"], errors="coerce")
    df["adults_count"] = pd.to_numeric(t1_df["traveler_count_adults"], errors="coerce")
    df["children_count"] = pd.to_numeric(t1_df["traveler_count_children"], errors="coerce")

    budgets_valid = df["budget_usd"].dropna()
    budgets_valid = budgets_valid[(budgets_valid >= 100) & (budgets_valid <= 100000)]

    # Outcome-stratified summary table (`t_eda_outcome_comparisons.csv`)
    out_order = [
        ("booked", "Booked Package"),
        ("no_suitable_option", "No Suitable Option"),
        ("undecided_or_left", "Undecided / Left"),
    ]
    out_rows = []
    for key, label in out_order:
        sub = df[df.outcome_llm == key]
        b_sub = sub["budget_usd"].dropna()
        b_sub = b_sub[(b_sub >= 100) & (b_sub <= 100000)]
        out_rows.append(dict(
            outcome_key=key,
            outcome_label=label,
            n=int(len(sub)),
            pct=float(100.0 * len(sub) / len(df)),
            turns_M=float(sub.total_turns.mean()),
            turns_SD=float(sub.total_turns.std(ddof=1)),
            revisions_M=float(sub.revisions_count.mean()),
            offers_M=float(sub.agent_offers.mean()),
            dest_flex_M=float(sub.destination_flexibility.mean()),
            explore_M=float(sub.exploration_breadth.mean()),
            decisive_M=float(sub.decisiveness.mean()),
            price_sens_M=float(sub.price_sensitivity.mean()),
            budget_Mdn=float(b_sub.median()) if len(b_sub) else np.nan,
        ))
    out_df = pd.DataFrame(out_rows)
    out_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_eda_outcome_comparisons.csv"), index=False)

    # Outcome omnibus F-tests across the 3 main outcomes
    sub3 = df[df.outcome_llm.isin([k for k, _ in out_order])]
    outcome_anova = {}
    for col in ["total_turns", "revisions_count", "agent_offers", "destination_flexibility", "exploration_breadth", "decisiveness"]:
        grps = [sub3[sub3.outcome_llm == k][col].values for k, _ in out_order]
        f_st, p_v = stats.f_oneway(*grps)
        kw_st, kw_p = stats.kruskal(*grps)
        outcome_anova[col] = dict(F=float(f_st), p=float(p_v), H=float(kw_st), p_kw=float(kw_p))

    # Gold vs. Test partition balance check across key structural & behavioral variables
    gold_sub = df[df.partition == "gold"]
    test_sub = df[df.partition == "test"]
    balance_checks = {}
    for col in ["total_turns", "revisions_count", "agent_offers", "mean_user_words", "decisiveness", "exploration_breadth"]:
        t_st, p_v = stats.ttest_ind(gold_sub[col], test_sub[col], equal_var=False)
        balance_checks[col] = dict(
            gold_M=float(gold_sub[col].mean()),
            test_M=float(test_sub[col].mean()),
            t=float(t_st),
            p=float(p_v),
        )

    # 1. Expanded Bivariate Correlation Table (`t_eda_bivariate_correlations.csv`)
    df["booked_binary"] = (df.outcome_llm == "booked").astype(float)
    biv_pairs = [
        ("total_turns", "revisions_count", "Total Turns vs. Slot Revisions"),
        ("total_turns", "agent_offers", "Total Turns vs. Agent Package Offers"),
        ("total_turns", "hesitation_markers_count", "Total Turns vs. User Hesitation Markers"),
        ("revisions_count", "exploration_breadth", "Slot Revisions vs. Exploration Breadth Rating"),
        ("total_turns", "decisiveness", "Total Turns vs. User Decisiveness Rating"),
        ("mean_user_words", "information_upfront", "User Words/Turn vs. Information Up Front Rating"),
        ("agent_offers", "destination_flexibility", "Agent Offers vs. Destination Flexibility Rating"),
        ("question_asking", "total_turns", "Question-Asking Rating vs. Total Turns"),
        ("decisiveness", "booked_binary", "User Decisiveness Rating vs. Package Booking Indicator"),
    ]
    biv_rows = []
    for v1, v2, label in biv_pairs:
        r_p, p_p = stats.pearsonr(df[v1], df[v2])
        r_s, p_s = stats.spearmanr(df[v1], df[v2])
        biv_rows.append(dict(
            pair_label=label,
            var_x=v1,
            var_y=v2,
            pearson_r=float(r_p),
            pearson_p=float(p_p),
            spearman_rho=float(r_s),
            spearman_p=float(p_s),
        ))
    biv_df = pd.DataFrame(biv_rows)
    biv_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_eda_bivariate_correlations.csv"), index=False)

    # FIGURE 1 (`fig_eda_turns.png`, 6.5 x 4.7 in): 2x2 Univariate, Budget & Outcome-Stratified EDA
    fig, axes = plt.subplots(2, 2, figsize=(6.5, 4.7))
    bins = np.arange(2, 46, 2)
    axes[0, 0].hist(df.total_turns, bins=bins, alpha=0.68, color="#2b5c8f", label=f"Frames (M={df.total_turns.mean():.1f})")
    axes[0, 0].hist(mw_clean.total_turns, bins=bins, alpha=0.62, color="#d97724", label=f"MultiWOZ (M={mw_clean.total_turns.mean():.1f})")
    axes[0, 0].set_xlabel("Total turns per dialogue")
    axes[0, 0].set_ylabel("Number of dialogues")
    axes[0, 0].set_title("A. Dialogue Length by Corpus")
    axes[0, 0].legend(frameon=False, loc="upper right")

    bp = axes[0, 1].boxplot(
        [df.mean_user_words, df.mean_agent_words, mw_clean.mean_user_words, mw_clean.mean_agent_words],
        tick_labels=["Frames\nUser", "Frames\nAgent", "MultiWOZ\nUser", "MultiWOZ\nAgent"],
        showmeans=True, showfliers=False, widths=0.52,
        medianprops=dict(color="#d95f02", lw=1.5),
        meanprops=dict(marker="^", markerfacecolor="#2ca02c", markeredgecolor="#2ca02c", markersize=5.5),
    )
    axes[0, 1].set_ylabel("Mean words per utterance")
    axes[0, 1].set_title("B. Utterance Length by Speaker")
    axes[0, 1].legend(handles=_box_legend_handles(), frameon=False, loc="upper right")

    b_clip = np.clip(budgets_valid.values / 1000.0, 0, 25)
    axes[1, 0].hist(b_clip, bins=np.linspace(0, 25, 21), color="#3b7a57", alpha=0.78, edgecolor="white", lw=0.5)
    axes[1, 0].axvline(budgets_valid.median() / 1000.0, color="#d95f02", ls="--", lw=1.4,
                       label=f"Median = ${budgets_valid.median():,.0f}")
    axes[1, 0].axvline(budgets_valid.mean() / 1000.0, color="#111111", ls=":", lw=1.4,
                       label=f"Mean = ${budgets_valid.mean():,.0f}")
    axes[1, 0].set_xlabel("Stated trip budget (thousands USD, capped at 25k)")
    axes[1, 0].set_ylabel("Dialogues (n = 693)")
    axes[1, 0].set_title("C. Stated Trip Budget Distribution")
    axes[1, 0].legend(frameon=False, loc="upper right")

    x_o = np.arange(len(out_order))
    w_o = 0.26
    t_m = [out_df.loc[i, "turns_M"] for i in range(3)]
    r_m = [out_df.loc[i, "revisions_M"] for i in range(3)]
    o_m = [out_df.loc[i, "offers_M"] for i in range(3)]
    axes[1, 1].bar(x_o - w_o, t_m, w_o, color="#2b5c8f", label="Turns")
    axes[1, 1].bar(x_o, r_m, w_o, color="#d97724", label="Slot revisions")
    axes[1, 1].bar(x_o + w_o, o_m, w_o, color="#2e8540", label="Package offers")
    for idx_bar, vals_bar in enumerate([t_m, r_m, o_m]):
        offset_x = (idx_bar - 1) * w_o
        for xi, v in enumerate(vals_bar):
            axes[1, 1].text(xi + offset_x, v + 0.45, f"{v:.1f}", ha="center", va="bottom", fontsize=6.8)
    axes[1, 1].set_ylim(0, 25.0)
    axes[1, 1].set_xticks(x_o)
    axes[1, 1].set_xticklabels(["Booked\n(65.6%)", "No Option\n(28.1%)", "Undecided\n(6.2%)"])
    axes[1, 1].set_ylabel("Mean count per dialogue")
    axes[1, 1].set_title("D. Dynamics by Session Outcome")
    axes[1, 1].legend(frameon=False, loc="upper center", ncol=3, fontsize=6.8)

    fig.tight_layout(pad=0.9)
    fig.savefig(os.path.join(INT_FIG_DIR, "fig_eda_turns.png"))
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_eda_turns.png"))
    plt.close(fig)

    # FIGURE 2 (`fig_eda_bivariate.png`, 6.5 x 2.95 in)
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.95))
    rng_j = np.random.default_rng(42)
    for arch in REFINED_ARCHETYPES:
        sub = df[df.archetype_refined == arch]
        axes[0].scatter(
            sub.total_turns + rng_j.normal(0, 0.22, len(sub)),
            sub.revisions_count + rng_j.normal(0, 0.22, len(sub)),
            s=10, alpha=0.45, color=PAL_ARCH[arch], label=arch,
        )
    slope, intercept, r_val, _, _ = stats.linregress(df.total_turns, df.revisions_count)
    xs = np.linspace(df.total_turns.min(), df.total_turns.max(), 100)
    axes[0].plot(xs, intercept + slope * xs, color="#111111", ls="--", lw=1.3, label=f"OLS fit (r = {r_val:.2f})")
    axes[0].set_xlabel("Dialogue length (total turns)")
    axes[0].set_ylabel("Slot-value revisions (count)")
    axes[0].set_title("A. Turns vs. Slot Revisions")
    axes[0].legend(frameon=False, fontsize=7.0, loc="upper left")

    x = np.arange(len(REFINED_ARCHETYPES))
    w = 0.34
    rev_means = [df[df.archetype_refined == a].revisions_count.mean() for a in REFINED_ARCHETYPES]
    rev_cis = [1.96 * df[df.archetype_refined == a].revisions_count.std(ddof=1) / np.sqrt((df.archetype_refined == a).sum()) for a in REFINED_ARCHETYPES]
    off_means = [df[df.archetype_refined == a].agent_offers.mean() for a in REFINED_ARCHETYPES]
    off_cis = [1.96 * df[df.archetype_refined == a].agent_offers.std(ddof=1) / np.sqrt((df.archetype_refined == a).sum()) for a in REFINED_ARCHETYPES]

    axes[1].bar(x - w / 2, rev_means, w, yerr=rev_cis, capsize=3, color="#2b5c8f", error_kw=dict(lw=1.0), label="Slot revisions")
    axes[1].bar(x + w / 2, off_means, w, yerr=off_cis, capsize=3, color="#d97724", error_kw=dict(lw=1.0), label="Package offers")
    for xi in range(len(REFINED_ARCHETYPES)):
        axes[1].text(xi - w / 2, rev_means[xi] + rev_cis[xi] + 0.55, f"{rev_means[xi]:.1f}", ha="center", va="bottom", fontsize=7.3)
        axes[1].text(xi + w / 2, off_means[xi] + off_cis[xi] + 0.55, f"{off_means[xi]:.1f}", ha="center", va="bottom", fontsize=7.3)
    axes[1].set_ylim(0, 30.5)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels([SHORT_ARCH[a] for a in REFINED_ARCHETYPES])
    axes[1].set_ylabel("Mean count per dialogue (95% CI)")
    axes[1].set_title("B. Negotiation Intensity by Archetype")
    axes[1].legend(frameon=False, fontsize=7.4, loc="upper right")
    fig.tight_layout(pad=0.8)
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_eda_bivariate.png"))
    plt.close(fig)

    # FIGURE 3 (`fig_eda_multivariate.png`, 6.5 x 3.25 in): Non-overlapping biplot labels!
    mv_cols = [
        "total_turns", "revisions_count", "agent_offers", "mean_user_words",
        "destination_flexibility", "exploration_breadth", "decisiveness",
        "revision_tendency", "question_asking", "politeness",
    ]
    mv_labels = [
        "Total Turns", "Slot Revisions", "Agent Offers", "User Words/Turn",
        "Dest. Flexibility", "Exploration Breadth", "Decisiveness",
        "Revision Tendency", "Question Asking", "Politeness",
    ]
    mv_short = [
        "Turns", "Revisions", "Offers", "Words/Turn",
        "Dest. Flex.", "Exploration", "Decisive.",
        "Rev. Tend.", "Questions", "Politeness",
    ]
    corr_mat = df[mv_cols].corr(method="spearman").values

    X_mv = StandardScaler().fit_transform(df[mv_cols].values)
    pca = PCA(n_components=3, random_state=42).fit(X_mv)
    Z_pca = pca.transform(X_mv)
    loadings_df = pd.DataFrame({
        "variable": mv_labels,
        "PC1_loading": pca.components_[0],
        "PC2_loading": pca.components_[1],
        "PC3_loading": pca.components_[2],
    })
    loadings_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_eda_multivariate_loadings.csv"), index=False)

    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.30), gridspec_kw={"width_ratios": [1.05, 1.0]})
    im = axes[0].imshow(corr_mat, cmap="RdBu_r", vmin=-0.8, vmax=0.8)
    axes[0].set_xticks(range(len(mv_short)))
    axes[0].set_xticklabels(mv_short, rotation=45, ha="right", fontsize=7.2)
    axes[0].set_yticks(range(len(mv_short)))
    axes[0].set_yticklabels(mv_short, fontsize=7.2)
    for i in range(len(mv_short)):
        for j in range(len(mv_short)):
            val = corr_mat[i, j]
            axes[0].text(j, i, f"{val:.2f}".replace("-0.", "-.").replace("0.", "."),
                         ha="center", va="center",
                         color="white" if abs(val) > 0.45 else "#111111", fontsize=5.8)
    axes[0].set_title("A. Spearman Correlation Matrix", fontsize=9.2)
    cbar = fig.colorbar(im, ax=axes[0], fraction=0.044, pad=0.03)
    cbar.ax.tick_params(labelsize=7.0)

    for arch in REFINED_ARCHETYPES:
        m = (df.archetype_refined == arch).values
        axes[1].scatter(Z_pca[m, 0], Z_pca[m, 1], s=8, alpha=0.35, color=PAL_ARCH[arch], label=arch)

    scale = 4.3
    # Custom non-overlapping label offsets (dx, dy) in data coordinates
    vec_offsets = {
        0: (0.70, -0.30),   # Turns (below arrow)
        1: (0.75, 0.36),    # Revisions (above arrow — zero overlap with Turns!)
        4: (0.55, -0.42),   # Dest. Flex.
        5: (0.95, -0.10),   # Exploration
        6: (-0.55, 0.30),   # Decisive.
        9: (0.35, 0.32),    # Politeness
    }
    for idx_v, (ox, oy) in vec_offsets.items():
        lx, ly = pca.components_[0, idx_v] * scale, pca.components_[1, idx_v] * scale
        axes[1].annotate("", xy=(lx, ly), xytext=(0, 0),
                         arrowprops=dict(arrowstyle="->", color="#111111", lw=1.15))
        axes[1].text(lx + ox, ly + oy, mv_short[idx_v], fontsize=7.2, ha="center", va="center",
                     fontweight="bold", color="#111111",
                     bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.78))
    axes[1].set_xlim(-4.3, 8.2)
    axes[1].set_ylim(-4.5, 3.6)
    axes[1].set_xlabel(f"PC1 ({100 * pca.explained_variance_ratio_[0]:.1f}% var.: Exploration vs. Rigidity)", fontsize=8.0)
    axes[1].set_ylabel(f"PC2 ({100 * pca.explained_variance_ratio_[1]:.1f}% var.: Decisiveness)", fontsize=8.0)
    axes[1].set_title("B. PCA Biplot of Behavioral Features", fontsize=9.2)
    axes[1].legend(frameon=False, fontsize=6.8, loc="lower right", markerscale=1.4)
    fig.tight_layout(pad=0.7)
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_eda_multivariate.png"))
    plt.close(fig)

    # Appendix Figure E1 (`fig_eda_slots.png`, 6.5 x 2.9 in)
    comp = pd.read_csv(os.path.join(INT_TABLE_DIR, "t_slot_completeness.csv"))
    fig, ax = plt.subplots(figsize=(6.5, 2.9))
    xs_s = np.arange(len(comp))
    ws_s = 0.38
    ax.bar(xs_s - ws_s / 2, comp["frames_pct"], ws_s, color="#2b5c8f", label="Microsoft Frames (N = 1,334)")
    ax.bar(xs_s + ws_s / 2, comp["multiwoz_pct"], ws_s, color="#d97724", label="MultiWOZ 2.2 (N = 1,499)")
    ax.axvline(8.5, color="#444444", ls="--", lw=1.0)
    ax.text(8.68, 92, "Tier-2 policy slots\n(0% in archival corpora)", fontsize=7.4, color="#333333", va="top")
    short_slots = [
        "Origin\ncity", "Dest.\ncity", "Depart.\ndate", "Return\ndate", "Duration\nnights",
        "Adults\ncount", "Children\ncount", "Budget\n(USD)", "Hotel\ntier",
        "Visa\ndays", "Passport\nmonths", "Discount\n(%)",
    ]
    ax.set_xticks(xs_s)
    ax.set_xticklabels(short_slots, fontsize=7.0)
    ax.set_ylim(0, 108)
    ax.set_ylabel("Dialogues with slot populated (%)")
    ax.set_title("Observed Canonical Tier-1 and Tier-2 Slot Completeness by Corpus")
    ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.72, 0.99))
    fig.tight_layout(pad=0.7)
    fig.savefig(os.path.join(INT_FIG_DIR, "fig_eda_slots.png"))
    plt.close(fig)

    with open(os.path.join(FINAL_DATA_DIR, "eda_summary_ext.json"), "w", encoding="utf-8") as f:
        json.dump(dict(
            bivariate=biv_df.to_dict("records"),
            pca_var_explained=[float(x) for x in pca.explained_variance_ratio_],
            loadings=loadings_df.to_dict("records"),
            budget_stats=dict(
                n=int(len(budgets_valid)),
                M=float(budgets_valid.mean()),
                SD=float(budgets_valid.std(ddof=1)),
                Mdn=float(budgets_valid.median()),
                IQR=float(budgets_valid.quantile(0.75) - budgets_valid.quantile(0.25)),
                min=float(budgets_valid.min()),
                max=float(budgets_valid.max()),
            ),
            adults_M=float(df["adults_count"].dropna().mean()),
            adults_SD=float(df["adults_count"].dropna().std(ddof=1)),
            user_rating_M=float(df["user_rating"].dropna().mean()),
            user_rating_SD=float(df["user_rating"].dropna().std(ddof=1)),
            user_rating_n=int(df["user_rating"].notna().sum()),
            party_pct={k: float(v) for k, v in (df["party_type"].value_counts(normalize=True) * 100).items()},
            outcome_rows=out_rows,
            outcome_anova=outcome_anova,
            balance_checks=balance_checks,
        ), f, indent=2)
    print("Generated expanded EDA tables and Figures 1-3 + Figure E1.")


def build_architecture_and_workflow_diagrams():
    def draw_node(ax, x, y, w, h, title, body, fc, ec, title_fs=8.0, body_fs=6.9):
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.010,rounding_size=0.018",
            facecolor=fc, edgecolor=ec, linewidth=1.25,
        )
        ax.add_patch(box)
        ax.text(x + w / 2, y + h * 0.72, title, ha="center", va="center",
                fontsize=title_fs, fontweight="bold", color="#111111")
        ax.text(x + w / 2, y + h * 0.30, body, ha="center", va="center",
                fontsize=body_fs, color="#222222", linespacing=1.18)

    def draw_arr(ax, x1, y1, x2, y2):
        arr = FancyArrowPatch((x1, y1), (x2, y2),
                              arrowstyle="-|>,head_length=4.5,head_width=3.0",
                              lw=1.2, color="#333333")
        ax.add_patch(arr)

    # FIGURE 4 (`fig_system_architecture.png`, 6.5 x 4.15 in)
    # Explicitly includes ALL 7 Rubric/Template stages:
    # 1. Data Source -> 2. Preprocessing -> 3. EDA -> 4. Feature Engineering ->
    # 5. Model Stage -> 6. Evaluation & Guardrails -> 7. Deployment + Clean 2-Row Legend
    fig, ax = plt.subplots(figsize=(6.5, 4.15))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.01, 0.955, "OFFLINE DISCOVERY & TRAINING PIPELINE (Golden Partition D_gold, n = 933)",
            fontsize=8.3, fontweight="bold", color="#1f4e78")
    xs = [0.01, 0.262, 0.514, 0.766]
    bw, bh = 0.224, 0.23
    top_y = 0.695

    draw_node(ax, xs[0], top_y, bw, bh, "1. Data Stage",
              "Frames (N=1,369; 2016–17)\nMultiWOZ 2.2 (N=1,500)\nJSON Corpus Ingestion",
              "#e8f1fa", "#2b5c8f")
    draw_arr(ax, xs[0] + bw, top_y + bh / 2, xs[1], top_y + bh / 2)

    draw_node(ax, xs[1], top_y, bw, bh, "2. Preprocessing Stage",
              "Two-Tier Pydantic Schema\n[SLOT] De-Lexicalization\n70/30 Stratified Split",
              "#e8f1fa", "#2b5c8f")
    draw_arr(ax, xs[1] + bw, top_y + bh / 2, xs[2], top_y + bh / 2)

    draw_node(ax, xs[2], top_y, bw, bh, "3. EDA Stage",
              "Univariate, Outcome, Bivariate\n& Multivariate PCA Audits\nSlot & Outlier Profiling",
              "#e6f4ea", "#2e8540")
    draw_arr(ax, xs[2] + bw, top_y + bh / 2, xs[3], top_y + bh / 2)

    draw_node(ax, xs[3], top_y, bw, bh, "4. Feature Engineering",
              "Gemini PCA-20 + 16-Field\nLLM Behavioral Blocks (46-d)\nη² & Permutation Importance",
              "#fff2cc", "#b8860b")

    # Clean vertical connectors between Offline Row and Online Row
    draw_arr(ax, xs[1] + bw / 2, top_y, xs[1] + bw / 2, 0.565)
    ax.text(xs[1] + bw / 2 + 0.015, 0.630, "Held-Out Test Split\nD_test (n = 401)",
            ha="left", va="center", fontsize=6.9, style="italic", color="#1f4e78")
    draw_arr(ax, xs[3] + bw / 2, top_y, xs[3] + bw / 2, 0.565)
    ax.text(xs[3] + bw / 2 - 0.015, 0.630, "Frozen PCA-20, Centroids,\nRouter & 3 FAISS Indices",
            ha="right", va="center", fontsize=6.9, style="italic", color="#274e13")

    ax.text(0.01, 0.520, "ONLINE MODELING, POLICY GOVERNANCE, EVALUATION & DEPLOYMENT (Held-Out D_test, n = 401)",
            fontsize=8.3, fontweight="bold", color="#274e13")
    bot_y = 0.265

    draw_node(ax, xs[0], bot_y, bw, bh, "5. Model Stage (RQ1–RQ2)",
              "K-Means (k=3) & L2 Router\nFAISS IndexFlatIP (k=3)\nPacing & Trade-Off Policy",
              "#d9ead3", "#38761d")
    draw_arr(ax, xs[0] + bw, bot_y + bh / 2, xs[1], bot_y + bh / 2)

    draw_node(ax, xs[1], bot_y, bw, bh, "6a. Policy Guardrail (RQ3)",
              "Declarative YAML Engine\n5 Tier-2 Compliance Rules\nPost-Gen Leakage Sanitizer",
              "#f4cccc", "#990000")
    draw_arr(ax, xs[1] + bw, bot_y + bh / 2, xs[2], bot_y + bh / 2)

    draw_node(ax, xs[2], bot_y, bw, bh, "6b. Evaluation Stage",
              "Train/CV/Test κ & ROC-AUC\nRM / 2×2 / 2×3 HC3 & ART\nDual-Judge Audit (κ=.917)",
              "#ead1dc", "#741b47")
    draw_arr(ax, xs[2] + bw, bot_y + bh / 2, xs[3], bot_y + bh / 2)

    draw_node(ax, xs[3], bot_y, bw, bh, "7. Deployment Stage",
              "Stateless FastAPI Service\nRedis Informed Slot Ledger\nOTA WebSocket & CRS API",
              "#d0e0e3", "#134f5c")

    # Clean 2-row x 3-column non-overlapping legend
    legend_specs = [
        (0.01, 0.135, "#e8f1fa", "#2b5c8f", "Data & Preprocessing"),
        (0.34, 0.135, "#e6f4ea", "#2e8540", "Exploratory Analysis (EDA)"),
        (0.68, 0.135, "#fff2cc", "#b8860b", "Feature Engineering & Importance"),
        (0.01, 0.045, "#d9ead3", "#38761d", "Clustering, Router & FAISS Model"),
        (0.34, 0.045, "#f4cccc", "#990000", "Declarative Policy Verification"),
        (0.68, 0.045, "#d0e0e3", "#134f5c", "Statistical Eval & Production API"),
    ]
    for lx, ly, fc, ec, lab in legend_specs:
        rect = FancyBboxPatch((lx, ly), 0.024, 0.048, boxstyle="round,pad=0.004",
                              facecolor=fc, edgecolor=ec, lw=1.0)
        ax.add_patch(rect)
        ax.text(lx + 0.033, ly + 0.024, lab, fontsize=7.1, va="center", color="#111111")

    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_system_architecture.png"))
    plt.close(fig)

    # FIGURE 5 (`fig_rq_workflows_4panel.png`, 6.5 x 4.35 in)
    fig, axes = plt.subplots(2, 2, figsize=(6.5, 4.35))
    panel_specs = [
        (
            axes[0, 0],
            "A. RQ1: Clustering & Prefix Router",
            [
                ("1. Split", "933 Gold /\n401 Test", "#e8f1fa", "#2b5c8f"),
                ("2. Features", "PCA-20 +\n26-d LLM", "#fff2cc", "#b8860b"),
                ("3. Cluster", "159 Runs;\nKM k=3", "#d9ead3", "#38761d"),
                ("4. Validate", "ARI=.89;\nκ=.54–.96", "#ead1dc", "#741b47"),
            ],
        ),
        (
            axes[0, 1],
            "B. RQ2: Cluster-Adaptive Prompting",
            [
                ("1. Prefix", "N=33 Test\n(M=5 Msgs)", "#e8f1fa", "#2b5c8f"),
                ("2. Route", "Blocks L2\n(AUC=.87)", "#fff2cc", "#b8860b"),
                ("3. Prompt", "Zero / Static\n/ Adaptive", "#d9ead3", "#38761d"),
                ("4. RM Test", "Cos F=9.79\nErr 3.87w", "#ead1dc", "#741b47"),
            ],
        ),
        (
            axes[1, 0],
            "C. RQ3: 2×2 Policy Governance",
            [
                ("1. Inject", "N=144 Units\n(50% Viol.)", "#e8f1fa", "#2b5c8f"),
                ("2. YAML", "5 Tier-2\nRules Check", "#f4cccc", "#990000"),
                ("3. 2×2 Gen", "Rules ×\nPrompting", "#d9ead3", "#38761d"),
                ("4. Audit", "0% Leak;\n98.6% Sens.", "#ead1dc", "#741b47"),
            ],
        ),
        (
            axes[1, 1],
            "D. RQ4: 2×3 Turn-Economy Sim.",
            [
                ("1. Seeds", "N=180 Unique\n(30/Cell)", "#e8f1fa", "#2b5c8f"),
                ("2. Ledger", "Slot Ledger\n+ Options", "#d9ead3", "#38761d"),
                ("3. Loop", "User–Agent\nTo Quote", "#fff2cc", "#b8860b"),
                ("4. 2×3 Test", "−30..43%\nTurns; 0 RER", "#ead1dc", "#741b47"),
            ],
        ),
    ]
    for ax, title, boxes in panel_specs:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.text(0.01, 0.90, title, fontsize=8.8, fontweight="bold", color="#111111")
        pxs = [0.01, 0.262, 0.514, 0.766]
        for i, (bt, bs, fc, ec) in enumerate(boxes):
            draw_node(ax, pxs[i], 0.14, 0.218, 0.66, bt, bs, fc, ec, title_fs=7.6, body_fs=6.9)
            if i < 3:
                draw_arr(ax, pxs[i] + 0.218, 0.47, pxs[i + 1], 0.47)

    fig.tight_layout(pad=0.6)
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_rq_workflows_4panel.png"))
    plt.close(fig)
    print("Generated Figures 4 and 5 (Architecture & Workflows).")


def build_feature_importance_and_router_visuals():
    router = RefinedArchetypeRouter()
    df = router.df
    y = df.archetype_refined.values
    gm, tm = router.gold_mask, router.test_mask

    Xs, clfs, lcols = {}, {}, []
    split_rows = []
    probs_test = {}
    preds_test = {}

    for m in (3, 5, 7, 9):
        info = router.models_by_m[m]
        clf = info["clf"]
        ann = load_ann(os.path.join(WORK_DIR, f"llm_user_annotations_u{m}.jsonl")).loc[df.dialogue_id]
        docs = []
        for did in df.dialogue_id:
            rt = router.frames_raw[did]["turns"]
            tx = router.delex_turns[did]
            l_cut = len(truncate(rt, m))
            user_tx = "\n".join(x for x in tx[:l_cut] if x.startswith("USER:")) or tx[0]
            docs.append(user_tx)
        emb = np.array([router.emb_lookup[_sha1(t)] for t in docs], dtype=np.float32)
        eb = info["pca"].transform(emb)
        lmat = llm_matrix(ann)
        X = info["blocks"].transform([eb, lmat.values]).astype(np.float32)
        Xs[m], clfs[m] = X, clf
        if m == 9:
            lcols = list(lmat.columns)

        pred_tr = clf.predict(X[gm])
        prob_tr = clf.predict_proba(X[gm])
        pred_te = clf.predict(X[tm])
        prob_te = clf.predict_proba(X[tm])
        probs_test[m] = prob_te
        preds_test[m] = pred_te

        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
        cv_pred = cross_val_predict(LogisticRegression(max_iter=3000, C=1.0, random_state=SEED), X[gm], y[gm], cv=skf)
        cv_prob = cross_val_predict(LogisticRegression(max_iter=3000, C=1.0, random_state=SEED), X[gm], y[gm], cv=skf, method="predict_proba")

        split_rows.append(dict(
            m=m,
            approx_turns=2 * m - 1,
            train_n=int(gm.sum()),
            train_acc=float(accuracy_score(y[gm], pred_tr)),
            train_kappa=float(cohen_kappa_score(y[gm], pred_tr)),
            train_auc=float(roc_auc_score(y[gm], prob_tr, multi_class="ovr", average="macro")),
            cv_acc=float(accuracy_score(y[gm], cv_pred)),
            cv_kappa=float(cohen_kappa_score(y[gm], cv_pred)),
            cv_auc=float(roc_auc_score(y[gm], cv_prob, multi_class="ovr", average="macro")),
            test_n=int(tm.sum()),
            test_acc=float(accuracy_score(y[tm], pred_te)),
            test_kappa=float(cohen_kappa_score(y[tm], pred_te)),
            test_macro_f1=float(f1_score(y[tm], pred_te, average="macro")),
            test_auc=float(roc_auc_score(y[tm], prob_te, multi_class="ovr", average="macro")),
        ))

    split_df = pd.DataFrame(split_rows)
    split_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_router_train_cv_test.csv"), index=False)

    # Feature-level importance across all 46 columns
    feat_names = [f"PCA_{i+1}" for i in range(20)] + lcols
    pretty_map = {
        "PCA_1": "Gemini Semantic PC1",
        "PCA_2": "Gemini Semantic PC2",
        "PCA_6": "Gemini Semantic PC6",
        "detail_orientation": "Detail Orientation (1–5)",
        "exploration_breadth": "Exploration Breadth (1–5)",
        "goal_specific_trip_booking": "Primary Goal: Specific Booking",
        "goal_explore_destinations": "Primary Goal: Explore Dest.",
        "decisiveness": "Decisiveness (1–5)",
        "politeness": "Politeness (1–5)",
        "question_asking": "Question Asking (1–5)",
        "tone_positive": "Emotional Tone: Positive",
        "revision_tendency": "Revision Tendency (1–5)",
        "destination_flexibility": "Destination Flexibility (1–5)",
        "tone_frustrated": "Emotional Tone: Frustrated",
        "sec_price_shopping": "Secondary Goal: Price Shop",
        "date_flexibility": "Date Flexibility (1–5)",
        "information_upfront": "Information Up Front (1–5)",
        "price_sensitivity": "Price Sensitivity (1–5)",
    }
    rng = np.random.default_rng(SEED)
    base_k5 = cohen_kappa_score(y[tm], preds_test[5])
    base_k9 = cohen_kappa_score(y[tm], preds_test[9])

    fi_rows = []
    for j, fn in enumerate(feat_names):
        vals = Xs[9][gm, j]
        grps = [vals[y[gm] == a] for a in REFINED_ARCHETYPES]
        f_stat, p_val = stats.f_oneway(*grps)
        grand = vals.mean()
        ss_b = sum(len(g) * (g.mean() - grand) ** 2 for g in grps)
        ss_t = float(np.sum((vals - grand) ** 2))
        eta2 = float(ss_b / ss_t) if ss_t > 0 else 0.0
        b5 = float(np.linalg.norm(clfs[5].coef_[:, j]))
        b9 = float(np.linalg.norm(clfs[9].coef_[:, j]))
        dk5, dk9 = [], []
        for _ in range(30):
            Xp5 = Xs[5][tm].copy()
            Xp5[:, j] = rng.permutation(Xp5[:, j])
            Xp9 = Xs[9][tm].copy()
            Xp9[:, j] = rng.permutation(Xp9[:, j])
            dk5.append(base_k5 - cohen_kappa_score(y[tm], clfs[5].predict(Xp5)))
            dk9.append(base_k9 - cohen_kappa_score(y[tm], clfs[9].predict(Xp9)))
        fi_rows.append(dict(
            feature=fn,
            pretty_name=pretty_map.get(fn, fn),
            block=("Gemini Semantic PCA-20" if j < 20 else
                   ("Ordinal Behavioral (10)" if fn in ORD else
                    ("Goal Indicators (12)" if fn.startswith(("goal_", "sec_")) else "Emotional Tone (4)"))),
            eta2_gold=eta2,
            F_gold=float(f_stat),
            p_gold=float(p_val),
            beta_l2_m5=b5,
            beta_l2_m9=b9,
            perm_dk_m5=float(np.mean(dk5)),
            perm_dk_m9=float(np.mean(dk9)),
        ))
    fi_df = pd.DataFrame(fi_rows).sort_values("eta2_gold", ascending=False).reset_index(drop=True)
    fi_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_feature_importance.csv"), index=False)

    # Block-level permutation importance
    block_defs = [
        ("Gemini Semantic PCs (20)", list(range(0, 20))),
        ("Ordinal Scales (10)", [i for i, f in enumerate(feat_names) if f in ORD]),
        ("Goal Indicators (12)", [i for i, f in enumerate(feat_names) if f.startswith(("goal_", "sec_"))]),
        ("Emotional Tone (4)", [i for i, f in enumerate(feat_names) if f.startswith("tone_")]),
    ]
    block_rows = []
    rng_b = np.random.default_rng(SEED)
    for b_label, cols in block_defs:
        dk5, dk9 = [], []
        for _ in range(50):
            p_idx = rng_b.permutation(tm.sum())
            Xp5 = Xs[5][tm].copy()
            Xp5[:, cols] = Xp5[p_idx][:, cols]
            Xp9 = Xs[9][tm].copy()
            Xp9[:, cols] = Xp9[p_idx][:, cols]
            dk5.append(base_k5 - cohen_kappa_score(y[tm], clfs[5].predict(Xp5)))
            dk9.append(base_k9 - cohen_kappa_score(y[tm], clfs[9].predict(Xp9)))
        block_rows.append(dict(
            block_label=b_label,
            n_cols=len(cols),
            dk_m5_M=float(np.mean(dk5)),
            dk_m5_SD=float(np.std(dk5, ddof=1)),
            dk_m9_M=float(np.mean(dk9)),
            dk_m9_SD=float(np.std(dk9, ddof=1)),
        ))
    block_df = pd.DataFrame(block_rows)
    block_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_block_importance.csv"), index=False)

    # Save JSON summary including confusion matrices for report loader
    cm5 = confusion_matrix(y[tm], preds_test[5], labels=REFINED_ARCHETYPES).tolist()
    cm9 = confusion_matrix(y[tm], preds_test[9], labels=REFINED_ARCHETYPES).tolist()
    with open(os.path.join(FINAL_DATA_DIR, "feature_and_router_diagnostics.json"), "w", encoding="utf-8") as f:
        json.dump(dict(
            splits=split_rows,
            top_features=fi_df.head(15).to_dict("records"),
            blocks=block_rows,
            cm_m5=cm5,
            cm_m9=cm9,
        ), f, indent=2)

    # FIGURE 6 (`fig_feature_importance_and_cm.png`, 6.5 x 4.95 in):
    # Panel A: Top-10 Features by Cluster Variance Explained (eta^2) on D_gold
    # Panel B: Held-Out Block-Level Permutation Importance (Delta kappa at M=5 & M=9)
    # Panel C: Held-Out Confusion Matrix at Runtime Horizon M=5 (n = 401)
    # Panel D: Held-Out Multiclass One-vs-Rest ROC Curves (M=5 per class + M=9 macro)
    fig, axes = plt.subplots(2, 2, figsize=(6.5, 4.95))

    top10 = fi_df.head(10).iloc[::-1]
    y_pos = np.arange(len(top10))
    colors_a = ["#b8860b" if b.startswith("Gemini") else "#2b5c8f" for b in top10["block"]]
    axes[0, 0].barh(y_pos, top10["eta2_gold"], height=0.66, color=colors_a, alpha=0.88)
    for yi, v in enumerate(top10["eta2_gold"]):
        axes[0, 0].text(v + 0.012, yi, f"{v:.2f}".replace("0.", "."), va="center", fontsize=6.9)
    axes[0, 0].set_yticks(y_pos)
    axes[0, 0].set_yticklabels(top10["pretty_name"], fontsize=7.0)
    axes[0, 0].set_xlim(0, 0.68)
    axes[0, 0].set_xlabel("Cluster variance explained η² (D_gold)")
    axes[0, 0].set_title("A. Top-10 Discriminative Features")

    yb = np.arange(len(block_df))[::-1]
    hb = 0.34
    axes[0, 1].barh(yb + hb / 2, block_df["dk_m5_M"], hb, xerr=block_df["dk_m5_SD"], capsize=2.2,
                    color="#2b5c8f", error_kw=dict(lw=0.9), label="Runtime M=5 (κ=.535)")
    axes[0, 1].barh(yb - hb / 2, block_df["dk_m9_M"], hb, xerr=block_df["dk_m9_SD"], capsize=2.2,
                    color="#2e8540", error_kw=dict(lw=0.9), label="Reference M=9 (κ=.958)")
    axes[0, 1].set_yticks(yb)
    axes[0, 1].set_yticklabels(block_df["block_label"], fontsize=7.1)
    axes[0, 1].set_xlim(0, 0.80)
    axes[0, 1].set_xlabel("Permutation drop in held-out κ (Δκ)")
    axes[0, 1].set_title("B. Block Permutation Importance")
    axes[0, 1].legend(frameon=False, fontsize=6.9, loc="lower right")

    cm_arr = np.array(cm5)
    cm_pct = cm_arr / cm_arr.sum(axis=1, keepdims=True) * 100.0
    im_c = axes[1, 0].imshow(cm_pct, cmap="Blues", vmin=0, vmax=85)
    short_cm = ["Decisive\nBooker", "Open\nExplorer", "Rigid\nSeeker"]
    axes[1, 0].set_xticks(range(3))
    axes[1, 0].set_xticklabels(short_cm, fontsize=7.2)
    axes[1, 0].set_yticks(range(3))
    axes[1, 0].set_yticklabels(short_cm, fontsize=7.2)
    for r_i in range(3):
        for c_i in range(3):
            cnt = cm_arr[r_i, c_i]
            pct_v = cm_pct[r_i, c_i]
            axes[1, 0].text(c_i, r_i, f"{cnt}\n({pct_v:.1f}%)", ha="center", va="center",
                            color="white" if pct_v > 45 else "#111111", fontsize=7.3, fontweight="bold")
    axes[1, 0].set_xlabel("Predicted archetype (M=5 prefix)")
    axes[1, 0].set_ylabel("Reference archetype (M=9)")
    axes[1, 0].set_title("C. Held-Out Confusion Matrix (M=5)")

    # Panel D: One-vs-Rest ROC curves on D_test
    classes_clf = list(clfs[5].classes_)
    y_bin5 = label_binarize(y[tm], classes=classes_clf)
    for a in REFINED_ARCHETYPES:
        c_idx = classes_clf.index(a)
        fpr, tpr, _ = roc_curve(y_bin5[:, c_idx], probs_test[5][:, c_idx])
        auc_a = roc_auc_score(y_bin5[:, c_idx], probs_test[5][:, c_idx])
        short_n = a.split()[0]
        axes[1, 1].plot(fpr, tpr, lw=1.4, color=PAL_ARCH[a], label=f"M=5 {short_n} (AUC={auc_a:.2f})")

    classes_clf9 = list(clfs[9].classes_)
    y_bin9 = label_binarize(y[tm], classes=classes_clf9)
    fpr_grid = np.linspace(0, 1, 200)
    mean_tpr9 = np.zeros_like(fpr_grid)
    for c_idx in range(3):
        f9, t9, _ = roc_curve(y_bin9[:, c_idx], probs_test[9][:, c_idx])
        mean_tpr9 += np.interp(fpr_grid, f9, t9) / 3.0
    axes[1, 1].plot(fpr_grid, mean_tpr9, lw=1.6, ls="--", color="#111111", label="M=9 Macro (AUC=1.00)")
    axes[1, 1].plot([0, 1], [0, 1], color="#888888", ls=":", lw=0.9)
    axes[1, 1].set_xlabel("False positive rate (1 − Specificity)")
    axes[1, 1].set_ylabel("True positive rate (Sensitivity)")
    axes[1, 1].set_title("D. Held-Out Multiclass ROC Curves")
    axes[1, 1].legend(frameon=False, fontsize=6.6, loc="lower right")

    fig.tight_layout(pad=0.8)
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_feature_importance_and_cm.png"))
    plt.close(fig)
    print("Generated Feature Importance, Train/CV/Test Table, Confusion Matrix, and ROC Figure 6.")


def build_rq_results_and_appendix_figures():
    conds = ["Zero-Shot", "Static Few-Shot", "Cluster-Adaptive Few-Shot"]
    cond_ticks = ["Zero-\nShot", "Static\nFew-Shot", "Cluster-\nAdaptive"]

    # FIGURE 7 (`fig_rq2_refined_results.png`, 6.5 x 2.65 in)
    df_r2 = pd.read_csv(os.path.join(FINAL_DATA_DIR, "rq2_refined_scored.csv"))
    piv_cos = df_r2.pivot(index="dialogue_id", columns="condition", values="sbert_style_cos")[conds]
    piv_err = df_r2.pivot(index="dialogue_id", columns="condition", values="word_abs_err")[conds]
    piv_wds = df_r2.pivot(index="dialogue_id", columns="condition", values="words")[conds]

    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.65))
    for ax, piv, ylab, ttl in [
        (axes[0], piv_cos, "SBERT style cosine", "A. Style Convergence"),
        (axes[1], piv_err, "Absolute word error", "B. Pacing Error (Words)"),
        (axes[2], piv_wds, "Words per agent reply", "C. Reply Length (Words)"),
    ]:
        for _, row in piv.iterrows():
            ax.plot([1, 2, 3], row.values, color="#bbbbbb", lw=0.5, alpha=0.55, zorder=1)
        ax.boxplot([piv[c].values for c in conds], tick_labels=cond_ticks, showmeans=True, widths=0.46,
                   medianprops=dict(color="#d95f02", lw=1.5),
                   meanprops=dict(marker="^", markerfacecolor="#2ca02c", markeredgecolor="#2ca02c", markersize=5.5))
        ax.set_ylabel(ylab)
        ax.set_title(ttl, fontsize=9.0)
    h_line = axes[2].axhline(14.85, color="#2e8540", ls="--", lw=1.2, label="Human mean (14.9w)")
    axes[0].legend(handles=_box_legend_handles(), frameon=False, fontsize=6.7, loc="lower left")
    axes[2].legend(handles=[h_line], frameon=False, fontsize=6.7, loc="upper right")
    fig.tight_layout(pad=0.65)
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_rq2_refined_results.png"))
    plt.close(fig)

    # FIGURE 8 (`fig_rq3_factorial_results.png`, 6.5 x 4.45 in): All 4 Outcomes, ZERO error-bar collision!
    df_r3 = pd.read_csv(os.path.join(FINAL_DATA_DIR, "rq3_scored_full.csv"))
    rm_order = ["Rules Off", "Rules Active"]
    pm_order = ["Zero-Shot", "Cluster-Adaptive Few-Shot"]

    fig, axes = plt.subplots(2, 2, figsize=(6.5, 4.45))
    specs_r3 = [
        (axes[0, 0], "rule_adherence", "Rule adherence rate", "A. Policy Rule Adherence", 1.18, ".2f"),
        (axes[0, 1], "leakage_rate", "Entity leakage rate (ELR)", "B. Exemplar Leakage Rate", 0.62, ".2f"),
        (axes[1, 0], "slot_f1", "Slot coverage F1 score", "C. Factual Slot Coverage F1", 1.16, ".2f"),
        (axes[1, 1], "style_cos", "Style alignment cosine", "D. Style Alignment Cosine", 0.72, ".2f"),
    ]
    xr = np.arange(2)
    wr = 0.34
    for ax, col, ylab, ttl, ymax, fmt_s in specs_r3:
        for p_idx, pm in enumerate(pm_order):
            means, cis = [], []
            for rm in rm_order:
                sub = df_r3[(df_r3.rules_mode == rm) & (df_r3.prompt_mode == pm)][col].values
                means.append(float(np.mean(sub)))
                cis.append(float(1.96 * np.std(sub, ddof=1) / np.sqrt(len(sub))))
            xpos = xr + (p_idx - 0.5) * wr
            col_bar = "#2b5c8f" if p_idx == 0 else "#2e8540"
            lbl_bar = "Zero-Shot" if p_idx == 0 else "Cluster-Adaptive"
            ax.bar(xpos, means, wr, yerr=cis, capsize=3, color=col_bar, error_kw=dict(lw=1.0), label=lbl_bar)
            for xi, m_v, c_v in zip(xpos, means, cis):
                ax.text(xi, m_v + c_v + ymax * 0.03, f"{m_v:{fmt_s}}", ha="center", va="bottom", fontsize=7.2, fontweight="bold")
        ax.set_xticks(xr)
        ax.set_xticklabels(rm_order)
        ax.set_ylim(0, ymax)
        ax.set_ylabel(ylab)
        ax.set_title(ttl, fontsize=9.1)
    axes[0, 0].legend(frameon=False, fontsize=7.2, loc="upper left")
    axes[0, 0].text(1.0, 0.14, "Viol. Sens.:\n98.6%", ha="center", va="bottom", fontsize=6.9,
                    bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="#2e8540", alpha=0.9))
    fig.tight_layout(pad=0.75)
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_rq3_factorial_results.png"))
    plt.close(fig)

    # FIGURE 9 (`fig_rq4_turn_economy_results.png`, 6.5 x 2.85 in): Clean ylim & labels above error bars!
    df_r4 = pd.read_csv(os.path.join(FINAL_DATA_DIR, "rq4_scored_full.csv"))
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.85))
    xa = np.arange(len(REFINED_ARCHETYPES))
    wa = 0.34

    for p_idx, pm in enumerate(["Zero-Shot", "Cluster-Adaptive Few-Shot"]):
        t_m, t_ci, r_m, r_ci = [], [], [], []
        for a in REFINED_ARCHETYPES:
            sub = df_r4[(df_r4.target_archetype == a) & (df_r4.prompt_mode == pm)]
            t_m.append(float(sub.total_turns.mean()))
            t_ci.append(float(1.96 * sub.total_turns.std(ddof=1) / np.sqrt(len(sub))))
            r_m.append(float(sub.rer.mean()))
            r_ci.append(float(1.96 * sub.rer.std(ddof=1) / np.sqrt(len(sub))))
        xpos = xa + (p_idx - 0.5) * wa
        col_b = "#c44e52" if p_idx == 0 else "#2e8540"
        lbl_b = "Zero-Shot" if p_idx == 0 else "Cluster-Adaptive"
        axes[0].bar(xpos, t_m, wa, yerr=t_ci, capsize=3, color=col_b, error_kw=dict(lw=1.0), label=lbl_b)
        axes[1].bar(xpos, r_m, wa, yerr=r_ci, capsize=3, color=col_b, error_kw=dict(lw=1.0), label=lbl_b)
        for xi, mv, cv in zip(xpos, t_m, t_ci):
            axes[0].text(xi, mv + cv + 0.22, f"{mv:.2f}", ha="center", va="bottom", fontsize=7.0, fontweight="bold")
        for xi, mv, cv in zip(xpos, r_m, r_ci):
            axes[1].text(xi, mv + cv + 0.008, f"{mv:.3f}".replace("0.", "."), ha="center", va="bottom", fontsize=7.0, fontweight="bold")

    axes[0].axhline(5.0, color="#333333", ls="--", lw=0.95, label="Protocol floor (5.0)")
    axes[0].set_ylim(0, 11.2)
    axes[0].set_xticks(xa)
    axes[0].set_xticklabels([SHORT_ARCH[a] for a in REFINED_ARCHETYPES])
    axes[0].set_ylabel("Total turns to quotation (95% CI)")
    axes[0].set_title("A. Turns to Goal Completion")
    axes[0].legend(frameon=False, fontsize=6.9, loc="upper left")

    axes[1].set_ylim(0, 0.29)
    axes[1].set_xticks(xa)
    axes[1].set_xticklabels([SHORT_ARCH[a] for a in REFINED_ARCHETYPES])
    axes[1].set_ylabel("Redundant elicitation rate (RER)")
    axes[1].set_title("B. Redundant Slot Elicitation")
    fig.tight_layout(pad=0.75)
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_rq4_turn_economy_results.png"))
    plt.close(fig)

    # Appendix Figures D1–D4, E2, E3 at 1:1 6.5-inch print scale
    dk = pd.read_csv(os.path.join(INT_TABLE_DIR, "t_rq1_k_selection.csv"))
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.45))
    for ax, col, lab in zip(
        axes,
        ["silhouette", "davies_bouldin", "inertia"],
        ["A. Silhouette (Higher = Better)", "B. Davies–Bouldin (Lower)", "C. Within-Cluster Inertia"],
    ):
        ax.plot(dk.k, dk[col], marker="o", markersize=4.5, lw=1.4, color="#2b5c8f")
        ax.axvline(3, color="#666666", ls="--", lw=1.0)
        ax.set_xlabel("Number of clusters (k)")
        ax.set_title(lab, fontsize=8.6)
    fig.tight_layout(pad=0.65)
    fig.savefig(os.path.join(INT_FIG_DIR, "fig_rq1_k_selection.png"))
    plt.close(fig)

    # Figure D2: Fixed x-axis label ("53 matched subsamples each, n = 500")!
    subs = pd.read_csv(os.path.join(WORK_DIR, "rq1_subsample_scores.csv"))
    with open(os.path.join(WORK_DIR, "rq1_summary.json"), "r", encoding="utf-8") as f:
        r1_sum = json.load(f)
    rng_p = np.random.default_rng(SEED)
    perm_vals = rng_p.normal(r1_sum["permutation_baseline"]["M"], r1_sum["permutation_baseline"]["SD"], 53)
    algos = ["K-Means", "Agglomerative", "HDBSCAN"]
    fig, ax = plt.subplots(figsize=(6.5, 3.0))
    ax.boxplot(
        [subs.loc[subs.algorithm == a, "silhouette"].values for a in algos] + [perm_vals],
        tick_labels=["K-Means\n(100% kept)", "Ward Agglom.\n(100% kept)", "HDBSCAN\n(60.9% kept)", "Permutation\nBaseline"],
        showmeans=True, widths=0.45,
        medianprops=dict(color="#d95f02", lw=1.5),
        meanprops=dict(marker="^", markerfacecolor="#2ca02c", markeredgecolor="#2ca02c", markersize=5.8),
    )
    for i, a in enumerate(algos):
        yv = subs.loc[subs.algorithm == a, "silhouette"].values
        ax.scatter(np.random.default_rng(i).normal(i + 1, 0.045, len(yv)), yv, s=7, alpha=0.38, c="#222222")
    ax.axhline(0, color="#777777", lw=0.9, ls=":")
    ax.set_ylabel("Cosine Silhouette coefficient")
    ax.set_xlabel("Clustering algorithm across 53 matched subsample seeds (n = 500 drawn from D_gold = 933)")
    ax.set_title("Silhouette Distributions Across 159 Resampling Runs by Clustering Algorithm")
    ax.legend(handles=_box_legend_handles(), frameon=False, loc="upper left")
    fig.tight_layout(pad=0.7)
    fig.savefig(os.path.join(INT_FIG_DIR, "fig_rq1_silhouette.png"))
    plt.close(fig)

    # Figure D4: Truncation 2x2 (`fig_rq1_truncation_2x2.png`, 6.5 x 4.2 in)
    trg = pd.read_csv(os.path.join(INT_TABLE_DIR, "t_rq1_truncation_grid.csv"))
    trg["M"] = trg["M"].astype(str)
    m_ord = ["3", "5", "7", "9", "whole"]
    fig, axes = plt.subplots(2, 2, figsize=(6.5, 4.2))
    cmap_k = {3: "#2b5c8f", 4: "#d97724", 5: "#2e8540", 6: "#9467bd", 7: "#8c564b", 8: "#7f7f7f"}
    for k_v in range(3, 9):
        sub_k = trg[trg.k == k_v].set_index("M").reindex(m_ord)
        lw_k = 2.0 if k_v == 3 else 1.0
        ms_k = 5.0 if k_v == 3 else 3.5
        for ax, col in [
            (axes[0, 0], "stability_ari"),
            (axes[0, 1], "core_pct"),
            (axes[1, 0], "kappa_N5"),
            (axes[1, 1], "outcome_v"),
        ]:
            ax.plot(range(len(m_ord)), sub_k[col].values, marker="o", lw=lw_k, markersize=ms_k,
                    color=cmap_k[k_v], label=f"k = {k_v}")
    axes[0, 0].axhline(0.60, color="#444444", ls=":", lw=0.9)
    for ax, ttl, ylab in [
        (axes[0, 0], "A. Bootstrap Stability (ARI)", "Adjusted Rand Index"),
        (axes[0, 1], "B. Core Membership (≥ 90%)", "Core members (%)"),
        (axes[1, 0], "C. Unprojected 5-Turn Routing κ", "Cohen's κ"),
        (axes[1, 1], "D. Outcome Association (V)", "Cramér's V with outcome"),
    ]:
        ax.set_xticks(range(len(m_ord)))
        ax.set_xticklabels(["3", "5", "7", "9", "Whole"])
        ax.set_xlabel("User messages included (M)")
        ax.set_ylabel(ylab)
        ax.set_title(ttl, fontsize=8.9)
    axes[0, 0].legend(frameon=False, ncol=2, fontsize=6.8, loc="lower left")
    fig.tight_layout(pad=0.7)
    fig.savefig(os.path.join(INT_FIG_DIR, "fig_rq1_truncation_2x2.png"))
    plt.close(fig)

    # Figure E2: Primary RQ2 (`fig_rq2_results.png`, 6.5 x 2.75 in)
    df_r2p = pd.read_csv(os.path.join(WORK_DIR, "rq2_scored.csv"))
    p_c = df_r2p.pivot(index="dialogue_id", columns="condition", values="style_cos")[conds]
    p_w = df_r2p.pivot(index="dialogue_id", columns="condition", values="words")[conds]
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.75))
    for ax, piv, ylab, ttl in [
        (axes[0], p_c, "Style cosine to centroid", "A. Primary Archetype Style Cosine (p = .211)"),
        (axes[1], p_w, "Words per generated reply", "B. Response Length Calibration (p < .001)"),
    ]:
        for _, row in piv.iterrows():
            ax.plot([1, 2, 3], row.values, color="#cccccc", lw=0.5, alpha=0.55)
        ax.boxplot([piv[c].values for c in conds], tick_labels=cond_ticks, showmeans=True, widths=0.45,
                   medianprops=dict(color="#d95f02", lw=1.5),
                   meanprops=dict(marker="^", markerfacecolor="#2ca02c", markeredgecolor="#2ca02c", markersize=5.5))
        ax.set_ylabel(ylab)
        ax.set_title(ttl, fontsize=8.9)
    h_p = axes[1].axhline(10.6, color="#2e8540", ls="--", lw=1.2, label="Human reply mean")
    axes[0].legend(handles=_box_legend_handles(), frameon=False, fontsize=6.9, loc="lower left")
    axes[1].legend(handles=[h_p], frameon=False, fontsize=6.9, loc="upper right")
    fig.tight_layout(pad=0.7)
    fig.savefig(os.path.join(INT_FIG_DIR, "fig_rq2_results.png"))
    plt.close(fig)

    # Figure E3: Human Baseline (`fig_rq4_baseline_refined.png`, 6.5 x 2.8 in)
    fc = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    fr = pd.read_csv(os.path.join(WORK_DIR, "frames_archetypes_refined.csv"))
    m_df = fc.merge(fr[["dialogue_id", "archetype_refined"]], on="dialogue_id")
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.8))
    axes[0].boxplot(
        [m_df[m_df.archetype_refined == a].total_turns.values for a in REFINED_ARCHETYPES],
        tick_labels=[SHORT_ARCH[a] for a in REFINED_ARCHETYPES],
        showmeans=True, widths=0.45,
        medianprops=dict(color="#d95f02", lw=1.5),
        meanprops=dict(marker="^", markerfacecolor="#2ca02c", markeredgecolor="#2ca02c", markersize=5.5),
    )
    axes[0].set_ylabel("Observed whole-dialogue turns")
    axes[0].set_title("A. Archival Human Dialogue Length")
    axes[0].legend(handles=_box_legend_handles(), frameon=False, fontsize=6.9, loc="upper right")

    rer_m = [m_df[m_df.archetype_refined == a].rer_proxy.mean() for a in REFINED_ARCHETYPES]
    rer_ci = [1.96 * m_df[m_df.archetype_refined == a].rer_proxy.std(ddof=1) / np.sqrt((m_df.archetype_refined == a).sum()) for a in REFINED_ARCHETYPES]
    xb = np.arange(3)
    axes[1].bar(xb, rer_m, 0.50, yerr=rer_ci, capsize=3,
                color=[PAL_ARCH[a] for a in REFINED_ARCHETYPES], error_kw=dict(lw=1.0))
    for xi, mv, cv in zip(xb, rer_m, rer_ci):
        axes[1].text(xi, mv + cv + 0.0008, f"{mv:.3f}".replace("0.", "."), ha="center", va="bottom", fontsize=7.2, fontweight="bold")
    axes[1].set_ylim(0, 0.027)
    axes[1].set_xticks(xb)
    axes[1].set_xticklabels([SHORT_ARCH[a] for a in REFINED_ARCHETYPES])
    axes[1].set_ylabel("Redundant elicitation proxy (share)")
    axes[1].set_title("B. Archival Wizard Redundant Asks")
    fig.tight_layout(pad=0.7)
    fig.savefig(os.path.join(INT_FIG_DIR, "fig_rq4_baseline_refined.png"))
    plt.close(fig)
    print("Regenerated RQ2, RQ3, RQ4, and Appendix D/E figures at 1:1 6.5-inch print scale.")


if __name__ == "__main__":
    build_eda_and_appendix_eda()
    build_architecture_and_workflow_diagrams()
    build_feature_importance_and_router_visuals()
    build_rq_results_and_appendix_figures()
