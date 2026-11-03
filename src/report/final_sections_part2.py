"""
Part 2 of the QM640 Final Report builder (calibrated for <= 30 core pages, zero markdown artifacts, strict APA 7):
  - Section 5: Results, Analysis, and Synthesis (Consolidated Summary Table 11, RQ1 Tables 12–13, RQ2 Table 14 & Figure 6, RQ3 Table 15 & Figure 7, RQ4 Table 16 & Figure 8, Technical & Business Synthesis)
  - Section 6: Implementation, Limitations, and Future Scope (Deployment & Real-World Use Case, Reproducibility, Limitations, Future Scope)
  - References (26 alphabetical peer-reviewed APA 7 entries)
  - Appendices A–E (Tables A1–A3, B1, C1–C3, D1–D6 + Figures D1–D4, E1–E5 + Figures E1–E3)
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
    qa = ctx["qa"]
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
    win = r1t["winner"]
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

    # ================================================================== 5. RESULTS, ANALYSIS, AND SYNTHESIS
    D.heading("Results, Analysis, and Synthesis", 1)
    D.heading("Consolidated Model Performance and Hypothesis Testing Summary", 2)
    D.para(
        "Table 11 summarizes the empirical results, parametric test statistics, heteroscedasticity-robust (Welch/HC3) "
        "and non-parametric (Kruskal–Wallis, Friedman, Mann–Whitney, and Aligned Rank Transform [ART]) checks, effect "
        "sizes, and hypothesis decisions across RQ1–RQ4. All four null hypotheses specified for the study "
        "(<i>H</i><sub>01</sub>–<i>H</i><sub>04</sub>) are rejected at <i>p</i> < .001 on the refined user archetype pipeline."
    )

    r2_sc = r2_ref["results"]["sbert_style_cos"]
    r2_sa = r2_sc["anova"]
    r2_we_r = r2_ref["results"]["word_abs_err"]
    r2_wa = r2_we_r["anova"]
    r3_a = r3_fin["anova"]
    r4_a = r4_fin["anova"]

    D.table(
        "Consolidated Summary of Empirical Results and Hypothesis Outcomes Across RQ1–RQ4",
        ["RQ and outcome", "Sample & design", "Baseline vs. proposed performance", "Primary parametric test & effect size", "Robust / non-parametric check", "Outcome"],
        [
            [
                "RQ1: Algorithm separation & refined archetypes",
                "<i>N</i> = 159 runs (53 matched <i>n</i> = 500 draws from <i>D</i><sub>gold</sub> = 933; <i>D</i><sub>test</sub> = 401)",
                f"MiniLM Sil: Perm = {nz(perm['M'], 3)} vs. KM = {nz(km.sil_M, 3)}, Ward = {nz(ag.sil_M, 3)}, HDB = {nz(hd.sil_M, 3)} (39.1% noise); Blocks ARI = .89 (.87 abl.); routing κ = .535 (<i>m</i>=5) to .958 (<i>m</i>=9)",
                f"One-way <i>F</i>(2, 156) = {n2(an['F'])}, <i>p</i> < .001, η<sup>2</sup> = {nz(an['eta2'])}; Matched RM-ANOVA <i>F</i>(1.72, 89.30) = {n2(r1_rm['F'])}, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = {nz(r1_rm['eta2_p'], 3)}",
                f"Friedman χ<sup>2</sup>(2) = {n2(r1_rm['friedman_chi2'])}, Welch <i>F</i> = {n2(we['F'])}, Kruskal <i>H</i>(2) = {n2(kw['H'])}, all <i>p</i> < .001",
                "Reject <i>H</i><sub>01</sub>",
            ],
            [
                "RQ2: De-lexicalized SBERT style cosine (Refined)",
                "<i>N</i> = 33 dialogues × 3 conditions (99 calls; combined exemplars + directive)",
                f"Static = {nz(r2_sc['desc']['Static Few-Shot'][0], 3)}, Zero-Shot = {nz(r2_sc['desc']['Zero-Shot'][0], 3)} vs. Cluster-Adaptive = {nz(r2_sc['desc']['Cluster-Adaptive Few-Shot'][0], 3)} (Gemini/BERTScore null, <i>p</i> ≥ .315)",
                f"RM-ANOVA <i>F</i>({n2(r2_sa['df1_gg'])}, {n2(r2_sa['df2_gg'])}) = {n2(r2_sa['F'])}, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = {nz(r2_sa['eta2_partial'])}",
                f"Friedman χ<sup>2</sup>(2) = {n2(r2_sc['friedman']['chi2'])}, <i>p</i> = {nz(r2_sc['friedman']['p'], 3)}; Holm <i>p</i> < .001 vs. Static",
                "Reject <i>H</i><sub>02</sub>",
            ],
            [
                "RQ2: Pacing calibration error (words)",
                "<i>N</i> = 33 dialogues × 3 conditions (99 calls)",
                f"Zero-Shot = {n2(r2_we_r['desc']['Zero-Shot'][0])}w, Static = {n2(r2_we_r['desc']['Static Few-Shot'][0])}w vs. Cluster-Adaptive = {n2(r2_we_r['desc']['Cluster-Adaptive Few-Shot'][0])}w",
                f"RM-ANOVA <i>F</i>({n2(r2_wa['df1_gg'])}, {n2(r2_wa['df2_gg'])}) = {n2(r2_wa['F'])}, <i>p</i> = {nz(r2_wa['p_gg'], 3)}, η<sub><i>p</i></sub><sup>2</sup> = {nz(r2_wa['eta2_partial'])}",
                f"Friedman χ<sup>2</sup>(2) = {n2(r2_we_r['friedman']['chi2'])}, <i>p</i> < .001; Holm <i>p</i> = .004 vs. Zero-Shot",
                "Reject <i>H</i><sub>02</sub>",
            ],
            [
                "RQ3: Policy rule adherence (Sens. / Spec. / Overall)",
                "<i>N</i> = 144 (2 × 2 across 36 dialogues, <i>n</i> = 36/cell; κ<sub>judge</sub> = .917)",
                "Viol. Sens. (<i>n</i>=18/cell): 5.6% → 98.6%; Comp. Spec. (<i>n</i>=18/cell): 94.4% vs. 88.9%; Overall (<i>n</i>=36/cell): .500 → .938",
                f"Sens. <i>F</i>(1, 68) = 498.78, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = .880; Overall Rules <i>F</i>(1, 140) = {n2(r3_a['rule_adherence']['effects']['rules_mode']['F'])}, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = {nz(r3_a['rule_adherence']['effects']['rules_mode']['eta2_partial'])}",
                f"HC3 <i>F</i> = {n2(r3_a['rule_adherence']['effects']['rules_mode']['F_hc3'])}, <i>p</i> < .001; ART <i>F</i> = {n2(r3_a['rule_adherence']['effects']['rules_mode']['F_art'])}, <i>p</i> < .001",
                "Reject <i>H</i><sub>03</sub>",
            ],
            [
                "RQ3: Exemplar entity leakage & Slot F<sub>1</sub>",
                "<i>N</i> = 144 (2 × 2, <i>n</i> = 36/cell)",
                "Leakage: Rules Off Cluster = .359 (55.6% cases) vs. Rules Active Cluster = .000 (0.0%); Slot F<sub>1</sub>: .485 → .952",
                f"Leakage Int. <i>F</i>(1, 140) = {n2(r3_a['leakage_rate']['effects']['interaction']['F'])}, <i>p</i> < .001; Slot F<sub>1</sub> Rules <i>F</i> = {n2(r3_a['slot_f1']['effects']['rules_mode']['F'])}, <i>p</i> < .001",
                f"Leakage Sum-HC3 <i>F</i> = 33.85, ART Int. <i>F</i> = {n2(r3_a['leakage_rate']['effects']['interaction']['F_art'])}, Simple Welch <i>t</i>(35) = 5.90, all <i>p</i> < .001",
                "Reject <i>H</i><sub>03</sub>",
            ],
            [
                "RQ4: Log turns to goal completion & RER",
                "<i>N</i> = 180 unique dialogues (2 × 3, <i>n</i> = 30/cell; κ<sub>persona</sub> = .933)",
                "Total turns reduced −34.2% (DB), −29.5% (OE), −42.7% (RCS; 5.00-turn floor); RER .109 → .000",
                f"Prompt <i>F</i>(1, 174) = {n2(r4_a['log_turns']['effects']['prompt_mode']['F'])}, <i>p</i> < .001; Int. <i>F</i>(2, 174) = {n2(r4_a['log_turns']['effects']['interaction']['F'])}, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = {nz(r4_a['log_turns']['effects']['interaction']['eta2_partial'])}",
                f"HC3 Int. <i>F</i> = {n2(r4_a['log_turns']['effects']['interaction']['F_hc3'])}, <i>p</i> < .001; ART Int. <i>F</i> = {n2(r4_a['log_turns']['effects']['interaction']['F_art'])}, <i>p</i> < .001",
                "Reject <i>H</i><sub>04</sub>",
            ],
        ],
        note="DB = Decisive Booker; OE = Open Explorer; RCS = Rigid-Constraint Seeker; Perm = permutation baseline; Sens. = violation enforcement sensitivity; Spec. = compliant acceptance specificity.",
        widths=[1.12, 0.93, 1.43, 1.25, 1.12, 0.65],
        align=["l", "l", "l", "l", "l", "c"],
        split=True,
    )

    # ------------------------------------------------------------------ RQ1 Results
    D.heading("RQ1 Results: Trajectory Clustering, Refined Archetypes, and Prefix Routing", 2)
    D.para(
        "<i>Primary algorithm benchmark, resampling sensitivity, and embedding invariance.</i> Table 12 summarizes the "
        "159-run clustering benchmark across <i>all-MiniLM-L6-v2</i> (384-d) and <i>gemini-embedding-001</i> (3,072-d) "
        "representations (cluster-number diagnostics, Tukey/Games–Howell post hoc contrasts, and UMAP plots are in "
        "Appendix D, Tables D1–D4 and Figures D1–D3). Because each of the 53 random seeds draws <i>n</i> = 500 dialogues "
        f"without replacement from the finite golden partition (<i>D</i><sub>gold</sub>, <i>n</i> = {s1['n_gold']}, a "
        "53.6% sampling fraction with ~268 overlapping dialogues between draws), the 159 evaluations represent a "
        "finite-population resampling stability analysis rather than 159 independent samples; accordingly, we report both "
        "matched-subsample repeated-measures tests across the 53 shared seeds and full-<i>D</i><sub>gold</sub> point "
        "estimates alongside the standard one-way benchmark. On MiniLM embeddings, HDBSCAN achieved the highest "
        f"Silhouette on its retained non-noise subset (<i>M</i> = {nz(hd.sil_M, 3)}, <i>SD</i> = {nz(hd.sil_SD, 3)}), "
        f"followed by <i>K</i>-Means (<i>M</i> = {nz(km.sil_M, 3)}, <i>SD</i> = {nz(km.sil_SD, 3)}; full-<i>D</i><sub>gold</sub> "
        f"point estimate = .141, Davies–Bouldin = 3.244) and Ward agglomerative clustering (<i>M</i> = {nz(ag.sil_M, 3)}, "
        f"<i>SD</i> = {nz(ag.sil_SD, 3)}), all exceeding the label-shuffled permutation baseline (<i>M</i> = "
        f"{nz(perm['M'], 3)}). Algorithm differences were highly significant under the matched-subsample repeated-measures "
        f"ANOVA, <i>F</i>({n2(r1_rm['df1_gg'])}, {n2(r1_rm['df2_gg'])}) = {n2(r1_rm['F'])}, <i>p</i> < .001, "
        f"η<sub><i>p</i></sub><sup>2</sup> = {nz(r1_rm['eta2_p'], 3)}, the non-parametric paired Friedman test, "
        f"χ<sup>2</sup>(2) = {n2(r1_rm['friedman_chi2'])}, <i>p</i> < .001, the one-way ANOVA, <i>F</i>({int(an['df1'])}, "
        f"{int(an['df2'])}) = {n2(an['F'])}, <i>p</i> < .001, η<sup>2</sup> = {nz(an['eta2'])}, Welch's test, "
        f"<i>F</i>({int(we['df1'])}, {n2(we['df2'])}) = {n2(we['F'])}, <i>p</i> < .001, and Kruskal–Wallis "
        f"<i>H</i>(2) = {n2(kw['H'])}, <i>p</i> < .001. Replicating on 3,072-d Gemini embeddings reproduced the same "
        f"ordering with stronger separation: for turn-pooled vectors (<i>G-pooled</i>), <i>K</i>-Means = "
        f"{nz(r1gm['G-pooled']['desc']['K-Means']['M'], 3)}, Ward = {nz(r1gm['G-pooled']['desc']['Agglomerative']['M'], 3)}, "
        f"and HDBSCAN = {nz(r1gm['G-pooled']['desc']['HDBSCAN']['M'], 3)} (<i>F</i>(2, 156) = "
        f"{n2(r1gm['G-pooled']['anova']['F'])}, η<sup>2</sup> = {nz(r1gm['G-pooled']['anova']['eta2'])}, <i>p</i> < .001); "
        f"for document vectors (<i>G-doc</i>), <i>K</i>-Means = {nz(r1gm['G-doc']['desc']['K-Means']['M'], 3)}, Ward = "
        f"{nz(r1gm['G-doc']['desc']['Agglomerative']['M'], 3)}, and HDBSCAN = "
        f"{nz(r1gm['G-doc']['desc']['HDBSCAN']['M'], 3)} (<i>F</i>(2, 156) = {n2(r1gm['G-doc']['anova']['F'])}, "
        f"η<sup>2</sup> = {nz(r1gm['G-doc']['anova']['eta2'])}, <i>p</i> < .001). Critically, however, HDBSCAN's higher "
        "Silhouette is computed strictly after excluding unassigned noise points: HDBSCAN failed at default settings "
        f"(<i>min_cluster_size</i> = 15) in {r1['hdbscan_default_fail']}/53 runs and discarded "
        f"<b>{pct(100 * r1['hdbscan_noise_M'])}</b> (<i>SD</i> = {pct(100 * r1['hdbscan_noise_SD'])}) of MiniLM dialogues, "
        f"<b>{pct(100 * r1gm['G-pooled']['hdbscan_noise_M'])}</b> of Gemini turn-pooled dialogues, and "
        f"<b>{pct(100 * r1gm['G-doc']['hdbscan_noise_M'])}</b> of Gemini document dialogues as noise when relaxed. "
        "Because a live travel assistant cannot refuse to route 26%–39% of incoming customer sessions, <i>K</i>-Means "
        "(<i>k</i> = 3) was selected on operational grounds to guarantee <b>100% dialogue coverage</b> and deterministic "
        "Voronoi centroid routing. Golden centroids generalized to held-out Frames dialogues "
        f"(<i>t</i>({n2(gt['df'], 1)}) = {n2(gt['t'])}, <i>p</i> {pv(gt['p'])}) but differed from MultiWOZ 2.2 "
        f"(<i>t</i>({n2(cc['df'], 1)}) = {n2(cc['t'])}, <i>p</i> < .001; Table D4)."
    )
    g_p = r1gm["G-pooled"]
    g_d = r1gm["G-doc"]
    D.table(
        "Cluster Quality by Algorithm and Embedding Family Across 53 Matched Subsample Seeds (159 Runs)",
        ["Representation and algorithm", "<i>n</i> seeds", "Retained (%)", "Silhouette <i>M</i> (<i>SD</i>)", "Davies–Bouldin <i>M</i> (<i>SD</i>)", "Omnibus & matched RM tests (<i>p</i> < .001)"],
        [
            ["MiniLM-L6-v2 (384-d) — K-Means (<i>k</i> = 3)", "53", "100.0%", f"{nz(km.sil_M, 3)} ({nz(km.sil_SD, 3)})", f"{n2(km.db_M, 3)} ({n2(km.db_SD, 3)})", f"One-way <i>F</i> = {n2(an['F'])}, η<sup>2</sup> = {nz(an['eta2'])}"],
            ["MiniLM-L6-v2 (384-d) —Ward Agglomerative", "53", "100.0%", f"{nz(ag.sil_M, 3)} ({nz(ag.sil_SD, 3)})", f"{n2(ag.db_M, 3)} ({n2(ag.db_SD, 3)})", f"Matched RM <i>F</i> = {n2(r1_rm['F'])}, η<sub><i>p</i></sub><sup>2</sup> = {nz(r1_rm['eta2_p'], 3)}"],
            ["MiniLM-L6-v2 (384-d) — HDBSCAN (non-noise)", "53", f"{pct(100 * (1 - r1['hdbscan_noise_M']))}", f"{nz(hd.sil_M, 3)} ({nz(hd.sil_SD, 3)})", f"{n2(hd.db_M, 3)} ({n2(hd.db_SD, 3)})", f"Friedman χ<sup>2</sup> = {n2(r1_rm['friedman_chi2'])}, Welch <i>F</i> = {n2(we['F'])}"],
            ["MiniLM-L6-v2 (384-d) — Permutation baseline", "53", "100.0%", f"{nz(perm['M'], 3)} ({nz(perm['SD'], 3)})", "—", "Full <i>D</i><sub>gold</sub> KM Sil = .141, DB = 3.244"],
            ["Gemini-001 (3,072-d turn pool) — KM / Ward / HDB", "53 × 3", f"100 / 100 / {pct(100 * (1 - g_p['hdbscan_noise_M']))}", f"{nz(g_p['desc']['K-Means']['M'], 3)} / {nz(g_p['desc']['Agglomerative']['M'], 3)} / {nz(g_p['desc']['HDBSCAN']['M'], 3)}", f"{n2(g_p['desc']['K-Means']['DB_M'], 2)} / {n2(g_p['desc']['Agglomerative']['DB_M'], 2)} / {n2(g_p['desc']['HDBSCAN']['DB_M'], 2)}", f"<i>F</i> = {n2(g_p['anova']['F'])}, η<sup>2</sup> = {nz(g_p['anova']['eta2'])}; Kruskal <i>H</i> = {n2(g_p['kruskal']['H'])}"],
            ["Gemini-001 (3,072-d document) — KM / Ward / HDB", "53 × 3", f"100 / 100 / {pct(100 * (1 - g_d['hdbscan_noise_M']))}", f"{nz(g_d['desc']['K-Means']['M'], 3)} / {nz(g_d['desc']['Agglomerative']['M'], 3)} / {nz(g_d['desc']['HDBSCAN']['M'], 3)}", f"{n2(g_d['desc']['K-Means']['DB_M'], 2)} / {n2(g_d['desc']['Agglomerative']['DB_M'], 2)} / {n2(g_d['desc']['HDBSCAN']['DB_M'], 2)}", f"<i>F</i> = {n2(g_d['anova']['F'])}, η<sup>2</sup> = {nz(g_d['anova']['eta2'])}; Kruskal <i>H</i> = {n2(g_d['kruskal']['H'])}"],
        ],
        note="Each seed draws <i>n</i> = 500 dialogues without replacement from <i>D</i><sub>gold</sub> (<i>n</i> = 933; 53.6% finite-population fraction). HDBSCAN metrics apply only to retained non-noise dialogues (discarding 39.1% noise on MiniLM, 35.8% on Gemini turn pool, and 25.7% on Gemini document vectors).",
        widths=[2.15, 0.55, 0.85, 1.05, 0.85, 1.05],
        align=["l", "c", "c", "c", "c", "c"],
        split=True,
    )

    rp = rprof.reindex(ARCH_REF)
    p16 = ctx["full_16_profile"]
    db_r, oe_r, rc_r = rp.loc["Decisive Booker"], rp.loc["Open Explorer"], rp.loc["Rigid-Constraint Seeker"]
    D.para(
        "<i>Sensitivity analysis, choice of k = 3 on Blocks, refined user archetypes, and hybrid prefix routing.</i> "
        "Auditing the primary whole-dialogue archetypes (<i>Direct Transactional</i>, <i>Constraint Negotiator</i>, "
        "<i>Guided Explorer</i>; Table D3) showed that whole-dialogue vectors conflate user and wizard turns, correlate "
        f"with role-players (Cramér's <i>V</i> = {nz(ctx['cramer_v'])}), and yield low early-turn routing agreement "
        f"(κ = {nz(kap_prim)}). Evaluating the 46-dimensional hybrid <i>Blocks</i> representation (PCA-20 Gemini user "
        "prefix embedding + 26 encoded numeric columns from the 13 clustering fields of the 16-field LLM behavioral "
        "schema) across truncation horizons <i>M</i> ∈ {3, 5, 7, 9, whole} and cluster counts <i>k</i> ∈ {2, ..., 8} "
        "(Appendix D, Tables D1, D5, and D6; Figure D4) demonstrated that truncating to the first <i>M</i> = 9 user "
        "messages at <b><i>k</i> = 3</b> is uniquely optimal. Specifically, on the final 46-d <i>Blocks</i> (<i>M</i> = 9) "
        "representation (Table D1, Panel B), <i>k</i> = 3 achieves the <b>lowest (best) Davies–Bouldin index (2.647 vs. "
        "2.796 at <i>k</i> = 2 and 2.729–2.784 at <i>k</i> = 4–6)</b>, highest eligible Silhouette (.094; null-calibrated "
        ".033 vs. .002–.010 at <i>k</i> = 4–6), high bootstrap resampling stability across 50 pairs of 80% golden "
        f"subsamples (<b>ARI = {nz(tr3.loc['9', 'stability_ari'])}</b> in the truncation grid [Table D5]; <b>ARI = "
        f"{nz(a9.loc[1, 'stability_ari'])}</b> with {pct(a9.loc[1, 'core_pct'], 1)} core membership at ≥ 90% co-assignment "
        f"under the independent random seed of the 6-configuration ablation [Table D6]), and balanced cluster sizes "
        f"(smallest cluster = {pct(rprof['pct'].min(), 1)} ≥ 20% floor). In contrast, <i>k</i> = 2 (DB = 2.796) collapses "
        "<i>Decisive Bookers</i> and <i>Rigid-Constraint Seekers</i> into a single undifferentiated bucket, while "
        "<i>k</i> = 4, 5, and 6 suffer a sharp drop in bootstrap stability (ARI = .589, .593, and .631) and fragment into "
        "small clusters (11.3%–12.5%, violating the 20% balanced-segment threshold). Since the Microsoft Frames dataset "
        "does not provide predefined behavioral archetype labels, we generated reference archetypes (<i>y</i><sup>(9)</sup>) "
        "through unsupervised <i>K</i>-Means (<i>k</i> = 3) clustering on the 46-dimensional hybrid <i>Blocks</i> "
        "representation (<i>X</i><sup>(9)</sup>) of the first nine user messages (see Appendix F and Table F1 for the "
        "deterministic centroid-naming protocol, and Appendix G and Table G1 for the distinct validation role of Judge "
        "LLMs). Importantly, total dialogue turns (<i>T</i>, user plus wizard turns, <i>M</i> = 14.93, <i>Mdn</i> = "
        "14.0; 96.4% ≥ 5 turns and 83.2% ≥ 9 turns) must be distinguished from user-only messages (<i>M</i>, customer "
        "turns only, <i>M</i> = 7.78, <i>Mdn</i> = 7.0; 83.2% ≥ 5 user messages and 37.6% ≥ 9 user messages): offline "
        "clustering caps input at min(user_turns, 9) to strip late checkout/abandonment turns from long sessions while "
        "retaining all user messages for shorter sessions. We subsequently trained prefix-specific multinomial Logistic "
        "Regression classifiers on <i>D</i><sub>gold</sub> (<i>n</i> = 933) to predict these nine-message reference "
        "cluster assignments using only the first <i>m</i> ∈ {3, 5, 7, 9} user messages (<i>X</i><sup>(<i>m</i>)</sup>). "
        "Because raw percentage agreement (<i>p<sub>o</sub></i>) includes expected chance agreement (<i>p<sub>e</sub></i> "
        "≈ 35.4%–36.6% given uneven cluster shares) and compares against an unsupervised cluster target rather than "
        "human labels, we report both <i>p<sub>o</sub></i> and chance-corrected Cohen's κ = (<i>p<sub>o</sub></i> − "
        "<i>p<sub>e</sub></i>) / (1 − <i>p<sub>e</sub></i>). On the held-out test partition (<i>D</i><sub>test</sub>, "
        "<i>n</i> = 401), chance-corrected prefix-to-cluster agreement increased from κ = "
        f"{nz(rt_diag.loc[3, 'cohen_kappa'], 3)} (<i>p<sub>o</sub></i> = {pct(100 * rt_diag.loc[3, 'routing_accuracy'])}, "
        "238/401, <i>p<sub>e</sub></i> = 36.6%; 87.5% on < 3 user messages) at <i>m</i> = 3 messages (≈ 5 total turns) "
        f"to κ = {nz(rt_diag.loc[5, 'cohen_kappa'], 3)} (<i>p<sub>o</sub></i> = "
        f"{pct(100 * rt_diag.loc[5, 'routing_accuracy'])}, 281/401, <i>p<sub>e</sub></i> = 35.7%; 81.8% on < 5 and "
        "67.8% on ≥ 5 user messages) at <i>m</i> = 5 messages (≈ 9 total turns, the runtime cut-off used in RQ2) and "
        f"κ = {nz(rt_diag.loc[7, 'cohen_kappa'], 3)} (<i>p<sub>o</sub></i> = "
        f"{pct(100 * rt_diag.loc[7, 'routing_accuracy'])}, 329/401, <i>p<sub>e</sub></i> = 35.5%; 93.2% on < 7 and "
        "74.6% on ≥ 7 user messages) at <i>m</i> = 7 messages (≈ 13 total turns). At <i>m</i> = 9 messages (≈ 17 total "
        f"turns), agreement reached κ = {nz(rt_diag.loc[9, 'cohen_kappa'], 3)} (<i>p<sub>o</sub></i> = "
        f"{pct(100 * rt_diag.loc[9, 'routing_accuracy'])}, 390/401, <i>p<sub>e</sub></i> = 35.4%; 96.0% on ≤ 9 and "
        "99.3% on ≥ 9 user messages), representing a same-feature boundary-consistency check between the linear "
        "Logistic Regression hyperplane and the <i>K</i>-Means Voronoi centroids on <i>X</i><sup>(9)</sup>. These "
        "results demonstrate progressively stronger early-prefix agreement with the clustering-derived reference "
        "archetypes; they do not, by themselves, establish independent human validation of the archetypes. Table 13 "
        "profiles the three refined user archetypes across all 16 schema fields: "
        f"<i>Decisive Booker</i> ({pct(db_r.pct, 1)}; high decisiveness = {n2(db_r.decisiveness)}, politeness = "
        f"{n2(db_r.politeness)}, {pct(db_r.goal_booking_pct, 1)} booking goal), <i>Open Explorer</i> ({pct(oe_r.pct, 1)}; "
        f"high destination flexibility = {n2(oe_r.destination_flexibility)} and exploration breadth = "
        f"{n2(oe_r.exploration_breadth)}, longest dialogues = {n2(oe_r.turns_M)} turns), and "
        f"<i>Rigid-Constraint Seeker</i> ({pct(rc_r.pct, 1)}; fixed destination/date constraints = "
        f"{n2(rc_r.destination_flexibility)}/{n2(rc_r.date_flexibility)}, concise {n2(rc_r.turns_M)}-turn sessions "
        f"where {pct(rc_r.no_option_pct, 1)} end without a suitable option unless rigid trade-offs are proactively resolved)."
    )
    t13_rows = [
        ["Golden / Held-out test size, <i>n</i> (%)", *[f"{int(r.n)} ({n2(r.pct, 1)}%) / {int(r1r['test_counts'][a])}" for a, r in rp.iterrows()]],
        ["Dialogue turns / User messages, <i>M</i>", *[f"{n2(r.turns_M)} ({n2(r.turns_SD)}) / {n2(r.user_turns_M)}" for _, r in rp.iterrows()]],
    ]
    for idx_f, (lab_, col_) in enumerate(feat, 1):
        t13_rows.append([f"{idx_f}. {lab_} (1–5 ordinal)", *[n2(r[col_]) for _, r in rp.iterrows()]])
    t13_rows += [
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
        t13_rows,
        note=f"Golden <i>N</i> = {s1['n_gold']}; held-out <i>N</i> = {s1['n_test']} (χ<sup>2</sup>(2) = "
             f"{n2(r1r['chi_gold_test']['chi2'])}, <i>p</i> = {nz(r1r['chi_gold_test']['p'], 3)}). Fields 1–13 are used "
             "in clustering (<i>llm_matrix</i>: 10 ordinal + 6 primary_goal + 6 secondary_goals + 4 emotional_tone = 26 "
             "numeric columns); Fields 14–16 are audit-only (excluded from clustering to prevent outcome "
             "leakage). Held-out <i>Blocks</i> prefix-to-cluster raw agreement <i>p<sub>o</sub></i> (chance-corrected κ, "
             "<i>p<sub>e</sub></i> ≈ 35.4%–36.6%) against the <i>M</i>=9 <i>K</i>-Means reference assignment: "
             "<i>m</i>=3: 59.4% (.359); <i>m</i>=5: 70.1% (.535); <i>m</i>=7: 82.0% (.722); <i>m</i>=9 (same-feature "
             "boundary consistency): 97.3% (.958).",
        widths=[2.55, 1.32, 1.32, 1.31],
        align=["l", "c", "c", "c"],
        split=True,
    )

    # ------------------------------------------------------------------ RQ2 Results
    D.heading("RQ2 Results: Cluster-Adaptive Few-Shot Prompting on Primary Versus Refined Archetypes", 2)
    sc_p = r2_prim["results"]["style_cos"]
    wd_p = r2_prim["results"]["words"]
    sc_r = r2_ref["results"]["sbert_style_cos"]
    gc_r = r2_ref["results"]["style_cos"]
    bf_r = r2_ref["results"]["bert_f1"]
    wd_r = r2_ref["results"]["words"]
    we_r = r2_ref["results"]["word_abs_err"]
    p_cs = {p["contrast"]: p for p in sc_r["pairs"]}
    p_we = {p["contrast"]: p for p in we_r["pairs"]}

    D.para(
        "Table 14 compares the repeated-measures prompting experiment (<i>N</i> = 33 held-out dialogues × 3 "
        "conditions = 99 Gemini 2.5 Flash generations) on the coarse primary archetypes versus the refined user "
        "archetypes, and Figure 6 displays the refined distributions (Holm contrasts across all six outcomes are in "
        "Appendix E, Table E3). Importantly, the <i>Cluster-Adaptive Few-Shot</i> condition evaluates a <b>combined "
        "personalization package</b> that couples archetype-partitioned FAISS exemplar retrieval (<i>k</i> = 3 "
        "slot-masked exemplars from the routed sub-index) with an explicit archetype pacing directive in the system "
        "prompt. On coarse primary archetypes with an unprojected 3-turn router (39.4% accuracy, κ = .24), style "
        f"convergence was non-significant, <i>F</i>({n2(sc_p['anova']['df1_gg'])}, {n2(sc_p['anova']['df2_gg'])}) = "
        f"{n2(sc_p['anova']['F'])}, <i>p</i> = {nz(sc_p['anova']['p_gg'], 3)}, η<sub><i>p</i></sub><sup>2</sup> = "
        f"{nz(sc_p['anova']['eta2_partial'])}, though few-shot prompting calibrated length (15.1–16.3 vs. 27.6 words, "
        f"<i>F</i> = {n2(wd_p['anova']['F'])}, <i>p</i> < .001; Figure E2). Re-running on the <b>Refined User "
        "Archetypes</b> with the <i>Blocks</i> router (<i>M</i> = 5 user messages, 70.1% raw agreement, κ = .535) "
        "<b>rejected <i>H</i><sub>02</sub> (<i>p</i> < .001) on structural style and pacing calibration</b>: "
        "de-lexicalized SBERT style convergence differed significantly under Greenhouse–Geisser correction "
        f"(Greenhouse & Geisser, 1959), <i>F</i>({n2(sc_r['anova']['df1_gg'])}, {n2(sc_r['anova']['df2_gg'])}) = "
        f"{n2(sc_r['anova']['F'])}, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = "
        f"{nz(sc_r['anova']['eta2_partial'])}, and Friedman testing, χ<sup>2</sup>(2) = "
        f"{n2(sc_r['friedman']['chi2'])}, <i>p</i> = {nz(sc_r['friedman']['p'], 3)}. Cluster-Adaptive Few-Shot "
        f"(<i>M</i> = {nz(sc_r['desc']['Cluster-Adaptive Few-Shot'][0], 3)}, <i>SD</i> = "
        f"{nz(sc_r['desc']['Cluster-Adaptive Few-Shot'][1], 3)}) significantly outperformed Static Few-Shot "
        f"(<i>M</i> = {nz(sc_r['desc']['Static Few-Shot'][0], 3)}, <i>t</i>(32) = "
        f"{n2(p_cs['Cluster-Adaptive Few-Shot vs. Static Few-Shot']['t'])}, <i>p</i><sub>Holm</sub> < .001, "
        f"<i>d<sub>z</sub></i> = {n2(p_cs['Cluster-Adaptive Few-Shot vs. Static Few-Shot']['d_z'])}) and Zero-Shot "
        f"(<i>M</i> = {nz(sc_r['desc']['Zero-Shot'][0], 3)}, <i>t</i>(32) = "
        f"{n2(p_cs['Cluster-Adaptive Few-Shot vs. Zero-Shot']['t'])}, <i>p</i><sub>Holm</sub> = "
        f"{nz(p_cs['Cluster-Adaptive Few-Shot vs. Zero-Shot']['p_holm'], 3)}, <i>d<sub>z</sub></i> = "
        f"{n2(p_cs['Cluster-Adaptive Few-Shot vs. Zero-Shot']['d_z'])}), and cut archetype pacing error from "
        f"{n2(we_r['desc']['Zero-Shot'][0])} (Zero-Shot) and {n2(we_r['desc']['Static Few-Shot'][0])} (Static) to "
        f"<b>{n2(we_r['desc']['Cluster-Adaptive Few-Shot'][0])} words</b> (<i>F</i> = {n2(we_r['anova']['F'])}, "
        f"<i>p</i> = {nz(we_r['anova']['p_gg'], 3)}; Friedman χ<sup>2</sup>(2) = {n2(we_r['friedman']['chi2'])}, "
        "<i>p</i> < .001; Holm <i>p</i> = .004 vs. Zero-Shot, <i>p</i> = .024 vs. Static). By contrast, generic "
        "semantic similarity metrics—including Gemini 3,072-d cosine ("
        f"{nz(gc_r['desc']['Cluster-Adaptive Few-Shot'][0], 3)} vs. {nz(gc_r['desc']['Zero-Shot'][0], 3)}, "
        f"<i>F</i> = {n2(gc_r['anova']['F'])}, <i>p</i> = {nz(gc_r['anova']['p_gg'], 3)}) and token-level BERTScore "
        f"F<sub>1</sub> ({nz(bf_r['desc']['Cluster-Adaptive Few-Shot'][0], 3)} vs. "
        f"{nz(bf_r['desc']['Zero-Shot'][0], 3)}, <i>F</i> = {n2(bf_r['anova']['F'])}, <i>p</i> = "
        f"{nz(bf_r['anova']['p_gg'], 3)}; Table E3)—did not differ significantly across conditions, confirming that "
        "archetype-adaptive prompting selectively calibrates discourse structure and turn pacing without distorting "
        "underlying domain semantics."
    )
    D.table(
        "Repeated-Measures Comparison of Prompting Strategies on Primary Versus Refined User Archetypes (RQ2)",
        ["Experiment and outcome metric", "Zero-Shot <i>M</i> (<i>SD</i>)", "Static Few-Shot <i>M</i> (<i>SD</i>)", "Cluster-Adaptive <i>M</i> (<i>SD</i>)", "RM-ANOVA <i>F</i> (GG)", "<i>p</i> (GG)", "η<sub><i>p</i></sub><sup>2</sup>"],
        [
            [
                "Primary archetypes (<i>M</i>=3 prefix, κ=.24) — Style cosine",
                f"{nz(sc_p['desc']['Zero-Shot'][0], 3)} ({nz(sc_p['desc']['Zero-Shot'][1], 3)})",
                f"{nz(sc_p['desc']['Static Few-Shot'][0], 3)} ({nz(sc_p['desc']['Static Few-Shot'][1], 3)})",
                f"{nz(sc_p['desc']['Cluster-Adaptive Few-Shot'][0], 3)} ({nz(sc_p['desc']['Cluster-Adaptive Few-Shot'][1], 3)})",
                n2(sc_p["anova"]["F"]),
                pv_cell(sc_p["anova"]["p_gg"]),
                nz(sc_p["anova"]["eta2_partial"]),
            ],
            [
                "Primary archetypes — Response length (words)",
                f"{n2(wd_p['desc']['Zero-Shot'][0], 1)} ({n2(wd_p['desc']['Zero-Shot'][1], 1)})",
                f"{n2(wd_p['desc']['Static Few-Shot'][0], 1)} ({n2(wd_p['desc']['Static Few-Shot'][1], 1)})",
                f"{n2(wd_p['desc']['Cluster-Adaptive Few-Shot'][0], 1)} ({n2(wd_p['desc']['Cluster-Adaptive Few-Shot'][1], 1)})",
                n2(wd_p["anova"]["F"]),
                pv_cell(wd_p["anova"]["p_gg"]),
                nz(wd_p["anova"]["eta2_partial"]),
            ],
            [
                "Refined archetypes (<i>M</i>=5 Blocks, κ=.535) — SBERT style cosine",
                f"{nz(sc_r['desc']['Zero-Shot'][0], 3)} ({nz(sc_r['desc']['Zero-Shot'][1], 3)})",
                f"{nz(sc_r['desc']['Static Few-Shot'][0], 3)} ({nz(sc_r['desc']['Static Few-Shot'][1], 3)})",
                f"{nz(sc_r['desc']['Cluster-Adaptive Few-Shot'][0], 3)} ({nz(sc_r['desc']['Cluster-Adaptive Few-Shot'][1], 3)})",
                n2(sc_r["anova"]["F"]),
                pv_cell(sc_r["anova"]["p_gg"]),
                nz(sc_r["anova"]["eta2_partial"]),
            ],
            [
                "Refined archetypes — Gemini 3,072-d style cosine",
                f"{nz(gc_r['desc']['Zero-Shot'][0], 3)} ({nz(gc_r['desc']['Zero-Shot'][1], 3)})",
                f"{nz(gc_r['desc']['Static Few-Shot'][0], 3)} ({nz(gc_r['desc']['Static Few-Shot'][1], 3)})",
                f"{nz(gc_r['desc']['Cluster-Adaptive Few-Shot'][0], 3)} ({nz(gc_r['desc']['Cluster-Adaptive Few-Shot'][1], 3)})",
                n2(gc_r["anova"]["F"]),
                pv_cell(gc_r["anova"]["p_gg"]),
                nz(gc_r["anova"]["eta2_partial"]),
            ],
            [
                "Refined archetypes — Token-level BERTScore F<sub>1</sub>",
                f"{nz(bf_r['desc']['Zero-Shot'][0], 3)} ({nz(bf_r['desc']['Zero-Shot'][1], 3)})",
                f"{nz(bf_r['desc']['Static Few-Shot'][0], 3)} ({nz(bf_r['desc']['Static Few-Shot'][1], 3)})",
                f"{nz(bf_r['desc']['Cluster-Adaptive Few-Shot'][0], 3)} ({nz(bf_r['desc']['Cluster-Adaptive Few-Shot'][1], 3)})",
                n2(bf_r["anova"]["F"]),
                pv_cell(bf_r["anova"]["p_gg"]),
                nz(bf_r["anova"]["eta2_partial"]),
            ],
            [
                "Refined archetypes — Pacing calibration error (words)",
                f"{n2(we_r['desc']['Zero-Shot'][0], 2)} ({n2(we_r['desc']['Zero-Shot'][1], 2)})",
                f"{n2(we_r['desc']['Static Few-Shot'][0], 2)} ({n2(we_r['desc']['Static Few-Shot'][1], 2)})",
                f"{n2(we_r['desc']['Cluster-Adaptive Few-Shot'][0], 2)} ({n2(we_r['desc']['Cluster-Adaptive Few-Shot'][1], 2)})",
                n2(we_r["anova"]["F"]),
                pv_cell(we_r["anova"]["p_gg"]),
                nz(we_r["anova"]["eta2_partial"]),
            ],
            [
                "Refined archetypes — Response length (words)",
                f"{n2(wd_r['desc']['Zero-Shot'][0], 1)} ({n2(wd_r['desc']['Zero-Shot'][1], 1)})",
                f"{n2(wd_r['desc']['Static Few-Shot'][0], 1)} ({n2(wd_r['desc']['Static Few-Shot'][1], 1)})",
                f"{n2(wd_r['desc']['Cluster-Adaptive Few-Shot'][0], 1)} ({n2(wd_r['desc']['Cluster-Adaptive Few-Shot'][1], 1)})",
                n2(wd_r["anova"]["F"]),
                pv_cell(wd_r["anova"]["p_gg"]),
                nz(wd_r["anova"]["eta2_partial"]),
            ],
        ],
        note="<i>N</i> = 33 held-out dialogues per experiment (99 generations each; <i>gemini-2.5-flash</i>). Cluster-Adaptive combines archetype-partitioned FAISS exemplars with an explicit archetype pacing directive. GG = Greenhouse–Geisser correction.",
        widths=[2.15, 0.95, 0.95, 0.95, 0.5, 0.5, 0.5],
        align=["l", "c", "c", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "Style Convergence and Archetype Pacing Calibration Across Prompting Conditions on Refined User Archetypes",
        os.path.join(FIG_FIN, "fig_rq2_refined_results.png"),
        note="<i>N</i> = 33 held-out dialogues. Panel A: De-lexicalized SBERT style convergence cosine. Panel B: Absolute pacing error (words).",
        width=4.6,
    )

    # ------------------------------------------------------------------ RQ3 Results
    D.heading("RQ3 Results: 2 × 2 Factorial Evaluation of Declarative Rules and Adaptive Prompting", 2)
    jr = r3_fin["judge_reliability_flash_vs_pro"]
    c3 = r3_fin["cell_means"]
    D.para(
        "Table 15 and Figure 7 present the 2 × 2 factorial experiment across <i>N</i> = 144 evaluations (36 stratified "
        "held-out dialogues—18 policy-violating and 18 compliant—evaluated across all four conditions, <i>n</i> = "
        "36/cell), where the <i>Rules Active</i> condition represents an integrated three-component governance package "
        "(pre-generation declarative YAML rule checking, [SLOT] exemplar masking, and post-generation regex leakage "
        "sanitization). Cross-model inter-rater reliability on a stratified 48-unit subsample between "
        f"<i>gemini-2.5-flash</i> and independent <i>gemini-2.5-pro</i> reached {pct(100 * jr['raw_agreement'], 1)} raw "
        f"agreement and Cohen's κ = {nz(jr['cohen_kappa'], 3)} (PABAK = {nz(jr['pabak'], 3)}; Table C3). Four findings "
        "<b>reject <i>H</i><sub>03</sub> (<i>p</i> < .001)</b>: (1) separating <b>Rule Adherence</b> into its two "
        "constituent scenario classes reveals that <b>Violation Enforcement Rate (Sensitivity, <i>n</i> = 18 violating "
        "cases/cell)</b> rose from 5.6% (<i>SD</i> = 23.6%) under both <i>Rules Off</i> cells to <b>100.0%</b> "
        "(<i>Rules Active × Zero-Shot</i>) and <b>97.2%</b> (<i>SD</i> = 11.8%, <i>Rules Active × Cluster-Adaptive</i>), "
        f"yielding a massive rules main effect, <i>F</i>(1, 68) = {n2(r3_rar_anova['viol_F_rules'])}, <i>p</i> < .001, "
        f"η<sub><i>p</i></sub><sup>2</sup> = {nz(r3_rar_anova['viol_eta2_rules'], 3)}, whereas <b>Compliant-Case "
        "Acceptance Rate (Specificity, 1 − false_block, <i>n</i> = 18 compliant cases/cell)</b> remained statistically "
        "indistinguishable between <i>Rules Off</i> (94.4%, 17/18) and <i>Rules Active</i> (88.9%, 16/18), "
        f"<i>F</i>(1, 68) = {n2(r3_rar_anova['comp_F_rules'])}, <i>p</i> = {nz(r3_rar_anova['comp_p_rules'], 3)}, "
        f"η<sub><i>p</i></sub><sup>2</sup> = {nz(r3_rar_anova['comp_eta2_rules'], 3)}, confirming that strict policy "
        "enforcement does not induce significant false-positive blocking; pooled across all 36 cases per cell, "
        f"<b>Overall Rule-Decision Accuracy</b> rose from .500 to .944/.931, rules main effect <i>F</i>(1, 140) = "
        f"{n2(r3_a['rule_adherence']['effects']['rules_mode']['F'])}, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> "
        f"= {nz(r3_a['rule_adherence']['effects']['rules_mode']['eta2_partial'])} (HC3 <i>F</i> = "
        f"{n2(r3_a['rule_adherence']['effects']['rules_mode']['F_hc3'])}; ART <i>F</i> = "
        f"{n2(r3_a['rule_adherence']['effects']['rules_mode']['F_art'])}, both <i>p</i> < .001), with zero prompting "
        "main effect (<i>F</i> = 0.01, <i>p</i> = .916); (2) <b>Exemplar Entity Leakage Rate</b> showed a strong "
        f"rules × prompting interaction, <i>F</i>(1, 140) = {n2(r3_a['leakage_rate']['effects']['interaction']['F'])}, "
        f"<i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = "
        f"{nz(r3_a['leakage_rate']['effects']['interaction']['eta2_partial'])} (Sum-coded HC3 <i>F</i> = "
        f"{n2(r3_a['leakage_rate']['effects']['interaction']['F_hc3'])}; ART <i>F</i> = "
        f"{n2(r3_a['leakage_rate']['effects']['interaction']['F_art'])}, both <i>p</i> < .001), where unguarded "
        "<i>Cluster-Adaptive Few-Shot</i> leaked stale exemplar entities at a .359 rate (20/36 = 55.6% incidence) but "
        "<i>Rules Active × Cluster-Adaptive</i> reduced detected leakage in the evaluated sample to <b>0.0% (.000, 0/36 "
        "incidence; simple-effect Welch <i>t</i>(35) = 5.90, <i>p</i> < .001, Mann–Whitney <i>U</i> = 1008.0, "
        "<i>p</i> < .001, Fisher's exact <i>p</i> = 4.68 × 10<sup>−8</sup>)</b>; (3) <b>Slot Coverage F<sub>1</sub></b> "
        f"rose from .208/.485 to <b>.977/.952</b> under active rules, <i>F</i>(1, 140) = "
        f"{n2(r3_a['slot_f1']['effects']['rules_mode']['F'])}, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = "
        f"{nz(r3_a['slot_f1']['effects']['rules_mode']['eta2_partial'])}; and (4) <b>Style Alignment</b> was "
        f"significantly boosted by Cluster-Adaptive Few-Shot, <i>F</i>(1, 140) = "
        f"{n2(r3_a['style_cos']['effects']['prompt_mode']['F'])}, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = "
        f"{nz(r3_a['style_cos']['effects']['prompt_mode']['eta2_partial'])}, making <b>Rules Active × Cluster-Adaptive "
        "Few-Shot</b> the unique Pareto-optimal cell."
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
    for eff_key, eff_name in [("rules_mode", "ANOVA Main Effect: Rules Mode"), ("prompt_mode", "ANOVA Main Effect: Prompting Mode"), ("interaction", "ANOVA Interaction: Rules × Prompting")]:
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
        "Cell Means and 2 × 2 Factorial ANOVA Results for RQ3 Outcomes (N = 144)",
        ["Experimental cell or ANOVA effect", "<i>n</i> or <i>df</i>", "Rule Acc. <i>M</i> (<i>SD</i>) | Sens. / Spec.", "Exemplar leakage <i>M</i> (<i>SD</i>) / Inc. %", "Slot coverage F<sub>1</sub> <i>M</i> (<i>SD</i>)", "Style alignment <i>M</i> (<i>SD</i>)"],
        r3_rows,
        note="Rule Acc. = overall rule-decision accuracy (<i>n</i> = 36/cell); Sens. = violation enforcement sensitivity on violating scenarios (<i>n</i> = 18/cell; Rules <i>F</i>(1, 68) = 498.78, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = .880); Spec. = compliant-case acceptance specificity (1 − false_block, <i>n</i> = 18/cell; Rules <i>F</i>(1, 68) = 0.69, <i>p</i> = .408); Inc. % = responses with ≥ 1 leaked entity. Dual-judge κ = .917. For exemplar leakage, because three of the four balanced 2 × 2 cells (<i>n</i> = 36/cell) are identically .000 and only <i>Rules Off × Cluster-Adaptive</i> is non-zero (<i>M</i> = .35926), all three orthogonal +1/−1 Sum-coded contrasts <i>c<sub>A</sub></i> = (+1,+1,−1,−1), <i>c<sub>B</sub></i> = (−1,+1,−1,+1), and <i>c<sub>AB</sub></i> = (+1,−1,−1,+1) have identical contrast sum of squares <i>SS</i> = <i>n</i>(Σ<i>c<sub>j</sub>Ȳ<sub>j</sub></i>)<sup>2</sup> / Σ<i>c<sub>j</sub></i><sup>2</sup> = 36(.35926)<sup>2</sup> / 4 = 1.162 (equivalently, while the difference-of-differences interaction estimate −.359 is twice the marginal main-effect difference ±.180, its standard error √(4σ<sup>2</sup>/<i>n</i>) is also twice the marginal standard error √(σ<sup>2</sup>/<i>n</i>), yielding identical <i>t</i> = ±5.901, OLS <i>F</i>(1, 140) = <i>t</i><sup>2</sup> = 34.82, η<sub><i>p</i></sub><sup>2</sup> = .199, and Sum-coded HC3 <i>F</i> = 33.85, <i>p</i> < .001), whereas rank-based ART separates the main effects (<i>F</i> = 43.48) from the interaction (ART <i>F</i> = 2148.81, <i>p</i> < .001; simple-effect contrast within Cluster-Adaptive: Welch <i>t</i>(35) = 5.90, <i>p</i> < .001, Fisher's exact <i>p</i> = 4.68 × 10<sup>−8</sup>).",
        widths=[1.75, 0.52, 1.25, 1.13, 0.95, 0.9],
        align=["l", "c", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "2 × 2 Factorial Interaction Profiles for Rule Adherence, Exemplar Leakage, Slot Coverage F1, and Style Alignment",
        os.path.join(FIG_FIN, "fig_rq3_factorial_results.png"),
        note="<i>N</i> = 144 held-out units (<i>n</i> = 36 per cell). Error bars represent 95% confidence intervals.",
        width=4.7,
    )

    # ------------------------------------------------------------------ RQ4 Results
    D.heading("RQ4 Results: 2 × 3 Multi-Turn Simulation of Turn Economy Across Archetypes", 2)
    pv4 = r4_fin["persona_validation"]
    c4 = r4_fin["cell_means"]
    con4 = {r["archetype"]: r for r in r4_fin["archetype_contrasts"]}
    D.para(
        "Table 16 and Figure 8 report the 2 × 3 between-subjects multi-turn simulation across <b><i>N</i> = 180 unique, "
        "independent held-out seed dialogues</b> (60 per archetype, partitioned into <i>n</i> = 30 distinct dialogues for "
        "<i>Zero-Shot</i> and <i>n</i> = 30 distinct dialogues for <i>Cluster-Adaptive Few-Shot</i> with zero overlap; "
        "human corpus baseline is in Appendix E, Table E5 and Figure E3). In this experiment, <i>total_turns</i> counts "
        "total conversational turns (user plus assistant messages) until the simulated traveler issues "
        "<code>[ACCEPT_BOOKING]</code>, and <i>Cluster-Adaptive Few-Shot</i> evaluates the combined package of the "
        "<b>Verified Informed Slot Ledger</b> (forbidding re-asking any previously stated slot) and <b>archetype-specific "
        "turn-economy policies</b>. Blind evaluation of 45 simulated transcripts by <i>gemini-2.5-pro</i> confirmed 95.6% "
        f"within-simulation persona fidelity (43/45 vs. 33.3% chance, binomial <i>p</i> < .001, κ = "
        f"{nz(pv4['cohen_kappa'], 3)}; Table C3). On log-transformed turns to goal completion, the 2 × 3 between-subjects "
        f"ANOVA <b>rejected <i>H</i><sub>04</sub> (<i>p</i> < .001)</b>, with significant main effects of prompting, "
        f"<i>F</i>(1, 174) = {n2(r4_a['log_turns']['effects']['prompt_mode']['F'])}, <i>p</i> < .001, "
        f"η<sub><i>p</i></sub><sup>2</sup> = {nz(r4_a['log_turns']['effects']['prompt_mode']['eta2_partial'])}, and "
        f"archetype, <i>F</i>(2, 174) = {n2(r4_a['log_turns']['effects']['target_archetype']['F'])}, <i>p</i> = "
        f"{nz(r4_a['log_turns']['effects']['target_archetype']['p'], 3)}, η<sub><i>p</i></sub><sup>2</sup> = "
        f"{nz(r4_a['log_turns']['effects']['target_archetype']['eta2_partial'])}, plus a <b>significant prompting × "
        f"archetype interaction</b>, <i>F</i>(2, 174) = {n2(r4_a['log_turns']['effects']['interaction']['F'])}, "
        f"<i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = "
        f"{nz(r4_a['log_turns']['effects']['interaction']['eta2_partial'])} (HC3 <i>F</i> = "
        f"{n2(r4_a['log_turns']['effects']['interaction']['F_hc3'])}; ART <i>F</i> = "
        f"{n2(r4_a['log_turns']['effects']['interaction']['F_art'])}, both <i>p</i> < .001). Cluster-Adaptive Few-Shot "
        "compressed turns most strongly for <b>Rigid-Constraint Seekers</b> (−42.7%, 8.73 → 5.00 turns, Welch "
        f"<i>t</i><sub>log</sub> = {n2(con4['Rigid-Constraint Seeker']['t_welch_log'])}, <i>p</i> < .001, <i>d</i> = "
        f"{n2(con4['Rigid-Constraint Seeker']['cohen_d'])}) by proactively presenting both 4-star exact-date (Option A) "
        "and 5-star flexible-date (Option D) trade-offs when the exact-date 5-star option (Option C) exceeded budget, "
        f"followed by <b>Decisive Bookers</b> (−34.2%, 7.60 → 5.00 turns, <i>t</i><sub>log</sub> = "
        f"{n2(con4['Decisive Booker']['t_welch_log'])}, <i>d</i> = {n2(con4['Decisive Booker']['cohen_d'])}) and "
        f"<b>Open Explorers</b> (−29.5%, 7.47 → 5.27 turns, <i>t</i><sub>log</sub> = "
        f"{n2(con4['Open Explorer']['t_welch_log'])}, <i>d</i> = {n2(con4['Open Explorer']['cohen_d'])}). Notably, the "
        "<i>M</i> = 5.00 (<i>SD</i> = 0.00) result for <i>Decisive Bookers</i> and <i>Rigid-Constraint Seekers</i> under "
        "<i>Cluster-Adaptive Few-Shot</i> reflects a structural protocol floor effect: because every session requires "
        "Turn 1 (user states core trip slots), Turn 2 (assistant asks for the single remaining unknown slot, budget), "
        "Turn 3 (user states budget), Turn 4 (assistant presents tailored package offer[s]), and Turn 5 (user issues "
        "<code>[ACCEPT_BOOKING]</code>, guarded by <code>ex_idx ≥ 1</code> and budget confirmation in "
        "<i>step4_rq4_simulation.py</i>), 5 total conversational turns is the theoretical minimum completion length, "
        "which 30/30 episodes in those two cells achieved on the first offer turn (motivating our paired HC3, ART, and "
        "Mann–Whitney <i>U</i> checks). Redundant Elicitation Rate dropped from .194 (DB), .061 (OE), and .072 (RCS) in "
        "Zero-Shot to <b>0.000</b> across all archetypes in Cluster-Adaptive Few-Shot, main effect <i>F</i>(1, 174) = "
        f"{n2(r4_a['rer']['effects']['prompt_mode']['F'])}, <i>p</i> < .001, interaction <i>F</i>(2, 174) = "
        f"{n2(r4_a['rer']['effects']['interaction']['F'])}, <i>p</i> < .001."
    )

    r4_rows = []
    for a in ARCH_REF:
        z_row = next(r for r in c4 if r["target_archetype"] == a and r["prompt_mode"] == "Zero-Shot")
        c_row = next(r for r in c4 if r["target_archetype"] == a and r["prompt_mode"] == "Cluster-Adaptive Few-Shot")
        cn = con4[a]
        r4_rows.append([
            f"{a} — Zero-Shot (<i>n</i> = 30)",
            f"{n2(z_row['turns_M'])} ({n2(z_row['turns_SD'])})",
            f"{n2(z_row['log_turns_M'], 3)} ({n2(z_row['log_turns_SD'], 3)})",
            f"{nz(z_row['rer_M'], 3)} ({nz(z_row['rer_SD'], 3)})",
            "—",
            "—",
        ])
        r4_rows.append([
            f"{a} — Cluster-Adaptive (<i>n</i> = 30)",
            f"{n2(c_row['turns_M'])} ({n2(c_row['turns_SD'])})",
            f"{n2(c_row['log_turns_M'], 3)} ({n2(c_row['log_turns_SD'], 3)})",
            f"{nz(c_row['rer_M'], 3)} ({nz(c_row['rer_SD'], 3)})",
            f"−{n2(cn['turn_reduction_turns'])} (−{pct(cn['turn_reduction_pct'], 1)})",
            f"<i>t</i>={n2(cn['t_welch_log'])} (< .001), <i>d</i>={n2(cn['cohen_d'])}",
        ])
    for eff_key, eff_name in [("prompt_mode", "ANOVA Main Effect: Prompting Mode"), ("target_archetype", "ANOVA Main Effect: Refined Archetype"), ("interaction", "ANOVA Interaction: Prompting × Archetype")]:
        e_tt = r4_a["total_turns"]["effects"][eff_key]
        e_lt = r4_a["log_turns"]["effects"][eff_key]
        e_rr = r4_a["rer"]["effects"][eff_key]
        df_s = f"{int(e_lt['df1'])}, {int(e_lt['df2'])}"
        r4_rows.append([
            f"{eff_name} (<i>df</i> = {df_s})",
            f"<i>F</i>={n2(e_tt['F'])} ({pv_cell(e_tt['p'])}), η<sub><i>p</i></sub><sup>2</sup>={nz(e_tt['eta2_partial'])}",
            f"<i>F</i>={n2(e_lt['F'])} ({pv_cell(e_lt['p'])}), η<sub><i>p</i></sub><sup>2</sup>={nz(e_lt['eta2_partial'])}",
            f"<i>F</i>={n2(e_rr['F'])} ({pv_cell(e_rr['p'])}), η<sub><i>p</i></sub><sup>2</sup>={nz(e_rr['eta2_partial'])}",
            f"HC3 <i>F</i><sub>log</sub>={n2(e_lt['F_hc3'])} ({pv_cell(e_lt['p_hc3'])})",
            f"ART <i>F</i><sub>log</sub>={n2(e_lt['F_art'])} ({pv_cell(e_lt['p_art'])})",
        ])
    D.table(
        "Cell Means, Archetype Contrasts, and 2 × 3 Factorial ANOVA Results for Multi-Turn Turn Economy (N = 180)",
        ["Archetype × Prompting cell or ANOVA effect", "Total turns <i>M</i> (<i>SD</i>)", "Log turns <i>M</i> (<i>SD</i>)", "RER <i>M</i> (<i>SD</i>)", "Turn reduction / HC3 check", "Welch contrast / ART check"],
        r4_rows,
        note="<i>N</i> = 180 distinct held-out seed dialogues (<i>n</i> = 30 unique dialogues/cell; 100.0% goal completion). Total turns = user + assistant messages (protocol minimum = 5.00 turns: U1 → A1 → U2 → A2 → U3). Within-simulation persona fidelity audit (<i>gemini-2.5-pro</i>, <i>n</i> = 45): 95.6% accuracy, κ = .933.",
        widths=[1.85, 0.9, 0.9, 0.85, 1.0, 1.0],
        align=["l", "c", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "Dialogue Turn Economy and Redundant Elicitation Rate by User Archetype and Prompting Strategy",
        os.path.join(FIG_FIN, "fig_rq4_turn_economy_results.png"),
        note="<i>N</i> = 180 simulations (<i>n</i> = 30/cell). Panel A: Mean turns to goal completion. Panel B: Mean Redundant Elicitation Rate (RER).",
        width=4.6,
    )

    # ------------------------------------------------------------------ Synthesis
    D.heading("Technical Interpretation, Business Significance, and Synthesis of Conclusions", 2)
    D.para(
        "<i>Technical synthesis across RQ1–RQ4.</i> Together, the four experiments form an integrated four-stage "
        "research progression. First, RQ1 and RQ2 demonstrate that <b>in-context style adaptation is bounded by upstream "
        "representation and routing quality</b>: whole-dialogue primary archetypes suffered from outcome confounding and "
        "near-chance early routing (39.4%, κ = .24), yielding a null RQ2 style effect (<i>p</i> = .211); truncating to "
        "opening user behavior via the 46-d <i>Blocks</i> representation (bootstrap ARI = .89/.87) and routing in that "
        "exact space (70.1% raw agreement, κ = .535 at <i>m</i> = 5; 97.3% same-feature boundary consistency, κ = .958 at "
        "<i>m</i> = 9) unlocked significant structural style convergence on de-lexicalized SBERT cosine (<i>p</i> < .001, "
        "η<sub><i>p</i></sub><sup>2</sup> = .234) and reduced pacing error from 10.12 to 3.87 words (<i>p</i> = .007) "
        "while preserving semantic content (Gemini cosine and BERTScore F<sub>1</sub> <i>p</i> ≥ .315). Second, RQ3 "
        "demonstrates <b>functional orthogonality with protective interaction</b>: adaptive prompting governs discourse "
        "style (<i>F</i> = 24.00, <i>p</i> < .001), whereas the declarative governance layer governs policy violation "
        "enforcement sensitivity (5.6% → 98.6%, <i>F</i> = 498.78, <i>p</i> < .001; overall accuracy <i>F</i> = 43.92, "
        "<i>p</i> < .001) and slot grounding (<i>F</i> = 489.52, <i>p</i> < .001) while reducing the 35.9% entity "
        "leakage (55.6% incidence) of unguarded few-shot exemplars to zero detected leakage in the evaluated sample. "
        "Third, RQ4 demonstrates across 180 independent multi-turn simulations that pairing archetype-tailored "
        "recommendation policies with a Verified Informed Slot Ledger compresses total conversational turns by "
        "29.5%–42.7% and eliminates redundant slot questions."
    )
    D.para(
        "<i>Practical business significance (illustrative operational projection).</i> As an illustrative operational "
        "scenario, if an online travel agency or hospitality contact center handling 1,000,000 monthly sessions achieved "
        "a comparable turn reduction to that observed in the RQ4 simulation—reducing mean conversation length from 7.93 "
        "total turns (Zero-Shot) to 5.09 total turns (Cluster-Adaptive), a 35.8% reduction (2.84 turns per session)—it "
        "would save approximately 2.84 million message-generation calls per month, lowering inference compute and "
        "interaction latency by roughly one-third. Simultaneously, reducing redundant slot questions (10.9% → 0.0% in "
        "simulation), preventing exemplar price/promo leakage (55.6% incidence → 0.0% detected), and raising policy "
        "violation enforcement sensitivity from 5.6% to 98.6% (while maintaining 88.9% compliant-case acceptance) "
        "directly targets key drivers of customer drop-off and compliance risk."
    )

    # ================================================================== 6. IMPLEMENTATION, LIMITATIONS, AND FUTURE SCOPE
    D.heading("Implementation, Limitations, and Future Scope", 1)
    D.heading("Deployment Architecture, System Integration, and Real-World Use Case", 2)
    D.para(
        "<i>Enterprise deployment and integration.</i> The pipeline (<i>src/final_pipeline/</i>) deploys as a stateless "
        "Python microservice between an OTA's WebSocket chat gateway and its reservation API. Active sessions store "
        "the canonical <i>DialogueTrajectory</i> and <i>Verified Informed Slot Ledger</i> in Redis, query in-memory "
        "<i>faiss-cpu</i> archetype sub-indices (< 2 ms), run deterministic YAML policy checks via "
        "<i>src/rule_engine.py</i> (< 1 ms), and call <i>gemini-2.5-flash</i> with post-generation entity verification."
    )
    D.para(
        "<i>Real-world use case.</i> When a traveler states, <i>'I want a 10-day trip from Chicago to Tokyo departing "
        "in 10 days for 2 adults with a 5-star hotel under $2,200,'</i> a static chatbot asks repetitive slot "
        "questions and misses the 15-day visa lead-time rule. Under our deployed system: (1) <i>RefinedArchetypeRouter</i> "
        "routes the session to <i>Rigid-Constraint Seeker</i>; (2) the slot ledger locks all five stated slots against "
        "re-asking; (3) <i>RuleEngine</i> flags <i>RULE_VISA_LEAD_TIME</i> (< 15 days) and detects that the exact-date "
        "5-star package ($2,596) exceeds $2,200; and (4) the assistant immediately notifies the user of the 15-day "
        "visa requirement while presenting both the 4-star package ($1,936) and the flexible-date 5-star package "
        "($2,068) within budget, completing the booking in 5 turns with zero compliance risk."
    )

    D.heading("Computational Reproducibility and Operational Requirements", 2)
    D.para(
        "All code, random seeds (seed = 42), prompts, and JSONL caches (<i>data/interim/*.jsonl</i>, "
        f"<i>data/final/*.jsonl</i>) are versioned at {REPO}. Re-running the entire study from cached responses on a "
        "standard laptop (Apple M-series or 4-core CPU, 16 GB RAM, Python 3.11) completes in under 4 minutes at zero "
        "API cost. Cold regeneration of all ~8,900 Gemini API calls across RQ1–RQ4 completes in ~35 minutes using 8–12 "
        "workers and costs under $4.50 USD at standard Gemini 2.5 Flash/Pro pricing."
    )

    D.heading("Study Limitations and Threats to Validity", 2)
    D.para(
        "Five limitations bound this study: (1) <b>continuous archetype geometry and unsupervised reference labels</b>, "
        "as modest <i>K</i>-Means Silhouette scores (.094 on 46-d <i>Blocks</i>; .147–.161 across MiniLM and Gemini "
        "embeddings) indicate that traveler styles form a continuous behavioral manifold rather than discrete islands, "
        "and prefix routing κ (.535 at <i>m</i> = 5; .958 same-feature boundary consistency at <i>m</i> = 9) is evaluated "
        "against unsupervised <i>M</i> = 9 <i>K</i>-Means reference clusters rather than external human persona labels; "
        "(2) <b>early-turn routing latency</b>, since moderate-to-high <i>Blocks</i> routing requires 5–9 user messages, "
        "leaving Turn 1 cold-start routing noisy; (3) <b>bundled multi-component treatments in RQ2, RQ3, and RQ4</b>, "
        "since RQ2 evaluated <i>Cluster-Adaptive Few-Shot</i> as a joint package (archetype-partitioned FAISS exemplars + "
        "routed archetype pacing directive), RQ3 evaluated <i>Rules Active</i> as a joint governance package (declarative "
        "<i>RuleEngine</i> + [SLOT] masking + post-generation regex sanitization), and RQ4 evaluated the <i>Verified "
        "Informed Slot Ledger</i> jointly with archetype-specific turn-economy policies; (4) <b>corpus and synthetic "
        "Tier-2 scope</b>, because Frames uses role-players and Tier-2 rules (visa, passport, discount caps) required "
        "synthetic injection in RQ3; and (5) <b>simulated users and protocol floor in RQ4</b>, where cooperative LLM "
        "user simulators (validated for within-simulation persona fidelity at 95.6%, κ = .933, rather than live human "
        "traffic) and the 5-turn minimum protocol boundary (<i>M</i> = 5.00, <i>SD</i> = 0.00 for two cells) may "
        "overstate turn reductions relative to noisy production sessions."
    )

    D.heading("Future Scope and Research Extensions", 2)
    D.para(
        "Future doctoral research on <i>Dialogue Clustering and Methodologies to be Adapted for Human-Like "
        "Conversations</i> should pursue six extensions: (1) <b>orthogonal factorial ablations across RQ2, RQ3, and "
        "RQ4</b>—first, expanding the 3-condition RQ2 design into a 5-condition experiment (<b>Condition A</b>: Examples "
        "<i>None</i>, Directive <i>Off</i>; <b>Condition B</b>: Examples <i>Global/Static</i>, Directive <i>Off</i>; "
        "<b>Condition C</b>: Examples <i>Archetype-Partitioned</i>, Directive <i>Off</i>; <b>Condition D</b>: Examples "
        "<i>Global/Static</i>, Directive <i>On</i>; and <b>Condition E</b>: Examples <i>Archetype-Partitioned</i>, "
        "Directive <i>On</i>) at <i>N</i> ≥ 60 dialogues to orthogonally isolate explicit pacing directives from "
        "sub-index exemplars (preliminary <i>N</i> = 33 diagnostic testing shows that when directives are <i>Off</i>, "
        "<i>Condition C</i> improves style convergence over <i>Condition B</i> from .453 to .511, <i>p</i> = .028, and "
        "calibrates length to 15.03 words vs. the 14.85-word human benchmark, whereas when directives are <i>On</i>, the "
        "explicit routed directive dominates single-turn style at .597–.610 while retrieved exemplars tighten pacing "
        "variance); second, ablating pre-generation [SLOT] masking versus post-generation regex sanitization in RQ3; and "
        "third, crossing the <i>Verified Informed Slot Ledger</i> (Off/On) with <i>Archetype Action Policy</i> "
        "(Generic/Adaptive) in a 2 × 2 × 3 RQ4 design to separate ledger memory gains from persona policy gains; "
        "(2) <b>hierarchical context × behavior clustering and influencing-factor attribution</b>, developing a two-tier "
        "taxonomy (<i>C</i> × <i>K</i> = 24–36 micro-clusters over <i>N</i> > 50,000 enterprise dialogues) that "
        "separates macro situational trip regimes (party composition, budget stakes, travel lead window, and destination "
        "familiarity) from within-regime behavioral negotiation personas while avoiding the sample starvation and 35.9% "
        "entity leakage of naive 500-bucket parameter clustering; (3) <b>soft-mixture manifold routing</b> that blends "
        "exemplars using posterior probabilities for boundary travelers; (4) <b>turn-by-turn Bayesian persona tracking</b> "
        "from Turn 1 onward to capture mid-session persona drift; (5) <b>two-stage quotation-to-conversion funnel "
        "modeling</b> that decouples Stage 1 in-chat quotation agreement from Stage 2 post-quote purchase conversion "
        "under exogenous competitor and lodging controls; and (6) <b>constrained neuro-symbolic reinforcement learning "
        "and live OTA A/B testing</b> with human travelers and human domain raters across multilingual settings."
    )

    # ================================================================== REFERENCES
    D.heading("References", 1, new_page=True)
    for ref in REFERENCES:
        D.reference(ref)

    # ================================================================== APPENDICES A–E
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
            ["data/final/", "Cached Gemini 2.5 Flash/Pro JSONL responses and scored CSV/JSON results for Refined RQ2, RQ3 (<i>N</i>=144), and RQ4 (<i>N</i>=180)"],
            ["src/canonical_schema.py, src/ingestion.py", "Pydantic two-tier data models and corpus parsers"],
            ["src/rule_engine.py, rules/rules_enterprise.yaml", "Deterministic declarative policy engine and YAML rule definitions"],
            ["src/final_pipeline/", "Reproducible pipeline scripts for Steps 0–2i (power, cleaning, RQ1 clustering/sensitivity/refined archetypes), RefinedArchetypeRouter, Refined RQ2, RQ3 2×2 experiment, RQ4 2×3 simulation, and EDA/architecture figures"],
            ["src/report/, src/build_final_report.py", "APA 7 Word/PDF document generator with automated cross-reference and TOC pagination verification"],
            ["notebooks/01_.. to 05_..", "Five executed Jupyter notebooks covering EDA, RQ1, RQ2, RQ3, and RQ4"],
            ["outputs/interim/, outputs/final/", "All CSV summary tables and 300-DPI PNG figures"],
            ["final/", "Submission-ready QM_640_Final_Report_Sandeep_Surnella.docx and .pdf"],
        ],
        widths=[2.6, 3.9],
        align=["l", "l"],
        label="A1",
        split=True,
    )
    D.table(
        "End-to-End Replication Commands",
        ["Pipeline stage", "Command (run from repository root with .venv active)", "Outputs produced"],
        [
            ["0. Power analysis", "python src/final_pipeline/step0_sample_size.py", "Table 8"],
            ["1. Cleaning & univariate EDA", "python src/final_pipeline/step1_prepare_data.py", "Tables 5, 6, E1; Figures 1, E1"],
            ["2. Primary RQ1 clustering", "python src/final_pipeline/step2_rq1_clustering.py", "Table 12; Tables D1–D4; Figures D1–D3"],
            ["2b–2i. RQ1 sensitivity & refined", "python src/final_pipeline/step2g_rq1_truncation.py && python src/final_pipeline/step2h_rq1_ablation.py && python src/final_pipeline/step2i_rq1_refined_archetypes.py", "Table 13; Tables C1–C2, D5–D6, E5; Figures D4, E3"],
            ["3. Final harness & routing test", "python src/final_pipeline/test_step1_harness.py", "Table 13 routing note (t_rq1_hybrid_routing_diagnostics.csv)"],
            ["4. Refined RQ2 experiment", "python src/final_pipeline/step2_rq2_refined.py --execute", "Table 14 (refined rows); Table E3; Figure 6"],
            ["5. RQ3 2×2 factorial experiment", "python src/final_pipeline/step3_rq3_experiment.py --execute", "Table 15; Table C3; Figure 7"],
            ["6. RQ4 2×3 turn-economy sim.", "python src/final_pipeline/step4_rq4_simulation.py --execute", "Table 16; Table C3; Figure 8"],
            ["7. Bivariate/multivariate EDA & arch.", "python src/final_pipeline/step5_figures_and_eda.py", "Table 7; Table E2; Figures 2, 3, 4, 5"],
            ["8. Build Final Report (.docx/.pdf)", "python src/build_final_report.py", "final/QM_640_Final_Report_Sandeep_Surnella.docx & .pdf"],
        ],
        note="All random seeds are fixed at 42. Cached JSONL responses allow offline execution without API calls.",
        widths=[1.45, 3.25, 1.8],
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
        widths=[1.2, 2.05, 1.15, 2.1],
        align=["l", "l", "l", "l"],
        label="A3",
        split=True,
    )

    # Appendix B
    D.heading("Appendix B", 1, new_page=True)
    D.heading("Ten-Week Project Schedule and Milestone Completion Log", 1, toc=False)
    D.para("Table B1 documents the completed 10-week execution schedule aligned with QM640 course milestones.")
    D.table(
        "Ten-Week Project Schedule and Milestone Completion Status",
        ["Week", "QM640 course topic", "Completed project tasks and deliverables", "Status"],
        [
            ["1", "Define research problem & topic", "Business & technical problem statements finalized; GitHub repository initialized; Frames & MultiWOZ 2.2 ingested", "Complete"],
            ["2", "Synopsis draft", "Four research questions, hypotheses, and two-tier Pydantic schema defined", "Complete"],
            ["3", "Literature search & data collection", "26 peer-reviewed business & technical sources synthesized; canonical corpus parsed (<i>N</i> = 2,834 analytic)", "Complete"],
            ["4", "Objectives & hypotheses", "Data quality audit, univariate/bivariate/multivariate EDA, noncentral-<i>F</i> power analysis, and primary RQ1 clustering", "Complete"],
            ["5", "Research design & methodology", "Interim report submitted; primary RQ2 experiment (99 calls) and RQ1 sensitivity/truncation grid (Steps 2b–2i) completed", "Complete"],
            ["6", "Data analysis plan", "Built RefinedArchetypeRouter (Blocks prefix router, κ = .535–.958); repeated RQ2 on refined archetypes (<i>p</i> < .001)", "Complete"],
            ["7", "Data analysis plan execution", "Executed RQ3 2 × 2 factorial experiment (<i>N</i> = 144) and dual-LLM judge reliability audit (gemini-2.5-pro, κ = .917)", "Complete"],
            ["8", "Data analysis assessment", "Executed RQ4 2 × 3 multi-turn simulation (<i>N</i> = 180), persona fidelity validation (95.6%, κ = .933), and HC3/ART checks", "Complete"],
            ["9", "Refinement & documentation", "Generated publication architecture, workflow, and EDA diagrams; synchronized empirical Jupyter notebooks and README", "Complete"],
            ["10", "Document results & findings", "Compiled, audited, and exported submission-ready Final Report (.docx and .pdf)", "Complete"],
        ],
        widths=[0.6, 1.65, 3.35, 0.9],
        align=["c", "l", "l", "c"],
        label="B1",
        split=True,
    )

    # Appendix C
    D.heading("Appendix C", 1, new_page=True)
    D.heading("LLM Behavioral Annotation Codebook, Reliability, and Dual-Judge Validation", 1, toc=False)
    D.para(
        "Table C1 defines all 16 structured fields of the LLM behavioral codebook (`UserBehaviour` in "
        "<i>step2e_llm_user_annotation.py</i>: 10 ordinal 1–5 rating scales, 3 categorical goal/tone clustering fields, "
        "and 3 audit-only fields excluded from clustering), Table C2 reports test–retest reliability across all 16 "
        "fields and criterion validity against ground-truth Frames dialogue acts, and Table C3 summarizes the "
        "cross-model dual-judge reliability in RQ3 and simulator persona validation in RQ4."
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
        widths=[1.75, 1.25, 3.5],
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
        cs = crit.get(c, [(None, "—")])
        for j, (key, desc_) in enumerate(cs):
            rho = cv_.get(f"{c}~{key}", {}).get("rho") if key else None
            c2_rows.append([
                f"{idx_f}. {lab_}" if j == 0 else "",
                nz(rel16[c]) if j == 0 else "",
                desc_,
                nz(rho) if rho is not None else "—",
            ])
    for idx_f, lab_, c, desc_ in [
        (11, "Primary goal (6 classes)", "primary_goal", "Categorical Cohen's κ (clustering)"),
        (12, "Secondary goals (multi-label)", "secondary_goals", "Binary presence Cohen's κ (clustering)"),
        (13, "Emotional tone (4 classes)", "emotional_tone", "Categorical Cohen's κ (clustering)"),
        (14, "Session outcome (4 classes)", "outcome", "Categorical Cohen's κ (audit-only)"),
        (15, "Party type (6 classes)", "party_type", "Categorical Cohen's κ (audit-only)"),
        (16, "Unusual conversation (boolean)", "unusual_conversation", "Boolean Cohen's κ (99.0% raw agreement, audit-only)"),
    ]:
        c2_rows.append([f"{idx_f}. {lab_}", nz(rel16[c]), desc_, "—"])
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
        widths=[1.45, 0.55, 1.35, 0.9, 0.85, 1.4],
        align=["l", "c", "l", "c", "c", "l"],
        label="C3",
        split=True,
    )

    # Appendix D
    D.heading("Appendix D", 1, new_page=True)
    D.heading("RQ1 Sensitivity Grid, Ablation Diagnostics, and Primary Archetype Profiles", 1, toc=False)
    D.para(
        "Tables D1–D6 and Figures D1–D4 provide the complete diagnostic tables and visual plots supporting the RQ1 "
        "primary clustering benchmark and the representation × truncation sensitivity analysis."
    )
    d1_rows = [
        [f"Panel A (MiniLM-L6-v2 whole): <i>k</i> = {int(r.k)}", nz(r.silhouette, 3), n2(r.davies_bouldin, 3), f"Inertia = {n2(r.inertia, 1)}", f"{n2(r.smallest_cluster_pct, 1)}%"]
        for r in k_sel.itertuples()
    ] + [
        [f"Panel B (46-d Blocks, <i>M</i> = 9): <i>k</i> = {b['k']}", f"{nz(b['sil'], 3)} (cal. {nz(b['cal_sil'], 3)})", n2(b["db"], 3), f"ARI = {nz(b['ari'], 3)} ({n2(b['core_pct'], 1)}% core)", f"{n2(b['min_pct'], 1)}% — {b['note']}"]
        for b in blocks_k_sel
    ]
    D.table(
        "Choice of Number of Clusters k on the Golden Partition Across Initial MiniLM and Final 46-d Blocks (M = 9) Representations",
        ["Representation & <i>k</i>", "Cosine Silhouette", "Davies–Bouldin index", "Inertia / Bootstrap ARI", "Smallest cluster (%) & diagnostic"],
        d1_rows,
        note="On the final 46-d <i>Blocks</i> (<i>M</i> = 9) representation (Panel B), <i>k</i> = 3 achieves the lowest (best) Davies–Bouldin index (2.647), high bootstrap stability (ARI = .888 in the truncation grid; .869 in the 6-config ablation), and balanced cluster sizes (≥ 25.5%), whereas <i>k</i> = 2 collapses <i>Decisive Booker</i> and <i>Rigid-Constraint Seeker</i> and <i>k</i> ≥ 4 fails stability/size thresholds.",
        widths=[1.85, 1.05, 0.95, 1.25, 1.4],
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
        widths=[2.0, 1.1, 1.4, 1.0, 1.0],
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
        widths=[2.2, 1.43, 1.43, 1.44],
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
        widths=[1.5, 0.6, 1.4, 1.0, 1.0, 1.0],
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
                (nz(rt_diag.loc[int(m), "cohen_kappa"], 3) if m != "whole" else "—"),
                nz(r.outcome_v),
            ]
            for m, r in tr3.iterrows()
        ],
        note="Raw L1 κ uses unprojected 5-turn features (step2g); Blocks router κ projects prefix features into the exact golden Blocks space (RefinedArchetypeRouter).",
        widths=[1.35, 0.8, 0.7, 0.75, 0.75, 0.65, 0.8, 0.7],
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
        widths=[2.3, 0.8, 0.85, 0.9, 0.8, 0.85],
        align=["l", "c", "c", "c", "c", "c"],
        label="D6",
        split=True,
    )
    D.figure("Cluster-Number Diagnostics on Golden Partition", os.path.join(FIG_INT, "fig_rq1_k_selection.png"), width=5.2, label="D1")
    D.figure("Silhouette Coefficients Across 159 Subsample Runs by Algorithm", os.path.join(FIG_INT, "fig_rq1_silhouette.png"), width=5.0, label="D2")
    D.figure("UMAP Projection of Frames Archetypes and MultiWOZ 2.2 External Transfer Check", os.path.join(FIG_INT, "fig_rq1_umap.png"), width=5.3, label="D3")
    D.figure("Hybrid Archetype Stability, Routing, and Outcome Association Across Truncation Horizons", os.path.join(FIG_INT, "fig_rq1_truncation_2x2.png"), width=5.3, label="D4")

    # Appendix E
    D.heading("Appendix E", 1, new_page=True)
    D.heading("Supplementary EDA, RQ2 Pairwise Contrasts, and RQ3/RQ4 Groundwork Diagnostics", 1, toc=False)
    D.para(
        "Tables E1–E5 and Figures E1–E3 provide the supplementary slot-completeness table, multivariate PCA loadings, "
        "Holm-adjusted pairwise contrasts for RQ2, corpus rule coverage audit for RQ3, and human turn-economy baseline for RQ4."
    )
    D.table(
        "Observed Canonical Slot Completeness by Corpus",
        ["Canonical slot", "Schema tier", "Microsoft Frames (%)", "MultiWOZ 2.2 (%)"],
        [[s.replace("_", " "), t, n2(f, 1), n2(m, 1)] for s, t, f, m in comp.itertuples(index=False)],
        widths=[2.5, 1.1, 1.45, 1.45],
        align=["l", "c", "c", "c"],
        label="E1",
        split=True,
    )
    D.table(
        "Multivariate Principal Component Loadings of Structural and Behavioral Features (Frames)",
        ["Variable", "PC1 loading (40.8% var.)", "PC2 loading (17.2% var.)", "PC3 loading (10.6% var.)"],
        [[r.variable, nz(r.PC1_loading, 3), nz(r.PC2_loading, 3), nz(r.PC3_loading, 3)] for _, r in t_mv.iterrows()],
        widths=[2.3, 1.4, 1.4, 1.4],
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
        widths=[1.75, 1.85, 0.75, 0.55, 0.4, 0.65, 0.55],
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
        widths=[1.6, 1.9, 1.0, 1.1, 0.9],
        align=["l", "l", "c", "c", "c"],
        label="E4",
        split=True,
    )
    b4_df = base4r.reindex(ARCH_REF)
    D.table(
        "Human Wizard Baseline of Turn Economy and Redundant Elicitation by Refined Archetype (Frames)",
        ["Refined user archetype", "<i>n</i>", "Whole-dialogue turns <i>M</i> (<i>SD</i>)", "RER <i>M</i> (<i>SD</i>)", "Wizard request turns <i>M</i>"],
        [[a, str(int(r.n)), f"{n2(r.turns_M)} ({n2(r.turns_SD)})", f"{nz(r.rer_M, 3)} ({nz(r.rer_SD, 3)})", n2(r.req_turns_M)] for a, r in b4_df.iterrows()],
        note="Turns in Table E5 reflect total observed human-wizard turns (user + wizard messages) across complete archival Frames transcripts (including post-offer discussion and non-booking endings), whereas Table 16 (RQ4) measures total conversational turns until package agreement (<code>[ACCEPT_BOOKING]</code>) in closed-loop simulation.",
        widths=[1.85, 0.55, 1.35, 1.3, 1.45],
        align=["l", "c", "c", "c", "c"],
        label="E5",
        split=True,
    )
    D.figure("Observed Slot Completeness by Corpus", os.path.join(FIG_INT, "fig_eda_slots.png"), width=4.6, label="E1")
    D.figure("Primary RQ2 Results on Unrefined Whole-Dialogue Archetypes", os.path.join(FIG_INT, "fig_rq2_results.png"), width=5.2, label="E2")
    D.figure("Human Wizard Baseline of Turn Economy and Redundant Elicitation by Refined Archetype", os.path.join(FIG_INT, "fig_rq4_baseline_refined.png"), width=5.2, label="E3")

    # Appendix F
    D.heading("Appendix F", 1, new_page=True)
    D.heading("Derivation of User Archetype Cluster Names and Deterministic Centroid-Mapping Protocol", 1, toc=False)
    D.para(
        "Unsupervised clustering algorithms such as <i>K</i>-Means output anonymous integer cluster identifiers "
        "(<code>0</code>, <code>1</code>, <code>2</code>) rather than semantic persona names, and those integer "
        "identifiers are invariant up to permutation across random initializations (the <i>label-switching problem</i>). "
        "To ensure that human-interpretable archetype labels are assigned reproducibly without manual post-hoc "
        "cherry-picking, both the primary whole-dialogue clustering pipeline (<i>src/final_pipeline/"
        "step2_rq1_clustering.py</i>) and the refined opening-prefix clustering pipeline (<i>src/final_pipeline/"
        "step2i_rq1_refined_archetypes.py</i>) apply pre-declared, deterministic Python centroid-mapping rules to the "
        "golden-partition cluster means. Table F1 documents the exact sequential decision rule, distinguishing "
        "centroid criterion, and resulting golden-partition profile for each primary and refined archetype."
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
                "Step 1: <code>idxmax(turns_M)</code> among the 3 clusters",
                "Guided Explorer",
                "Longest dialogues (<i>M</i> = 19.65 turns, <i>n</i> = 187, 20.0%); highest option exploration across whole transcripts",
            ],
            [
                "Primary Whole-Dialogue Archetypes (<i>step2_rq1_clustering.py</i>)",
                "Step 2: <code>idxmax(revisions)</code> among the remaining 2 clusters",
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
                "Step 1: <code>idxmax(destination_flexibility)</code> across the 3 <i>Blocks</i> clusters (<i>M</i> = 9)",
                "Open Explorer",
                f"Highest destination flexibility ({n2(oe_r.destination_flexibility)}/5.0) and exploration breadth ({n2(oe_r.exploration_breadth)}/5.0); longest dialogues ({n2(oe_r.turns_M)} turns; <i>n</i> = {int(oe_r.n)}, {n2(oe_r.pct, 1)}%)",
            ],
            [
                "Refined Opening-Prefix Archetypes (<i>step2i_rq1_refined_archetypes.py</i>)",
                "Step 2: <code>idxmax(decisiveness)</code> among the remaining 2 clusters",
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
        note="All centroid-mapping rules are evaluated strictly on golden-partition means (<i>D</i><sub>gold</sub>, <i>n</i> = 933) after fitting <i>K</i>-Means (<i>k</i> = 3, seed = 42). Held-out test dialogues (<i>D</i><sub>test</sub>, <i>n</i> = 401) inherit the mapped archetype name of their nearest golden centroid.",
        widths=[1.45, 1.85, 1.25, 1.95],
        align=["l", "l", "l", "l"],
        label="F1",
        split=True,
    )

    # Appendix G
    D.heading("Appendix G", 1, new_page=True)
    D.heading("Role, Architecture, and Validation Scope of Judge and Annotator LLMs", 1, toc=False)
    D.para(
        "A critical methodological principle of this study is that <b>all primary hypothesis tests (<i>H</i><sub>01</sub> "
        "through <i>H</i><sub>04</sub>) are anchored in deterministic mathematical and programmatic Python verification "
        "metrics</b> rather than subjective LLM preference scores. Specifically, RQ1 cluster quality is evaluated via "
        "mathematical Silhouette, Davies–Bouldin, Calinski–Harabasz, and Adjusted Rand Index formulas; RQ2 style "
        "convergence and pacing calibration are evaluated via deterministic non-Gemini encoders (<i>all-MiniLM-L6-v2</i> "
        "cosine, <i>roberta-large</i> BERTScore <i>F</i><sub>1</sub>, and exact word-count error); RQ3 exemplar entity "
        "leakage (ELR) and slot grounding <i>F</i><sub>1</sub> are computed by deterministic Python string/set verifiers "
        "(<i>src/final_pipeline/metrics.py</i>); and RQ4 turn economy (turns to agreed package quotation and Redundant "
        "Elicitation Rate) is computed by deterministic turn counters and regex slot-ledger matching."
    )
    D.para(
        "Within this architecture, LLMs serve two strictly bounded measurement and validation functions: (a) in RQ1, "
        "<i>gemini-2.5-flash</i> (at temperature = 0) acts as a <b>structured behavioral codebook annotator</b> prior to "
        "<i>K</i>-Means clustering, extracting the 16-field <i>UserBehaviour</i> schema (validated via test–retest "
        "κ<sub><i>w</i></sub> = .87–.96 and ground-truth Frames dialogue-act correlations ρ = .30–.73; Table C2); and "
        "(b) in RQ3 and RQ4, the larger <i>gemini-2.5-pro</i> model serves strictly as an <b>independent cross-verification "
        "and quality-control validator</b> (Table C3). Importantly, the independent Judge LLM does not invent or "
        "contribute any standalone performance metric to firm up the paper's statistical conclusions; rather, it acts "
        "as an methodological gatekeeper. During the RQ3 pilot phase, cross-checking outputs against the deterministic "
        "verifier identified a prompt-ordering sensitivity (<i>pilot_v1</i> → <i>pilot_v2</i>) that was resolved prior "
        "to full execution. In the final experiments, because the independent <i>gemini-2.5-pro</i> validator strongly "
        "corroborated both the RQ3 policy evaluations (95.8% agreement, κ = .917 with <i>gemini-2.5-flash</i>; 93.1% "
        "agreement, κ = .861 with the deterministic regex verifier) and the RQ4 simulated customer personas (95.6% "
        "blind classification accuracy, κ = .933), no manual re-annotation or rework was required. Table G1 summarizes "
        "the exact role, deterministic counterpart, and gatekeeping outcome of every LLM annotator and judge in the "
        "pipeline."
    )
    D.table(
        "Functional Scope, Primary Deterministic Metrics, and Cross-Verification Role of Judge and Annotator LLMs Across RQ1–RQ4",
        [
            "Research question & pipeline stage",
            "Primary hypothesis-test metrics (Deterministic / Mathematical)",
            "LLM annotator / Judge model & role",
            "Cross-verification agreement & gatekeeping outcome",
        ],
        [
            [
                "RQ1: Opening-Prefix Behavioral Annotation (<i>step2e_llm_user_annotation.py</i>)",
                "Cosine Silhouette, Davies–Bouldin, Calinski–Harabasz, Bootstrap ARI (.89 truncation grid / .87 ablation), and <i>Blocks</i> prefix-to-cluster κ (.359–.958)",
                "<b>Codebook Annotator (<i>gemini-2.5-flash</i>, temp = 0):</b> Extracts Fields 1–13 (clustering inputs) and Fields 14–16 (audit-only) before <i>K</i>-Means runs; does not name clusters.",
                "Test–retest κ<sub><i>w</i></sub> = .87–.96 (mean .91) on ordinal Fields 1–10; κ = .75–.98 on Fields 11–16; significant Spearman ρ = .30–.73 (<i>p</i> < .001) against ground-truth Frames acts (Table C2).",
            ],
            [
                "RQ2: Style Convergence & Pacing Calibration (<i>step2_rq2_refined.py</i>)",
                "Hybrid & pure SBERT style cosine (<i>all-MiniLM-L6-v2</i>), BERTScore <i>F</i><sub>1</sub> (<i>roberta-large</i>), and absolute word-count error (|Words<sub>gen</sub> − Words<sub>human</sub>|)",
                "<b>No Judge LLM used:</b> All evaluation encoders are deterministic, non-Gemini neural and lexical metrics.",
                "Eliminates same-family LLM evaluation bias in RQ2; RM-ANOVA and Friedman tests confirm <i>p</i> < .001 on both hybrid and pure SBERT style convergence.",
            ],
            [
                "RQ3: Policy Compliance Dual-Judge Audit (<i>step3_rq3_experiment.py</i>)",
                "Deterministic regex rule verifier (<i>det_pass</i>), exact Exemplar Entity Leakage Rate (ELR), and deterministic Slot Grounding <i>F</i><sub>1</sub>",
                "<b>Primary Judge (<i>gemini-2.5-flash</i>) + Independent Validator Judge (<i>gemini-2.5-pro</i>):</b> Cross-verifies natural-language enforcement of 5 enterprise policy rules on stratified audit subsample (<i>n</i> = 48).",
                "Guided <i>pilot_v1</i> → <i>pilot_v2</i> prompt ordering fix; final dual-judge raw agreement = 95.8%, Cohen's κ = .917 (PABAK = .917), and 93.1% agreement (κ = .861) with deterministic regex verification (Table C3).",
            ],
            [
                "RQ4: Blind Simulator Persona Fidelity Audit (<i>step4_rq4_simulation.py</i>)",
                "Deterministic turn counter to agreed package quotation (<i>total_turns</i>, <i>log_turns</i>), regex Redundant Elicitation Rate (RER), and goal completion rate",
                "<b>Independent Blind Validator (<i>gemini-2.5-pro</i>):</b> Reads simulated customer transcripts (<i>n</i> = 45, 15 per archetype) blinded to true labels to verify persona fidelity; contributes zero metrics to RQ4 ANOVA.",
                "Classified 43/45 simulated users into their intended archetype (95.6% accuracy vs. 33.3% chance, Cohen's κ = .933, <i>p</i> < .001; Table C3), validating the multi-turn simulation environment.",
            ],
        ],
        note="All LLM annotation and judge calls use deterministic decoding (temperature = 0.0, Pydantic JSON schema enforcement) and are cached in <i>data/interim/</i> and <i>data/final/</i> for 100% offline reproducibility.",
        widths=[1.35, 1.65, 1.75, 1.75],
        align=["l", "l", "l", "l"],
        label="G1",
        split=True,
    )
