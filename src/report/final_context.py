"""
Shared empirical data loader and APA 7 formatting helpers for the QM640 Final Report.
Reads all numbers directly from `data/interim/`, `data/final/`, `outputs/interim/`, and `outputs/final/`.
"""

import json
import os
import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(SRC_DIR)

TAB_INT = os.path.join(ROOT, "outputs", "interim", "tables")
FIG_INT = os.path.join(ROOT, "outputs", "interim", "figures")
WORK_INT = os.path.join(ROOT, "data", "interim")

TAB_FIN = os.path.join(ROOT, "outputs", "final", "tables")
FIG_FIN = os.path.join(ROOT, "outputs", "final", "figures")
WORK_FIN = os.path.join(ROOT, "data", "final")

OUT_DIR = os.path.join(ROOT, "final")
BASENAME = "QM_640_Final_Report_Sandeep_Surnella"
TITLE = "Cluster-Adaptive Prompting for Multi-Turn Travel and Tourism Conversational Systems"
REPO = "https://github.com/surnella/QM640-Dialogue-Clustering-Capstone"
ARCH_PRIM = ["Direct Transactional", "Constraint Negotiator", "Guided Explorer"]
ARCH_REF = ["Decisive Booker", "Open Explorer", "Rigid-Constraint Seeker"]
CONDS = ["Zero-Shot", "Static Few-Shot", "Cluster-Adaptive Few-Shot"]


def T_int(name):
    return pd.read_csv(os.path.join(TAB_INT, name))


def J_int(name):
    with open(os.path.join(WORK_INT, name), "r", encoding="utf-8") as f:
        return json.load(f)


def T_fin(name):
    return pd.read_csv(os.path.join(TAB_FIN, name))


def J_fin(name):
    with open(os.path.join(WORK_FIN, name), "r", encoding="utf-8") as f:
        return json.load(f)


def n2(x, d=2):
    """Number with leading zero (values that can exceed 1)."""
    return f"{float(x):,.{d}f}".replace("-", "\u2212")


def nz(x, d=2):
    """Number without leading zero (values bounded by 1, e.g., p, r, silhouette, cosine)."""
    s = f"{float(x):.{d}f}"
    s = s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s
    return s.replace("-", "\u2212")


def pv(p):
    """APA p value with operator."""
    p = float(p)
    return "< .001" if p < .001 else f"= {nz(p, 3)}"


def pv_cell(p):
    """APA p value for table cell (no '=' sign)."""
    p = float(p)
    return "< .001" if p < .001 else ("> .999" if p > .999 else nz(p, 3))


def pct(x, d=1):
    return f"{float(x):.{d}f}%"


def games_howell(groups):
    names = list(groups)
    k = len(names)
    rows = []
    for i in range(k):
        for j in range(i + 1, k):
            a, b = np.asarray(groups[names[i]]), np.asarray(groups[names[j]])
            va, vb, na, nb = a.var(ddof=1), b.var(ddof=1), len(a), len(b)
            se = np.sqrt(va / na + vb / nb)
            diff = b.mean() - a.mean()
            df = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
            q = abs(diff) / se * np.sqrt(2)
            p = stats.studentized_range.sf(q, k, df)
            rows.append((names[i], names[j], diff, df, p))
    return rows


def load_all_context():
    ctx = {}
    ctx["ss"] = T_int("t_sample_size.csv").set_index("RQ")
    ctx["qa"] = T_int("t_quality_audit.csv")
    ctx["desc"] = T_int("t_corpus_descriptives.csv")
    ctx["comp"] = T_int("t_slot_completeness.csv")
    ctx["s1"] = J_int("step1_summary.json")
    ctx["r1"] = J_int("rq1_summary.json")
    ctx["k_sel"] = T_int("t_rq1_k_selection.csv")
    ctx["r1_desc"] = T_int("t_rq1_descriptives.csv").set_index("algorithm")
    ctx["r1_tk"] = T_int("t_rq1_tukey.csv")
    ctx["prof"] = T_int("t_rq1_profiles.csv").set_index("archetype")
    ctx["cross"] = T_int("t_rq1_cross_corpus.csv")
    ctx["r2p"] = J_int("rq2_pilot_summary.json")
    ctx["r2_ret"] = T_int("t_rq2_pilot_retrieval.csv")
    ctx["r2_units"] = pd.read_csv(os.path.join(WORK_INT, "rq2_pilot_units.csv"))
    ctx["r2_prim"] = J_int("rq2_results.json")
    ctx["r34"] = J_int("rq34_summary.json")
    ctx["rules"] = T_int("t_rq3_rules.csv")
    ctx["rtests"] = T_int("t_rq3_rule_tests.csv")
    ctx["audit"] = T_int("t_rq3_corpus_audit.csv").set_index("rule")
    ctx["base4"] = T_int("t_rq4_baseline.csv").set_index("archetype")

    # Sensitivity & Refined Archetypes
    ctx["rep_m"] = T_int("t_rq1_rep_grid.csv").set_index(["rep", "k"])
    ctx["r1gm"] = J_int("rq1_gemini_summary.json")
    ctx["r1h"] = J_int("rq1_llm_hybrid_summary.json")
    ctx["r1t"] = J_int("rq1_truncation_summary.json")
    ctx["r1r"] = J_int("rq1_refined_summary.json")
    trg = T_int("t_rq1_truncation_grid.csv")
    trg["M"] = trg.M.astype(str)
    ctx["trg"] = trg
    abl = T_int("t_rq1_ablation.csv")
    abl["M"] = abl.M.astype(str)
    ctx["abl"] = abl
    ctx["rprof"] = T_int("t_rq1_refined_profile.csv").set_index("archetype_refined")
    ctx["base4r"] = T_int("t_rq4_baseline_refined.csv").set_index("archetype_refined")

    # Final pipeline outputs
    ctx["s1_fin"] = J_fin("step1_harness_summary.json")
    rt_df = T_fin("t_rq1_hybrid_routing_diagnostics.csv").rename(columns={"routing_kappa": "cohen_kappa"})
    ctx["rt_diag"] = rt_df.set_index("user_messages_m")
    r2_ref = J_fin("rq2_refined_results.json")
    for dv_k, dv_v in r2_ref.get("results", {}).items():
        for cond_k, cond_v in list(dv_v.get("desc", {}).items()):
            if isinstance(cond_v, dict):
                dv_v["desc"][cond_k] = [cond_v["M"], cond_v["SD"]]
    ctx["r2_ref"] = r2_ref
    ctx["r3_fin"] = J_fin("rq3_results.json")
    ctx["r4_fin"] = J_fin("rq4_results.json")
    ctx["eda_ext"] = J_fin("eda_summary_ext.json")
    ctx["t_biv"] = T_fin("t_eda_bivariate_correlations.csv")
    ctx["t_mv"] = T_fin("t_eda_multivariate_loadings.csv")

    # Additional derived statistics
    fa = pd.read_csv(os.path.join(WORK_INT, "frames_archetypes.csv"))
    with open(os.path.join(ROOT, "data", "raw", "frames", "Frames-dataset", "frames.json"), "r", encoding="utf-8") as f:
        raw_frames = {f"frames_{d['id']}": d for d in json.load(f)}
    fa["user_id"] = fa.dialogue_id.map(lambda i: raw_frames[i]["user_id"] if i in raw_frames else None)
    ct = pd.crosstab(fa.archetype, fa.user_id)
    chi_u = stats.chi2_contingency(ct)
    ctx["cramer_v"] = float(np.sqrt(chi_u[0] / (ct.values.sum() * (min(ct.shape) - 1))))
    ctx["chi_u"] = chi_u
    ctx["n_users"] = int(fa.user_id.nunique())
    ctx["n_wizards"] = len({d["wizard_id"] for d in raw_frames.values()})
    ctx["n_frames_raw"] = len(raw_frames)

    gold_counts = fa[fa.partition == "gold"].archetype.value_counts().reindex(ARCH_PRIM)
    test_counts = fa[fa.partition == "test"].archetype.value_counts().reindex(ARCH_PRIM)
    ctx["chi_gt"] = stats.chisquare(test_counts.values, gold_counts.values / gold_counts.sum() * test_counts.sum())
    ctx["test_counts_prim"] = test_counts

    subs = pd.read_csv(os.path.join(WORK_INT, "rq1_subsample_scores.csv"))
    ctx["gh"] = games_howell({
        a: subs.loc[subs.algorithm == a, "silhouette"].values
        for a in ["K-Means", "Agglomerative", "HDBSCAN"]
    })

    n_ann_calls = 0
    for fp in ["llm_user_annotations.jsonl", "llm_user_annotations_retest.jsonl"] + [
        f"llm_user_annotations_u{m}.jsonl" for m in (3, 5, 7, 9)
    ]:
        with open(os.path.join(WORK_INT, fp), "r", encoding="utf-8") as f:
            n_ann_calls += sum(1 for l in f if l.strip() and "reused_full" not in l)
    ctx["n_ann_calls"] = n_ann_calls

    # Complete 16-field LLM behavioral schema profile & test-retest reliability
    from sklearn.metrics import cohen_kappa_score
    ref_df = pd.read_csv(os.path.join(WORK_INT, "frames_archetypes_refined.csv")).set_index("dialogue_id")
    u9_df = pd.DataFrame([json.loads(l) for l in open(os.path.join(WORK_INT, "llm_user_annotations_u9.jsonl")) if l.strip()]).drop_duplicates("dialogue_id").set_index("dialogue_id")
    full_df = pd.DataFrame([json.loads(l) for l in open(os.path.join(WORK_INT, "llm_user_annotations.jsonl")) if l.strip()]).drop_duplicates("dialogue_id").set_index("dialogue_id")
    ret_df = pd.DataFrame([json.loads(l) for l in open(os.path.join(WORK_INT, "llm_user_annotations_retest.jsonl")) if l.strip()]).drop_duplicates("dialogue_id").set_index("dialogue_id")

    g_ids = ref_df[ref_df.partition == "gold"].index
    dg = u9_df.loc[g_ids].copy()
    dg["arch"] = ref_df.loc[g_ids, "archetype_refined"]
    dg["outcome_full"] = full_df.loc[g_ids, "outcome"]
    dg["party_full"] = full_df.loc[g_ids, "party_type"]
    dg["unusual_full"] = full_df.loc[g_ids, "unusual_conversation"]
    dg["has_sec_goal"] = dg["secondary_goals"].apply(lambda x: len(x) > 0 if isinstance(x, list) else False)

    prof16 = {}
    for a in ARCH_REF:
        sub = dg[dg.arch == a]
        prof16[a] = {
            "has_sec_goal_pct": float(100.0 * sub["has_sec_goal"].mean()),
            "tone_pos_pct": float(100.0 * (sub["emotional_tone"] == "positive").mean()),
            "tone_neu_pct": float(100.0 * (sub["emotional_tone"] == "neutral").mean()),
            "party_solo_couple_pct": float(100.0 * sub["party_full"].isin(["solo", "couple"]).mean()),
            "unusual_pct": float(100.0 * sub["unusual_full"].mean()),
        }
    ctx["full_16_profile"] = prof16

    common_ret = full_df.index.intersection(ret_df.index)
    f_sub, r_sub = full_df.loc[common_ret], ret_df.loc[common_ret]
    sec_f = f_sub["secondary_goals"].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).astype(int)
    sec_r = r_sub["secondary_goals"].apply(lambda x: len(x) > 0 if isinstance(x, list) else False).astype(int)
    un_f = f_sub["unusual_conversation"].astype(int)
    un_r = r_sub["unusual_conversation"].astype(int)
    rel_ext = dict(ctx["r1h"]["reliability"])
    rel_ext["secondary_goals"] = float(cohen_kappa_score(sec_f, sec_r))
    rel_ext["unusual_conversation"] = float(cohen_kappa_score(un_f, un_r))
    ctx["full_16_reliability"] = rel_ext

    return ctx
