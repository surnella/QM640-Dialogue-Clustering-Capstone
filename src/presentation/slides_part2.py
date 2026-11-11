"""
Part 2 of the QM640 Capstone Defense Presentation (Slides 25–48):
  - RQ1-Identify (RQ1 — IDENTIFY, Slides 25–33):
      * Slide 25: Cluster-Number Selection (k=2..8, Fig. D1) & 159-Run Silhouette Benchmark (Fig. D2)
      * Slide 26: Detailed Walkthrough of Table 14 (Why K-Means k=3 Wins, One-Way vs. Matched RM-ANOVA, Embedding Invariance)
      * Slide 27: Cross-Corpus Generalization (Fig. D3 & Table D4) & 3 Diagnostic Flaws in Whole-Dialogue Clustering
      * Slide 28: Representation × Truncation Breakthrough (Fig. D4 & Tables D5–D6: M=9 User Prefix + LLM Codebook)
      * Slide 29: 16-Field LLM Codebook Validation (Table C2) & 3-Tier Feature Importance Results (η², ‖β_j‖₂, Δκ)
      * Slide 30: Separated Train / 5-Fold Stratified CV / Held-Out Test Prefix Router Performance (Table 12 Walkthrough)
      * Slide 31: Held-Out Prefix Router 3×3 Confusion Matrices & Multiclass OvR ROC Curves (Fig. 6 & Table 13)
      * Slide 32: Full 16-Field Refined Archetype Profiles (Table 15), Centroid Naming (Table F1) & 3 Partitioned FAISS Indices
      * Slide 33: STORYLINE APPEARANCE #2 — End of RQ1-Identify Stage Pictorial Microsoft-Shapes Decision & Handoff Diagram
  - RQ2-Personalize (RQ2 — PERSONALIZE, Slides 34–37):
      * Slide 34: Causal Contrast Between Primary (p = .211, Fig. E2) and Refined (p < .001, Fig. 7) Archetypes
      * Slide 35: Detailed Walkthrough of Table 16 & Holm Contrasts (Why SBERT Moves While BERTScore Stays Flat, GG ε, Pacing 3.87w)
      * Slide 36: Why RQ2-Personalize Alone Is Incomplete: Style Succeeds (Green) While Unguarded Rules & Leakage Are Vulnerable (Orange)
      * Slide 37: STORYLINE APPEARANCE #3 — End of RQ2-Personalize Stage Pictorial Microsoft-Shapes Decision & Handoff Diagram
  - RQ3-Govern (RQ3 — GOVERN, Slides 38–42):
      * Slide 38: 2 × 2 Factorial Design (N=144), 5 Declarative YAML Rules (Table 9) & Dual-Judge Reliability (κ = .917, Table C3)
      * Slide 39: Visual Walkthrough of the 4-Panel 2 × 2 Interaction Profiles (Fig. 8)
      * Slide 40: Detailed Walkthrough of Table 17 (Violation Sensitivity 5.6%→98.6% vs. Specificity, Orthogonal Sum-Contrast SS = 1.162)
      * Slide 41: Concrete Dallas-to-Tokyo Side-by-Side Output Proof Across the 2 × 2 Cells (Red vs. Orange vs. Green)
      * Slide 42: STORYLINE APPEARANCE #4 — End of RQ3-Govern Stage Pictorial Microsoft-Shapes Decision & Handoff Diagram
  - RQ4-Optimize (RQ4 — OPTIMIZE, Slides 43–48):
      * Slide 43: 2 × 3 Closed-Loop Simulation Design (N=180), 4-Option Catalog & Blind Persona Audit (κ = .933, Table C3)
      * Slide 44: Visual Walkthrough of Multi-Turn Economy & Redundant Elicitation Profiles (Fig. 9)
      * Slide 45: Complete Table 18 Statistics & Structural Protocol Floor Analysis (5.00 Turns, SD = 0.00)
      * Slide 46: Deep-Dive Guide to Table 18 Columns & Rows (Why Both Raw & Log Turns, 2-Way ANOVA, Cohen's d & ηp²)
      * Slide 47: Reference Comparison Against Historical Human Travel Consultants in Microsoft Frames (Fig. E3 & Table E5)
      * Slide 48: STORYLINE APPEARANCE #5 — End of RQ4-Optimize Stage Complete 4-Stage Validated Solution Approach Diagram
"""

import os
from presentation.ppt_styles import (
    BLUE,
    CALLOUT_BG,
    CARD_ALT,
    CARD_BG,
    CORAL,
    GOLD,
    GREEN,
    GREEN_BG,
    NAVY,
    RED_BG,
    TEAL,
)
from presentation.storyline_slides import add_storyline_discovery_slide
from report.final_context import FIG_FIN, FIG_INT


def build_slides_part2(D, ctx):
    # =========================================================================
    # SLIDE 25: RQ1-IDENTIFY (RQ1 PART 1) — CLUSTER-NUMBER SELECTION & 159-RUN BENCHMARK FIGURES
    # =========================================================================
    s = D.content_slide(
        "5. RQ1-Identify Stage Results",
        "RQ1-Identify (Part 1): Cluster-Number Selection & 159-Run Silhouette Benchmark",
        "Figures D1 & D2: Why k = 3 satisfies the ≥ 20% adequacy rule and how K-Means, Ward, and HDBSCAN compare against a null baseline",
        notes="Walk through Figures D1 and D2 in detail. Explain how k=3 was selected on D_gold (n=933) and how the 159 subsample runs (53 per algorithm) were evaluated.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_k_selection.png"),
        0.35, 1.48, 6.15, 3.30,
        caption="Figure D1: Cluster-Number Selection (k = 2..8) on D_gold (k = 3 balances Silhouette & size ≥ 20%)",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_silhouette.png"),
        6.80, 1.48, 6.18, 3.30,
        caption="Figure D2: Cosine Silhouette Across 159 Subsample Runs (53 per Algorithm) vs. Permutation Null",
    )
    D.add_card(
        s, 0.35, 4.86, 6.15, 1.42,
        title="How to Read Figure D1 (Selecting k = 3 on D_gold = 933)",
        header_bg=NAVY,
        bullets=[
            "<b>Why Not `k = 2`?</b> Over-merges consultative explorers and constraint negotiators into one coarse bucket, hiding multi-option comparison behavior.",
            "<b>Why Not `k ≥ 4`?</b> At `k = 4..8`, the smallest cluster falls below the pre-declared <b>`≥ 20%` operational adequacy floor</b> (`11.2%–16.8%`) and Davies–Bouldin degrades (`> 3.25`).",
            "<b>Why `k = 3` Is Optimal:</b> Balances local Silhouette peak with balanced cluster shares (`42.3% / 37.6% / 20.0%` primary; `45.0% / 25.5% / 29.5%` refined).",
        ],
        font_size=8.9,
    )
    D.add_card(
        s, 6.80, 4.86, 6.18, 1.42,
        title="How to Read Figure D2 (159 Subsample Runs vs. Null Baseline)",
        header_bg=TEAL,
        bullets=[
            "<b>Experimental Protocol:</b> 53 independent 80% random subsamples (`n = 746` each) drawn from `D_gold (n = 933)` and clustered under `K-Means (k=3)`, `Ward (k=3)`, and `HDBSCAN` (`53 × 3 = 159` runs).",
            "<b>Permutation Null Baseline:</b> Randomly shuffling cluster assignments yields `Silhouette = −.013 (SD = .006)`—proving all three algorithms capture genuine geometric structure (`p < .001`).",
            "<b>The HDBSCAN Catch:</b> While `HDBSCAN` scores `.211*` on retained core points, it discards <b>`39.1%` of customers as unroutable `-1` noise</b>!",
        ],
        font_size=8.9,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ1-Identify Solution Approach Alignment (`Identify`):</b> "
        "Figures D1–D2 establish the first empirical branch of `RQ1-Identify`: `k ≥ 4` and `HDBSCAN` (`39.1%` customer drop-out) are closed (<b>Red</b>), while `k = 3` with `100%` customer coverage (`K-Means`) advances to the statistical test table (`Table 14`).",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 26: RQ1-IDENTIFY (RQ1 PART 2) — DETAILED WALKTHROUGH OF TABLE 14
    # =========================================================================
    s = D.content_slide(
        "5. RQ1-Identify Stage Results",
        "RQ1-Identify (Part 2): Detailed Walkthrough of Table 14 & Embedding Invariance",
        "Explaining every column and row of Table 14: One-Way ANOVA vs. Matched RM-ANOVA and MiniLM (384-d) vs. Gemini (3,072-d)",
        notes="Walk through every column and row of Table 14. Explain why both One-Way ANOVA and Matched RM-ANOVA are reported and why Row 1 (K-Means) and Row 6 (Gemini Document) win.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 2.75,
        headers=[
            "Embedding Family & Clustering Algorithm (Table 14)",
            "Runs",
            "Cosine Silhouette M (SD)",
            "Davies–Bouldin M (SD)",
            "Parametric Omnibus & Matched RM Tests",
            "Robust & Non-Parametric Checks",
            "η² / ηp²",
        ],
        rows=[
            [
                "1. MiniLM (384-d) — K-Means (k = 3) [Algorithm Winner: 100% Cov.]",
                "53",
                ".147 (.019)",
                "3.129 (0.113)",
                "One-way F(2, 156) = 91.33 (< .001)\nMatched RM F(1.72, 89.30) = 83.04 (< .001)",
                "Welch F(2, 89.15) = 66.98 (< .001)\nTukey & Games–Howell KM > Ward (< .001)",
                ".539 /\n.615",
            ],
            [
                "2. MiniLM (384-d) — Agglomerative (Ward, k = 3) [Dropped ✗]",
                "53",
                ".118 (.040)",
                "3.550 (0.269)",
                "Inferior separation & higher DB index\nthan K-Means across all 53 seeds",
                "Paired Friedman χ²(2) = 56.30 (< .001)\nKruskal–Wallis H(2) = 86.82 (< .001)",
                "—",
            ],
            [
                "3. MiniLM (384-d) — HDBSCAN (39.1% Noise Loss*) [Dropped ✗]",
                "53",
                ".211 (.044)*",
                "2.657 (0.241)*",
                "*Computed on 60.9% retained core only;\ndiscards 39.1% of customers as -1 noise",
                "Fails 100% live routing requirement\nin 53 / 53 default runs",
                "—",
            ],
            [
                "4. MiniLM (384-d) — Permutation Null Baseline",
                "53",
                "−.013 (.006)",
                "—",
                "Randomly shuffled labels confirm\non-chance separation (p < .001)",
                "—",
                "—",
            ],
            [
                "5. Gemini-001 (3,072-d Turn Pool) — KM / Ward / HDB*",
                "159",
                ".158 / .150 / .289*",
                "35.8% HDB noise*",
                "One-way F(2, 156) = 77.09 (< .001)",
                "Welch & Kruskal–Wallis p < .001",
                ".497",
            ],
            [
                "6. Gemini-001 (3,072-d Document) [Best Embedding Space ✓]",
                "159",
                ".161 / .213 / .345*",
                "25.7% HDB noise*",
                "One-way F(2, 156) = 127.47 (< .001)",
                "Highest Silhouette & largest η² (.620)",
                ".620",
            ],
        ],
        col_widths=[3.15, 0.55, 1.35, 1.25, 2.55, 2.65, 0.83],
        font_size=8.6,
        align_left_cols=(0, 4, 5),
        highlight_rows=(0, 4, 5),
    )
    D.add_card(
        s, 0.35, 4.30, 6.15, 1.98,
        title="Significance of the Columns: Why Report Both One-Way & Matched RM-ANOVA?",
        header_bg=NAVY,
        bullets=[
            "<b>1. Cosine Silhouette `M (SD)` vs. Davies–Bouldin `M (SD)`:</b> Silhouette (`[-1, +1]`, higher is better) measures cosine cohesion vs. separation; Davies–Bouldin (`≥ 0`, lower is better) measures within-cluster scatter relative to between-centroid distance.",
            "<b>2. Why Both One-Way ANOVA (`F = 91.33`) AND Matched RM-ANOVA (`F = 83.04`)?</b>",
            (1, "Because the 53 runs use the <b>exact same 53 random 80% subsample draws</b> across all 3 algorithms, `One-Way ANOVA` treats the 159 runs as independent (`η² = .539`), while `Matched RM-ANOVA` blocks on subsample seed (`GG ε = 0.86`, `ηp² = .615`, `Friedman χ² = 56.30, p < .001`), proving the algorithm ranking holds under both formulations!"),
        ],
        font_size=8.8,
    )
    D.add_card(
        s, 6.80, 4.30, 6.18, 1.98,
        title="Significance of the Rows: Comparing Row 1 → Row 5 → Row 6",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Why Row 1 (`K-Means k=3`) Beats Rows 2 & 3:</b> `Ward` (Row 2, `.118`) has significantly worse separation (`Tukey & Games–Howell p < .001`), while `HDBSCAN` (Row 3) abandons `39.1%` of shoppers as unroutable noise.",
            "<b>2. Why Row 6 (`Gemini-001 Document`) Beats Rows 1 & 5:</b> Moving from `MiniLM 384-d` (256-token window, `KM = .147, η² = .539`) to `Gemini 3,072-d Turn-Pool` (Row 5, `KM = .158`) and `Gemini 3,072-d Document` (Row 6, `KM = .161, F = 127.47, η² = .620`) yields the strongest geometric separation because Gemini encodes cross-turn context without token truncation.",
        ],
        font_size=8.8,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ1-Identify Solution Approach Alignment (`Identify — Reject H01 at p < .001`):</b> "
        "`Ward` and `HDBSCAN` are closed (<b>Red</b>). The winning algorithm (`K-Means k = 3` with 100% coverage) and winning embedding family (`Gemini-001 3,072-d`) advance to the diagnostic audit of whole-dialogue vs. prefix clustering.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 27: RQ1-IDENTIFY (RQ1 PART 3) — CROSS-CORPUS CHECK & WHOLE-DIALOGUE DIAGNOSTIC AUDIT
    # =========================================================================
    s = D.content_slide(
        "5. RQ1-Identify Stage Results",
        "RQ1-Identify (Part 3): Cross-Corpus Transfer & Diagnosis of Whole-Dialogue Clusters",
        "Figure D3 & Tables D3–D4: Why clustering whole transcripts caused wizard confounding (V = .45) and weak early routing (κ = .24)",
        notes="Show how testing the primary whole-dialogue clusters uncovered three crucial diagnostic flaws that motivated the prefix truncation + LLM behavioral codebook breakthrough.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_umap.png"),
        0.35, 1.48, 6.10, 4.78,
        caption="Figure D3: UMAP Projection of Frames Golden/Test Archetypes (Panel A) vs. MultiWOZ 2.2 Projection (Panel B)",
    )
    D.add_table(
        s, 6.60, 1.48, 6.38, 1.95,
        headers=["Partition / Corpus (Table D4)", "N", "Centroid Cosine M (SD)", "Direct Trans. (%)", "Constraint Neg. (%)", "Guided Exp. (%)"],
        rows=[
            ["Frames Golden (`D_gold`)", "933", ".466 (.116)", "42.3%", "37.6%", "20.0%"],
            ["Frames Held-Out (`D_test`)", "401", ".467 (.116)", "42.6%", "37.7%", "19.7%"],
            ["MultiWOZ 2.2 Sample", "1,499", ".269 (.115)", "71.4%", "28.6%", "0.1%"],
        ],
        col_widths=[1.75, 0.55, 1.35, 0.91, 0.91, 0.91],
        font_size=9.0,
        align_left_cols=(0,),
        highlight_rows=(0, 1),
    )
    D.add_card(
        s, 6.60, 3.52, 6.38, 2.74,
        title="Three Diagnostic Flaws Uncovered in Whole-Dialogue Clustering",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>Check 1 — Cross-Corpus Domain Specificity (Table D4):</b> Within Frames, Golden (`.466`) and Held-Out (`.467`) centroid similarity matched (`t = −0.10, p = .923`). Projecting MultiWOZ dropped similarity to `.269 (t = 28.08, p < .001)` with only `0.1%` Guided Explorers—proving consultative package archetypes are domain-specific.",
            "<b>Flaw 1 — Role-Player / Wizard Confounding (`Cramér's V = .45`):</b> Pooling user and wizard turns caused clusters to reflect <i>which human wizard</i> handled the chat rather than the customer's persona!",
            "<b>Flaw 2 — End-of-Dialogue Outcome Confounding (`Cramér's V = .29`):</b> Whole-dialogue vectors included Turn 15 closing acts (`Booked` vs. `No Option`), grouping chats by how they <i>ended</i> rather than how the user shops.",
            "<b>Flaw 3 — Near-Chance Early Prefix Routing (`39.4%, κ = .24`):</b> Because whole-dialogue clusters depended on late-turn outcomes, predicting them from opening turns failed (`κ = .24`)!",
        ],
        font_size=8.9,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ1-Identify Solution Approach Alignment (`Why Whole-Dialogue Clustering Is Closed [Red]`):</b> "
        "This diagnostic audit proves that clustering full transcripts (`Direct Transactional / Constraint Negotiator / Guided Explorer`) is a <b>dead end for live early-turn routing (`κ = .24`, Red node)</b>—requiring truncation to opening user messages (`M = 9`) and explicit behavioral profiling.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 28: RQ1-IDENTIFY (RQ1 PART 4) — THE REPRESENTATION × TRUNCATION BREAKTHROUGH
    # =========================================================================
    s = D.content_slide(
        "5. RQ1-Identify Stage Results",
        "RQ1-Identify (Part 4): The Representation × Truncation Breakthrough",
        "Figure D4 & Tables D5–D6: Truncating to M = 9 user messages and fusing PCA-20 Gemini prefixes with 13 LLM behavioral fields (`46-d Blocks`)",
        notes="Walk through Figure D4 and Tables D5-D6, showing how truncating to user-only prefixes (M=9) and joining PCA-20 Gemini embeddings with the LLM behavioral codebook solved all three diagnostic flaws.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_truncation_2x2.png"),
        0.35, 1.48, 6.20, 4.78,
        caption="Figure D4: Bootstrap ARI Stability (A), Core Membership (B), Prefix Routing κ (C), and Outcome V (D) Across M",
    )
    D.add_table(
        s, 6.70, 1.48, 6.28, 2.30,
        headers=["Modality Configuration at M = 9 User Msgs (Table D6)", "Dims", "Best k", "Bootstrap ARI", "Davies–Bouldin", "Core (≥80%)"],
        rows=[
            ["1. Gemini Prefix Embeddings Only (`PCA-20`) [Orange !]", "20", "3", ".39", "3.412", "61.4%"],
            ["2. LLM Behavioral Scales Only (10 Ord + 16 Cat)", "26", "3", ".67", "2.891", "81.2%"],
            ["3. Unweighted Concatenation (`PCA-20 + 26 LLM`)", "46", "3", ".78", "2.744", "85.6%"],
            ["4. Block-Weighted `46-d Blocks` (`w_ord = 1.5`) [Winner ✓]", "46", "3", ".89 (.87 abl.)", "2.647 (Lowest)", "93.1% (89.2%)"],
        ],
        col_widths=[2.65, 0.55, 0.55, 0.95, 0.88, 0.70],
        font_size=8.6,
        align_left_cols=(0,),
        highlight_rows=(3,),
    )
    D.add_table(
        s, 6.70, 3.88, 6.28, 2.38,
        headers=["Prefix Horizon m (Table D5)", "Chats > m", "Bootstrap ARI", "Test Agreement p_o (κ)", "p_o (≤m / >m Msgs)", "Outcome V"],
        rows=[
            ["m = 3 user msgs (≈ 5 turns)", "96.0%", ".57", "59.4% (κ = .359)", "87.5% / 58.2%", ".14"],
            ["m = 5 user msgs (≈ 9t — RQ2-Personalize Runtime)", "83.2%", ".84", "70.1% (κ = .535)", "81.8% / 67.8%", ".17"],
            ["m = 7 user msgs (≈ 13 turns)", "59.9%", ".85", "82.0% (κ = .722)", "93.2% / 74.6%", ".18"],
            ["m = 9 user msgs (Golden Reference X^(9))", "38.6%", ".89 (.87)", "97.3% (κ = .958)", "96.0% / 99.3%", ".20"],
            ["Whole conversation (Un-truncated)", "0.0%", ".62", "Confounded (κ = .24)", "—", ".29 (Leaky)"],
        ],
        col_widths=[1.85, 0.68, 0.78, 1.25, 1.05, 0.67],
        font_size=8.4,
        align_left_cols=(0,),
        highlight_rows=(1, 3),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ1-Identify Solution Approach Alignment (`Why 46-d Blocks at M = 9 Wins [Green]`):</b> "
        "Prefix embeddings alone (`ARI = .39`, <b>Orange node</b>) are too noisy, while whole-chat vectors (`V = .29`, <b>Red node</b>) leak outcomes. Fusing `PCA-20` user prefixes with the 13 clustering behavioral fields (`46-d Blocks` at `M = 9`) achieves <b>`ARI = .89 (.87 ablation)`, `93.1%` core stability, and lowest `DB = 2.647` at `k = 3` (Green node)</b>!",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 29: RQ1-IDENTIFY (RQ1 PART 5) — CODEBOOK VALIDATION & 3-TIER FEATURE IMPORTANCE RESULTS
    # =========================================================================
    s = D.content_slide(
        "5. RQ1-Identify Stage Results",
        "RQ1-Identify (Part 5): Codebook Validation & 3-Tier Feature Importance Results",
        "Table C2 & Section 5.1.4: Empirical results for Unsupervised η², Supervised L1 Router ‖β_j‖₂, and Block-Drop Routing Ablation Δκ",
        notes="Present the concrete empirical feature importance findings expanded in the Final Report (eta-squared, L1 weight norms, and block-drop delta-kappa).",
    )
    D.add_table(
        s, 0.35, 1.48, 6.35, 3.10,
        headers=[
            "Top Discriminating Features in `46-d Blocks`",
            "Block Type",
            "Tier 1: Cluster η² (F on D_gold)",
            "Tier 2: L1 Router ‖β_j‖₂ (M=5)",
            "Primary Archetype Separated",
        ],
        rows=[
            ["1. `decisiveness` (Field 4)", "Ordinal (1–5)", ".524 (F = 511.8***)", "2.84 (Rank 1)", "Decisive Booker (3.97 vs 2.58)"],
            ["2. `goal_specificity` (Field 11)", "Categorical", ".486 (F = 439.5***)", "2.52 (Rank 2)", "Decisive (99.3%) vs Explorer (50.8%)"],
            ["3. `revision_tendency` (Field 6)", "Ordinal (1–5)", ".412 (F = 325.9***)", "1.95 (Rank 5)", "Open Explorer (3.03 vs 2.00)"],
            ["4. `exploration_breadth` (Field 3)", "Ordinal (1–5)", ".389 (F = 296.1***)", "2.41 (Rank 3)", "Open Explorer (2.96 vs 1.59 Rigid)"],
            ["5. `destination_flexibility` (Field 1)", "Ordinal (1–5)", ".341 (F = 240.7***)", "2.19 (Rank 4)", "Open Explorer (3.49 vs 2.20 Rigid)"],
            ["6. `Gemini_PC1` (Semantic Intent)", "Embedding PC", ".318 (F = 216.8***)", "1.88 (Rank 6)", "Multi-city vs Single-package intent"],
            ["7. `politeness` (Field 8) & `date_flex` (Field 2)", "Ordinal (1–5)", ".294 / .268***", "1.64 / 1.51", "Rigid Seeker (3.07 / 2.18 lowest)"],
            ["8. Tail Embedding Components (`PC15–PC20`)", "Embedding PC", "< .015 (p > .10)", "0.00 (L1 Pruned!)", "Zeroed out by L1 sparsity penalty"],
        ],
        col_widths=[1.85, 0.95, 1.25, 1.10, 1.20],
        font_size=8.3,
        align_left_cols=(0, 1, 4),
        highlight_rows=(0, 1, 2, 3, 4, 5),
    )
    D.add_table(
        s, 6.85, 1.48, 6.13, 2.05,
        headers=[
            "Tier 3: Block-Drop Ablation on D_test (n = 401, M = 5)",
            "Dims Kept",
            "Test Acc (%)",
            "Cohen's κ",
            "Drop Δκ vs. Full",
        ],
        rows=[
            ["Full `46-d Blocks` (`PCA-20 + 10 Ord + 16 Cat`) [Winner ✓]", "46", "70.1%", ".535", "Baseline (0.000)"],
            ["Drop Gemini Embeddings (`Keep 26 LLM Behavioral Cols`)", "26", "66.8%", ".484", "−.051 (−3.3% acc)"],
            ["Drop Categorical Goal/Tone (`Keep PCA-20 + 10 Ord`)", "30", "65.8%", ".472", "−.063 (−4.3% acc)"],
            ["Drop 10 Ordinal Behavioral Scales (`Keep PCA-20 + 16 Cat`)", "36", "60.3%", ".387", "−.148 (−9.8% acc)"],
            ["Keep Gemini Prefix Embeddings Only (`PCA-20 Only`) [Orange !]", "20", "55.9%", ".312", "−.223 (−14.2% acc)"],
        ],
        col_widths=[2.55, 0.72, 0.88, 0.88, 1.10],
        font_size=8.3,
        align_left_cols=(0,),
        highlight_rows=(0, 3, 4),
    )
    D.add_card(
        s, 0.35, 4.68, 12.63, 1.60,
        title="Codebook Reliability (Table C2) & How Feature Importance Results Are Used Operationally",
        header_bg=TEAL,
        bullets=[
            "<b>1. LLM Codebook Reliability (`Table C2`):</b> Blind test–retest (`n = 50`) achieved quadratic weighted <b>`κ_w = .87 to .96` (mean `.91`)</b> across Ordinal Fields 1–10 and <b>`κ = .75 to .98`</b> across Categorical/Audit Fields 11–16. Ground-truth Frames act correlations confirmed criterion validity (`revision_tendency × slot_revisions ρ = .64`, `exploration_breadth × frame_switches ρ = .41`, `information_upfront × Turn-1 slots ρ = .52`, all `p < .001`).",
            "<b>2. Three Operational Uses of Feature Importance:</b> (a) <b>Block Weighting (`w_ord = 1.5`):</b> Because the 10 ordinal scales carry the largest discrimination (`η² = .268–.524`, `Δκ = −.148` when dropped), weighting them at `1.5` prevents 20 PCs from diluting them; (b) <b>L1 Router Sparsity:</b> L1 regularization automatically zeroes out noisy tail PCs (`PC15–PC20`, `η² < .015 → β_j = 0`); and (c) <b>Centroid Naming (`Table F1`):</b> Top-`η²` features (`destination_flexibility` & `decisiveness`) define the deterministic Python naming rules!",
        ],
        font_size=8.8,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ1-Identify Solution Approach Alignment (`Feature Importance → RQ1-Identify & RQ2-Personalize Handoff`):</b> "
        "Tier 3 ablation proves that dropping the LLM behavioral scales degrades live `M = 5` prefix routing from `κ = .535` down to `.312` (`Δκ = −.223`)—confirming why the hybrid `46-d Blocks` representation is mandatory before entering `RQ2-Personalize Stage`.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 30: RQ1-IDENTIFY (RQ1 PART 6) — SEPARATED TRAIN / 5-FOLD CV / HELD-OUT TEST ROUTING (TABLE 12)
    # =========================================================================
    s = D.content_slide(
        "5. RQ1-Identify Stage Results",
        "RQ1-Identify (Part 6): Train, 5-Fold CV & Held-Out Test Prefix Routing (Table 12)",
        "Evaluating the supervised L1 logistic prefix router across m ∈ {3, 5, 7, 9} user messages with zero overfitting across partitions",
        notes="Walk through Table 12 column by column, showing that D_gold Train (n=933), D_gold 5-Fold Stratified CV (n=933), and Held-Out D_test (n=401) agree closely at every prefix horizon m.",
    )
    D.add_table(
        s, 0.35, 1.48, 12.63, 2.85,
        headers=[
            "Prefix Horizon m (User Msgs / ≈ Total Turns)",
            "D_gold Train (n = 933)\nAcc (%) / κ / Macro-F1",
            "D_gold 5-Fold CV (n = 933)\nAcc (%) / κ / Macro-F1",
            "D_test Held-Out (n = 401)\nAcc (%) / κ / Macro-F1",
            "D_test Short (≤m) vs.\nLong (>m) Acc (%)",
            "Operational Role in the 4-Stage Solution Approach",
        ],
        rows=[
            [
                "m = 3 user msgs\n(≈ 5 total turns — Early Cold-Start)",
                "62.1% / .402 / .598",
                "60.1% / .371 / .576",
                "59.4% / .359 / .569",
                "87.5% (≤3 msgs) /\n58.2% (>3 msgs)",
                "Initial turn-3 routing (`+24.0%` above `35.4%` chance baseline); safe fallback before package comparison.",
            ],
            [
                "m = 5 user msgs\n(≈ 9 total turns — RQ2-Personalize Runtime)",
                "72.8% / .576 / .719",
                "70.8% / .545 / .699",
                "70.1% / .535 / .698",
                "81.8% (≤5 msgs) /\n67.8% (>5 msgs)",
                "<b>Adopted RQ2-Personalize Runtime Horizon:</b> Routes mid-conversation replies with `70.1%` accuracy (`κ = .535, p < .001`).",
            ],
            [
                "m = 7 user msgs\n(≈ 13 total turns — Mid-Negotiation)",
                "84.2% / .755 / .838",
                "82.5% / .729 / .821",
                "82.0% / .722 / .816",
                "93.2% (≤7 msgs) /\n74.6% (>7 msgs)",
                "High-precision mid-session routing (`κ = .722`) as exploratory frame switches accumulate.",
            ],
            [
                "m = 9 user msgs\n(≈ 17 turns — Golden Cap `min(M, 9)`)",
                "97.9% / .967 / .978",
                "97.1% / .955 / .970",
                "97.3% / .958 / .972",
                "96.0% (≤9 msgs) /\n99.3% (>9 msgs)",
                "<b>Same-Feature Boundary Consistency Check</b> on `X^(9)` (`97.3%` agreement; used for RQ3-Govern/4 archetype seeding).",
            ],
            [
                "Primary Whole-Chat Router\n(Baseline at Turn 3 without `Blocks`)",
                "44.2% / .281 / .410",
                "40.8% / .251 / .382",
                "39.4% / .240 / .368",
                "—",
                "<b>Closed Path (Red ✗):</b> Near-chance routing caused Primary RQ2-Personalize prompting to fail (`p = .211`).",
            ],
        ],
        col_widths=[2.15, 1.95, 1.95, 1.95, 1.65, 2.98],
        font_size=8.6,
        align_left_cols=(0, 5),
        highlight_rows=(1, 3),
    )
    D.add_card(
        s, 0.35, 4.43, 6.15, 1.85,
        title="Why Reporting Train, 5-Fold CV & Held-Out Test Together Matters",
        header_bg=NAVY,
        bullets=[
            "<b>1. Proof of Zero Overfitting:</b> Across all four horizons `m ∈ {3, 5, 7, 9}`, the gap between `D_gold` Train, `D_gold` 5-Fold Stratified CV, and Held-Out `D_test (n = 401)` is less than <b>`0.8% to 2.7%`</b> (e.g., at `m = 5`: `72.8% Train → 70.8% CV → 70.1% Test`).",
            "<b>2. Why?</b> Because L1 regularization (`C = 1.0`) prunes noisy tail PCs and the `PCA-20` + z-score scaler are fitted strictly on `D_gold` without peeking at `D_test`.",
        ],
        font_size=9.1,
    )
    D.add_card(
        s, 6.80, 4.43, 6.18, 1.85,
        title="How to Interpret Short (≤ m) vs. Long (> m) Dialogue Accuracy",
        header_bg=TEAL,
        bullets=[
            "<b>Why Are Short Chats (`≤ m` user messages) Even More Accurate (`81.8%–96.0%`)?</b>",
            (1, "When a dialogue has `≤ m` user messages (e.g., a fast 5-message booking), `min(m, M_i)` observes the traveler's complete user-turn history (`87.5%` at `m=3`; `81.8%` at `m=5`)."),
            (1, "Even on strictly truncated long conversations (`> m` user messages, where future turns are hidden), out-of-sample routing reaches <b>`67.8%` at `m = 5`</b>, <b>`74.6%` at `m = 7`</b>, and <b>`99.3%` at `m = 9`</b>!"),
        ],
        font_size=9.1,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ1-Identify Solution Approach Alignment (`Prefix Router Qualification → RQ2-Personalize`):</b> "
        "Table 12 proves that lifting held-out routing from `39.4% (κ = .240, Red)` to `70.1% at m = 5 (κ = .535, Green)` and `97.3% at m = 9 (κ = .958, Green)` is a genuine out-of-sample generalization gain, qualifying the `RefinedArchetypeRouter` for `RQ2-Personalize`.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 31: RQ1-IDENTIFY (RQ1 PART 7) — CONFUSION MATRIX & MULTICLASS ROC CURVES (FIGURE 6 & TABLE 13)
    # =========================================================================
    s = D.content_slide(
        "5. RQ1-Identify Stage Results",
        "RQ1-Identify (Part 7): Held-Out Confusion Matrices & Multiclass ROC Curves",
        "Figure 6 & Table 13: Per-archetype Precision, Recall, F1, and One-vs-Rest ROC-AUC on D_test (n = 401) at m = 5 and m = 9",
        notes="Walk through Figure 6 (Panels A-D) and Table 13, explaining the class-wise precision, recall, F1, and ROC-AUC curves on the 401 held-out test dialogues.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_feature_importance_and_cm.png"),
        0.35, 1.48, 6.45, 4.78,
        caption="Figure 6: Feature Importance (Panel A), Block Permutations (Panel B), Held-Out Confusion Matrix (Panel C) & Multiclass ROC (Panel D)",
    )
    D.add_table(
        s, 6.95, 1.48, 6.03, 2.75,
        headers=[
            "Horizon & Target Archetype (Table 13, D_test = 401)",
            "Support (n)",
            "Precision",
            "Recall",
            "F1-Score",
            "OvR ROC-AUC",
        ],
        rows=[
            ["m = 5 — Decisive Booker (DB)", "165", ".716", ".745", ".730", ".868"],
            ["m = 5 — Open Explorer (OE)", "140", ".689", ".643", ".665", ".841"],
            ["m = 5 — Rigid-Constraint Seeker (RCS)", "96", ".691", ".708", ".700", ".881"],
            ["m = 5 — Macro / Weighted Average", "401", ".699 / .701", ".699 / .701", ".698 / .700", ".863 / .862"],
            ["m = 9 — Decisive Booker (DB)", "165", ".970", ".988", ".979", ".999"],
            ["m = 9 — Open Explorer (OE)", "140", ".978", ".964", ".971", ".998"],
            ["m = 9 — Rigid-Constraint Seeker (RCS)", "96", ".968", ".958", ".963", ".998"],
            ["m = 9 — Macro / Weighted Average", "401", ".972 / .973", ".970 / .973", ".971 / .972", ".998 / .998"],
        ],
        col_widths=[2.25, 0.68, 0.75, 0.72, 0.75, 0.88],
        font_size=8.4,
        align_left_cols=(0,),
        highlight_rows=(3, 7),
    )
    D.add_card(
        s, 6.95, 4.33, 6.03, 1.93,
        title="Diagnostic Interpretation of Figure 6 & Table 13",
        header_bg=NAVY,
        bullets=[
            "<b>1. Balanced Class Discrimination at `m = 5` (Panels A–B):</b> Across all three personas on `D_test (n = 401)`, One-vs-Rest `ROC-AUC` reaches <b>`.868` (DB), `.841` (OE), and `.881` (RCS)</b> (`Macro ROC-AUC = .863`), with balanced `F1` scores (`.665–.730`).",
            "<b>2. Where Residual `m = 5` Errors Occur:</b> In Panel A, off-diagonal errors occur primarily between `Open Explorer` and `Decisive Booker` (`29` OE predicted as DB) when an explorer states an initial city at Turn 1–2 before requesting multi-city comparisons at Turn 6–8.",
            "<b>3. Near-Perfect Boundary Recovery at `m = 9` (Panels C–D):</b> By `m = 9`, `F1` reaches <b>`.963–.979` (`Macro ROC-AUC = .998`)</b>, with only `11 / 401` boundary cases misclassified.",
        ],
        font_size=8.7,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ1-Identify Solution Approach Alignment (`Confusion Matrix & ROC Proof → RQ2-Personalize & Doctoral Pillar 2`):</b> "
        "High multiclass `ROC-AUC (.863 at m=5; .998 at m=9)` confirms that RQ1-Identify's router reliably separates all 3 personas for `RQ2-Personalize` FAISS retrieval—while the `m=5 → m=7 → m=9` trajectory directly motivates <b>turn-by-turn Bayesian posterior updating in Doctoral Pillar 2</b>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 32: RQ1-IDENTIFY (RQ1 PART 8) — FULL 16-FIELD ARCHETYPE PROFILES & 3 FAISS INDICES
    # =========================================================================
    s = D.content_slide(
        "5. RQ1-Identify Stage Results",
        "RQ1-Identify (Part 8): 16-Field Archetype Profiles, Naming Rules & 3 FAISS Indices",
        "Tables 15 & F1: Complete profile of Decisive Booker, Open Explorer, and Rigid-Constraint Seeker and how the 3 FAISS sub-indices work",
        notes="Walk through Table 15 (all 16 UserBehaviour fields), explain how integer cluster IDs 0, 1, 2 are named via Table F1, and explain how 1 FAISS index per cluster (3 total) is constructed.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 3.42,
        headers=[
            "Schema Field Group & Attribute (All 16 Fields, Table 15)",
            "Archetype 1: Decisive Booker",
            "Archetype 2: Open Explorer",
            "Archetype 3: Rigid-Constraint Seeker",
            "How This Profile Drives RQ2–RQ4 Adaptation & FAISS Indexing",
        ],
        rows=[
            ["D_gold (n=933) / D_test (n=401) Share", "420 (45.0%) / 165 (41.1%)", "238 (25.5%) / 140 (34.9%)", "275 (29.5%) / 96 (23.9%)", "Builds <b>3 Partitioned FAISS `IndexFlatIP(46)` DBs</b> (`n=420, 238, 275`)"],
            ["Total Turns M (SD) / Wizard Words M", "14.96 (6.08) / 12.9w", "17.99 (6.65) / 18.6w", "10.64 (5.68) / 14.8w", "Sets RQ2-Personalize target word-pacing norms (`12.9w / 18.6w / 14.8w`)"],
            ["Fields 1–2 (ORD): Dest. / Date Flexibility", "2.54 / 2.57 (Moderate)", "<b>3.49</b> / 2.77 (Highest → OE)", "<b>2.20 / 2.18</b> (Lowest → RCS)", "`idxmax(dest_flex) = 3.49` deterministically names <i>Open Explorer</i>"],
            ["Fields 3–4 (ORD): Exploration / Decisiveness", "1.97 / <b>3.97</b> (Highest → DB)", "<b>2.96</b> / 2.58 (Broad, deliberative)", "1.59 / 3.23 (Narrow, firm)", "`idxmax(decisiveness) = 3.97` deterministically names <i>Decisive Booker</i>"],
            ["Fields 5–6 (ORD): Detail / Revision Tendency", "2.39 / 2.00 (Low revisions)", "2.87 / <b>3.03</b> (Frequent pivots)", "1.46 / 2.40 (Constraint focus)", "Drives RQ4-Optimize `3-Option Side-by-Side Comparison` for Explorers"],
            ["Fields 7–10 (ORD): Qs / Polite / Price / Upfront", "2.05 / <b>4.26</b> / 3.20 / <b>2.18</b>", "<b>2.72</b> / 3.80 / 3.18 / 1.82", "1.43 / 3.07 / 3.12 / 2.16", "Drives RQ4-Optimize `1-Option Direct Confirm` for Decisive Bookers"],
            ["Fields 11–13 (CAT Cluster): Goal / Sec. / Tone", "99.3% Book | 42.4% | 52.4% Pos", "39.1% Exp, 50.8% Book | 69.3% Neut", "89.8% Book | 16.4% | 7.6% Pos", "Encoded into 16 binary cols (`20 PC + 10 Ord + 16 Cat = 46-d Blocks`)"],
            ["Fields 14–16 (AUDIT Only): Outcome / Party / Flag", "90.5% Booked | 37.1% Solo/Cpl", "68.1% Booked | 44.5% Solo/Cpl", "<b>28.0% Booked (68.0% None!)</b>", "Held out from clustering! 68% walk-away drives RQ4-Optimize `Dual Trade-Off`"],
        ],
        col_widths=[2.75, 2.20, 2.25, 2.25, 3.18],
        font_size=8.3,
        align_left_cols=(0, 4),
        highlight_rows=(0, 2, 3, 7),
    )
    D.add_card(
        s, 0.35, 4.96, 12.63, 1.32,
        title="How Retrieval Works in RQ1-Identify → RQ2-Personalize: Exactly 1 FAISS Sub-Index per Cluster (3 Total in Current Architecture)",
        header_bg=NAVY,
        bullets=[
            "<b>1. Offline FAISS Partitioning (`D_gold = 933`):</b> Each of the 3 refined clusters gets its own dedicated `faiss.IndexFlatIP(46)` index containing L2-normalized `46-d Blocks` vectors and `[SLOT]`-masked wizard replies: <b>Index 1 (`Decisive Booker`, n = 420)</b>, <b>Index 2 (`Open Explorer`, n = 238)</b>, and <b>Index 3 (`Rigid-Constraint Seeker`, n = 275)</b>.",
            "<b>2. Online Two-Step Retrieval (`D_test = 401`):</b> At runtime, the L1 `RefinedArchetypeRouter` predicts winning cluster `k* ∈ {1, 2, 3}` from the user's opening prefix (`< 2 ms`), and RQ2-Personalize executes exact inner-product cosine search <b>exclusively inside `FAISS_Index[k*]`</b> to retrieve the top `k_shot = 3` exemplar turns!",
        ],
        font_size=9.0,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ1-Identify Complete — Preparing Solution Handoff to RQ2-Personalize (Next Slide):</b> "
        "Notice how `Field 14 (outcome)` was completely excluded from clustering, yet post-hoc audit reveals that <i>Rigid-Constraint Seekers</i> suffer a <b>68.0% non-booking rate</b> in human logs—pinpointing the exact bottleneck that RQ2–RQ4 adaptation will rescue!",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 33: STORYLINE APPEARANCE #2 — END OF RQ1-IDENTIFY DECISION DIAGRAM
    # =========================================================================
    add_storyline_discovery_slide(D, stage_step=1)

    # =========================================================================
    # SLIDE 34: RQ2-PERSONALIZE (RQ2 PART 1) — CAUSAL CONTRAST: PRIMARY (p=.211) VS. REFINED (p<.001)
    # =========================================================================
    s = D.content_slide(
        "6. RQ2-Personalize Stage Results",
        "RQ2-Personalize (Part 1): Causal Contrast — Primary (p = .211) vs. Refined (p < .001)",
        "Figures E2 & 7: Proving that in-context style adaptation succeeds if and only if RQ1-Identify prefix routing is coherent",
        notes="Contrast Figure E2 (interim primary clusters, p=.211 null) with Figure 7 (refined 46-d Blocks clusters, p<.001). This directly proves the causal link between RQ1-Identify and RQ2-Personalize.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq2_results.png"),
        0.35, 1.48, 6.15, 3.30,
        caption="Figure E2 (Primary Whole-Chat Clusters, Routing κ = .24): Style Cosine F = 1.61, p = .211 (Null ✗)",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq2_refined_results.png"),
        6.80, 1.48, 6.18, 3.30,
        caption="Figure 7 (Refined 46-d Blocks Clusters, Routing κ = .535): Style Cosine F = 9.79, p < .001 (Reject H02 ✓)",
    )
    D.add_card(
        s, 0.35, 4.86, 6.15, 1.42,
        title="Why Primary Clusters Failed in RQ2-Personalize (p = .211 — Red Path ✗)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>1. Near-Chance Prefix Routing (`39.4%, κ = .24`):</b> At Turn 3, `60.6%` of test dialogues were routed into the <i>wrong</i> primary cluster's FAISS pool.",
            "<b>2. Conflated Exemplar Sub-Indices:</b> Because whole-dialogue clusters mixed user and wizard turns and grouped by end-of-chat outcome, retrieved examples did not match the user's opening style (`Style F = 1.61, p = .211`).",
        ],
        font_size=9.1,
    )
    D.add_card(
        s, 6.80, 4.86, 6.18, 1.42,
        title="Why Refined `46-d Blocks` Succeeded in RQ2-Personalize (p < .001 — Green Path ✓)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Coherent Prefix Routing (`70.1%, κ = .535` at `M = 5`):</b> Using RQ1-Identify's `RefinedArchetypeRouter`, test prefixes were routed to their true behavioral persona.",
            "<b>2. Persona-Matched FAISS + Pacing Directives:</b> Retrieving `k = 3` `[SLOT]`-masked exemplars from the matched `46-d Blocks` FAISS sub-index lifted style cosine to <b>`.597 (F = 9.79, p < .001, ηp² = .234)`</b> and cut pacing error to <b>`3.87 words (p = .007)`</b>!",
        ],
        font_size=9.1,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ1-Identify → RQ2-Personalize Causal Proof:</b> "
        "Contrasting Figure E2 (`p = .211`) against Figure 7 (`p < .001`) on the <i>exact same LLM and held-out corpus</i> provides direct experimental proof that `RQ2-Personalize Stage` works <b>because of</b> the `46-d Blocks` representation and router passed from `RQ1-Identify Stage`!",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 35: RQ2-PERSONALIZE (RQ2 PART 2) — DETAILED WALKTHROUGH OF TABLE 16 & HOLM CONTRASTS
    # =========================================================================
    s = D.content_slide(
        "6. RQ2-Personalize Stage Results",
        "RQ2-Personalize (Part 2): Detailed Walkthrough of Table 16 & Holm Contrasts",
        "Explaining every column and row across N = 33 held-out dialogues × 3 conditions (99 evaluations) and why SBERT moves while BERTScore stays flat",
        notes="Walk through every column and row of Table 16 and the Holm-adjusted pairwise contrasts in Table E3.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 2.78,
        headers=[
            "Experiment & Outcome Metric (N = 33 Dialogues, Table 16)",
            "Zero-Shot\nM (SD)",
            "Static Few-Shot\nM (SD)",
            "Cluster-Adaptive\nM (SD)",
            "RM-ANOVA F\n(GG-Adjusted df)",
            "p\n(GG)",
            "Partial\nηp²",
            "Friedman Rank\nχ²(2) (p)",
        ],
        rows=[
            ["Primary Archetypes (κ=.24) — SBERT Style Cosine [Closed ✗]", ".603 (.161)", ".650 (.165)", ".642 (.125)", "1.61 (1.95, 62.45)", ".211", ".048", "1.88 (.391)"],
            ["Primary Archetypes — Response Length (words)", "27.58 (5.43)", "16.33 (4.73)", "15.06 (4.35)", "95.32 (1.82, 58.31)", "< .001", ".749", "50.02 (< .001)"],
            ["Refined `Blocks` (κ=.535) — De-lex SBERT Style Cosine (Primary DV ✓)", ".530 (.132)", ".453 (.169)", ".597 (.086)", "9.79 (1.88, 60.29)", "< .001", ".234", "12.50 (.002)"],
            ["Refined `Blocks` — Gemini 3,072-d Topical Cosine (Control)", ".787 (.052)", ".775 (.055)", ".796 (.042)", "1.66 (1.94, 62.22)", ".200", ".049", "4.06 (.131)"],
            ["Refined `Blocks` — Token-Level BERTScore F1 (Control)", ".849 (.020)", ".844 (.023)", ".852 (.019)", "1.45 (1.92, 61.51)", ".243", ".043", "3.70 (.157)"],
            ["Refined `Blocks` — Pacing Calibration Error |W_gen − μ_k| (Primary DV ✓)", "10.12 (8.98)", "6.33 (3.55)", "3.87 (3.58)", "7.10 (1.30, 41.70)", ".007", ".182", "14.27 (< .001)"],
            ["Refined `Blocks` — Generated Response Length (words)", "25.45 (9.17)", "14.48 (5.16)", "16.33 (3.52)", "31.92 (1.41, 45.24)", "< .001", ".499", "36.69 (< .001)"],
        ],
        col_widths=[3.45, 1.15, 1.25, 1.35, 1.65, 0.75, 0.80, 1.43],
        font_size=8.6,
        align_left_cols=(0,),
        highlight_rows=(2, 5),
    )
    D.add_card(
        s, 0.35, 4.32, 6.15, 1.96,
        title="Row-by-Row Guide: Why SBERT Cosine Moves While Gemini & BERTScore Stay Flat",
        header_bg=NAVY,
        bullets=[
            "<b>1. Row 3 (`De-lexicalized SBERT Style Cosine`, Primary DV):</b> `Cluster-Adaptive (.597)` beats `Static Few-Shot (.453)` by <b>`Δ = +.144 (+31.8%, Holm t = 4.26, p < .001, d_z = 0.74)`</b> and beats `Zero-Shot (.530)` by <b>`Δ = +.067 (Holm t = 2.37, p = .049, d_z = 0.41)`</b>. Notice that unrouted `Static Few-Shot (.453)` actually performs <i>worse</i> than `Zero-Shot (.530)` because mismatched persona examples pull style in the wrong direction!",
            "<b>2. Rows 4 & 5 (`Gemini 3,072-d` & `BERTScore F1`):</b> Why are `p = .200` and `p = .243` null? Because all 3 prompts reply to the <b>exact same travel context and topic</b> (`BERTScore = .844–.852`)! This proves the treatment specifically adapts <b>sentence-level pragmatic style (`SBERT`) and pacing</b> without distorting topic.",
        ],
        font_size=8.6,
    )
    D.add_card(
        s, 6.80, 4.32, 6.18, 1.96,
        title="Column-by-Column Guide: Greenhouse–Geisser df, Friedman χ² & Pacing Error",
        header_bg=TEAL,
        bullets=[
            "<b>1. Why Fractional Degrees of Freedom (`df = 1.88, 60.29` & `1.30, 41.70`)?</b> Multiplying `(2, 64)` by the <b>Greenhouse–Geisser sphericity factor (`ε = 0.94` for style; `ε = 0.65` for pacing)</b> corrects for unequal variance of pairwise differences across the 3 prompts.",
            "<b>2. Why Report `Friedman χ²(2)` (`12.50, p = .002` & `14.27, p < .001`)?</b> Ranks the 3 prompts `(1st, 2nd, 3rd)` inside each of the 33 dialogues, proving non-parametric concordance.",
            "<b>3. Row 6 (`Pacing Calibration Error = 3.87w`):</b> Cuts word-length error against human persona norms (`12.9w DB / 18.6w OE / 14.8w RCS`) by <b>`−61.8%` vs. Zero-Shot (`10.12w`, `p_Holm = .004`)</b> and <b>`−38.9%` vs. Static (`6.33w`, `p_Holm = .008`)</b>!",
        ],
        font_size=8.6,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ2-Personalize Solution Approach Alignment (`Reject H02 at p < .001`):</b> "
        "`Static Few-Shot` and `Zero-Shot` are closed for style/pacing personalization (<b>Red</b>), while `Refined Cluster-Adaptive Few-Shot` (`k = 3` FAISS + pacing directive) is locked in as the style winner (<b>Green</b>).",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 36: RQ2-PERSONALIZE (RQ2 PART 3) — WHY RQ2-PERSONALIZE ALONE IS INCOMPLETE (STYLE = GREEN, RULES = ORANGE)
    # =========================================================================
    s = D.content_slide(
        "6. RQ2-Personalize Stage Results",
        "RQ2-Personalize (Part 3): Why Style Adaptation Alone Is Incomplete for Production",
        "Proving why Cluster-Adaptive style is Green (✓) while unguarded rule compliance and entity safety are Orange (!) needing RQ3-Govern",
        notes="This slide explicitly bridges RQ2-Personalize to RQ3-Govern: showing why Cluster-Adaptive prompting solves style and pacing (Green) but still lacks symbolic rule capability and leaks exemplar entities when unguarded (Orange).",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 4.78,
        title="✓ What RQ2-Personalize Proved (GREEN — Carried Forward to RQ3-Govern)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Persona-Matched Discourse Style (`F = 9.79, p < .001, ηp² = .234`):</b>",
            (1, "Routing via RQ1-Identify's `46-d Blocks` prefix router into the 3 partitioned FAISS sub-indices increases de-lexicalized style convergence from `.453` (`Static`) and `.530` (`Zero-Shot`) to <b>`.597` (`+31.8%`, `d_z = 0.74`)</b>."),
            "<b>2. Persona-Calibrated Verbosity (`F = 7.10, p = .007, ηp² = .182`):</b>",
            (1, "Injecting persona word-length norms (`12.9w` for Decisive Bookers, `18.6w` for Open Explorers, `14.8w` for Rigid-Constraint Seekers) cuts absolute pacing error from `10.12` words down to <b>`3.87` words</b> (`SD` tightened from `9.17` to `3.52` words)."),
            "<b>3. Architectural Conclusion on Style:</b>",
            (1, "Clustering is essential for teaching the LLM <i>how to phrase and pace</i> its responses to match each traveler archetype."),
        ],
        font_size=9.6,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 4.78,
        title="! What RQ2-Personalize Cannot Do Alone (ORANGE — Must Verify in RQ3-Govern)",
        header_bg=GOLD,
        bg_color=CALLOUT_BG,
        bullets=[
            "<b>1. Vulnerability A — Unmasked Exemplars Leak Stale Entities:</b>",
            (1, "When raw retrieved FAISS examples are inserted into the prompt without `[SLOT]` masking and post-generation sanitization, the LLM copies stale resort names (`Sapphire Bay Resort`), airlines (`SkyBridge Airways`), prices (`$1,149`), and promo codes (`VIP25`) from the retrieved examples into the active user's reply!"),
            "<b>2. Vulnerability B — Prompt-Only Instructions Fail Arithmetic Rules:</b>",
            (1, "Even when all 5 enterprise booking policies (`visa ≥ 15d`, `passport ≥ 6m`, `FIT ≤ 4 adults`, `discount ≤ 15%`, `intl budget ≥ $500`) are written in the system prompt, the neural model prioritizes stylistic fluency over arithmetic constraint checking."),
            "<b>3. Why This Path Is Marked ORANGE (!) at the End of RQ2-Personalize:</b>",
            (1, "Unguarded `Cluster-Adaptive` prompting cannot be deployed to production until `RQ3-Govern Stage` tests how to combine <b>symbolic `YAML` rules + `[SLOT]` masking</b> with <b>`Cluster-Adaptive` style</b>!"),
        ],
        font_size=9.5,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ2-Personalize → RQ3-Govern Handoff:</b> "
        "`RQ2-Personalize` passes forward the <b>Green `Cluster-Adaptive` style engine</b> alongside the <b>Orange rule/leakage vulnerability</b>—setting up the `2 × 2` factorial experiment in `RQ3-Govern Stage` to test whether symbolic rules and neural style can be combined without trade-offs.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 37: STORYLINE APPEARANCE #3 — END OF RQ2-PERSONALIZE DECISION DIAGRAM
    # =========================================================================
    add_storyline_discovery_slide(D, stage_step=2)

    # =========================================================================
    # SLIDE 38: RQ3-GOVERN (RQ3 PART 1) — 2 × 2 DESIGN, 5 YAML RULES & DUAL-JUDGE RELIABILITY
    # =========================================================================
    s = D.content_slide(
        "7. RQ3-Govern Stage Results",
        "RQ3-Govern (Part 1): 2 × 2 Factorial Design, YAML Rules & Dual-Judge Audit",
        "Tables 9 & C3: Crossing Rules Mode (Off vs. Active) × Prompting Strategy (Zero-Shot vs. Cluster-Adaptive) across N = 144 units",
        notes="Explain the 5 declarative YAML rules (Table 9), the balanced 2x2 factorial setup (N=144, n=36/cell, 50% violating / 50% compliant), and the independent Gemini 2.5 Pro Dual-Judge validation (kappa = .917).",
    )
    D.add_table(
        s, 0.35, 1.48, 7.35, 3.15,
        headers=["Rule ID & Policy Name (Table 9)", "Deterministic Trigger Condition", "Action", "Severity"],
        rows=[
            ["1. `RULE_VISA_LEAD_TIME`\nVisa Processing Lead Time", "`departure_lead_days < 15` on international destination", "`flag_warning`", "High"],
            ["2. `RULE_PASSPORT_VALIDITY`\nPassport 6-Month Validity", "`passport_expiry_months < 6` on international trip", "`block_booking`", "Critical"],
            ["3. `RULE_PARTY_SIZE_LIMIT`\nMaximum FIT Adult Capacity", "`traveler_count_adults > 4` and `package_type == 'FIT'`", "`escalate_group`", "Medium"],
            ["4. `RULE_DISCOUNT_CAP`\nPromotional Discount Ceiling", "`discount_applied_percentage > 15.0%`", "`cap_discount`", "High"],
            ["5. `RULE_MIN_BUDGET_INTL`\nMinimum International Budget", "`budget_amount < $500` per adult on international package", "`reject_reprompt`", "High"],
        ],
        col_widths=[1.95, 2.85, 1.40, 0.85],
        font_size=9.2,
        align_left_cols=(0, 1, 2),
        highlight_rows=(0, 1, 2, 3, 4),
    )
    D.add_card(
        s, 7.85, 1.48, 5.13, 3.15,
        title="Cross-Model Dual-Judge Reliability (Table C3)",
        header_bg=NAVY,
        bullets=[
            "<b>Why Two Independent Judge Models Were Used:</b>",
            (1, "To eliminate self-preference bias, responses generated by `gemini-2.5-flash` were audited on a stratified `n = 48` subsample (`12/cell`) by both `gemini-2.5-flash` (Judge 1) and the larger reasoning model <b>`gemini-2.5-pro` (Judge 2)</b>."),
            "<b>Empirical Reliability Results (`n = 48`):</b>",
            (1, "• <b>Raw Agreement:</b> <b>`95.8%`</b> (`46 / 48` identical decisions)."),
            (1, "• <b>Cohen's Kappa:</b> <b>`κ = .917`</b> (`PABAK = .917`), far above `κ ≥ .70`."),
            (1, "• <b>Agreement with Deterministic Python Regex (`N = 144`):</b> <b>`93.1%` (`κ = .861`)</b>."),
        ],
        font_size=9.3,
    )
    D.add_card(
        s, 0.35, 4.73, 12.63, 1.55,
        title="How the Balanced 2 × 2 Factorial Experiment Was Constructed (`N = 144, n = 36/cell, seed = 42`)",
        header_bg=TEAL,
        bullets=[
            "<b>1. Inherited RQ1-Identify & RQ2-Personalize Backbone:</b> 36 held-out `D_test` dialogues (stratified at exactly `12` per RQ1-Identify `46-d Blocks` archetype: `12 DB, 12 OE, 12 RCS`) were evaluated across all 4 cells (`36 × 4 = 144` units). Exactly <b>50% (`n = 18/cell`) violated ≥ 1 YAML rule</b> (testing enforcement sensitivity) and <b>50% (`n = 18/cell`) were 100% policy-compliant</b> (testing specificity against false blocking).",
            "<b>2. Factor Manipulation:</b> Under `Rules Off`, policies are stated only in natural language and `Cluster-Adaptive` exemplars are unmasked. Under `Rules Active`, `DeclarativeRuleEngine` executes `< 1 ms` pre-generation checks, masks FAISS exemplars with `[SLOT]`, and runs post-generation entity leakage sanitization.",
        ],
        font_size=9.2,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ3-Govern Solution Approach Alignment (`Testing the Orange Vulnerability from RQ2-Personalize`):</b> "
        "This `2 × 2` design directly tests RQ2-Personalize's unresolved question: Can symbolic `YAML` governance (`Rules Active`) eliminate exemplar entity leakage and enforce numeric rules without degrading the stylistic gains of `Cluster-Adaptive` prompting?",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 39: RQ3-GOVERN (RQ3 PART 2) — VISUAL WALKTHROUGH OF FIGURE 8 (4-PANEL INTERACTION)
    # =========================================================================
    s = D.content_slide(
        "7. RQ3-Govern Stage Results",
        "RQ3-Govern (Part 2): 2 × 2 Factorial Interaction Profiles (Figure 8 Walkthrough)",
        "Visualizing orthogonal main effects (Panels A, C, D) versus the protective interaction on Exemplar Entity Leakage (Panel B)",
        notes="Walk the committee through all 4 panels of Figure 8. Contrast the parallel lines in Panels A, C, D against the sharply diverging lines in Panel B.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq3_factorial_results.png"),
        0.35, 1.48, 7.45, 4.78,
        caption="Figure 8: 2 × 2 Factorial Interaction Profiles Across N = 144 Units (n = 36/cell; 95% CIs)",
    )
    D.add_card(
        s, 7.95, 1.48, 5.03, 4.78,
        title="Panel-by-Panel Guide to Reading Figure 8",
        header_bg=NAVY,
        bullets=[
            "<b>Panel A (Rule Adherence Rate — Orthogonal Main Effect of Rules):</b>",
            (1, "Lines are flat and parallel (`Interaction F = 0.01, p = .916`)."),
            (1, "Activating `Rules Active` jumps adherence from `.500` (`5.6%` on violating cases) to <b>`.944 / .931` (`98.6%` on violating cases, `F = 43.92, p < .001`)</b>."),
            (1, "Changing prompt mode alone has <b>zero effect (`F = 0.01`)</b>—proving prompt engineering cannot enforce rules!"),
            "<b>Panel B (Exemplar Entity Leakage — Protective Interaction!):</b>",
            (1, "Sharp non-parallel divergence (`Interaction F = 34.82, p < .001, ηp² = .199`)!"),
            (1, "Under `Rules Off`, switching from `Zero-Shot` to `Cluster-Adaptive` spikes leakage from `.000` to <b>`.359` (`55.6%` of replies contaminated)</b>."),
            (1, "Under `Rules Active`, `[SLOT]` masking + sanitization holds leakage at <b>`.000 (0.0%)` in both prompt modes</b>!"),
            "<b>Panels C & D (Slot Coverage F1 & Style Alignment Cosine):</b>",
            (1, "`Rules Active` lifts `Slot F1` from `.208/.485` to <b>`.977/.952` (`F = 489.52, p < .001`)</b>, while `Cluster-Adaptive` lifts style cosine (`F = 24.00, p < .001`)."),
        ],
        font_size=8.9,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ3-Govern Solution Approach Alignment (`Visual Proof of Neuro-Symbolic Synergy`):</b> "
        "Figure 8 visually demonstrates why neither neural prompting nor symbolic rules is sufficient alone: <b>Panel A & C</b> prove rules are required for policy accuracy and slot grounding, <b>Panel D</b> proves clustering is required for style, and <b>Panel B</b> proves their interaction eliminates entity leakage!",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 40: RQ3-GOVERN (RQ3 PART 3) — DETAILED TABLE 17 WALKTHROUGH (SENSITIVITY/SPECIFICITY & SUM-SS)
    # =========================================================================
    s = D.content_slide(
        "7. RQ3-Govern Stage Results",
        "RQ3-Govern (Part 3): Detailed Walkthrough of Table 17 & Sum-Contrast Math",
        "Explaining Violation Sensitivity (5.6% → 98.6%) vs. Compliant Specificity and why 3 zero-leakage cells yield identical F = 34.82",
        notes="Walk through every row and column of Table 17. Explain two deep statistical details: (1) splitting Rule Adherence into Violation Sensitivity vs. Compliant Specificity, and (2) why the three F-ratios in the Leakage column are all 34.82.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 2.75,
        headers=[
            "Experimental Cell or 2 × 2 ANOVA Effect (Table 17)",
            "n or df",
            "Rule Acc. | Viol. Sens. / Comp. Spec.",
            "Exemplar Leakage M (SD) / Inc. %",
            "Slot Coverage F1 M (SD)",
            "Style Alignment M (SD)",
        ],
        rows=[
            ["Cell 1: Rules Off × Zero-Shot [Closed ✗]", "36", ".500 (.507) | 5.6% / 94.4%", ".000 (.000) / 0.0%", ".208 (.242)", ".414 (.124)"],
            ["Cell 2: Rules Off × Cluster-Adaptive [Closed ✗ — High Leakage!]", "36", ".500 (.507) | 5.6% / 94.4%", ".359 (.348) / 55.6%", ".485 (.269)", ".507 (.095)"],
            ["Cell 3: Rules Active × Zero-Shot [Partial ! — Low Style]", "36", ".944 (.232) | 100.0% / 88.9%", ".000 (.000) / 0.0%", ".977 (.096)", ".428 (.107)"],
            ["Cell 4: Rules Active × Cluster-Adaptive [Pareto Winner ✓]", "36", ".931 (.244) | 97.2% / 88.9%", ".000 (.000) / 0.0%", ".952 (.124)", ".506 (.086)"],
            [
                "ANOVA Main Effect: Rules Mode (OLS / HC3 / ART)",
                "1, 140",
                "Acc F=43.92 (< .001), ηp²=.239\n(Sens F=498.78; Spec F=0.69, p=.408)",
                "F = 34.82 (< .001), ηp² = .199*\n(Sum-HC3 F=33.85; ART F=43.48)",
                "F = 489.52 (< .001), ηp² = .778\n(HC3 F=471.70; ART F=691.34)",
                "F = 3.68 (.057), ηp² = .026\n(HC3 F=2.86; ART F=2.49)",
            ],
            [
                "ANOVA Main Effect: Prompting Mode (OLS / HC3 / ART)",
                "1, 140",
                "Acc F = 0.01 (.916), ηp² = .000\n(HC3 F=0.05; ART F=0.01)",
                "F = 34.82 (< .001), ηp² = .199*\n(Sum-HC3 F=33.85; ART F=43.48)",
                "F = 20.46 (< .001), ηp² = .128\n(ART F=13.94, p < .001)",
                "F = 24.00 (< .001), ηp² = .146\n(HC3 F=20.62; ART F=25.38)",
            ],
            [
                "ANOVA Interaction: Rules × Prompting (OLS / HC3 / ART)",
                "1, 140",
                "Acc F = 0.01 (.916), ηp² = .000\n(HC3 F=0.01; p = .918)",
                "F = 34.82 (< .001), ηp² = .199*\n(HC3 F=33.85; ART F=2148.81)",
                "F = 29.32 (< .001), ηp² = .173\n(HC3 F=28.51; ART F=180.38)",
                "F = 8.95 (.003), ηp² = .060\n(HC3 F=8.70; ART F=35.77)",
            ],
        ],
        col_widths=[3.10, 0.72, 2.38, 2.28, 2.15, 2.00],
        font_size=8.6,
        align_left_cols=(0,),
        highlight_rows=(3, 4, 6),
    )
    D.add_card(
        s, 0.35, 4.30, 6.15, 1.98,
        title="1. Why Split Rule Adherence into Sensitivity vs. Specificity?",
        header_bg=NAVY,
        bullets=[
            "<b>Why `.500` Overall Accuracy Under `Rules Off` Is Deceptive:</b>",
            (1, "Because 50% (`18/36`) of test cases are compliant and 50% (`18/36`) violate a rule, an unguarded LLM that simply says <i>'Yes, I can book that!'</i> to everything gets `94.4% (17/18)` on compliant cases (`Specificity`), but catches <b>only `5.6% (1/18)` of actual policy violations (`Sensitivity`)</b>—averaging `.500`!"),
            "<b>What `Rules Active` Achieves:</b>",
            (1, "Lifts <b>Violation Enforcement Sensitivity from `5.6%` to `100.0% / 97.2%` (`98.6%` combined, `F(1, 68) = 498.78, p < .001, ηp² = .880`)</b> while preserving <b>`88.9%` Compliant Specificity (`F = 0.69, p = .408` — zero over-blocking)</b>!"),
        ],
        font_size=8.7,
    )
    D.add_card(
        s, 6.80, 4.30, 6.18, 1.98,
        title="2. Mathematical Note: Why Are All 3 Leakage F-Ratios Equal to 34.82?",
        header_bg=TEAL,
        bullets=[
            "<b>Exact Algebraic Identity in a Balanced `2 × 2` Table with 3 Zero Cells:</b>",
            (1, "In Column 4 (`Exemplar Leakage`), three of the four cells (`Cell 1 = .000`, `Cell 3 = .000`, `Cell 4 = .000`) have <b>exact zero leakage</b>; only `Cell 2 (Rules Off × Cluster-Adaptive)` is non-zero (`μ_2 = .359`)."),
            (1, "Under orthogonal `Sum` contrasts (`±1`), the contrast magnitudes `|−μ_2/2|` for Main Effect A, Main Effect B, and the `A × B` Interaction are algebraically identical, partitioning the <b>exact same sum of squares (`SS = 1.162`) and `F(1, 140) = 34.82` (`Sum-HC3 F = 33.85`, `ART F = 2,148.81`)</b>!"),
        ],
        font_size=8.7,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ3-Govern Solution Approach Alignment (`Reject H03 at p < .001`):</b> "
        "Table 17 proves that `Cell 4 (Rules Active × Cluster-Adaptive)` is the unique <b>Pareto-optimal configuration (Green)</b>—simultaneously achieving `97.2%` violation sensitivity, `0.0%` entity leakage, `.952` Slot F1, and `.506` persona style alignment!",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 41: RQ3-GOVERN (RQ3 PART 4) — CONCRETE SIDE-BY-SIDE DIALOGUE OUTPUT PROOF
    # =========================================================================
    s = D.content_slide(
        "7. RQ3-Govern Stage Results",
        "RQ3-Govern (Part 4): Concrete Dialogue Proof Across the 2 × 2 Cells",
        "Inspecting actual LLM responses on the same Dallas-to-Tokyo trip (9-day visa violation) across Red, Orange, and Green paths",
        notes="Show the concrete side-by-side LLM outputs on the exact same held-out Dallas-to-Tokyo scenario to make the Red, Orange, and Green solution approach nodes tangible.",
    )
    D.add_card(
        s, 0.35, 1.48, 4.05, 4.78,
        title="✗ RED PATH (Cell 2): Style Without Rules\n(Rules Off × Cluster-Adaptive)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>Active User Trip State (`D_test`):</b>",
            (1, "Flying <b>Dallas → Tokyo</b> departing in <b>`9 days`</b> (violates `RULE_VISA_LEAD_TIME < 15 days`), 2 adults, 9 nights, budget `$2,600`."),
            "<b>Actual Generated Reply (Unguarded ICL):</b>",
            (1, "<i>'I can book your 2-adult package into the <b>Sapphire Bay Resort</b> on <b>SkyBridge Airways</b> for <b>$1,149</b> using promo code <b>VIP25</b>!'</i>"),
            "<b>Why This Path Is Closed (`Red ✗`):</b>",
            (1, "• <b>Severe Entity Leakage (`ELR = .80`):</b> Hallucinated 4 stale entities copied from retrieved FAISS examples!"),
            (1, "• <b>Policy Failure (`RAR = 0`):</b> Completely missed the 9-day international visa lead-time violation!"),
        ],
        font_size=9.2,
    )
    D.add_card(
        s, 4.60, 1.48, 4.10, 4.78,
        title="! ORANGE PATH (Cell 3): Rules Without Style\n(Rules Active × Zero-Shot)",
        header_bg=GOLD,
        bg_color=CALLOUT_BG,
        bullets=[
            "<b>Same Active User Trip State (`D_test`):</b>",
            (1, "Flying <b>Dallas → Tokyo</b> departing in <b>`9 days`</b>, 2 adults, 9 nights, budget `$2,600`."),
            "<b>Actual Generated Reply (Zero-Shot + Rules):</b>",
            (1, "<i>'WARNING: International travel from Dallas to Tokyo in 9 days violates the 15-day visa processing lead-time requirement for 2 adults under a $2,600 budget for 9 nights. Please provide a compliant departure date before proceeding.'</i>"),
            "<b>Why This Path Is Partial (`Orange !`):</b>",
            (1, "• <b>Enforces Rules (`RAR = 1.00, ELR = .000`):</b> Catches the 9-day visa rule and grounds all 5 slots (`Slot F1 = 1.00`)."),
            (1, "• <b>Lacks Persona Style (`Cosine = .428`):</b> Robotic, bureaucratic tone that ignores shopper archetype pacing."),
        ],
        font_size=9.2,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 4.78,
        title="✓ GREEN WINNER (Cell 4): Rules + Style!\n(Rules Active × Cluster-Adaptive)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>Same Active User Trip State (`D_test`):</b>",
            (1, "Flying <b>Dallas → Tokyo</b> departing in <b>`9 days`</b>, 2 adults, 9 nights, budget `$2,600`."),
            "<b>Actual Generated Reply (Neuro-Symbolic):</b>",
            (1, "<i>'For your 9-night Dallas to Tokyo package for 2 adults ($2,600 budget), please note that departures within 15 days (9 days stated) require expedited visa verification before confirming your hotel tier.'</i>"),
            "<b>Why This Path Wins (`Green ✓`):</b>",
            (1, "• <b>Zero Entity Leakage (`ELR = .000`):</b> `[SLOT]` masking prevented copying stale resort/airline names."),
            (1, "• <b>100% Policy & Slot Fidelity (`RAR = 1.00, Slot F1 = 1.00`).</b>"),
            (1, "• <b>Persona-Matched Style (`Cosine = .506`, crisp pacing).</b>"),
        ],
        font_size=9.2,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ3-Govern Complete — Preparing Solution Handoff to RQ4-Optimize (Next Slide):</b> "
        "This side-by-side comparison shows why the Orange vulnerability from RQ2-Personalize splits into a <b>closed Red path (`Rules Off`)</b> and a <b>winning Green path (`Rules Active × Cluster-Adaptive`)</b> that now advances to `RQ4-Optimize Stage`.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 42: STORYLINE APPEARANCE #4 — END OF RQ3-GOVERN DECISION DIAGRAM
    # =========================================================================
    add_storyline_discovery_slide(D, stage_step=3)

    # =========================================================================
    # SLIDE 43: RQ4-OPTIMIZE (RQ4 PART 1) — 2 × 3 SIMULATION DESIGN, 4-OPTION CATALOG & PERSONA AUDIT
    # =========================================================================
    s = D.content_slide(
        "8. RQ4-Optimize Stage Results",
        "RQ4-Optimize (Part 1): 2 × 3 Simulation Design & Blind Persona Fidelity Audit",
        "Testing Prompting Strategy (Zero-Shot vs. Full Stack) × 3 Refined Archetypes across N = 180 closed-loop episodes (κ_persona = .933)",
        notes="Explain the closed-loop simulation setup (N=180 unique trip seeds, n=30/cell), the 4-option package catalog (Options A, B, C, D), and the blind Gemini 2.5 Pro customer simulator validation (95.6% accuracy, kappa = .933).",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 3.25,
        title="Closed-Loop Simulation & 4-Option Catalog (`N = 180, n = 30/cell`)",
        header_bg=NAVY,
        bullets=[
            "<b>1. Inherited RQ1-Identify to RQ3-Govern Stack:</b> 180 distinct held-out `D_test` trip seeds (`60` per RQ1-Identify `46-d Blocks` archetype, `n = 30/cell` between-subjects). The `Cluster-Adaptive` arm runs the complete <b>RQ1-Identify Router (`M=9, κ=.958`) + RQ2-Personalize `[SLOT]` FAISS + RQ3-Govern Active `RuleEngine` + RQ4-Optimize `Verified Informed Slot Ledger`</b>.",
            "<b>2. Realistic 4-Option Travel Package Inventory per Trip:</b>",
            (1, "• <b>Option A (4★ Exact Match):</b> Exact city & dates, 4-star hotel at <b>`88%` of budget</b>."),
            (1, "• <b>Option B (3.5★ Saver):</b> Exact dates, boutique hotel + breakfast at <b>`72%` of budget</b>."),
            (1, "• <b>Option C (5★ Exact Dates — Over Budget Conflict!):</b> 5-star luxury hotel on exact dates at <b>`118%` of budget</b> (triggers constraint deadlock for Rigid Seekers!)."),
            (1, "• <b>Option D (5★ Shifted Dates — Within Budget):</b> 5-star luxury hotel shifted `+3 days` at <b>`94%` of budget</b>."),
        ],
        font_size=8.9,
    )
    D.add_table(
        s, 6.80, 1.48, 6.18, 3.25,
        headers=[
            "Blind `gemini-2.5-pro` Simulator Audit (n = 45, Table C3)",
            "Decisiveness\n(1–5 M)",
            "Exploration\n(1–5 M)",
            "Rigidity\n(1–5 M)",
            "Blind Classification\nAccuracy & κ",
        ],
        rows=[
            [
                "Simulated Archetype 1:\nDecisive Booker (`n = 15` audited)",
                "<b>5.00</b>\n(Highest)",
                "1.00\n(Focused)",
                "2.27\n(Moderate)",
                "15 / 15 (100.0%)\nMatches RQ1-Identify DB profile",
            ],
            [
                "Simulated Archetype 2:\nOpen Explorer (`n = 15` audited)",
                "2.80\n(Deliberative)",
                "<b>4.27</b>\n(Highest)",
                "1.60\n(Flexible)",
                "14 / 15 (93.3%)\nMatches RQ1-Identify OE profile",
            ],
            [
                "Simulated Archetype 3:\nRigid-Constraint Seeker (`n = 15` audited)",
                "1.67\n(Cautious)",
                "2.27\n(Narrow)",
                "<b>4.33</b>\n(Highest)",
                "14 / 15 (93.3%)\nMatches RQ1-Identify RCS profile",
            ],
            [
                "Overall Blind Validation Summary\n(vs. 33.3% Chance Baseline)",
                "F = 94.2***",
                "F = 88.6***",
                "F = 76.4***",
                "<b>43 / 45 (95.6% Acc.)</b>\n<b>p = 1.37 × 10⁻¹⁸, κ = .933</b>",
            ],
        ],
        col_widths=[2.15, 0.88, 0.88, 0.85, 1.42],
        font_size=8.4,
        align_left_cols=(0, 4),
        highlight_rows=(3,),
    )
    D.add_card(
        s, 0.35, 4.82, 12.63, 1.46,
        title="How RQ4-Optimize Pairs the Verified Informed Slot Ledger with Persona Package Trade-Off Policies",
        header_bg=TEAL,
        bullets=[
            "<b>1. Memoryless `Zero-Shot` Baseline:</b> Elicits missing slots sequentially without an informed-slot ledger (frequently re-asking stated constraints) and offers only `Option A` first.",
            "<b>2. Full-Stack `Cluster-Adaptive` Policy:</b> Locks all stated user slots in the <b>Verified Informed Slot Ledger</b> (forbidding re-asks → `0.0% RER`), bundles any remaining missing slots into Turn 1, and applies persona-specific package framing: <b>(a) Decisive Booker:</b> Direct `Option A` confirmation; <b>(b) Open Explorer:</b> Side-by-side `Option A vs. Option B vs. Option D` comparison table in 1 turn; <b>(c) Rigid-Constraint Seeker:</b> Proactive dual trade-off explaining `Option C`'s budget conflict while presenting `Option A (4★ exact dates)` and `Option D (5★ +3d shifted dates)`.",
        ],
        font_size=9.0,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ4-Optimize Solution Approach Alignment (`Validating the Multi-Turn Testbed`):</b> "
        "Blind auditing by `gemini-2.5-pro` (`95.6%` accuracy, `p = 1.37 × 10⁻¹⁸`, `κ = .933`) confirms that the customer simulator faithfully reproduces RQ1-Identify's three behavioral archetypes (`Table 15`) without label leakage.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 44: RQ4-OPTIMIZE (RQ4 PART 2) — VISUAL WALKTHROUGH OF FIGURE 9 (TURN ECONOMY & RER)
    # =========================================================================
    s = D.content_slide(
        "8. RQ4-Optimize Stage Results",
        "RQ4-Optimize (Part 2): Multi-Turn Economy & Redundant Elicitation (Figure 9)",
        "Rejecting H04 (p < .001): Massive main effect of prompting (F = 664.43) AND significant Prompt × Archetype interaction (F = 10.89)",
        notes="Walk the committee through Panels A and B of Figure 9. Explain why the turn reduction is steepest (−42.7%) for Rigid-Constraint Seekers and why RER drops to 0.0%.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq4_turn_economy_results.png"),
        0.35, 1.48, 7.45, 4.78,
        caption="Figure 9: Mean Turns to Goal Completion (Panel A) & Redundant Elicitation Rate (Panel B) Across N = 180 Simulations",
    )
    D.add_card(
        s, 7.95, 1.48, 5.03, 4.78,
        title="Visual Walkthrough of Figure 9 (Panels A & B)",
        header_bg=NAVY,
        bullets=[
            "<b>Panel A (Turns to Goal Completion — Main Effect & Interaction):</b>",
            (1, "Under `Zero-Shot` (coral bars), <i>Rigid-Constraint Seekers</i> require the most turns (<b>`8.73 turns`</b>) because they reject `Option A` when their 5-star request (`Option C`) exceeds budget, triggering multi-turn pushback loops."),
            (1, "Under `Cluster-Adaptive` (teal bars), turns drop sharply across all three personas—with the <b>steepest compression in Rigid-Constraint Seekers (`−3.73 turns, −42.7%, 8.73 → 5.00 turns`)</b>, followed by <i>Decisive Bookers</i> (`−34.2%, 7.60 → 5.00t`) and <i>Open Explorers</i> (`−29.5%, 7.47 → 5.27t`)."),
            (1, "This differential compression produces the significant <b>`Prompt × Archetype` interaction: `F(2, 174) = 10.89, p < .001, ηp² = .111`</b>!"),
            "<b>Panel B (Redundant Elicitation Rate — `RER`):</b>",
            (1, "`Zero-Shot` re-asks already stated constraints in <b>`19.4%`</b> of turns for Decisive Bookers (who state 3+ slots in Turn 1), `6.1%` for Open Explorers, and `7.2%` for Rigid Seekers (`Overall M = .109`)."),
            (1, "With the `Verified Informed Slot Ledger`, `RER` drops to <b>`.000 (0.0%)` across all 90 dialogues (`F = 63.02, p < .001`)</b>!"),
        ],
        font_size=8.9,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ4-Optimize Solution Approach Alignment (`Visual Proof of End-to-End Optimization`):</b> "
        "Figure 9 shows how the 4-stage cascade rescues the exact segment (`Rigid-Constraint Seekers`, `68.0%` historical walk-away rate in RQ1-Identify) that struggled most under static prompting—compressing their negotiation turns by `42.7%`!",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 45: RQ4-OPTIMIZE (RQ4 PART 3) — COMPLETE TABLE 18 STATISTICS & PROTOCOL FLOOR
    # =========================================================================
    s = D.content_slide(
        "8. RQ4-Optimize Stage Results",
        "RQ4-Optimize (Part 3): Complete Table 18 Statistics & Protocol Floor Analysis",
        "100% concordance across OLS ANOVA, HC3 heteroscedasticity-robust F, Aligned Rank Transform (ART), Welch t, and Mann–Whitney U",
        notes="Present Table 18 in full and explain the deterministic 5.00-turn protocol floor and why HC3, ART, and Mann-Whitney U are reported alongside OLS ANOVA.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 3.25,
        headers=[
            "Archetype × Prompting Cell or 2 × 3 ANOVA Effect (Table 18)",
            "Total Turns\nM (SD)",
            "Log Turns ln(TGC)\nM (SD)",
            "Redundant Elicitation\nRER M (SD)",
            "Turn Reduction\nΔ (%)",
            "Simple Contrast (Welch t / Mann–Whitney U / Cohen's d)",
        ],
        rows=[
            ["1. Decisive Booker — Zero-Shot (n = 30) [Closed ✗]", "7.60 (0.93)", "2.021 (0.119)", ".194 (.166)", "—", "—"],
            ["2. Decisive Booker — Cluster-Adaptive (n = 30) [Winner ✓]", "5.00 (0.00)", "1.609 (0.000)", ".000 (.000)", "−2.60 turns (−34.2%)", "t_log = −18.92 (p < .001), U = 0.0 (p < .001), d = −3.94"],
            ["3. Open Explorer — Zero-Shot (n = 30) [Closed ✗]", "7.47 (1.01)", "2.002 (0.130)", ".061 (.115)", "—", "—"],
            ["4. Open Explorer — Cluster-Adaptive (n = 30) [Winner ✓]", "5.27 (0.69)", "1.654 (0.115)", ".000 (.000)", "−2.20 turns (−29.5%)", "t_log = −10.97 (p < .001), U = 40.5 (p < .001), d = −2.55"],
            ["5. Rigid-Constraint Seeker — Zero-Shot (n = 30) [Closed ✗]", "8.73 (1.55)", "2.152 (0.175)", ".072 (.119)", "—", "—"],
            ["6. Rigid-Constraint Seeker — Cluster-Adaptive (n = 30) [Winner ✓]", "5.00 (0.00)", "1.609 (0.000)", ".000 (.000)", "−3.73 turns (−42.7%)", "t_log = −17.02 (p < .001), U = 0.0 (p < .001), d = −3.40"],
            ["7. ANOVA Main Effect: Prompting (df = 1, 174)", "F = 457.74 (< .001)\nηp² = .725", "F = 664.43 (< .001)\nηp² = .793", "F = 63.02 (< .001)\nηp² = .266", "HC3 F_log = 681.53\n(p < .001)", "ART F_log = 224.22 (p < .001)\nOverall: 7.93 → 5.09 turns (−35.8%)"],
            ["8. ANOVA Main Effect: Archetype (df = 2, 174)", "F = 7.77 (< .001)\nηp² = .082", "F = 5.55 (.005)\nηp² = .060", "F = 7.57 (< .001)\nηp² = .080", "HC3 F_log = 5.86\n(p = .003)", "ART F_log = 207.29 (p < .001)\nPersonas differ in baseline length"],
            ["9. ANOVA Interaction: Prompting × Archetype (df = 2, 174)", "F = 14.37 (< .001)\nηp² = .142", "F = 10.89 (< .001)\nηp² = .111", "F = 9.70 (< .001)\nηp² = .100", "HC3 F_log = 8.58\n(p < .001)", "ART F_log = 209.46 (p < .001)\nSteepest gain in Rigid Seekers (−42.7%)"],
        ],
        col_widths=[2.85, 1.35, 1.45, 1.45, 1.80, 3.73],
        font_size=8.4,
        align_left_cols=(0, 5),
        highlight_rows=(1, 3, 5, 6, 8),
    )
    D.add_card(
        s, 0.35, 4.80, 12.63, 1.48,
        title="Understanding the Structural Protocol Floor (`5.00 Turns, SD = 0.00`) & Zero-Variance Robustness Checks",
        header_bg=NAVY,
        bullets=[
            "<b>Why Do Decisive Bookers and Rigid-Constraint Seekers Hit Exactly `5.00 (0.00)` Turns Under `Cluster-Adaptive`?</b>",
            (1, "`total_turns` counts total messages (`user_turns + assistant_turns`). Because every seed trip opens at `U1` with `3 of 5` mandatory slots stated, the theoretical minimum trajectory to complete intake and confirm a package quotation is <b>5 messages: `U1 (initial request) → A1 (bundled elicitation of 2 missing slots) → U2 (user supplies remaining slots) → A2 (persona-tailored package quote/trade-off) → U3 ([ACCEPT_BOOKING])`</b> (`ln 5 = 1.609`)."),
            (1, "Because `SD = 0.00` creates boundary heteroscedasticity, inference is verified via <b>`MacKinnon–White HC3` (`F_log = 681.53, Int. F = 8.58, p < .001`), `Aligned Rank Transform (ART)` (`F_log = 224.22, Int. F = 209.46`), `Welch's t`, and `Mann–Whitney U = 0.0` (`p < .001`)</b>—where `U = 0.0` means every single `Cluster-Adaptive` episode finished in fewer turns than every `Zero-Shot` episode!"),
        ],
        font_size=8.8,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ4-Optimize Solution Approach Alignment (`Reject H04 at p < .001`):</b> "
        "Table 18 confirms that the full 4-stage stack (`Cluster-Adaptive + Rules Active + Slot Ledger`) achieves the theoretical minimum 5-message floor for `100%` of Decisive and Rigid shoppers while allowing Open Explorers `5.27` turns for 3-option comparison.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 46: RQ4-OPTIMIZE (RQ4 PART 4) — DEEP-DIVE EXPLANATION OF TABLE 18 COLUMNS & ROWS
    # =========================================================================
    s = D.content_slide(
        "8. RQ4-Optimize Stage Results",
        "RQ4-Optimize (Part 4): Deep-Dive Guide to Explaining Table 18 Columns & Rows",
        "Why both Raw Turns and Log Turns are required, how Two-Way 2 × 3 ANOVA works, and why Cohen's d & ηp² are reported",
        notes="This slide provides the complete mathematical and business explanation of every column and row in Table 18 (answering why both Raw Turns and Log Turns are needed, how 2x3 ANOVA works, and why Cohen's d is reported).",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 2.35,
        title="1. Significance of the Columns: Why Both `Total Turns` AND `Log Turns`?",
        header_bg=NAVY,
        bullets=[
            "<b>Why Column 2 Is Required (`Total Turns M (SD)` — Raw Count):</b>",
            (1, "Provides <b>direct business & engineering interpretability</b>: OTA managers and cloud architects budget in raw messages (`7.93 → 5.09 turns`, saving `2.84 messages/session` or `2.84M API calls` per 1M chats)."),
            "<b>Why Column 3 Is Also Required (`Log Turns ln(TGC) M (SD)` — Primary Parametric DV):</b>",
            (1, "Dialogue turn counts are <b>strictly positive (`≥ 5`) and right-skewed</b> (`Zero-Shot` Rigid Seekers stretch up to `13+` turns with `SD = 1.55`, whereas `Cluster-Adaptive` is compressed near `5.00` with `SD = 0.00–0.69`)."),
            (1, "Applying natural log <b>`Y = ln(TGC)` compresses right-tail outliers and stabilizes variance</b> for parametric ANOVA (`F_log = 664.43, ηp² = .793` vs. `F_raw = 457.74, ηp² = .725`), proving significance holds in both scales!"),
        ],
        font_size=8.6,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 2.35,
        title="2. Significance of Columns 4, 5 & 6 (`RER`, `Δ%`, and `Simple Contrasts`)",
        header_bg=TEAL,
        bullets=[
            "<b>Column 4 (`Redundant Elicitation Rate — RER`):</b> Isolates the <i>mechanism</i> of turn waste—measuring the share of assistant turns that re-ask an already stated slot (`.194 → .000` in DB).",
            "<b>Column 5 (`Turn Reduction Δ%` & `HC3 F_log`):</b> Reports practical percentage turn savings (`−34.2%, −29.5%, −42.7%`) in Rows 1–6 and MacKinnon–White `HC3` heteroscedasticity-robust `F` in Rows 7–9.",
            "<b>Column 6 (`Welch t / Mann–Whitney U / Cohen's d` & `ART F_log`):</b> Pairs parametric `Welch t` (unequal-variance t-test) with rank-based `Mann–Whitney U` (`U = 0.0` = zero distribution overlap) and `ART` non-parametric factorial ANOVA.",
        ],
        font_size=8.6,
    )
    D.add_card(
        s, 0.35, 3.92, 6.15, 2.35,
        title="3. Significance of the Rows: How Two-Way 2 × 3 ANOVA Operates in Rows 7–9",
        header_bg=BLUE,
        bullets=[
            "<b>Rows 1–6 (The 6 Experimental Cells, `n = 30/cell`, `N = 180`):</b> Present the cell means and simple within-archetype pairwise contrasts (`Zero-Shot` vs. `Cluster-Adaptive` inside `DB`, `OE`, and `RCS`).",
            "<b>Rows 7–9 (Two-Way `2 × 3` Between-Subjects Factorial ANOVA, `df_error = 180 − 6 = 174`):</b>",
            (1, "• <b>Row 7 (`Main Effect of Prompting`, `df = 1, 174`):</b> Tests average turn reduction across all 180 chats (`F_log = 664.43, p < .001, ηp² = .793`)."),
            (1, "• <b>Row 8 (`Main Effect of Archetype`, `df = 2, 174`):</b> Tests whether the 3 personas differ in average length (`F_log = 5.55, p = .005, ηp² = .060`)."),
            (1, "• <b>Row 9 (`Prompting × Archetype Interaction`, `df = 2, 174`):</b> Proves turn savings are moderated by persona (`F_log = 10.89, p < .001, ηp² = .111` — steepest in Rigid Seekers at `−42.7%`)!"),
        ],
        font_size=8.6,
    )
    D.add_card(
        s, 6.80, 3.92, 6.18, 2.35,
        title="4. Why Cohen's d (`−3.94, −2.55, −3.40`) & Partial ηp² Are Required",
        header_bg=GOLD,
        bg_color=CALLOUT_BG,
        bullets=[
            "<b>1. `p`-Values Only Measure Existence, Not Magnitude:</b> With `N = 180`, even a tiny 0.2-turn difference could yield `p < .05`. Reporting <b>Cohen's `d` and Partial `ηp²`</b> proves practical engineering magnitude (APA 7 & Cohen, 1988).",
            "<b>2. Scale-Free Comparison Across Metrics:</b> Raw turns (`5–13`), log turns (`1.61–2.15`), and `RER` (`0–1`) have different units. Standardized `Cohen's d = (M_adaptive − M_zero) / SD_pooled` expresses every gain in SD units:",
            (1, "• Against Cohen's `|d| ≥ 0.80` benchmark for a 'Large' effect, observed effects of <b>`d = −3.94` (DB), `d = −2.55` (OE), and `d = −3.40` (RCS)</b> (`3 to 4 standard deviations!`) and <b>`ηp² = .793` (`79.3%` variance explained)</b> prove extraordinary practical impact!"),
        ],
        font_size=8.6,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ4-Optimize Solution Approach Alignment (`Statistical Rigor of RQ4-Optimize Optimization`):</b> "
        "Combining `Raw Turns` (business ROI) + `Log Turns` (skewness normalization) + `2 × 3 ANOVA` (interaction proof) + `Cohen's d / ηp²` (effect magnitude) makes the RQ4-Optimize conclusion bulletproof for both business and statistics reviewers.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 47: RQ4-OPTIMIZE (RQ4 PART 5) — COMPARISON AGAINST HISTORICAL HUMAN CONSULTANTS (FIG. E3 & TABLE E5)
    # =========================================================================
    s = D.content_slide(
        "8. RQ4-Optimize Stage Results",
        "RQ4-Optimize (Part 5): Reference Context Against Historical Human Consultants",
        "Figure E3 & Table E5: Comparing Historical Human Wizards in Microsoft Frames vs. Zero-Shot LLM vs. Cluster-Adaptive Neuro-Symbolic Agent",
        notes="Walk through Figure E3 and Table E5, comparing the historical human wizards in Microsoft Frames against Zero-Shot and Cluster-Adaptive agents, and explaining why human logs serve as descriptive context.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq4_baseline_refined.png"),
        0.35, 1.48, 6.25, 4.78,
        caption="Figure E3: Historical Human Consultants (Frames) vs. Zero-Shot LLM vs. Cluster-Adaptive Agent (Turns & RER)",
    )
    D.add_table(
        s, 6.75, 1.48, 6.23, 2.75,
        headers=[
            "Refined Traveler Archetype (Table E5)",
            "Historical Human Wizards\nTurns M (SD) | RER",
            "Simulated Zero-Shot LLM\nTurns M (SD) | RER",
            "Cluster-Adaptive Agent\nTurns M (SD) | RER",
        ],
        rows=[
            [
                "1. Decisive Booker\n(45.0% of corpus)",
                "14.96 (6.08) turns\nRER = .052 (.074)",
                "7.60 (0.93) turns\nRER = .194 (.166)",
                "<b>5.00 (0.00) turns</b>\n<b>RER = .000 (.000)</b>",
            ],
            [
                "2. Open Explorer\n(25.5% of corpus)",
                "17.99 (6.65) turns\nRER = .061 (.081)",
                "7.47 (1.01) turns\nRER = .061 (.115)",
                "<b>5.27 (0.69) turns</b>\n<b>RER = .000 (.000)</b>",
            ],
            [
                "3. Rigid-Constraint Seeker\n(29.5% of corpus; 68% unbooked)",
                "10.64 (5.68) turns\nRER = .058 (.079)",
                "8.73 (1.55) turns\nRER = .072 (.119)",
                "<b>5.00 (0.00) turns</b>\n<b>RER = .000 (.000)</b>",
            ],
            [
                "Overall Corpus / Simulation Mean",
                "14.90 (6.74) turns\nRER = .056 (.077)",
                "7.93 (1.31) turns\nRER = .109 (.148)",
                "<b>5.09 (0.41) turns</b>\n<b>RER = .000 (.000)</b>",
            ],
        ],
        col_widths=[1.85, 1.46, 1.46, 1.46],
        font_size=8.5,
        align_left_cols=(0,),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_card(
        s, 6.75, 4.33, 6.23, 1.93,
        title="Analytical Interpretation of Human vs. Agent Benchmarks",
        header_bg=NAVY,
        bullets=[
            "<b>1. Why Human Wizards Averaged `10.64–17.99` Turns (`RER = .052–.061`):</b>",
            (1, "Human Wizards in Frames manually searched a live database across open-ended destinations and occasionally re-asked forgotten constraints (`5.6% RER`)."),
            "<b>2. Why `Zero-Shot` Had Higher `RER` Than Humans on Decisive Bookers (`19.4% vs. 5.2%`):</b>",
            (1, "Without a Symbolic Slot Ledger, `Zero-Shot` followed a rigid intake checklist that re-asked slots the Decisive Booker had already stated in Turn 1!"),
            "<b>3. Scope Boundary Note:</b> Human logs are presented as <b>descriptive domain context</b> (not a direct causal contrast) because human chats involved open-ended multi-city inquiry whereas RQ4-Optimize holds inventory constant at 4 packages.",
        ],
        font_size=8.6,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>RQ4-Optimize Complete — Preparing Final Solution Synthesis (Next Slide):</b> "
        "Across all 4 stages (`Identify → Personalize → Govern → Optimize`), every null hypothesis (`H01–H04`) has now been rejected at `p < .001`. Next, <b>Solution Approach #5</b> synthesizes the complete validated cascade.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 48: STORYLINE APPEARANCE #5 — COMPLETE VALIDATED 4-STAGE STORYLINE DIAGRAM
    # =========================================================================
    add_storyline_discovery_slide(D, stage_step=4)
