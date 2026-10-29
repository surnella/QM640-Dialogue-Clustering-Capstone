"""
Part 2 of the QM640 Capstone Defense Presentation (Slides 22–42):
  - Module 6 (Slides 22–34): Deep-Dive Empirical Results & Plain-English Walkthroughs for RQ1, RQ2, RQ3, and RQ4
  - Module 7 (Slides 35–38): Anticipated Defense Committee Questions & Direct Evidence-Backed Answers
  - Module 8 (Slides 39–42): Conclusive Story & Doctoral Dissertation Roadmap
    ("Dialogue Clustering and Methodologies to be Adapted for Human-Like Conversations")
"""

import os
from presentation.ppt_styles import (
    BLUE,
    CALLOUT_BG,
    CARD_BG,
    CORAL,
    GOLD,
    GREEN,
    GREEN_BG,
    NAVY,
    RED_BG,
    TEAL,
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
        headers=["Embedding Family & Algorithm", "Runs", "Silhouette M (SD)", "Davies–Bouldin", "ANOVA F (p)", "η²"],
        rows=[
            ["MiniLM (384-d) — K-Means (k = 3)", "53", ".099 (.005)", "2.712 (0.068)", "F(2, 156) = 91.33\n(p < .001)", ".539"],
            ["MiniLM (384-d) — Agglomerative (Ward)", "53", ".075 (.007)", "3.047 (0.129)", "Welch F = 113.84\n(p < .001)", "—"],
            ["MiniLM (384-d) — HDBSCAN (relaxed)", "53", ".170 (.050)", "1.787 (0.310)", "Kruskal H = 123.70\n(p < .001)", "—"],
            ["MiniLM (384-d) — Permutation Baseline", "53", "−.001 (.002)", "—", "Shuffled labels", "—"],
            ["Gemini-001 (3,072-d turn pool) — KM / Ward / HDB", "159", ".075 / .058 / .198", "—", "F = 169.39 (< .001)", ".685"],
            ["Gemini-001 (3,072-d document) — KM / Ward / HDB", "159", ".091 / .068 / .268", "—", "F = 813.09 (< .001)", ".912"],
        ],
        col_widths=[2.5, 0.5, 1.2, 1.1, 1.2, 0.5],
        font_size=9.5,
        align_left_cols=(0,),
        highlight_rows=(0, 4, 5),
    )
    D.add_card(
        s, 5.95, 4.88, 7.03, 2.22,
        title="Plain-English Interpretation for Non-AI & Math Reviewers",
        header_bg=NAVY,
        bullets=[
            "<b>1. Why All 3 Algorithms Beat Chance:</b> Random label shuffling gives Silhouette = <b>−.001</b>. All three algorithms find genuine structure (<i>p</i> < .001, explaining <b>53.9% to 91.2%</b> of variance).",
            "<b>2. Why HDBSCAN Cannot Be Used for Live Routing:</b> HDBSCAN achieves `.170` Silhouette only by <b>throwing away 71.7% of dialogues as 'noise'</b> (and failing completely in 53/53 runs at default `min_cluster_size=15`). A production chatbot cannot refuse to route 72% of customers!",
            "<b>3. Operational Winner:</b> <b>K-Means (<i>k</i> = 3)</b> partitions 100% of dialogues, significantly outperforms Ward agglomerative clustering (Tukey HSD & Games–Howell <i>p</i> < .001), and replicates across both 384-d and 3,072-d embeddings.",
        ],
        font_size=10,
    )

    # =========================================================================
    # SLIDE 23: RQ1 PART B — CROSS-CORPUS CHECK & WHY WHOLE-DIALOGUE CLUSTERS FAILED ROUTING
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (RQ1)",
        "RQ1 (Part 2): Cross-Corpus Transfer & Diagnosis of Whole-Dialogue Archetypes",
        "Figure D3 & Tables D3–D4: Why clustering full transcripts caused wizard confounding (V = .45) and weak early routing (κ = .24)",
        notes="Show intellectual honesty and scientific rigor: explain what our diagnostic audit found on the initial whole-dialogue clusters and why that motivated the representation x truncation breakthrough.",
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
        notes="Explain how we solved the three flaws: (1) user turns only, (2) truncated to first M=9 user messages, and (3) paired with a validated 16-field LLM behavioral profile.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_truncation_2x2.png"),
        0.35, 1.50, 6.30, 5.55,
        caption="Figure D4: Bootstrap Stability (ARI), Core Membership, Early Routing, and Outcome Association Across M",
    )
    D.add_table(
        s, 6.80, 1.50, 6.18, 2.75,
        headers=["Prefix Cut-Off (M User Msgs / ≈T Total Turns)", "Dialogues > M", "Bootstrap ARI", "Overall Test Acc (κ)", "Acc (<M / ≥M User Msgs)", "Outcome V"],
        rows=[
            ["M = 3 user msgs (≈ 5 total turns)", "96.0%", ".69", "59.4% (κ = .359)", "87.5% / 58.2%", ".14"],
            ["M = 5 user msgs (≈ 9 turns — RQ2 Runtime)", "83.2%", ".57", "70.1% (κ = .535)", "81.8% / 67.8%", ".17"],
            ["M = 7 user msgs (≈ 13 total turns)", "59.9%", ".69", "82.0% (κ = .722)", "93.2% / 74.6%", ".18"],
            ["M = 9 user msgs (≈ 17 turns — Offline Cap)", "38.6%", ".76", "97.3% (κ = .958)", "96.0% / 99.3%", ".20"],
            ["Whole conversation (Un-truncated)", "0.0%", ".89", "Confounded by outcome", "—", ".29"],
        ],
        col_widths=[1.85, 0.70, 0.65, 1.25, 1.15, 0.58],
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
            "<b>Ablation Proof (Table D6):</b> Embeddings-only at <i>M</i>=9 gets ARI = .39; combining PCA-20 Gemini + 13 clustering behavioral fields (`Blocks`) reaches <b>ARI = .76</b>!",
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
            ["Fields 11–13 (CAT Cluster): Goal / Sec. / Tone", "0.5% Exp, 99.3% Book | 42.4% | 52.4% Pos", "39.1% Exp, 50.8% Book | 56.3% | 69.3% Neut", "2.2% Exp, 89.8% Book | 16.4% | 7.6% Pos", "One-hot / binary features in 21-d LLM behavioral matrix"],
            ["Fields 14–16 (AUDIT Only): Outcome / Party / Flag", "90.5% Booked | 37.1% Solo/Cpl | 1.0% Flag", "68.1% Booked | 44.5% Solo/Cpl | 1.7% Flag", "28.0% Booked (68.0% None) | 34.5% | 6.9%", "Excluded from clustering to prevent outcome leakage!"],
        ],
        col_widths=[2.85, 2.25, 2.35, 2.35, 2.83],
        font_size=8.8,
        align_left_cols=(0, 4),
        highlight_rows=(0, 2, 3, 7, 8),
    )
    D.add_callout(
        s, 0.35, 5.95, 12.63, 1.10,
        "<b>Key Distinction — Total Turns (T) vs. User Messages (M), and Offline Cap (M = 9) vs. Runtime Routing (M = 5 in RQ2):</b>\n"
        "In Frames (<i>N</i> = 1,334), <b>total turns (T = User + Agent) average 14.93 (83.2% have ≥ 9 total turns / ≥ 5 user messages)</b>, while user-only messages average 7.78 (37.6% ≥ 9 user messages). "
        "Offline clustering uses `min(user_turns, 9)` to strip checkout outcome leakage from long chats while keeping all user turns for shorter chats. At runtime, routing is progressive: "
        "<b>M = 3 (≈5 turns): 59.4% (κ = .359)</b> → <b>M = 5 (≈9 turns, used in RQ2): 70.1% (κ = .535; 81.8% on <5-msg & 67.8% on ≥5-msg chats)</b> → <b>M = 7: 82.0%</b> → <b>M = 9: 97.3% (96.0% on ≤9 & 99.3% on ≥9 user msgs)</b>.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=10.0,
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
        title="Step-by-Step Computation of Holm-Adjusted Pairwise Contrasts",
        header_bg=NAVY,
        bullets=[
            "<b>Why Holm–Bonferroni Step-Down Adjustment?</b> Testing 3 pairs (`Adaptive vs Static`, `Adaptive vs Zero-Shot`, `Static vs Zero-Shot`) requires controlling familywise α = .05 by sorting raw <i>p</i>-values from smallest to largest and multiplying by (3, 2, 1).",
            "<b>Contrast 1 (`Cluster-Adaptive vs. Static Few-Shot`):</b>",
            (1, "Mean gain Δ = <b>+.144 cosine units (+31.8%)</b>, paired <i>t</i>(32) = <b>4.26</b>, <b><i>p</i><sub>Holm</sub> < .001</b>, standardized effect <b><i>d<sub>z</sub></i> = 0.74</b> (large)."),
            "<b>Contrast 2 (`Cluster-Adaptive vs. Zero-Shot`):</b>",
            (1, "Mean gain Δ = <b>+.067 cosine units (+12.6%)</b>, paired <i>t</i>(32) = <b>2.37</b>, <b><i>p</i><sub>Holm</sub> = .049</b>, <b><i>d<sub>z</sub></i> = 0.41</b>."),
        ],
        font_size=10,
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
        notes="Explain the 5 YAML policy rules (Table 9) and how we validated the LLM judge using an independent Gemini 2.5 Pro second judge (kappa = .917).",
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
            "<b>Why We Used Two Independent Judge Models:</b>",
            (1, "To prevent self-preference bias, responses generated by `gemini-2.5-flash` were audited on a stratified 48-unit subsample by both `gemini-2.5-flash` (Judge 1) and the larger reasoning model <b>`gemini-2.5-pro` (Judge 2)</b>."),
            "<b>Empirical Reliability Results (n = 48):</b>",
            (1, "<b>Raw Agreement:</b> <b>95.8%</b> (46 / 48 units identical)."),
            (1, "<b>Cohen's Kappa:</b> <b>κ = .917</b> (PABAK = .917), far exceeding the pre-registered κ ≥ .70 threshold!"),
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
        headers=["Experimental Cell or 2 × 2 ANOVA Effect", "n or df", "Rule Adherence M (SD) / Viol. %", "Exemplar Leakage M (SD) / Inc. %", "Slot Coverage F1 M (SD)", "Style Alignment M (SD)"],
        rows=[
            ["Cell 1: Rules Off × Zero-Shot", "36", ".500 (.507) / 5.6%", ".000 (.000) / 0.0%", ".208 (.242)", ".414 (.124)"],
            ["Cell 2: Rules Off × Cluster-Adaptive", "36", ".500 (.507) / 5.6%", ".359 (.348) / 55.6%", ".485 (.269)", ".507 (.095)"],
            ["Cell 3: Rules Active × Zero-Shot", "36", ".944 (.232) / 100.0%", ".000 (.000) / 0.0%", ".977 (.096)", ".428 (.107)"],
            ["Cell 4: Rules Active × Cluster-Adaptive (Pareto Optimal)", "36", ".931 (.244) / 97.2%", ".000 (.000) / 0.0%", ".952 (.124)", ".506 (.086)"],
            ["ANOVA Main Effect: Rules Mode (OLS / HC3 / ART)", "1, 140", "F = 43.92 (< .001), ηp² = .239\n(HC3 F=42.71; ART F=39.12)", "F = 34.82 (< .001), ηp² = .199\n(HC3 F=33.85; ART F=2148.8)", "F = 489.52 (< .001), ηp² = .778\n(HC3 F=476.0; ART F=194.2)", "F = 0.14 (.713), ηp² = .001"],
            ["ANOVA Main Effect: Prompting Mode (OLS / HC3 / ART)", "1, 140", "F = 0.01 (.916), ηp² = .000", "F = 34.82 (< .001), ηp² = .199", "F = 16.59 (< .001), ηp² = .106", "F = 24.00 (< .001), ηp² = .146"],
            ["ANOVA Interaction: Rules × Prompting (OLS / HC3 / ART)", "1, 140", "F = 0.01 (.916), ηp² = .000", "F = 34.82 (< .001), ηp² = .199\n(HC3 F=33.85; ART F=2148.8)", "F = 24.30 (< .001), ηp² = .148", "F = 0.19 (.665), ηp² = .001"],
        ],
        col_widths=[3.0, 0.8, 2.3, 2.3, 2.2, 2.0],
        font_size=9.3,
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
            "<b>Generated Reply (Neuro-Symbolic):</b> <i>'For your Dallas to Tokyo trip for 2 adults ($2,600 budget), please note that international departures within 15 days (9 days stated) require expedited visa verification before we lock in your 9-night package.'</i>",
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
            "<b>1. Grounded Seed Trips:</b> 30 held-out test dialogues per archetype (90 unique trip goals × 2 prompting modes = 180 multi-turn episodes).",
            "<b>2. Realistic 4-Option Travel Inventory per Dialogue:</b>",
            (1, "<b>Option A (4-Star Exact Match):</b> Exact destination & dates, 4-star hotel, priced at <b>88% of budget</b>."),
            (1, "<b>Option B (3.5-Star Saver):</b> Exact dates, boutique hotel, priced at <b>72% of budget</b>."),
            (1, "<b>Option C (5-Star Exact Dates — Over Budget):</b> 5-star luxury hotel on exact dates, priced at <b>118% of budget</b> (creates realistic constraint conflict!)."),
            (1, "<b>Option D (5-Star Shifted Dates — Within Budget):</b> 5-star luxury hotel with dates shifted +3 days, priced at <b>94% of budget</b>."),
            "<b>3. Stopping Criterion:</b> Conversation runs turn-by-turn until the user simulator issues `[ACCEPT_BOOKING]` (or hits 16-turn cap).",
        ],
        font_size=10,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 3.65,
        title="Blind Persona Fidelity Audit by Gemini 2.5 Pro (Table C3)",
        header_bg=TEAL,
        bullets=[
            "<b>How We Validated the User Simulator (n = 45 Transcripts):</b>",
            (1, "An independent `gemini-2.5-pro` judge read ONLY the customer utterances from 45 simulated dialogues (15 per archetype, blinded to condition and archetype label) and rated Decisiveness, Exploration Breadth, and Constraint Rigidity (1–5) plus predicted the archetype."),
            "<b>Validation Results:</b>",
            (1, "<b>Blind Classification Accuracy:</b> <b>95.6% (43 / 45 correct)</b> vs. 33.3% chance (exact binomial <b>p = 1.37 × 10⁻¹⁸ < .001</b>, <b>Cohen's κ = .933</b>)."),
            (1, "<b>Mean Behavioral Ratings (Decisiveness / Exploration / Rigidity):</b>\n"
                "      • <i>Decisive Booker:</i> <b>5.00</b> / 1.00 / 2.27\n"
                "      • <i>Open Explorer:</i> 2.80 / <b>4.27</b> / 1.60\n"
                "      • <i>Rigid-Constraint Seeker:</i> 1.67 / 2.27 / <b>4.33</b>"),
        ],
        font_size=10,
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
        "<b>Comparison with Human Wizard Baseline in Microsoft Frames (Appendix Table E5 & Figure E3):</b>\n"
        "In the historical human corpus, human travel agents averaged <b>14.96 turns (RER = .052)</b> for Decisive Bookers, <b>17.99 turns (RER = .061)</b> for Open Explorers, and <b>10.64 turns (RER = .053, with 44.5% failing to find an option)</b> for Rigid-Constraint Seekers. Our neuro-symbolic `Cluster-Adaptive Few-Shot` pipeline resolves all three archetypes in <b>5.00 to 5.27 turns with 100% goal completion and 0.000 RER</b>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=11,
    )

    # =========================================================================
    # SLIDE 34: CONSOLIDATED HYPOTHESIS SCORECARD & ENTERPRISE ROI SYNTHESIS
    # =========================================================================
    s = D.content_slide(
        "Module 6: Deep-Dive Empirical Results (Synthesis)",
        "Consolidated Hypothesis Testing Scorecard (Table 11) & Enterprise ROI",
        "All four null hypotheses (H01–H04) are rejected at p < .001 with large effect sizes and substantial operational savings",
        notes="Present Table 11 as the master executive summary of all empirical findings, followed by the concrete business ROI calculation.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 3.55,
        headers=["Research Question & Outcome", "Sample & Design", "Baseline vs. Proposed Performance", "Primary Parametric Test & Effect Size", "Robust / Non-Parametric Check", "Decision"],
        rows=[
            ["RQ1: Algorithm Separation &\nRefined Prefix Routing", "N = 159 runs\n(D_gold=933, D_test=401)", "Perm. Sil = −.001 vs. KM = .099, HDB = .170;\nRefined ARI = .76; Routing κ = .535 (M=5) to .958 (M=9)", "F(2, 156) = 91.33, p < .001, η² = .54\n(Gemini 3,072-d: F = 813.09, η² = .91)", "Welch F = 113.84, p < .001;\nKruskal H(2) = 123.70, p < .001", "Reject H01\n(p < .001)"],
            ["RQ2: Style Convergence &\nPacing Error (Refined)", "N = 33 dialogues × 3\nconditions (99 calls)", "Style Cos: Static = .453, Zero = .530 vs. Adaptive = .597\nPacing Error: Zero = 10.12w, Static = 6.33w vs. Adaptive = 3.87w", "Style F(1.88, 60.29) = 9.79, p < .001, ηp² = .234\nPacing F(1.30, 41.70) = 7.10, p = .007, ηp² = .182", "Friedman χ² = 12.50 (p = .002) &\n14.27 (p < .001); Holm p < .001", "Reject H02\n(p < .001)"],
            ["RQ3: Policy Rule Adherence,\nLeakage & Slot F1", "N = 144 (2 × 2,\nn = 36/cell; κ_judge = .917)", "Viol. Enforcement: 5.6% (Off) → 98.6% (Active)\nFew-Shot Leakage: .359 (55.6%) → .000 (0.0%); Slot F1: .485 → .952", "RAR Rules F(1, 140) = 43.92, p < .001, ηp² = .239\nELR Int. F = 34.82, p < .001; Slot F1 F = 489.52", "HC3 F = 42.71 & 33.85 (p < .001);\nART F = 39.12 & 2148.81 (p < .001)", "Reject H03\n(p < .001)"],
            ["RQ4: Multi-Turn Economy\n(Log Turns & RER)", "N = 180 (2 × 3,\nn = 30/cell; κ_persona = .933)", "Turns: −34.2% (DB), −29.5% (OE), −42.7% (RCS)\nOverall Turns: 7.93 → 5.09 (−35.8%); RER: .109 → .000", "Prompt F(1, 174) = 664.43, p < .001, ηp² = .793\nPrompt × Arch Int. F(2, 174) = 10.89, p < .001, ηp² = .111", "HC3 Int. F = 8.58, p < .001;\nART Int. F = 209.46, p < .001", "Reject H04\n(p < .001)"],
        ],
        col_widths=[2.0, 1.6, 3.1, 2.5, 2.2, 1.2],
        font_size=9.5,
        align_left_cols=(0, 1, 2, 3, 4),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_card(
        s, 0.35, 5.20, 12.63, 1.85,
        title="Practical Business Significance & Enterprise ROI (For an OTA Handling 1,000,000 Monthly Sessions)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Cloud Inference & Latency Savings (−35.8%):</b> Compressing mean dialogue length from 7.93 turns (`Zero-Shot`) to 5.09 turns (`Cluster-Adaptive`) saves <b>2.84 turns per session = 2,840,000 fewer LLM generation calls every month</b>, cutting token compute spend and customer wait time by more than one-third.",
            "<b>2. Zero Hallucination & Chargeback Prevention:</b> Eliminating exemplar entity leakage (from 55.6% incidence to <b>0.0%</b>) and raising booking policy compliance on invalid requests (short visa lead times, expiring passports, unauthorized 25% discounts) from 5.6% to <b>98.6%</b> prevents regulatory fines and disputed bookings.",
            "<b>3. Rescuing Rigid-Constraint Shoppers:</b> Proactive single-turn trade-off framing cuts negotiation turns by <b>42.7%</b> for the hardest customer segment (which suffered a 44.5% failure rate in historical human logs).",
        ],
        font_size=10.5,
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
            (1, "We assumed a standard 5% false-positive ceiling across all primary omnibus tests, supplemented by Tukey HSD (RQ1) and Holm–Bonferroni (RQ2) familywise error control for pairwise contrasts."),
            "<b>Assumption 2 — Target Statistical Power (1 − β ≥ .80, β ≤ .20):</b>",
            (1, "Following Cohen (1988), we set false-negative risk at ≤ 20%, requiring noncentrality λ = 8.00 (<i>df</i><sub>1</sub> = 1) to λ = 9.88 (<i>df</i><sub>1</sub> = 2)."),
            "<b>Assumption 3 — Medium Minimum Detectable Effect Size (f = .25):</b>",
            (1, "We powered every experiment to detect at least a medium effect (<i>f</i> = .25, equivalent to η<sup>2</sup> ≈ .059 or ~6% explained variance) so that any statistically significant effect also carries practical engineering meaning."),
            "<b>Assumption 4 — Within-Dialogue Correlation (ρ = .50) & Sphericity (ε = 1.0) in RQ2:</b>",
            (1, "For repeated-measures RQ2, we assumed moderate within-dialogue correlation ρ = .50 across the <i>m</i> = 3 prompt conditions."),
            "<b>Assumption 5 — +10% Cell-Balancing & Attrition Buffer:</b>",
            (1, "Minimum sample sizes (<i>N</i><sub>min</sub> = 158, 28, 128, 158) were buffered by ≥ 10% to exact integer multiples of cell counts: <b>159 (53×3), 33 (11×3), 144 (36×4), and 180 (30×6)</b>, achieving final a priori power of <b>.804 to .865</b>."),
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 5.45,
        title="Post-Hoc Empirical Audit: Did Our Data Satisfy Every Assumption?",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Observed Effect Sizes Far Exceeded f = .25 (η² = .059):</b>",
            (1, "• RQ1 Algorithm η<sup>2</sup> = <b>.539 to .912</b> (<i>f</i> = 1.08 to 3.22)"),
            (1, "• RQ2 Refined Style η<sub><i>p</i></sub><sup>2</sup> = <b>.234</b> (<i>f</i> = 0.55) & Pacing η<sub><i>p</i></sub><sup>2</sup> = <b>.182</b> (<i>f</i> = 0.47)"),
            (1, "• RQ3 Rules RAR η<sub><i>p</i></sub><sup>2</sup> = <b>.239</b>, Leakage Int. η<sub><i>p</i></sub><sup>2</sup> = <b>.199</b>, Slot F1 η<sub><i>p</i></sub><sup>2</sup> = <b>.778</b>"),
            (1, "• RQ4 Log Turns Prompt η<sub><i>p</i></sub><sup>2</sup> = <b>.793</b>, Interaction η<sub><i>p</i></sub><sup>2</sup> = <b>.111</b> (<i>f</i> = 0.35)"),
            (1, "→ Achieved post-hoc power > <b>.99</b> on all primary main effects and > <b>.95</b> on interactions!"),
            "<b>2. How We Handled Violations of Normality & Homoscedasticity:</b>",
            (1, "Classical ANOVA assumes normal residuals and equal cell variances. Because RQ3/RQ4 rates are bounded in [0, 1], we did NOT rely on normality alone: we ran <b>Welch / HC3 sandwich estimators</b> and <b>Aligned Rank Transform (ART) / Friedman / Kruskal–Wallis</b> tests."),
            "<b>3. How the +18% Buffer Saved RQ2 Under Sphericity Departure:</b>",
            (1, "In RQ2 pacing error, Greenhouse–Geisser ε was 0.65 (reducing effective <i>df</i> from 2, 64 to 1.30, 41.70). Because we buffered <i>N</i> from 28 to 33, the GG-adjusted test still achieved <i>p</i> = .007!"),
        ],
        font_size=10.2,
    )

    # =========================================================================
    # SLIDE 36: DEFENSE Q&A 2 & 3 — PRIOR RESEARCH USED VS. UNIQUE ORIGINALITY
    # =========================================================================
    s = D.content_slide(
        "Module 7: Anticipated Defense Q&A Bank",
        "Defense Q&A #2 & #3: 'What Prior Research Did You Use, and What Is Uniquely Yours?'",
        "Clear demarcation between inherited scientific building blocks and the five original contributions of this study",
        notes="Use this slide to answer Defense Questions #2 and #3 concisely and authoritatively.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 5.55,
        headers=["Scientific Component", "Q2: What Prior Research We Used & How We Applied It", "Q3: What Is Uniquely Original in This Study (Never Done in Prior Literature)"],
        rows=[
            [
                "1. User Trajectory Representation & Archetype Discovery (RQ1)",
                "Used <b>Sentence-BERT</b> (Reimers & Gurevych, 2019), <b>Gemini 3,072-d Embeddings</b> (Lee et al., 2025), <b>K-Means / Ward / HDBSCAN</b> (McInnes et al., 2017), <b>Bootstrap ARI</b> (Hennig, 2007), and <b>zero-temp LLM rating reliability</b> (Gilardi et al., 2023).",
                "<b>Original Contribution 1:</b> Discovered that whole-dialogue clustering in consultative travel is confounded by wizard identity (<i>V</i> = .45) and session outcome (<i>V</i> = .29). Invented the <b>prefix-truncated (M = 9 user messages) hybrid `Blocks` representation</b> (PCA-20 Gemini prefix + 16-field LLM behavioral codebook) and `RefinedArchetypeRouter`, achieving <b>ARI = .76</b> and out-of-sample prefix routing of <b>κ = .535 (M=5) to .958 (M=9)</b>.",
            ],
            [
                "2. Archetype-Routed In-Context Learning (RQ2)",
                "Built upon <b>few-shot in-context learning</b> (Brown et al., 2020), <b>KATE nearest-neighbor example selection</b> (Liu et al., 2022), <b>FAISS vector indexing</b> (Johnson et al., 2021), and <b>BERTScore</b> (Zhang et al., 2020).",
                "<b>Original Contribution 2:</b> Partitioned FAISS into <b>archetype-specific sub-indices with `[SLOT]` masking</b> and proved a <b>causal boundary condition</b> by contrasting Primary (<i>p</i> = .211) vs. Refined (<i>p</i> < .001) archetypes: dynamic exemplar retrieval improves style (+31.8% over static, <i>d<sub>z</sub></i> = 0.74) and pacing (3.87w error) <i>only when upstream prefix routing exceeds κ > .50</i>.",
            ],
            [
                "3. Neuro-Symbolic Policy Verification & Leakage Control (RQ3)",
                "Drew motivation from <b>NeMo Guardrails</b> (Rebedea et al., 2023), <b>τ-bench policy failure benchmarks</b> (Yao et al., 2024), and <b>TD-EVAL</b> (Acikgoz et al., 2025).",
                "<b>Original Contribution 3:</b> Executed the first <b>2 × 2 factorial experiment crossing declarative rule verification with cluster-adaptive prompting</b>. Quantified the <b>35.9% exemplar entity leakage hazard</b> (55.6% incidence) of unguarded few-shot prompting and proved a significant interaction (<i>F</i> = 34.82, <i>p</i> < .001) where symbolic verification reduces leakage to <b>0.0%</b> while raising violation enforcement from <b>5.6% to 98.6%</b>.",
            ],
            [
                "4. Multi-Turn Turn Economy & Slot Ledger (RQ4)",
                "Built on <b>hospitality service ROI theory</b> (Buhalis & Sinarta, 2019; Ivanov & Webster, 2019; Melián-González et al., 2021) and <b>travel agency interaction analysis</b> (Inaba et al., 2022).",
                "<b>Original Contribution 4:</b> Designed the <b>Verified Informed Slot Ledger + Archetype-Specific Turn-Economy Policy</b> and proved a <b>2 × 3 Prompting × Archetype interaction (F = 10.89, p < .001)</b>: compressing multi-turn sessions by <b>29.5% to 42.7%</b> (largest gain for <i>Rigid-Constraint Seekers</i>, <i>d</i> = −3.40) and eliminating redundant slot questions (<b>RER .109 → .000</b>).",
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
        "Defense Q&A #4: 'What Is the Authenticity of the Datasets & Do They Match Your Research?'",
        "Addressing corpus provenance, why they were created, why they fit, and how we handled their structural boundaries",
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
        title="2. Why They Match Our Research—and How We Addressed Boundaries",
        header_bg=TEAL,
        bullets=[
            "<b>Why Microsoft Frames Is the Ideal Match for RQ1–RQ4:</b>",
            (1, "Unlike synthetic LLM-generated datasets, Frames contains natural human decision-making heterogeneity—hesitations, price bargaining, city comparisons, and 25.8% unbooked sessions—allowing authentic discovery of <i>Decisive Bookers</i>, <i>Open Explorers</i>, and <i>Rigid-Constraint Seekers</i>."),
            "<b>Why MultiWOZ 2.2 Is the Ideal External Contrast:</b>",
            (1, "Because MultiWOZ has transactional city bookings without flight+hotel package bargaining, our RQ1 transfer check (<i>t</i> = 28.08, <i>p</i> < .001) empirically proves that consultative travel archetypes are distinct from generic slot-filling."),
            "<b>How We Transparently Bridged Two Corpus Boundaries:</b>",
            (1, "<b>Boundary A (Tier-2 Enterprise Rules):</b> Public corpora do not log visa windows or passport expiry (0% in Table E1/E4). We preserved the exact held-out Frames user prefixes and injected controlled, seeded Tier-2 states in RQ3."),
            (1, "<b>Boundary B (Interactive Multi-Turn Evaluation in RQ4):</b> Static corpus logs cannot reply to new chatbot actions. We seeded persona simulators from real held-out Frames trip goals and proved <b>95.6% persona fidelity (κ = .933)</b> via blind `gemini-2.5-pro` audit."),
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
            (1, "We cross-checked `gemini-2.5-flash` against the larger independent `gemini-2.5-pro` judge on <i>n</i> = 48 units: <b>95.8% raw agreement, κ = .917</b>, and <b>93.1% agreement (κ = .861)</b> with deterministic regex verification."),
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
        title="Chapter 1 of Our Story (RQ1)\nDiscover Who Is Talking",
        header_bg=NAVY,
        bullets=[
            "<b>The Question:</b> Can we discover stable traveler archetypes and route them early?",
            "<b>What We Proved:</b>",
            (1, "Whole-dialogue clustering fails early routing (κ = .24) due to outcome confounding."),
            (1, "Combining <b>PCA-20 Gemini user prefixes + 16 LLM behavioral ratings (`Blocks`)</b> on the first 9 messages yields 3 stable personas (<b>ARI = .76</b>): <i>Decisive Booker</i>, <i>Open Explorer</i>, and <i>Rigid-Constraint Seeker</i>."),
            (1, "Out-of-sample routing reaches <b>70.1% (M=5) to 97.3% (M=9)</b>."),
        ],
        font_size=10,
    )
    D.add_card(
        s, 3.55, 1.50, 3.05, 4.20,
        title="Chapter 2 of Our Story (RQ2)\nAdapt How the Agent Speaks",
        header_bg=TEAL,
        bullets=[
            "<b>The Question:</b> Does archetype-matched few-shot retrieval improve style and pacing?",
            "<b>What We Proved:</b>",
            (1, "Coarse routing (κ = .24) yields null style adaptation (<i>p</i> = .211)."),
            (1, "Accurate `Blocks` routing (κ = .535) unlocks highly significant style convergence (<b>F = 9.79, p < .001, ηp² = .234</b>) and cuts pacing error from 10.12w to <b>3.87 words (p = .007)</b>."),
            (1, "<b>Lesson:</b> Dynamic ICL is bounded by upstream routing fidelity."),
        ],
        font_size=10,
    )
    D.add_card(
        s, 6.75, 1.50, 3.05, 4.20,
        title="Chapter 3 of Our Story (RQ3)\nGuard Against Leakage & Policy Drift",
        header_bg=CORAL,
        bullets=[
            "<b>The Question:</b> How do symbolic rules and adaptive prompts interact?",
            "<b>What We Proved:</b>",
            (1, "Unguarded few-shot prompting leaks stale exemplar entities in <b>55.6% of replies (ELR = .359)</b> and misses <b>94.4%</b> of policy violations."),
            (1, "Pairing `Cluster-Adaptive` with our declarative `RuleEngine` eliminates leakage to <b>0.0% (Interaction F = 34.82, p < .001)</b>, raises violation enforcement to <b>97.2%</b>, and boosts Slot F1 to <b>.952</b>."),
        ],
        font_size=10,
    )
    D.add_card(
        s, 9.95, 1.50, 3.03, 4.20,
        title="Chapter 4 of Our Story (RQ4)\nCompress Multi-Turn Negotiations",
        header_bg=GREEN,
        bullets=[
            "<b>The Question:</b> Does our full architecture improve multi-turn turn economy?",
            "<b>What We Proved:</b>",
            (1, "Across 180 simulations (persona κ = .933), `Cluster-Adaptive` + Informed Slot Ledger cuts turns by <b>−42.7% for Rigid Seekers</b>, <b>−34.2% for Decisive Bookers</b>, and <b>−29.5% for Open Explorers</b> (<i>F</i> = 664.43, Interaction <i>F</i> = 10.89, <i>p</i> < .001)."),
            (1, "Redundant slot questions drop from <b>10.9% to 0.0%</b>."),
        ],
        font_size=10,
    )
    D.add_callout(
        s, 0.35, 5.85, 12.63, 1.20,
        "<b>Master Conclusion of the Paper:</b>\n"
        "Improving enterprise conversational AI is not a matter of choosing between 'better prompts' OR 'strict rules'. It requires a <b>three-part neuro-symbolic synergy</b>: (1) <b>Early Behavioral-Semantic Routing</b> (`Blocks`) to know <i>who</i> the user is; (2) <b>Slot-Masked Archetype Exemplar Retrieval</b> to adapt <i>how</i> the assistant communicates and frames trade-offs; and (3) <b>Declarative Symbolic Verification & Slot Ledgers</b> to guarantee <i>what</i> the assistant says is 100% policy-compliant, grounded, and non-repetitive.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=11,
    )

    # =========================================================================
    # SLIDE 40: WHERE THIS CAPSTONE ENDS — OPEN QUESTIONS FOR DOCTORAL RESEARCH
    # =========================================================================
    s = D.content_slide(
        "Module 8: Conclusive Story & Doctoral Dissertation Roadmap",
        "Where This Capstone Ends: Four Scientific Frontiers Opened by Our Findings",
        "Requirement #5b: Identifying the fundamental boundaries discovered in RQ1–RQ4 that motivate a full Doctoral Dissertation",
        notes="Transition from the master's capstone findings to the bigger doctoral dissertation topic: 'Dialogue Clustering and Methodologies to be Adapted for Human-Like Conversations'.",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 2.65,
        title="Frontier 1: Continuous Manifold vs. Hard K-Means Clusters",
        header_bg=NAVY,
        bullets=[
            "<b>What Our Capstone Data Revealed (RQ1):</b>",
            (1, "While <i>K</i>-Means (<i>k</i> = 3) achieved high bootstrap stability (ARI = .76), raw cosine Silhouette scores (.099–.268) and our Multivariate PCA Biplot (Figure 3) proved that human conversational styles form a <b>continuous behavioral manifold</b> rather than isolated islands."),
            "<b>What Remains Unsolved for the Dissertation:</b>",
            (1, "25.2% of speakers sit near cluster boundaries (e.g., a traveler who is 55% <i>Open Explorer</i> and 45% <i>Rigid-Constraint Seeker</i>). Hard argmax routing forces a binary choice rather than blending styles smoothly."),
        ],
        font_size=10,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 2.65,
        title="Frontier 2: Dynamic Mid-Session Persona Drift (Non-Stationarity)",
        header_bg=TEAL,
        bullets=[
            "<b>What Our Capstone Data Revealed (RQ1 & RQ4):</b>",
            (1, "Our prefix router assigns a static archetype after <i>M</i> = 5 to 9 messages. However, real humans <b>shift personas mid-conversation</b>: an <i>Open Explorer</i> in Turns 1–5 often becomes a <i>Rigid-Constraint Seeker</i> in Turn 7 once they experience sticker shock!"),
            "<b>What Remains Unsolved for the Dissertation:</b>",
            (1, "How to model a user's conversational style as a <b>non-stationary stochastic trajectory</b> <b>z</b><sub><i>t</i></sub> that updates turn-by-turn from Turn 1 onward via Bayesian belief tracking."),
        ],
        font_size=10,
    )
    D.add_card(
        s, 0.35, 4.30, 6.15, 2.75,
        title="Frontier 3: Micro-Conversational Human-Likeness & Conversational Repair",
        header_bg=BLUE,
        bullets=[
            "<b>What Our Capstone Data Revealed (EDA & RQ2):</b>",
            (1, "Our bivariate EDA (Table 7) showed that human uncertainty is marked by <i>hesitation markers</i> (<i>r</i> = .192 with revisions), empathetic grounding, and collaborative repair when constraints conflict."),
            "<b>What Remains Unsolved for the Dissertation:</b>",
            (1, "Matching centroid cosine and word count (RQ2) captures <i>macro-style</i>, but true <b>human-like conversation</b> requires modeling <i>micro-pragmatics</i>: backchanneling, empathetic acknowledgment of budget frustration, mixed-initiative turn-taking, and graceful conversational repair."),
        ],
        font_size=10,
    )
    D.add_card(
        s, 6.80, 4.30, 6.18, 2.75,
        title="Frontier 4: Moving Beyond Cooperative LLM Simulators to Live Humans",
        header_bg=GOLD,
        bullets=[
            "<b>What Our Capstone Data Revealed (RQ4):</b>",
            (1, "Even though our persona simulator achieved κ = .933 fidelity, simulated users completed 100% of sessions in 5.00–5.27 turns—whereas real humans in Frames had a 25.8% non-completion rate and noisier multi-topic tangents."),
            "<b>What Remains Unsolved for the Dissertation:</b>",
            (1, "Training and evaluating adaptive dialogue policies with <b>offline-to-online Reinforcement Learning from Human Conversations (RLHC)</b> with live human participants across multiple domains."),
        ],
        font_size=10,
    )

    # =========================================================================
    # SLIDE 41: DOCTORAL DISSERTATION ROADMAP
    # =========================================================================
    s = D.content_slide(
        "Module 8: Conclusive Story & Doctoral Dissertation Roadmap",
        "Future Doctoral Dissertation Roadmap: 'Dialogue Clustering & Methodologies for Human-Like Conversations'",
        "Requirement #5b: Four doctoral research pillars directly extending this capstone's findings and codebase",
        notes="Present the concrete 4-pillar plan for your upcoming doctoral dissertation.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 4.35,
        headers=["Doctoral Dissertation Pillar", "Core Research Question for the Dissertation", "Proposed Methodology & Mathematical Framework", "How This Capstone's Findings Directly Aid & Seed This Pillar"],
        rows=[
            [
                "Pillar 1:\nSoft-Mixture & Variational Manifold Trajectory Clustering",
                "Can continuous Gaussian Mixture / Variational Autoencoder (VAE) latent spaces outperform hard K-Means partitioning for boundary speakers?",
                "Replace hard centroid assignment with a Dirichlet / Von Mises–Fisher mixture over the `Blocks` manifold: retrieve a <b>convex combination of exemplars</b> weighted by posterior probabilities P(c_k | prefix_t).",
                "Directly reuses our validated 36-d `Blocks` representation (PCA-20 Gemini + 16-field behavioral codebook) and our 25.2% non-core boundary dialogue subset identified in `step2h/2i`.",
            ],
            [
                "Pillar 2:\nTurn-by-Turn Bayesian Persona Tracking & Drift Detection",
                "How can an agent detect mid-dialogue persona shifts (e.g., Explorer → Rigid Negotiator) starting from Turn 1?",
                "Formulate a <b>Hidden Markov / Kalman State-Space Persona Tracker</b> that updates posterior persona beliefs P(z_t | u_1..t) after every user utterance and detects change-points in constraint rigidity.",
                "Builds directly on our truncation horizon curve (M = 3, 5, 7, 9 in Table D5) and `RefinedArchetypeRouter`, extending static prefix routing into sequential filtering.",
            ],
            [
                "Pillar 3:\nPragmatic & Affective Micro-Adaptations for Human-Like Dialogue",
                "Which linguistic, affective, and conversational-repair micro-strategies make an AI agent indistinguishable from a skilled human consultant?",
                "Expand our 16-field behavioral codebook to 30+ <b>pragmatic/affective act dimensions</b> (empathy, hedging, collaborative trade-off framing, grounding acts) and condition generation on turn-level pragmatic transitions.",
                "Extends our RQ2 style-convergence and pacing-error metrics (`step2_rq2_refined.py`) from surface cosine/length to discourse-act transition matrices.",
            ],
            [
                "Pillar 4:\nConstrained Neuro-Symbolic RL for Multi-Domain Human-Like Agents",
                "Can we optimize multi-turn human-likeness, rapport, and task efficiency simultaneously under zero-violation symbolic constraints?",
                "Formulate a <b>Constrained Markov Decision Process (CMDP)</b> where our declarative `RuleEngine` acts as a hard safety shield while Offline RL (CQL / DPO) optimizes turn economy and human rapport across Travel, Healthcare & Banking.",
                "Uses our RQ3 `RuleEngine` (0.0% leakage, 98.6% adherence) as the deterministic safety shield and our RQ4 multi-turn simulator (`step4_rq4_simulation.py`) as the pre-deployment training gym.",
            ],
        ],
        col_widths=[2.2, 2.8, 4.0, 3.6],
        font_size=9.8,
        align_left_cols=(0, 1, 2, 3),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_callout(
        s, 0.35, 6.00, 12.63, 1.05,
        "<b>Why This Capstone Is the Ideal Foundation for the Doctoral Dissertation:</b>\n"
        "This master's study solved the <i>foundational architecture</i>—proving that behavioral-semantic trajectory clustering (`Blocks`), slot-masked exemplar retrieval, and declarative symbolic guardrails work together with <i>p</i> < .001 across all four RQs. The doctoral dissertation elevates this static, episode-level travel framework into a <b>continuous, dynamic, cross-domain theory of human-like conversational adaptation</b>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=11,
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
            "<b>1. RQ1 (Discovery & Routing):</b> Truncating to opening user behavior (`M = 9` messages) and combining Gemini embeddings with 16 validated LLM behavioral ratings (`Blocks`) yields 3 stable archetypes (<b>ARI = .76</b>) and raises held-out prefix routing to <b>70.1% (M=5) and 97.3% (M=9, κ = .958)</b>.",
            "<b>2. RQ2 (Style & Pacing):</b> Contrasting Primary (<i>p</i> = .211) vs. Refined (<b>p < .001, ηp² = .234</b>) archetypes proves that in-context style convergence (+31.8% over static, <i>d<sub>z</sub></i> = 0.74) and pacing calibration (<b>3.87w error</b>) succeed once upstream routing is coherent.",
            "<b>3. RQ3 (Safety & Guardrails):</b> Declarative rule verification eliminates the <b>35.9% entity leakage</b> of unguarded few-shot prompting down to <b>0.0% (Interaction F = 34.82, p < .001)</b> while raising policy violation enforcement from <b>5.6% to 98.6%</b> and Slot F1 to <b>.952</b> (Dual-judge <b>κ = .917</b>).",
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
            (1, "`src/interim_pipeline/` (Steps 0–4 & sensitivity Steps 2b–2i)"),
            (1, "`src/final_pipeline/` (`common_llm.py`, `routing.py`, `metrics.py`, `step2_rq2_refined.py`, `step3_rq3_experiment.py`, `step4_rq4_simulation.py`, `step5_figures_and_eda.py`)"),
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

