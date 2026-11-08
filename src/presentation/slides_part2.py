"""
Part 2 of the QM640 Capstone Defense Presentation (Slides 22–42):
  - Module 6 (Slides 22–34): Deep-Dive Empirical Results & Plain-English Walkthroughs for RQ1, RQ2, RQ3, and RQ4
  - Module 7 (Slides 35–38): Anticipated Defense Committee Questions & Direct Evidence-Backed Answers
  - Module 8 (Slides 39–42): Conclusive Story & Doctoral Dissertation Roadmap
    ("Dialogue Clustering and Methodologies to be Adapted for Human-Like Conversations")
"""

import os
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from presentation.ppt_styles import (
    BLUE,
    CALLOUT_BG,
    CARD_BG,
    CORAL,
    DARK,
    GOLD,
    GREEN,
    GREEN_BG,
    NAVY,
    RED_BG,
    TEAL,
    WHITE,
    _add_formatted_runs,
)
from report.final_context import FIG_FIN, FIG_INT, REPO


def build_slides_part2(D, ctx):
    # =========================================================================
    # SLIDE 22: RQ1 PART A — PRIMARY ALGORITHM BENCHMARK & EMBEDDING INVARIANCE
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ1)",
        "RQ1 (Part 1): Clustering Algorithm Benchmark Across 159 Runs & Embedding Invariance",
        "Table 12 & Figures D1–D2: Rejecting H01 (p < .001) across both MiniLM (384-d) and Gemini (3,072-d) spaces",
        notes="Explain how to read Table 12 and Figures D1-D2. Emphasize why K-Means (k=3) is chosen operationally despite HDBSCAN's higher raw Silhouette on retained points.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_k_selection.png"),
        0.35, 1.50, 5.45, 2.55,
        caption="Figure D1: Cluster-Number Selection (k = 2..8) on Golden Partition (k = 3 balances Silhouette & size ≥ 20%)",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_silhouette.png"),
        0.35, 4.15, 5.45, 2.95,
        caption="Figure D2: Cosine Silhouette Across 159 Subsample Runs (53 per Algorithm) vs. Permutation Baseline",
    )
    D.add_table(
        s, 5.95, 1.50, 7.03, 3.25,
        headers=["Embedding Family & Algorithm", "Runs", "Silhouette M (SD)", "Davies–Bouldin", "Parametric & Matched RM Tests", "η² / ηp²"],
        rows=[
            ["1. MiniLM (384-d) — K-Means (k = 3) [Alg. Winner: 100% Cov.]", "53", ".147 (.019)", "3.129 (0.113)", "One-way F(2, 156) = 91.33 (< .001)\nMatched RM F(1.72, 89.30) = 83.04", ".539 /\n.615"],
            ["2. MiniLM (384-d) — Agglomerative (Ward)", "53", ".118 (.040)", "3.550 (0.269)", "Welch F(2, 89.15) = 66.98 (< .001)\nPaired Friedman χ²(2) = 56.30 (< .001)", "—"],
            ["3. MiniLM (384-d) — HDBSCAN (39.1% noise)", "53", ".211 (.044)*", "2.657 (0.241)*", "Kruskal H(2) = 86.82 (< .001)\n*Excludes 39.1% noise dialogues", "—"],
            ["4. MiniLM (384-d) — Permutation Baseline", "53", "−.013 (.006)", "—", "Shuffled cluster labels (null)", "—"],
            ["5. Gemini-001 (3,072-d Turn Pool) — KM / Ward / HDB*", "159", ".158 / .150 / .289*", "35.8% HDB noise*", "F(2, 156) = 77.09 (< .001)", ".497"],
            ["6. Gemini-001 (3,072-d Document) [Best Space: KM=.161]", "159", ".161 / .213 / .345*", "25.7% HDB noise*", "F(2, 156) = 127.47 (< .001)", ".620"],
        ],
        col_widths=[2.45, 0.45, 1.15, 1.10, 1.35, 0.53],
        font_size=9.0,
        align_left_cols=(0,),
        highlight_rows=(0, 4, 5),
    )
    D.add_card(
        s, 5.95, 4.88, 7.03, 2.22,
        title="How to Compare the 3 Highlighted Rows (Row 1 → Row 5 → Row 6)",
        header_bg=NAVY,
        bullets=[
            "<b>1. Why Row 1 Is Highlighted (Winning Algorithm = K-Means, k = 3):</b> Within MiniLM (Rows 1–4), HDBSCAN discards <b>39.1% of customers as noise</b>, while K-Means (.147) beats Ward (.118, Tukey & Games–Howell <i>p</i> < .001) with <b>100% routing coverage</b>.",
            "<b>2. Why Row 6 Is the Best of the 3 Highlighted Rows (Row 1 < Row 5 < Row 6):</b> Moving from `MiniLM 384-d` (Row 1, KM=.147) to `Gemini 3,072-d Turn-Pool` (Row 5, KM=.158) and `Gemini 3,072-d Document` (Row 6) yields the <b>highest Silhouette (KM=.161, Ward=.213, HDB=.345) and largest effect size (F = 127.47, η² = .620)</b> because full-document Gemini preserves cross-turn context without MiniLM's 256-token cutoff.",
            "<b>3. What Moves Forward:</b> <b>Algorithm Winner (`K-Means k=3`) + Embedding Winner (`Gemini-001 Document`, Row 6)</b> are carried forward into the `46-d Blocks` model!",
        ],
        font_size=9.2,
    )

    # =========================================================================
    # SLIDE 23: RQ1 PART B — CROSS-CORPUS CHECK & WHY WHOLE-DIALOGUE CLUSTERS FAILED ROUTING
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ1)",
        "RQ1 (Part 2): Cross-Corpus Transfer & Diagnosis of Whole-Dialogue Archetypes",
        "Figure D3 & Tables D3–D4: Why clustering full transcripts caused wizard confounding (V = .45) and weak early routing (κ = .24)",
        notes="Show intellectual honesty and scientific rigor: explain what the diagnostic audit found on the initial whole-dialogue clusters and why that motivated the representation x truncation breakthrough.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_umap.png"),
        0.35, 1.50, 6.20, 5.55,
        caption="Figure D3: UMAP Projection of Frames Golden/Test Archetypes (Panel A) vs. MultiWOZ 2.2 Projection (Panel B)",
    )
    D.add_table(
        s, 6.70, 1.50, 6.28, 2.30,
        headers=["Partition / Corpus", "N", "Centroid Cosine M (SD)", "Direct Trans. (%)", "Constraint Neg. (%)", "Guided Exp. (%)"],
        rows=[
            ["Frames Golden (D_gold)", "933", ".466 (.116)", "42.3%", "37.6%", "20.0%"],
            ["Frames Held-Out (D_test)", "401", ".467 (.116)", "42.6%", "37.7%", "19.7%"],
            ["MultiWOZ 2.2 Sample", "1,499", ".269 (.115)", "71.4%", "28.6%", "0.1%"],
        ],
        col_widths=[1.7, 0.6, 1.3, 0.9, 0.9, 0.9],
        font_size=9.5,
        align_left_cols=(0,),
        highlight_rows=(0, 1),
    )
    D.add_card(
        s, 6.70, 3.92, 6.28, 3.13,
        title="Three Diagnostic Flaws Discovered in Whole-Dialogue Clustering",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>Check 1 — Internal vs. External Generalization (Table D4):</b>",
            (1, "Within Frames, Golden (.466) and Held-Out (.467) centroid similarity matched perfectly (<i>t</i> = −0.10, <i>p</i> = .923). Across corpora, MultiWOZ dropped to .269 (<i>t</i> = 28.08, <i>p</i> < .001) with 0.1% Guided Explorers—proving consultative travel archetypes are domain-specific."),
            "<b>Check 2 — Role-Player Confounding (Cramér's V = .45):</b>",
            (1, "Pooling both user and wizard turns caused clusters to reflect <i>which human wizard</i> handled the chat rather than the customer's own persona!"),
            "<b>Check 3 — Poor Early-Turn Routing (κ = .24) & Outcome Leakage:</b>",
            (1, "Predicting a whole-dialogue cluster from the first 5 turns achieved only κ = .24 (39.4% accuracy). Why? Because whole-dialogue clusters were separated by how the chat <i>ended</i> (Turn 15 booking vs. abandonment), which hasn't happened yet at Turn 3!"),
        ],
        font_size=10,
    )

    # =========================================================================
    # SLIDE 24: RQ1 PART C — REPRESENTATION × TRUNCATION BREAKTHROUGH & LLM CODEBOOK
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ1)",
        "RQ1 (Part 3): The Representation × Truncation Breakthrough (Figure D4 & Tables C2, D5–D6)",
        "Combining PCA-20 Gemini user prefix embeddings + 16-field LLM behavioral ratings on the first M = 9 user messages",
        notes="Explain how the three flaws were solved: (1) user turns only, (2) truncated to first M=9 user messages, and (3) paired with a validated 16-field LLM behavioral profile.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_truncation_2x2.png"),
        0.35, 1.50, 6.30, 5.55,
        caption="Figure D4: Bootstrap Stability (ARI), Core Membership, Early Routing, and Outcome Association Across M",
    )
    D.add_table(
        s, 6.80, 1.50, 6.18, 2.75,
        headers=["Prefix Horizon (m User Msgs / ≈T Turns)", "Dialogues > m", "Bootstrap ARI", "Raw Agreement p_o (κ)", "p_o (<m / ≥m Msgs)", "Outcome V"],
        rows=[
            ["m = 3 user msgs (≈ 5 total turns)", "96.0%", ".57", "59.4% (κ = .359)", "87.5% / 58.2%", ".14"],
            ["m = 5 user msgs (≈ 9 turns — RQ2 Runtime)", "83.2%", ".84", "70.1% (κ = .535)", "81.8% / 67.8%", ".17"],
            ["m = 7 user msgs (≈ 13 total turns)", "59.9%", ".85", "82.0% (κ = .722)", "93.2% / 74.6%", ".18"],
            ["m = 9 user msgs (Same-Feature Consistency)", "38.6%", ".89 (.87 abl.)", "97.3% (κ = .958)", "96.0% / 99.3%", ".20"],
            ["Whole conversation (Un-truncated)", "0.0%", ".62", "Confounded by outcome", "—", ".29"],
        ],
        col_widths=[1.85, 0.70, 0.72, 1.20, 1.13, 0.58],
        font_size=8.8,
        align_left_cols=(0,),
        highlight_rows=(1, 3),
    )
    D.add_card(
        s, 6.80, 4.38, 6.18, 2.67,
        title="Validating All 16 Fields of the LLM Behavioral Codebook (Table C2)",
        header_bg=TEAL,
        bullets=[
            "<b>16-Field `UserBehaviour` Schema (`step2e` & `step2g`):</b> <b>Fields 1–10</b> (10 ordinal 1–5 scales) + <b>Fields 11–13</b> (3 categorical goal/tone fields) form the 13 clustering inputs; <b>Fields 14–16</b> (`outcome`, `party_type`, `unusual_conversation`) are held out for post-hoc audit to prevent outcome leakage.",
            "<b>Test–Retest Reliability (n = 50, All 16 Fields):</b> Quadratic weighted <b>κ_w = .87 to .96</b> across Ordinal Fields 1–10 (mean .91) and <b>κ = .75 to .98</b> across Categorical/Audit Fields 11–16.",
            "<b>Ground-Truth Criterion Validity (N = 1,334 Frames Acts):</b>",
            (1, "LLM <i>revision_tendency</i> × ground-truth slot revisions: <b>Spearman ρ = .64 (p < .001)</b>."),
            (1, "LLM <i>exploration_breadth</i> × frame-switch rate: <b>ρ = .41 (p < .001)</b>."),
            (1, "LLM <i>information_upfront</i> × Turn-1 slot share: <b>ρ = .52 (p < .001)</b>."),
            "<b>Ablation Proof (Table D6):</b> Embeddings-only at <i>M</i>=9 gets ARI = .39; combining PCA-20 Gemini + 13 clustering behavioral fields (`Blocks`) reaches <b>ARI = .89 (.87 in 6-config ablation; DB = 2.647 lowest at k = 3)</b>!",
        ],
        font_size=9.5,
    )

    # =========================================================================
    # SLIDE 25: RQ1 PART D — PROFILES OF THE THREE REFINED USER ARCHETYPES (TABLE 13)
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ1)",
        "RQ1 (Part 4): Full 16-Field Profile of the Three Refined User Archetypes (Tables 13 & C1)",
        "Complete accounting of all 16 schema fields (10 ordinal + 3 categorical clustering + 3 audit-only) across D_gold (n = 933) and D_test (n = 401)",
        notes="Walk through Table 13 and Table C1 in detail. Point out how all 16 fields of the UserBehaviour schema differentiate Decisive Booker, Open Explorer, and Rigid-Constraint Seeker.",
    )
    D.add_table(
        s, 0.35, 1.48, 12.63, 4.38,
        headers=["Schema Field Group & Behavioral Attribute (All 16 Fields)", "Archetype 1: Decisive Booker", "Archetype 2: Open Explorer", "Archetype 3: Rigid-Constraint Seeker", "Operational Role in Clustering & Prompting (RQ1–RQ4)"],
        rows=[
            ["Golden (n=933) / Held-Out (n=401) Share", "420 (45.0%) / 165 (41.1%)", "238 (25.5%) / 140 (34.9%)", "275 (29.5%) / 96 (23.9%)", "Balanced partition (smallest cluster = 25.5% > 20% rule)"],
            ["Total Turns M (SD) / User Turns M", "14.96 (6.08) / 7.90", "17.99 (6.65) / 9.48", "10.64 (5.68) / 5.79", "Explorers converse 69% longer than Rigid-Constraint Seekers"],
            ["Fields 1–2 (ORD): Dest. / Date Flexibility", "2.54 / 2.57 (Moderate)", "3.49 / 2.77 (Open dest./dates)", "2.20 / 2.18 (Fixed city & dates)", "Offer multi-city alternatives only to Open Explorers"],
            ["Fields 3–4 (ORD): Exploration / Decisiveness", "1.97 (Focused) / 3.97 (Decisive)", "2.96 (Broad) / 2.58 (Deliberative)", "1.59 (Narrow) / 3.23 (Firm)", "Present 2–3 side-by-side options to Open Explorers"],
            ["Fields 5–6 (ORD): Detail / Revision Tendency", "2.39 / 2.00 (Low revisions)", "2.87 / 3.03 (Frequent pivots)", "1.46 / 2.40 (Constraint-focused)", "Proactive dual trade-off framing for Rigid-Constraint Seekers"],
            ["Fields 7–8 (ORD): Question Asking / Politeness", "2.05 / 4.26 (Warm, direct)", "2.72 / 3.80 (Inquisitive)", "1.43 / 3.07 (Terse, direct)", "Fast booking confirmation for Decisive Bookers"],
            ["Fields 9–10 (ORD): Price Sens. / Info Upfront", "3.20 / 2.18 (Stated early)", "3.18 / 1.82 (Gradual disclosure)", "3.12 / 2.16 (Hard ceiling)", "Calibrate budget-ceiling and package-tier emphasis"],
            ["Fields 11–13 (CAT Cluster): Goal / Sec. / Tone", "0.5% Exp, 99.3% Book | 42.4% | 52.4% Pos", "39.1% Exp, 50.8% Book | 56.3% | 69.3% Neut", "2.2% Exp, 89.8% Book | 16.4% | 7.6% Pos", "One-hot / multi-hot encoded into 16 binary cols (10+16 = 26 LLM cols)"],
            ["Fields 14–16 (AUDIT Only): Outcome / Party / Flag", "90.5% Booked | 37.1% Solo/Cpl | 1.0% Flag", "68.1% Booked | 44.5% Solo/Cpl | 1.7% Flag", "28.0% Booked (68.0% None) | 34.5% | 6.9%", "Excluded from clustering to prevent outcome leakage!"],
        ],
        col_widths=[2.85, 2.25, 2.35, 2.35, 2.83],
        font_size=8.8,
        align_left_cols=(0, 4),
        highlight_rows=(0, 2, 3, 7, 8),
    )
    D.add_callout(
        s, 0.35, 5.95, 12.63, 1.10,
        "<b>Statistical Interpretation of Reference Labels y<sup>(9)</sup>, Raw Agreement (p<sub>o</sub>), and Chance-Corrected κ (Section 5.1 & Appendix F):</b>\n"
        "Because Frames has no predefined persona labels, reference archetypes <i>y</i><sup>(9)</sup> are unsupervised <i>K</i>-Means (<i>k</i>=3) assignments on the <i>M</i>=9 `Blocks` space <i>X</i><sup>(9)</sup>. "
        "Prefix Logistic Regression classifiers trained on <i>D</i><sub>gold</sub> predict <i>y</i><sup>(9)</sup> from <i>m</i> ∈ {3, 5, 7, 9} user messages on <i>D</i><sub>test</sub> (<i>n</i> = 401; chance baseline <i>p<sub>e</sub></i> ≈ 35.4%–36.6%): "
        "<b>m = 3: κ = .359 (p<sub>o</sub> = 59.4%)</b> → <b>m = 5 (RQ2 runtime): κ = .535 (p<sub>o</sub> = 70.1%)</b> → <b>m = 7: κ = .722 (p<sub>o</sub> = 82.0%)</b>. At <b>m = 9, κ = .958 (p<sub>o</sub> = 97.3%)</b> is a <i>same-feature boundary-consistency check</i> on <i>X</i><sup>(9)</sup> (not human-label classification).",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.7,
    )

    # =========================================================================
    # SLIDE 26: RQ2 PART A — WHY PRIMARY ARCHETYPES FAILED (p=.211) & REFINED SUCCEEDED (p<.001)
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ2)",
        "RQ2 (Part 1): The Causal Contrast Between Primary (p = .211) and Refined (p < .001) Archetypes",
        "Figures E2 & 6: Proving that in-context style adaptation succeeds if and only if upstream routing is coherent",
        notes="This is one of the strongest scientific stories in the paper: contrasting Figure E2 (interim primary archetypes) against Figure 6 (refined archetypes).",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq2_results.png"),
        0.35, 1.50, 6.15, 3.85,
        caption="Figure E2 (Interim Primary Archetypes, Routing κ = .24): Style Cosine F = 1.61, p = .211 (Null)",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq2_refined_results.png"),
        6.80, 1.50, 6.18, 3.85,
        caption="Figure 6 (Final Refined Archetypes, Blocks Router κ = .535): Style Cosine F = 9.79, p < .001 (Reject H02!)",
    )
    D.add_card(
        s, 0.35, 5.45, 6.15, 1.60,
        title="Why Primary RQ2 Yielded a Null Style Effect (p = .211)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>1. Near-Chance Prefix Routing (39.4%, κ = .24):</b> 60.6% of held-out dialogues were routed to the <i>wrong</i> primary cluster at Turn 3.",
            "<b>2. Conflated Exemplar Pools:</b> Because primary clusters mixed user and wizard turns across whole sessions, retrieving from a cluster's FAISS pool fed mismatched examples into the prompt.",
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 6.80, 5.45, 6.18, 1.60,
        title="Why Refined RQ2 Decisively Rejected H02 (p < .001)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Accurate `Blocks` Prefix Routing (70.1%, κ = .535 at M = 5):</b> Test dialogues were routed to their true behavioral archetype.",
            "<b>2. Coherent Sub-Indices & Pacing Directives:</b> Retrieving <i>k</i> = 3 slot-masked exemplars from the matched refined archetype boosted style convergence (<b>F = 9.79, p < .001</b>) and cut pacing error to <b>3.87 words</b>.",
        ],
        font_size=10.2,
    )

    # =========================================================================
    # SLIDE 27: RQ2 PART B — DETAILED COMPUTATION OF TABLE 14 & HOLM CONTRASTS
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ2)",
        "RQ2 (Part 2): Detailed Computation of Table 14 & Holm-Adjusted Contrasts (Table E3)",
        "How to read every repeated-measures statistic (N = 33 held-out dialogues × 3 conditions = 99 Gemini 2.5 Flash calls)",
        notes="Walk through Table 14 and the pairwise Holm-Bonferroni contrasts in Table E3 so math and non-AI professors see every number clearly.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 3.25,
        headers=["Experiment & Outcome Metric (N = 33 Dialogues)", "Zero-Shot M (SD)", "Static Few-Shot M (SD)", "Cluster-Adaptive M (SD)", "RM-ANOVA F (GG df)", "p (GG)", "Partial ηp²", "Friedman χ² (p)"],
        rows=[
            ["Primary Archetypes (κ=.24) — Style Cosine", ".603 (.161)", ".650 (.165)", ".642 (.125)", "1.61 (1.95, 62.45)", ".211", ".048", "1.88 (.391)"],
            ["Primary Archetypes — Response Length (words)", "27.58 (5.43)", "16.33 (4.73)", "15.06 (4.35)", "95.32 (1.82, 58.31)", "< .001", ".749", "50.02 (< .001)"],
            ["Refined Archetypes (κ=.535) — SBERT Style Cosine (Primary DV)", ".530 (.132)", ".453 (.169)", ".597 (.086)", "9.79 (1.88, 60.29)", "< .001", ".234", "12.50 (.002)"],
            ["Refined Archetypes — Gemini 3,072-d Style Cosine", ".787 (.052)", ".775 (.055)", ".796 (.042)", "1.66 (1.94, 62.22)", ".200", ".049", "4.06 (.131)"],
            ["Refined Archetypes — Token-Level BERTScore F1", ".849 (.020)", ".844 (.023)", ".852 (.019)", "1.45 (1.92, 61.51)", ".243", ".043", "3.70 (.157)"],
            ["Refined Archetypes — Pacing Calibration Error (words)", "10.12 (8.98)", "6.33 (3.55)", "3.87 (3.58)", "7.10 (1.30, 41.70)", ".007", ".182", "14.27 (< .001)"],
            ["Refined Archetypes — Response Length (words)", "25.45 (9.17)", "14.48 (5.16)", "16.33 (3.52)", "31.92 (1.41, 45.24)", "< .001", ".499", "36.69 (< .001)"],
        ],
        col_widths=[3.1, 1.3, 1.3, 1.4, 1.6, 0.8, 0.9, 1.4],
        font_size=9.5,
        align_left_cols=(0,),
        highlight_rows=(2, 5),
    )
    D.add_card(
        s, 0.35, 4.90, 6.15, 2.15,
        title="Holm Contrasts & Metric Specificity (Why SBERT Moves While BERTScore Stays Flat)",
        header_bg=NAVY,
        bullets=[
            "<b>Combined Package & Holm Contrasts:</b> `Cluster-Adaptive` (jointly combining `Archetype Directive` + archetype-partitioned exemplars) beats `Static Few-Shot` by <b>Δ = +.144 (+31.8%, t = 4.26, p<sub>Holm</sub> < .001, d<sub>z</sub> = 0.74)</b> and `Zero-Shot` by <b>Δ = +.067 (t = 2.37, p<sub>Holm</sub> = .049, d<sub>z</sub> = 0.41)</b>.",
            "<b>Why SBERT Cosine Is Significant While Gemini & BERTScore Are Null:</b>",
            (1, "All 3 prompts reply to the <b>same dialogue context and travel topic</b>, so broad 3,072-d topical cosine (.775–.796, <i>p</i> = .200) and token-level `BERTScore F1` (.844–.852, <i>p</i> = .243) stay high and invariant."),
            (1, "Adaptation operates specifically on <b>sentence-level discourse structure (`all-MiniLM-L6-v2`, F = 9.79, p < .001) and pacing calibration (F = 7.10, p = .007)</b>!"),
        ],
        font_size=9.5,
    )
    D.add_card(
        s, 6.80, 4.90, 6.18, 2.15,
        title="Why Pacing Error Drops from 10.12 Words to 3.87 Words",
        header_bg=TEAL,
        bullets=[
            "<b>What Is Pacing Calibration Error (`word_abs_err`)?</b>",
            (1, "Formula: <b>|Words<sub>generated</sub> − μ<sub>Words, target archetype</sub>|</b>."),
            (1, "Human consultants use ~13 words for <i>Decisive Bookers</i>, ~19 words for <i>Open Explorers</i>, and ~15 words for <i>Rigid-Constraint Seekers</i>."),
            "<b>Why `Cluster-Adaptive` Wins on Pacing:</b>",
            (1, "`Zero-Shot` is overly verbose (25.5 words → 10.12w error). `Static Few-Shot` forces one fixed length (6.33w error). `Cluster-Adaptive` matches each archetype's exact pacing, cutting error to <b>3.87 words</b> (<i>p</i><sub>Holm</sub> = .008 vs. Static; <i>p</i><sub>Holm</sub> = .004 vs. Zero-Shot)!"),
        ],
        font_size=10,
    )

    # =========================================================================
    # SLIDE 28: RQ3 PART A — 2 × 2 FACTORIAL DESIGN, YAML RULES & DUAL-JUDGE RELIABILITY
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ3)",
        "RQ3 (Part 1): 2 × 2 Factorial Design, Declarative Rules & Dual-Judge Reliability",
        "Tables 9 & C3: Testing Rules Mode (Off vs. Active) × Prompting Strategy (Zero-Shot vs. Cluster-Adaptive) across N = 144 units",
        notes="Explain the 5 YAML policy rules (Table 9) and how the LLM judge was validated using an independent Gemini 2.5 Pro second judge (kappa = .917).",
    )
    D.add_table(
        s, 0.35, 1.50, 7.35, 3.35,
        headers=["Rule ID & Policy Name", "Deterministic Trigger Condition", "Action", "Severity"],
        rows=[
            ["RULE_VISA_LEAD_TIME:\nVisa Processing Lead Time", "departure_lead_days < 15 on international destination", "flag_warning", "high"],
            ["RULE_PASSPORT_VALIDITY:\nPassport 6-Month Validity", "passport_expiry_months < 6 on international trip", "block_booking", "critical"],
            ["RULE_PARTY_SIZE_LIMIT:\nMaximum FIT Adult Capacity", "traveler_count_adults > 4 and package_type == 'FIT'", "escalate_group_desk", "medium"],
            ["RULE_DISCOUNT_CAP:\nPromotional Discount Ceiling", "discount_applied_percentage > 15.0%", "cap_discount", "high"],
            ["RULE_MIN_BUDGET_INTL:\nMinimum International Budget", "budget_amount < $500 per adult on international package", "reject_and_reprompt", "high"],
        ],
        col_widths=[1.8, 2.8, 1.4, 0.9],
        font_size=9.8,
        align_left_cols=(0, 1, 2),
        highlight_rows=(0, 1, 2, 3, 4),
    )
    D.add_card(
        s, 7.85, 1.50, 5.13, 3.35,
        title="Cross-Model Dual-Judge Reliability (Table C3)",
        header_bg=NAVY,
        bullets=[
            "<b>Purpose of Two Independent Judge Models:</b>",
            (1, "To prevent self-preference bias, responses generated by `gemini-2.5-flash` were audited on a stratified 48-unit subsample by both `gemini-2.5-flash` (Judge 1) and the larger reasoning model <b>`gemini-2.5-pro` (Judge 2)</b>."),
            "<b>Empirical Reliability Results (n = 48):</b>",
            (1, "<b>Raw Agreement:</b> <b>95.8%</b> (46 / 48 units identical)."),
            (1, "<b>Cohen's Kappa:</b> <b>κ = .917</b> (PABAK = .917), far exceeding the a priori κ ≥ .70 threshold!"),
            (1, "<b>Agreement with Deterministic Regex Audit (N = 144):</b> <b>93.1% raw agreement (κ = .861)</b>."),
        ],
        font_size=10,
    )
    D.add_callout(
        s, 0.35, 5.02, 12.63, 2.03,
        "<b>How the 2 × 2 Factorial Experiment Was Constructed (N = 144, n = 36 per Cell, Seed = 42):</b>\n"
        "• 36 held-out test dialogues (12 per refined archetype) were paired with seeded Tier-2 policy states: exactly <b>50% (18 per cell) violated ≥ 1 YAML rule</b> (e.g., 10-day visa window, 4-month passport validity, 6 FIT adults, 25% discount request, or $350 international budget) and <b>50% (18 per cell) were 100% policy-compliant</b> (testing that the rule engine does not falsely block valid bookings).\n"
        "• In `Rules Off`, the prompt contains natural-language reminders of policies, and exemplars in `Cluster-Adaptive` are unmasked. In `Rules Active`, `RuleEngine` injects verified pre-check directives, masks exemplar slots with `[SLOT]`, and runs post-generation entity leakage sanitization.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=10.8,
    )

    # =========================================================================
    # SLIDE 29: RQ3 PART B — VISUAL INTERACTION PROFILES (FIGURE 7)
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ3)",
        "RQ3 (Part 2): 2 × 2 Factorial Interaction Profiles (Figure 7 Walkthrough)",
        "Visualizing orthogonal main effects (Panels A, C, D) versus the protective interaction on Exemplar Leakage (Panel B)",
        notes="Walk the committee through all 4 panels of Figure 7. Explain why Panel A/C/D have parallel lines while Panel B has sharply crossing/diverging lines.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq3_factorial_results.png"),
        0.35, 1.50, 7.55, 5.55,
        caption="Figure 7: 2 × 2 Factorial Interaction Profiles Across N = 144 Units (n = 36/cell; 95% CIs)",
    )
    D.add_card(
        s, 8.05, 1.50, 4.93, 5.55,
        title="How to Read the 4 Panels of Figure 7",
        header_bg=TEAL,
        bullets=[
            "<b>Panel A (Rule Adherence Rate):</b>",
            (1, "Lines are flat and parallel! Turning `Rules Active` jumps adherence from <b>.500</b> (only 5.6% on violating cases) to <b>.938</b> (98.6% on violating cases), <i>F</i> = 43.92, <i>p</i> < .001."),
            (1, "Changing prompt mode has <b>zero effect</b> (<i>F</i> = 0.01, <i>p</i> = .916) → proves prompt engineering alone cannot enforce rules!"),
            "<b>Panel B (Exemplar Entity Leakage — The Interaction):</b>",
            (1, "Sharp non-parallel divergence (<b>Interaction F = 34.82, p < .001</b>)!"),
            (1, "Under `Rules Off`, switching from Zero-Shot to Cluster-Adaptive spikes leakage from .000 to <b>.359 (55.6% incidence)</b>."),
            (1, "Under `Rules Active`, leakage stays at <b>.000 (0.0%)</b> in both conditions!"),
            "<b>Panel C (Factual Slot Coverage F1):</b>",
            (1, "Active rules + slot ledger jump Slot F1 from .208/.485 to <b>.977/.952</b> (<i>F</i> = 489.52, <i>p</i> < .001)."),
            "<b>Panel D (Style Alignment Cosine):</b>",
            (1, "Cluster-Adaptive prompting lifts style cosine in both modes (<i>F</i> = 24.00, <i>p</i> < .001)."),
        ],
        font_size=9.8,
    )

    # =========================================================================
    # SLIDE 30: RQ3 PART C — TABLE 15 COMPUTATION & REAL DIALOGUE PROOF
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ3)",
        "RQ3 (Part 3): Complete Table 15 Statistics & Side-by-Side Output Proof",
        "Proving that 'Rules Active × Cluster-Adaptive Few-Shot' is the unique Pareto-optimal configuration (Reject H03, p < .001)",
        notes="Show the exact numbers in Table 15 and read the real side-by-side LLM output comparison at the bottom.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 3.25,
        headers=["Experimental Cell or 2 × 2 ANOVA Effect", "n or df", "Rule Acc. | Viol. Sens. / Comp. Spec.", "Exemplar Leakage M (SD) / Inc. %", "Slot Coverage F1 M (SD)", "Style Alignment M (SD)"],
        rows=[
            ["Cell 1: Rules Off × Zero-Shot", "36", ".500 (.507) | 5.6% / 94.4%", ".000 (.000) / 0.0%", ".208 (.242)", ".414 (.124)"],
            ["Cell 2: Rules Off × Cluster-Adaptive", "36", ".500 (.507) | 5.6% / 94.4%", ".359 (.348) / 55.6%", ".485 (.269)", ".507 (.095)"],
            ["Cell 3: Rules Active × Zero-Shot", "36", ".944 (.232) | 100.0% / 88.9%", ".000 (.000) / 0.0%", ".977 (.096)", ".428 (.107)"],
            ["Cell 4: Rules Active × Cluster-Adaptive (Pareto Optimal)", "36", ".931 (.244) | 97.2% / 88.9%", ".000 (.000) / 0.0%", ".952 (.124)", ".506 (.086)"],
            ["ANOVA Main Effect: Rules Mode (OLS / HC3 / ART)", "1, 140", "Acc F=43.92 (< .001), ηp²=.239\n(Sens F=498.78; Spec F=0.69, p=.408)", "F = 34.82 (< .001), ηp² = .199*\n(Sum-HC3 F=33.85; ART F=43.48)", "F = 489.52 (< .001), ηp² = .778\n(HC3 F=471.70; ART F=691.34)", "F = 3.68 (.057), ηp² = .026\n(HC3 F=2.86; ART F=2.49)"],
            ["ANOVA Main Effect: Prompting Mode (OLS / HC3 / ART)", "1, 140", "Acc F = 0.01 (.916), ηp² = .000\n(HC3 F=0.05; ART F=0.01)", "F = 34.82 (< .001), ηp² = .199*\n(Sum-HC3 F=33.85; ART F=43.48)", "F = 20.46 (< .001), ηp² = .128\n(ART F=13.94, p < .001)", "F = 24.00 (< .001), ηp² = .146\n(HC3 F=20.62; ART F=25.38)"],
            ["ANOVA Interaction: Rules × Prompting (OLS / HC3 / ART)", "1, 140", "Acc F = 0.01 (.916), ηp² = .000\n(HC3 F=0.01; p = .918)", "F = 34.82 (< .001), ηp² = .199*\n(HC3 F=33.85; ART F=2148.81)", "F = 29.32 (< .001), ηp² = .173\n(HC3 F=28.51; ART F=180.38)", "F = 8.95 (.003), ηp² = .060\n(HC3 F=8.70; ART F=35.77)"],
        ],
        col_widths=[2.95, 0.75, 2.40, 2.30, 2.20, 2.03],
        font_size=9.0,
        align_left_cols=(0,),
        highlight_rows=(3, 4, 6),
    )
    D.add_card(
        s, 0.35, 4.90, 6.15, 2.15,
        title="Real Output Example: Rules Off × Cluster-Adaptive (Cell 2)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>Active User State:</b> Flying Dallas → Tokyo in <b>9 days</b> (violates 15-day visa rule), 2 adults, budget $2,600.",
            "<b>Generated Reply (Unguarded):</b> <i>'I can book you into the <b>Sapphire Bay Resort</b> on <b>SkyBridge Airways</b> for <b>$1,149</b> using code <b>VIP25</b>!'</i>",
            "<b>What Went Wrong:</b> Leaked 4 stale exemplar entities (`ELR = .80`) AND completely missed the 9-day visa lead-time violation (`RAR = 0`)!",
        ],
        font_size=10,
    )
    D.add_card(
        s, 6.80, 4.90, 6.18, 2.15,
        title="Real Output Example: Rules Active × Cluster-Adaptive (Cell 4)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>Same User State:</b> Dallas → Tokyo in <b>9 days</b>, 2 adults, budget $2,600.",
            "<b>Generated Reply (Neuro-Symbolic):</b> <i>'For your Dallas to Tokyo trip for 2 adults ($2,600 budget), please note that international departures within 15 days (9 days stated) require expedited visa verification before locking in your 9-night package.'</i>",
            "<b>Result:</b> <b>0.0% entity leakage</b>, <b>100% rule enforcement</b>, <b>1.00 Slot F1</b>, and crisp archetype-matched style!",
        ],
        font_size=10,
    )

    # =========================================================================
    # SLIDE 31: RQ4 PART A — 2 × 3 MULTI-TURN SIMULATION & PERSONA VALIDATION
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ4)",
        "RQ4 (Part 1): 2 × 3 Multi-Turn Simulation Design & Persona Fidelity Validation",
        "Testing Prompting Strategy (Zero-Shot vs. Cluster-Adaptive) × Refined Archetype across N = 180 closed-loop dialogues",
        notes="Explain how the RQ4 closed-loop simulation works, why the 4-option package inventory is realistic, and how Gemini 2.5 Pro validated the customer simulator at 95.6% accuracy (kappa = .933).",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 3.65,
        title="How the Closed-Loop Simulation Works (N = 180, n = 30/cell)",
        header_bg=NAVY,
        bullets=[
            "<b>1. Grounded Seed Trips:</b> 60 unique held-out test dialogues per archetype (180 distinct trip goals across 3 archetypes × 2 prompting modes = 180 between-subjects episodes; n = 30/cell).",
            "<b>2. Realistic 4-Option Travel Inventory per Dialogue:</b>",
            (1, "<b>Option A (4-Star Exact Match):</b> Exact destination & dates, 4-star hotel, priced at <b>88% of budget</b>."),
            (1, "<b>Option B (3.5-Star Saver):</b> Exact dates, boutique hotel, priced at <b>72% of budget</b>."),
            (1, "<b>Option C (5-Star Exact Dates — Over Budget):</b> 5-star luxury hotel on exact dates, priced at <b>118% of budget</b> (creates realistic constraint conflict!)."),
            (1, "<b>Option D (5-Star Shifted Dates — Within Budget):</b> 5-star luxury hotel with dates shifted +3 days, priced at <b>94% of budget</b>."),
            "<b>3. Stopping Criterion:</b> Conversation runs turn-by-turn until the user simulator issues `[ACCEPT_BOOKING]` (or hits 16-turn cap; `total_turns` = user + assistant messages).",
        ],
        font_size=9.8,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 3.65,
        title="Blind Persona Fidelity Audit by Gemini 2.5 Pro (Table C3)",
        header_bg=TEAL,
        bullets=[
            "<b>User Simulator Validation Protocol (n = 45 Transcripts):</b>",
            (1, "An independent `gemini-2.5-pro` judge read ONLY the customer utterances from 45 simulated dialogues (15 per archetype, blinded to condition and archetype label) and rated Decisiveness, Exploration Breadth, and Constraint Rigidity (1–5) plus predicted the archetype."),
            "<b>Validation Results (Within-Simulation Fidelity):</b>",
            (1, "<b>Blind Classification Accuracy:</b> <b>95.6% (43 / 45 correct)</b> vs. 33.3% chance (exact binomial <b>p = 1.37 × 10⁻¹⁸ < .001</b>, <b>Cohen's κ = .933</b>), confirming strong internal construct fidelity."),
            (1, "<b>Mean Behavioral Ratings (Decisiveness / Exploration / Rigidity):</b>\n"
                "      • <i>Decisive Booker:</i> <b>5.00</b> / 1.00 / 2.27\n"
                "      • <i>Open Explorer:</i> 2.80 / <b>4.27</b> / 1.60\n"
                "      • <i>Rigid-Constraint Seeker:</i> 1.67 / 2.27 / <b>4.33</b>"),
        ],
        font_size=9.8,
    )
    D.add_callout(
        s, 0.35, 5.30, 12.63, 1.75,
        "<b>Why Archetype-Specific Turn-Economy Policies Matter in RQ4:</b>\n"
        "• <b>Zero-Shot Baseline:</b> Uses a generic sequential policy—asks clarifying questions one by one and offers only Option A first, without a Verified Informed Slot Ledger.\n"
        "• <b>Cluster-Adaptive Few-Shot (Routed via `Blocks` at M = 9, κ = .958):</b> Combines the <b>Verified Informed Slot Ledger</b> (forbidding re-asking any stated slot) with archetype-specific action policies: (1) immediate Option A confirmation for <i>Decisive Bookers</i>; (2) side-by-side Option A vs. Option B comparison table for <i>Open Explorers</i>; and (3) proactive single-turn trade-off resolution (explaining Option C's budget conflict while presenting Option A [4-star exact date] and Option D [5-star flexible date]) for <i>Rigid-Constraint Seekers</i>.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=10.5,
    )

    # =========================================================================
    # SLIDE 32: RQ4 PART B — TURN ECONOMY & RER INTERACTION PROFILES (FIGURE 8)
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ4)",
        "RQ4 (Part 2): Multi-Turn Turn Economy & Redundant Elicitation Profiles (Figure 8)",
        "Rejecting H04 (p < .001): Massive main effect of prompting (F = 664.43) AND significant Prompt × Archetype interaction (F = 10.89)",
        notes="Walk the committee through Panels A and B of Figure 8. Explain why the turn reduction is steepest (−42.7%) for Rigid-Constraint Seekers.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq4_turn_economy_results.png"),
        0.35, 1.50, 7.55, 5.55,
        caption="Figure 8: Mean Turns to Goal Completion (Panel A) & Redundant Elicitation Rate (Panel B) Across N = 180 Simulations",
    )
    D.add_card(
        s, 8.05, 1.50, 4.93, 5.55,
        title="Visual Walkthrough of Figure 8",
        header_bg=NAVY,
        bullets=[
            "<b>Panel A (Turns to Goal Completion):</b>",
            (1, "Under `Zero-Shot` (coral bars), <i>Rigid-Constraint Seekers</i> take the longest (<b>8.73 turns</b>) because they reject Option A when their 5-star request exceeds budget, triggering multi-turn pushback loops."),
            (1, "Under `Cluster-Adaptive Few-Shot` (teal bars), turns drop dramatically across all three personas—and the drop is <b>steepest for Rigid-Constraint Seekers (−3.73 turns, −42.7%, 8.73 → 5.00 turns)</b>!"),
            (1, "This non-uniform compression produces the highly significant <b>Prompt × Archetype interaction: F(2, 174) = 10.89, p < .001, ηp² = .111</b>."),
            "<b>Panel B (Redundant Elicitation Rate — RER):</b>",
            (1, "Under `Zero-Shot`, the bot re-asks already stated slots in <b>19.4%</b> of turns for Decisive Bookers (who state many slots up front), 6.1% for Open Explorers, and 7.2% for Rigid Seekers."),
            (1, "Under `Cluster-Adaptive Few-Shot` with the Verified Informed Slot Ledger, RER drops to <b>0.000 (0.0%) across all 90 dialogues</b> (<i>F</i> = 63.02, <i>p</i> < .001)!"),
        ],
        font_size=10,
    )

    # =========================================================================
    # SLIDE 33: RQ4 PART C — DETAILED COMPUTATION OF TABLE 16 & CONTRASTS
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ4)",
        "RQ4 (Part 3): Complete Table 16 Statistics, Simple Contrasts & Robust Checks",
        "100% concordance across OLS ANOVA, HC3 heteroscedasticity-robust F, Aligned Rank Transform (ART), Welch t, and Mann–Whitney U",
        notes="Walk through every row of Table 16 so the committee sees both raw turns, log turns, RER, Cohen's d, and non-parametric checks.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 3.70,
        headers=["Archetype × Prompting Cell or 2 × 3 ANOVA Effect", "Total Turns M (SD)", "Log Turns ln(TGC) M (SD)", "Redundant Elicitation (RER)", "Turn Reduction Δ (%)", "Simple Contrast (Welch t / Mann–Whitney U / Cohen's d)"],
        rows=[
            ["Decisive Booker — Zero-Shot (n = 30)", "7.60 (0.93)", "2.021 (0.119)", ".194 (.166)", "—", "—"],
            ["Decisive Booker — Cluster-Adaptive (n = 30)", "5.00 (0.00)", "1.609 (0.000)", ".000 (.000)", "−2.60 turns (−34.2%)", "t_log = −18.92 (p < .001), U = 0.0 (p < .001), d = −3.94"],
            ["Open Explorer — Zero-Shot (n = 30)", "7.47 (1.01)", "2.002 (0.130)", ".061 (.115)", "—", "—"],
            ["Open Explorer — Cluster-Adaptive (n = 30)", "5.27 (0.69)", "1.654 (0.115)", ".000 (.000)", "−2.20 turns (−29.5%)", "t_log = −10.97 (p < .001), U = 40.5 (p < .001), d = −2.55"],
            ["Rigid-Constraint Seeker — Zero-Shot (n = 30)", "8.73 (1.55)", "2.152 (0.175)", ".072 (.119)", "—", "—"],
            ["Rigid-Constraint Seeker — Cluster-Adaptive (n = 30)", "5.00 (0.00)", "1.609 (0.000)", ".000 (.000)", "−3.73 turns (−42.7%)", "t_log = −17.02 (p < .001), U = 0.0 (p < .001), d = −3.40"],
            ["ANOVA Main Effect: Prompting (df = 1, 174)", "F = 457.74 (< .001), ηp² = .725", "F = 664.43 (< .001), ηp² = .793", "F = 63.02 (< .001), ηp² = .266", "HC3 F_log = 681.53 (< .001)", "ART F_log = 224.22 (< .001)"],
            ["ANOVA Main Effect: Archetype (df = 2, 174)", "F = 7.77 (< .001), ηp² = .082", "F = 5.55 (.005), ηp² = .060", "F = 7.57 (< .001), ηp² = .080", "HC3 F_log = 5.86 (.003)", "ART F_log = 207.29 (< .001)"],
            ["ANOVA Interaction: Prompting × Archetype (df = 2, 174)", "F = 14.37 (< .001), ηp² = .142", "F = 10.89 (< .001), ηp² = .111", "F = 9.70 (< .001), ηp² = .100", "HC3 F_log = 8.58 (< .001)", "ART F_log = 209.46 (< .001)"],
        ],
        col_widths=[2.8, 1.5, 1.6, 1.6, 1.9, 3.2],
        font_size=9.2,
        align_left_cols=(0, 5),
        highlight_rows=(1, 3, 5, 6, 8),
    )
    D.add_callout(
        s, 0.35, 5.35, 12.63, 1.70,
        "<b>Structural Protocol Floor (`5.00 Turns, SD = 0.00`) & Human Baseline Context (Table E5):</b>\n"
        "• `total_turns` counts total messages (`user_turns + assistant_turns`). Because each seed opens with 3/5 slots stated, the minimum trajectory is <b>5 messages (`U1 → A1 [bundled intake] → U2 [remaining slots] → A2 [archetype-tailored quote] → U3 [ACCEPT_BOOKING]`)</b>. `Cluster-Adaptive` achieves this deterministic 5.00-turn floor (`SD = 0.00`) across all 30 <i>Decisive Bookers</i> and 30 <i>Rigid-Constraint Seekers</i> (confirmed by `HC3 F = 681.53`, `ART F = 224.22`, and `Mann–Whitney U = 0.0, p < .001`).\n"
        "• Historical human wizards in Microsoft Frames averaged <b>14.96, 17.99, and 10.64 turns</b> (`RER = .052–.061`), provided as descriptive context (given open-ended human exploration).",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.7,
    )

    # =========================================================================
    # SLIDE 34: CONSOLIDATED HYPOTHESIS SCORECARD & ENTERPRISE ROI SYNTHESIS
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (Synthesis)",
        "Consolidated Hypothesis Testing Scorecard (Table 11) & Illustrative Operational ROI",
        "All four null hypotheses (H01–H04) are rejected at p < .001 with large effect sizes and substantial operational savings",
        notes="Present Table 11 as the master executive summary of all empirical findings, followed by the illustrative operational scenario.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 3.55,
        headers=["Research Question & Outcome", "Sample & Design", "Baseline vs. Proposed Performance", "Primary Parametric Test & Effect Size", "Robust / Non-Parametric Check", "Decision"],
        rows=[
            ["RQ1: Algorithm Separation &\nRefined Prefix Routing", "N = 159 runs\n(D_gold=933, D_test=401)", "Perm. Sil = −.013 vs. KM = .147, HDB = .211 (39.1% noise);\nBlocks ARI = .89 (.87 abl.); Routing κ = .535 (M=5) to .958 (M=9)", "One-way F(2, 156) = 91.33, p < .001, η² = .54\nMatched RM F(1.72, 89.30) = 83.04, ηp² = .615", "Friedman χ²(2) = 56.30, p < .001;\nWelch F = 66.98; Kruskal H = 86.82", "Reject H01\n(p < .001)"],
            ["RQ2: Style Convergence &\nPacing Error (Refined)", "N = 33 dialogues × 3\nconditions (99 calls)", "Style Cos: Static = .453, Zero = .530 vs. Adaptive = .597\nPacing Error: Zero = 10.12w, Static = 6.33w vs. Adaptive = 3.87w", "Style F(1.88, 60.29) = 9.79, p < .001, ηp² = .234\nPacing F(1.30, 41.70) = 7.10, p = .007, ηp² = .182", "Friedman χ² = 12.50 (p = .002) &\n14.27 (p < .001); Holm p < .001", "Reject H02\n(p < .001)"],
            ["RQ3: Policy Rule Adherence,\nLeakage & Slot F1", "N = 144 (2 × 2,\nn = 36/cell; κ_judge = .917)", "Viol. Sens.: 5.6% (Off) → 98.6% (Active); Comp. Spec.: 94.4% vs 88.9%\nFew-Shot Leakage: .359 (55.6%) → .000 (0.0%); Slot F1: .485 → .952", "RAR Acc F(1, 140) = 43.92; Sens F(1, 68) = 498.78\nELR Int. F = 34.82, p < .001; Slot F1 F = 489.52", "Sum-HC3 F = 42.71 & 33.85 (p < .001);\nART F = 39.12 & 2148.81 (p < .001)", "Reject H03\n(p < .001)"],
            ["RQ4: Multi-Turn Economy\n(Log Turns & RER)", "N = 180 (2 × 3,\nn = 30/cell; κ_persona = .933)", "Turns: −34.2% (DB), −29.5% (OE), −42.7% (RCS)\nOverall Turns: 7.93 → 5.09 (−35.8%); RER: .109 → .000", "Prompt F(1, 174) = 664.43, p < .001, ηp² = .793\nPrompt × Arch Int. F(2, 174) = 10.89, p < .001, ηp² = .111", "HC3 Int. F = 8.58, p < .001;\nART Int. F = 209.46, p < .001", "Reject H04\n(p < .001)"],
        ],
        col_widths=[2.0, 1.6, 3.1, 2.5, 2.2, 1.2],
        font_size=9.3,
        align_left_cols=(0, 1, 2, 3, 4),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_card(
        s, 0.35, 5.20, 12.63, 1.85,
        title="Illustrative Operational Scenario (Hypothetical OTA Handling 1,000,000 Monthly Sessions)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Illustrative Cloud Inference & Latency Savings (−35.8%):</b> Under a hypothetical 1M-session monthly volume, compressing mean turns from 7.93 (`Zero-Shot`) to 5.09 (`Cluster-Adaptive`) corresponds to <b>2.84 fewer messages per session (≈ 2.84M fewer message turns/month)</b> in simulation.",
            "<b>2. Zero Exemplar Leakage & Policy Enforcement:</b> Eliminating exemplar entity leakage (55.6% incidence → <b>0.0%</b>) and raising violation sensitivity from 5.6% to <b>98.6%</b> (`F = 498.78, p < .001`, while preserving 88.9% compliant specificity) mitigates policy compliance failures.",
            "<b>3. Rescuing Rigid-Constraint Shoppers:</b> Proactive single-turn trade-off framing cuts simulated negotiation turns by <b>42.7%</b> for the segment that experienced a 68.0% non-booking rate in historical human logs.",
        ],
        font_size=10.2,
    )

    # =========================================================================
    # SLIDE 35: DEFENSE Q&A 1 — SAMPLE SIZE ASSUMPTIONS & VALIDATION
    # =========================================================================
    s = D.content_slide(
        "Module 7: Anticipated Defense Q&A Bank",
        "Defense Q&A #1: 'What Assumptions Were Taken to Arrive at Sample Sizes?'",
        "Direct, rigorous answer prepared for statistical and quantitative methodology reviewers on the defense panel",
        notes="Use this slide if asked Question #1: What are the assumptions taken to arrive at proper sample sizes?",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 5.45,
        title="Five Explicit A Priori Assumptions (`step0_sample_size.py`)",
        header_bg=NAVY,
        bullets=[
            "<b>Assumption 1 — Type I Error Control (α = .05, two-tailed / omnibus F):</b>",
            (1, "A standard 5% false-positive ceiling was set across all primary omnibus tests, supplemented by Tukey HSD (RQ1) and Holm–Bonferroni (RQ2) familywise error control for pairwise contrasts."),
            "<b>Assumption 2 — Target Statistical Power (1 − β ≥ .80, β ≤ .20):</b>",
            (1, "Following Cohen (1988), false-negative risk was set at ≤ 20%, requiring noncentrality λ = 8.00 (<i>df</i><sub>1</sub> = 1) to λ = 9.88 (<i>df</i><sub>1</sub> = 2)."),
            "<b>Assumption 3 — Medium Minimum Detectable Effect Size (f = .25):</b>",
            (1, "Every experiment was powered to detect at least a medium effect (<i>f</i> = .25, equivalent to η<sup>2</sup> ≈ .059 or ~6% explained variance) so that any statistically significant effect also carries practical engineering meaning."),
            "<b>Assumption 4 — Within-Dialogue Correlation (ρ = .50) & Sphericity (ε = 1.0) in RQ2:</b>",
            (1, "For repeated-measures RQ2, moderate within-dialogue correlation ρ = .50 was specified across the <i>m</i> = 3 prompt conditions."),
            "<b>Assumption 5 — +10% Cell-Balancing & Attrition Buffer:</b>",
            (1, "Minimum sample sizes (<i>N</i><sub>min</sub> = 158, 28, 128, 158) were buffered by ≥ 10% to exact integer multiples of cell counts: <b>159 (53×3), 33 (11×3), 144 (36×4), and 180 (30×6)</b>, achieving final a priori power of <b>.804 to .865</b>."),
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 5.45,
        title="Post-Hoc Empirical Audit: Did the Data Satisfy Every Assumption?",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Observed Effect Sizes Far Exceeded f = .25 (η² = .059):</b>",
            (1, "• RQ1 Algorithm η<sup>2</sup> = <b>.497 to .620</b> (Matched RM η<sub><i>p</i></sub><sup>2</sup> = <b>.615</b>)"),
            (1, "• RQ2 Refined Style η<sub><i>p</i></sub><sup>2</sup> = <b>.234</b> (<i>f</i> = 0.55) & Pacing η<sub><i>p</i></sub><sup>2</sup> = <b>.182</b> (<i>f</i> = 0.47)"),
            (1, "• RQ3 Rules RAR η<sub><i>p</i></sub><sup>2</sup> = <b>.239</b>, Leakage Int. η<sub><i>p</i></sub><sup>2</sup> = <b>.199</b>, Slot F1 η<sub><i>p</i></sub><sup>2</sup> = <b>.778</b>"),
            (1, "• RQ4 Log Turns Prompt η<sub><i>p</i></sub><sup>2</sup> = <b>.793</b>, Interaction η<sub><i>p</i></sub><sup>2</sup> = <b>.111</b> (<i>f</i> = 0.35)"),
            (1, "→ Achieved post-hoc power > <b>.99</b> on all primary main effects and > <b>.95</b> on interactions!"),
            "<b>2. Handling Violations of Normality & Homoscedasticity:</b>",
            (1, "Classical ANOVA assumes normal residuals and equal cell variances. Because RQ3/RQ4 rates are bounded in [0, 1], inference did NOT rely on normality alone: every test was paired with <b>Welch / HC3 sandwich estimators</b> and <b>Aligned Rank Transform (ART) / Friedman / Kruskal–Wallis</b> tests."),
            "<b>3. How the +18% Buffer Protected RQ2 Under Sphericity Departure:</b>",
            (1, "In RQ2 pacing error, Greenhouse–Geisser ε was 0.65 (reducing effective <i>df</i> from 2, 64 to 1.30, 41.70). Buffering <i>N</i> from 28 to 33 ensured the GG-adjusted test still achieved <i>p</i> = .007!"),
        ],
        font_size=10.2,
    )

    # =========================================================================
    # SLIDE 36: DEFENSE Q&A 2 & 3 — PRIOR RESEARCH USED VS. UNIQUE ORIGINALITY
    # =========================================================================
    s = D.content_slide(
        "Module 7: Anticipated Defense Q&A Bank",
        "Defense Q&A #2 & #3: 'What Prior Research Was Used, and What Is Original?'",
        "Clear demarcation between inherited scientific building blocks and the five original contributions of this study",
        notes="Use this slide to answer Defense Questions #2 and #3 concisely and authoritatively.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 5.55,
        headers=["Scientific Component", "Q2: Prior Research Foundations & Application", "Q3: Original Contributions in This Study (Not Present in Prior Literature)"],
        rows=[
            [
                "1. User Trajectory Representation & Archetype Discovery (RQ1)",
                "Used <b>Sentence-BERT</b> (Reimers & Gurevych, 2019), <b>Gemini 3,072-d Embeddings</b> (Lee et al., 2025), <b>K-Means / Ward / HDBSCAN</b> (McInnes et al., 2017), <b>Bootstrap ARI</b> (Hennig, 2007), and <b>zero-temp LLM rating reliability</b> (Gilardi et al., 2023).",
                "<b>Original Contribution 1:</b> Discovered that whole-dialogue clustering in consultative travel is confounded by wizard identity (<i>V</i> = .45) and session outcome (<i>V</i> = .29). Designed the <b>prefix-truncated (M = 9 user messages) hybrid `Blocks` representation</b> (PCA-20 Gemini prefix + 16-field LLM behavioral codebook) and `RefinedArchetypeRouter`, achieving <b>ARI = .89 (.87 in ablation)</b> and out-of-sample prefix routing of <b>κ = .535 (M=5) to .958 (M=9)</b>.",
            ],
            [
                "2. Archetype-Routed In-Context Learning (RQ2)",
                "Built upon <b>few-shot in-context learning</b> (Brown et al., 2020), <b>KATE nearest-neighbor example selection</b> (Liu et al., 2022), <b>FAISS vector indexing</b> (Johnson et al., 2021), and <b>BERTScore</b> (Zhang et al., 2020).",
                "<b>Original Contribution 2:</b> Partitioned FAISS into <b>archetype-specific sub-indices with `[SLOT]` masking</b> and demonstrated a <b>critical routing dependency</b> by contrasting Primary (<i>p</i> = .211) vs. Refined (<i>p</i> < .001) archetypes: dynamic exemplar retrieval + directives improve style (+31.8% over static, <i>d<sub>z</sub></i> = 0.74) and pacing (3.87w error) when upstream prefix routing exceeds κ > .50.",
            ],
            [
                "3. Neuro-Symbolic Policy Verification & Leakage Control (RQ3)",
                "Drew motivation from <b>NeMo Guardrails</b> (Rebedea et al., 2023), <b>τ-bench policy failure benchmarks</b> (Yao et al., 2024), and <b>TD-EVAL</b> (Acikgoz et al., 2025).",
                "<b>Original Contribution 3:</b> Executed a <b>2 × 2 factorial experiment crossing declarative rule verification with cluster-adaptive prompting</b>. Quantified the <b>35.9% exemplar entity leakage hazard</b> (55.6% incidence) of unguarded few-shot prompting and demonstrated a significant interaction (<i>F</i> = 34.82, <i>p</i> < .001) where symbolic verification reduces leakage to <b>0.0%</b> while raising violation enforcement sensitivity from <b>5.6% to 98.6%</b>.",
            ],
            [
                "4. Multi-Turn Turn Economy & Slot Ledger (RQ4)",
                "Built on <b>hospitality service ROI theory</b> (Buhalis & Sinarta, 2019; Ivanov & Webster, 2019; Melián-González et al., 2021) and <b>travel agency interaction analysis</b> (Inaba et al., 2022).",
                "<b>Original Contribution 4:</b> Designed the <b>Verified Informed Slot Ledger + Archetype-Specific Turn-Economy Policy</b> and demonstrated a <b>2 × 3 Prompting × Archetype interaction (F = 10.89, p < .001)</b>: compressing multi-turn sessions by <b>29.5% to 42.7%</b> (largest gain for <i>Rigid-Constraint Seekers</i>, <i>d</i> = −3.40) and eliminating redundant slot questions (<b>RER .109 → .000</b>).",
            ],
        ],
        col_widths=[2.2, 4.7, 5.7],
        font_size=10,
        align_left_cols=(0, 1, 2),
        highlight_rows=(0, 1, 2, 3),
    )

    # =========================================================================
    # SLIDE 37: DEFENSE Q&A 4 — DATASET AUTHENTICITY, PURPOSE & RESEARCH FIT
    # =========================================================================
    s = D.content_slide(
        "Module 7: Anticipated Defense Q&A Bank",
        "Defense Q&A #4: 'What Is the Authenticity of the Datasets & How Do They Fit the Study?'",
        "Addressing corpus provenance, why they were created, why they fit, and how structural boundaries were resolved",
        notes="Use this slide when asked Question #4 about dataset authenticity and fit.",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 5.45,
        title="1. Authenticity & Original Purpose of the Two Datasets",
        header_bg=NAVY,
        bullets=[
            "<b>Microsoft Frames (El Asri et al., 2017 — Maluuba / Microsoft Research):</b>",
            (1, "<b>Authenticity:</b> 100% real human–human dialogues (1,369 sessions, 19,986 turns) collected over 20 days between trained human travel agents ('wizards' with live inventory access) and human travelers."),
            (1, "<b>Original Purpose:</b> Created specifically to move beyond simple slot-filling and capture <b>multi-turn consultative vacation package negotiation, budget trade-offs, and non-linear frame-switching</b>."),
            "<b>MultiWOZ 2.2 (Budzianowski et al., 2018; Zang et al., 2020 — Cambridge / Google):</b>",
            (1, "<b>Authenticity:</b> Peer-reviewed ACL/EMNLP standard benchmark (10,438 human–human dialogues; 1,499 analytic travel subset used here) with Google-verified slot span annotations."),
            (1, "<b>Original Purpose:</b> Created to benchmark supervised multi-domain Dialogue State Tracking (DST) across local city services (hotel, train, taxi, attraction)."),
        ],
        font_size=10.5,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 5.45,
        title="2. Research Fit & Resolution of Structural Boundaries",
        header_bg=TEAL,
        bullets=[
            "<b>Why Microsoft Frames Is the Ideal Match for RQ1–RQ4:</b>",
            (1, "Unlike synthetic LLM-generated datasets, Frames contains natural human decision-making heterogeneity—hesitations, price bargaining, city comparisons, and 25.8% unbooked sessions—allowing authentic discovery of <i>Decisive Bookers</i>, <i>Open Explorers</i>, and <i>Rigid-Constraint Seekers</i>."),
            "<b>Why MultiWOZ 2.2 Is the Ideal External Contrast:</b>",
            (1, "Because MultiWOZ has transactional city bookings without flight+hotel package bargaining, the RQ1 transfer check (<i>t</i> = 28.08, <i>p</i> < .001) empirically proves that consultative travel archetypes are distinct from generic slot-filling."),
            "<b>Transparently Bridging Two Corpus Boundaries:</b>",
            (1, "<b>Boundary A (Tier-2 Enterprise Rules):</b> Public corpora do not log visa windows or passport expiry (0% in Table E1/E4). Exact held-out Frames user prefixes were preserved and paired with controlled, seeded Tier-2 states in RQ3."),
            (1, "<b>Boundary B (Interactive Multi-Turn Evaluation in RQ4):</b> Static corpus logs cannot reply to new chatbot actions. Persona simulators were seeded from real held-out Frames trip goals and verified at <b>95.6% persona fidelity (κ = .933)</b> via blind `gemini-2.5-pro` audit."),
        ],
        font_size=10.5,
    )

    # =========================================================================
    # SLIDE 38: DEFENSE Q&A 5 & 6 — ADDITIONAL HIGH-PROBABILITY COMMITTEE QUESTIONS
    # =========================================================================
    s = D.content_slide(
        "Module 7: Anticipated Defense Q&A Bank",
        "Defense Q&A #5 & #6: Judge Independence, Cold-Start Routing & Model Choice",
        "Prepared answers for deep technical questions from AI/ML and systems faculty",
        notes="Extra defense Q&A slide covering LLM-as-judge validity, cold-start Turn 1 routing, and Gemini 2.5 Flash/Pro model selection.",
    )
    D.add_card(
        s, 0.35, 1.50, 4.05, 5.45,
        title="Q5: 'Isn't Using an LLM Judge Circular or Biased?'",
        header_bg=NAVY,
        bullets=[
            "<b>Three-Layer Defense Against Judge Bias:</b>",
            "<b>1. Deterministic Primary Metrics:</b>",
            (1, "In RQ1, Silhouette, DB, and ARI are 100% mathematical. In RQ2, SBERT cosine (`all-MiniLM-L6-v2`) and BERTScore (`roberta-large`) use independent non-Gemini encoders! In RQ3 & RQ4, Exemplar Leakage, Slot F1, Turns, and RER are computed by <b>deterministic Python regex/set verifiers</b> (`src/final_pipeline/metrics.py`)."),
            "<b>2. Cross-Model Dual-Judge Audit (RQ3):</b>",
            (1, "`gemini-2.5-flash` was cross-checked against the larger independent `gemini-2.5-pro` judge on <i>n</i> = 48 units: <b>95.8% raw agreement, κ = .917</b>, and <b>93.1% agreement (κ = .861)</b> with deterministic regex verification."),
            "<b>3. Blind Persona Audit (RQ4):</b>",
            (1, "`gemini-2.5-pro` was completely blinded to archetype labels and still classified 43/45 simulated users correctly (<b>95.6%, κ = .933</b>)."),
        ],
        font_size=10,
    )
    D.add_card(
        s, 4.60, 1.50, 4.10, 5.45,
        title="Q6: 'What Happens When Turns < 9? How Long Are Frames Chats?'",
        header_bg=TEAL,
        bullets=[
            "<b>1. Total Turns (T) vs. User Messages (M) in Frames (N = 1,334):</b>",
            (1, "Total turns (User + Agent) average <b>14.93 (Mdn = 14.0)</b>: <b>96.4% have ≥ 5 total turns</b> and <b>83.2% have ≥ 9 total turns (≥ 5 user msgs)</b>. User-only messages average 7.78 (37.6% ≥ 9 user msgs)."),
            "<b>2. Are Predictions Wrong When User Messages < 9? No!</b>",
            (1, "• <b>M = 3 user msgs (≈ 5 turns):</b> <b>59.4% overall (κ = .359)</b>; <b>87.5%</b> on short chats (<3 user msgs)."),
            (1, "• <b>M = 5 user msgs (≈ 9 turns — RQ2 Runtime):</b> <b>70.1% overall (κ = .535)</b>; <b>81.8%</b> on <5-msg chats & <b>67.8%</b> on ≥5-msg chats—sufficient to yield <i>p</i> < .001 in RQ2!"),
            (1, "• <b>M = 7 user msgs (≈ 13 turns):</b> <b>82.0% overall (κ = .722)</b>; <b>93.2%</b> on <7-msg & <b>74.6%</b> on ≥7-msg chats."),
            (1, "• <b>M = 9 user msgs (≈ 17 turns — Offline Cap `min(M,9)`):</b> <b>97.3% overall (κ = .958)</b>; <b>96.0%</b> on ≤9-msg chats (full user history seen) & <b>99.3%</b> on long ≥9-msg chats!"),
        ],
        font_size=9.5,
    )
    D.add_card(
        s, 8.90, 1.50, 4.08, 5.45,
        title="Q7: 'Why Not Fine-Tune a Model Instead of Using FAISS + Rules?'",
        header_bg=BLUE,
        bullets=[
            "<b>Three Enterprise Reasons Why Neuro-Symbolic ICL Beats Fine-Tuning:</b>",
            "<b>1. Instant Policy Updates (< 1 ms):</b>",
            (1, "When visa lead times or promo discount caps change at an OTA, updating `rules_enterprise.yaml` takes 1 second with 100% deterministic enforcement—whereas fine-tuning an LLM takes hours and still hallucinates rules."),
            "<b>2. Zero Catastrophic Forgetting:</b>",
            (1, "Adding new exemplary human dialogues to the three FAISS sub-indices requires zero gradient updates."),
            "<b>3. Explainability & Auditability:</b>",
            (1, "Every turn logs the exact predicted archetype, the 3 retrieved FAISS dialogue IDs, and the exact YAML rule IDs triggered—providing a complete compliance audit trail."),
        ],
        font_size=10,
    )

    # =========================================================================
    # SLIDE 39: DEFENSE Q&A #8 — QUOTATION AGREEMENT VS. REAL-WORLD BOOKING NOISE
    # =========================================================================
    s = D.content_slide(
        "Module 7: Anticipated Defense Committee Questions",
        "Defense Q&A #8: Quotation Agreement vs. Real-World Booking — Avoiding Exogenous Noise",
        "Why linking commercial checkout bookings directly to chat turns induces noise, how literature handles it, and what RQ4 measures",
        notes="Address the crucial distinction between reaching an agreed trip quotation inside the chat vs. external booking conversion.",
    )
    D.add_card(
        s, 0.35, 1.50, 4.05, 4.35,
        title="1. The Real-World Attribution Problem:\nQuotation Agreement vs. Paid Booking",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>Logical End of a Customer–Seller Chat:</b>",
            (1, "In travel counseling, a conversation naturally concludes when the seller sends an <b>agreed itinerary & package quotation</b>."),
            "<b>Why Final Booking Conversion Has Massive Noise:</b>",
            (1, "Whether a customer pays for that quotation depends on <b>exogenous off-chat factors</b> outside the agent's control:"),
            (2, "• Getting a last-minute coupon/discount from a competing travel startup."),
            (2, "• Arranging personal accommodation with friends or relatives and booking flight-only tickets independently."),
            (2, "• Family/spouse schedule changes or credit-card limits."),
            (1, "<b>Consequence:</b> Linking raw checkout conversion directly to chat turns confounds conversational quality with external market noise!"),
        ],
        font_size=9.6,
    )
    D.add_card(
        s, 4.60, 1.50, 4.10, 4.35,
        title="2. How Research Literature & the RQ1\nDesign Handle This Noise",
        header_bg=NAVY,
        bullets=[
            "<b>PARADISE Framework (Walker et al., 1997) & TOD Surveys (Deriu et al., 2021; Kwan et al., 2023):</b>",
            (1, "Explicitly decouple <b>Dialogue-Internal Goal Resolution</b> (reaching a valid matching quotation) from exogenous commercial checkout."),
            "<b>Microsoft Frames (El Asri et al., 2017) & MultiWOZ 2.2:</b>",
            (1, "Frames has no external payment—its `book` act is strictly <b>verbal itinerary/quotation agreement</b>. MultiWOZ separates `Inform` (valid quote) from `Success` (reference delivery)."),
            "<b>RQ1 Diagnostic & Solution (`step2g`):</b>",
            (1, "Whole-dialogue clustering was confounded by session outcome (<i>V</i> = .29 → poor early routing κ = .24)."),
            (1, "Making <b>Field 14 (`outcome`) AUDIT-ONLY</b> (excluded from clustering) and truncating at `min(M, 9)` ensures personas reflect <i>how users shop</i>, not whether they bought!"),
        ],
        font_size=9.5,
    )
    D.add_card(
        s, 8.90, 1.50, 4.08, 4.35,
        title="3. What Economy Does RQ4 Measure?\nTurns to Agreed Package Quotation!",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>Exact Operational Definition in `step4_rq4_simulation.py`:</b>",
            (1, "• <b>Goal Slots (5):</b> `origin_city`, `destination_city`, `departure_date`, `duration_nights`, `budget_amount` (+ `adults`)."),
            (1, "• <b>Quotation Catalog:</b> 3 concrete package quotes (Option A 4-Star, Option B 3.5-Star, Option C/D 5-Star)."),
            (1, "• <b>Stopping Criterion (`total_turns` & `RER`):</b> The turn counter stops the moment the agent elicits the missing slots (with 0% redundant re-asking) and presents a feasible <b>package quotation</b> (hotel, star tier, dates, total price) that the customer agrees fits their plan (`[ACCEPT_BOOKING]`)."),
            "<b>Why This Is Noise-Free:</b>",
            (1, "RQ4 measures <b>Turns to Quotation Agreement</b> (cutting turns from 10.37–13.20 down to <b>6.80–9.30 turns, −29.5% to −42.7%</b>)—the exact part of the funnel the chatbot controls!"),
        ],
        font_size=9.5,
    )
    D.add_callout(
        s, 0.35, 5.98, 12.63, 1.05,
        "<b>Defense Takeaway & Doctoral Dissertation Link:</b>\n"
        "Trying to predict post-chat payment from dialogue text alone conflates chatbot quality with competitor pricing and personal lodging alternatives. "
        "This capstone isolates <b>conversational quotation efficiency (Turns to Agreed Quotation & Redundant Elicitation Rate)</b>, while the doctoral dissertation roadmap extends this into a two-stage model separating <i>Stage 1 (In-Chat Quotation Agreement)</i> from <i>Stage 2 (Post-Quote Conversion with External Price/Competitor Controls)</i>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=10.3,
    )

    # =========================================================================
    # SLIDE 40: DEFENSE Q&A #9 — MULTI-OPTION EXPLORATION (2-3 OPTIONS) & TURN ECONOMY
    # =========================================================================
    s = D.content_slide(
        "Module 7: Anticipated Defense Committee Questions",
        "Defense Q&A #9: Handling Flexible Customers Who Explore 2–3 Options Before Quotation",
        "Separating healthy multi-option comparison (Open Explorer) from chatbot inefficiency via side-by-side comparative quoting",
        notes="Explain how multi-option exploration is captured in Frames, separated into Open Explorer in RQ1, and served via side-by-side 3-option comparison in RQ4.",
    )
    D.add_card(
        s, 0.35, 1.50, 4.05, 3.85,
        title="1. Dataset & RQ1 Level: Separating\nHealthy Exploration from Inefficiency",
        header_bg=NAVY,
        bullets=[
            "<b>Why Customers Explore 2–3 Options:</b>",
            (1, "In real travel planning, flexible customers rarely lock onto 1 option immediately—they compare 2–3 destinations or hotel tiers before agreeing on a quotation, which naturally increases turn count."),
            "<b>How Microsoft Frames Captures This:</b>",
            (1, "Every alternative option creates a new semantic `Frame` (`switch_frame` & `compare` acts). The LLM codebook (`exploration_breadth` & `revision_tendency`) correlates strongly with ground-truth frame switching (<b>ρ = .41 to .73, p < .001</b>)."),
            "<b>How RQ1 Clustering Isolates It (Table 13):</b>",
            (1, "<b>Archetype 2 (`Open Explorer`, 25.5%)</b> specifically captures these shoppers: high destination flexibility (<b>3.49/5</b>), high exploration breadth (<b>2.96/5</b>), and the longest human dialogues (<b>17.99 turns</b> vs. 14.96 for Decisive Bookers)."),
        ],
        font_size=9.5,
    )
    D.add_card(
        s, 4.60, 1.50, 4.10, 3.85,
        title="2. How Zero-Shot Fails Open Explorers\n(Sequential 1-Option Ping-Pong = 13.20 Turns)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>What Happens in `Zero-Shot` (`step4_rq4_simulation.py`):</b>",
            (1, "In RQ4, the `Open Explorer` simulator is explicitly programmed to <b>refuse quotation agreement until it has compared at least 2–3 distinct within-budget package options</b>."),
            (1, "• <b>Mistake 1 (Redundant Intake):</b> Zero-Shot asks one slot at a time and re-asks stated slots (10.7% RER)."),
            (1, "• <b>Mistake 2 (Single-Option Quoting):</b> Zero-Shot presents only <b>1 package option per turn</b> (<i>'Here is Option A...'</i>)."),
            (1, "• <b>Resulting Turn Inflation:</b> The customer has to ask <i>'What other package or hotel tier options do you have?'</i> across multiple sequential turns, dragging the chat out to <b>13.20 turns</b>!"),
        ],
        font_size=9.5,
    )
    D.add_card(
        s, 8.90, 1.50, 4.08, 3.85,
        title="3. How Cluster-Adaptive Serves Them\n(Side-by-Side 3-Option Quote = 9.30 Turns)",
        header_bg=TEAL,
        bg_color=GREEN_BG,
        bullets=[
            "<b>`Open Explorer` Policy (`step4_rq4_simulation.py` L173–180):</b>",
            (1, "When `RefinedArchetypeRouter` identifies an `Open Explorer`, it does <b>NOT</b> rush them or restrict their choices."),
            (1, "Instead, once budget is known, the agent presents a <b>structured SIDE-BY-SIDE COMPARISON of 3 distinct quotations in a SINGLE turn</b>:"),
            (2, "• <b>Option A:</b> 4-Star Value Match ($2,288)"),
            (2, "• <b>Option B:</b> 3.5-Star Boutique + Breakfast ($2,054)"),
            (2, "• <b>Option D:</b> 5-Star Flexible-Date Deal ($2,470)"),
            (1, "• <b>Result:</b> The customer still compares all 3 options, but selects their preferred quotation immediately—cutting wasted ping-pong turns by <b>−29.5% (13.20 → 9.30 turns, p < .001)</b>!"),
        ],
        font_size=9.5,
    )
    D.add_table(
        s, 0.35, 5.48, 12.63, 1.55,
        headers=["Refined User Archetype", "Option Exploration Behavior", "Human Logs Turns M", "RQ4 Zero-Shot Turns M", "RQ4 Cluster-Adaptive Turns M", "Turn Savings (Δ%) & Mechanism"],
        rows=[
            ["Decisive Booker (45.0%)", "Fixed route/date; wants 1 matching quote fast", "14.96", "10.37", "6.80", "−34.2% (Direct confirmation + 0% RER)"],
            ["Open Explorer (25.5%)", "Flexible; compares 2–3 options before quote agreement", "17.99 (Longest)", "13.20 (Longest)", "9.30 (Still longest!)", "−29.5% (3-option side-by-side quote in 1 turn)"],
            ["Rigid-Constraint Seeker (29.5%)", "Strict ceiling conflict; needs feasible trade-off quote", "10.64 (68% walk away)", "12.80", "7.33", "−42.7% (Dual 4★ exact vs 5★ shifted-date quote)"],
        ],
        col_widths=[2.25, 3.10, 1.45, 1.45, 1.65, 2.73],
        font_size=9.0,
        align_left_cols=(0, 1, 5),
        highlight_rows=(1,),
    )

    # =========================================================================
    # SLIDE 41: DEFENSE Q&A #10 — WHY 3 BEHAVIORAL ARCHETYPES VS. 500+ PARAMETER CLUSTERS?
    # =========================================================================
    s = D.content_slide(
        "Module 7: Anticipated Defense Committee Questions",
        "Defense Q&A #10: Why Cluster by 3 Behavioral Archetypes Instead of 500+ Trip-Parameter Clusters?",
        "Why clustering on Origin × Destination × Travel Window × Pax × Budget fails for prompting—and how it seeds the Doctoral Dissertation",
        notes="Address the committee question: Why not cluster on mandatory trip parameters (Destination, Window, Pax, Origin, Budget) into 500+ micro-clusters?",
    )
    D.add_card(
        s, 0.35, 1.50, 4.05, 4.30,
        title="1. Same 5 Trip Parameters ≠ Same\nConversational Strategy (WHAT vs. HOW)",
        header_bg=NAVY,
        bullets=[
            "<b>Parameters Tell SQL <i>WHAT</i> to Query; Archetypes Tell the LLM <i>HOW</i> to Converse:</b>",
            (1, "Suppose 3 customers share the <b>exact same 5 parameters</b>: <i>Dallas → Cancun, Aug 12 (5 nights), 2 adults, $2,400</i>. In a 500-cluster parameter taxonomy, all 3 land in the <b>same cluster</b>, yet:"),
            (2, "• <b>Customer A (Decisive Booker):</b> Wants a crisp 14-word confirmation of 1 package to close in 6 turns."),
            (2, "• <b>Customer B (Open Explorer):</b> Used Cancun only as an initial idea (3.49/5 flexibility) and wants to compare 3 resort options side-by-side."),
            (2, "• <b>Customer C (Rigid Seeker):</b> Insists on a 5★ resort under $2,400 (costs $2,688) and walks away unless given a dual 4★ vs. shifted-date 5★ trade-off!"),
            (1, "<b>RQ3 Proof Against Entity Clustering (Table 15):</b>"),
            (2, "Retrieving unmasked exemplars by concrete cities/prices causes <b>35.9% Entity Leakage (`ELR`) across 55.6% of replies</b>! De-lexicalizing entities (`[DST_CITY]`) + symbolic slot ledgers gives <b>0.0% leakage</b>."),
        ],
        font_size=9.2,
    )
    D.add_card(
        s, 4.60, 1.50, 4.10, 4.30,
        title="2. Mathematical & Operational Collapse\nat k = 500+ Parameter Clusters",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>1. Combinatorial Sparsity & Sample Starvation:</b>",
            (1, "50 origins × 50 destinations × 12 months × 4 pax × 4 budget tiers = <b>480,000 cells</b>. Even at <i>k</i> = 500 clusters across <i>N</i> = 933 golden dialogues, each cluster averages <b>933 / 500 = 1.86 dialogues</b>—insufficient to retrieve <i>k</i><sub>shot</sub> = 3 successful exemplars!"),
            "<b>2. Early-Turn Cold-Start Failure:</b>",
            (1, "At Turn 2–3, an <i>Open Explorer</i> often hasn't stated a destination, date, or budget yet (<i>'Somewhere warm in September'</i>). A parameter router fails when slots are `None`, whereas the behavioral router already achieves <b>59.4%–70.1% accuracy</b>!"),
            "<b>3. Statistical Power Collapse (Eq. 1):</b>",
            (1, "In the RQ1 grid (`step2g`), even <i>k</i> > 4 violated cluster adequacy (<20%) and lowered bootstrap ARI. Powering <i>k</i> = 500 at 80% power requires <i>N</i> > 15,000 dialogues."),
        ],
        font_size=9.3,
    )
    D.add_card(
        s, 8.90, 1.50, 4.08, 4.30,
        title="3. Combining Both Layers\n+ Doctoral Dissertation Extension!",
        header_bg=TEAL,
        bg_color=GREEN_BG,
        bullets=[
            "<b>How the Current Architecture Uses Mandatory Parameters Without 500 Brittle Clusters:</b>",
            (1, "• <b>Macro-Layer (<i>k</i> = 3 Archetypes):</b> Selects the conversational policy (<i>Decisive</i> vs. <i>Explorer</i> vs. <i>Rigid</i>)."),
            (1, "• <b>Micro-Layer (Continuous FAISS <i>k</i>-NN):</b> Searches inside the archetype sub-index (`IndexFlatIP`) for the 3 closest structural neighbors—giving continuous local precision without sample starvation!"),
            (1, "• <b>Symbolic Layer (`RuleEngine` + Slot Ledger):</b> Injects exact `Origin`, `Dest`, `Window`, `Pax`, `Budget` with <b>.952 Slot F1</b>."),
            "<b>Doctoral Dissertation Pillar 1 (Context × Behavior):</b>",
            (1, "While raw city names shouldn't be clustered, <b>macro trip regimes</b> (<i>Family Group vs. Solo Business, High-Stakes Luxury vs. Weekend Budget, Urgent Lead Time</i>) <b>DO influence user behavior</b>—motivating a <b>Two-Tier Hierarchical Taxonomy (C × K = 24–30 micro-personas)</b> in the dissertation!"),
        ],
        font_size=9.2,
    )
    D.add_callout(
        s, 0.35, 5.93, 12.63, 1.10,
        "<b>Summary Defense Answer:</b>\n"
        "Clustering into 500+ raw parameter buckets confuses <i>database slot filtering</i> with <i>conversational style adaptation</i>, starves each bucket to <2 dialogues, and triggers 35.9% entity leakage when unmasked. "
        "However, exploring how <b>situational trip regimes (party type, budget stakes, lead window) interact with behavioral archetypes</b> is a major research question formally incorporated as <b>Pillar 1 of the Doctoral Dissertation Roadmap</b>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=10.3,
    )

    # =========================================================================
    # SLIDE 42: DEFENSE Q&A #11 — CLUSTER NAME DERIVATION (APPENDIX F) & JUDGE LLM ROLE (APPENDIX G)
    # =========================================================================
    s = D.content_slide(
        "Module 7: Anticipated Defense Committee Questions",
        "Defense Q&A #11: Who Named the 3 Clusters (Appendix F) & What Is the Judge LLM's Role (Appendix G)?",
        "Deterministic centroid-mapping rules (`step2i`) vs. independent cross-verification gatekeeping (`gemini-2.5-pro`)",
        notes="Explain Appendix F (how K-Means integer IDs 0, 1, 2 are mapped to archetype names) and Appendix G (why the Judge LLM is strictly a cross-verification validator).",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 4.30,
        title="1. Appendix F (Table F1): How Cluster Names Are Derived\n(K-Means Outputs Integers 0, 1, 2 — Not English Names!)",
        header_bg=NAVY,
        bullets=[
            "<b>Why a Deterministic Naming Rule Is Needed:</b>",
            (1, "Unsupervised <i>K</i>-Means (`step2g_rq1_truncation.py`) outputs anonymous integer cluster IDs (`0`, `1`, `2`) that can permute across random seeds (the <i>label-switching problem</i>)."),
            "<b>Pre-Declared Python Rule on Golden Centroid Means (`step2i_rq1_refined_archetypes.py`):</b>",
            (1, "• <b>Step 1 — `idxmax(destination_flexibility)` → <i>Open Explorer</i>:</b>"),
            (2, "Cluster with highest mean destination flexibility (<b>3.49/5.0</b>) & exploration breadth (<b>2.96/5.0</b>; longest chats = <b>17.99 turns</b>; <i>n</i> = 238, 25.5%)."),
            (1, "• <b>Step 2 — `idxmax(decisiveness)` of remaining 2 → <i>Decisive Booker</i>:</b>"),
            (2, "Cluster with highest decisiveness (<b>3.97/5.0</b>), politeness (<b>4.26/5.0</b>), and <b>99.3%</b> specific booking goal (<i>n</i> = 420, 45.0%)."),
            (1, "• <b>Step 3 — Remaining cluster ID → <i>Rigid-Constraint Seeker</i>:</b>"),
            (2, "Lowest destination/date flexibility (<b>2.20 / 2.18</b>) and <b>68.0%</b> no-suitable-option rate under strict ceilings (<i>n</i> = 275, 29.5%)."),
            (1, "<i>(Primary clusters in `step2_rq1_clustering.py` use the same logic: `idxmax(turns_M)` → Guided Explorer; `idxmax(revisions)` → Constraint Negotiator; remaining → Direct Transactional.)</i>"),
        ],
        font_size=9.3,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 4.30,
        title="2. Appendix G (Table G1): What Is the Judge LLM Used For?\n(Strictly Cross-Verification & Gatekeeping — Not Inventing Metrics!)",
        header_bg=TEAL,
        bullets=[
            "<b>All 4 Primary Hypothesis Tests (H<sub>01</sub>–H<sub>04</sub>) Use Deterministic Math/Python Metrics:</b>",
            (1, "• <b>RQ1:</b> Mathematical Silhouette, Davies–Bouldin, ARI (.89 / .87), and κ (.359–.958). (Note: `gemini-2.5-flash` at temp=0 is used <i>before</i> K-Means as the 16-field behavioral codebook annotator, validated at κ<sub><i>w</i></sub> = .87–.96 & ρ = .30–.73.)"),
            (1, "• <b>RQ2:</b> Non-Gemini encoders (`all-MiniLM-L6-v2` cosine, `roberta-large` BERTScore F<sub>1</sub>, exact word error). Zero Judge LLM used!"),
            (1, "• <b>RQ3 & RQ4:</b> Exact Python string/set entity-leakage verifier (`ELR`), Slot F<sub>1</sub>, deterministic turn counter, and regex slot-ledger (`RER`)."),
            "<b>Exact Role of Independent `gemini-2.5-pro` Judge (Pure Validator, Table C3 & G1):</b>",
            (1, "• <b>Pilot Gatekeeper:</b> Caught a prompt-ordering issue in RQ3 (`pilot_v1` → `pilot_v2`) before full execution."),
            (1, "• <b>RQ3 Cross-Verifier (<i>n</i> = 48):</b> Corroborated policy compliance with <b>95.8% agreement (κ = .917)</b> vs. `flash` and <b>93.1% (κ = .861)</b> vs. deterministic regex."),
            (1, "• <b>RQ4 Blind Persona Auditor (<i>n</i> = 45):</b> Verified simulated customer personas with <b>95.6% blind accuracy (κ = .933)</b> without contributing any metric to the RQ4 ANOVA table!"),
        ],
        font_size=9.2,
    )
    D.add_callout(
        s, 0.35, 5.93, 12.63, 1.10,
        "<b>Defense Takeaway (Appendices F & G):</b>\n"
        "The <b>Judge LLM does not by itself invent or contribute any standalone performance metric</b> to firm up the paper. Had `gemini-2.5-pro` found major contradictions (κ < .70), it would have triggered rework or manual human re-annotation; because it strongly corroborated the deterministic verifiers (κ = .861–.933), its role in the final paper is strictly that of an <b>independent quality-assurance validator</b>.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=10.2,
    )

    # =========================================================================
    # SLIDE 39: THE CONCLUSIVE STORY OF THE PAPER ACROSS RQ1–RQ4
    # =========================================================================
    s = D.content_slide(
        "Module 8: Conclusive Story & Doctoral Dissertation Roadmap",
        "The Conclusive Story: How RQ1–RQ4 Transform Conversational Travel AI",
        "Requirement #5a: Integrating all four empirical findings into one cohesive scientific and business conclusion",
        notes="Deliver the overarching synthesis of the entire capstone: how each question's data builds the complete picture.",
    )
    D.add_card(
        s, 0.35, 1.50, 3.05, 4.20,
        title="Stage 1 (RQ1): IDENTIFY\nDiscover Who Is Talking",
        header_bg=NAVY,
        bullets=[
            "<b>Empirical Finding (Reject H<sub>01</sub>):</b>",
            (1, "K-Means (<i>k</i>=3) achieves 100% coverage (<i>F</i> = 91.33, <i>p</i> < .001), whereas HDBSCAN drops 39.1% as noise."),
            (1, "`46-d Blocks` (PCA-20 Gemini prefix + 26 LLM behavioral cols at <i>M</i>=9) yields 3 stable personas (<b>ARI = .89 / .87</b>) and lifts held-out routing from κ = .24 to <b>.535 (M=5) & .958 (M=9)</b>."),
            "<b>Decision & Carried-Forward Output ➔ RQ2–RQ4:</b>",
            (1, "Locks in the <b>3 `46-d Blocks` Archetypes</b>, `RefinedArchetypeRouter`, and <b>3 Partitioned 46-d FAISS Sub-Indices</b>."),
        ],
        font_size=9.5,
    )
    D.add_card(
        s, 3.55, 1.50, 3.05, 4.20,
        title="Stage 2 (RQ2): PERSONALIZE\nAdapt How the Agent Speaks",
        header_bg=TEAL,
        bullets=[
            "<b>Empirical Finding (Reject H<sub>02</sub>):</b>",
            (1, "Inherits RQ1's `46-d Blocks` router & FAISS sub-indices across <i>N</i> = 33 test chats (11 per `Blocks` archetype)."),
            (1, "Coarse clusters (κ = .24) failed (<i>p</i> = .211); `46-d Blocks` routing (κ = .535) boosted style cosine (<b>.453 → .597, F = 9.79, p < .001</b>) and cut pacing error to <b>3.87 words (p = .007)</b>."),
            "<b>Decision & Carried-Forward Output ➔ RQ3–RQ4:</b>",
            (1, "Drops Static Few-Shot; carries forward <b>`Cluster-Adaptive` (k=3 46-d FAISS + Pacing Directives)</b>."),
        ],
        font_size=9.5,
    )
    D.add_card(
        s, 6.75, 1.50, 3.05, 4.20,
        title="Stage 3 (RQ3): GOVERN\nGuard Against Leakage & Policy Drift",
        header_bg=CORAL,
        bullets=[
            "<b>Empirical Finding (Reject H<sub>03</sub>):</b>",
            (1, "Inherits RQ1's `46-d Blocks` clusters (12/archetype/cell = 36/cell, <i>N</i> = 144) + RQ2's `Cluster-Adaptive` prompt."),
            (1, "Unguarded few-shot leaks stale entities in <b>55.6% of replies (ELR = .359)</b> and misses <b>94.4%</b> of rule violations."),
            (1, "`Rules Active` cuts leakage to <b>0.0% (Int. F = 34.82)</b>, raises rule sensitivity to <b>98.6%</b>, and lifts Slot F1 to <b>.952</b>."),
            "<b>Decision & Carried-Forward Output ➔ RQ4:</b>",
            (1, "Locks <b>`Rules Active` (`[SLOT]` masking + 5 YAML rules)</b> ON for RQ4."),
        ],
        font_size=9.5,
    )
    D.add_card(
        s, 9.95, 1.50, 3.03, 4.20,
        title="Stage 4 (RQ4): OPTIMIZE\nCompress Multi-Turn Negotiations",
        header_bg=GREEN,
        bullets=[
            "<b>Empirical Finding (Reject H<sub>04</sub>):</b>",
            (1, "Inherits RQ1's <b>3 `46-d Blocks` Archetypes</b> (Factor B: 30 trips/cell × 6 = 180 chats) + RQ2's `[SLOT]` FAISS + RQ3's active `RuleEngine`."),
            (1, "Cuts turns by <b>−42.7% for Rigid Seekers</b>, <b>−34.2% for Decisive</b>, and <b>−29.5% for Explorers</b> (<i>F</i> = 664.43, Int. <i>F</i> = 10.89, <i>p</i> < .001) and RER from <b>.109 → .000</b>."),
            "<b>Final Locked Architecture ➔ Dissertation:</b>",
            (1, "Validates the full 4-stage stack (`RQ1+RQ2+RQ3+RQ4`) & seeds Doctoral Pillars 1–6."),
        ],
        font_size=9.5,
    )
    D.add_callout(
        s, 0.35, 5.85, 12.63, 1.20,
        "<b>Master Conclusion of the Paper:</b>\n"
        "Improving enterprise conversational AI is not a matter of choosing between 'better prompts' OR 'strict rules'. It requires a <b>three-part neuro-symbolic synergy</b>: (1) <b>Early Behavioral-Semantic Routing</b> (`Blocks`) to know <i>who</i> the user is; (2) <b>Slot-Masked Archetype Exemplar Retrieval</b> to adapt <i>how</i> the assistant communicates and frames trade-offs; and (3) <b>Declarative Symbolic Verification & Slot Ledgers</b> to guarantee <i>what</i> the assistant says is 100% policy-compliant, grounded, and non-repetitive.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=11,
    )

    # =========================================================================
    # SLIDE 44: WHERE THIS CAPSTONE ENDS — OPEN QUESTIONS FOR DOCTORAL RESEARCH
    # =========================================================================
    s = D.content_slide(
        "Module 8: Conclusive Story & Doctoral Dissertation Roadmap",
        "Where This Capstone Ends: Six Scientific Frontiers Opened by the Findings",
        "Requirement #5b: Fundamental boundaries in RQ1–RQ4 and enterprise travel deployment that motivate a full Doctoral Dissertation",
        notes="Transition from the master's capstone findings to the 6 frontiers motivating the doctoral dissertation, including Enterprise Call Stages (a-f) and 200-Package USP Narrowing.",
    )
    D.add_card(
        s, 0.35, 1.48, 4.08, 2.68,
        title="Frontier 1: Continuous Manifold vs. Hard K-Means",
        header_bg=NAVY,
        bullets=[
            "<b>Capstone Finding (RQ1):</b>",
            (1, "While <i>K</i>-Means (<i>k</i> = 3) achieved high stability (ARI = .89/.87), raw Silhouette (.094–.345) and PCA Biplot (Fig. 3) show styles form a <b>continuous manifold</b>."),
            "<b>What Remains Unsolved for the Dissertation:</b>",
            (1, "25.2% of speakers sit near cluster boundaries (e.g., 55% <i>Explorer</i> / 45% <i>Rigid</i>). Hard argmax routing forces a binary choice rather than soft style blending."),
        ],
        font_size=8.8,
    )
    D.add_card(
        s, 4.62, 1.48, 4.08, 2.68,
        title="Frontier 2: Dynamic Mid-Session Persona Drift",
        header_bg=TEAL,
        bullets=[
            "<b>Capstone Finding (RQ1 & RQ4):</b>",
            (1, "The prefix router assigns a static persona after <i>M</i> = 5–9 messages. Yet real travelers <b>shift personas mid-chat</b> (e.g., <i>Open Explorer</i> → <i>Rigid Seeker</i> after sticker shock)."),
            "<b>What Remains Unsolved for the Dissertation:</b>",
            (1, "Modeling user style as a <b>non-stationary stochastic trajectory z<sub><i>t</i></sub></b> updated turn-by-turn from Turn 1 via Bayesian belief filtering."),
        ],
        font_size=8.8,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 2.68,
        title="Frontier 3: Enterprise Call Stages (a–f) & Lead Propensity",
        header_bg=GREEN,
        bullets=[
            "<b>Enterprise Call-Stage Reality:</b>",
            (1, "Enterprise agent turns follow <b>6 Call Stages</b>: <b>(a)</b> Opening, <b>(b)</b> Mandatory Parameters, <b>(c)</b> Product Positioning, <b>(d)</b> Budget/Constraint Negotiation, <b>(e)</b> Urgency & Compliance, <b>(f)</b> Closure & Quotation."),
            "<b>What Remains Unsolved for the Dissertation:</b>",
            (1, "Conditioning prompts on <b>(Persona × Call Stage)</b> and scoring <b>Hot / Warm / Cold Lead Propensity</b> at Stage (f) closure before off-chat conversion noise."),
        ],
        font_size=8.7,
    )
    D.add_card(
        s, 0.35, 4.32, 4.08, 2.68,
        title="Frontier 4: 200-Package USP Catalog Narrowing",
        header_bg=CORAL,
        bullets=[
            "<b>Enterprise Product Knowledge Reality:</b>",
            (1, "After Stage (b) mandatory slots, <b>200+ regional packages</b> (e.g., Europe) still match! Narrowing requires micro-qualifiers (<i>seniors, children, breakfast, sightseeing tempo, honeymoon/occasion</i>)."),
            "<b>What Remains Unsolved for the Dissertation:</b>",
            (1, "Sequencing the <b>minimum persona-adapted questions</b> by combining <b>Information Gain</b> with pre-indexed <b>Package USPs</b> to pitch the best package when it fits."),
        ],
        font_size=8.7,
    )
    D.add_card(
        s, 4.62, 4.32, 4.08, 2.68,
        title="Frontier 5: Orthogonal Prompt Ablation (A–E)",
        header_bg=BLUE,
        bullets=[
            "<b>Capstone Finding (RQ2):</b>",
            (1, "Refined RQ2 evaluated `Cluster-Adaptive Few-Shot` as a joint package (routed `Archetype Directive` + archetype FAISS exemplars, <i>F</i> = 9.79, <i>p</i> < .001)."),
            "<b>Future 5-Condition Ablation (Conditions A–E):</b>",
            (1, "Cross `Examples` × `Directive` at <i>N</i> ≥ 60: <b>A</b> (<i>None/Off</i>), <b>B</b> (<i>Static/Off</i>), <b>C</b> (<i>Arch/Off</i>), <b>D</b> (<i>Static/On</i>), <b>E</b> (<i>Arch/On</i>). Diagnostic <i>N</i>=33 shows <b>C beats B</b> (.511 vs .453, <i>p</i>=.028)."),
        ],
        font_size=8.7,
    )
    D.add_card(
        s, 8.90, 4.32, 4.08, 2.68,
        title="Frontier 6: Live Human Agents & RLHC Optimization",
        header_bg=GOLD,
        bullets=[
            "<b>Capstone Finding (RQ4):</b>",
            (1, "While the simulator achieved κ = .933 fidelity, simulated users completed 100% of chats in 5.00–5.27 turns vs. 25.8% human non-completion in Frames."),
            "<b>What Remains Unsolved for the Dissertation:</b>",
            (1, "Training adaptive policies via <b>Offline-to-Online Reinforcement Learning from Human Conversations (RLHC)</b> with live human travelers and agents."),
        ],
        font_size=8.8,
    )

    # =========================================================================
    # SLIDE 45: DOCTORAL DISSERTATION ROADMAP
    # =========================================================================
    s = D.content_slide(
        "Module 8: Conclusive Story & Doctoral Dissertation Roadmap",
        "Future Doctoral Dissertation Roadmap: 'Dialogue Clustering & Methodologies for Human-Like Conversations'",
        "Requirement #5b: Six doctoral research pillars integrating customer archetypes, call stages (a–f), and 200-package USP narrowing",
        notes="Present the concrete 6-pillar plan for the upcoming doctoral dissertation, including Call Stages (a-f) & Lead Propensity (Pillar 3) and 200-Package USP Narrowing (Pillar 4).",
    )
    D.add_table(
        s, 0.35, 1.45, 12.63, 4.48,
        headers=["Doctoral Dissertation Pillar", "Core Research Question for the Dissertation", "Proposed Methodology & Mathematical Framework", "How This Capstone's Findings Directly Aid & Seed This Pillar"],
        rows=[
            [
                "Pillar 1:\nHierarchical Context × Behavior Factor Attribution",
                "How do situational trip parameters (budget stakes, pax/party type, lead window, familiarity) interact with persona to shape clusters?",
                "Formulate a <b>Two-Tier Hierarchical Dirichlet / Product-Quantized Taxonomy (C × K = 24–36 micro-clusters)</b>: Tier 1 partitions macro trip regimes; Tier 2 clusters behavioral negotiation style within each regime.",
                "Directly extends the Two-Tier Pydantic Schema (`Tier1UniversalSlots` + `Tier2EnterpriseSlots`) and 16-field `UserBehaviour` profile (`party_type`, `price_sensitivity`) to enterprise scale (N > 50,000).",
            ],
            [
                "Pillar 2:\nSoft-Mixture Manifold & Bayesian Persona Drift",
                "How can an agent blend styles for boundary users and track mid-chat persona shifts (e.g., Explorer → Rigid) from Turn 1?",
                "Combine a <b>Von Mises–Fisher / VAE Soft Mixture</b> over the `Blocks` manifold with a <b>Hidden Markov / Kalman State-Space Tracker</b> updating P(z_t | u_1..t) after every turn to detect constraint change-points.",
                "Directly reuses the 46-d `Blocks` representation, the 25.2% boundary speaker diagnostics (`step2h/2i`), and the truncation horizon curve (M = 3, 5, 7, 9 in Table D5).",
            ],
            [
                "Pillar 3:\nStage-Gated Call Flow (a–f) & Lead Propensity Scoring",
                "How do agent strategies adapt across the 6 enterprise call stages (a–f) and predict Hot, Warm, or Cold lead propensity at closure?",
                "Build a <b>3 (Archetypes) × 6 (Call Stages: a. Opening → b. Mandatory Slots → c. Positioning → d. Negotiation → e. Compliance/Urgency → f. Closure) = 18-Cell FAISS Matrix</b> + ordinal <b>Hot/Warm/Cold Lead Propensity Classifier</b>.",
                "Combines the RQ2/RQ4 archetype policies with RQ3 compliance checks at Stage (e) and extends the RQ1 outcome features (`Fields 14–16`) into Stage (f) lead scoring prior to off-chat conversion noise.",
            ],
            [
                "Pillar 4:\n200-Package USP Graph & Optimal Question Sequencing",
                "When mandatory slots match 200+ packages, what is the optimal persona-adapted question sequence to narrow to 1 package and pitch its USP?",
                "Formulate catalog narrowing as an <b>Archetype-Conditioned POMDP / Maximum Information-Gain Tree</b> over a 200-package USP Knowledge Graph (<i>seniors, children, breakfast, sightseeing, occasion</i>), selecting questions that maximize <b>Entropy Reduction × Persona Weight × USP Fit</b>.",
                "Extends the RQ4 `Verified Informed Slot Ledger` and 4-option trade-off policy (`step4_rq4_simulation.py`) to large-scale enterprise product catalogs without inflating turn counts.",
            ],
            [
                "Pillar 5:\nOrthogonal Prompting Ablation (A–E) & Funnel Isolation",
                "How do explicit routed directives vs. sub-index exemplars orthogonally drive style, and how does Quotation Agreement decouple from conversion?",
                "Run a powered (<i>N</i> ≥ 60) <b>5-Condition Ablation (A: None/Off, B: Static/Off, C: Arch/Off, D: Static/On, E: Arch/On)</b> + 30-dim pragmatic codebook + <b>Two-Stage Funnel Model</b> (Stage 1 In-Chat Quote vs. Stage 2 Off-Chat Booking).",
                "Directly extends the RQ2 style/pacing metrics (`step2_rq2_refined.py`, where diagnostic C vs. B = .511 vs. .453, <i>p</i> = .028) and the separation of in-chat turn economy from exogenous conversion factors.",
            ],
            [
                "Pillar 6:\nConstrained Neuro-Symbolic RL for Live Human Agents",
                "Can human-likeness, stage progression, and turn economy be jointly optimized under zero-violation symbolic guardrails with live humans?",
                "Formulate a <b>Constrained Markov Decision Process (CMDP)</b> where the declarative `RuleEngine` acts as a hard safety shield while Offline RL (CQL / DPO) optimizes turn economy and rapport in live Agent-Assist deployment.",
                "Uses the RQ3 `RuleEngine` (0.0% leakage, 98.6% adherence) as the deterministic safety shield and the RQ4 multi-turn simulator as the pre-deployment training gym.",
            ],
        ],
        col_widths=[2.20, 2.70, 4.15, 3.58],
        font_size=7.6,
        align_left_cols=(0, 1, 2, 3),
        highlight_rows=(0, 1, 2, 3, 4, 5),
    )
    D.add_callout(
        s, 0.35, 6.00, 12.63, 1.05,
        "<b>Why This Capstone Is the Ideal Foundation for the Doctoral Dissertation:</b>\n"
        "This master's study established the <i>foundational 1D persona architecture</i>—proving that behavioral-semantic clustering (`Blocks`), slot-masked exemplar retrieval, and declarative symbolic guardrails succeed with <i>p</i> < .001 across RQ1–RQ4. The doctoral dissertation elevates this into a <b>3D Neuro-Symbolic Enterprise Framework (Customer Archetype × Call Stage a–f × 200-Package USP Question Sequencing)</b>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=10.8,
    )

    # =========================================================================
    # SLIDE 42: CONCLUDING SUMMARY & DEFENSE Q&A CLOSING
    # =========================================================================
    s = D.content_slide(
        "Module 8: Conclusive Story & Doctoral Dissertation Roadmap",
        "Concluding Summary & Defense Open Floor",
        "A complete, reproducible, empirically validated blueprint for neuro-symbolic conversational personalization",
        notes="Final summary slide to leave on screen during the committee's open questioning.",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 4.30,
        title="Key Scientific & Engineering Takeaways",
        header_bg=NAVY,
        bullets=[
            "<b>1. RQ1 (Discovery & Routing):</b> Truncating to opening user behavior (`M = 9` messages) and combining Gemini embeddings with 16 validated LLM behavioral ratings (`Blocks`) yields 3 stable archetypes (<b>ARI = .89 / .87</b>) and raises held-out prefix routing to <b>70.1% (M=5) and 97.3% (M=9, κ = .958)</b>.",
            "<b>2. RQ2 (Style & Pacing):</b> Contrasting Primary (<i>p</i> = .211) vs. Refined (<b>p < .001, ηp² = .234</b>) archetypes demonstrates that in-context style convergence (+31.8% over static, <i>d<sub>z</sub></i> = 0.74) and pacing calibration (<b>3.87w error</b>) succeed once upstream routing is coherent.",
            "<b>3. RQ3 (Safety & Guardrails):</b> Declarative rule verification eliminates the <b>35.9% entity leakage</b> of unguarded few-shot prompting down to <b>0.0% (Interaction F = 34.82, p < .001)</b> while raising policy violation enforcement sensitivity from <b>5.6% to 98.6% (F = 498.78, p < .001)</b> and Slot F1 to <b>.952</b> (Dual-judge <b>κ = .917</b>).",
            "<b>4. RQ4 (Turn Economy):</b> Archetype-adaptive policies + Verified Informed Slot Ledger compress multi-turn sessions by <b>29.5% to 42.7%</b> (<i>F</i> = 664.43, Interaction <i>F</i> = 10.89, <i>p</i> < .001) and eliminate redundant slot questions (<b>RER .109 → .000</b>; Persona <b>κ = .933</b>).",
        ],
        font_size=10,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 4.30,
        title="Complete Reproducibility & Artifact Inventory",
        header_bg=TEAL,
        bullets=[
            f"<b>GitHub Repository:</b> {REPO}",
            "<b>Final Report Deliverables:</b>",
            (1, "`final/QM_640_Final_Report_Sandeep_Surnella.docx` & `.pdf` (30 Core Report pages; 52 total pages; 104 verified cross-references; 26 APA 7 references)."),
            "<b>Empirical Codebase & Cached Data:</b>",
            (1, "`src/final_pipeline/` (Steps 0–2i data prep/clustering, `common_llm.py`, `routing.py`, `metrics.py`, `step2_rq2_refined.py`, `step3_rq3_experiment.py`, `step4_rq4_simulation.py`, `step5_figures_and_eda.py`)"),
            (1, "`notebooks/01_..` to `05_..` (5 executed Jupyter notebooks)"),
            (1, "`data/interim/` & `data/final/` (100% cached JSONL responses — full offline replication in < 4 minutes with seed = 42)."),
        ],
        font_size=10,
    )
    D.add_callout(
        s, 0.35, 5.95, 12.63, 1.10,
        "<b>Thank You — Open Floor for Defense Committee Questions</b>\n"
        "<i>Surnella Sandeep  |  Department of Data Analytics, Walsh College  |  QM640: Data Analytics Capstone  |  Mentor: Mr. Smitraj Raut</i>",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=13,
    )

    # =========================================================================
    # SLIDE 47: PICTORIAL SYNTHESIS OF SLIDES 44 & 45 (CAPSTONE vs. DISSERTATION)
    # =========================================================================
    s = D.content_slide(
        "Module 8: Conclusive Story & Doctoral Dissertation Roadmap",
        "Pictorial Synthesis: From Capstone (RQ1–RQ4) to Doctoral Human-Like Conversational AI",
        "Visualizing Addressed Capstone Parameters (Teal/Navy) vs. Doctoral Exploration Blocks (Amber/Coral) & Labeled Output Flows",
        notes=(
            "This pictorial blueprint synthesizes Slides 44 (Six Scientific Frontiers) and 45 (Doctoral Dissertation Roadmap) "
            "into a single end-to-end methodological architecture. Teal/Navy blocks show what is empirically completed in "
            "this Master's Capstone (RQ1-RQ4), Amber/Gold blocks show the 6 Doctoral Dissertation extensions and their "
            "probable parameters, and labeled connector arrows show how each module's output feeds the next toward the "
            "common research goal of a reproducible human-like enterprise chatbot."
        ),
    )

    # Color shades for Capstone vs. Doctoral vs. Goal
    CAP_BG = RGBColor(224, 242, 241)       # Soft Teal/Cyan tint for Capstone (RQ1-RQ4)
    CAP_HDR = TEAL                         # Deep Teal header for Capstone blocks
    CAP_BORDER = NAVY                      # Solid Navy border

    DOC_BG = RGBColor(255, 246, 224)       # Warm Amber/Gold tint for Doctoral Dissertation
    DOC_HDR = RGBColor(184, 51, 42)        # Coral/Crimson header for Doctoral blocks
    DOC_BORDER = GOLD                      # Warm Gold border

    GOAL_BG = RGBColor(225, 245, 232)      # Soft Emerald tint for Common Goal Hub
    GOAL_HDR = GREEN                       # Deep Emerald header
    GOAL_BORDER = GREEN

    # 1. Top Legend Bar (y = 1.43, h = 0.31)
    def _add_legend_pill(left, width, bg_col, hdr_col, bdr_col, tag_txt, desc_txt):
        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(1.43), Inches(width), Inches(0.30))
        box.adjustments[0] = 0.15
        box.fill.solid()
        box.fill.fore_color.rgb = bg_col
        box.line.color.rgb = bdr_col
        box.line.width = Pt(1.25)
        badge = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.04), Inches(1.46), Inches(1.55), Inches(0.24))
        badge.adjustments[0] = 0.2
        badge.fill.solid()
        badge.fill.fore_color.rgb = hdr_col
        badge.line.fill.background()
        p_b = badge.text_frame.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_b, tag_txt, font_size=7.8, color=WHITE, bold=True)
        tb = s.shapes.add_textbox(Inches(left + 1.63), Inches(1.45), Inches(width - 1.68), Inches(0.26))
        tb.text_frame.word_wrap = True
        tb.text_frame.margin_left = tb.text_frame.margin_top = Inches(0)
        p_t = tb.text_frame.paragraphs[0]
        _add_formatted_runs(p_t, desc_txt, font_size=8.0, color=DARK, bold=True)

    _add_legend_pill(
        0.25, 4.15, CAP_BG, CAP_HDR, CAP_BORDER,
        "CAPSTONE (RQ1–RQ4)",
        "Currently Addressed Modules & Validated Parameters (p < .001)",
    )
    _add_legend_pill(
        4.48, 4.55, DOC_BG, DOC_HDR, DOC_BORDER,
        "DOCTORAL (PILLARS 1–6)",
        "Future Dissertation Blocks & Probable Parameters to Explore",
    )
    _add_legend_pill(
        9.11, 3.97, GOAL_BG, GOAL_HDR, GOAL_BORDER,
        "CORE RESEARCH GOAL",
        "Reproducible Methodology for Human-Like Chatbot AI",
    )

    # Helper to draw an analysis block
    def _add_analysis_block(left, top, width, height, title, lines, is_capstone=True):
        bg = CAP_BG if is_capstone else DOC_BG
        hdr_c = CAP_HDR if is_capstone else DOC_HDR
        bdr_c = CAP_BORDER if is_capstone else DOC_BORDER

        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.adjustments[0] = 0.03
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = bdr_c
        card.line.width = Pt(1.4)

        hdr_h = 0.27
        hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(hdr_h))
        hdr.adjustments[0] = 0.03
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = hdr_c
        hdr.line.fill.background()
        tf_h = hdr.text_frame
        tf_h.word_wrap = True
        tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_h.margin_left = Inches(0.08)
        p_h = tf_h.paragraphs[0]
        _add_formatted_runs(p_h, title, font_size=8.6, color=WHITE, bold=True)

        tb = s.shapes.add_textbox(
            Inches(left + 0.06),
            Inches(top + hdr_h + 0.02),
            Inches(width - 0.12),
            Inches(height - hdr_h - 0.04),
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.02)
        tf.margin_top = tf.margin_bottom = Inches(0.01)
        for idx, ln in enumerate(lines):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_after = Pt(1.5)
            _add_formatted_runs(p, ln, font_size=7.4, color=DARK)

    # Helper to draw a labeled horizontal connector arrow between columns
    def _add_labeled_arrow(left, top, width, height, label_top, label_bottom, is_capstone=True):
        arr_c = CAP_HDR if is_capstone else DOC_HDR
        bdr_c = NAVY if is_capstone else GOLD
        arr = s.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW,
            Inches(left + 0.03),
            Inches(top + height * 0.34),
            Inches(width - 0.06),
            Inches(0.24),
        )
        arr.fill.solid()
        arr.fill.fore_color.rgb = arr_c
        arr.line.color.rgb = bdr_c
        arr.line.width = Pt(0.75)

        # Callout tag above arrow
        tb1 = s.shapes.add_textbox(Inches(left - 0.02), Inches(top + 0.02), Inches(width + 0.04), Inches(0.32))
        tf1 = tb1.text_frame
        tf1.word_wrap = True
        tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = Inches(0)
        p1 = tf1.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p1, label_top, font_size=6.9, color=NAVY if is_capstone else DOC_HDR, bold=True)

        # Parameter tag below arrow
        tb2 = s.shapes.add_textbox(Inches(left - 0.02), Inches(top + height * 0.34 + 0.25), Inches(width + 0.04), Inches(0.45))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = Inches(0)
        p2 = tf2.paragraphs[0]
        p2.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p2, label_bottom, font_size=6.6, color=DARK)

    # Helper to draw small vertical flow arrow between stacked blocks inside a column
    def _add_vert_connector(center_x, top_y, label_txt):
        arr = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(center_x - 0.11), Inches(top_y), Inches(0.22), Inches(0.14))
        arr.fill.solid()
        arr.fill.fore_color.rgb = GOLD
        arr.line.color.rgb = DOC_HDR
        arr.line.width = Pt(0.6)
        tb = s.shapes.add_textbox(Inches(center_x + 0.13), Inches(top_y - 0.02), Inches(1.55), Inches(0.16))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = Inches(0)
        p = tf.paragraphs[0]
        _add_formatted_runs(p, label_txt, font_size=6.5, color=DOC_HDR, bold=True)

    # Coordinates for 3 rows
    R1_Y, R2_Y, R3_Y = 1.80, 3.44, 5.08
    ROW_H = 1.50

    # =========================================================================
    # COLUMN 1: USER ARCHETYPE & HIERARCHICAL / MANIFOLD CLUSTERING (x=0.25, w=2.65)
    # =========================================================================
    C1_X, C1_W = 0.25, 2.65
    _add_analysis_block(
        C1_X, R1_Y, C1_W, ROW_H,
        "[CAPSTONE RQ1] User Archetypes Analysis",
        [
            "• <b>Method:</b> Opening-turn (`M=9`) `K-Means (k=3)` + `L2 LogReg` Router on `46-d Blocks`.",
            "• <b>Addressed Params (46-d):</b> `PCA-20` Gemini semantic prefix + `26` behavioral cols (<i>destination_flexibility, decisiveness, price_sensitivity, exploration_breadth, goals, tone</i>).",
            "• <b>Validated Result:</b> `ARI = .89/.87`, `97.3%` prefix routing (`κ = .958`, `p < .001`).",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C1_X + 0.85, R1_Y + ROW_H, "Expands 1D k=3 → 2D Hierarchy")

    _add_analysis_block(
        C1_X, R2_Y, C1_W, ROW_H,
        "[DOCTORAL P1] Hierarchical Clustering (C × K)",
        [
            "• <b>Method:</b> Two-Tier Context × Behavior (`24–36` micro-personas) + Domain Transfer.",
            "• <b>Probable Context Params (Tier 1):</b> `party_type` (solo / couple / family / group), `budget_stakes` (economy / luxury), `lead_window`, `trip_familiarity`.",
            "• <b>Probable Behavioral Params (Tier 2):</b> Conditional pacing & decision latency within regime `C`.",
        ],
        is_capstone=False,
    )
    _add_vert_connector(C1_X + 0.85, R2_Y + ROW_H, "Replaces Hard k-Means w/ Soft Drift")

    _add_analysis_block(
        C1_X, R3_Y, C1_W, ROW_H,
        "[DOCTORAL P2] Soft-Mixture & Bayesian Drift",
        [
            "• <b>Method:</b> Variational / vMF Manifold + Turn-by-Turn Posterior Update.",
            "• <b>Probable Drift Params:</b> Continuous blend weights (`w_1..w_K`) for `25.2%` boundary speakers (`s < .05`) + mid-call shift `P(z_t | u_1..t)` (e.g., <i>Exploratory → Budget</i> after quote).",
        ],
        is_capstone=False,
    )

    # =========================================================================
    # ARROWS 1 → 2 (x=2.91, w=0.77)
    # =========================================================================
    A1_X, A1_W = 2.91, 0.77
    _add_labeled_arrow(
        A1_X, R1_Y + 0.15, A1_W, ROW_H - 0.2,
        "RQ1 Output → RQ2",
        "3 Personas + Prefix Router (κ=.535→.958)",
        is_capstone=True,
    )
    _add_labeled_arrow(
        A1_X, R2_Y + 0.15, A1_W, ROW_H - 0.2,
        "Pillar 1 Output",
        "C×K Regime State + Party/Stakes Vector",
        is_capstone=False,
    )
    _add_labeled_arrow(
        A1_X, R3_Y + 0.15, A1_W, ROW_H - 0.2,
        "Pillar 2 Output",
        "Live Persona Posterior P(z_t | u_1..t)",
        is_capstone=False,
    )

    # =========================================================================
    # COLUMN 2: AGENT CLASSIFICATION, STYLE & 200-PACKAGE NARROWING (x=3.70, w=2.85)
    # =========================================================================
    C2_X, C2_W = 3.70, 2.85
    _add_analysis_block(
        C2_X, R1_Y, C2_W, ROW_H,
        "[DOCTORAL P3] Agent Call-Stage Classification (a–f)",
        [
            "• <b>Method:</b> Supervised / HMM Stage Classifier (`3 × 6` Persona × Stage Policy).",
            "• <b>Probable Call-Stage Params:</b> <b>(a)</b> Opening Call → <b>(b)</b> Mandatory Params → <b>(c)</b> Product Positioning → <b>(d)</b> Budget & Constraint Negotiation → <b>(e)</b> Sales Urgency & Compliance → <b>(f)</b> Closure & `Hot/Warm/Cold` Lead.",
        ],
        is_capstone=False,
    )
    _add_vert_connector(C2_X + 0.90, R1_Y + ROW_H, "Stage Gate Modulates Style & Pacing")

    _add_analysis_block(
        C2_X, R2_Y, C2_W, ROW_H,
        "[CAPSTONE RQ2] Partitioned FAISS Style & Pacing",
        [
            "• <b>Method:</b> Archetype-Partitioned FAISS (`k=3`) + `[SLOT]` Masking + Directive.",
            "• <b>Addressed Params:</b> Target word norms (`12.9w` / `18.6w` / `14.8w`), tone alignment, syntax templates, pacing calibration.",
            "• <b>Validated Result:</b> Style `.597` (`+31.8%`, `p < .001`) & `3.87w` length error.",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C2_X + 0.90, R2_Y + ROW_H, "Persona + Stage Drives Catalog Narrowing")

    _add_analysis_block(
        C2_X, R3_Y, C2_W, ROW_H,
        "[DOCTORAL P4] 200-Package Knowledge & USP Tree",
        [
            "• <b>Method:</b> Max Info-Gain Question Sequencer (`200 → 1–2` Packages).",
            "• <b>Probable Narrowing Params:</b> `Senior-citizen presence`, `Child sensitivity`, `Breakfast inclusiveness`, `Sightseeing tempo`, `Occasion (Honeymoon)`.",
            "• <b>USP Pitching:</b> Matches customer signals to <b>pre-indexed Package USPs</b>.",
        ],
        is_capstone=False,
    )

    # =========================================================================
    # ARROWS 2 → 3 (x=6.57, w=0.76)
    # =========================================================================
    A2_X, A2_W = 6.57, 0.76
    _add_labeled_arrow(
        A2_X, R1_Y + 0.15, A2_W, ROW_H - 0.2,
        "Pillar 3 Output",
        "Stage (a–f) Gate + Compliance Trigger",
        is_capstone=False,
    )
    _add_labeled_arrow(
        A2_X, R2_Y + 0.15, A2_W, ROW_H - 0.2,
        "RQ2 Output → RQ3/4",
        "Style (.597) + 3.87w Pacing + [SLOT] Mask",
        is_capstone=True,
    )
    _add_labeled_arrow(
        A2_X, R3_Y + 0.15, A2_W, ROW_H - 0.2,
        "Pillar 4 Output",
        "Optimal Q Sequence + Top 1–2 USP Fit",
        is_capstone=False,
    )

    # =========================================================================
    # COLUMN 3: SYMBOLIC GUARDRAILS, SLOT LEDGER & RL OPTIMIZATION (x=7.35, w=2.73)
    # =========================================================================
    C3_X, C3_W = 7.35, 2.73
    _add_analysis_block(
        C3_X, R1_Y, C3_W, ROW_H,
        "[CAPSTONE RQ3] Symbolic Policy & Entity Guard",
        [
            "• <b>Method:</b> Declarative `YAML` Rule Engine + Post-Gen Entity Sanitizer.",
            "• <b>Addressed Params:</b> `visa_lead ≥ 15d`, `passport ≥ 6m`, `FIT_pax ≤ 4`, `discount ≤ 15%`, `budget ≥ $500`, zero entity leakage.",
            "• <b>Validated Result:</b> `0.0%` leakage (`F = 34.82`) & `98.6%` rule enforcement (`κ = .917`).",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C3_X + 0.85, R1_Y + ROW_H, "Verified Slots Feed Turn Ledger")

    _add_analysis_block(
        C3_X, R2_Y, C3_W, ROW_H,
        "[CAPSTONE RQ4] Verified Slot Ledger & Economy",
        [
            "• <b>Method:</b> Explicit Turn-State Memory + Trade-Off Package Framing.",
            "• <b>Addressed Params:</b> `Informed` vs. `Missing` mandatory slots (`origin, dest, dates, duration, budget`) + `Option A/B/D` trade-off pitch.",
            "• <b>Validated Result:</b> `−29.5%..−42.7%` turns (`F = 664.43`), `RER .109 → .000`.",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C3_X + 0.85, R2_Y + ROW_H, "Decomposes Gains & Trains Live RLHC")

    _add_analysis_block(
        C3_X, R3_Y, C3_W, ROW_H,
        "[DOCTORAL P5–6] Turn Intelligence & RLHC (DTQ)",
        [
            "• <b>Method:</b> Cluster Turn Tablebase (`DTQ` / `CMDP`) + `5-Arm (A–E)` Ablation.",
            "• <b>Probable Params:</b> Next-Best-Move `A_t*` minimizing Distance-to-Quotation (`DTQ`), `Directive × Exemplar × Ledger` weights, `Stage 1/2` Funnel + `Hot/Warm/Cold` Lead.",
        ],
        is_capstone=False,
    )

    # =========================================================================
    # ARROWS 3 → 4 CONVERGING INTO GOAL HUB (x=10.10, w=0.68)
    # =========================================================================
    A3_X, A3_W = 10.10, 0.68
    _add_labeled_arrow(
        A3_X, R1_Y + 0.15, A3_W, ROW_H - 0.2,
        "RQ3 Output",
        "0.0% Leakage & 98.6% Guard",
        is_capstone=True,
    )
    _add_labeled_arrow(
        A3_X, R2_Y + 0.15, A3_W, ROW_H - 0.2,
        "RQ4 Output",
        "−30..43% Turns & .000 RER",
        is_capstone=True,
    )
    _add_labeled_arrow(
        A3_X, R3_Y + 0.15, A3_W, ROW_H - 0.2,
        "P5–6 Output",
        "CMDP Policy + Lead Score",
        is_capstone=False,
    )

    # =========================================================================
    # COLUMN 4: COMMON RESEARCH GOAL CONVERGENCE HUB (x=10.80, w=2.28, y=1.80..6.58)
    # =========================================================================
    G_X, G_Y, G_W, G_H = 10.80, 1.80, 2.28, 4.78
    goal_card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(G_X), Inches(G_Y), Inches(G_W), Inches(G_H))
    goal_card.adjustments[0] = 0.03
    goal_card.fill.solid()
    goal_card.fill.fore_color.rgb = GOAL_BG
    goal_card.line.color.rgb = GOAL_BORDER
    goal_card.line.width = Pt(2.0)

    goal_hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(G_X), Inches(G_Y), Inches(G_W), Inches(0.54))
    goal_hdr.adjustments[0] = 0.03
    goal_hdr.fill.solid()
    goal_hdr.fill.fore_color.rgb = GOAL_HDR
    goal_hdr.line.fill.background()
    tf_gh = goal_hdr.text_frame
    tf_gh.word_wrap = True
    tf_gh.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_gh = tf_gh.paragraphs[0]
    p_gh.alignment = PP_ALIGN.CENTER
    _add_formatted_runs(
        p_gh,
        "CORE DISSERTATION GOAL:\nHuman-Like Conversational AI",
        font_size=9.2,
        color=WHITE,
        bold=True,
    )

    goal_items = [
        ("1. Adaptive Persona Empathy", "Tracks `C × K` archetypes & live behavioral drift (`RQ1 + P1–P2`)."),
        ("2. Enterprise Call-Stage Flow", "Executes stages `a → f` with calibrated style & word pacing (`RQ2 + P3`)."),
        ("3. Intelligent USP Narrowing", "Narrows `200+` packages via optimal question trees & USPs (`P4`)."),
        ("4. Zero-Leakage Governance", "Enforces `100%` grounded entities & business compliance (`RQ3`)."),
        ("5. Frictionless Closure & Lead", "Zero redundant questions (`RQ4`) + `Hot/Warm/Cold` lead scoring (`P5–P6`)."),
    ]
    cur_gy = G_Y + 0.62
    for g_title, g_desc in goal_items:
        sub = s.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(G_X + 0.08),
            Inches(cur_gy),
            Inches(G_W - 0.16),
            Inches(0.76),
        )
        sub.adjustments[0] = 0.06
        sub.fill.solid()
        sub.fill.fore_color.rgb = WHITE
        sub.line.color.rgb = GOAL_BORDER
        sub.line.width = Pt(1.0)
        tf_s = sub.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = Inches(0.06)
        tf_s.margin_top = tf_s.margin_bottom = Inches(0.03)
        p_st = tf_s.paragraphs[0]
        _add_formatted_runs(p_st, g_title, font_size=7.8, color=GOAL_HDR, bold=True)
        p_sd = tf_s.add_paragraph()
        p_sd.space_before = Pt(1.5)
        _add_formatted_runs(p_sd, g_desc, font_size=7.1, color=DARK)
        cur_gy += 0.81

    # Bottom Thesis Takeaway Bar (y = 6.64, h = 0.52)
    D.add_callout(
        s, 0.25, 6.64, 12.83, 0.52,
        "<b>Core Methodological Thesis:</b> Creating a truly <b>human-like enterprise conversational AI</b> is not a single-prompt trick—it requires a <b>reproducible, modular neuro-symbolic methodology</b> where <b>Capstone Blocks (Teal: RQ1–RQ4)</b> provide validated persona routing, style conditioning, symbolic safety, and slot memory, and <b>Doctoral Blocks (Amber: Pillars 1–6)</b> add hierarchical context, Bayesian drift, stage-gated sales progression (`a–f`), `200 → 1` USP catalog narrowing, and Chess-style Turn Intelligence (`DTQ`).",
        bg_color=CALLOUT_BG, border_color=NAVY, font_size=8.3,
    )

    # =========================================================================
    # SLIDE 48: DOCTORAL DEEP-DIVE — CHESS-STYLE TURN INTELLIGENCE & NEXT-BEST-MOVE TABLEBASE
    # =========================================================================
    s = D.content_slide(
        "Module 8: Conclusive Story & Doctoral Dissertation Roadmap",
        "Doctoral Deep-Dive: 'Chess Engine' Turn Intelligence & Next-Best-Move Tablebase (DTQ)",
        "Upgrading from Backward-Looking Cosine Top-3 (RQ2) to a Cluster-Conditioned 'Distance-to-Quotation' (DTQ) Next-Move Predictor",
        notes=(
            "This slide answers how the consultative travel chatbot maps to a Chess Engine where Quotation Agreement "
            "(1-3 packages + Hot/Warm/Cold lead) is Checkmate, why cosine top-3 retrieval alone is insufficient for "
            "predicting the optimal next move, and how a dedicated Turn Intelligence module inside each Hierarchical "
            "Cluster (C x K) predicts the Next Best Agent Move A_t* to minimize Distance-to-Quotation (DTQ)."
        ),
    )

    # Left Top: Chess vs. Travel Consultation (POMDP) Analogy Table
    D.add_table(
        s, 0.25, 1.46, 5.55, 3.12,
        headers=["Chess Engine Concept", "Travel Chatbot ('Quotation Checkmate') Equivalent", "Capstone vs. Doctoral Status"],
        rows=[
            [
                "Checkmate\n(Terminal Goal State)",
                "Customer agrees all constraints are met & requests formal quotation (1–3 packages) + Hot/Warm/Cold lead.",
                "Capstone RQ4 (`[ACCEPT_BOOKING]`) → Doctoral Stage `f` Quote + Lead Score",
            ],
            [
                "Board State (S_t)\nat Move t",
                "Discrete Symbolic State: `(C×K Cluster, Stage a–f, 9-Slot Bitmask, |P_t| Packages Left, Active Conflict)`.",
                "Capstone 5-Slot Ledger → Doctoral Full Symbolic State Hash",
            ],
            [
                "Opponent A vs. B\n(Game Type)",
                "Customer (`C×K` Persona) vs. Agent (`A_t` Move) in a Cooperative Hidden-Info Game (`POMDP`).",
                "Customer preferences start hidden; moves must gather info + narrow 200 pkgs",
            ],
            [
                "Chess Referee\n(Illegal Move Filter)",
                "Declarative `YAML` Rule Engine (`RQ3`) + Verified Slot Ledger (`RQ4`) block rule violations & repeat asks.",
                "Completed in Capstone RQ3 (`0.0%` leakage, `98.6%` guard) & RQ4 (`.000` RER)",
            ],
            [
                "Endgame Tablebase\n(Distance-to-Mate)",
                "Turn-Economy Tablebase (`Turn-Q DB`): scores every `(S_t, A_t)` by Distance-to-Quotation (`DTQ` turns left).",
                "New Doctoral Turn Intelligence Module inside `C × K` Clusters!",
            ],
        ],
        col_widths=[1.35, 2.55, 1.65],
        font_size=7.6,
        header_size=8.3,
        align_left_cols=(0, 1, 2),
        highlight_rows=(0, 4),
    )

    # Left Bottom: Why Cosine Top-3 Needs Upgrading to Turn Tablebase
    D.add_card(
        s, 0.25, 4.66, 5.55, 1.90,
        title="Why RQ2 Cosine Top-3 Must Evolve into a Turn-Economy Tablebase",
        header_bg=CORAL,
        bg_color=DOC_BG,
        border_color=GOLD,
        bullets=[
            "<b>1. Gap in Pure Cosine Retrieval (`RQ2`):</b> Retrieving top-3 turns by `cos(q_t, e_j)` looks <b>backward at context similarity</b> (great for <i>HOW to phrase</i>), but is blind to <b>forward turn economy</b>—treating a past wizard move that took 9 more turns the same as one that closed in 1 turn!",
            "<b>2. The Turn-Q Tablebase Upgrade:</b> Indexes every historical/simulated turn `(S_t, A_j)` with its empirical <b>Distance-to-Quotation `DTQ = E[T_quote − t | S_t, A_j]`</b>, package reduction `Δ|P_t|`, and win rate `Q*(S_t, A_j)`.",
            "<b>3. Advantage-Weighted Retrieval Formula:</b>\n"
            "    `Score(e_j | S_t, q_t) = α·cos(q_t, e_j) + β·Q*(S_t, A_j) − γ·DTQ(S_t, A_j)`",
        ],
        font_size=7.7,
        title_size=9.2,
        bullet_spacing=2,
    )

    # Right Side: 4-Stage Pictorial Diagram of the Turn Intelligence Engine inside C x K Clusters
    R_X, R_W = 5.92, 7.16
    hdr_panel = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(R_X), Inches(1.46), Inches(R_W), Inches(5.10))
    hdr_panel.adjustments[0] = 0.02
    hdr_panel.fill.solid()
    hdr_panel.fill.fore_color.rgb = RGBColor(244, 247, 251)
    hdr_panel.line.color.rgb = NAVY
    hdr_panel.line.width = Pt(1.5)

    p_banner = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(R_X), Inches(1.46), Inches(R_W), Inches(0.34))
    p_banner.adjustments[0] = 0.02
    p_banner.fill.solid()
    p_banner.fill.fore_color.rgb = NAVY
    p_banner.line.fill.background()
    p_bt = p_banner.text_frame.paragraphs[0]
    p_bt.alignment = PP_ALIGN.CENTER
    _add_formatted_runs(
        p_bt,
        "PICTORIAL ARCHITECTURE: DEDICATED 'TURN INTELLIGENCE ENGINE' INSIDE HIERARCHICAL CLUSTERS (C × K)",
        font_size=8.6,
        color=WHITE,
        bold=True,
    )

    def _add_ti_step(top_y, h_box, badge_txt, title_txt, desc_lines, bg_c, hdr_c, bdr_c):
        bx = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(R_X + 0.12), Inches(top_y), Inches(R_W - 0.24), Inches(h_box))
        bx.adjustments[0] = 0.04
        bx.fill.solid()
        bx.fill.fore_color.rgb = bg_c
        bx.line.color.rgb = bdr_c
        bx.line.width = Pt(1.3)

        bd = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(R_X + 0.20), Inches(top_y + 0.07), Inches(1.55), Inches(h_box - 0.14))
        bd.adjustments[0] = 0.08
        bd.fill.solid()
        bd.fill.fore_color.rgb = hdr_c
        bd.line.fill.background()
        tf_bd = bd.text_frame
        tf_bd.word_wrap = True
        tf_bd.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_bd = tf_bd.paragraphs[0]
        p_bd.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_bd, badge_txt, font_size=7.8, color=WHITE, bold=True)

        tb = s.shapes.add_textbox(Inches(R_X + 1.82), Inches(top_y + 0.04), Inches(R_W - 2.02), Inches(h_box - 0.08))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = Inches(0.01)
        p0 = tf.paragraphs[0]
        p0.space_after = Pt(1.5)
        _add_formatted_runs(p0, title_txt, font_size=8.4, color=hdr_c, bold=True)
        for ln in desc_lines:
            p = tf.add_paragraph()
            p.space_after = Pt(1.0)
            _add_formatted_runs(p, ln, font_size=7.3, color=DARK)

    # Step 1
    _add_ti_step(
        1.88, 0.96,
        "STEP 1: BOARD STATE\nHASH (S_t)",
        "Compress Live Conversation into Canonical Symbolic State Inside Cluster (C × K)",
        [
            "• <b>Active State Vector `S_t`:</b> `Cluster = (Family, Economy, Rigid Seeker)` | `Stage = d (Negotiation)` | `Known Slots = 7/9` | `Missing = {Senior, Breakfast}` | `Candidate Packages |P_t| = 38` | `Conflict = 5★ Over Budget`.",
        ],
        CAP_BG, CAP_HDR, CAP_BORDER,
    )
    _add_vert_connector(R_X + 2.8, 2.86, "State S_t Queries Cluster Turn-Q DB")

    # Step 2
    _add_ti_step(
        3.02, 1.24,
        "STEP 2: TURN-Q DB &\n2-PLY LOOKAHEAD\n(DTQ ENGINE)",
        "Evaluate Candidate Agent Moves A_t Within Cluster (C × K) to Minimize Distance-to-Quotation",
        [
            "• <b>Move A1 (Generic Sightseeing Ask):</b> `|P_t|: 38 → 31` | `Win Q* = .42` | <b>`DTQ = 5.4 turns left` (Blunder ✗)</b>",
            "• <b>Move A2 (Ask Senior Only):</b> `|P_t|: 38 → 14` | `Win Q* = .68` | <b>`DTQ = 3.1 turns left` (Sub-optimal)</b>",
            "• <b>Move A3* (Optimal Next Move):</b> `[Bundle Ask Senior+Breakfast + Pitch 4★ Exact USP vs. 5★ +3d Shift]` → `|P_t|: 38 → 2` | `Win Q* = .94` | <b>`DTQ = 1.0 turn to Quote!` (Best Move ✓)</b>",
        ],
        DOC_BG, DOC_HDR, DOC_BORDER,
    )
    _add_vert_connector(R_X + 2.8, 4.28, "Pass Winning Move A3* + Top-3 Winning Exemplars")

    # Step 3
    _add_ti_step(
        4.44, 1.02,
        "STEP 3: DECOUPLED\nMOVE vs. STYLE +\nRULE REFEREE",
        "Combine WHAT to Play (Turn Intelligence A_t*) + HOW to Say It (FAISS) + Legal Referee (RQ3/RQ4)",
        [
            "• <b>WHAT Move to Play (`Doctoral Turn Intelligence`):</b> Execute discrete move `A3*` (`Senior+Breakfast + Option A/D USP Pitch`).",
            "• <b>HOW to Phrase It (`Capstone RQ2 FAISS`):</b> Top-3 `[SLOT]`-masked exemplars from Cluster `(C,K)` & Move `A3*` (`14.8w` norm).",
            "• <b>Referee Check (`Capstone RQ3 + RQ4`):</b> Verifies `0.0%` entity leakage, `5 YAML` rules, and `0.0%` redundant slot asks.",
        ],
        CAP_BG, NAVY, CAP_BORDER,
    )
    _add_vert_connector(R_X + 2.8, 5.48, "Reaches Terminal Goal in Minimum Turns")

    # Step 4
    _add_ti_step(
        5.64, 0.84,
        "STEP 4: QUOTATION\nCHECKMATE (S_goal)",
        "Terminal Goal Reached: 1–3 Shortlisted Packages Agreed + Lead Propensity Scored in Minimum Turns",
        [
            "• Customer confirms adjusted constraints & requests formal quotation for top 2 matched packages → <b>Stage `f` Closure creates `Hot / Warm / Cold` Lead in optimal turn economy!</b>",
        ],
        GOAL_BG, GOAL_HDR, GOAL_BORDER,
    )

    # Bottom Takeaway Callout
    D.add_callout(
        s, 0.25, 6.62, 12.83, 0.54,
        "<b>Key Architectural Insight:</b> Separating <b>Turn Intelligence (`WHAT` move `A_t*` minimizes Distance-to-Quotation `DTQ` inside each `C × K` cluster)</b> from <b>Stylistic FAISS Retrieval (`HOW` to phrase move `A_t*` in the customer's persona voice)</b> and <b>Symbolic Governance (`WHETHER` the move is legal under business rules)</b> transforms the chatbot into a true <b>Grandmaster Consultative Sales Engine</b>.",
        bg_color=CALLOUT_BG, border_color=NAVY, font_size=8.3,
    )

