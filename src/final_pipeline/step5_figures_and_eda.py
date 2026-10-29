"""
Step 8 - Generate all new EDA (Univariate, Bivariate, Multivariate) tables/figures and
System Architecture / Per-RQ Workflow diagrams required by the QM640 Final Report Template
and Master Submission Checklist.

Outputs:
  - `outputs/final/tables/t_eda_bivariate_correlations.csv`
  - `outputs/final/tables/t_eda_multivariate_loadings.csv`
  - `outputs/final/figures/fig_eda_bivariate.png`
  - `outputs/final/figures/fig_eda_multivariate.png`
  - `outputs/final/figures/fig_system_architecture.png`
  - `outputs/final/figures/fig_rq_workflows_4panel.png`
"""

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(ROOT, "src"), os.path.join(ROOT, "src", "interim_pipeline")):
    if p not in sys.path:
        sys.path.insert(0, p)

from common import WORK_DIR  # noqa: E402
from final_pipeline.common_llm import FINAL_DATA_DIR, FINAL_FIG_DIR, FINAL_TABLE_DIR  # noqa: E402
from final_pipeline.routing import REFINED_ARCHETYPES  # noqa: E402
from step2f_rq1_llm_hybrid import ORD, load_ann  # noqa: E402

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 10,
})


def build_eda_bivariate_and_multivariate():
    df_clean = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    df_ref = pd.read_csv(os.path.join(WORK_DIR, "frames_archetypes_refined.csv"))
    ann9 = load_ann(os.path.join(WORK_DIR, "llm_user_annotations_u9.jsonl")).loc[df_clean.dialogue_id]

    df = df_clean.merge(
        df_ref[["dialogue_id", "archetype_refined", "archetype_primary"]],
        on="dialogue_id",
    )
    df["revisions_count"] = df["revisions"]
    df["agent_offers"] = df["offers"]
    df["hesitation_markers_count"] = df["hesitations"]
    for col in ORD:
        df[col] = ann9[col].astype(float).values

    # 1. Bivariate Correlation Table (`t_eda_bivariate_correlations.csv`)
    biv_pairs = [
        ("total_turns", "revisions_count", "Total Turns vs. Slot Revisions"),
        ("total_turns", "agent_offers", "Total Turns vs. Agent Package Offers"),
        ("total_turns", "hesitation_markers_count", "Total Turns vs. User Hesitation Markers"),
        ("revisions_count", "exploration_breadth", "Slot Revisions vs. Exploration Breadth Rating"),
        ("total_turns", "decisiveness", "Total Turns vs. User Decisiveness Rating"),
        ("mean_user_words", "information_upfront", "User Words/Turn vs. Information Up Front Rating"),
        ("agent_offers", "destination_flexibility", "Agent Offers vs. Destination Flexibility Rating"),
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

    # Figure: Bivariate EDA (`fig_eda_bivariate.png`)
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.3), dpi=300)
    palette = {
        "Decisive Booker": "#4c72b0",
        "Open Explorer": "#dd8452",
        "Rigid-Constraint Seeker": "#55a868",
    }
    for arch in REFINED_ARCHETYPES:
        sub = df[df.archetype_refined == arch]
        axes[0].scatter(
            sub.total_turns + np.random.default_rng(42).normal(0, 0.25, len(sub)),
            sub.revisions_count + np.random.default_rng(43).normal(0, 0.25, len(sub)),
            s=14, alpha=0.45, color=palette[arch], label=arch,
        )
    slope, intercept, r_val, _, _ = stats.linregress(df.total_turns, df.revisions_count)
    xs = np.linspace(df.total_turns.min(), df.total_turns.max(), 100)
    axes[0].plot(xs, intercept + slope * xs, color="black", ls="--", lw=1.3, label=f"OLS trend (r = {r_val:.2f})")
    axes[0].set_xlabel("Dialogue Length (Total Turns)")
    axes[0].set_ylabel("Cumulative Slot-Value Revisions (Count)")
    axes[0].set_title("A. Bivariate: Dialogue Turns vs. Slot Revisions")
    axes[0].legend(frameon=False, fontsize=8)

    # Panel B: Agent Offers & Revisions by Refined Archetype
    x = np.arange(len(REFINED_ARCHETYPES))
    w = 0.34
    rev_means = [df[df.archetype_refined == a].revisions_count.mean() for a in REFINED_ARCHETYPES]
    rev_cis = [1.96 * df[df.archetype_refined == a].revisions_count.std(ddof=1) / np.sqrt((df.archetype_refined == a).sum()) for a in REFINED_ARCHETYPES]
    off_means = [df[df.archetype_refined == a].agent_offers.mean() for a in REFINED_ARCHETYPES]
    off_cis = [1.96 * df[df.archetype_refined == a].agent_offers.std(ddof=1) / np.sqrt((df.archetype_refined == a).sum()) for a in REFINED_ARCHETYPES]

    axes[1].bar(x - w / 2, rev_means, w, yerr=rev_cis, capsize=4, color="#4c72b0", label="Slot revisions (count)")
    axes[1].bar(x + w / 2, off_means, w, yerr=off_cis, capsize=4, color="#dd8452", label="Agent package offers (count)")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels([a.replace("Rigid-Constraint Seeker", "Rigid-Constraint\nSeeker") for a in REFINED_ARCHETYPES])
    axes[1].set_ylabel("Mean Count per Dialogue (95% CI)")
    axes[1].set_title("B. Bivariate: Negotiation Intensity by Archetype")
    axes[1].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_eda_bivariate.png"))
    plt.close(fig)

    # 2. Multivariate EDA (`fig_eda_multivariate.png` & `t_eda_multivariate_loadings.csv`)
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

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.8), dpi=300)
    im = axes[0].imshow(corr_mat, cmap="RdBu_r", vmin=-0.8, vmax=0.8)
    axes[0].set_xticks(range(len(mv_labels)))
    axes[0].set_xticklabels(mv_labels, rotation=45, ha="right", fontsize=8)
    axes[0].set_yticks(range(len(mv_labels)))
    axes[0].set_yticklabels(mv_labels, fontsize=8)
    for i in range(len(mv_labels)):
        for j in range(len(mv_labels)):
            val = corr_mat[i, j]
            axes[0].text(j, i, f"{val:.2f}", ha="center", va="center",
                         color="white" if abs(val) > 0.45 else "black", fontsize=6.5)
    axes[0].set_title("A. Multivariate Spearman Correlation Matrix")
    fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.04)

    for arch in REFINED_ARCHETYPES:
        m = (df.archetype_refined == arch).values
        axes[1].scatter(Z_pca[m, 0], Z_pca[m, 1], s=12, alpha=0.40, color=palette[arch], label=arch)
    # Plot top loading vectors as biplot arrows
    scale = 4.2
    for idx_v in [0, 1, 4, 5, 6, 9]:
        lx, ly = pca.components_[0, idx_v] * scale, pca.components_[1, idx_v] * scale
        axes[1].annotate(
            "", xy=(lx, ly), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
        )
        axes[1].text(lx * 1.12, ly * 1.12, mv_labels[idx_v], fontsize=7.5, ha="center", va="center", fontweight="bold")
    axes[1].set_xlabel(f"PC1 ({100 * pca.explained_variance_ratio_[0]:.1f}% variance: Exploration vs. Rigidity)")
    axes[1].set_ylabel(f"PC2 ({100 * pca.explained_variance_ratio_[1]:.1f}% variance: Decisiveness & Politeness)")
    axes[1].set_title("B. Multivariate PCA Biplot of Behavioral & Structural Features")
    axes[1].legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_eda_multivariate.png"))
    plt.close(fig)

    with open(os.path.join(FINAL_DATA_DIR, "eda_summary_ext.json"), "w", encoding="utf-8") as f:
        json.dump(dict(
            bivariate=biv_df.to_dict("records"),
            pca_var_explained=[float(x) for x in pca.explained_variance_ratio_],
            loadings=loadings_df.to_dict("records"),
        ), f, indent=2)
    print("Generated bivariate and multivariate EDA tables and figures.")


def _draw_box(ax, x, y, w, h, title, subtitle, fc="#e8f0f8", ec="#2b5c8f", title_fs=9.0, sub_fs=7.8):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.02",
        facecolor=fc, edgecolor=ec, linewidth=1.4,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center", fontsize=title_fs, fontweight="bold", color="#111111")
    ax.text(x + w / 2, y + h * 0.28, subtitle, ha="center", va="center", fontsize=sub_fs, color="#222222")


def _draw_arrow(ax, x1, y1, x2, y2, label=""):
    arr = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>,head_length=6,head_width=4", lw=1.4, color="#333333")
    ax.add_patch(arr)
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.025, label, ha="center", va="bottom", fontsize=7.5, style="italic")


def build_architecture_and_workflow_diagrams():
    # 1. End-to-End System Architecture (`fig_system_architecture.png`)
    fig, ax = plt.subplots(figsize=(12.5, 5.6), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Top row: Offline Data Ingestion, Preprocessing, EDA, and Archetype Learning (Stages 1-4)
    ax.text(0.02, 0.94, "OFFLINE DATA PIPELINE & ARCHETYPE DISCOVERY (Golden Partition D_gold, n = 933)",
            fontsize=9.5, fontweight="bold", color="#1f4e78")
    _draw_box(ax, 0.02, 0.70, 0.20, 0.19, "1. Data Sources",
              "Microsoft Frames (N=1,369)\nMultiWOZ 2.2 (N=1,500)\nPublic JSON Corpora", fc="#e8f1fa", ec="#2b5c8f")
    _draw_arrow(ax, 0.22, 0.795, 0.26, 0.795)
    _draw_box(ax, 0.26, 0.70, 0.21, 0.19, "2. Preprocessing & Schema",
              "Two-Tier Canonical Mapping\nSlot De-Lexicalization\n70/30 Stratified Split", fc="#e8f1fa", ec="#2b5c8f")
    _draw_arrow(ax, 0.47, 0.795, 0.51, 0.795)
    _draw_box(ax, 0.51, 0.70, 0.22, 0.19, "3. Feature Engineering",
              "S-BERT Decay Vectors (384-d)\nGemini User PCA-20 + 16-Field\nLLM Behavioral Codebook", fc="#fff2cc", ec="#b8860b")
    _draw_arrow(ax, 0.73, 0.795, 0.77, 0.795)
    _draw_box(ax, 0.77, 0.70, 0.21, 0.19, "4. Archetype Clustering (RQ1)",
              "K-Means / Ward / HDBSCAN\n3 Refined Archetypes (M=9)\nPer-Cluster FAISS Sub-Indices", fc="#d9ead3", ec="#38761d")

    # Vertical connectors from Offline Artifacts to Online Inference Pipeline
    _draw_arrow(ax, 0.875, 0.70, 0.875, 0.52, "Frozen Centroids\n& FAISS Indices")
    _draw_arrow(ax, 0.365, 0.70, 0.12, 0.52, "Held-Out Test\nDialogues (D_test, n=401)")

    # Middle/Bottom row: Online Adaptive Inference, Rule Verification, and Evaluation (Stages 5-7)
    ax.text(0.02, 0.55, "ONLINE ADAPTIVE PROMPTING, DECLARATIVE VERIFICATION & EVALUATION (Held-Out D_test)",
            fontsize=9.5, fontweight="bold", color="#274e13")
    _draw_box(ax, 0.02, 0.28, 0.20, 0.20, "5. Live Prefix Router",
              "Opening User Prefix (M=5)\nHybrid Blocks Logistic Router\n(Accuracy = 70.1%, κ = .53)", fc="#fff2cc", ec="#b8860b")
    _draw_arrow(ax, 0.22, 0.38, 0.26, 0.38)
    _draw_box(ax, 0.26, 0.28, 0.22, 0.20, "6a. Dynamic Few-Shot (RQ2)",
              "Archetype FAISS Sub-Index (k=3)\nSlot-Masked Golden Exemplars\n+ Archetype Pacing Directive", fc="#d9ead3", ec="#38761d")
    _draw_arrow(ax, 0.48, 0.38, 0.52, 0.38)
    _draw_box(ax, 0.52, 0.28, 0.22, 0.20, "6b. Rule Verification (RQ3)",
              "External YAML Rule Engine\nVisa, Passport, Pax, Discount,\nBudget Checks + Entity Guard", fc="#f4cccc", ec="#990000")
    _draw_arrow(ax, 0.74, 0.38, 0.78, 0.38)
    _draw_box(ax, 0.78, 0.28, 0.20, 0.20, "7. Multi-Turn Agent & Eval",
              "LLM Response Generation\nStyle Cosine, Slot F1, Leakage,\nAdherence & Turn Economy (RQ4)", fc="#ead1dc", ec="#741b47")

    # Legend at bottom
    legend_items = [
        ("#e8f1fa", "#2b5c8f", "Data Ingestion & Canonicalization"),
        ("#fff2cc", "#b8860b", "Embedding, Feature Engineering & Prefix Routing"),
        ("#d9ead3", "#38761d", "Unsupervised Archetype Modeling & FAISS Retrieval"),
        ("#f4cccc", "#990000", "Deterministic Policy Verification Guardrail"),
        ("#ead1dc", "#741b47", "LLM Generation & Statistical Hypothesis Testing"),
    ]
    ax.text(0.02, 0.14, "Legend:", fontsize=8.5, fontweight="bold")
    lx = 0.09
    for fc, ec, lab in legend_items:
        rect = FancyBboxPatch((lx, 0.115), 0.022, 0.045, boxstyle="round,pad=0.005", facecolor=fc, edgecolor=ec, lw=1.1)
        ax.add_patch(rect)
        ax.text(lx + 0.028, 0.138, lab, fontsize=7.5, va="center")
        lx += 0.182 if "Deterministic" not in lab else 0.195

    fig.tight_layout()
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_system_architecture.png"))
    plt.close(fig)

    # 2. Four-Panel Per-RQ Workflow Diagram (`fig_rq_workflows_4panel.png`)
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 7.6), dpi=300)
    panel_specs = [
        (
            axes[0, 0],
            "A. RQ1 Workflow: Trajectory & Hybrid Archetype Discovery",
            [
                ("Step 1: Corpus & Split", "933 Golden / 401 Held-Out\nFrames Dialogues (Seed 42)", "#e8f1fa", "#2b5c8f"),
                ("Step 2: Representation", "Decay S-BERT (384-d) vs.\nGemini PCA-20 + 16 LLM Ratings", "#fff2cc", "#b8860b"),
                ("Step 3: 159-Run Benchmark", "K-Means, Ward, HDBSCAN\n53 Subsamples x 3 Algos", "#d9ead3", "#38761d"),
                ("Step 4: Validation", "One-Way ANOVA (F=91.33)\nStability ARI=.89, 3 Archetypes", "#ead1dc", "#741b47"),
            ],
        ),
        (
            axes[0, 1],
            "B. RQ2 Workflow: Dynamic Cluster-Adaptive Few-Shot Prompting",
            [
                ("Step 1: Prefix Input", "Held-Out Test Prefix (N=33)\nOpening 5 User Messages", "#e8f1fa", "#2b5c8f"),
                ("Step 2: Hybrid Router", "PCA-20 + Opening Profile\nRoutes to Archetype (κ=.53)", "#fff2cc", "#b8860b"),
                ("Step 3: 3 Prompt Arms", "Zero-Shot vs. Static (k=3)\nvs. Cluster-Adaptive (k=3)", "#d9ead3", "#38761d"),
                ("Step 4: RM-ANOVA Eval", "Style Cosine (F=9.79, p<.001)\nBERTScore & Pacing Calibration", "#ead1dc", "#741b47"),
            ],
        ),
        (
            axes[1, 0],
            "C. RQ3 Workflow: 2x2 Declarative Rule Engine vs. Prompting",
            [
                ("Step 1: State Injection", "N=144 Held-Out Dialogues\n50% Violating Tier-2 Rules", "#e8f1fa", "#2b5c8f"),
                ("Step 2: Rule Evaluation", "YAML Engine Checks 5 Rules\n(Visa, Passport, Pax, Disc, Budget)", "#f4cccc", "#990000"),
                ("Step 3: 2x2 Generation", "Rules (Off/Active) x Prompt\n(Zero-Shot/Cluster-Adaptive)", "#d9ead3", "#38761d"),
                ("Step 4: Dual-Judge ANOVA", "Adherence, Leakage & Slot F1\nFlash vs. Pro Reliability (κ)", "#ead1dc", "#741b47"),
            ],
        ),
        (
            axes[1, 1],
            "D. RQ4 Workflow: 2x3 Multi-Turn Turn-Economy Simulation",
            [
                ("Step 1: Goal & Persona", "N=180 Test Goals (30/Cell)\n3 Refined Archetype Personas", "#e8f1fa", "#2b5c8f"),
                ("Step 2: Agent Policies", "Zero-Shot vs. Cluster-Adaptive\n(Slot Ledger + Option Bundling)", "#d9ead3", "#38761d"),
                ("Step 3: Closed-Loop Chat", "Turn-by-Turn Simulation\nUntil Goal Met or Turn Cap", "#fff2cc", "#b8860b"),
                ("Step 4: 2x3 HC3 ANOVA", "Log Turns (TGC), Redundant\nElicitation (RER) & Persona Check", "#ead1dc", "#741b47"),
            ],
        ),
    ]
    for ax, title, boxes in panel_specs:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.text(0.02, 0.90, title, fontsize=10, fontweight="bold", color="#111111")
        xs = [0.02, 0.27, 0.52, 0.77]
        for i, (b_title, b_sub, fc, ec) in enumerate(boxes):
            _draw_box(ax, xs[i], 0.24, 0.21, 0.54, b_title, b_sub, fc=fc, ec=ec, title_fs=8.5, sub_fs=7.3)
            if i < 3:
                _draw_arrow(ax, xs[i] + 0.21, 0.51, xs[i + 1], 0.51)

    fig.tight_layout()
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_rq_workflows_4panel.png"))
    plt.close(fig)
    print("Generated system architecture and 4-panel RQ workflow diagrams.")


if __name__ == "__main__":
    build_eda_bivariate_and_multivariate()
    build_architecture_and_workflow_diagrams()
