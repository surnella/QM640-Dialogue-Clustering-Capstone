"""
Part 2 of the QM640 Final Report builder (aligned to the QM 640 Final Report Template,
Moderator Committee feedback, and 400-point Final Report Rubric):
  - Section 5: Results (Model Performance Tables 11–12, Visual Evidence & Feature Importance Table 13 & Figure 6,
    Results by Research Question [RQ1 Tables 14–15, RQ2 Table 16 & Figure 7, RQ3 Table 17 & Figure 8,
    RQ4 Table 18 & Figure 9], Overall Interpretation, Practical Significance)
  - Section 6: Implementation and User Benefit (Deployment Approach, System Integration, User Interaction,
    Benefits to Users, Example Use Case)
  - Section 7: Limitations and Further Improvements (Limitations [Data & Model], Impact of Limitations,
    Future Improvements, Future Scope [incl. Multi-Interaction Opportunity_ID TTL/TTQ/CSET & Turn-Q DB])
  - References (30 standardized APA 7 entries with published JOSS UMAP & [Preprint] tags)
  - Appendices A–G (Tables A1–A3, B1, C1–C3, D1–D6 + Figures D1–D4, E1–E5 + Figures E1–E3, F1, G1)
"""

import os
import pandas as pd
from report.final_context import (
    ARCH_PRIM,
    ARCH_REF,
    FIG_FIN,
    FIG_INT,
    REPO,
    n2,
    nz,
    pct,
    pv,
    pv_cell,
)
from report.references import REFERENCES


def build_part2(D, ctx):
    comp = ctx["comp"]
    s1 = ctx["s1"]
    r1 = ctx["r1"]
    k_sel = ctx["k_sel"]
    r1_desc = ctx["r1_desc"]
    r1_tk = ctx["r1_tk"]
    prof = ctx["prof"]
    cross = ctx["cross"]
    r2_prim = ctx["r2_prim"]
    r2_ref = ctx["r2_ref"]
    r3_fin = ctx["r3_fin"]
    r4_fin = ctx["r4_fin"]
    audit = ctx["audit"]
    rep_m = ctx["rep_m"]
    r1gm = ctx["r1gm"]
    r1h = ctx["r1h"]
    r1t = ctx["r1t"]
    r1r = ctx["r1r"]
    trg = ctx["trg"]
    abl = ctx["abl"]
    rprof = ctx["rprof"]
    base4r = ctx["base4r"]
    rt_diag = ctx["rt_diag"]
    t_mv = ctx["t_mv"]
    t_fi = ctx["t_fi"]
    t_blk = ctx["t_blk"]
    t_split = ctx["t_split"]
    fi_diag = ctx["fi_diag"]
    gh = ctx["gh"]
    r1_rm = ctx["r1_rm"]
    r3_rar_cells = ctx["r3_rar_cells"]
    r3_rar_anova = ctx["r3_rar_anova"]
    blocks_k_sel = ctx["blocks_k_sel"]

    an = r1["anova"]
    we = r1["welch"]
    kw = r1["kruskal"]
    perm = r1["permutation_baseline"]
    cc = r1["cross_corpus_t"]
    gt = r1["gold_vs_test_t"]
    km, ag, hd = (r1_desc.loc[a] for a in ["K-Means", "Agglomerative", "HDBSCAN"])
    tr3 = trg[trg.k == 3].set_index("M")
    a9 = abl[abl.M == "9"].set_index("config")
    aw = abl[abl.M == "whole"].set_index("config")
    kap_prim = float(rep_m.loc[("R0", 3), "kappa_N5"])

    feat = [
        ("Destination flexibility", "destination_flexibility"),
        ("Date flexibility", "date_flexibility"),
        ("Exploration breadth", "exploration_breadth"),
        ("Decisiveness", "decisiveness"),
        ("Detail orientation", "detail_orientation"),
        ("Revision tendency", "revision_tendency"),
        ("Question asking", "question_asking"),
        ("Politeness", "politeness"),
        ("Price sensitivity", "price_sensitivity"),
        ("Information given up front", "information_upfront"),
    ]
    cv_ = r1h["criterion_validity"]

    r2_sc = r2_ref["results"]["sbert_style_cos"]
    r2_sa = r2_sc["anova"]
    r2_we_r = r2_ref["results"]["word_abs_err"]
    r2_wa = r2_we_r["anova"]
    r3_a = r3_fin["anova"]
    r4_a = r4_fin["anova"]

    # ================================================================== 5. RESULTS
    D.heading("Results", 1)
    D.heading("Model Performance", 2)
    D.para(
        "Table 11 presents the consolidated model performance comparison across all four experimental stages, "
        "reporting features used, validation and data-splitting methods, separated baseline/training and held-out test "
        "metrics, omnibus statistical tests, and explicit identification of the best-performing model in each stage. "
        "All four study null hypotheses (<i>H</i><sub>01</sub>–<i>H</i><sub>04</sub>) are rejected at <b><i>p</i> < .001</b> "
        "(well below α = .05). To verify out-of-sample generalization of the supervised prefix router without "
        "overfitting, Table 12 reports separated <b>training (<i>D</i><sub>gold</sub>, <i>n</i> = 933)</b>, <b>5-fold "
        "stratified cross-validation (<i>D</i><sub>gold</sub>)</b>, and <b>held-out test (<i>D</i><sub>test</sub>, "
        "<i>n</i> = 401)</b> accuracy, chance-corrected Cohen's κ, macro F<sub>1</sub>, and macro One-vs-Rest "
        "receiver operating characteristic area under the curve (ROC-AUC) across prefix cut-offs <i>M</i> ∈ {3, 5, 7, 9}."
    )
    D.table(
        "Consolidated Model Performance Comparison Across Discovery/Training and Held-Out Test Splits",
        [
            "Model / Pipeline stage",
            "Features used",
            "Validation & split",
            "Metric 1 (Train / Baseline)",
            "Metric 2 (Held-Out Test / Proposed)",
            "Key observation & best model",
        ],
        [
            [
                "<b>RQ1-Identify (Clustering):</b> ★ <b>K-Means (<i>k</i>=3, Best)</b> vs. Ward & HDBSCAN",
                "384-d MiniLM, 3,072-d Gemini, & 46-d <i>Blocks</i> (<i>M</i>=9)",
                "53 matched <i>n</i>=500 seeds on <i>D</i><sub>gold</sub> (933) + <i>D</i><sub>test</sub> (401)",
                f"<i>D</i><sub>gold</sub> KM Sil = {nz(km.sil_M, 3)} (100% kept) vs. HDB = {nz(hd.sil_M, 3)} (39.1% noise); Blocks DB = 2.647, ARI = .89",
                f"<i>D</i><sub>test</sub> centroid cos = .523 vs. <i>D</i><sub>gold</sub> .526 (<i>p</i> {pv(gt['p'])}); RM <i>F</i> = {n2(r1_rm['F'])}, <i>p</i> < .001",
                "<b>★ Best: K-Means (<i>k</i>=3) on 46-d Blocks</b> (100% routing coverage, lowest DB, ARI = .89; Reject <i>H</i><sub>01</sub>)",
            ],
            [
                "<b>RQ1-Identify (Prefix Router):</b> ★ <b>Blocks L2 Logistic (Best)</b> vs. Raw Prefix",
                "PCA-20 Gemini prefix + 26-d LLM behavior (<i>M</i>=3..9)",
                "Train (<i>n</i>=933), 5-fold CV, & Held-out <i>D</i><sub>test</sub> (<i>n</i>=401)",
                "<i>M</i>=5 Train Acc = 73.8% (κ = .591, AUC = .892); 5-Fold CV Acc = 70.0% (κ = .530)",
                "<i>M</i>=5 Test Acc = 70.1% (κ = .535, AUC = .871); <i>M</i>=9 Test Acc = 97.3% (κ = .958, AUC = .999)",
                "<b>★ Best: Projected Blocks L2 Router</b> (0.1% CV–test gap; +29.5 κ pts over raw .240; Reject <i>H</i><sub>01</sub>)",
            ],
            [
                "<b>RQ2-Personalize (Prompting):</b> ★ <b>Cluster-Adaptive (Best)</b> vs. Static & Zero-Shot",
                "Routed FAISS sub-index (<i>k</i>=3 [SLOT] ex.) + directive",
                "Repeated-measures on <i>D</i><sub>test</sub> (<i>N</i>=33 × 3 = 99 calls)",
                f"Static cos = {nz(r2_sc['desc']['Static Few-Shot'][0], 3)} (6.33w err.); Zero-Shot cos = {nz(r2_sc['desc']['Zero-Shot'][0], 3)} (10.12w err.)",
                f"Cluster-Adaptive cos = <b>{nz(r2_sc['desc']['Cluster-Adaptive Few-Shot'][0], 3)}</b> (<b>3.87w</b> err.); RM <i>F</i> = {n2(r2_sa['F'])}, <i>p</i> < .001",
                "<b>★ Best: Cluster-Adaptive Few-Shot</b> (+31.8% style cos over Static, <i>d<sub>z</sub></i> = 0.74; Reject <i>H</i><sub>02</sub>)",
            ],
            [
                "<b>RQ3-Govern (Governance):</b> ★ <b>Rules Active × Adaptive (Best)</b> vs. 3 Arms",
                "5 YAML rules + [SLOT] masking + entity sanitizer",
                "2 × 2 factorial on <i>D</i><sub>test</sub> (<i>N</i>=144, <i>n</i>=36/cell; κ=.917)",
                "Rules Off × Adaptive: Sens. = 5.6%, ELR = .359 (55.6% leak), Slot F<sub>1</sub> = .485",
                "Rules Active × Adaptive: Sens. = <b>97.2%</b> (overall 98.6%), ELR = <b>.000</b>, Slot F<sub>1</sub> = <b>.952</b>, cos = .506",
                "<b>★ Best: Rules Active × Cluster-Adaptive</b> (Pareto-optimal zero leakage + high style; Reject <i>H</i><sub>03</sub>)",
            ],
            [
                "<b>RQ4-Optimize (Turn Economy):</b> ★ <b>Ledger + Adaptive (Best)</b> vs. Zero-Shot",
                "Verified Informed Slot Ledger + persona trade-offs",
                "2 × 3 between-subjects on <i>D</i><sub>test</sub> (<i>N</i>=180 unique, <i>n</i>=30/cell)",
                "Zero-Shot mean = 7.93 turns (DB 7.60, OE 7.47, RCS 8.73); mean RER = .109",
                "Adaptive mean = <b>5.09 turns</b> (−34.2% DB, −29.5% OE, −42.7% RCS); RER = <b>.000</b> (<i>F</i> = 664.43)",
                "<b>★ Best: Slot Ledger + Cluster-Adaptive</b> (35.8% overall turn cut, zero repeat asks; Reject <i>H</i><sub>04</sub>)",
            ],
        ],
        note="★ indicates the selected best-performing model at each pipeline stage. DB = Decisive Booker; OE = Open Explorer; RCS = Rigid-Constraint Seeker.",
        widths=[1.12, 0.96, 1.00, 1.14, 1.18, 1.10],
        align=["l", "l", "l", "l", "l", "l"],
        split=True,
    )

    sp_rows = []
    for m_v in (3, 5, 7, 9):
        sr = t_split.loc[m_v]
        role_tag = "Runtime router (RQ2–RQ4)" if m_v == 5 else ("Reference boundary check" if m_v == 9 else "Early prefix horizon")
        sp_rows.append([
            f"<i>M</i> = {m_v} (~{int(sr.approx_turns)} turns)",
            f"{pct(100 * sr.train_acc)} ({nz(sr.train_kappa, 3)}) / {nz(sr.train_auc, 3)}",
            f"{pct(100 * sr.cv_acc)} ({nz(sr.cv_kappa, 3)}) / {nz(sr.cv_auc, 3)}",
            f"<b>{pct(100 * sr.test_acc)}</b> (<b>{nz(sr.test_kappa, 3)}</b>)",
            f"{nz(sr.test_macro_f1, 3)} / <b>{nz(sr.test_auc, 3)}</b>",
            role_tag,
        ])
    D.table(
        "Separated Training (Golden Partition), 5-Fold Cross-Validation, and Held-Out Test Routing Performance",
        [
            "Prefix cut-off (<i>M</i> user msgs)",
            "Train <i>D</i><sub>gold</sub> (<i>n</i>=933) Acc (κ) / AUC",
            "5-Fold CV (<i>D</i><sub>gold</sub>) Acc (κ) / AUC",
            "Held-Out <i>D</i><sub>test</sub> (<i>n</i>=401) Acc (κ)",
            "Held-Out Macro F<sub>1</sub> / ROC-AUC",
            "Analytical role",
        ],
        sp_rows,
        note="All PCA-20 projections, block scalers, and L2 multinomial logistic regression weights (<i>C</i> = 1.0) are fitted strictly on <i>D</i><sub>gold</sub>. Minimal gaps between 5-fold CV and held-out <i>D</i><sub>test</sub> (e.g., 70.0% vs. 70.1% at <i>M</i> = 5) confirm zero overfitting.",
        widths=[1.08, 1.25, 1.25, 1.05, 0.95, 0.92],
        align=["l", "c", "c", "c", "c", "l"],
        split=True,
    )

    # ------------------------------------------------------------------ Visual Evidence & Feature Importance
    D.heading("Visual Evidence", 2)
    cm5 = fi_diag["cm_m5"]
    cm9 = fi_diag["cm_m9"]
    D.para(
        "Table 13 and Figure 6 present the visual and quantitative evaluation diagnostics for feature importance, "
        "confusion matrix structure, and multi-class receiver operating characteristic (ROC) discrimination. First, "
        "assessing feature importance across all 46 <i>Blocks</i> dimensions (Table 13, top rows; Figure 6, Panel A) "
        "shows that <i>Gemini Semantic PC1</i> (η<sup>2</sup> = .580, <i>F</i> = 641.12, Δκ<sub><i>M</i>=5</sub> = .190) "
        "and <i>PC2</i> (η<sup>2</sup> = .392, <i>F</i> = 300.10, Δκ<sub><i>M</i>=5</sub> = .104) capture the primary "
        "lexical-semantic axis, while five structured behavioral indicators, namely <i>detail orientation</i> (η<sup>2</sup> = "
        ".372, ‖<b>β</b>‖<sub>2,<i>M</i>=5</sub> = 2.09), <i>exploration breadth</i> (η<sup>2</sup> = .304), "
        "<i>primary_goal: specific_trip_booking</i> (η<sup>2</sup> = .296), <i>primary_goal: explore_destinations</i> "
        "(η<sup>2</sup> = .284), and <i>decisiveness</i> (η<sup>2</sup> = .280, ‖<b>β</b>‖<sub>2,<i>M</i>=5</sub> = "
        "2.01), drive behavioral persona separation (all <i>p</i> < .001). At the early <i>M</i> = 5 runtime horizon, "
        "<i>information_upfront</i> also carries substantial router weight (‖<b>β</b>‖<sub>2</sub> = 1.85, Δκ = .021) "
        "because front-loaded trip constraints distinguish <i>Decisive Bookers</i> before later turns unfold. Second, "
        "block-level permutation testing on held-out <i>D</i><sub>test</sub> (Table 13, bottom rows; Figure 6, Panel B) "
        "confirms synergistic complementarity: permuting the 20 Gemini PCs reduces held-out κ by .310 at <i>M</i> = 5 "
        "(.674 at <i>M</i> = 9), while permuting the 10 ordinal behavioral scales reduces κ by .133 at <i>M</i> = 5 "
        "(.197 at <i>M</i> = 9). Third, the held-out <i>M</i> = 5 confusion matrix (Figure 6, Panel C) achieves strong "
        f"diagonal recall across <i>Decisive Booker</i> ({cm5[0][0]}/175 = 74.9%), <i>Rigid-Constraint Seeker</i> "
        f"({cm5[2][2]}/127 = 72.4%), and <i>Open Explorer</i> ({cm5[1][1]}/99 = 58.6%, where residual off-diagonal "
        "cases reflect explorers who have not yet switched frames by message 5; by <i>M</i> = 9, diagonal recall reaches "
        f"100.0% [{cm9[0][0]}/175], 98.0% [{cm9[1][1]}/99], and 92.9% [{cm9[2][2]}/127]). Fourth, held-out One-vs-Rest "
        "ROC curves (Figure 6, Panel D) confirm high discrimination at <i>M</i> = 5 across all three classes (AUC = "
        ".83 for <i>Decisive Booker</i>, .85 for <i>Open Explorer</i>, .93 for <i>Rigid-Constraint Seeker</i>; macro "
        "AUC = .871) and near-ideal boundary alignment at <i>M</i> = 9 (macro AUC = .999). <b><i>Feature-importance "
        "handoff (dropped vs. carried forward):</i></b> Because the three schema audit fields (<i>session_outcome</i>, "
        "<i>party_type</i>, and <i>is_unusual</i>) capture post-session outcomes or non-behavioral demographics rather "
        "than early conversational behavior, they are <b>dropped</b> from the clustering matrix, whereas both the 20-d "
        "Gemini semantic prefix block (Δκ = .310) and the 26-d LLM behavioral block (Δκ = .215) prove essential under "
        "permutation testing and are <b>carried forward</b> together in the 46-d <i>Blocks</i> prefix router."
    )
    fi_top_rows = []
    for _, fr in t_fi.head(10).iterrows():
        fi_top_rows.append([
            fr.pretty_name,
            fr.block,
            nz(fr.eta2_gold, 3),
            n2(fr.F_gold, 1),
            f"{n2(fr.beta_l2_m5)} / {n2(fr.beta_l2_m9)}",
            f"{nz(fr.perm_dk_m5, 3)} / {nz(fr.perm_dk_m9, 3)}",
        ])
    for _, br in t_blk.iterrows():
        fi_top_rows.append([
            f"<b>Block: {br.block_label}</b>",
            f"{int(br.n_cols)} columns",
            "N/A",
            "N/A",
            "Joint block",
            f"<b>{nz(br.dk_m5_M, 3)}</b> / <b>{nz(br.dk_m9_M, 3)}</b>",
        ])
    D.table(
        "Feature Importance Assessment of the 46-Dimensional Blocks Representation and Block-Level Permutation Impact",
        [
            "Feature or modality block",
            "Block category",
            "Golden η<sup>2</sup>",
            "ANOVA <i>F</i> (<i>p</i><.001)",
            "Router ‖<b>β</b>‖<sub>2</sub> (<i>M</i>=5 / 9)",
            "Held-Out Perm. Δκ (<i>M</i>=5 / 9)",
        ],
        fi_top_rows,
        note="Top 10 individual features ranked by cluster variance explained η<sup>2</sup> on <i>D</i><sub>gold</sub> (<i>n</i> = 933, <i>df</i> = 2, 930). Held-out permutation Δκ measures mean drop in Cohen's κ across 30–50 random permutations on <i>D</i><sub>test</sub> (<i>n</i> = 401).",
        widths=[1.85, 1.15, 0.68, 0.82, 0.98, 1.02],
        align=["l", "l", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "Feature Importance, Block Permutation Impact, Held-Out Confusion Matrix (M = 5), and Multiclass ROC Curves",
        os.path.join(FIG_FIN, "fig_feature_importance_and_cm.png"),
        note="Evaluated on golden discovery (<i>D</i><sub>gold</sub>, <i>n</i> = 933; Panel A) and held-out test dialogues (<i>D</i><sub>test</sub>, <i>n</i> = 401; Panels B–D).",
    )

    # ------------------------------------------------------------------ Results by Research Question
    D.heading("Results by Research Question", 2)

    # RQ1
    D.heading("RQ1-Identify Stage: Trajectory Clustering, Refined Archetypes, and Prefix Routing", 3)
    D.para(
        "Table 14 summarizes the 159-run clustering benchmark across <i>all-MiniLM-L6-v2</i> (384-d) and "
        "<i>gemini-embedding-001</i> (3,072-d) representations (cluster-number diagnostics, Tukey/Games–Howell post hoc "
        "contrasts, primary profiles, and UMAP projections are in Appendix D, Tables D1, D2, D3, and D4 and Figures D1, D2, and D3). Because each of the 53 "
        f"random seeds draws <i>n</i> = 500 dialogues without replacement from <i>D</i><sub>gold</sub> (<i>n</i> = "
        f"{s1['n_gold']}, a 53.6% finite-population fraction), matched-subsample repeated-measures tests across the 53 "
        "shared seeds and full-<i>D</i><sub>gold</sub> point estimates are reported alongside the one-way ANOVA. On "
        f"MiniLM embeddings, HDBSCAN achieved the highest Silhouette on its retained non-noise subset (<i>M</i> = "
        f"{nz(hd.sil_M, 3)}, <i>SD</i> = {nz(hd.sil_SD, 3)}), followed by <i>K</i>-Means (<i>M</i> = {nz(km.sil_M, 3)}, "
        f"<i>SD</i> = {nz(km.sil_SD, 3)}; full-<i>D</i><sub>gold</sub> Sil = .141, DB = 3.244) and Ward agglomerative "
        f"clustering (<i>M</i> = {nz(ag.sil_M, 3)}, <i>SD</i> = {nz(ag.sil_SD, 3)}), all exceeding the permutation "
        f"baseline ({nz(perm['M'], 3)}; Figure D2). Algorithm differences were highly significant under matched RM-ANOVA, "
        f"<i>F</i>({n2(r1_rm['df1_gg'])}, {n2(r1_rm['df2_gg'])}) = {n2(r1_rm['F'])}, <i>p</i> < .001, "
        f"η<sub><i>p</i></sub><sup>2</sup> = {nz(r1_rm['eta2_p'], 3)}, paired Friedman χ<sup>2</sup>(2) = "
        f"{n2(r1_rm['friedman_chi2'])}, <i>p</i> < .001, one-way ANOVA <i>F</i>({int(an['df1'])}, {int(an['df2'])}) = "
        f"{n2(an['F'])}, <i>p</i> < .001, η<sup>2</sup> = {nz(an['eta2'])}, Welch <i>F</i> = {n2(we['F'])}, and "
        f"Kruskal–Wallis <i>H</i>(2) = {n2(kw['H'])}, <i>p</i> < .001 (with all pairwise Tukey HSD and Games–Howell post hoc contrasts significant at <i>p</i> < .001; Table D2). Replicating on 3,072-d Gemini turn-pooled and "
        f"document embeddings reproduced the exact same ordering (<i>F</i> = {n2(r1gm['G-pooled']['anova']['F'])} and "
        f"{n2(r1gm['G-doc']['anova']['F'])}, both <i>p</i> < .001). Critically, HDBSCAN failed at default settings in "
        f"{r1['hdbscan_default_fail']}/53 runs and discarded <b>{pct(100 * r1['hdbscan_noise_M'])}</b> (MiniLM), "
        f"<b>{pct(100 * r1gm['G-pooled']['hdbscan_noise_M'])}</b> (Gemini turn-pooled), and "
        f"<b>{pct(100 * r1gm['G-doc']['hdbscan_noise_M'])}</b> (Gemini document) of dialogues as unroutable noise. "
        "Because a live travel assistant must route 100% of customer sessions, <i>K</i>-Means (<i>k</i> = 3) was "
        "selected. Golden centroids generalized cleanly to held-out Frames dialogues "
        f"(<i>t</i>({n2(gt['df'], 1)}) = {n2(gt['t'])}, <i>p</i> {pv(gt['p'])}) while confirming domain shift against "
        f"flight-free MultiWOZ 2.2 (<i>t</i>({n2(cc['df'], 1)}) = {n2(cc['t'])}, <i>p</i> < .001; Table D4). "
        "<b><i>RQ1-Identify algorithm handoff (dropped vs. carried forward):</i></b> Although HDBSCAN achieved the highest "
        "Silhouette on its retained subset, it is <b>dropped</b> because rejecting 24.4%–39.1% of live customer "
        "sessions as unroutable noise prevents universal downstream personalization, and Ward agglomerative clustering "
        "is <b>dropped</b> due to lower Silhouette separation and the absence of a native centroid router; "
        "<b>100%-coverage <i>K</i>-Means (<i>k</i> = 3)</b> is therefore <b>carried forward</b> as the clustering engine."
    )
    g_p = r1gm["G-pooled"]
    g_d = r1gm["G-doc"]
    D.table(
        "Cluster Quality by Algorithm and Embedding Family Across 53 Matched Subsample Seeds (159 Runs)",
        ["Representation and algorithm", "<i>n</i> seeds", "Retained (%)", "Silhouette <i>M</i> (<i>SD</i>)", "Davies–Bouldin <i>M</i> (<i>SD</i>)", "Omnibus & matched RM tests (<i>p</i> < .001)"],
        [
            ["MiniLM-L6-v2 (384-d): K-Means (<i>k</i> = 3)", "53", "100.0%", f"{nz(km.sil_M, 3)} ({nz(km.sil_SD, 3)})", f"{n2(km.db_M, 3)} ({n2(km.db_SD, 3)})", f"One-way <i>F</i> = {n2(an['F'])}, η<sup>2</sup> = {nz(an['eta2'])}"],
            ["MiniLM-L6-v2 (384-d): Ward Agglomerative", "53", "100.0%", f"{nz(ag.sil_M, 3)} ({nz(ag.sil_SD, 3)})", f"{n2(ag.db_M, 3)} ({n2(ag.db_SD, 3)})", f"Matched RM <i>F</i> = {n2(r1_rm['F'])}, η<sub><i>p</i></sub><sup>2</sup> = {nz(r1_rm['eta2_p'], 3)}"],
            ["MiniLM-L6-v2 (384-d): HDBSCAN (non-noise)", "53", f"{pct(100 * (1 - r1['hdbscan_noise_M']))}", f"{nz(hd.sil_M, 3)} ({nz(hd.sil_SD, 3)})", f"{n2(hd.db_M, 3)} ({n2(hd.db_SD, 3)})", f"Friedman χ<sup>2</sup> = {n2(r1_rm['friedman_chi2'])}, Welch <i>F</i> = {n2(we['F'])}"],
            ["MiniLM-L6-v2 (384-d): Permutation baseline", "53", "100.0%", f"{nz(perm['M'], 3)} ({nz(perm['SD'], 3)})", "N/A", "Full <i>D</i><sub>gold</sub> KM Sil = .141, DB = 3.244"],
            ["Gemini-001 (3,072-d turn pool): KM / Ward / HDB", "53 × 3", f"100 / 100 / {pct(100 * (1 - g_p['hdbscan_noise_M']))}", f"{nz(g_p['desc']['K-Means']['M'], 3)} / {nz(g_p['desc']['Agglomerative']['M'], 3)} / {nz(g_p['desc']['HDBSCAN']['M'], 3)}", f"{n2(g_p['desc']['K-Means']['DB_M'], 2)} / {n2(g_p['desc']['Agglomerative']['DB_M'], 2)} / {n2(g_p['desc']['HDBSCAN']['DB_M'], 2)}", f"<i>F</i> = {n2(g_p['anova']['F'])}, η<sup>2</sup> = {nz(g_p['anova']['eta2'])}; Kruskal <i>H</i> = {n2(g_p['kruskal']['H'])}"],
            ["Gemini-001 (3,072-d document): KM / Ward / HDB", "53 × 3", f"100 / 100 / {pct(100 * (1 - g_d['hdbscan_noise_M']))}", f"{nz(g_d['desc']['K-Means']['M'], 3)} / {nz(g_d['desc']['Agglomerative']['M'], 3)} / {nz(g_d['desc']['HDBSCAN']['M'], 3)}", f"{n2(g_d['desc']['K-Means']['DB_M'], 2)} / {n2(g_d['desc']['Agglomerative']['DB_M'], 2)} / {n2(g_d['desc']['HDBSCAN']['DB_M'], 2)}", f"<i>F</i> = {n2(g_d['anova']['F'])}, η<sup>2</sup> = {nz(g_d['anova']['eta2'])}; Kruskal <i>H</i> = {n2(g_d['kruskal']['H'])}"],
        ],
        note="Each seed draws <i>n</i> = 500 dialogues without replacement from <i>D</i><sub>gold</sub> (<i>n</i> = 933). HDBSCAN metrics apply only to retained non-noise subsets.",
        widths=[2.15, 0.55, 0.85, 1.05, 0.85, 1.05],
        align=["l", "c", "c", "c", "c", "c"],
        split=True,
    )

    rp = rprof.reindex(ARCH_REF)
    p16 = ctx["full_16_profile"]
    db_r, oe_r, rc_r = rp.loc["Decisive Booker"], rp.loc["Open Explorer"], rp.loc["Rigid-Constraint Seeker"]
    D.para(
        "Auditing the primary whole-dialogue clusters (Table D3) revealed role-player correlation "
        f"(Cramér's <i>V</i> = {nz(ctx['cramer_v'])}) and weak early routing (κ = {nz(kap_prim)}). Evaluating the 46-d "
        "<i>Blocks</i> representation across horizons <i>M</i> ∈ {3, 5, 7, 9, whole} and <i>k</i> ∈ {2, ..., 8} "
        "(Appendix D, Tables D1, D5, D6; Figure D4) proved that <i>M</i> = 9 at <b><i>k</i> = 3</b> achieves the lowest "
        "Davies–Bouldin index (2.647 vs. 2.796 at <i>k</i> = 2 and 2.729–2.784 at <i>k</i> = 4–6), high bootstrap "
        f"stability (<b>ARI = {nz(tr3.loc['9', 'stability_ari'])}</b> in the truncation grid; <b>ARI = "
        f"{nz(a9.loc[1, 'stability_ari'])}</b> with {pct(a9.loc[1, 'core_pct'], 1)} core membership in the ablation), "
        f"and balanced cluster shares (smallest = {pct(rprof['pct'].min(), 1)} ≥ 20% floor). Applying the deterministic "
        "feature-importance centroid rules (Appendix F, Table F1; independent Judge LLM validation role in Appendix G, "
        "Table G1) yields the three refined user archetypes profiled in Table 15: "
        f"<i>Decisive Booker</i> ({pct(db_r.pct, 1)}; decisiveness = {n2(db_r.decisiveness)}, {pct(db_r.goal_booking_pct, 1)} "
        f"booking goal), <i>Open Explorer</i> ({pct(oe_r.pct, 1)}; destination flexibility = "
        f"{n2(oe_r.destination_flexibility)}, exploration breadth = {n2(oe_r.exploration_breadth)}, {n2(oe_r.turns_M)} "
        f"turns), and <i>Rigid-Constraint Seeker</i> ({pct(rc_r.pct, 1)}; low flexibility = "
        f"{n2(rc_r.destination_flexibility)}/{n2(rc_r.date_flexibility)}, {pct(rc_r.no_option_pct, 1)} ending without "
        "a suitable option unless proactive trade-offs are offered). <b><i>RQ1-Identify → RQ2-Personalize stage handoff "
        "(dropped vs. carried forward):</i></b> Because whole-dialogue clusters suffered role-player confounding (<i>V</i> = "
        ".18) and near-chance early routing (κ = .24), the whole-dialogue representation and raw unprojected prefix "
        "routers are <b>dropped</b>; instead, the frozen 46-d <i>Blocks</i> <i>K</i>-Means (<i>k</i> = 3) centroids, the "
        "<i>M</i> = 5 L2 logistic prefix router (70.1% accuracy, κ = .535, ROC-AUC = .871), and the three "
        "archetype-partitioned FAISS <i>IndexFlatIP</i> exemplar sub-indices are <b>carried forward into the "
        "RQ2-Personalize stage</b>."
    )
    t15_rows = [
        ["Golden / Held-out test size, <i>n</i> (%)", *[f"{int(r.n)} ({n2(r.pct, 1)}%) / {int(r1r['test_counts'][a])}" for a, r in rp.iterrows()]],
        ["Dialogue turns / User messages, <i>M</i>", *[f"{n2(r.turns_M)} ({n2(r.turns_SD)}) / {n2(r.user_turns_M)}" for _, r in rp.iterrows()]],
    ]
    for idx_f, (lab_, col_) in enumerate(feat, 1):
        t15_rows.append([f"{idx_f}. {lab_} (1–5 ordinal)", *[n2(r[col_]) for _, r in rp.iterrows()]])
    t15_rows += [
        ["11. Primary goal: explore / book trip (%)", *[f"{n2(r.goal_explore_pct, 1)}% / {n2(r.goal_booking_pct, 1)}%" for _, r in rp.iterrows()]],
        ["12. Secondary goals present (%)", *[f"{n2(p16[a]['has_sec_goal_pct'], 1)}%" for a in ARCH_REF]],
        ["13. Emotional tone: positive / neutral (%)", *[f"{n2(p16[a]['tone_pos_pct'], 1)}% / {n2(p16[a]['tone_neu_pct'], 1)}%" for a in ARCH_REF]],
        ["14. Session outcome (audit): booked / no option (%)", *[f"{n2(r.booked_pct, 1)}% / {n2(r.no_option_pct, 1)}%" for _, r in rp.iterrows()]],
        ["15. Party type (audit): solo or couple (%)", *[f"{n2(p16[a]['party_solo_couple_pct'], 1)}%" for a in ARCH_REF]],
        ["16. Unusual conversation flag (audit, %)", *[f"{n2(p16[a]['unusual_pct'], 1)}%" for a in ARCH_REF]],
        ["Frames wizard task success (%)", *[f"{n2(r.success_pct, 1)}%" for _, r in rp.iterrows()]],
    ]
    D.table(
        "Profiles of the Three Refined User Archetypes Across All 16 Behavioral Schema Fields and Prefix Routing Performance",
        ["Behavioral schema field or routing attribute", *ARCH_REF],
        t15_rows,
        note=f"Golden <i>N</i> = {s1['n_gold']}; held-out <i>N</i> = {s1['n_test']} (χ<sup>2</sup>(2) = "
             f"{n2(r1r['chi_gold_test']['chi2'])}, <i>p</i> = {nz(r1r['chi_gold_test']['p'], 3)}). Fields 1–13 form "
             "the 26-column clustering matrix; Fields 14–16 are audit-only (excluded from clustering). Held-out prefix "
             "routing accuracy (κ, macro ROC-AUC) vs. <i>M</i>=9 reference clusters: <i>M</i>=3: 59.4% (.359, .753); "
             "<i>M</i>=5: 70.1% (.535, .871); <i>M</i>=7: 82.0% (.722, .948); <i>M</i>=9 (boundary consistency): 97.3% (.958, .999).",
        widths=[2.55, 1.32, 1.32, 1.31],
        align=["l", "c", "c", "c"],
        split=True,
    )

    # RQ2
    D.heading("RQ2-Personalize Stage: Cluster-Adaptive Few-Shot Prompting", 3)
    sc_p = r2_prim["results"]["style_cos"]
    wd_p = r2_prim["results"]["words"]
    sc_r = r2_ref["results"]["sbert_style_cos"]
    gc_r = r2_ref["results"]["style_cos"]
    bf_r = r2_ref["results"]["bert_f1"]
    wd_r = r2_ref["results"]["words"]
    we_r = r2_ref["results"]["word_abs_err"]
    p_cs = {p["contrast"]: p for p in sc_r["pairs"]}

    D.para(
        "Table 16 compares the repeated-measures prompting experiment (<i>N</i> = 33 held-out dialogues × 3 conditions = "
        "99 <i>gemini-2.5-flash</i> generations) on primary whole-dialogue archetypes versus refined user archetypes, "
        "and Figure 7 displays the refined distributions (all Holm-adjusted pairwise contrasts are in Appendix E, "
        "Table E3). On coarse primary archetypes with weak routing (39.4%, κ = .24; Figure E2), style convergence was "
        f"null, <i>F</i>({n2(sc_p['anova']['df1_gg'])}, {n2(sc_p['anova']['df2_gg'])}) = {n2(sc_p['anova']['F'])}, "
        f"<i>p</i> = {nz(sc_p['anova']['p_gg'], 3)}. Re-running on the <b>Refined User Archetypes</b> routed via the "
        "five-message <i>Blocks</i> router (70.1% accuracy, κ = .535) <b>rejected <i>H</i><sub>02</sub> (<i>p</i> < .001)</b>: "
        "de-lexicalized SBERT style cosine differed significantly under Greenhouse–Geisser RM-ANOVA, "
        f"<i>F</i>({n2(sc_r['anova']['df1_gg'])}, {n2(sc_r['anova']['df2_gg'])}) = {n2(sc_r['anova']['F'])}, "
        f"<i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = {nz(sc_r['anova']['eta2_partial'])}, and Friedman "
        f"χ<sup>2</sup>(2) = {n2(sc_r['friedman']['chi2'])}, <i>p</i> = {nz(sc_r['friedman']['p'], 3)}. "
        f"<i>Cluster-Adaptive Few-Shot</i> (<i>M</i> = {nz(sc_r['desc']['Cluster-Adaptive Few-Shot'][0], 3)}) "
        f"outperformed both <i>Static Few-Shot</i> ({nz(sc_r['desc']['Static Few-Shot'][0], 3)}, <i>t</i>(32) = "
        f"{n2(p_cs['Cluster-Adaptive Few-Shot vs. Static Few-Shot']['t'])}, <i>p</i><sub>Holm</sub> < .001, "
        f"<i>d<sub>z</sub></i> = {n2(p_cs['Cluster-Adaptive Few-Shot vs. Static Few-Shot']['d_z'])}) and <i>Zero-Shot</i> "
        f"({nz(sc_r['desc']['Zero-Shot'][0], 3)}, <i>p</i><sub>Holm</sub> = "
        f"{nz(p_cs['Cluster-Adaptive Few-Shot vs. Zero-Shot']['p_holm'], 3)}) while cutting pacing error from 10.12 "
        f"(Zero-Shot) and 6.33 (Static) to <b>{n2(we_r['desc']['Cluster-Adaptive Few-Shot'][0])} words</b> "
        f"(<i>F</i> = {n2(we_r['anova']['F'])}, <i>p</i> = {nz(we_r['anova']['p_gg'], 3)}; Friedman <i>p</i> < .001). "
        "Generic semantic metrics (Gemini 3,072-d cosine <i>p</i> = .507; BERTScore F<sub>1</sub> <i>p</i> = .315) "
        "remained invariant, confirming selective calibration of discourse structure and pacing without semantic drift. "
        "<b><i>RQ2-Personalize → RQ3-Govern stage handoff (dropped vs. carried forward):</i></b> Because prompting on "
        "coarse unrefined clusters yielded null style effects (<i>p</i> = .211) and <i>Static Few-Shot</i> degraded "
        "style alignment (.453 vs. .530 <i>Zero-Shot</i>) by injecting cross-persona mismatched examples, both unrefined "
        "prompting and <i>Static Few-Shot</i> are <b>dropped</b>; the validated <b>Refined Cluster-Adaptive Few-Shot</b> "
        "generator (combining <i>M</i> = 5 prefix routing, partitioned FAISS retrieval, and persona pacing directives) "
        "is <b>carried forward into the RQ3-Govern stage</b> alongside <i>Zero-Shot</i> as the unpersonalized factorial "
        "control."
    )
    D.table(
        "Repeated-Measures Comparison of Prompting Strategies on Primary Versus Refined User Archetypes (RQ2)",
        ["Experiment and outcome metric", "Zero-Shot <i>M</i> (<i>SD</i>)", "Static Few-Shot <i>M</i> (<i>SD</i>)", "Cluster-Adaptive <i>M</i> (<i>SD</i>)", "RM-ANOVA <i>F</i> (GG)", "<i>p</i> (GG)", "η<sub><i>p</i></sub><sup>2</sup>"],
        [
            ["Primary archetypes (<i>M</i>=3, κ=.24): Style cosine", f"{nz(sc_p['desc']['Zero-Shot'][0], 3)} ({nz(sc_p['desc']['Zero-Shot'][1], 3)})", f"{nz(sc_p['desc']['Static Few-Shot'][0], 3)} ({nz(sc_p['desc']['Static Few-Shot'][1], 3)})", f"{nz(sc_p['desc']['Cluster-Adaptive Few-Shot'][0], 3)} ({nz(sc_p['desc']['Cluster-Adaptive Few-Shot'][1], 3)})", n2(sc_p["anova"]["F"]), pv_cell(sc_p["anova"]["p_gg"]), nz(sc_p["anova"]["eta2_partial"])],
            ["Primary archetypes: Response length (words)", f"{n2(wd_p['desc']['Zero-Shot'][0], 1)} ({n2(wd_p['desc']['Zero-Shot'][1], 1)})", f"{n2(wd_p['desc']['Static Few-Shot'][0], 1)} ({n2(wd_p['desc']['Static Few-Shot'][1], 1)})", f"{n2(wd_p['desc']['Cluster-Adaptive Few-Shot'][0], 1)} ({n2(wd_p['desc']['Cluster-Adaptive Few-Shot'][1], 1)})", n2(wd_p["anova"]["F"]), pv_cell(wd_p["anova"]["p_gg"]), nz(wd_p["anova"]["eta2_partial"])],
            ["Refined archetypes (<i>M</i>=5, κ=.535): SBERT style cosine", f"{nz(sc_r['desc']['Zero-Shot'][0], 3)} ({nz(sc_r['desc']['Zero-Shot'][1], 3)})", f"{nz(sc_r['desc']['Static Few-Shot'][0], 3)} ({nz(sc_r['desc']['Static Few-Shot'][1], 3)})", f"<b>{nz(sc_r['desc']['Cluster-Adaptive Few-Shot'][0], 3)}</b> ({nz(sc_r['desc']['Cluster-Adaptive Few-Shot'][1], 3)})", n2(sc_r["anova"]["F"]), pv_cell(sc_r["anova"]["p_gg"]), nz(sc_r["anova"]["eta2_partial"])],
            ["Refined archetypes: Gemini 3,072-d style cosine", f"{nz(gc_r['desc']['Zero-Shot'][0], 3)} ({nz(gc_r['desc']['Zero-Shot'][1], 3)})", f"{nz(gc_r['desc']['Static Few-Shot'][0], 3)} ({nz(gc_r['desc']['Static Few-Shot'][1], 3)})", f"{nz(gc_r['desc']['Cluster-Adaptive Few-Shot'][0], 3)} ({nz(gc_r['desc']['Cluster-Adaptive Few-Shot'][1], 3)})", n2(gc_r["anova"]["F"]), pv_cell(gc_r["anova"]["p_gg"]), nz(gc_r["anova"]["eta2_partial"])],
            ["Refined archetypes: Token-level BERTScore F<sub>1</sub>", f"{nz(bf_r['desc']['Zero-Shot'][0], 3)} ({nz(bf_r['desc']['Zero-Shot'][1], 3)})", f"{nz(bf_r['desc']['Static Few-Shot'][0], 3)} ({nz(bf_r['desc']['Static Few-Shot'][1], 3)})", f"{nz(bf_r['desc']['Cluster-Adaptive Few-Shot'][0], 3)} ({nz(bf_r['desc']['Cluster-Adaptive Few-Shot'][1], 3)})", n2(bf_r["anova"]["F"]), pv_cell(bf_r["anova"]["p_gg"]), nz(bf_r["anova"]["eta2_partial"])],
            ["Refined archetypes: Pacing calibration error (words)", f"{n2(we_r['desc']['Zero-Shot'][0], 2)} ({n2(we_r['desc']['Zero-Shot'][1], 2)})", f"{n2(we_r['desc']['Static Few-Shot'][0], 2)} ({n2(we_r['desc']['Static Few-Shot'][1], 2)})", f"<b>{n2(we_r['desc']['Cluster-Adaptive Few-Shot'][0], 2)}</b> ({n2(we_r['desc']['Cluster-Adaptive Few-Shot'][1], 2)})", n2(we_r["anova"]["F"]), pv_cell(we_r["anova"]["p_gg"]), nz(we_r["anova"]["eta2_partial"])],
            ["Refined archetypes: Response length (words)", f"{n2(wd_r['desc']['Zero-Shot'][0], 1)} ({n2(wd_r['desc']['Zero-Shot'][1], 1)})", f"{n2(wd_r['desc']['Static Few-Shot'][0], 1)} ({n2(wd_r['desc']['Static Few-Shot'][1], 1)})", f"{n2(wd_r['desc']['Cluster-Adaptive Few-Shot'][0], 1)} ({n2(wd_r['desc']['Cluster-Adaptive Few-Shot'][1], 1)})", n2(wd_r["anova"]["F"]), pv_cell(wd_r["anova"]["p_gg"]), nz(wd_r["anova"]["eta2_partial"])],
        ],
        note="<i>N</i> = 33 held-out dialogues per experiment (99 generations each). Cluster-Adaptive combines archetype-partitioned FAISS exemplars with a routed pacing directive. GG = Greenhouse–Geisser correction.",
        widths=[2.15, 0.95, 0.95, 0.95, 0.50, 0.50, 0.50],
        align=["l", "c", "c", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "Style Convergence, Archetype Pacing Error, and Reply Length Across Prompting Conditions (RQ2)",
        os.path.join(FIG_FIN, "fig_rq2_refined_results.png"),
        note="<i>N</i> = 33 held-out dialogues across three repeated-measures conditions. Gray lines link paired dialogues.",
    )

    # RQ3
    D.heading("RQ3-Govern Stage: Declarative Policy Governance Versus Adaptive Prompting", 3)
    jr = r3_fin["judge_reliability_flash_vs_pro"]
    c3 = r3_fin["cell_means"]
    D.para(
        "Table 17 and Figure 8 report the 2 × 2 factorial experiment across <i>N</i> = 144 evaluations (36 stratified "
        "held-out dialogues, comprising 18 policy-violating and 18 compliant cases; archival rule audit in Table E4, evaluated across all "
        "four cells, <i>n</i> = 36/cell; dual-judge agreement between <i>gemini-2.5-flash</i> and independent "
        f"<i>gemini-2.5-pro</i> = {pct(100 * jr['raw_agreement'], 1)}, κ = {nz(jr['cohen_kappa'], 3)}, prevalence-adjusted "
        f"bias-adjusted kappa [PABAK] = {nz(jr['pabak'], 3)}; Table C3). Four findings <b>reject <i>H</i><sub>03</sub> "
        "(<i>p</i> < .001)</b>: (1) decomposing <b>Rule Adherence</b> shows that <b>Violation Enforcement Sensitivity</b> "
        "(<i>n</i> = 18 violating cases/cell) jumped from 5.6% under both <i>Rules Off</i> cells to <b>100.0%</b> "
        "(<i>Rules Active × Zero-Shot</i>) and <b>97.2%</b> (<i>Rules Active × Cluster-Adaptive</i>; pooled 98.6%), "
        f"<i>F</i>(1, 68) = {n2(r3_rar_anova['viol_F_rules'])}, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = "
        f"{nz(r3_rar_anova['viol_eta2_rules'], 3)}, while <b>Compliant Acceptance Specificity</b> (<i>n</i> = 18 "
        f"compliant cases/cell) remained statistically invariant (94.4% vs. 88.9%, <i>F</i> = "
        f"{n2(r3_rar_anova['comp_F_rules'])}, <i>p</i> = {nz(r3_rar_anova['comp_p_rules'], 3)}), lifting overall rule "
        f"accuracy from .500 to .944/.931 (<i>F</i>(1, 140) = {n2(r3_a['rule_adherence']['effects']['rules_mode']['F'])}, "
        "<i>p</i> < .001); (2) <b>Exemplar Entity Leakage Rate</b> exhibited a decisive rules × prompting interaction, "
        f"<i>F</i>(1, 140) = {n2(r3_a['leakage_rate']['effects']['interaction']['F'])}, <i>p</i> < .001, "
        f"η<sub><i>p</i></sub><sup>2</sup> = {nz(r3_a['leakage_rate']['effects']['interaction']['eta2_partial'])} "
        f"(HC3 <i>F</i> = {n2(r3_a['leakage_rate']['effects']['interaction']['F_hc3'])}; ART <i>F</i> = "
        f"{n2(r3_a['leakage_rate']['effects']['interaction']['F_art'])}, both <i>p</i> < .001), eliminating the .359 "
        "unguarded leakage rate (20/36 = 55.6% incidence) down to <b>.000 (0/36 incidence; Welch <i>t</i>(35) = 5.90, "
        "Fisher's exact <i>p</i> = 4.68 × 10<sup>−8</sup>)</b>; (3) <b>Slot Coverage F<sub>1</sub></b> rose from "
        f".208/.485 to <b>.977/.952</b> (<i>F</i> = {n2(r3_a['slot_f1']['effects']['rules_mode']['F'])}, <i>p</i> < "
        ".001); and (4) <b>Style Alignment</b> was preserved under active rules (prompting main effect <i>F</i> = "
        f"{n2(r3_a['style_cos']['effects']['prompt_mode']['F'])}, <i>p</i> < .001; Panel D), establishing "
        "<b>Rules Active × Cluster-Adaptive Few-Shot</b> as the unique Pareto-optimal configuration. <b><i>RQ3-Govern → "
        "RQ4-Optimize stage handoff (dropped vs. carried forward):</i></b> Because both <i>Rules Off</i> arms failed to "
        "enforce enterprise booking policies (5.6% violation sensitivity) and unguarded few-shot prompting leaked "
        "foreign exemplar entities in 55.6% of sessions (.359 rate), all unguarded <i>Rules Off</i> configurations are "
        "<b>dropped</b>; the Pareto-optimal <b>Rules Active × Cluster-Adaptive Few-Shot</b> neuro-symbolic architecture "
        "(combining deterministic YAML rule verification, <i>[SLOT]</i> exemplar masking, and persona-routed style "
        "prompts) is <b>carried forward into the RQ4-Optimize stage</b>."
    )
    r3_rows = []
    for row in c3:
        rc_cell = r3_rar_cells[(row["rules_mode"], row["prompt_mode"])]
        r3_rows.append([
            f"{row['rules_mode']} × {row['prompt_mode'].replace(' Few-Shot', '')}",
            str(int(row["n"])),
            f"{nz(row['rule_adherence_M'], 3)} ({nz(row['rule_adherence_SD'], 3)}) | {pct(100 * rc_cell['viol_M'], 1)} / {pct(100 * rc_cell['comp_M'], 1)}",
            f"{nz(row['leakage_rate_M'], 3)} ({nz(row['leakage_rate_SD'], 3)}) / {pct(row['leakage_incidence_pct'], 1)}",
            f"{nz(row['slot_f1_M'], 3)} ({nz(row['slot_f1_SD'], 3)})",
            f"{nz(row['style_cos_M'], 3)} ({nz(row['style_cos_SD'], 3)})",
        ])
    for eff_key, eff_name in [
        ("rules_mode", "ANOVA Main: Rules Mode"),
        ("prompt_mode", "ANOVA Main: Prompting"),
        ("interaction", "ANOVA Int.: Rules × Prompt"),
    ]:
        e_rar = r3_a["rule_adherence"]["effects"][eff_key]
        e_elr = r3_a["leakage_rate"]["effects"][eff_key]
        e_sf1 = r3_a["slot_f1"]["effects"][eff_key]
        e_sty = r3_a["style_cos"]["effects"][eff_key]
        r3_rows.append([
            eff_name,
            "1, 140",
            f"<i>F</i>={n2(e_rar['F'])} ({pv_cell(e_rar['p'])}), η<sub><i>p</i></sub><sup>2</sup>={nz(e_rar['eta2_partial'])}",
            f"<i>F</i>={n2(e_elr['F'])} ({pv_cell(e_elr['p'])}), η<sub><i>p</i></sub><sup>2</sup>={nz(e_elr['eta2_partial'])}",
            f"<i>F</i>={n2(e_sf1['F'])} ({pv_cell(e_sf1['p'])}), η<sub><i>p</i></sub><sup>2</sup>={nz(e_sf1['eta2_partial'])}",
            f"<i>F</i>={n2(e_sty['F'])} ({pv_cell(e_sty['p'])}), η<sub><i>p</i></sub><sup>2</sup>={nz(e_sty['eta2_partial'])}",
        ])
    D.table(
        "Cell Means and 2 × 2 Factorial ANOVA Results for Policy Governance and Prompting (RQ3, N = 144)",
        ["Experimental cell or ANOVA effect", "<i>n</i> / <i>df</i>", "Rule Acc. <i>M</i> (<i>SD</i>) | Sens. / Spec.", "Leakage <i>M</i> (<i>SD</i>) / Inc. %", "Slot F<sub>1</sub> <i>M</i> (<i>SD</i>)", "Style cos <i>M</i> (<i>SD</i>)"],
        r3_rows,
        note="Sens. = violation enforcement sensitivity (<i>n</i> = 18/cell; Rules <i>F</i>(1, 68) = 498.78, <i>p</i> < .001); Spec. = compliant specificity (<i>n</i> = 18/cell; <i>p</i> = .408). Because three of the four leakage cells equal .000, orthogonal +1/−1 Sum contrasts share identical sum of squares (<i>SS</i> = 1.162; OLS <i>F</i> = 34.82, Sum-HC3 <i>F</i> = 33.85, ART Int. <i>F</i> = 2148.81, all <i>p</i> < .001).",
        widths=[1.62, 0.50, 1.38, 1.15, 0.93, 0.92],
        align=["l", "c", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "2 × 2 Factorial Profiles for Rule Adherence, Exemplar Leakage, Slot Coverage F1, and Style Alignment (RQ3)",
        os.path.join(FIG_FIN, "fig_rq3_factorial_results.png"),
        note="<i>N</i> = 144 evaluations (<i>n</i> = 36/cell). Error bars denote 95% confidence intervals.",
    )

    # RQ4
    D.heading("RQ4-Optimize Stage: Multi-Turn Dialogue Turn Economy Across Archetypes", 3)
    pv4 = r4_fin["persona_validation"]
    c4 = r4_fin["cell_means"]
    con4 = {r["archetype"]: r for r in r4_fin["archetype_contrasts"]}
    D.para(
        "Table 18 and Figure 9 present the 2 × 3 between-subjects multi-turn simulation across <b><i>N</i> = 180 unique, "
        "non-overlapping held-out seed dialogues</b> (<i>n</i> = 30 distinct dialogues/cell; human baseline in "
        "Appendix E, Table E5 and Figure E3; blind persona fidelity audit by <i>gemini-2.5-pro</i> = 95.6% accuracy, "
        f"43/45 vs. 33.3% chance, κ = {nz(pv4['cohen_kappa'], 3)}; Table C3). On natural-log-transformed turns to "
        f"quotation agreement, the 2 × 3 ANOVA <b>rejected <i>H</i><sub>04</sub> (<i>p</i> < .001)</b>, revealing "
        f"significant main effects of prompting, <i>F</i>(1, 174) = {n2(r4_a['log_turns']['effects']['prompt_mode']['F'])}, "
        f"<i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = "
        f"{nz(r4_a['log_turns']['effects']['prompt_mode']['eta2_partial'])}, and archetype, <i>F</i>(2, 174) = "
        f"{n2(r4_a['log_turns']['effects']['target_archetype']['F'])}, <i>p</i> = "
        f"{nz(r4_a['log_turns']['effects']['target_archetype']['p'], 3)}, plus a <b>significant prompting × archetype "
        f"interaction</b>, <i>F</i>(2, 174) = {n2(r4_a['log_turns']['effects']['interaction']['F'])}, <i>p</i> < .001, "
        f"η<sub><i>p</i></sub><sup>2</sup> = {nz(r4_a['log_turns']['effects']['interaction']['eta2_partial'])} "
        f"(HC3 <i>F</i> = {n2(r4_a['log_turns']['effects']['interaction']['F_hc3'])}; ART <i>F</i> = "
        f"{n2(r4_a['log_turns']['effects']['interaction']['F_art'])}, both <i>p</i> < .001). Pairing the <i>Verified "
        "Informed Slot Ledger</i> with archetype trade-off policies compressed turns sharpest for <b>Rigid-Constraint "
        "Seekers</b> (−42.7%, 8.73 → 5.00 turns, Welch <i>t</i><sub>log</sub> = "
        f"{n2(con4['Rigid-Constraint Seeker']['t_welch_log'])}, <i>d</i> = "
        f"{n2(con4['Rigid-Constraint Seeker']['cohen_d'])}) by proactively pitching both 4-star exact-date and 5-star "
        "flexible-date alternatives when exact-date 5-star inventory exceeded budget, followed by <b>Decisive Bookers</b> "
        f"(−34.2%, 7.60 → 5.00 turns, <i>d</i> = {n2(con4['Decisive Booker']['cohen_d'])}) and <b>Open Explorers</b> "
        f"(−29.5%, 7.47 → 5.27 turns, <i>d</i> = {n2(con4['Open Explorer']['cohen_d'])}). Reaching 5.00 turns "
        "(<i>SD</i> = 0.00) reflects the deterministic 5-turn protocol floor (<i>U1 → A1 → U2 → A2 → U3</i> once budget "
        "is confirmed), which HC3, ART, and Mann–Whitney <i>U</i> tests accommodate cleanly. Redundant Elicitation Rate "
        "dropped from .194 (DB), .061 (OE), and .072 (RCS) in Zero-Shot to <b>.000</b> across all archetypes "
        f"(<i>F</i>(1, 174) = {n2(r4_a['rer']['effects']['prompt_mode']['F'])}, <i>p</i> < .001). <b><i>RQ4-Optimize "
        "stage operational completion (dropped vs. deployed):</i></b> Because memoryless <i>Zero-Shot</i> prompting "
        "re-asked already-stated slots in 10.9% of turns and required 7.93 turns on average (8.73 turns for "
        "<i>Rigid-Constraint Seekers</i>), static memoryless prompting is <b>dropped</b>; cascading the "
        "<b>RQ1-Identify</b> prefix router, <b>RQ2-Personalize</b> archetype-adaptive prompting, <b>RQ3-Govern</b> "
        "YAML rule verification, and the <b>RQ4-Optimize</b> <i>Verified Informed Slot Ledger</i> with persona "
        "trade-off policies completes the four-stage <b>RQ1-Identify → RQ2-Personalize → RQ3-Govern → RQ4-Optimize</b> "
        "progression and is <b>carried forward into production microservice deployment (Section 6)</b>."
    )
    r4_rows = []
    for a in ARCH_REF:
        z_row = next(r for r in c4 if r["target_archetype"] == a and r["prompt_mode"] == "Zero-Shot")
        c_row = next(r for r in c4 if r["target_archetype"] == a and r["prompt_mode"] == "Cluster-Adaptive Few-Shot")
        cn = con4[a]
        r4_rows.append([
            f"{a}: Zero-Shot (<i>n</i> = 30)",
            f"{n2(z_row['turns_M'])} ({n2(z_row['turns_SD'])})",
            f"{n2(z_row['log_turns_M'], 3)} ({n2(z_row['log_turns_SD'], 3)})",
            f"{nz(z_row['rer_M'], 3)} ({nz(z_row['rer_SD'], 3)})",
            "N/A",
            "N/A",
        ])
        r4_rows.append([
            f"{a}: Cluster-Adaptive (<i>n</i> = 30)",
            f"<b>{n2(c_row['turns_M'])}</b> ({n2(c_row['turns_SD'])})",
            f"{n2(c_row['log_turns_M'], 3)} ({n2(c_row['log_turns_SD'], 3)})",
            f"<b>{nz(c_row['rer_M'], 3)}</b> ({nz(c_row['rer_SD'], 3)})",
            f"−{n2(cn['turn_reduction_turns'])} (−{pct(cn['turn_reduction_pct'], 1)})",
            f"<i>t</i>={n2(cn['t_welch_log'])} (< .001), <i>d</i>={n2(cn['cohen_d'])}",
        ])
    for eff_key, eff_name in [
        ("prompt_mode", "ANOVA Main: Prompting"),
        ("target_archetype", "ANOVA Main: Archetype"),
        ("interaction", "ANOVA Int.: Prompt × Arch."),
    ]:
        e_tt = r4_a["total_turns"]["effects"][eff_key]
        e_lt = r4_a["log_turns"]["effects"][eff_key]
        e_rr = r4_a["rer"]["effects"][eff_key]
        df_s = f"{int(e_lt['df1'])}, {int(e_lt['df2'])}"
        r4_rows.append([
            f"{eff_name} (<i>df</i>={df_s})",
            f"<i>F</i>={n2(e_tt['F'])} ({pv_cell(e_tt['p'])}), η<sub><i>p</i></sub><sup>2</sup>={nz(e_tt['eta2_partial'])}",
            f"<i>F</i>={n2(e_lt['F'])} ({pv_cell(e_lt['p'])}), η<sub><i>p</i></sub><sup>2</sup>={nz(e_lt['eta2_partial'])}",
            f"<i>F</i>={n2(e_rr['F'])} ({pv_cell(e_rr['p'])}), η<sub><i>p</i></sub><sup>2</sup>={nz(e_rr['eta2_partial'])}",
            f"HC3 <i>F</i><sub>log</sub>={n2(e_lt['F_hc3'])} ({pv_cell(e_lt['p_hc3'])})",
            f"ART <i>F</i><sub>log</sub>={n2(e_lt['F_art'])} ({pv_cell(e_lt['p_art'])})",
        ])
    D.table(
        "Cell Means, Archetype Contrasts, and 2 × 3 Factorial ANOVA Results for Multi-Turn Turn Economy (RQ4, N = 180)",
        ["Archetype × Prompting cell or ANOVA effect", "Total turns <i>M</i> (<i>SD</i>)", "Log turns <i>M</i> (<i>SD</i>)", "RER <i>M</i> (<i>SD</i>)", "Turn cut / HC3 check", "Welch contrast / ART check"],
        r4_rows,
        note="<i>N</i> = 180 distinct held-out seed dialogues (<i>n</i> = 30/cell; 100.0% goal completion). Protocol minimum = 5.00 turns (<i>U1 → A1 → U2 → A2 → U3</i>).",
        widths=[1.80, 0.92, 0.92, 0.86, 1.00, 1.00],
        align=["l", "c", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "Dialogue Turn Economy and Redundant Elicitation Rate by User Archetype and Prompting Strategy (RQ4)",
        os.path.join(FIG_FIN, "fig_rq4_turn_economy_results.png"),
        note="<i>N</i> = 180 simulations (<i>n</i> = 30/cell). Panel A: Mean turns to quotation agreement vs. 5.0-turn floor. Panel B: Redundant Elicitation Rate (RER).",
    )

    # ------------------------------------------------------------------ Overall Interpretation & Practical Significance
    D.heading("Overall Interpretation", 2)
    D.para(
        "Synthesizing the empirical cascade across the four stages, <b>RQ1-Identify, RQ2-Personalize, RQ3-Govern, and "
        "RQ4-Optimize</b>, demonstrates that business optimization in multi-turn conversational AI is achieved not by "
        "any single isolated technique, but by selectively pruning non-viable methods at each stage boundary and "
        "transferring only validated causal artifacts forward. First, the <b>RQ1-Identify → RQ2-Personalize stage "
        "transition proves that downstream personalization is bounded by upstream feature representation and routing "
        "fidelity</b>: dropping noise-rejecting HDBSCAN (39.1% noise) and outcome-confounded whole-dialogue clusters "
        "(κ = .24, which produced null RQ2 style effects, <i>p</i> = .211) in favor of full-coverage <i>K</i>-Means "
        "(<i>k</i> = 3) on the feature-importance-pruned 46-d <i>Blocks</i> prefix representation (Δκ = .310 semantic + "
        ".215 behavioral; <i>M</i> = 5 routing κ = .535, ROC-AUC = .871) was the decisive prerequisite that unlocked "
        "significant <b>RQ2-Personalize</b> style convergence (<i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = "
        ".234) and pacing calibration (3.87 words, <i>p</i> = .007). Second, the <b>RQ2-Personalize → RQ3-Govern stage "
        "transition proves that stylistic prompting and symbolic governance are functionally orthogonal yet "
        "protectively interactive</b>: dropping Static Few-Shot and unguarded prompting while pairing the "
        "<b>RQ2-Personalize</b> cluster-adaptive generator with the YAML rule engine and <i>[SLOT]</i> masking "
        "preserved persona style (<i>F</i> = 24.00) while driving policy sensitivity from 5.6% to 98.6% "
        "(<i>F</i> = 498.78), Slot F<sub>1</sub> to .952, and exemplar entity leakage from .359 to .000 (interaction "
        "<i>F</i> = 34.82). Third, the <b>RQ3-Govern → RQ4-Optimize stage transition proves that business turn economy "
        "emerges from the complete cascade</b>: combining the <b>RQ1-Identify</b> router, <b>RQ2-Personalize</b> "
        "adaptive pacing, and <b>RQ3-Govern</b> rule-verified slot ledger with persona trade-off policies eliminated "
        "redundant asks (.109 → .000) and compressed negotiation turns by 29.5%–42.7%, peaking for "
        "<i>Rigid-Constraint Seekers</i> (−42.7%, 8.73 → 5.00 turns)."
    )

    D.heading("Practical Significance", 2)
    D.para(
        "In operational decision-making for OTAs, tour operators, and hotel contact centers, these findings provide an "
        "immediately actionable deployment blueprint. In an illustrative production volume of 1,000,000 monthly package "
        "inquiries, achieving the simulated 35.8% average turn compression (7.93 → 5.09 turns, saving 2.84 turns per "
        "session) eliminates ~2.84 million LLM generation calls per month, cutting cloud inference cost and cumulative "
        "user wait time by roughly one-third. Simultaneously, driving redundant slot re-asking from 10.9% to 0.0%, "
        "eliminating foreign price/hotel leakage (55.6% → 0.0% incidence), and enforcing 98.6% of visa, passport, "
        "occupancy, and discount rules before response transmission directly mitigates regulatory liability and "
        "customer booking abandonment."
    )

    # ================================================================== 6. IMPLEMENTATION AND USER BENEFIT
    D.heading("Implementation and User Benefit", 1)
    D.heading("Deployment Approach", 2)
    D.para(
        "The validated codebase (<i>src/final_pipeline/</i>) packages into a stateless containerized Python 3.11 and "
        "FastAPI microservice deployable on cloud Kubernetes pods or serverless containers. At startup, the service "
        "loads the frozen golden <i>PCA-20</i> projection matrix, <i>Blocks</i> scalers, L2 logistic router weights, "
        "three in-memory <i>faiss-cpu</i> <i>IndexFlatIP</i> archetype sub-indices (< 15 megabytes [MB] of random-access "
        "memory [RAM], < 2 ms query latency), and <i>rules/rules_enterprise.yaml</i> (< 1 ms evaluation latency). All "
        f"random seeds (seed = 42) and JSONL caches are versioned at {REPO} (see Appendix A, Tables A1 and A2 for the "
        "repository artifact inventory and single-command replication pipeline, and Appendix B, Table B1 for the "
        "completed 10-week project execution schedule and milestone log); full offline reproduction from cached "
        "responses completes in under 4 minutes on a standard 8-core laptop CPU at $0 application programming interface "
        "(API) cost, while cold regeneration of all ~8,900 Gemini 2.5 Flash/Pro calls completes in ~35 minutes for "
        "under $4.50 USD."
    )

    D.heading("System Integration", 2)
    D.para(
        "Within an enterprise travel stack, the microservice sits as an orchestration layer between the customer-facing "
        "WebSocket chat/voice gateway, the customer relationship management (CRM) lead store, and the Global "
        "Distribution System (GDS) or central reservation system (CRS) inventory API. Active sessions persist the "
        "canonical <i>DialogueTrajectory</i> and <i>Verified Informed Slot Ledger</i> in a low-latency Redis key–value "
        "cache keyed by session and CRM <i>Opportunity_ID</i>, while marketing and compliance teams update promotional "
        "caps or visa lead windows directly in <i>rules_enterprise.yaml</i> without retraining any neural weights."
    )

    D.heading("User Interaction", 2)
    D.para(
        "End users interact through natural conversational text or voice-to-text turns in web, mobile app, or messaging "
        "channels. Behind the interface, Turns 1–3 use the Verified Informed Slot Ledger to capture stated constraints "
        "without repeat questions; once opening turns accumulate, <i>RefinedArchetypeRouter</i> classifies the shopper's "
        "persona, retrieves slot-masked exemplars, runs deterministic Tier-2 compliance checks, and streams back "
        "persona-calibrated package cards, transparent policy advisories, or one-click quotation confirmations."
    )

    D.heading("Benefits to Users", 2)
    D.para(
        "The system delivers measurable operational, financial, and strategic benefits across three user groups: "
        "(1) <i>travelers</i> experience shorter, non-repetitive consultations matched to their shopping style with "
        "upfront transparency on visa and passport requirements; (2) <i>human travel consultants</i> receive pre-qualified, "
        "policy-verified structured slot ledgers when complex itineraries escalate, cutting manual intake handling "
        "time; and (3) <i>OTA and hospitality executives</i> lower LLM token expenditure by ~35%, prevent hallucinated "
        "discount or fare commitments, and audit every policy decision deterministically."
    )

    D.heading("Example Use Case", 2)
    D.para(
        "Consider a traveler entering an OTA portal and stating: <i>'Need a 10-day vacation package from Chicago to "
        "Tokyo departing in 10 days for 2 adults with a 5-star hotel under $2,200.'</i> A conventional static chatbot "
        "sequentially re-asks trip duration or party size and overlooks the international visa window. Under the "
        "deployed neuro-symbolic assistant: (1) the <i>Verified Informed Slot Ledger</i> locks all five stated Tier-1 "
        "slots against re-asking (RER = 0.0%); (2) <i>RefinedArchetypeRouter</i> identifies the tight fixed-date/5-star "
        "ceiling signature of a <i>Rigid-Constraint Seeker</i>; (3) <i>DeclarativeRuleEngine</i> triggers "
        "<i>RULE_VISA_LEAD_TIME</i> (10 days < 15-day minimum) and detects that the exact-date 5-star package ($2,596) "
        "exceeds $2,200; and (4) in a concise 14-word-norm reply, the assistant flags the 15-day visa requirement while "
        "presenting both an exact-date 4-star package ($1,936) and a +6-day shifted 5-star package ($2,068) that clears "
        "both the visa rule and the $2,200 budget, reaching quotation agreement in 5 total turns with zero compliance risk."
    )

    # ================================================================== 7. LIMITATIONS AND FURTHER IMPROVEMENTS
    D.heading("Limitations and Further Improvements", 1)
    D.heading("Limitations", 2)
    D.lead_para(
        "Data limitations",
        "First, Microsoft Frames (El Asri et al., 2017) was collected with instructed Wizard-of-Oz participants rather "
        "than live revenue-bearing OTA checkout traffic, and neither Frames nor MultiWOZ 2.2 records natural Tier-2 "
        "visa, passport, or promotional-discount attributes (0.0% archival completeness in Table E1), necessitating "
        "controlled synthetic Tier-2 state injection in RQ3. Second, both corpora are English-only single-session "
        "transcripts and therefore do not capture multilingual code-switching or multi-day repeat customer callbacks.",
    )
    D.lead_para(
        "Model and methodological limitations",
        "First, modest <i>K</i>-Means Silhouette scores (.094 on 46-d <i>Blocks</i>; .147–.161 on MiniLM/Gemini) show "
        "that traveler personas span a continuous manifold rather than disjoint clusters, and prefix routing κ (.535 at "
        "<i>M</i> = 5; .958 boundary consistency at <i>M</i> = 9) is measured against unsupervised <i>M</i> = 9 "
        "<i>K</i>-Means reference labels rather than human-annotated persona ground truth. Second, moderate routing "
        "accuracy requires 5 user messages, leaving Turn 1 cold-start routing noisy. Third, RQ2, RQ3, and RQ4 evaluate "
        "combined operational packages (exemplars + directive in RQ2; YAML rules + [SLOT] masking + regex sanitizer in "
        "RQ3; slot ledger + persona trade-off policy in RQ4) rather than full sub-component ablations. Fourth, RQ4 uses "
        "cooperative LLM user simulators (validated for within-simulation persona fidelity at 95.6%, κ = .933) and a "
        "5-turn protocol floor (<i>M</i> = 5.00, <i>SD</i> = 0.00 in two cells).",
    )

    D.heading("Impact of Limitations", 2)
    D.para(
        "These limitations bound internal interpretation and external generalizability in specific, quantifiable ways: "
        "(a) continuous cluster boundaries mean ~25.2% of boundary shoppers sit near Voronoi hyperplanes where hard "
        "single-cluster assignment can misroute mixed behaviors; (b) bundled treatments establish the efficacy of each "
        "integrated stage but prevent attributing exact variance shares to exemplars versus directives without follow-up "
        "ablation; and (c) cooperative simulators and the 5-turn floor mean that the 29.5%–42.7% turn reductions "
        "represent an upper-bound controlled benchmark relative to noisy production traffic where users abandon chats "
        "due to exogenous shocks (such as leave denial or competitor browsing)."
    )

    D.heading("Future Improvements", 2)
    D.para(
        "Immediate methodological improvements include: (1) executing orthogonal sub-component ablations, expanding RQ2 "
        "to a 5-arm design crossing Exemplar Source (None / Static / Archetype-Partitioned) with Pacing Directive "
        "(Off / On) at <i>N</i> ≥ 60, separating pre-generation [SLOT] masking from post-generation regex sanitization "
        "in RQ3, and crossing the Slot Ledger (Off / On) with Persona Policy (Generic / Adaptive) in a 2 × 2 × 3 RQ4 "
        "experiment; (2) introducing <b>hierarchical context × behavior clustering (<i>C</i> × <i>K</i> = 24–36 "
        "micro-clusters)</b> over situational trip stakes (<i>party_type</i>, <i>budget_stakes</i>, <i>lead_window</i>) "
        "using top-15 parent FAISS retrieval with contextual metadata back-off; and (3) replacing hard <i>K</i>-Means "
        "routing with <b>soft-mixture exemplar quotas</b> and <b>turn-by-turn Bayesian posterior tracking</b> "
        "<i>P</i>(<i>z<sub>t</sub></i> | <i>u</i><sub>1..<i>t</i></sub>) to handle boundary users and mid-chat price shocks."
    )

    D.heading("Future Scope", 2)
    D.para(
        "For broader doctoral and enterprise extension across real-world tour operators, where customers rarely book in "
        "a single chat but instead engage across <b>4–5 chats and calls under a shared CRM <i>Opportunity_ID</i></b> and "
        "may abandon final payment for exogenous reasons, future research will extend this framework in four directions: "
        "(1) replacing noisy single-chat <i>Turns-to-Booking</i> with controllable multi-session metrics, namely <b>Turns-to-Lead "
        "(TTL)</b> on Call 1, per-session <b>Turns-to-Quotation (TTQ<sub><i>s</i></sub>)</b> across Calls 2–5, and "
        "<b>Cross-Session Excess Turns (CSET = Σ<sub><i>s</i></sub>[<i>T<sub>s</sub></i> − <i>T<sub>s</sub></i><sup>min</sup>])</b> "
        "modeled via linear mixed-effects models and right-censored Markov transitions across persistent <i>Cold → Warm "
        "→ Hot</i> lead states (pre-loading prior-call slot ledgers for 0.0% cross-session RER); (2) expanding FAISS "
        "into a <b>3 × 6 (Archetype × Call Stages <i>a–f</i>: Opening, Mandatory Slots, Positioning, Negotiation, "
        "Compliance, Closure)</b> lookup matrix; (3) indexing <b>200+ regional packages by Unique Selling Propositions "
        "(USPs)</b> queried via an information-gain question tree (<i>seniors, children, breakfast, sightseeing tempo, "
        "occasion</i>); and (4) pairing FAISS style cosine with a <b>Historical Turn-Economy Database (<i>Turn-Q DB</i>)</b> "
        "and constrained offline-to-online reinforcement learning under live multilingual OTA A/B testing."
    )

    # ================================================================== REFERENCES
    D.heading("References", 1, new_page=True)
    for ref in REFERENCES:
        D.reference(ref)

    # ================================================================== APPENDICES A–G
    # Appendix A
    D.heading("Appendix A", 1, new_page=True)
    D.heading("Repository Structure, Replication Guide, and Raw Source Schema", 1, toc=False)
    D.para(
        f"All code, data schemas, cached LLM outputs, and report builders are available at {REPO}. Table A1 outlines "
        "the repository directory structure, Table A2 lists the exact shell commands that reproduce every table and "
        "figure, and Table A3 provides Part A (raw source fields) and Part B (canonical schema fields) of the data "
        "dictionary."
    )
    D.table(
        "Repository Structure and Artifact Inventory",
        ["Directory or file path", "Contents and analytical purpose"],
        [
            ["data/raw/", "Downloaded Microsoft Frames (1,369 dialogues) and MultiWOZ 2.2 corpora (excluded from Git)"],
            ["data/canonical/", "Normalized two-tier Pydantic dialogue trajectories (canonical_corpus.jsonl)"],
            ["data/interim/", "Cleaned samples, partitions, embeddings, primary/refined archetypes, LLM annotations, and RQ1/RQ2 JSON summaries"],
            ["data/final/", "Cached Gemini 2.5 Flash/Pro JSONL responses, feature/router diagnostics, and scored CSV/JSON results for RQ2–RQ4"],
            ["src/canonical_schema.py, src/ingestion.py", "Pydantic two-tier data models and corpus parsers"],
            ["src/rule_engine.py, rules/rules_enterprise.yaml", "Deterministic declarative policy engine and YAML rule definitions"],
            ["src/final_pipeline/", "Reproducible pipeline scripts for Steps 0–5 (power, cleaning, RQ1 clustering/refined archetypes, router, RQ2–RQ4, feature importance, & 300-DPI figures)"],
            ["src/report/, src/build_final_report.py", "APA 7 Word/PDF document generator with automated cross-reference, word-count, and TOC pagination verification"],
            ["notebooks/01_.. to 05_..", "Five executed Jupyter notebooks covering EDA, RQ1, RQ2, RQ3, and RQ4"],
            ["outputs/interim/, outputs/final/", "All CSV summary tables and 1:1 6.5-inch 300-DPI PNG figures"],
            ["final/", "Submission-ready QM_640_Final_Report_Sandeep_Surnella.docx and .pdf"],
        ],
        widths=[2.45, 4.05],
        align=["l", "l"],
        label="A1",
        split=True,
    )
    D.table(
        "End-to-End Replication Commands",
        ["Pipeline stage", "Command (run from repository root with .venv active)", "Outputs produced"],
        [
            ["0. Power analysis", "python src/final_pipeline/step0_sample_size.py", "Table 8"],
            ["1. Cleaning & univariate EDA", "python src/final_pipeline/step1_prepare_data.py", "Tables 5, 6, E1"],
            ["2. Primary RQ1 clustering", "python src/final_pipeline/step2_rq1_clustering.py", "Table 14; Tables D1–D4; Figure D3"],
            ["2b–2i. Sensitivity & refined", "python src/final_pipeline/step2g_rq1_truncation.py; step2h_rq1_ablation.py; step2i_rq1_refined_archetypes.py", "Table 15; Tables C1–C2, D5–D6, E5, F1"],
            ["3. Prefix routing harness", "python src/final_pipeline/test_step1_harness.py", "Table 15 routing diagnostics"],
            ["4. Refined RQ2 experiment", "python src/final_pipeline/step2_rq2_refined.py --execute", "Table 16; Table E3"],
            ["5. RQ3 2×2 governance exp.", "python src/final_pipeline/step3_rq3_experiment.py --execute", "Table 17; Tables C3, G1"],
            ["6. RQ4 2×3 turn-economy sim.", "python src/final_pipeline/step4_rq4_simulation.py --execute", "Table 18; Tables C3, G1"],
            ["7. Feature importance & figs.", "python src/final_pipeline/step5_figures_and_eda.py", "Tables 6, 7, 11–13, E2; Figures 1–9, D1, D2, D4, E1–E3"],
            ["8. Compile Final Report", "python src/build_final_report.py", "final/QM_640_Final_Report_Sandeep_Surnella.docx & .pdf"],
        ],
        note="All random seeds are fixed at 42. Cached JSONL responses allow full offline execution without external API calls.",
        widths=[1.45, 3.15, 1.90],
        align=["l", "l", "l"],
        label="A2",
        split=True,
    )
    D.table(
        "Data Dictionary, Parts A and B: Raw Corpus Fields and Canonical Schema Mapping",
        ["Source / Layer", "Field name", "Data type (Unit)", "Description and mapping role"],
        [
            ["Frames (Raw)", "id, user_id, wizard_id", "String (ID)", f"Unique dialogue ID and role-player IDs ({ctx['n_users']} users, {ctx['n_wizards']} wizards)"],
            ["Frames (Raw)", "turns[].author, text, timestamp", "String / Float (ms)", "Speaker (user or wizard), raw utterance text, and Unix timestamp"],
            ["Frames (Raw)", "turns[].labels.acts[].name, args", "List / Key–Value", "Dialogue act tags (inform, request, offer, switch_frame) and slot–value pairs"],
            ["Frames (Raw)", "labels.wizardSurveyTaskSuccessful, userSurveyRating", "Boolean / Float (1–5)", "Wizard task completion flag and user satisfaction rating"],
            ["MultiWOZ (Raw)", "dialogue_id, services", "String / List", "Unique dialogue ID and active service domains (hotel, train, taxi, attraction)"],
            ["MultiWOZ (Raw)", "turns[].speaker, utterance, frames[].state", "String / Dict", "Speaker (USER or SYSTEM), utterance text, and turn-level slot state dictionary"],
            ["Canonical (Tier 1)", "origin_city, destination_city, accommodation_tier", "String (City / Tier)", "Normalized origin, destination, and hotel star rating or category"],
            ["Canonical (Tier 1)", "departure_date, return_date, duration_nights", "String (Date) / Int (nights)", "Normalized trip dates and length of stay in nights"],
            ["Canonical (Tier 1)", "traveler_count_adults, traveler_count_children, budget_amount", "Int (persons) / Float (USD)", "Party composition and numeric budget ceiling in US dollars"],
            ["Canonical (Tier 2)", "visa_processing_window_days, passport_expiry_months", "Int (days / months)", "Departure lead window (days) and remaining passport validity (months)"],
            ["Canonical (Tier 2)", "package_type, sharing_basis, discount_applied_percentage", "String / Float (%)", "Package class (FIT or Group), room occupancy, and promotional discount (%)"],
        ],
        widths=[1.20, 2.05, 1.15, 2.10],
        align=["l", "l", "l", "l"],
        label="A3",
        split=True,
    )

    # Appendix B
    D.heading("Appendix B", 1, new_page=True)
    D.heading("Ten-Week Project Schedule and Milestone Completion Log", 1, toc=False)
    D.para(
        "Table B1 documents the completed 10-week execution schedule aligned with QM640 course milestones "
        "(referenced in the Repository & Reproducibility overview and Section 6)."
    )
    D.table(
        "Ten-Week Project Schedule and Milestone Completion Status",
        ["Week", "QM640 course topic", "Completed project tasks and deliverables", "Status"],
        [
            ["1", "Define research problem & topic", "Business & technical problem statements finalized; GitHub repository initialized; Frames & MultiWOZ 2.2 ingested", "Complete"],
            ["2", "Synopsis draft", "Four research questions, formal hypotheses, and two-tier Pydantic schema defined", "Complete"],
            ["3", "Literature search & data collection", "30 sources synthesized across 14-row relevance matrix; canonical corpus parsed (<i>N</i> = 2,833 analytic)", "Complete"],
            ["4", "Objectives & hypotheses", "Data quality audit, univariate/outcome/bivariate/multivariate EDA, noncentral-<i>F</i> power analysis, and primary RQ1 clustering", "Complete"],
            ["5", "Research design & methodology", "Interim report submitted; primary RQ2 experiment (99 calls) and RQ1 sensitivity/truncation grid (Steps 2b–2i) completed", "Complete"],
            ["6", "Data analysis plan", "Built RefinedArchetypeRouter, feature-importance & Train/CV/Test ROC-AUC diagnostics; repeated RQ2 on refined archetypes (<i>p</i> < .001)", "Complete"],
            ["7", "Data analysis plan execution", "Executed RQ3 2 × 2 factorial experiment (<i>N</i> = 144) and dual-LLM judge reliability audit (<i>gemini-2.5-pro</i>, κ = .917)", "Complete"],
            ["8", "Data analysis assessment", "Executed RQ4 2 × 3 multi-turn simulation (<i>N</i> = 180), persona fidelity validation (95.6%, κ = .933), and HC3/ART checks", "Complete"],
            ["9", "Refinement & documentation", "Regenerated 1:1 6.5-inch 300-DPI figures, confusion matrix, ROC curves, and synchronized notebooks", "Complete"],
            ["10", "Document results & findings", "Compiled, audited, and exported submission-ready Final Report (.docx and .pdf)", "Complete"],
        ],
        widths=[0.55, 1.65, 3.40, 0.90],
        align=["c", "l", "l", "c"],
        label="B1",
        split=True,
    )

    # Appendix C
    D.heading("Appendix C", 1, new_page=True)
    D.heading("LLM Behavioral Annotation Codebook, Reliability, and Dual-Judge Validation", 1, toc=False)
    D.para(
        "Table C1 defines all 16 structured fields of the LLM behavioral codebook (<i>UserBehaviour</i> in "
        "<i>step2e_llm_user_annotation.py</i>: 10 ordinal 1–5 rating scales, 3 categorical goal/tone clustering fields, "
        "and 3 audit-only fields excluded from clustering; see also Appendix B, Table B1 for milestone sequence), "
        "Table C2 reports test–retest reliability across all 16 fields and criterion validity against ground-truth "
        "Frames dialogue acts, and Table C3 summarizes the cross-model dual-judge reliability in RQ3 and simulator "
        "persona validation in RQ4."
    )
    D.table(
        "LLM Behavioral Annotation Codebook (All 16 Structured Schema Fields)",
        ["# & Schema field", "Scale & role", "Operational definition and scale anchors"],
        [
            ["1. destination_flexibility", "Ordinal 1–5 (Cluster)", "1 = insists on one fixed destination; 5 = open to any destination recommendation"],
            ["2. date_flexibility", "Ordinal 1–5 (Cluster)", "1 = fixed travel dates; 5 = wide date window or completely flexible timing"],
            ["3. exploration_breadth", "Ordinal 1–5 (Cluster)", "1 = evaluates a single option; 5 = actively compares multiple destinations, hotels, or dates"],
            ["4. decisiveness", "Ordinal 1–5 (Cluster)", "1 = hesitant or leaves undecided; 5 = commits quickly and firmly once a matching offer is shown"],
            ["5. detail_orientation", "Ordinal 1–5 (Cluster)", "1 = asks no package details; 5 = probes amenities, star ratings, flight times, and inclusions"],
            ["6. revision_tendency", "Ordinal 1–5 (Cluster)", "1 = never modifies initial constraints; 5 = repeatedly shifts dates, destinations, or budgets"],
            ["7. question_asking", "Ordinal 1–5 (Cluster)", "1 = passive responder; 5 = asks frequent clarifying and comparison questions"],
            ["8. politeness", "Ordinal 1–5 (Cluster)", "1 = curt or abrupt; 5 = consistently courteous and appreciative"],
            ["9. price_sensitivity", "Ordinal 1–5 (Cluster)", "1 = price never mentioned or irrelevant; 5 = price/budget dominates every decision"],
            ["10. information_upfront", "Ordinal 1–5 (Cluster)", "1 = reveals constraints gradually across turns; 5 = states nearly all trip constraints in opening message"],
            ["11. primary_goal", "Categorical (Cluster)", "6 classes: explore_destinations, price_shopping, specific_trip_booking, compare_options, information_only, other"],
            ["12. secondary_goals", "Multi-label (Cluster)", "Multi-hot subset of the 6 goal classes above clearly present in user utterances"],
            ["13. emotional_tone", "Categorical (Cluster)", "4 classes: positive, neutral, impatient, or frustrated"],
            ["14. outcome", "Categorical (Audit)", "4 classes: booked, no_suitable_option, undecided_or_left, unclear (excluded from clustering input)"],
            ["15. party_type", "Categorical (Audit)", "6 classes: solo, couple, family, group, business, unknown (excluded from clustering input)"],
            ["16. unusual_conversation", "Boolean (Audit)", "True only if off-task or anomalous request (excluded from clustering input)"],
        ],
        note="Fields 1–13 form the clustering feature matrix (<i>llm_matrix</i>: 10 ordinal + 6 primary_goal + 6 secondary_goals + 4 emotional_tone = 26 numeric columns). Fields 14–16 are retained strictly for post-clustering validation.",
        widths=[1.75, 1.25, 3.50],
        align=["l", "c", "l"],
        label="C1",
        split=True,
    )
    crit = {
        "revision_tendency": [("user_revisions", "Slot-value changes in user acts")],
        "question_asking": [("request_rate", "Request acts per user turn")],
        "exploration_breadth": [("switch_rate", "Frame switches per user turn"), ("compare_rate", "Comparison requests per user turn")],
        "information_upfront": [("front_loading", "Share of slots stated in first user turn")],
        "price_sensitivity": [("budget_stated", "Numeric budget stated")],
        "detail_orientation": [("preference_keys", "Distinct preference slots mentioned")],
    }
    rel16 = ctx["full_16_reliability"]
    c2_rows = []
    for idx_f, (lab_, c) in enumerate(feat, 1):
        cs = crit.get(c, [(None, "N/A")])
        for j, (key, desc_) in enumerate(cs):
            rho = cv_.get(f"{c}~{key}", {}).get("rho") if key else None
            c2_rows.append([
                f"{idx_f}. {lab_}" if j == 0 else "",
                nz(rel16[c]) if j == 0 else "",
                desc_,
                nz(rho) if rho is not None else "N/A",
            ])
    for idx_f, lab_, c, desc_ in [
        (11, "Primary goal (6 classes)", "primary_goal", "Categorical Cohen's κ (clustering)"),
        (12, "Secondary goals (multi-label)", "secondary_goals", "Binary presence Cohen's κ (clustering)"),
        (13, "Emotional tone (4 classes)", "emotional_tone", "Categorical Cohen's κ (clustering)"),
        (14, "Session outcome (4 classes)", "outcome", "Categorical Cohen's κ (audit-only)"),
        (15, "Party type (6 classes)", "party_type", "Categorical Cohen's κ (audit-only)"),
        (16, "Unusual conversation (boolean)", "unusual_conversation", "Boolean Cohen's κ (99.0% raw agreement, audit-only)"),
    ]:
        c2_rows.append([f"{idx_f}. {lab_}", nz(rel16[c]), desc_, "N/A"])
    D.table(
        "Test–Retest Reliability and Criterion Validity Across All 16 LLM Behavioral Schema Fields",
        ["Schema field (#1–16)", "Test–retest κ", "Ground-truth Frames act criterion or field role", "Spearman ρ (<i>p</i> < .001)"],
        c2_rows,
        note=f"Test–retest subsample <i>n</i> = {r1h['reliability']['n']} (quadratic-weighted κ for ordinal Fields 1–10; Cohen's κ for Fields 11–16); criterion validity <i>N</i> = {n2(r1h['n_dialogues'], 0)} Frames dialogues.",
        widths=[1.95, 0.95, 2.55, 1.05],
        align=["l", "c", "l", "c"],
        label="C2",
        split=True,
    )
    jr_d = r3_fin["judge_reliability_flash_vs_det"]
    mr4 = pv4["mean_ratings_by_archetype"]
    D.table(
        "Cross-Model Dual-Judge Reliability (RQ3) and Simulator Persona Fidelity Validation (RQ4)",
        ["Validation audit", "Sample <i>n</i>", "Evaluator models compared", "Raw agreement / Accuracy", "Cohen's κ (PABAK)", "Additional validity evidence"],
        [
            [
                "RQ3 Policy Compliance Dual-Judge Audit",
                str(jr["n"]),
                "<i>gemini-2.5-flash</i> vs. <i>gemini-2.5-pro</i>",
                pct(100 * jr["raw_agreement"], 1),
                f"{nz(jr['cohen_kappa'], 3)} ({nz(jr['pabak'], 3)})",
                f"Flash vs. deterministic regex audit: {pct(100 * jr_d['raw_agreement'], 1)} agreement, κ = {nz(jr_d['cohen_kappa'], 3)}",
            ],
            [
                "RQ4 Simulator Persona Fidelity Audit",
                str(pv4["n"]),
                "Intended Archetype vs. Blind <i>gemini-2.5-pro</i> Judge",
                f"{pct(100 * pv4['accuracy'], 1)} (vs. 33.3% chance)",
                f"{nz(pv4['cohen_kappa'], 3)} (<i>p</i> < .001)",
                f"Mean ratings (Decisiveness / Exploration / Rigidity): DB = {n2(mr4['Decisive Booker']['decisiveness'], 1)}/{n2(mr4['Decisive Booker']['exploration_breadth'], 1)}/{n2(mr4['Decisive Booker']['constraint_rigidity'], 1)}; OE = {n2(mr4['Open Explorer']['decisiveness'], 1)}/{n2(mr4['Open Explorer']['exploration_breadth'], 1)}/{n2(mr4['Open Explorer']['constraint_rigidity'], 1)}; RCS = {n2(mr4['Rigid-Constraint Seeker']['decisiveness'], 1)}/{n2(mr4['Rigid-Constraint Seeker']['exploration_breadth'], 1)}/{n2(mr4['Rigid-Constraint Seeker']['constraint_rigidity'], 1)}",
            ],
        ],
        widths=[1.45, 0.55, 1.35, 0.90, 0.85, 1.40],
        align=["l", "c", "l", "c", "c", "l"],
        label="C3",
        split=True,
    )

    # Appendix D
    D.heading("Appendix D", 1, new_page=True)
    D.heading("RQ1 Sensitivity Grid, Ablation Diagnostics, and Primary Archetype Profiles", 1, toc=False)
    D.para(
        "Tables D1, D2, D3, D4, D5, and D6 and Figures D1, D2, D3, and D4 provide the complete diagnostic tables and "
        "visual plots supporting the RQ1 primary clustering benchmark, Tukey/Games–Howell post hoc algorithm contrasts, "
        "primary whole-dialogue archetype profiles, cross-corpus centroid projection, and the representation × "
        "truncation sensitivity and ablation analysis."
    )
    d1_rows = [
        [f"Panel A (MiniLM-L6-v2 whole): <i>k</i> = {int(r.k)}", nz(r.silhouette, 3), n2(r.davies_bouldin, 3), f"Inertia = {n2(r.inertia, 1)}", f"{n2(r.smallest_cluster_pct, 1)}%"]
        for r in k_sel.itertuples()
    ] + [
        [f"Panel B (46-d Blocks, <i>M</i> = 9): <i>k</i> = {b['k']}", f"{nz(b['sil'], 3)} (cal. {nz(b['cal_sil'], 3)})", n2(b["db"], 3), f"ARI = {nz(b['ari'], 3)} ({n2(b['core_pct'], 1)}% core)", f"{n2(b['min_pct'], 1)}%: {b['note']}"]
        for b in blocks_k_sel
    ]
    D.table(
        "Choice of Number of Clusters k on the Golden Partition Across Initial MiniLM and Final 46-d Blocks (M = 9) Representations",
        ["Representation & <i>k</i>", "Cosine Silhouette", "Davies–Bouldin index", "Inertia / Bootstrap ARI", "Smallest cluster (%) & diagnostic"],
        d1_rows,
        note="On the final 46-d <i>Blocks</i> (<i>M</i> = 9) representation (Panel B), <i>k</i> = 3 achieves the lowest (best) Davies–Bouldin index (2.647), high bootstrap stability (ARI = .888 in the truncation grid; .869 in the 6-config ablation), and balanced cluster sizes (≥ 25.5%).",
        widths=[1.85, 1.05, 0.95, 1.25, 1.40],
        align=["l", "c", "c", "c", "l"],
        label="D1",
        split=True,
    )

    def tk_row(g1, g2):
        r = r1_tk[((r1_tk.group1 == g1) & (r1_tk.group2 == g2)) | ((r1_tk.group1 == g2) & (r1_tk.group2 == g1))].iloc[0]
        if r.group1 == g1:
            return r.meandiff, r["p-adj"], r.lower, r.upper
        return -r.meandiff, r["p-adj"], -r.upper, -r.lower

    def gh_p(g1, g2):
        for a, b, d, df, p in gh:
            if {a, b} == {g1, g2}:
                return p, df

    tk_rows = []
    for g1, g2 in [("Agglomerative", "K-Means"), ("Agglomerative", "HDBSCAN"), ("K-Means", "HDBSCAN")]:
        d, p_t, lo, hi = tk_row(g1, g2)
        p_g, _ = gh_p(g1, g2)
        tk_rows.append([f"{g2} − {g1}", nz(d, 3), f"[{nz(lo, 3)}, {nz(hi, 3)}]", pv_cell(p_t), pv_cell(p_g)])
    D.table(
        "Pairwise Post Hoc Comparisons of Mean Silhouette Across Clustering Algorithms",
        ["Algorithm comparison", "Mean difference", "95% CI (Tukey HSD)", "<i>p</i> (Tukey HSD)", "<i>p</i> (Games–Howell)"],
        tk_rows,
        widths=[2.00, 1.10, 1.40, 1.00, 1.00],
        align=["l", "c", "c", "c", "c"],
        label="D2",
        split=True,
    )
    pr = prof.reindex(ARCH_PRIM)
    D.table(
        "Behavioral Profiles of the Three Primary Whole-Dialogue Archetypes (Golden Partition)",
        ["Feature", *ARCH_PRIM],
        [
            ["<i>n</i> (%)", *[f"{int(r.n)} ({n2(r.pct, 1)}%)" for r in pr.itertuples()]],
            ["Turns, <i>M</i> (<i>SD</i>)", *[f"{n2(r.turns_M)} ({n2(r.turns_SD)})" for r in pr.itertuples()]],
            ["Words per user / agent turn", *[f"{n2(r.user_words)} / {n2(r.agent_words)}" for r in pr.itertuples()]],
            ["Slot-value revisions / Hesitations", *[f"{n2(r.revisions, 1)} / {n2(r.hesitations, 1)}" for r in pr.itertuples()]],
            ["Agent package offers", *[n2(r.offers) for r in pr.itertuples()]],
            ["Budget stated (%) / Task success (%)", *[f"{n2(r.budget_pct, 1)}% / {n2(r.success_pct, 1)}%" for r in pr.itertuples()]],
        ],
        widths=[2.20, 1.43, 1.43, 1.44],
        align=["l", "c", "c", "c"],
        label="D3",
        split=True,
    )
    D.table(
        "Primary Archetype Assignment and Centroid Similarity Across Partitions and MultiWOZ 2.2",
        ["Sample", "<i>N</i>", "Centroid cosine <i>M</i> (<i>SD</i>)", *[f"{a} (%)" for a in ARCH_PRIM]],
        [
            [
                s.replace("D_gold", "golden").replace("D_test", "held-out"),
                n2(r.N, 0),
                f"{nz(r.sim_M, 3)} ({nz(r.sim_SD, 3)})",
                *[n2(getattr(r, a.replace(" ", "_")), 1) for a in ARCH_PRIM],
            ]
            for s, r in cross.rename(columns={a: a.replace(" ", "_") for a in ARCH_PRIM}).set_index("set").iterrows()
        ],
        widths=[1.50, 0.60, 1.40, 1.00, 1.00, 1.00],
        align=["l", "c", "c", "c", "c", "c"],
        label="D4",
        split=True,
    )
    D.table(
        "Stability, Routing Agreement, and Outcome Association of Hybrid Archetypes by Conversation Length",
        ["User messages used (<i>M</i>)", "Dialogues shortened (%)", "Bootstrap ARI", "Core members (%)", "Smallest cluster (%)", "Raw L1 κ", "Blocks router κ", "Outcome <i>V</i>"],
        [
            [
                ("Whole conversation" if m == "whole" else f"First {m} messages"),
                n2(r1t["annotations"]["None" if m == "whole" else m]["truncated_pct"], 1),
                nz(r.stability_ari),
                n2(r.core_pct, 1),
                n2(r.min_cluster_pct, 1),
                nz(r.kappa_N5),
                (nz(rt_diag.loc[int(m), "cohen_kappa"], 3) if m != "whole" else "N/A"),
                nz(r.outcome_v),
            ]
            for m, r in tr3.iterrows()
        ],
        note="Raw L1 κ uses unprojected 5-turn features (<i>step2g</i>); Blocks router κ projects prefix features into the exact golden <i>Blocks</i> space (<i>RefinedArchetypeRouter</i>).",
        widths=[1.35, 0.80, 0.70, 0.75, 0.75, 0.65, 0.80, 0.70],
        align=["l"] + ["c"] * 7,
        label="D5",
        split=True,
    )
    D.table(
        "Ablation of the Refined Archetype Definition at M = 9 User Messages (k = 3)",
        ["Representation configuration", "ARI (whole)", "ARI (9 msgs)", "Core members (%)", "Outcome <i>V</i>", "ARI vs. adopted"],
        [
            [
                a9.loc[c, "name"].replace("behavioural", "behavior") + (" (adopted)" if c == 1 else ""),
                nz(aw.loc[c, "stability_ari"]),
                nz(a9.loc[c, "stability_ari"]),
                n2(a9.loc[c, "core_pct"], 1),
                nz(a9.loc[c, "outcome_v"]),
                "1.00" if c == 1 else nz(a9.loc[c, "ari_vs_adopted"]),
            ]
            for c in a9.index
        ],
        widths=[2.30, 0.80, 0.85, 0.90, 0.80, 0.85],
        align=["l", "c", "c", "c", "c", "c"],
        label="D6",
        split=True,
    )
    D.figure("Cluster-Number Diagnostics on Golden Partition", os.path.join(FIG_INT, "fig_rq1_k_selection.png"), label="D1")
    D.figure("Silhouette Coefficients Across 159 Matched Resampling Runs by Algorithm", os.path.join(FIG_INT, "fig_rq1_silhouette.png"), label="D2")
    D.figure("UMAP Projection of Frames Archetypes and MultiWOZ 2.2 External Transfer Check", os.path.join(FIG_INT, "fig_rq1_umap.png"), label="D3")
    D.figure("Hybrid Archetype Stability, Routing, and Outcome Association Across Truncation Horizons", os.path.join(FIG_INT, "fig_rq1_truncation_2x2.png"), label="D4")

    # Appendix E
    D.heading("Appendix E", 1, new_page=True)
    D.heading("Supplementary EDA, RQ2 Pairwise Contrasts, and RQ3/RQ4 Groundwork Diagnostics", 1, toc=False)
    D.para(
        "Tables E1, E2, E3, E4, and E5 and Figures E1, E2, and E3 provide the supplementary slot-completeness table and "
        "plot, multivariate PCA loadings, Holm-adjusted pairwise contrasts and primary unrefined evaluation for RQ2, "
        "corpus rule coverage audit for RQ3, and human turn-economy baseline for RQ4."
    )
    D.table(
        "Observed Canonical Slot Completeness by Corpus",
        ["Canonical slot", "Schema tier", "Microsoft Frames (%)", "MultiWOZ 2.2 (%)"],
        [[s.replace("_", " "), t, n2(f, 1), n2(m, 1)] for s, t, f, m in comp.itertuples(index=False)],
        widths=[2.50, 1.10, 1.45, 1.45],
        align=["l", "c", "c", "c"],
        label="E1",
        split=True,
    )
    D.table(
        "Multivariate Principal Component Loadings of Structural and Behavioral Features (Frames)",
        ["Variable", "PC1 loading (40.8% var.)", "PC2 loading (17.2% var.)", "PC3 loading (10.6% var.)"],
        [[r.variable, nz(r.PC1_loading, 3), nz(r.PC2_loading, 3), nz(r.PC3_loading, 3)] for _, r in t_mv.iterrows()],
        widths=[2.30, 1.40, 1.40, 1.40],
        align=["l", "c", "c", "c"],
        label="E2",
        split=True,
    )
    e3_rows = []
    for dv_key, dv_lab in [
        ("sbert_style_cos", "Refined: SBERT style cosine"),
        ("style_cos", "Refined: Gemini style cosine"),
        ("bert_f1", "Refined: BERTScore F1"),
        ("word_abs_err", "Refined: Pacing error (words)"),
        ("words", "Refined: Response length (words)"),
    ]:
        for p_ in r2_ref["results"][dv_key]["pairs"]:
            mdiff = n2(p_["mean_diff"], 2) if "word" in dv_key else nz(p_["mean_diff"], 3)
            e3_rows.append([
                dv_lab,
                p_["contrast"].replace(" Few-Shot", ""),
                mdiff,
                n2(p_["t"]),
                str(int(p_["df"])),
                pv_cell(p_["p_holm"]),
                n2(p_["d_z"]),
            ])
    D.table(
        "Holm-Adjusted Paired Contrasts for Refined RQ2 Outcomes (N = 33)",
        ["Outcome metric", "Pairwise contrast", "Mean diff.", "<i>t</i>", "<i>df</i>", "<i>p</i> (Holm)", "<i>d<sub>z</sub></i>"],
        e3_rows,
        widths=[1.75, 1.85, 0.75, 0.55, 0.40, 0.65, 0.55],
        align=["l", "l", "c", "c", "c", "c", "c"],
        label="E3",
        split=True,
    )
    D.table(
        "Empirical Corpus Audit of Policy Rule Coverage in Microsoft Frames (N = 1,334)",
        ["Declarative rule", "Required canonical slot", "Slot observed (%)", "Dialogues triggering (<i>n</i>)", "Triggering (%)"],
        [
            [
                r.replace("RULE_", "").replace("_", " ").lower(),
                a.required_slot.replace("_", " "),
                n2(a.slot_observed_pct, 1),
                str(int(a.trigger_n)),
                n2(a.trigger_pct, 2),
            ]
            for r, a in audit.iterrows()
        ],
        widths=[1.60, 1.90, 1.00, 1.10, 0.90],
        align=["l", "l", "c", "c", "c"],
        label="E4",
        split=True,
    )
    b4_df = base4r.reindex(ARCH_REF)
    D.table(
        "Human Wizard Baseline of Turn Economy and Redundant Elicitation by Refined Archetype (Frames)",
        ["Refined user archetype", "<i>n</i>", "Whole-dialogue turns <i>M</i> (<i>SD</i>)", "RER <i>M</i> (<i>SD</i>)", "Wizard request turns <i>M</i>"],
        [[a, str(int(r.n)), f"{n2(r.turns_M)} ({n2(r.turns_SD)})", f"{nz(r.rer_M, 3)} ({nz(r.rer_SD, 3)})", n2(r.req_turns_M)] for a, r in b4_df.iterrows()],
        note="Turns in Table E5 reflect total observed human-wizard turns across complete archival Frames transcripts, whereas Table 18 (RQ4) measures total conversational turns until package agreement (<i>[ACCEPT_BOOKING]</i>) in closed-loop simulation.",
        widths=[1.85, 0.55, 1.35, 1.30, 1.45],
        align=["l", "c", "c", "c", "c"],
        label="E5",
        split=True,
    )
    D.figure("Observed Canonical Slot Completeness by Corpus", os.path.join(FIG_INT, "fig_eda_slots.png"), label="E1")
    D.figure("Primary RQ2 Results on Unrefined Whole-Dialogue Archetypes", os.path.join(FIG_INT, "fig_rq2_results.png"), label="E2")
    D.figure("Human Wizard Baseline of Turn Economy and Redundant Elicitation by Refined Archetype", os.path.join(FIG_INT, "fig_rq4_baseline_refined.png"), label="E3")

    # Appendix F
    D.heading("Appendix F", 1, new_page=True)
    D.heading("Derivation of User Archetype Cluster Names and Deterministic Centroid-Mapping Protocol", 1, toc=False)
    D.para(
        "Unsupervised clustering algorithms such as <i>K</i>-Means output anonymous integer cluster identifiers "
        "(<i>0</i>, <i>1</i>, <i>2</i>) rather than semantic persona names, and those integer identifiers are invariant "
        "up to permutation across random initializations (the <i>label-switching problem</i>). To ensure that "
        "human-interpretable archetype labels are assigned reproducibly using the highest-importance behavioral "
        "features (Table 13), both the primary whole-dialogue pipeline (<i>src/final_pipeline/step2_rq1_clustering.py</i>) "
        "and the refined opening-prefix pipeline (<i>src/final_pipeline/step2i_rq1_refined_archetypes.py</i>) apply "
        "pre-declared, deterministic Python centroid-mapping rules to the golden-partition cluster means (Table F1)."
    )
    D.table(
        "Deterministic Centroid-Mapping Rules for Primary and Refined User Archetypes",
        [
            "Clustering taxonomy & script",
            "Step & deterministic Python rule on cluster centroid means",
            "Assigned archetype name",
            "Distinguishing golden-partition centroid signature (<i>N</i> = 933)",
        ],
        [
            [
                "Primary Whole-Dialogue Archetypes (<i>step2_rq1_clustering.py</i>)",
                "Step 1: <i>idxmax(turns_M)</i> among the 3 clusters",
                "Guided Explorer",
                "Longest dialogues (<i>M</i> = 19.65 turns, <i>n</i> = 187, 20.0%); highest option exploration across whole transcripts",
            ],
            [
                "Primary Whole-Dialogue Archetypes (<i>step2_rq1_clustering.py</i>)",
                "Step 2: <i>idxmax(revisions)</i> among the remaining 2 clusters",
                "Constraint Negotiator",
                "Highest slot-revision count (<i>M</i> = 1.98 revisions, <i>M</i> = 15.80 turns, <i>n</i> = 351, 37.6%)",
            ],
            [
                "Primary Whole-Dialogue Archetypes (<i>step2_rq1_clustering.py</i>)",
                "Step 3: Remaining cluster ID",
                "Direct Transactional",
                "Shortest whole-dialogue sessions (<i>M</i> = 11.98 turns, <i>n</i> = 395, 42.3%); lowest revision count",
            ],
            [
                "Refined Opening-Prefix Archetypes (<i>step2i_rq1_refined_archetypes.py</i>)",
                "Step 1: <i>idxmax(destination_flexibility)</i> across the 3 <i>Blocks</i> clusters (<i>M</i> = 9)",
                "Open Explorer",
                f"Highest destination flexibility ({n2(oe_r.destination_flexibility)}/5.0) and exploration breadth ({n2(oe_r.exploration_breadth)}/5.0); longest dialogues ({n2(oe_r.turns_M)} turns; <i>n</i> = {int(oe_r.n)}, {n2(oe_r.pct, 1)}%)",
            ],
            [
                "Refined Opening-Prefix Archetypes (<i>step2i_rq1_refined_archetypes.py</i>)",
                "Step 2: <i>idxmax(decisiveness)</i> among the remaining 2 clusters",
                "Decisive Booker",
                f"Highest decisiveness ({n2(db_r.decisiveness)}/5.0), politeness ({n2(db_r.politeness)}/5.0), and specific trip booking goal ({n2(db_r.goal_booking_pct, 1)}%; <i>n</i> = {int(db_r.n)}, {n2(db_r.pct, 1)}%)",
            ],
            [
                "Refined Opening-Prefix Archetypes (<i>step2i_rq1_refined_archetypes.py</i>)",
                "Step 3: Remaining cluster ID",
                "Rigid-Constraint Seeker",
                f"Lowest destination/date flexibility ({n2(rc_r.destination_flexibility)}/{n2(rc_r.date_flexibility)}) and detail orientation ({n2(rc_r.detail_orientation)}/5.0); highest non-booking rate under rigid constraints ({n2(rc_r.no_option_pct, 1)}% no suitable option; <i>n</i> = {int(rc_r.n)}, {n2(rc_r.pct, 1)}%)",
            ],
        ],
        note="All centroid-mapping rules are evaluated strictly on golden-partition means (<i>D</i><sub>gold</sub>, <i>n</i> = 933) after fitting <i>K</i>-Means (<i>k</i> = 3, seed = 42).",
        widths=[1.45, 1.85, 1.25, 1.95],
        align=["l", "l", "l", "l"],
        label="F1",
        split=True,
    )

    # Appendix G
    D.heading("Appendix G", 1, new_page=True)
    D.heading("Role, Architecture, and Validation Scope of Judge and Annotator LLMs", 1, toc=False)
    D.para(
        "All primary hypothesis tests (<i>H</i><sub>01</sub>–<i>H</i><sub>04</sub>) are anchored in deterministic "
        "mathematical and programmatic Python verification metrics rather than subjective LLM preference scores: RQ1 "
        "uses mathematical Silhouette, Davies–Bouldin, ARI, Cohen's κ, and ROC-AUC; RQ2 uses deterministic non-Gemini "
        "encoders (<i>all-MiniLM-L6-v2</i> cosine, BERTScore F<sub>1</sub>, and exact word-count error); RQ3 computes "
        "entity leakage (ELR) and Slot F<sub>1</sub> via exact Python set verifiers (<i>src/final_pipeline/metrics.py</i>); "
        "and RQ4 computes turn economy (TGC and RER) via deterministic turn counters and regex slot-ledger matching."
    )
    D.para(
        "LLMs serve two bounded functions (Table G1): (a) in RQ1, <i>gemini-2.5-flash</i> (temperature = 0) extracts "
        "the 16-field <i>UserBehaviour</i> codebook prior to clustering (validated via test–retest κ<sub><i>w</i></sub> = "
        ".87–.96 and Frames act correlations ρ = .30–.73; Table C2); and (b) in RQ3 and RQ4, <i>gemini-2.5-pro</i> "
        "acts strictly as an independent cross-verification gatekeeper (95.8% agreement, κ = .917 with "
        "<i>gemini-2.5-flash</i> and 93.1% agreement, κ = .861 with deterministic regex in RQ3; 95.6% blind persona "
        "accuracy, κ = .933 in RQ4; Table C3)."
    )
    D.table(
        "Functional Scope, Primary Deterministic Metrics, and Cross-Verification Role of Judge and Annotator LLMs",
        [
            "Research question & pipeline stage",
            "Primary hypothesis-test metrics (Deterministic / Mathematical)",
            "LLM annotator / Judge model & role",
            "Cross-verification agreement & gatekeeping outcome",
        ],
        [
            [
                "RQ1-Identify Stage: Opening-Prefix Behavioral Annotation (<i>step2e_llm_user_annotation.py</i>)",
                "Cosine Silhouette, Davies–Bouldin, Bootstrap ARI (.89 / .87), feature importance (η<sup>2</sup>, Δκ), and prefix κ / ROC-AUC",
                "<b>Codebook Annotator (<i>gemini-2.5-flash</i>, temp = 0):</b> Extracts Fields 1–13 (clustering inputs) and Fields 14–16 (audit-only) before <i>K</i>-Means runs.",
                "Test–retest κ<sub><i>w</i></sub> = .87–.96 (mean .91) on ordinal Fields 1–10; κ = .75–.98 on Fields 11–16; Spearman ρ = .30–.73 (<i>p</i> < .001) vs. Frames acts (Table C2).",
            ],
            [
                "RQ2-Personalize Stage: Style Convergence & Pacing Calibration (<i>step2_rq2_refined.py</i>)",
                "De-lexicalized SBERT style cosine (<i>all-MiniLM-L6-v2</i>), BERTScore F<sub>1</sub>, and absolute word-count error",
                "<b>No Judge LLM used:</b> All evaluation encoders are deterministic, non-Gemini neural and lexical metrics.",
                "Eliminates same-family LLM evaluation bias in RQ2; RM-ANOVA and Friedman tests confirm <i>p</i> < .001 on SBERT style convergence.",
            ],
            [
                "RQ3-Govern Stage: Policy Compliance Dual-Judge Audit (<i>step3_rq3_experiment.py</i>)",
                "Deterministic regex rule verifier (<i>det_pass</i>), exact Exemplar Entity Leakage Rate (ELR), and deterministic Slot Grounding F<sub>1</sub>",
                "<b>Primary Judge (<i>gemini-2.5-flash</i>) + Independent Validator (<i>gemini-2.5-pro</i>):</b> Cross-verifies enforcement of 5 policy rules on stratified audit subsample (<i>n</i> = 48).",
                "Guided <i>pilot_v1</i> → <i>pilot_v2</i> prompt ordering fix; final dual-judge agreement = 95.8% (κ = .917, PABAK = .917) and 93.1% (κ = .861) vs. regex (Table C3).",
            ],
            [
                "RQ4-Optimize Stage: Blind Simulator Persona Fidelity Audit (<i>step4_rq4_simulation.py</i>)",
                "Deterministic turn counter to agreed package quotation (<i>total_turns</i>, <i>log_turns</i>), regex Redundant Elicitation Rate (RER), and completion rate",
                "<b>Independent Blind Validator (<i>gemini-2.5-pro</i>):</b> Reads simulated customer transcripts (<i>n</i> = 45, 15/archetype) blinded to true labels; contributes zero metrics to RQ4 ANOVA.",
                "Classified 43/45 simulated users into their intended archetype (95.6% accuracy vs. 33.3% chance, Cohen's κ = .933, <i>p</i> < .001; Table C3).",
            ],
        ],
        note="All LLM annotation and judge calls use deterministic decoding (temperature = 0.0, Pydantic JSON schema enforcement) and are cached in <i>data/interim/</i> and <i>data/final/</i>.",
        widths=[1.35, 1.65, 1.75, 1.75],
        align=["l", "l", "l", "l"],
        label="G1",
        split=True,
    )
