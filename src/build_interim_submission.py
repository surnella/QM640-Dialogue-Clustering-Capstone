"""
Build the submission-ready QM640 interim report (APA 7 student paper).

All numbers are read from the outputs of src/interim_pipeline (steps 0-4, including the RQ1 sensitivity
steps 2b-2i), so the text,
tables, and figures stay consistent with the analysis. Run after the pipeline:

    python src/build_interim_submission.py

Output: interim/QM_640_Interim_Report_Sandeep_Surnella.docx and .pdf
A two-pass build fills in the table-of-contents page numbers from the rendered PDF.
"""

import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from report.docx_apa import APADoc  # noqa: E402
from report.references import REFERENCES  # noqa: E402

TAB = os.path.join(ROOT, "outputs", "interim", "tables")
FIG = os.path.join(ROOT, "outputs", "interim", "figures")
WORK = os.path.join(ROOT, "data", "interim")
OUT_DIR = os.path.join(ROOT, "interim")
BASENAME = "QM_640_Interim_Report_Sandeep_Surnella"
TITLE = "Cluster-Adaptive Prompting for Multi-Turn Travel and Tourism Conversational Systems"
REPO = "https://github.com/surnella/QM640-Dialogue-Clustering-Capstone"
ARCH = ["Direct Transactional", "Constraint Negotiator", "Guided Explorer"]


# ----------------------------------------------------------------------------- formatting helpers
def T(name):
    return pd.read_csv(os.path.join(TAB, name))


def J(name):
    with open(os.path.join(WORK, name)) as f:
        return json.load(f)


def n2(x, d=2):
    """Number with leading zero (values that can exceed 1)."""
    return f"{x:,.{d}f}".replace("-", "\u2212")


def nz(x, d=2):
    """Number without leading zero (values bounded by 1, e.g., p, r, silhouette, cosine)."""
    s = f"{x:.{d}f}"
    s = s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s
    return s.replace("-", "\u2212")


def pv(p):
    """APA p value with operator."""
    return "< .001" if p < .001 else f"= {nz(p, 3)}"


def pct(x, d=1):
    return f"{x:.{d}f}%"


def games_howell(groups):
    """Games-Howell pairwise comparisons (unequal variances)."""
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


# ----------------------------------------------------------------------------- load results
ss = T("t_sample_size.csv").set_index("RQ")
qa = T("t_quality_audit.csv")
desc = T("t_corpus_descriptives.csv")
comp = T("t_slot_completeness.csv")
s1 = J("step1_summary.json")
r1 = J("rq1_summary.json")
k_sel = T("t_rq1_k_selection.csv")
r1_desc = T("t_rq1_descriptives.csv").set_index("algorithm")
r1_tk = T("t_rq1_tukey.csv")
prof = T("t_rq1_profiles.csv").set_index("archetype")
cross = T("t_rq1_cross_corpus.csv")
r2p = J("rq2_pilot_summary.json")
r2_ret = T("t_rq2_pilot_retrieval.csv")
r2_units = pd.read_csv(os.path.join(WORK, "rq2_pilot_units.csv"))
r34 = J("rq34_summary.json")
rules = T("t_rq3_rules.csv")
rtests = T("t_rq3_rule_tests.csv")
audit = T("t_rq3_corpus_audit.csv").set_index("rule")
base4 = T("t_rq4_baseline.csv").set_index("archetype")
RQ2_DONE = os.path.exists(os.path.join(WORK, "rq2_results.json"))
r2x = J("rq2_results.json") if RQ2_DONE else None
if not RQ2_DONE:
    raise SystemExit("Run src/interim_pipeline/step3_rq2_pipeline.py --execute first (RQ2 results missing).")
CONDS = ["Zero-Shot", "Static Few-Shot", "Cluster-Adaptive Few-Shot"]
sc_r, gc_r, wd_r = (r2x["results"][k] for k in ("style_cos", "gold_cos", "words"))
sc_a, gc_a, wd_a = sc_r["anova"], gc_r["anova"], wd_r["anova"]
sc_d, wd_d = sc_r["desc"], wd_r["desc"]
sc_sh = [v["p"] for v in sc_r["shapiro_diffs"].values()]
wd_pairs = {p["contrast"]: p for p in wd_r["pairs"]}
f_rq2 = float(np.sqrt(sc_a["eta2_partial"] / (1 - sc_a["eta2_partial"])))

# RQ1 sensitivity analysis of the archetype definition (steps 2b-2i)
rep_m = T("t_rq1_rep_grid.csv").set_index(["rep", "k"])
r1gm = J("rq1_gemini_summary.json")
r1h = J("rq1_llm_hybrid_summary.json")
r1t = J("rq1_truncation_summary.json")
r1r = J("rq1_refined_summary.json")
trg = T("t_rq1_truncation_grid.csv")
trg["M"] = trg.M.astype(str)
abl = T("t_rq1_ablation.csv")
abl["M"] = abl.M.astype(str)
rprof = T("t_rq1_refined_profile.csv").set_index("archetype_refined")
base4r = T("t_rq4_baseline_refined.csv").set_index("archetype_refined")
ARCH2 = r1r["order"]  # Decisive Booker, Open Explorer, Rigid-Constraint Seeker
r4r = r1r["rq4"]
win = r1t["winner"]
tr3 = trg[trg.k == 3].set_index("M")
tr_hi = trg[trg.k >= 4].groupby("M").stability_ari.max()
kap_prim = float(rep_m.loc[("R0", 3), "kappa_N5"])
n_ann_calls = 0
for _fp in ["llm_user_annotations.jsonl", "llm_user_annotations_retest.jsonl"] + \
        [f"llm_user_annotations_u{m}.jsonl" for m in (3, 5, 7, 9)]:
    with open(os.path.join(WORK, _fp)) as _f:
        n_ann_calls += sum(1 for l in _f if l.strip() and "reused_full" not in l)


subs = pd.read_csv(os.path.join(WORK, "rq1_subsample_scores.csv"))
gh = games_howell({a: subs.loc[subs.algorithm == a, "silhouette"].values
                   for a in ["K-Means", "Agglomerative", "HDBSCAN"]})

fa = pd.read_csv(os.path.join(WORK, "frames_archetypes.csv"))
# Held-out archetype distribution vs. golden proportions
gold_counts = fa[fa.partition == "gold"].archetype.value_counts().reindex(ARCH)
test_counts = fa[fa.partition == "test"].archetype.value_counts().reindex(ARCH)
chi_gt = stats.chisquare(test_counts.values, gold_counts.values / gold_counts.sum() * test_counts.sum())

# Role-player confound check: archetype x Frames user role-player
with open(os.path.join(ROOT, "data", "raw", "frames", "Frames-dataset", "frames.json")) as f:
    _raw = {f"frames_{d['id']}": d for d in json.load(f)}
fa["user_id"] = fa.dialogue_id.map(lambda i: _raw[i]["user_id"] if i in _raw else None)
ct = pd.crosstab(fa.archetype, fa.user_id)
chi_u = stats.chi2_contingency(ct)
cramer_v = float(np.sqrt(chi_u[0] / (ct.values.sum() * (min(ct.shape) - 1))))
n_users = fa.user_id.nunique()
n_wizards = len({d["wizard_id"] for d in _raw.values()})
n_frames_raw = len(_raw)

fq = qa.iloc[0]
mq = qa.iloc[1]
fd = desc.iloc[0]
md = desc.iloc[1]
an = r1["anova"]
we = r1["welch"]
kw = r1["kruskal"]
lev = r1["levene"]
sh = r1["shapiro"]
perm = r1["permutation_baseline"]
cc = r1["cross_corpus_t"]
gt = r1["gold_vs_test_t"]
km, ag, hd = (r1_desc.loc[a] for a in ["K-Means", "Agglomerative", "HDBSCAN"])
eta = an["eta2"]
f_obs = np.sqrt(eta / (1 - eta))
cr = cross.set_index("set")
rm = r2p["retrieval_rm"]
pairs = {p["contrast"]: p for p in r2p["retrieval_pairs"]}
ret = r2_ret.set_index("strategy")
own_M, own_SD = r2_units.gold_style_own.mean(), r2_units.gold_style_own.std(ddof=1)
oth_M, oth_SD = r2_units.gold_style_other.mean(), r2_units.gold_style_other.std(ddof=1)
n_route = int(r2_units.routing_correct.sum())


def tk_row(g1, g2):
    r = r1_tk[((r1_tk.group1 == g1) & (r1_tk.group2 == g2)) | ((r1_tk.group1 == g2) & (r1_tk.group2 == g1))].iloc[0]
    if r.group1 == g1:
        return r.meandiff, r["p-adj"], r.lower, r.upper
    return -r.meandiff, r["p-adj"], -r.upper, -r.lower


def gh_p(g1, g2):
    for a, b, d, df, p in gh:
        if {a, b} == {g1, g2}:
            return p, df


# ============================================================================= document
# Section order follows the QM640 interim report template: Introduction, Scope and Objectives, Literature
# Survey, Data Description, Analysis, Modeling, Preliminary Results, Interim Limitations and Risks, Next Steps,
# References, Appendices. First-level (conclusion-bearing) tables and figures stay in the body; second-level
# supporting material is in Appendix E and is summarized in the body where it is referenced.
def build(toc_pages=None):
    D = APADoc()
    # Shared values used in several sections
    ORDS = ["price_sensitivity", "destination_flexibility", "date_flexibility", "exploration_breadth",
            "decisiveness", "detail_orientation", "information_upfront", "revision_tendency", "question_asking",
            "politeness"]
    cv_ = r1h["criterion_validity"]
    wk = trg[(trg.M == "whole") & trg.eligible].sort_values("kappa_N5").iloc[-1]
    a9 = abl[abl.M == "9"].set_index("config")
    aw = abl[abl.M == "whole"].set_index("config")
    feat = [("Destination flexibility", "destination_flexibility"), ("Date flexibility", "date_flexibility"),
            ("Exploration breadth", "exploration_breadth"), ("Decisiveness", "decisiveness"),
            ("Detail orientation", "detail_orientation"), ("Revision tendency", "revision_tendency"),
            ("Question asking", "question_asking"), ("Politeness", "politeness"),
            ("Price sensitivity", "price_sensitivity"), ("Information given up front", "information_upfront")]

    # ------------------------------------------------------------------ title page
    D.title_page(
        [TITLE, "Interim Report"],
        ["Surnella Sandeep", "Department of Data Analytics, Walsh College",
         "QM640: Data Analytics Capstone", "Mr. Smitraj Raut", "October 27, 2026"])

    # ------------------------------------------------------------------ repository link + contents
    D.para(f"<b>GitHub repository:</b> {REPO}", indent=False)
    D.toc(toc_pages[0] if toc_pages else [], toc_pages[1] if toc_pages else None)

    # ================================================================== INTRODUCTION
    D.heading(TITLE, 1)
    D.heading("Background and Context", 2)
    D.para(
        "Conversational artificial intelligence (AI) agents are now widely used in travel and tourism to support "
        "destination discovery, itinerary planning, and booking (Jannach et al., 2021). Travelers differ in how they "
        "converse: some state every constraint in the first message, some revise budgets and dates repeatedly, and "
        "others rely on the agent to lead the search (Inaba et al., 2022). Most travel assistants, however, use one "
        "static prompt for every user, which produces repetitive clarification questions, mismatched pacing, and "
        "abandoned sessions.")
    D.para(
        "Designers usually adapt a large language model (LLM) agent's style through prompt engineering, for example, "
        "by inserting example dialogues into the prompt. Prompt-only adaptation creates two risks (Rebedea et al., "
        "2023): the model can copy stale details such as earlier prices, dates, or destinations from the examples, "
        "and style instructions compete with business constraints, so the agent may propose an itinerary that "
        "violates passport, visa, capacity, or discount policies. This study therefore separates the two concerns: "
        "conversation archetypes learned from historical dialogues select in-context examples that steer style, and "
        "a declarative rule engine outside the prompt checks policy.")
    D.heading("Problem Statement", 2)
    D.para(
        "Travel conversational agents lack a data-driven way to recognize a user's conversation archetype and adapt "
        "their style to it, and prompt-based style steering can introduce factual leakage and policy violations. The "
        "study measures how four independent variables—clustering algorithm (RQ1), in-context conditioning strategy "
        "(RQ2), rule-engine mode (RQ3), and conditioning strategy crossed with user archetype (RQ4)—affect cluster "
        "separation, style convergence, slot accuracy, exemplar leakage, rule adherence, and turn economy.")
    D.heading("Purpose of the Study", 2)
    D.para("The purpose of this quantitative study is to", keep_next=True)
    D.items([
        "discover and interpret conversation archetypes in human travel dialogues and identify the clustering "
        "algorithm that separates them best (RQ1);",
        "measure whether archetype-matched in-context examples move an LLM agent's responses toward the target "
        "archetype's style more than zero-shot or static examples do (RQ2);",
        "isolate the effects of a declarative rule engine and of cluster-adaptive prompting on slot accuracy, "
        "exemplar leakage, and rule adherence (RQ3); and",
        "estimate whether cluster-adaptive prompting changes turn economy differently across archetypes (RQ4)."])
    D.heading("Interim Project Status", 2)
    D.items([
        "<i>Completed:</i> data ingestion, quality audit, cleaning, exploratory analysis, and power analysis; RQ1 "
        "end to end, including a sensitivity analysis that produced three refined archetypes (Decisive Booker, Open "
        f"Explorer, and Rigid-Constraint Seeker); and the RQ2 experiment ({r2x['n_calls']} LLM generations).",
        "<i>In progress:</i> groundwork for RQ3 and RQ4—the rule engine is verified, the corpus is audited for "
        "policy information, and a human baseline for turn economy is measured.",
        "<i>Pending:</i> repeating RQ2 with the refined archetypes, the RQ3 2 × 2 experiment, the RQ4 simulation, "
        "robustness checks, and the final report (Appendix B)."], numbered=False)

    # ================================================================== SCOPE AND OBJECTIVES
    D.heading("Scope and Objectives", 1)
    D.heading("Inclusions", 2)
    D.para(
        f"The study includes English-language, multi-turn, human–human travel dialogues from two public corpora: all "
        f"{n2(n_frames_raw, 0)} Microsoft Frames dialogues and a {n2(int(mq.n_raw), 0)}-dialogue sample of MultiWOZ 2.2 "
        "dialogues that involve at least one travel service (hotel, train, taxi, or attraction), each with at least "
        "three turns. The pre-specified analyses use one embedding model (Sentence-BERT all-MiniLM-L6-v2), three "
        "clustering algorithms, and one LLM family (Gemini Flash); the RQ1 sensitivity analysis adds Gemini "
        "embeddings and LLM ratings of user behavior. Scope is contained by using Frames as the only corpus for "
        "learning, retrieval, and experiments, and by having every research question reuse one pipeline, one set of "
        "archetype assignments, and one held-out partition, so that each later question adds an experimental factor "
        "rather than a new method.")
    D.heading("Exclusions", 2)
    D.para(
        "No claim is made that Frames archetypes transfer to MultiWOZ or other domains; MultiWOZ serves only as a "
        "descriptive projection check. Proprietary, enterprise, or customer data, new human-subject data, and "
        "synthetic training dialogues are excluded; the only synthetic elements are the author-defined policy rules "
        "and scenarios used in RQ3. Non-English, voice, restaurant-only, and sub-three-turn dialogues, model "
        "fine-tuning, other LLM providers, live deployment, real bookings, and user-satisfaction outcomes are also "
        "out of scope.")
    D.heading("Feasibility", 2)
    D.para(
        "Both corpora are freely downloadable, and the core pipeline runs on a laptop in under 15 minutes. RQ2 "
        f"required {int(ss.loc['RQ2', 'N_final']) * 3} LLM calls, the RQ1 sensitivity analysis "
        f"{n2(n_ann_calls, 0)} annotation calls, and RQ3 and RQ4 together need fewer than 2,000, all within the free "
        "tier of the Gemini application programming interface. Every response is cached so that interrupted runs "
        "resume.")
    D.heading("Research Questions and Hypotheses", 2)
    D.para("Table 1 states each research question with its hypotheses and the analysis that tests it.")
    D.table(
        "Research Questions, Hypotheses, and Planned Analyses",
        ["RQ", "Research question", "Hypotheses", "Analysis"],
        [["RQ1", "Which clustering algorithm (K-Means, agglomerative, HDBSCAN) gives the best separation of "
                 "dialogue-trajectory embeddings, and which archetypes emerge?",
          "H<sub>0</sub>: mean Silhouette is equal across algorithms. H<sub>1</sub>: at least one mean differs.",
          "One-way ANOVA (Welch and Kruskal–Wallis as robustness checks); Tukey and Games–Howell post hoc"],
         ["RQ2", "Does cluster-adaptive few-shot prompting increase style convergence relative to zero-shot and "
                 "static few-shot prompting?",
          "H<sub>0</sub>: mean style cosine is equal across conditions. H<sub>1</sub>: cluster-adaptive > static "
          "and zero-shot.",
          "One-way repeated-measures ANOVA; Greenhouse–Geisser correction; Holm-adjusted paired contrasts"],
         ["RQ3", "Do a declarative rule engine and cluster-adaptive prompting affect slot F1, exemplar leakage, and "
                 "rule adherence?",
          "H<sub>0</sub>: no main or interaction effects. H<sub>1</sub>: rules raise adherence and reduce leakage "
          "without lowering style convergence.",
          "2 × 2 between-subjects factorial ANOVA"],
         ["RQ4", "Does cluster-adaptive prompting change turns to goal completion and redundant elicitation "
                 "differently across archetypes?",
          "H<sub>0</sub>: no conditioning × archetype interaction. H<sub>1</sub>: the reduction in turns differs "
          "by archetype.",
          "2 × 3 factorial ANOVA on log turns"]],
        note="RQ = research question; ANOVA = analysis of variance. Significance level α = .05 for all tests.",
        widths=[0.5, 2.1, 2.1, 1.8], align=["l", "l", "l", "l"])

    # ================================================================== LITERATURE SURVEY
    D.heading("Literature Survey", 1)
    D.heading("Literature Review Approach", 2)
    D.para(
        "Sources were located in the ACL Anthology, Google Scholar, and arXiv with combinations of the terms "
        "task-oriented dialogue corpus, dialogue clustering, sentence embeddings, in-context example selection, LLM "
        "guardrails, policy compliance, and LLM annotation. Peer-reviewed papers and widely cited preprints were "
        "retained when they supplied a corpus, method, or measure used in this study, and seminal statistical "
        "sources were added for each metric and test. Each source was mapped to the research questions it informs; "
        "the relevance matrix of the closest studies is in Appendix C.")
    D.heading("Thematic Review and Research Gaps", 2)
    D.lead_para(
        "Task-oriented dialogue corpora",
        "MultiWOZ (Budzianowski et al., 2018) is the standard multi-domain benchmark, and MultiWOZ 2.2 (Zang et al., "
        "2020) corrected its state annotations, but it covers local services in one city and contains no flights or "
        "package negotiation. Microsoft Frames (El Asri et al., 2017) was designed for exactly that setting: users "
        "negotiate flight-and-hotel packages under a budget and compare several offers before deciding. Frames is "
        "therefore the primary corpus, and MultiWOZ 2.2 is an external comparison.")
    D.lead_para(
        "Dialogue representation and clustering",
        "Sentence-BERT (Reimers & Gurevych, 2019) yields embeddings whose cosine distances reflect semantic "
        "similarity, enabling whole-dialogue representations without task-specific training. K-Means, Ward "
        "agglomerative clustering, and HDBSCAN (McInnes et al., 2017) assume different cluster shapes and should be "
        "compared rather than chosen a priori; quality is judged with the Silhouette coefficient (Rousseeuw, 1987) "
        "and the Davies–Bouldin index (Davies & Bouldin, 1979), and stability with the adjusted Rand index under "
        "resampling (Hennig, 2007; Hubert & Arabie, 1985). UMAP (McInnes et al., 2018) and scikit-learn (Pedregosa "
        "et al., 2011) support inspection and reproducibility.")
    D.lead_para(
        "In-context exemplar selection",
        "LLMs can perform new tasks from a few in-context examples (Brown et al., 2020), and examples retrieved by "
        "embedding similarity outperform random ones (Liu et al., 2022); FAISS (Johnson et al., 2021) makes such "
        "retrieval fast. These studies evaluate single-turn accuracy, not conversational style, and retrieve from "
        "one global pool rather than from behaviorally defined sub-pools. LLMs can also annotate text as reliably "
        "as trained crowd workers (Gilardi et al., 2023), which supports LLM ratings of user behavior.")
    D.lead_para(
        "Policy compliance and evaluation",
        "NeMo Guardrails (Rebedea et al., 2023) moves policy logic into programmable rails outside the model, "
        "τ-bench (Yao et al., 2024) shows that policy adherence must be measured separately from task success, and "
        "TD-EVAL (Acikgoz et al., 2025) argues that dialogue-level similarity such as BERTScore (Zhang et al., 2020) "
        "must be complemented by turn-level checks of factual consistency and policy compliance.")
    D.para(
        "Three gaps follow. No reviewed study derives conversation archetypes from dialogue trajectories and uses "
        "them to select in-context examples; studies that steer style do not measure whether examples leak stale "
        "facts, and studies that enforce policy do not adapt style; and the turn-economy effect of style adaptation "
        "across user archetypes has not been tested. RQ1 and RQ2 address the first gap, RQ3 the second, and RQ4 "
        "the third.")

    # ================================================================== DATA DESCRIPTION
    D.heading("Data Description", 1)
    D.heading("Data Sources and Access", 2)
    D.para(
        f"Microsoft Frames (El Asri et al., 2017) contains {n2(n_frames_raw, 0)} English Wizard-of-Oz dialogues in "
        "which a user role-player negotiates a flight-and-hotel package with a wizard who searches a database of "
        "fictional cities; it is available from Microsoft Research at "
        "https://www.microsoft.com/en-us/research/project/frames-dataset/. MultiWOZ 2.2 (Zang et al., 2020) contains "
        "10,438 dialogues with per-turn dialogue states and is available at https://github.com/budzianowski/multiwoz. "
        "Both corpora were downloaded in full and are public, were collected with consent for research use, and "
        "identify role-players only by codes, so no new human data are collected. Only public dialogue text with "
        "fictional cities is sent to the LLM, and archetypes are described only by conversational behavior, never by "
        "inferred demographics.")
    D.heading("Dataset Overview", 2)
    D.para("Table 2 summarizes the records, variables, time coverage, unit of analysis, and outcome variables.")
    D.table("Dataset Overview",
            ["Attribute", "Microsoft Frames (primary)", "MultiWOZ 2.2 (comparison)"],
            [["Records", f"{n2(n_frames_raw, 0)} dialogues; {n2(fq.n_analytic, 0)} analytic (golden partition "
                         f"{s1['n_gold']}, held-out partition {s1['n_test']})",
              f"10,438 dialogues; seeded sample of {n2(mq.n_raw, 0)}; {n2(mq.n_analytic, 0)} analytic"],
             ["Variables used", "Utterance text, speaker, dialogue acts with slot–value arguments, task-success "
                                "label, user rating, role-player codes (Table E1)",
              "Utterance text, speaker, services, per-turn dialogue state (Table E1)"],
             ["Time period", "Released 2017; timestamps record collection time only and are not analyzed",
              "Released 2018 (version 2.2 in 2020); no timestamps"],
             ["Unit of analysis", "Dialogue; clustering run (RQ1 algorithm test); generated agent turn (RQ2)",
              "Dialogue (descriptive projection only)"],
             ["Target or outcome", "No supervised target; outcomes are Silhouette (RQ1), style convergence (RQ2), "
                                   "slot F1, leakage, and adherence (RQ3), turns and redundant elicitation (RQ4)",
              "Similarity to the nearest Frames centroid"]],
            widths=[1.3, 2.75, 2.45], align=["l", "l", "l"])
    D.heading("Data Dictionary", 2)
    D.para(
        "Table 3 defines the analysis variables. The raw source fields read from each corpus and the canonical "
        "schema produced by preprocessing are listed in Tables E1 and E2 in Appendix E.")
    D.table("Data Dictionary of the Analysis Variables",
            ["Variable", "Role", "Type", "Operational definition", "RQ"],
            [["Clustering algorithm", "IV", "Nominal (3)", "K-Means, Ward agglomerative, HDBSCAN", "1"],
             ["Silhouette coefficient", "DV", "Continuous [−1, 1]", "Cosine Silhouette of a clustering run", "1"],
             ["Davies–Bouldin index", "DV", "Continuous ≥ 0", "Mean cluster similarity ratio (lower is better)", "1"],
             ["Archetype (primary)", "IV / moderator", "Nominal (3)", "Nearest frozen <i>K</i>-Means centroid "
              "(cosine, MiniLM trajectory vectors)", "1, 2"],
             ["Archetype (refined)", "IV / moderator", "Nominal (3)", "<i>K</i>-Means on the Gemini embedding and "
              "LLM behavior profile of the first nine user messages", "1, 3, 4"],
             ["Behavior rating", "Feature", "Ordinal (1–5)", "Ten LLM ratings of user behavior (Appendix D)", "1"],
             ["Conditioning strategy", "IV", "Nominal (3)", "Zero-shot, static few-shot, cluster-adaptive few-shot "
              "(<i>k</i> = 3 exemplars)", "2–4"],
             ["Style convergence", "DV", "Continuous [−1, 1]", "Cosine between response and target archetype's "
              "agent-style centroid", "2, 3"],
             ["Gold similarity", "DV", "Continuous [−1, 1]", "Cosine between response and the human reply", "2"],
             ["Rule-engine mode", "IV", "Nominal (2)", "Active or off", "3"],
             ["Slot F1", "DV", "Proportion", "F1 of slot values in the response against the dialogue state", "3"],
             ["Exemplar leakage rate", "DV", "Proportion", "Entities in the response that occur in exemplars but "
              "not in the dialogue / all entities", "3"],
             ["Rule adherence rate", "DV", "Proportion", "1 − (violating agent turns / agent turns)", "3"],
             ["Turns to goal completion", "DV", "Count (log)", "Turns until all required slots are filled and an "
              "offer is accepted", "4"],
             ["Redundant elicitation rate", "DV", "Proportion", "Agent requests for an already-informed slot / "
              "agent turns", "4"]],
            note="IV = independent variable; DV = dependent variable. All cosine measures use de-lexicalized text and "
                 "all-MiniLM-L6-v2 embeddings.",
            widths=[1.5, 0.85, 1.05, 2.6, 0.5], align=["l", "l", "l", "l", "c"], split=True)
    D.heading("GitHub Data Availability Statement", 2)
    D.para(
        f"Code, configuration, processed data, and results are in the public repository ({REPO}). The raw corpora "
        "are not redistributed: data/raw/ is excluded from version control and is recreated by downloading Frames "
        "and MultiWOZ 2.2 from the sources above. Processed data (cleaned samples, partitions, archetype labels, LLM "
        "annotations, and saved prompts) are in data/interim/, result tables and figures in outputs/interim/, and the "
        "analysis code in src/interim_pipeline/. This report is generated from those files, so rerunning the steps "
        "in Appendix A reproduces every number.")
    D.heading("Dataset Limitations", 2)
    cmp_ = comp.set_index("slot")
    D.para(
        f"Frames dialogues were produced by {n_users} user role-players and {n_wizards} wizards following written "
        "scenarios, so archetypes may partly reflect individual habits, and its cities and prices are fictional. "
        "MultiWOZ covers one city without flights or package negotiation and records price only as a category. "
        "Several slots are often absent (Table E3): Frames mentions children in only "
        f"{pct(cmp_.loc['traveler_count_children', 'frames_pct'])} of dialogues and trip duration in "
        f"{pct(cmp_.loc['duration_nights', 'frames_pct'])}, MultiWOZ never records a return date, and neither corpus "
        "contains visa, passport, or discount information, so RQ3 must inject these conditions. Neither corpus "
        "records demographics or real booking outcomes; the Frames task-success label is wizard-reported and "
        f"imbalanced ({pct(fd.success_pct)} successful), and {int(fq.missing_user_rating)} dialogues lack a user "
        "rating.")

    # ================================================================== ANALYSIS
    D.heading("Analysis", 1)
    D.heading("Data Cleaning", 2)
    D.para(
        "Table 4 is the cleaning log. Missing slot values are not imputed, because a slot that is never mentioned is "
        "correctly unobserved for a dialogue-state tracker, and turn-count outliers are retained because long "
        "negotiations are genuine behavior of interest.")
    D.para(
        "Both corpora were parsed into one canonical format. Frames labels such as <i>dst_city</i> and MultiWOZ labels "
        "such as <i>train-destination</i> were mapped to a two-tier schema: Tier 1 holds nine universal travel slots "
        "(origin, destination, departure and return dates, duration, adults, children, budget, and accommodation "
        "tier), and Tier 2 holds policy slots (visa processing window, passport validity, package type, room "
        "sharing, and discount) used only by the rule engine. After cleaning, the "
        f"{n2(int(fq.n_analytic), 0)} analytic Frames dialogues were split once (seed 42, stratified on task "
        f"success) into a golden partition (<i>D</i><sub>gold</sub>, 70%, <i>n</i> = {s1['n_gold']}) used to fit "
        "clusters and build the exemplar pool, and a held-out partition (<i>D</i><sub>test</sub>, 30%, <i>n</i> = "
        f"{s1['n_test']}) used only for evaluation.")
    D.table("Data Cleaning Log",
            ["Issue", "Variables", "Detection", "Frames", "MultiWOZ", "Treatment and rationale"],
            [["Duplicate identifiers", "Dialogue ID", "Uniqueness check", "0", "0", "None needed"],
             ["Duplicate full text", "All utterances", "Hash of the dialogue text", str(int(fq.duplicate_text)),
              str(int(mq.duplicate_text)), "Removed; would double-weight one dialogue"],
             ["Empty utterances", "Utterance text", "Length check", "0", "0", "None needed"],
             ["Fewer than three turns", "Turns", "Turn count", str(int(fq.excluded_lt_min_turns)),
              str(int(mq.excluded_lt_min_turns)), "Excluded; no negotiation trajectory"],
             ["Turn-count outliers", "Turns", "> Q3 + 1.5 × IQR",
              f"{int(fq.turn_outliers_iqr)} (> {n2(fq.outlier_threshold, 1)})",
              f"{int(mq.turn_outliers_iqr)} (> {n2(mq.outlier_threshold, 1)})",
              "Retained; decay weighting and log turns limit influence"],
             ["Missing slot values", "Tier 1 and 2 slots", "Slot never mentioned", "See Figure 2", "See Figure 2",
              "Not imputed; unobserved is the correct state"],
             ["Missing user rating", "User rating", "Null check", str(int(fq.missing_user_rating)), "Not available",
              "Retained; rating is descriptive only"],
             ["Corpus-specific labels", "Slots, speakers", "Schema mapping", "All", "All",
              "Mapped to one two-tier schema; speakers become USER or AGENT"],
             ["Entity values in text", "Utterance text", "Slot values and numbers", "All", "All",
              "Replaced with slot tokens so examples carry style, not facts"],
             ["Analytic sample", "", "", n2(fq.n_analytic, 0), n2(mq.n_analytic, 0), ""]],
            note="IQR = interquartile range. Restaurant-only MultiWOZ dialogues were excluded before sampling. No "
                 "dialogue lacked a task-success label (Frames).",
            widths=[1.25, 1.0, 1.15, 0.6, 0.7, 1.8], align=["l", "l", "l", "c", "c", "l"], split=True)
    D.heading("Exploratory Data Analysis Results", 2)
    D.para(
        "Table 5 describes the analytic samples. Frames and MultiWOZ dialogues have similar mean lengths "
        f"(<i>M</i> = {n2(fd.turns_M)} and {n2(md.turns_M)} turns), but Frames lengths vary more "
        f"(<i>SD</i> = {n2(fd.turns_SD)} vs. {n2(md.turns_SD)}) and have a longer right tail (Figure 1). The golden and "
        "held-out partitions are nearly identical in length, utterance length, and success rate, which confirms that "
        "the stratified split worked as intended.")
    rows = []
    for _, r in desc.iterrows():
        rows.append([r.corpus.replace(" (D_gold)", "").replace(" (D_test)", ""), n2(r.N, 0), f"{n2(r.turns_M)} ({n2(r.turns_SD)})", n2(r.turns_Mdn, 0),
                     f"{int(r.turns_min)}–{int(r.turns_max)}", n2(r.user_words_M, 1), n2(r.agent_words_M, 1),
                     "—" if pd.isna(r.success_pct) else n2(r.success_pct, 1)])
    D.table("Descriptive Statistics of the Analytic Samples",
            ["Sample", "<i>N</i>", "Turns <i>M</i> (<i>SD</i>)", "<i>Mdn</i>", "Range", "User words",
             "Agent words", "Task success (%)"],
            rows,
            note="User and agent words are mean words per utterance. Task success is the wizard-reported label "
                 "(not available in MultiWOZ).",
            widths=[2.0, 0.5, 0.95, 0.45, 0.6, 0.6, 0.6, 0.8], align=["l", "c", "c", "c", "c", "c", "c", "c"])
    D.figure("Distribution of Dialogue Length by Corpus", os.path.join(FIG, "fig_eda_turns.png"),
             note="Turn counts after cleaning. Frames <i>N</i> = "
                  f"{n2(fq.n_analytic, 0)}; MultiWOZ <i>N</i> = {n2(mq.n_analytic, 0)}.", width=5.6)
    D.para(
        "Figure 2 compares slot completeness (exact percentages in Table E3). Frames users state origin and "
        "destination in almost every dialogue and a budget in most, whereas MultiWOZ dialogues mention travel slots "
        "far less often and never mention return dates. Three insights shape the analysis. First, Frames is the only "
        "corpus with enough budget and package information for the negotiation behavior that the archetypes are "
        "meant to capture. Second, length differences between the corpora mean that any archetype tied to dialogue "
        "length will be distributed differently across corpora, which motivates treating MultiWOZ only as a "
        "descriptive check. Third, the absence of policy slots in both corpora confirms that RQ3 requires injected "
        "scenarios.")
    D.figure("Slot Completeness by Corpus", os.path.join(FIG, "fig_eda_slots.png"),
             note="Percentage of dialogues that mention each canonical slot at least once.", width=5.6)

    # ================================================================== MODELING
    D.heading("Modeling", 1)
    D.heading("Research Design and Sample Size", 2)
    D.para(
        "The study uses a quantitative design with one observational component (RQ1) and three controlled "
        "experiments (RQ2 to RQ4). All random steps use seed 42, and leakage is prevented by keeping the partitions "
        "disjoint, freezing centroids before any held-out dialogue is seen, routing and retrieving with only the "
        "turns available at generation time, and using the human reply only for scoring, never in a prompt.")
    D.para(
        "Each sample size was computed for the exact test used later, with a medium effect <i>f</i> = .25 (Cohen, "
        "1988), α = .05, and power .80, because no prior study reports effect sizes for these comparisons. Power was "
        "computed from the noncentral <i>F</i> distribution and checked against G*Power 3 (Faul et al., 2007):",
        keep_next=True)
    D.equation("1 − β = 1 − <i>F</i><sub>nc</sub>(<i>F</i><sub>crit</sub>; <i>df</i><sub>1</sub>, "
               "<i>df</i><sub>2</sub>, λ),   <i>F</i><sub>crit</sub> = <i>F</i><sub>1−α</sub>"
               "(<i>df</i><sub>1</sub>, <i>df</i><sub>2</sub>)", "1")
    r = ss.loc["RQ1"]
    D.para(
        "where <i>F</i><sub>nc</sub> is the cumulative noncentral <i>F</i> distribution and λ = "
        "<i>f</i><sup>2</sup><i>N</i> for between-subjects designs. The smallest <i>N</i> with power ≥ .80 "
        "(<i>N</i><sub>min</sub>) was rounded up to a balanced design and, for LLM experiments, increased by 10% for "
        f"failed generations. For RQ1, for example, <i>N</i> = {int(r.N_min)} gives λ = .0625 × {int(r.N_min)} = "
        f"{n2(r.lambda_at_Nmin, 3)}, <i>F</i><sub>crit</sub>(2, {int(r.df2_at_Nmin)}) = {n2(r.F_crit, 3)}, and power "
        f"= {nz(r.power_at_Nmin, 3)}, so {int(r.N_final)} clustering runs ({int(r.per_group)} per algorithm) are "
        "used. Table 6 gives the computation for every research question. The experiments draw from the held-out "
        f"partition, so the binding requirement is the largest experimental sample, {int(ss.loc['RQ4', 'N_final'])} "
        f"dialogues, which is smaller than |<i>D</i><sub>test</sub>| = {s1['n_test']}.", indent=False)
    rows = []
    for rq in ["RQ1", "RQ2", "RQ3", "RQ4"]:
        r = ss.loc[rq]
        rows.append([rq, r.Design.replace(" x ", " × "), f"{int(r.df1)}, {int(r.df2_at_Nmin)}",
                     n2(r.lambda_at_Nmin, 2), n2(r.F_crit, 2), str(int(r.N_min)), nz(r.power_at_Nmin, 3),
                     f"{int(r.N_final)} ({int(r.per_group)})", nz(r.power_final, 3)])
    D.table("Sample Size Calculations Matched to Each Planned Analysis",
            ["RQ", "Planned analysis", "<i>df</i> at <i>N</i><sub>min</sub>", "λ", "<i>F</i><sub>crit</sub>",
             "<i>N</i><sub>min</sub>", "Power", "<i>N</i><sub>final</sub> (per group)", "Final power"],
            rows,
            note="All calculations use <i>f</i> = .25 and α = .05. RQ1 units are clustering runs on subsamples of "
                 "the golden partition; RQ3 and RQ4 units are test dialogues. RQ2 units are test dialogues measured "
                 "under <i>m</i> = 3 conditions, with λ = <i>f</i><sup>2</sup><i>Nm</i>ε/(1 − ρ), ρ = .50, and "
                 "ε = 1 (Faul et al., 2007). RQ2 to RQ4 include a 10% buffer for failed generations.",
            widths=[0.45, 1.75, 0.65, 0.5, 0.5, 0.5, 0.55, 0.95, 0.65],
            align=["l", "l", "c", "c", "c", "c", "c", "c", "c"])

    D.heading("Choice of Models With Justification", 2)
    D.para(
        "No predictive model is trained. Each research question is answered with an unsupervised or experimental "
        "model and a statistical test matched to its design; baselines and assumptions are stated for each.")
    D.heading("RQ1: Clustering Algorithms and Archetype Definition", 3)
    D.para(
        "K-Means (<i>k</i> = 3, 10 initializations), Ward agglomerative clustering (<i>k</i> = 3), and HDBSCAN, "
        "which chooses the number of clusters itself, were each applied to "
        f"{int(ss.loc['RQ1', 'per_group'])} independent random subsamples of 500 golden dialogues and compared with a "
        "one-way ANOVA on Silhouette. HDBSCAN noise points were assigned to the nearest centroid so that every "
        "dialogue receives an archetype. The baselines are a permutation baseline (K-Means labels shuffled within "
        "each subsample) and K-Means as the conventional reference.")
    D.lead_para("Independence of runs",
                "Each run uses its own subsample; because subsamples share dialogues, the test compares algorithms on "
                "this corpus rather than across datasets.")
    D.lead_para("Normality",
                "Shapiro–Wilk tests did not reject normality (K-Means <i>W</i> = "
                f"{nz(sh['K-Means']['W'], 3)}, <i>p</i> {pv(sh['K-Means']['p'])}; agglomerative <i>W</i> = "
                f"{nz(sh['Agglomerative']['W'], 3)}, <i>p</i> {pv(sh['Agglomerative']['p'])}; HDBSCAN <i>W</i> = "
                f"{nz(sh['HDBSCAN']['W'], 3)}, <i>p</i> {pv(sh['HDBSCAN']['p'])}).")
    D.lead_para("Homogeneity of variance",
                f"Levene's test was significant, <i>W</i> = {n2(lev['W'])}, <i>p</i> {pv(lev['p'])}, so Welch's "
                "ANOVA, Games–Howell comparisons, and the Kruskal–Wallis test are reported as well.")
    D.lead_para("Meaningful embedding geometry",
                "Cosine distance is assumed to reflect conversational behavior; this was checked with behavioral "
                "features not used in clustering (Table 10).")
    D.lead_para("Cross-corpus invariance",
                "The synopsis assumed that Frames archetypes would apply to MultiWOZ; projection onto the frozen "
                "centroids did not support this.")
    D.para(
        "A sensitivity analysis varied whose turns are represented (whole dialogue or user turns), how (MiniLM or "
        "Gemini embeddings, with or without an LLM behavior profile), and how much of the conversation (first 3, 5, "
        "7, or 9 user messages, or all), under a selection rule fixed before results were inspected. "
        "Stability was the mean adjusted Rand index (ARI) between K-Means fits on two random 80% subsamples, "
        "repeated 50 times (Hennig, 2007). Eligible solutions had three to eight clusters, ARI ≥ .60, and a smallest "
        "cluster ≥ 5%; for each length, the eligible solution that a router could predict best from the first five "
        "turns (Cohen's κ) was retained, and the most stable retained solution was adopted. Two-cluster solutions "
        "were excluded in advance as too coarse for archetype-specific prompting. The confirmatory RQ1 test is "
        "unchanged; this analysis only selects the archetype labels used later.")
    D.lead_para("Valid behavior ratings",
                "LLM ratings are assumed to measure user behavior; this was tested by re-annotation and by "
                "correlation with behaviors counted from the corpus annotations (see Features).")

    D.heading("RQ2: Repeated-Measures Prompting Experiment", 3)
    D.para(
        f"The experiment sampled {int(ss.loc['RQ2', 'N_final'])} held-out dialogues, "
        f"{int(ss.loc['RQ2', 'per_group'])} per primary archetype (it was run before the sensitivity analysis). The "
        "first three turns form the prefix, and Gemini 2.5 Flash (temperature 0.2, reasoning disabled) generated the "
        "next agent turn under three conditions: zero-shot, static few-shot (the same three random golden exemplars "
        "for every dialogue), and cluster-adaptive few-shot, in which the prefix is routed to the nearest archetype "
        "centroid and the three most similar golden dialogues are retrieved from that archetype's FAISS index. "
        "Zero-shot and static few-shot are the baselines, and unclustered global nearest-neighbor retrieval (Liu et "
        "al., 2022) was compared in the pilot. A one-way repeated-measures ANOVA with Holm-adjusted contrasts tests "
        f"the conditions; all {r2x['n_calls']} generations completed (<i>N</i> = {r2x['N']}).")
    D.lead_para("Sphericity",
                f"Mauchly's test was not significant for style convergence, <i>W</i> = {nz(sc_a['mauchly_W'])}, "
                f"χ<sup>2</sup>(2) = {n2(sc_a['mauchly_chi2'])}, <i>p</i> {pv(sc_a['mauchly_p'])}, or gold "
                f"similarity, <i>W</i> = {nz(gc_a['mauchly_W'])}, <i>p</i> {pv(gc_a['mauchly_p'])}; "
                "Greenhouse–Geisser-corrected results (Greenhouse & Geisser, 1959) are reported for consistency.")
    D.lead_para("Normality of difference scores",
                f"Shapiro–Wilk <i>p</i> values for the paired differences ranged from {nz(min(sc_sh), 3)} to "
                f"{nz(max(sc_sh), 3)}, so the Friedman test is reported as a distribution-free check.")
    D.lead_para("Valid style metric and correct routing",
                "The style score assumes that a turn written for an archetype is closer to its agent-style "
                "centroid, and routing assumes that the prefix identifies the archetype; the pilot tested both.")
    D.lead_para("Exemplars carry style, not facts",
                "De-lexicalization is assumed to remove factual content; this is tested as exemplar leakage in RQ3.")

    D.heading("RQ3: Rules-by-Prompting Factorial Experiment", 3)
    D.para(
        f"RQ3 randomly assigns {int(ss.loc['RQ3', 'N_final'])} held-out dialogues to a 2 × 2 between-subjects design "
        "(rule engine active or off × zero-shot or cluster-adaptive prompting with the refined archetypes). Each "
        "dialogue state is augmented with seeded synthetic Tier 2 values, half of which violate at least one rule. "
        "When active, the engine evaluates the state before generation and adds violations to the prompt as "
        "required actions. The baseline cell is zero-shot prompting with rules off. Table 7 lists the five "
        "author-defined rules, which do not represent any company's policy.")
    D.lead_para("Deterministic rule evaluation",
                f"All {r34['rule_tests_passed']} of {r34['rule_tests_total']} boundary tests passed, including "
                "values exactly at each threshold and the domestic and group-package exemptions.")
    D.lead_para("Decoupling",
                "Rules are assumed to act independently of prompt style; this is the interaction term, so it is "
                "tested rather than assumed.")
    D.lead_para("Residual normality and equal variances",
                "Shapiro–Wilk and Levene tests will be applied; because adherence proportions are likely near 0 or "
                "1, an aligned rank transform ANOVA or a logistic model will be used if they fail.")
    D.lead_para("International travel",
                "Frames cities are fictional, so all trips are treated as international for the visa, passport, "
                "and budget rules.")
    D.table("Declarative Policy Rules Used in RQ3",
            ["Rule", "Condition", "Action", "Severity"],
            [[r["name"], r["condition"].replace("budget_amount is not None and ", "budget stated; ").replace("==", "=").replace(" and ", "; "),
              r["action"].replace("_", " ").lower(), r["severity"].lower()] for _, r in rules.iterrows()],
            note="Rules are stored in a YAML file and evaluated outside the LLM by src/rule_engine.py.",
            widths=[1.9, 2.5, 1.3, 0.8], align=["l", "l", "l", "l"])

    D.heading("RQ4: Turn-Economy Simulation", 3)
    D.para(
        f"RQ4 uses {int(ss.loc['RQ4', 'N_final'])} held-out dialogues, {int(ss.loc['RQ4', 'per_group'])} per cell of "
        "a 2 × 3 design (zero-shot or cluster-adaptive prompting × the three refined archetypes; the held-out "
        f"partition contains {r1r['test_counts'][ARCH2[0]]}, {r1r['test_counts'][ARCH2[1]]}, and "
        f"{r1r['test_counts'][ARCH2[2]]} dialogues of these archetypes). An LLM user simulator receives the "
        "dialogue's user goal and its archetype profile (Table 12) and converses with the agent until the goal is "
        "met or 30 turns elapse. The zero-shot agent is the baseline, and the human dialogues give a reference "
        "level. A 2 × 3 factorial ANOVA on log turns tests the interaction.")
    D.lead_para("Log-normal turn counts",
                "Turn counts are right-skewed and are analyzed on the log scale; residuals will be checked with "
                "Shapiro–Wilk tests.")
    D.lead_para("Equal variances",
                "In the human baseline, Levene's test on log turns was significant, "
                f"<i>W</i> = {n2(r4r['levene_log_turns']['W'])}, <i>p</i> {pv(r4r['levene_log_turns']['p'])}, so "
                "heteroscedasticity-robust (HC3) standard errors will be used.")
    D.lead_para("Comparable goals",
                "Turn counts are compared only within Frames, so the schema need not be invariant across corpora.")
    D.lead_para("Archetype effect by construction",
                "Archetypes partly reflect dialogue length, so an archetype main effect is expected and is not a "
                "finding; the tests of interest are the conditioning effect and the interaction.")
    D.lead_para("Valid persona simulation",
                "Simulated user turns will be annotated with the same codebook and tested for assignment to the "
                "intended archetype above chance.")

    D.heading("Features Included and Feature Engineering", 2)
    D.para(
        "<i>Trajectory vectors (primary archetypes, RQ2 routing).</i> Each de-lexicalized turn <i>t</i> of a "
        "dialogue with <i>T</i> turns was embedded with Sentence-BERT as a 384-dimensional vector "
        "<b>e</b><sub><i>t</i></sub>, and the dialogue vector is the decay-weighted mean", keep_next=True)
    D.equation("<b>v</b> = Σ<sub><i>t</i></sub> <i>w</i><sub><i>t</i></sub><b>e</b><sub><i>t</i></sub>,   "
               "<i>w</i><sub><i>t</i></sub> = exp[−λ<sub>d</sub>(<i>T</i> − <i>t</i>)] / "
               "Σ<sub><i>j</i></sub> exp[−λ<sub>d</sub>(<i>T</i> − <i>j</i>)]", "2")
    D.para(
        "with λ<sub>d</sub> = 0.15 and L2 normalization, which emphasizes how a dialogue develops and closes. "
        "Structural features (turns, revisions, hesitations, offers) are excluded from the vector and used only to "
        "interpret clusters.", indent=False)
    D.para(
        "<i>Hybrid features (refined archetypes).</i> Two equally weighted blocks were combined: the first 20 "
        "principal components of the Gemini embedding (gemini-embedding-001, 3,072 dimensions; Lee et al., 2025) of "
        "the user's messages, and an LLM behavior profile. For the profile, Gemini 2.5 Flash (temperature 0, output "
        "constrained to a JSON schema) rated each user against a 16-field codebook (Table D1): ten 1–5 ratings such "
        "as price sensitivity, destination flexibility, decisiveness, and revision tendency, plus goal and tone "
        "indicators; outcome and party type were annotated but not used. Both blocks were computed on the same first "
        "<i>M</i> user messages. Re-annotating 100 random dialogues at temperature 0.7 gave quadratic-weighted κ from "
        f"{nz(min(r1h['reliability'][x] for x in ORDS))} to {nz(max(r1h['reliability'][x] for x in ORDS))} for the "
        f"ratings, and the ratings correlated with behaviors counted from the Frames acts, for example revision "
        f"tendency with slot revisions (ρ = {nz(cv_['revision_tendency~user_revisions']['rho'])}) and question "
        f"asking with request rate (ρ = {nz(cv_['question_asking~request_rate']['rho'])}; Table D2).")
    D.para(
        "<i>Exemplar features (RQ2 to RQ4).</i> Retrieval keys embed the same number of opening turns as the test "
        "prefix, so neither side uses future turns; exemplars are de-lexicalized and truncated to six turns.")

    D.heading("Evaluation Metrics", 2)
    D.para("Table 8 defines every outcome metric with its formula.")
    D.table("Evaluation Metrics and Formulae",
            ["Metric", "Formula", "RQ", "Interpretation"],
            [["Silhouette", "<i>s</i>(<i>i</i>) = [<i>b</i>(<i>i</i>) − <i>a</i>(<i>i</i>)] / max{<i>a</i>(<i>i</i>), "
              "<i>b</i>(<i>i</i>)}, averaged over <i>i</i>; <i>a</i>, <i>b</i> = mean cosine distance to own and "
              "nearest other cluster", "1", "−1 to 1; higher is better separated"],
             ["Davies–Bouldin index", "<i>DB</i> = (1/<i>k</i>) Σ<sub><i>i</i></sub> max<sub><i>j</i>≠<i>i</i></sub> "
              "(σ<sub><i>i</i></sub> + σ<sub><i>j</i></sub>) / <i>d</i>(<b>c</b><sub><i>i</i></sub>, "
              "<b>c</b><sub><i>j</i></sub>)", "1", "≥ 0; lower is better"],
             ["Adjusted Rand index", "<i>ARI</i> = (<i>RI</i> − E[<i>RI</i>]) / (max <i>RI</i> − E[<i>RI</i>])", "1",
              "0 = chance agreement; 1 = identical partitions"],
             ["Cohen's κ", "κ = (<i>p</i><sub>o</sub> − <i>p</i><sub>e</sub>) / (1 − <i>p</i><sub>e</sub>)", "1",
              "Routing and rating agreement beyond chance"],
             ["Cramér's <i>V</i>", "<i>V</i> = √[χ<sup>2</sup> / (<i>N</i>(min(<i>r</i>, <i>c</i>) − 1))]", "1",
              "0 to 1; association of archetype with a category"],
             ["Style convergence", "cos(<b>r</b>, <b>c</b><sub><i>a</i></sub>) = <b>r</b> · <b>c</b><sub><i>a</i></sub> "
              "/ (‖<b>r</b>‖ ‖<b>c</b><sub><i>a</i></sub>‖); <b>c</b><sub><i>a</i></sub> = mean golden agent turn of "
              "archetype <i>a</i>", "2, 3", "Higher is closer to the target style"],
             ["Gold similarity", "cos(<b>r</b>, <b>h</b>); <b>h</b> = embedding of the human reply", "2",
              "Higher is closer to the human agent"],
             ["Slot F1", "<i>F</i><sub>1</sub> = 2<i>PR</i> / (<i>P</i> + <i>R</i>) over slot values", "3",
              "0 to 1; higher is more accurate"],
             ["Exemplar leakage rate", "|<i>E</i><sub>r</sub> ∩ (<i>E</i><sub>x</sub> \\ <i>E</i><sub>d</sub>)| / "
              "|<i>E</i><sub>r</sub>|; entities in response, exemplars, dialogue", "3", "0 to 1; lower is better"],
             ["Rule adherence rate", "1 − <i>V</i><sub>t</sub> / <i>A</i><sub>t</sub>; violating and all agent turns",
              "3", "0 to 1; higher is better"],
             ["Turns to goal", "Turns until all required slots are filled and an offer is accepted (log scale)",
              "4", "Lower is more economical"],
             ["Redundant elicitation rate", "<i>R</i><sub>red</sub> / <i>A</i><sub>t</sub>; requests for an "
              "already-informed slot over agent turns", "4", "0 to 1; lower is better"]],
            note="Cosine measures use de-lexicalized all-MiniLM-L6-v2 embeddings. ARI follows Hubert and Arabie "
                 "(1985). BERTScore (Zhang et al., 2020) is planned as a token-level check for the final report.",
            widths=[1.35, 3.0, 0.5, 1.65], align=["l", "l", "c", "l"], split=True)

    # ================================================================== PRELIMINARY RESULTS
    D.heading("Preliminary Results", 1)
    # ------------------------------------------------------------------ RQ1 primary
    D.heading("RQ1: Clustering Algorithms and Primary Archetypes (Complete)", 2)
    best_k = int(k_sel.loc[k_sel.silhouette.idxmax(), "k"])
    ks = k_sel.set_index("k")
    D.para(
        f"On the full golden partition, Silhouette was highest at <i>k</i> = {best_k} "
        f"({nz(ks.loc[best_k, 'silhouette'], 3)}) and nearly flat from <i>k</i> = 3 to 5 "
        f"({nz(ks.loc[3, 'silhouette'], 3)} to {nz(ks.loc[5, 'silhouette'], 3)}), with no clear Davies–Bouldin or "
        "inertia elbow, so the pre-specified <i>k</i> = 3 was retained to give interpretable archetypes with enough "
        f"exemplars (smallest cluster {pct(ks.loc[3, 'smallest_cluster_pct'])}; see Table E4 and Figure E1 in "
        "Appendix E for the diagnostics).")
    D.para(
        f"Table 9 compares the algorithms. HDBSCAN produced the highest mean Silhouette (<i>M</i> = "
        f"{nz(hd.sil_M, 3)}, <i>SD</i> = {nz(hd.sil_SD, 3)}), followed by K-Means (<i>M</i> = {nz(km.sil_M, 3)}, "
        f"<i>SD</i> = {nz(km.sil_SD, 3)}) and agglomerative clustering (<i>M</i> = {nz(ag.sil_M, 3)}, <i>SD</i> = "
        f"{nz(ag.sil_SD, 3)}), and all three far exceeded the permutation baseline (<i>M</i> = {nz(perm['M'], 3)}). "
        f"The one-way ANOVA was significant, <i>F</i>({int(an['df1'])}, {int(an['df2'])}) = {n2(an['F'])}, "
        f"<i>p</i> {pv(an['p'])}, η<sup>2</sup> = {nz(eta)}, and held under Welch's correction, "
        f"<i>F</i>({int(we['df1'])}, {n2(we['df2'])}) = {n2(we['F'])}, <i>p</i> {pv(we['p'])}, and the "
        f"Kruskal–Wallis test, <i>H</i>(2) = {n2(kw['H'])}, <i>p</i> {pv(kw['p'])}. Every pairwise difference was "
        "significant under Tukey and Games–Howell comparisons (Table E5; runs plotted in Figure E2). The null "
        "hypothesis is rejected.")
    kf = r1["hdbscan_k_found"]
    k_mode = max(kf, key=kf.get)
    D.para(
        "Two qualifications matter. HDBSCAN's advantage depends on its settings: with the common minimum cluster size "
        f"of 15 it found no clusters in {r1['hdbscan_default_fail']} of {int(ss.loc['RQ1', 'per_group'])} subsamples, "
        f"and with a minimum of 5 it still labeled {pct(100 * r1['hdbscan_noise_M'])} of dialogues as noise and found "
        f"{min(map(int, kf))} to {max(map(int, kf))} clusters (most often {k_mode}), so its higher Silhouette partly "
        "reflects fewer clusters. All Silhouette values are below .25, which indicates weak structure: archetypes "
        "are tendencies on a continuum. Because routing needs a stable number of archetypes and a centroid for every "
        "dialogue, K-Means with <i>k</i> = 3 defined the archetypes.")
    D.table("Cluster Quality by Algorithm",
            ["Algorithm", "<i>n</i> runs", "Silhouette <i>M</i>", "Silhouette <i>SD</i>", "Davies–Bouldin <i>M</i>",
             "Davies–Bouldin <i>SD</i>"],
            [[a, str(int(r.n)), nz(r.sil_M, 3), nz(r.sil_SD, 3), n2(r.db_M, 3), n2(r.db_SD, 3)]
             for a, r in [("K-Means", km), ("Agglomerative (Ward)", ag), ("HDBSCAN", hd)]]
            + [["Permutation baseline", str(int(ss.loc['RQ1', 'per_group'])), nz(perm['M'], 3), nz(perm['SD'], 3),
                "—", "—"]],
            note="Each run clusters an independent random subsample of 500 golden dialogues. The permutation "
                 "baseline shuffles K-Means labels within each subsample.",
            widths=[1.7, 0.8, 1.0, 1.0, 1.0, 1.0], align=["l", "c", "c", "c", "c", "c"])
    pr = prof.reindex(ARCH)
    dt_, cn_, ge_ = (pr.loc[a] for a in ["Direct Transactional", "Constraint Negotiator", "Guided Explorer"])
    D.para(
        "Table 10 profiles the archetypes on features not used for clustering; names follow a fixed rule (most "
        "revisions = Constraint Negotiator; longer of the other two = Guided Explorer). Direct Transactional "
        f"dialogues are short ({n2(dt_.turns_M, 1)} turns) with almost no offers ({n2(dt_.offers)}). Constraint "
        f"Negotiators write the longest utterances and revise slot values most often ({n2(cn_.revisions, 1)}). Guided "
        f"Explorers form the largest group ({pct(ge_.pct)}) and have the longest dialogues ({n2(ge_.turns_M, 1)} "
        "turns) but the shortest user utterances, indicating an agent-led search. Task success is high in every "
        "archetype, so they differ in how users converse rather than in whether they succeed.")
    D.para(
        "Archetype was associated with the Frames user role-player, χ<sup>2</sup>"
        f"({chi_u[2]}, <i>N</i> = {n2(ct.values.sum(), 0)}) = {n2(chi_u[0])}, <i>p</i> {pv(chi_u[1])}, Cramér's "
        f"<i>V</i> = {nz(cramer_v)}, so individual role-player style contributes to the archetypes. The frozen "
        "centroids generalized within Frames: centroid similarity did not differ between golden and held-out "
        f"dialogues, <i>t</i>({n2(gt['df'], 1)}) = {n2(gt['t'])}, <i>p</i> {pv(gt['p'])}, and held-out proportions "
        f"matched the golden ones, χ<sup>2</sup>(2, <i>N</i> = {int(test_counts.sum())}) = {n2(chi_gt.statistic)}, "
        f"<i>p</i> {pv(chi_gt.pvalue)}. They did not transfer to MultiWOZ: MultiWOZ dialogues were far less similar to "
        f"their nearest Frames centroid (<i>M</i> = {nz(cr.loc['MultiWOZ 2.2', 'sim_M'], 3)} vs. "
        f"{nz(cr.loc['Frames D_test', 'sim_M'], 3)}), <i>t</i>({n2(cc['df'], 1)}) = {n2(cc['t'])}, <i>p</i> "
        f"{pv(cc['p'])}, and {pct(cr.loc['MultiWOZ 2.2', 'Guided Explorer'])} fell into one archetype (Table E6 and "
        "the UMAP projection in Figure E3), which supports keeping MultiWOZ descriptive.")
    D.table("Behavioral Profiles of the Three Primary Archetypes (Golden Partition)",
            ["Feature", *ARCH],
            [["<i>n</i> (%)", *[f"{int(r.n)} ({n2(r.pct, 1)})" for r in pr.itertuples()]],
             ["Turns, <i>M</i> (<i>SD</i>)", *[f"{n2(r.turns_M)} ({n2(r.turns_SD)})" for r in pr.itertuples()]],
             ["Words per user utterance", *[n2(r.user_words) for r in pr.itertuples()]],
             ["Words per agent utterance", *[n2(r.agent_words) for r in pr.itertuples()]],
             ["Slot-value revisions", *[n2(r.revisions) for r in pr.itertuples()]],
             ["Hesitation markers", *[n2(r.hesitations) for r in pr.itertuples()]],
             ["Agent offers", *[n2(r.offers) for r in pr.itertuples()]],
             ["Budget stated (%)", *[n2(r.budget_pct, 1) for r in pr.itertuples()]],
             ["Task success (%)", *[n2(r.success_pct, 1) for r in pr.itertuples()]]],
            note="Values are means per dialogue unless stated. Revisions count changes of a slot's value across "
                 "user and agent acts.",
            widths=[2.2, 1.43, 1.43, 1.44], align=["l", "c", "c", "c"])
    D.para(
        "<i>Interim answer.</i> The algorithms differ significantly with a large effect. HDBSCAN separates best but "
        "only with relaxed settings, heavy noise, and an unstable number of clusters, whereas K-Means gives a stable "
        "three-archetype solution that generalizes to held-out Frames dialogues but not to MultiWOZ. The "
        "pre-specified answer to RQ1 is the three primary archetypes, which were used in RQ2.")

    # ------------------------------------------------------------------ RQ1 sensitivity
    D.heading("RQ1 Sensitivity Analysis: Refined Archetypes (Complete)", 2)
    D.para(
        "Three diagnostics showed that the primary archetypes are a weak basis for routing: a router predicting the "
        f"archetype from the first five turns reached only κ = {nz(kap_prim)} on held-out dialogues, the "
        "trajectory vectors mix user and agent behavior, and the archetypes are partly tied to role-players. With "
        "Gemini embeddings, the 159-run algorithm comparison reproduced the primary result with larger effects "
        f"(η<sup>2</sup> = {nz(r1gm['G-pooled']['anova']['eta2'])} for turn vectors and "
        f"{nz(r1gm['G-doc']['anova']['eta2'])} for document vectors, both <i>p</i> < .001; Table D3), so the answer to "
        "RQ1 does not depend on the embedding model. Restricting MiniLM vectors to user turns raised three-cluster "
        f"stability from ARI = {nz(rep_m.loc[('R0', 3), 'stability_ari'])} to "
        f"{nz(rep_m.loc[('R1', 3), 'stability_ari'])} and lowered the role-player association from <i>V</i> = "
        f"{nz(rep_m.loc[('R0', 3), 'roleplayer_v'])} to {nz(rep_m.loc[('R1', 3), 'roleplayer_v'])}.")
    D.para(
        "On whole conversations the hybrid representation was unstable (best eligible solution <i>k</i> = "
        f"{int(wk.k)}, ARI = {nz(wk.stability_ari)}) and largely reproduced how the dialogue ended (three-cluster "
        f"association with the rated outcome <i>V</i> = {nz(tr3.loc['whole', 'outcome_v'])}), because late messages "
        "record the result of the search rather than the user's approach. Table 11 shows that truncating to the first "
        "<i>M</i> user messages solved this: three-cluster solutions were stable at every cut-off (ARI = "
        f"{nz(tr3.drop(index='whole').stability_ari.min())} to {nz(tr3.drop(index='whole').stability_ari.max())}), no "
        f"solution with four or more clusters exceeded ARI = {nz(tr_hi.max())}, and the outcome association rose with "
        f"more messages (<i>V</i> = {nz(tr3.loc['3', 'outcome_v'])} at three to {nz(tr3.loc['9', 'outcome_v'])} at "
        "nine; all panels in Figure E4). The pre-declared rule selected the first "
        f"{({'3': 'three', '5': 'five', '7': 'seven', '9': 'nine'}).get(win['M'], win['M'])} user messages with "
        f"<i>k</i> = {win['k']} (ARI = {nz(win['stability_ari'])}; {pct(win['core_pct'], 0)} core members that keep "
        f"their archetype in at least 90% of 30 refits; smallest archetype {pct(win['min_cluster_pct'], 0)}).")
    D.table("Stability, Routing, and Outcome Association of Hybrid Archetypes by Conversation Length",
            ["User messages used", "Dialogues shortened (%)", "Stability ARI", "Core members (%)",
             "Smallest cluster (%)", "Routing κ", "Outcome <i>V</i>", "Best ARI, <i>k</i> ≥ 4"],
            [[("Whole conversation" if m == "whole" else m),
              n2(r1t["annotations"]["None" if m == "whole" else m]["truncated_pct"], 1),
              nz(r.stability_ari), n2(r.core_pct, 1), n2(r.min_cluster_pct, 1), nz(r.kappa_N5), nz(r.outcome_v),
              nz(tr_hi.loc[m])] for m, r in tr3.iterrows()],
            note=f"Values are for <i>k</i> = 3 on the golden partition (<i>N</i> = {s1['n_gold']}) unless stated. "
                 "Stability is the mean ARI between K-Means fits on 50 pairs of random 80% subsamples; core members "
                 "keep their archetype in at least 90% of 30 refits. Routing κ compares the archetype of held-out "
                 "dialogues with a logistic-regression prediction from their first five turns. Outcome <i>V</i> is "
                 "Cramér's <i>V</i> with the LLM-rated outcome of the whole conversation. The adopted solution uses "
                 "nine messages. ARI = adjusted Rand index.",
            widths=[1.15, 0.85, 0.75, 0.8, 0.8, 0.7, 0.7, 0.75], align=["l"] + ["c"] * 7)
    rp = rprof.reindex(ARCH2)
    db_, oe_, rc_ = (rp.loc[a] for a in ARCH2)
    D.para(
        "Table 12 profiles the refined archetypes; names follow a fixed rule (highest destination flexibility = Open "
        "Explorer; more decisive of the other two = Decisive Booker). Decisive Bookers "
        f"({pct(db_.pct)}) are polite and decisive, pursue one specific trip ({pct(db_.goal_booking_pct, 0)}), and "
        f"book in {pct(db_.booked_pct, 0)} of dialogues. Open Explorers ({pct(oe_.pct)}) are flexible about the "
        f"destination, consider many alternatives, revise often, and have the longest dialogues "
        f"({n2(oe_.turns_M, 1)} turns). Rigid-Constraint Seekers ({pct(rc_.pct)}) have a fixed destination and dates "
        f"and ask few questions; their dialogues are short ({n2(rc_.turns_M, 1)} turns) and end without a suitable "
        f"option in {pct(rc_.no_option_pct, 0)} of cases. Frames task success does not distinguish them (Cramér's "
        f"<i>V</i> = {nz(r1r['cramers_v_task_success'])}).")
    D.table("Profiles of the Three Refined Archetypes (Golden Partition)",
            ["Feature", *ARCH2],
            [["<i>n</i> (%)", *[f"{int(r.n)} ({n2(r.pct, 1)})" for _, r in rp.iterrows()]],
             ["Turns, <i>M</i> (<i>SD</i>)", *[f"{n2(r.turns_M)} ({n2(r.turns_SD)})" for _, r in rp.iterrows()]],
             ["User messages, <i>M</i>", *[n2(r.user_turns_M) for _, r in rp.iterrows()]]]
            + [[f"{lab_} (1–5)", *[n2(r[c]) for _, r in rp.iterrows()]] for lab_, c in feat]
            + [["Goal: explore destinations (%)", *[n2(r.goal_explore_pct, 1) for _, r in rp.iterrows()]],
               ["Goal: book a specific trip (%)", *[n2(r.goal_booking_pct, 1) for _, r in rp.iterrows()]],
               ["Outcome: booked (%)", *[n2(r.booked_pct, 1) for _, r in rp.iterrows()]],
               ["Outcome: no suitable option (%)", *[n2(r.no_option_pct, 1) for _, r in rp.iterrows()]],
               ["Frames task success (%)", *[n2(r.success_pct, 1) for _, r in rp.iterrows()]]],
            note="Ratings and goals are LLM annotations of the first nine user messages (the clustering input); "
                 "outcomes are LLM annotations of the whole conversation and were not used for clustering.",
            widths=[2.3, 1.4, 1.4, 1.4], align=["l", "c", "c", "c"])
    D.para(
        f"The refined and primary archetypes overlap only partly (ARI = {nz(r1r['ari_vs_primary'])}). On held-out "
        "dialogues the refined archetypes reproduced the golden proportions, "
        f"χ<sup>2</sup>({r1r['chi_gold_test']['df']}, <i>N</i> = {r1r['chi_gold_test']['N']}) = "
        f"{n2(r1r['chi_gold_test']['chi2'])}, <i>p</i> {pv(r1r['chi_gold_test']['p'])}, and routing after five turns "
        f"improved from κ = {nz(kap_prim)} to {nz(win['kappa_N5'])}, which is still only fair. An ablation (Table E7) "
        "showed that truncation is the main driver of the gain: with the behavior profile, stability rose from ARI = "
        f"{nz(aw.loc[[1, 2, 3]].stability_ari.min())} to {nz(aw.loc[[1, 2, 3]].stability_ari.max())} on whole "
        f"conversations to {nz(a9.loc[[1, 2, 3]].stability_ari.min())} to {nz(a9.loc[[1, 2, 3]].stability_ari.max())} "
        "on nine messages; alternative representations agree only partly with the adopted labels (ARI = "
        f"{nz(a9.drop(index=1).ari_vs_adopted.min())} to {nz(a9.drop(index=1).ari_vs_adopted.max())}).")
    D.para(
        "<i>Decision.</i> The primary archetypes remain the pre-specified answer to RQ1 and were used in RQ2. RQ3 and "
        "RQ4 use the refined archetypes because they are more stable, describe the user rather than the whole "
        "dialogue, and are recognized earlier; RQ2 will be repeated with them. They remain regions of a continuum "
        f"(Silhouette only {nz(win['calibrated_silhouette'], 3)} above its permutation baseline) and partly capture "
        f"whether a suitable package was available (outcome <i>V</i> = {nz(win['outcome_v'])}).")

    # ------------------------------------------------------------------ RQ2
    D.heading("RQ2: Cluster-Adaptive Few-Shot Prompting (Complete)", 2)
    D.para(
        "The pilot ran every step except the LLM call on the experimental sample (Tables E8 and E9; Figure E5). "
        f"Routing from a three-turn prefix was correct for {n_route} of {r2p['N']} dialogues "
        f"({pct(100 * r2p['routing_accuracy'])}), close to the 33.3% expected by chance. Exemplar relevance differed by "
        f"strategy, <i>F</i>({n2(rm['df1_gg'])}, {n2(rm['df2_gg'])}) = {n2(rm['F'])}, <i>p</i> {pv(rm['p_gg'])}, "
        f"partial η<sup>2</sup> = {nz(rm['eta2_partial'])}: both similarity-based strategies retrieved far more "
        "relevant exemplars than the static set, and global retrieval was slightly more relevant than "
        "cluster-adaptive retrieval. The style metric was valid but modest: human replies were closer to their own "
        f"archetype's centroid than to the others, <i>t</i>({r2p['N'] - 1}) = {n2(r2p['style_metric_t']['t'])}, "
        f"<i>p</i> {pv(r2p['style_metric_t']['p'])}, <i>d</i><sub><i>z</i></sub> = {nz(r2p['style_metric_dz'])}.")
    D.para(
        "Table 13 shows the experimental results. Style convergence did not differ by condition, "
        f"<i>F</i>({n2(sc_a['df1_gg'])}, {n2(sc_a['df2_gg'])}) = {n2(sc_a['F'])}, <i>p</i> {pv(sc_a['p_gg'])}, "
        f"partial η<sup>2</sup> = {nz(sc_a['eta2_partial'])}, and the Friedman test agreed, χ<sup>2</sup>(2, "
        f"<i>N</i> = {r2x['N']}) = {n2(sc_r['friedman']['chi2'])}, <i>p</i> {pv(sc_r['friedman']['p'])}. Zero-shot "
        f"responses were descriptively closest to the target centroid (<i>M</i> = {nz(sc_d['Zero-Shot'][0], 3)}), the "
        "opposite of the hypothesized order, no Holm-adjusted contrast was significant (Table E10; Figure E6), and "
        "similarity to the human reply did not differ either. The null hypothesis for RQ2 is not rejected.")
    D.para(
        "The exploratory length measure showed a large effect: zero-shot responses averaged "
        f"{n2(wd_d['Zero-Shot'][0], 1)} words, whereas static and cluster-adaptive responses averaged "
        f"{n2(wd_d['Static Few-Shot'][0], 1)} and {n2(wd_d['Cluster-Adaptive Few-Shot'][0], 1)} words, close to the "
        f"human replies (<i>M</i> = {n2(r2x['gold_words']['M'], 1)}), partial η<sup>2</sup> = "
        f"{nz(wd_a['eta2_partial'])}; the two few-shot conditions did not differ from each other (Holm <i>p</i> "
        f"{pv(wd_pairs['Cluster-Adaptive Few-Shot vs. Static Few-Shot']['p_holm'])}).")
    rows = []
    lab = {"style_cos": "Style convergence (cosine)", "gold_cos": "Similarity to human reply (cosine)",
           "words": "Response length (words)"}
    for dv in ["style_cos", "gold_cos", "words"]:
        r_ = r2x["results"][dv]
        a_ = r_["anova"]
        fmt = (lambda m, s_: f"{n2(m, 1)} ({n2(s_, 1)})") if dv == "words" else \
              (lambda m, s_: f"{nz(m, 3)} ({nz(s_, 3)})")
        rows.append([lab[dv]] + [fmt(*r_["desc"][c]) for c in CONDS] +
                    [f"{n2(a_['F'])}", "< .001" if a_["p_gg"] < .001 else nz(a_["p_gg"], 3), nz(a_["eta2_partial"])])
    D.table("Generated Responses by Prompting Condition",
            ["Outcome", "Zero-shot <i>M</i> (<i>SD</i>)", "Static few-shot <i>M</i> (<i>SD</i>)",
             "Cluster-adaptive <i>M</i> (<i>SD</i>)", "<i>F</i>", "<i>p</i>", "η<sub><i>p</i></sub><sup>2</sup>"],
            rows,
            note=f"<i>N</i> = {r2x['N']} held-out dialogues, each measured under all three conditions; "
                 f"{r2x['model']}. <i>p</i> values use the Greenhouse–Geisser correction. Response length is "
                 "exploratory.",
            widths=[1.75, 1.0, 1.0, 1.0, 0.55, 0.55, 0.65], align=["l", "c", "c", "c", "c", "c", "c"])
    D.para(
        "<i>Interim answer.</i> Any human examples move the model toward human pacing, but archetype-matched examples "
        "add nothing measurable beyond fixed examples. Two likely reasons are near-chance routing, so most dialogues "
        "received exemplars from the wrong archetype, and weak archetype separation with a modest style metric; the "
        f"observed effect (<i>f</i> = {n2(f_rq2)}) is below the medium effect assumed in the power analysis.")

    # ------------------------------------------------------------------ RQ3 and RQ4
    D.heading("RQ3: Rules Versus Prompting (Groundwork Complete)", 2)
    pax, bud = audit.loc["RULE_PAX_CAPACITY"], audit.loc["RULE_BUDGET_MINIMUM"]
    D.para(
        f"The rule engine passed all {r34['rule_tests_passed']} boundary tests. The corpus audit (Table E11) shows "
        f"that only two rules can be checked from Frames annotations: a user-stated number of adults appears in "
        f"{pct(pax.slot_observed_pct)} of dialogues and triggers the capacity rule in {int(pax.trigger_n)}, and a "
        f"numeric budget appears in {pct(bud.slot_observed_pct)} and triggers the minimum-budget rule in "
        f"{int(bud.trigger_n)}. The visa, passport, and discount rules can never be triggered by public data, which "
        "is the empirical basis for injecting synthetic scenarios. RQ3 is not yet answered.")
    D.heading("RQ4: Turn Economy Across Archetypes (Groundwork Complete)", 2)
    b = base4r.reindex(ARCH2)
    D.para(
        f"Table 14 gives the human baseline for all {n2(r4r['n'], 0)} Frames dialogues by refined archetype. Turn "
        f"counts differed by archetype, <i>H</i>(2) = {n2(r4r['kruskal_turns']['H'])}, <i>p</i> "
        f"{pv(r4r['kruskal_turns']['p'])}, as expected by construction (distributions in Figure E7). Redundant "
        f"elicitation was rare among human agents (<i>M</i> = {nz(r4r['overall_rer_M'], 3)}, about one request in "
        f"{int(round(1 / r4r['overall_rer_M']))} agent turns) and did not differ by archetype, <i>H</i>(2) = "
        f"{n2(r4r['kruskal_rer']['H'])}, <i>p</i> {pv(r4r['kruskal_rer']['p'])}. The synopsis expectation of "
        "reducing RER from .16 is therefore not supported; RER will instead be compared between the two LLM agents.")
    D.table("Human Baseline of Turn Economy by Refined Archetype (Frames)",
            ["Archetype", "<i>n</i>", "Turns <i>M</i> (<i>SD</i>)", "RER <i>M</i> (<i>SD</i>)",
             "Agent request turns <i>M</i>"],
            [[a, str(int(r.n)), f"{n2(r.turns_M)} ({n2(r.turns_SD)})", f"{nz(r.rer_M, 3)} ({nz(r.rer_SD, 3)})",
              n2(r.req_turns_M)] for a, r in b.iterrows()],
            note="RER = redundant elicitation rate. Archetypes for held-out dialogues were assigned with the K-Means "
                 "model fitted on the golden partition.",
            widths=[1.9, 0.6, 1.3, 1.3, 1.4], align=["l", "c", "c", "c", "c"])

    # ================================================================== LIMITATIONS AND RISKS
    D.heading("Interim Limitations and Risks", 1)
    D.para(
        "Archetypes are weakly separated (primary Silhouette < .25; refined only "
        f"{nz(win['calibrated_silhouette'], 3)} above the permutation baseline) and routing after five turns reaches "
        f"only κ = {nz(win['kappa_N5'])}, so routing errors dilute any effect of archetype-matched prompting. The "
        f"primary archetypes are associated with role-players (<i>V</i> = {nz(cramer_v)}) and the refined ones with "
        f"the final outcome (<i>V</i> = {nz(win['outcome_v'])}), and other reasonable representations give partly "
        "different archetypes. The behavior ratings come from an LLM and were validated on whole "
        "conversations, RQ3 scenarios are synthetic, and RQ4 relies on a simulated user. Frames is role-play with "
        "fictional cities, so conclusions apply to vacation-package negotiation dialogues of this kind. The archetype "
        "definition was refined after the primary analysis (mitigated by a pre-declared rule and by reporting every "
        f"configuration), and the observed RQ2 effect (<i>f</i> = {nz(f_rq2)}) was smaller than the medium effect "
        "assumed for power.")
    D.para(
        "Project risks are API quota limits (mitigated by caching every response), weak routing (refined archetypes "
        "and a global nearest-neighbor condition), an unrealistic simulator (persona check), and schedule slippage "
        "(analysis ends in Week 8, leaving Weeks 9 and 10 as buffer).")

    # ================================================================== NEXT STEPS
    D.heading("Next Steps", 1)
    D.items([
        "Week 6: repeat RQ2 with the refined archetypes and global retrieval; prepare RQ3 scenarios.",
        "Week 7: run the RQ3 experiment (slot F1, exemplar leakage, rule adherence).",
        "Week 8: RQ4 simulation, persona and annotation-reliability checks, BERTScore, and robustness checks.",
        "Weeks 9 and 10: final presentation, final report, and repository release (Appendix B)."],
        numbered=False)

    # ================================================================== REFERENCES
    D.heading("References", 1, new_page=True)
    for ref in REFERENCES:
        D.reference(ref)

    # ================================================================== APPENDICES
    D.heading("Appendix A", 1, new_page=True)
    D.heading("Repository Structure and Replication Guide", 1, toc=False)
    D.para(f"All materials are available at {REPO}. Table A1 lists the parts of the repository used in this report, "
           "and Table A2 lists the commands that reproduce every table and figure.")
    D.table("Repository Structure",
            ["Path", "Contents"],
            [["data/raw/", "Downloaded Frames and MultiWOZ 2.2 corpora"],
             ["data/canonical/", "Canonical two-tier dialogue file"],
             ["data/interim/", "Cleaned samples, embeddings, archetypes, LLM annotations, prompts, and run summaries"],
             ["data/embeddings/gemini/", "Cached Gemini embeddings (regenerated by step 2c; not versioned)"],
             ["src/ingestion.py, src/canonical_schema.py", "Corpus parsers and Pydantic schema"],
             ["src/rule_engine.py, rules/", "Declarative rule engine and YAML rule file"],
             ["src/interim_pipeline/", "Reproducible analysis steps 0 to 4, including steps 2b to 2i (this report)"],
             ["src/report/, src/build_interim_submission.py", "APA report builder"],
             ["outputs/interim/tables/, outputs/interim/figures/", "Result tables (CSV) and figures (PNG)"],
             ["requirements.txt", "Python dependencies"]],
            widths=[3.0, 3.5], align=["l", "l"], label="A1")
    D.table("Replication Commands",
            ["Step", "Command (run from src/interim_pipeline/)", "Produces"],
            [["0", "python step0_sample_size.py", "Table 6"],
             ["1", "python step1_prepare_data.py", "Tables 4, 5, and E3; Figures 1 and 2"],
             ["2", "python step2_rq1_clustering.py", "Tables 9, 10, and E4 to E6; Figures E1 to E3"],
             ["2b", "python step2b_rq1_representation.py --emb minilm", "User-turn and dialogue-act representations"],
             ["2c", "python step2c_gemini_embeddings.py", "Gemini embeddings (requires GEMINI_API_KEY)"],
             ["2d", "python step2d_rq1_gemini_algorithms.py", "Table D3"],
             ["2e", "python step2e_llm_user_annotation.py (also --retest and --max-user-msgs 3, 5, 7, 9)",
              "LLM behavior annotations (requires GEMINI_API_KEY)"],
             ["2f", "python step2f_rq1_llm_hybrid.py", "Table D2; whole-conversation hybrid"],
             ["2g", "python step2g_rq1_truncation.py", "Table 11; Figure E4; refined labels"],
             ["2h", "python step2h_rq1_ablation.py", "Table E7"],
             ["2i", "python step2i_rq1_refined_archetypes.py", "Tables 12 and 14; Figure E7"],
             ["3", "python step3_rq2_pipeline.py", "Tables E8 and E9; Figure E5; saved prompts"],
             ["3 (execution)", "python step3_rq2_pipeline.py --execute", "Tables 13 and E10; Figure E6 (requires GEMINI_API_KEY)"],
             ["4", "python step4_rq3_rq4_groundwork.py", "Tables 7 and E11"],
             ["Report", "python src/build_interim_submission.py (from the repository root)", "This document"]],
            note="Python 3.11; all random steps use seed 42. LLM and embedding responses are cached, so steps 2c and "
                 "2e only call the API for missing items.",
            widths=[1.0, 3.4, 2.1], align=["l", "l", "l"], label="A2")

    D.heading("Appendix B", 1, new_page=True)
    D.heading("Ten-Week Project Schedule", 1, toc=False)
    D.para("Table B1 maps the project to the 10-week QM640 schedule. All analysis finishes in Week 8, and Weeks 9 and "
           "10 are reserved for the presentation and final report.")
    D.table("Ten-Week Schedule Aligned With the QM640 Course Topics",
            ["Week (dates)", "Course topic", "Project tasks and deliverables", "Status"],
            [["1 (Sep 27–Oct 3)", "Define research problem and topic", "Problem statement finalized; repository set "
              "up; Frames and MultiWOZ downloaded", "Complete"],
             ["2 (Oct 4–10)", "Synopsis draft", "Research questions and two-tier schema; synopsis draft (Oct 6)",
              "Complete"],
             ["3 (Oct 11–17)", "Literature search and data collection", "Synopsis final (Oct 13); ingestion, "
              "canonicalization, and embeddings", "Complete"],
             ["4 (Oct 18–24)", "Objectives and hypotheses", "Quality audit, EDA, power analysis, RQ1 clustering; "
              "RQ2 pilot; RQ3 and RQ4 groundwork; interim draft (Oct 20)", "Complete"],
             ["5 (Oct 25–31)", "Research design and methodology", "Interim report final (Oct 27); RQ2 generation "
              "run and analysis (complete); RQ1 sensitivity analysis of the archetype definition (complete)",
              "In progress"],
             ["6 (Nov 1–7)", "Data analysis plan", "RQ2 repeated with refined archetypes and global k-NN; RQ3 "
              "scenario injection; final report draft (Nov 3)",
              "Planned"],
             ["7 (Nov 8–14)", "Data analysis plan execution", "RQ3 2 × 2 experiment and analysis", "Planned"],
             ["8 (Nov 15–21)", "Data analysis assessment", "RQ4 simulation, 2 × 3 analysis, robustness checks; "
              "analysis complete", "Planned"],
             ["9 (Nov 22–28)", "Refinement and documentation", "Final presentation (Nov 27–28)", "Planned"],
             ["10 (Nov 29–Dec 5)", "Document results and findings", "Final report and repository release",
              "Planned"]],
            note="EDA = exploratory data analysis. No tasks are scheduled outside Weeks 1 to 10.",
            widths=[1.25, 1.55, 2.8, 0.9], align=["l", "l", "l", "l"], label="B1")

    D.heading("Appendix C", 1, new_page=True)
    D.heading("Comparison With Related Research", 1, toc=False)
    D.para("Table C1 compares the studies closest to this capstone and shows how the present design extends them.")
    D.table("Related Research and Its Relationship to the Present Study",
            ["Study", "Main contribution", "Connection to this study", "Gap addressed here"],
            [["El Asri et al. (2017), Frames", "1,369 human–human vacation-package dialogues with frame tracking",
              "Primary corpus for embeddings, archetypes, and exemplars", "Does not cluster dialogues or use them "
              "for prompting"],
             ["Zang et al. (2020), MultiWOZ 2.2", "Corrected multi-domain dialogue states and schema",
              "External projection check and schema mapping", "Focuses on slot tracking, not archetypes or prompting"],
             ["Liu et al. (2022), KATE", "Similarity-based in-context example selection beats random selection",
              "Motivates retrieval; global nearest neighbor is a comparison", "Single-turn tasks; no style or "
              "leakage measures"],
             ["Rebedea et al. (2023), NeMo Guardrails", "Programmable rails outside the LLM", "Motivates the "
              "decoupled rule engine", "Does not adapt style or test interaction with prompting"],
             ["Yao et al. (2024), τ-bench", "Agent evaluation against explicit domain policies", "Supports measuring "
              "rule adherence separately", "Tool-calling agents; no archetype adaptation"],
             ["Acikgoz et al. (2025), TD-EVAL", "Turn-level and dialogue-level evaluation", "Supports combining "
              "similarity with turn-level checks", "Evaluation framework only; no adaptive prompting"]],
            note="The comparison describes relevance to this study and does not imply that the cited studies used "
                 "the same data or metrics.",
            widths=[1.45, 1.75, 1.65, 1.65], align=["l", "l", "l", "l"], label="C1")

    D.heading("Appendix D", 1, new_page=True)
    D.heading("Behavior Annotation Codebook and Quality Checks", 1, toc=False)
    D.para("Table D1 gives the codebook used by the LLM to rate each Frames user in the RQ1 sensitivity analysis. "
           "The model read the conversation (whole or truncated after the <i>M</i>-th user message) and rated only "
           "the user, using the agent's messages as context. Table D2 reports the reliability and criterion "
           "validity of the ratings, and Table D3 repeats the RQ1 algorithm comparison with Gemini embeddings.")
    D.table("LLM Behavior Annotation Codebook",
            ["Field", "Type", "Definition and scale anchors"],
            [["Primary goal", "Category", "Main purpose: explore destinations, price shopping, book a specific trip, "
              "compare options, information only, or other"],
             ["Secondary goals", "Categories", "Other purposes clearly present (same categories; may be empty)"],
             ["Price sensitivity", "1–5", "1 = price never matters; 5 = price dominates every decision"],
             ["Destination flexibility", "1–5", "1 = one fixed destination; 5 = open to anywhere"],
             ["Date flexibility", "1–5", "1 = fixed dates; 5 = fully flexible dates"],
             ["Exploration breadth", "1–5", "1 = considers a single option; 5 = considers many alternatives"],
             ["Decisiveness", "1–5", "1 = hesitant, cannot decide; 5 = decides quickly and firmly"],
             ["Detail orientation", "1–5", "1 = no interest in specifics; 5 = asks about many details"],
             ["Information up front", "1–5", "1 = reveals requirements bit by bit; 5 = states all requirements in "
              "the first message"],
             ["Revision tendency", "1–5", "1 = never changes requirements; 5 = changes them repeatedly"],
             ["Question asking", "1–5", "1 = asks no questions; 5 = asks many questions"],
             ["Politeness", "1–5", "1 = curt or rude; 5 = very polite"],
             ["Emotional tone", "Category", "Positive, neutral, impatient, or frustrated"],
             ["Outcome", "Category", "Booked, no suitable option, undecided or left, or unclear (not used for "
              "clustering)"],
             ["Party type", "Category", "Solo, couple, family, group, business, or unknown (not used for "
              "clustering)"],
             ["Unusual conversation", "Yes/no", "Off-task, nonsensical, or unlike a normal travel request"]],
            note="Gemini 2.5 Flash, temperature 0, internal reasoning disabled, output constrained to a JSON schema "
                 "with these fields. The instruction asked the model to base every rating on evidence in the user's "
                 "messages and to use 3 for moderate or mixed behavior.",
            widths=[1.6, 0.9, 4.0], align=["l", "l", "l"], label="D1")
    crit = {"revision_tendency": [("user_revisions", "Slot-value changes in user acts")],
            "question_asking": [("request_rate", "Request acts per user turn")],
            "exploration_breadth": [("switch_rate", "Frame switches per user turn"),
                                    ("compare_rate", "Comparison requests per user turn")],
            "information_upfront": [("front_loading", "Share of slots stated in the first user turn")],
            "price_sensitivity": [("budget_stated", "Budget stated")],
            "detail_orientation": [("preference_keys", "Distinct preference slots mentioned")]}
    rows = []
    for lab_, c in feat:
        cs = crit.get(c, [(None, "—")])
        for j, (key, desc_) in enumerate(cs):
            rho = cv_.get(f"{c}~{key}", {}).get("rho") if key else None
            rows.append([lab_ if j == 0 else "", nz(r1h["reliability"][c]) if j == 0 else "", desc_,
                         nz(rho) if rho is not None else "—"])
    for c, lab_ in [("primary_goal", "Primary goal"), ("emotional_tone", "Emotional tone"), ("outcome", "Outcome"),
                    ("party_type", "Party type")]:
        rows.append([lab_, nz(r1h["reliability"][c]), "—", "—"])
    D.table("Reliability and Criterion Validity of the LLM Behavior Ratings",
            ["Field", "Re-annotation κ", "Behavior counted from Frames acts", "Spearman ρ"],
            rows,
            note=f"Re-annotation: <i>n</i> = {r1h['reliability']['n']} random dialogues annotated a second time at "
                 "temperature 0.7; quadratic-weighted κ for ratings and Cohen's κ for categories. Criterion "
                 f"validity: <i>N</i> = {n2(r1h['n_dialogues'], 0)} dialogues; all ρ <i>p</i> < .001. Both checks use "
                 "whole-conversation annotations.",
            widths=[1.7, 1.0, 2.8, 1.0], align=["l", "c", "l", "c"], label="D2")
    rows = []
    for key, lab_ in [("G-pooled", "Decay-weighted turn vectors"), ("G-doc", "Whole-dialogue document vectors")]:
        g_ = r1gm[key]
        for j, a in enumerate(["K-Means", "Agglomerative", "HDBSCAN"]):
            rows.append([lab_ if j == 0 else "", a, f"{nz(g_['desc'][a]['M'], 3)} ({nz(g_['desc'][a]['SD'], 3)})",
                         f"<i>F</i>(2, 156) = {n2(g_['anova']['F'])}" if j == 0 else "",
                         nz(g_["anova"]["eta2"]) if j == 0 else ""])
        rows.append(["", "Permutation baseline", f"{nz(g_['permutation_M'], 3)} ({nz(g_['permutation_SD'], 3)})",
                     "", ""])
    D.page_break()
    D.table("Algorithm Comparison Repeated With Gemini Embeddings",
            ["Representation", "Algorithm", "Silhouette <i>M</i> (<i>SD</i>)", "ANOVA", "η<sup>2</sup>"],
            rows,
            note=f"Each algorithm was run on {int(ss.loc['RQ1', 'per_group'])} random subsamples of 500 golden "
                 "dialogues, as in Table 9, using gemini-embedding-001 vectors (3,072 dimensions). All "
                 "ANOVAs <i>p</i> < .001; Welch and Kruskal–Wallis tests agreed.",
            widths=[1.9, 1.4, 1.2, 1.4, 0.6], align=["l", "l", "c", "c", "c"], label="D3")

    # ================================================================== APPENDIX E (supplementary results)
    D.heading("Appendix E", 1, new_page=True)
    D.heading("Supplementary Tables and Figures", 1, toc=False)
    D.para("This appendix holds second-level material that supports the conclusions stated in the body. Each table "
           "and figure is summarized where it is cited in the body.")
    D.heading("Data Description", 2, toc=False)
    D.table("Data Dictionary, Raw Source Fields Used",
            ["Corpus", "Field", "Type", "Description", "Use"],
            [["Frames", "id", "String", "Unique dialogue identifier", "Key"],
             ["Frames", "user_id, wizard_id", "String", f"Role-player identifiers ({n_users} users, {n_wizards} wizards)",
              "Confound check"],
             ["Frames", "turns[].author", "Category", "user or wizard", "Speaker tag"],
             ["Frames", "turns[].text", "String", "Utterance text", "Embedding"],
             ["Frames", "turns[].timestamp", "Float", "Collection time (Unix ms)", "Not used"],
             ["Frames", "turns[].labels.acts[].name", "Category", "Dialogue act (e.g., inform, request, offer, "
              "switch_frame)", "Features, RER"],
             ["Frames", "turns[].labels.acts[].args[].key/val", "String", "Slot name and value (e.g., dst_city, "
              "budget)", "Tier 1 slots"],
             ["Frames", "labels.wizardSurveyTaskSuccessful", "Boolean", "Wizard-reported task success", "Stratify, "
              "pool"],
             ["Frames", "labels.userSurveyRating", "Float", "User satisfaction rating (1–5)", "Descriptive"],
             ["MultiWOZ", "dialogue_id", "String", "Unique dialogue identifier", "Key"],
             ["MultiWOZ", "services", "List", "Services involved (hotel, train, taxi, ...)", "Inclusion"],
             ["MultiWOZ", "turns[].speaker", "Category", "USER or SYSTEM", "Speaker tag"],
             ["MultiWOZ", "turns[].utterance", "String", "Utterance text", "Embedding"],
             ["MultiWOZ", "turns[].frames[].state.slot_values", "Map", "Cumulative dialogue state per service",
              "Tier 1 slots"]],
            note="RER = redundant elicitation rate. Only the fields listed were read; all other fields were ignored.",
            widths=[0.8, 2.0, 0.7, 2.0, 1.0], align=["l", "l", "l", "l", "l"], label="E1")
    D.table("Data Dictionary, Canonical Schema Fields",
            ["Field", "Type", "Description"],
            [["dialogue_id, source_dataset", "String", "Identifier and corpus of origin (frames or multiwoz)"],
             ["total_turns, user_turns, wizard_turns", "Integer", "Turn counts"],
             ["turns[].turn_id, speaker, utterance", "Mixed", "Ordered turns with corpus-neutral speaker and text"],
             ["turns[].acts, slots_mentioned, revisions", "List, map", "Acts, slots informed, and slots whose value "
              "changed in the turn"],
             ["Tier 1: origin_city, destination_city", "String", "Trip endpoints"],
             ["Tier 1: departure_date, return_date, duration_nights", "String, integer", "Trip timing"],
             ["Tier 1: traveler_count_adults, traveler_count_children", "Integer", "Party size"],
             ["Tier 1: budget_amount, accommodation_tier", "Float, string", "Budget ceiling and hotel tier"],
             ["Tier 2: visa_processing_window_days, passport_expiry_months", "Integer", "Policy timing (synthetic in "
              "RQ3)"],
             ["Tier 2: package_type, sharing_basis, discount_applied_percentage", "String, float", "Package, room, "
              "and discount (synthetic in RQ3)"],
             ["revisions_count", "Integer", "Number of slot-value changes across the dialogue"],
             ["hesitation_markers_count", "Integer", "User hesitation phrases (e.g., \"maybe,\" \"not sure\")"],
             ["budget_specified", "Boolean", "Whether a numeric budget was stated"]],
            note="Schema implemented as Pydantic models in src/canonical_schema.py.",
            widths=[2.9, 1.0, 2.6], align=["l", "l", "l"], label="E2")
    D.table("Observed Slot Completeness by Corpus",
            ["Slot", "Tier", "Frames (%)", "MultiWOZ 2.2 (%)"],
            [[s.replace("_", " "), t, n2(f, 1), n2(m, 1)] for s, t, f, m in comp.itertuples(index=False)],
            note="Percentage of dialogues in which the slot is mentioned at least once in the dialogue-act (Frames) "
                 "or dialogue-state (MultiWOZ) annotations. MultiWOZ budget is the categorical price range. "
                 f"Frames <i>N</i> = {n2(fq.n_analytic, 0)}; MultiWOZ <i>N</i> = {n2(mq.n_analytic, 0)}. Figure 2 "
                 "in the body plots these values.",
            widths=[2.6, 1.0, 1.4, 1.5], align=["l", "c", "c", "c"], label="E3")

    D.heading("RQ1: Clustering Diagnostics", 2, toc=False)
    D.table("Choice of the Number of Clusters (K-Means on the Golden Partition)",
            ["<i>k</i>", "Silhouette", "Davies–Bouldin", "Inertia", "Smallest cluster (%)"],
            [[str(int(r.k)), nz(r.silhouette, 3), n2(r.davies_bouldin, 3), n2(r.inertia, 1),
              n2(r.smallest_cluster_pct, 1)] for r in k_sel.itertuples()],
            note=f"<i>N</i> = {s1['n_gold']} golden dialogues; cosine Silhouette.",
            widths=[0.6, 1.3, 1.4, 1.3, 1.6], align=["c"] * 5, label="E4")
    D.figure("Cluster-Number Diagnostics", os.path.join(FIG, "fig_rq1_k_selection.png"),
             note="The dashed line marks the pre-specified <i>k</i> = 3.", width=6.3, label="E1")
    D.figure("Silhouette Coefficients by Algorithm", os.path.join(FIG, "fig_rq1_silhouette.png"),
             note="Each point is one subsample run; triangles mark means. The permutation baseline shows the "
                  "Silhouette expected with no structure.", width=5.8, label="E2")
    rows = []
    for g1, g2 in [("Agglomerative", "K-Means"), ("Agglomerative", "HDBSCAN"), ("K-Means", "HDBSCAN")]:
        d, p_t, lo, hi = tk_row(g1, g2)
        p_g, df_g = gh_p(g1, g2)
        rows.append([f"{g2} − {g1}", nz(d, 3), f"[{nz(lo, 3)}, {nz(hi, 3)}]", ("< .001" if p_t < .001 else nz(p_t, 3)),
                     ("< .001" if p_g < .001 else nz(p_g, 3))])
    D.table("Pairwise Comparisons of Mean Silhouette",
            ["Comparison", "Mean difference", "95% CI (Tukey)", "<i>p</i> (Tukey)", "<i>p</i> (Games–Howell)"],
            rows, note="CI = confidence interval. Games–Howell comparisons do not assume equal variances.",
            widths=[2.0, 1.1, 1.4, 0.9, 1.1], align=["l", "c", "c", "c", "c"], label="E5")
    D.table("Archetype Assignment and Centroid Similarity Across Samples",
            ["Sample", "<i>N</i>", "Centroid similarity <i>M</i> (<i>SD</i>)", *[f"{a} (%)" for a in ARCH]],
            [[s.replace("D_gold", "golden").replace("D_test", "held-out"), n2(r.N, 0),
              f"{nz(r.sim_M, 3)} ({nz(r.sim_SD, 3)})", *[n2(getattr(r, a.replace(' ', '_')), 1) for a in ARCH]]
             for s, r in cross.rename(columns={a: a.replace(" ", "_") for a in ARCH}).set_index("set").iterrows()],
            note="Centroid similarity is the cosine between a dialogue vector and its nearest frozen centroid. "
                 "Centroids were fitted on the golden partition only.",
            widths=[1.5, 0.6, 1.4, 1.0, 1.0, 1.0], align=["l", "c", "c", "c", "c", "c"], label="E6")
    D.figure("Archetypes in the Frames Embedding Space and Projection of MultiWOZ 2.2",
             os.path.join(FIG, "fig_rq1_umap.png"),
             note="Two-dimensional UMAP projection (McInnes et al., 2018) fitted on the golden partition; MultiWOZ "
                  "dialogues were transformed into the same projection without refitting.", width=6.3, label="E3")
    D.figure("Hybrid Archetype Diagnostics by Conversation Length and Number of Clusters",
             os.path.join(FIG, "fig_rq1_truncation_2x2.png"),
             note="Each line is one number of clusters (<i>k</i>). The dotted line in Panel A marks the stability "
                  "threshold of .60. Panel C shows routing κ after five turns; Panel D shows Cramér's <i>V</i> "
                  "between archetype and the rated outcome of the whole conversation.", width=6.3, label="E4")
    D.table("Ablation of the Refined Archetype Definition (Three Clusters)",
            ["Representation", "Stability ARI (whole)", "Stability ARI (9 messages)", "Core members (%)",
             "Outcome <i>V</i>", "Routing κ", "ARI with adopted labels"],
            [[a9.loc[c, "name"].replace("behavioural", "behavior").replace(" (no LLM)", "")
              + (" (adopted)" if c == 1 else ""),
              nz(aw.loc[c, "stability_ari"]), nz(a9.loc[c, "stability_ari"]), n2(a9.loc[c, "core_pct"], 1),
              nz(a9.loc[c, "outcome_v"]), nz(a9.loc[c, "kappa_N5"]),
              "1.00" if c == 1 else nz(a9.loc[c, "ari_vs_adopted"])] for c in a9.index],
            note="Core members, outcome <i>V</i>, routing κ, and agreement with the adopted labels refer to the "
                 "nine-message version. Behavior profile = LLM ratings with goal and tone indicators; dialogue-act "
                 "features are counted from the Frames annotations without an LLM. Bootstrap stability varies by "
                 "about .03 between runs, which explains small differences from Table 11. ARI = adjusted Rand index.",
            widths=[2.0, 0.75, 0.8, 0.75, 0.75, 0.65, 0.8], align=["l"] + ["c"] * 6, label="E7")

    D.heading("RQ2: Pilot and Experimental Details", 2, toc=False)
    D.table("Pilot Exemplar Relevance by Retrieval Strategy",
            ["Strategy", "Cosine to prefix <i>M</i>", "<i>SD</i>", "Exemplars from target archetype (%)"],
            [[s, nz(r.sim_M, 3), nz(r.sim_SD, 3), n2(100 * r.arch_match_M, 1)] for s, r in ret.iterrows()],
            note=f"<i>N</i> = {r2p['N']} held-out dialogue prefixes; three exemplars per prefix. Relevance is the mean "
                 "cosine between the prefix and the retrieval keys of the selected exemplars.",
            widths=[2.4, 1.3, 0.8, 2.0], align=["l", "c", "c", "c"], label="E8")
    rows = []
    for c, p in pairs.items():
        rows.append([c, nz(p["mean_diff"], 3), f"{n2(p['t'])}", str(int(p["df"])),
                     "< .001" if p["p_holm"] < .001 else nz(p["p_holm"], 3), n2(p["d_z"])])
    D.table("Holm-Adjusted Paired Contrasts of Exemplar Relevance",
            ["Contrast", "Mean difference", "<i>t</i>", "<i>df</i>", "<i>p</i> (Holm)",
             "<i>d</i><sub><i>z</i></sub>"],
            rows, note="Positive differences favor the first-named strategy.",
            widths=[2.5, 1.0, 0.8, 0.5, 0.9, 0.8], align=["l", "c", "c", "c", "c", "c"], label="E9")
    D.figure("RQ2 Pilot: Exemplar Relevance and Style-Metric Validity", os.path.join(FIG, "fig_rq2_pilot.png"),
             note="Panel A: lines connect the three strategies for the same prefix. Panel B: cosine similarity of the "
                  "human agent reply to its own versus the other archetype centroids; error bars show 1 <i>SD</i>. "
                  f"The nearest centroid matched the archetype for {pct(100 * r2p['style_argmax_accuracy'])} of "
                  "replies.", width=6.3, label="E5")
    rows = []
    for dv in ["style_cos", "gold_cos", "words"]:
        for p_ in r2x["results"][dv]["pairs"]:
            ph = p_["p_holm"]
            mdiff = nz(p_["mean_diff"], 3) if dv != "words" else n2(p_["mean_diff"], 1)
            rows.append([lab[dv].split(" (")[0], p_["contrast"].replace(" Few-Shot", "").replace("-Shot", "-shot"),
                         mdiff, n2(p_["t"]), str(int(p_["df"])),
                         "< .001" if ph < .001 else ("> .999" if ph > .999 else nz(ph, 3)), n2(p_["d_z"])])
    D.table("Holm-Adjusted Paired Contrasts for the RQ2 Outcomes",
            ["Outcome", "Contrast", "Mean difference", "<i>t</i>", "<i>df</i>", "<i>p</i> (Holm)",
             "<i>d</i><sub><i>z</i></sub>"],
            rows, note="Positive differences favor the first-named condition.",
            widths=[1.5, 2.0, 0.8, 0.6, 0.4, 0.7, 0.5], align=["l", "l", "c", "c", "c", "c", "c"], label="E10")
    D.figure("RQ2 Results: Style Convergence and Response Length by Prompting Condition",
             os.path.join(FIG, "fig_rq2_results.png"),
             note="Lines connect the three conditions for the same dialogue; triangles mark means. The dashed line "
                  "in Panel B is the mean length of the human agent replies.", width=6.3, label="E6")

    D.heading("RQ3 and RQ4: Groundwork Details", 2, toc=False)
    D.table("Corpus Audit of Rule Coverage in Frames",
            ["Rule", "Required slot", "Slot observed (%)", "Dialogues triggering (<i>n</i>)", "Triggering (%)"],
            [[r.replace("RULE_", "").replace("_", " ").lower(), a.required_slot.replace("_", " "),
              n2(a.slot_observed_pct, 1), str(int(a.trigger_n)), n2(a.trigger_pct, 2)] for r, a in audit.iterrows()],
            note=f"<i>N</i> = {n2(r34['frames_n'], 0)} Frames dialogues. Only numeric values stated by the user were "
                 "counted, so the adult and budget percentages are lower than the any-mention rates in Table E3.",
            widths=[1.6, 1.9, 1.0, 1.1, 0.9], align=["l", "l", "c", "c", "c"], label="E11")
    D.figure("Human Baseline of Turn Economy and Redundant Elicitation by Refined Archetype",
             os.path.join(FIG, "fig_rq4_baseline_refined.png"),
             note="Panel A: triangles mark means. Panel B: error bars show 95% confidence intervals.", width=6.3,
             label="E7")
    return D



# ============================================================================= TOC page detection + PDF
def convert_docx_to_pdf(docx_path, pdf_path):
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    script = f'''
    tell application "Microsoft Word"
        open POSIX file "{docx_path}"
        set activeDoc to active document
        save as activeDoc file name "{pdf_path}" file format format PDF
        close activeDoc saving no
    end tell
    '''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Word PDF conversion failed: {res.stderr}")


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_pages(pdf_path, headings):
    import pymupdf
    pages = []
    with pymupdf.open(pdf_path) as doc:
        for pg in doc:
            bold = []
            for blk in pg.get_text("dict")["blocks"]:
                for ln in blk.get("lines", []):
                    spans = [s for s in ln["spans"] if s["text"].strip()]
                    if spans and all(("Bold" in s["font"]) or (s["flags"] & 16) for s in spans):
                        bold.append(_norm("".join(s["text"] for s in spans)))
            cands = set(bold)
            for n in (2, 3):
                cands |= {"".join(bold[i:i + n]) for i in range(len(bold) - n + 1)}
            pages.append(cands)
    # Skip the title page and contents: the body starts on the first page (after page 1) with the title
    tkey = _norm(TITLE)
    start = next(i for i in range(1, len(pages)) if tkey in pages[i])
    result, cur = {}, start
    for idx, (lvl, txt) in enumerate(headings):
        if lvl > 2:
            continue
        key = _norm(txt)
        for i in range(cur, len(pages)):
            if key in pages[i]:
                result[idx] = str(i + 1)
                cur = i
                break
    return result


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    docx_path = os.path.join(OUT_DIR, BASENAME + ".docx")
    pdf_path = os.path.join(OUT_DIR, BASENAME + ".pdf")
    D = build()
    entries = list(D.headings)
    # Pass 1 with placeholder page numbers of realistic width so pagination is stable
    D = build(toc_pages=(entries, {i: "00" for i in range(len(entries))}))
    D.save(docx_path)
    convert_docx_to_pdf(docx_path, pdf_path)
    pages = find_pages(pdf_path, entries)
    D = build(toc_pages=(entries, pages))
    D.save(docx_path)
    convert_docx_to_pdf(docx_path, pdf_path)
    pages2 = find_pages(pdf_path, entries)
    if pages2 != pages:
        D = build(toc_pages=(entries, pages2))
        D.save(docx_path)
        convert_docx_to_pdf(docx_path, pdf_path)
    missing = [entries[i][1] for i in range(len(entries)) if entries[i][0] <= 2 and i not in pages2]
    print("Saved", docx_path, "and", pdf_path)
    if missing:
        print("Headings not located in PDF:", missing)


if __name__ == "__main__":
    main()
