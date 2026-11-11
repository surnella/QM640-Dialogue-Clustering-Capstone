"""
Part 1 of the QM640 Final Report builder (aligned to the QM 640 Final Report Template,
Moderator Committee feedback, and 400-point Final Report Rubric):
  - Front Matter (Title Page, GitHub Repository & Table of Contents)
  - Abstract (single focused paragraph, strictly 300–350 words, covering problem, solution,
    data N/unit/timeframe, CPU/GPU technology, RQ1–RQ4 metrics, and implementation)
  - Section 1: Introduction (Background and Context, Problem Statement with Y/X/unit/timeframe/metrics,
    Purpose of the Study, Research Problems and Research Questions + Table 1, Contributions and Expected Value)
  - Section 2: Literature Review (Literature Review Approach, Summary of Key Literature + 6-column
    Table 2 Relevance Matrix, 4-paragraph Thematic Synthesis covering DL and Agentic/LLM work)
  - Section 3: Materials and Methods (Data Sources/URLs/Inclusion-Exclusion + Tables 3–5,
    Database Setup/Vector Indexing/Data Access/Splitting, Expanded Univariate/Outcome/Bivariate/Multivariate
    EDA + Tables 6–7 & Figures 1–3, Research Design/Hypotheses/Sample Size Eq. 1 & Table 8,
    Model Selection/Feature Importance Assessment & Utilization/Metrics Eq. 2 & Tables 9–10)
  - Section 4: Architecture and Workflow (System Overview, Architecture Diagram Figures 4–5,
    Workflow Components [Ingestion, Preprocessing/Scaling/Encoding, Missing/Outliers, EDA/Features,
    Model Dev/Eval/Deployment], Tools and Technologies)
"""

import os
import pandas as pd
from report.final_context import (
    FIG_FIN,
    FIG_INT,
    REPO,
    TITLE,
    n2,
    nz,
    pct,
    pv,
    pv_cell,
)


def build_part1(D, ctx, toc_pages=None):
    ss = ctx["ss"]
    qa = ctx["qa"]
    desc = ctx["desc"]
    s1 = ctx["s1"]
    r1 = ctx["r1"]
    r1h = ctx["r1h"]
    r1t = ctx["r1t"]
    r2_ref = ctx["r2_ref"]
    r3_fin = ctx["r3_fin"]
    r4_fin = ctx["r4_fin"]
    rules = ctx["rules"]
    t_biv = ctx["t_biv"]
    t_out = ctx["t_out"]
    t_fi = ctx["t_fi"]
    t_blk = ctx["t_blk"]
    t_split = ctx["t_split"]
    eda_ext = ctx["eda_ext"]
    rt_diag = ctx["rt_diag"]
    trg = ctx["trg"]
    tr3 = trg[trg.k == 3].set_index("M")

    fq = qa.iloc[0]
    mq = qa.iloc[1]
    fd = desc.iloc[0]
    md = desc.iloc[1]
    ORDS = [
        "price_sensitivity", "destination_flexibility", "date_flexibility", "exploration_breadth",
        "decisiveness", "detail_orientation", "information_upfront", "revision_tendency",
        "question_asking", "politeness",
    ]
    cv_ = r1h["criterion_validity"]

    an1 = r1["anova"]
    r2_sc = r2_ref["results"]["sbert_style_cos"]
    r2_sa = r2_sc["anova"]
    r2_we = r2_ref["results"]["word_abs_err"]["anova"]
    r3_rar_a = r3_fin["anova"]["rule_adherence"]["effects"]["rules_mode"]
    r3_elr_i = r3_fin["anova"]["leakage_rate"]["effects"]["interaction"]
    r3_sf1_a = r3_fin["anova"]["slot_f1"]["effects"]["rules_mode"]
    r4_lt_p = r4_fin["anova"]["log_turns"]["effects"]["prompt_mode"]
    r4_lt_i = r4_fin["anova"]["log_turns"]["effects"]["interaction"]

    # ------------------------------------------------------------------ Title Page
    D.title_page(
        ["Data Analytics Capstone", TITLE, "Final Report"],
        [
            "Surnella Sandeep",
            "Department of Data Analytics, Walsh College",
            "QM640: Data Analytics Capstone",
            "Instructor and Mentor: Mr. Smitraj Raut",
            "November 10, 2026",
            f"<b>GitHub Repository:</b> {REPO}",
        ],
    )

    # ------------------------------------------------------------------ TOC
    D.toc(toc_pages[0] if toc_pages else [], toc_pages[1] if toc_pages else None)

    # ================================================================== ABSTRACT
    D.heading("Abstract", 1, new_page=True)
    D.para(
        "Online travel agencies (OTAs) deploy large language model (LLM) agents for package "
        "booking, yet static prompts ignore user diversity while unguarded few-shot "
        "prompts risk entity leakage and rule violations. This study tests a neuro-symbolic system "
        "joining power analysis, clustering, deep learning embeddings, and "
        "agentic prompting with rule checks. The study proceeds across four stages formulated "
        "as separate research questions, <b>RQ1-Identify, RQ2-Personalize, RQ3-Govern, and RQ4-Optimize</b>, where "
        "each stage proves a prerequisite, drops non-viable methods, and transfers its validated causal artifacts "
        "to the next stage. First, the <b>RQ1-Identify</b> stage proves shopper behavior can be segmented "
        "from opening prefixes without outcome confounding, dropping noise-rejecting and whole-dialogue "
        "models to transfer three archetype centroids, vector sub-indices, and a prefix router to "
        "the <b>RQ2-Personalize</b> stage. Second, the <b>RQ2-Personalize</b> stage uses those routed labels "
        "and exemplar pools to prove cluster-adaptive few-shot prompting aligns assistant style and "
        "word-length pacing to the persona without semantic drift, dropping static prompts and "
        "transferring the adaptive generator to the <b>RQ3-Govern</b> stage. Third, the <b>RQ3-Govern</b> stage tests "
        "the adaptive generator under policy stress to prove pairing symbolic rule checks with slot "
        "masking eliminates entity leakage and enforces booking rules while preserving style, dropping unguarded "
        "prompts and transferring the governed agent to the <b>RQ4-Optimize</b> stage. Fourth, the "
        "<b>RQ4-Optimize</b> stage deploys the cascaded <b>RQ1-Identify</b> router, <b>RQ2-Personalize</b> adaptive "
        "prompts, and <b>RQ3-Govern</b> rule-governed slot ledger in closed-loop multi-turn simulations to prove that "
        "matching memory tracking and trade-off framing to each archetype compresses turns and removes repeat slot "
        "asks. Multi-turn user–agent dialogues form the unit of analysis across "
        f"<i>N</i> = {n2(fq.n_analytic, 0)} Microsoft Frames dialogues (2016–2017; "
        f"70% golden <i>n</i> = {s1['n_gold']}, 30% test <i>n</i> = {s1['n_test']}) and "
        f"<i>N</i> = {n2(mq.n_analytic, 0)} MultiWOZ 2.2 dialogues (2020) over 10 weeks in 2026, built in Python "
        "3.11 (<i>scikit-learn</i>, <i>Statsmodels</i>, Facebook AI Similarity Search [<i>FAISS</i>], Sentence-BERT "
        "[SBERT]) on an 8-core Apple M-series CPU and cloud GPU/TPU via Gemini 2.5 Flash and Pro (α = .05). "
        "Across the four stages, empirical findings confirm each handoff: in the <b>RQ1-Identify</b> stage, "
        "density clustering dropped 24.4%–39.1% of sessions as noise and whole-dialogue clusters suffered outcome "
        "confounding (κ = .24); dropping both, 100%-coverage <i>K</i>-Means (<i>k</i> = 3) on a 46-d <i>Blocks</i> "
        "prefix matrix yielded three stable archetypes (Adjusted Rand Index = .89), namely <i>Decisive Booker</i>, "
        "<i>Open Explorer</i>, and <i>Rigid-Constraint Seeker</i>, routing test prefixes at 70.1% accuracy (κ = .535, "
        "area under curve [AUC] = .871) at five messages and 97.3% (κ = .958) at nine to hand off the router and "
        f"FAISS sub-indices to the <b>RQ2-Personalize</b> stage. In the <b>RQ2-Personalize</b> stage (<i>N</i> = {r2_ref['N']}), "
        "coarse unrefined clusters failed (<i>p</i> = .211) and were dropped, whereas the carried-forward refined "
        "router and slot-masked FAISS exemplars raised SBERT style cosine from .453 (static) and .530 (zero-shot) to "
        ".597 (<i>p</i> < .001) and cut pacing error from 10.12 to 3.87 words (<i>p</i> = .007), handing off the "
        f"adaptive generator to the <b>RQ3-Govern</b> stage. In the <b>RQ3-Govern</b> stage (2 × 2, <i>N</i> = {r3_fin['N']}), "
        "unguarded few-shot prompts leaked exemplar entities (.359 rate) and caught only 5.6% of violations; dropping "
        "unguarded prompts and activating YAML rules with <i>[SLOT]</i> masking drove leakage to .000 "
        "(<i>p</i> < .001), lifted violation sensitivity to 98.6% (<i>p</i> < .001), and raised Slot F<sub>1</sub> "
        "to .952 while preserving style, handing off the governed agent to the <b>RQ4-Optimize</b> stage. In the "
        f"<b>RQ4-Optimize</b> stage (2 × 3, <i>N</i> = {r4_fin['N']}), cascading all upstream stages with a slot "
        "ledger and persona trade-offs removed repeat asks (.109 → .000, <i>p</i> < .001) and cut turns by 29.5%–42.7% "
        "(<i>p</i> < .001; 8.73 → 5.00 turns for <i>Rigid-Constraint Seekers</i>), operationalizing turn economy "
        "in a FastAPI/Redis service.",
        indent=False,
    )
    D.para(
        "<i>Keywords:</i> conversational artificial intelligence, customer archetypes, large language models, "
        "in-context learning, feature importance, business-rule enforcement, dialogue turn economy",
        indent=False,
    )

    # ================================================================== 1. INTRODUCTION
    D.heading("Introduction", 1, new_page=True)
    D.heading("Background and Context", 2)
    D.para(
        "Conversational artificial intelligence (AI) assistants have become a primary digital service channel in "
        "travel, tourism, and hospitality, supporting destination discovery, multi-package comparison, and itinerary "
        "booking across online travel agencies (OTAs), tour operators, and hotel contact centers (Buhalis & Sinarta, "
        "2019; Ivanov & Webster, 2019; Jannach et al., 2021). Unlike single-turn informational queries, vacation "
        "package booking is a consultative, multi-turn negotiation in which travelers balance competing constraints "
        "across origin city, destination city, departure and return dates, trip duration, party composition, hotel "
        "star rating, and total budget (El Asri et al., 2017). Empirical observations of travel agency dialogues show "
        "that shoppers exhibit markedly different behavioral trajectories: some state complete trip parameters up "
        "front and seek immediate confirmation, others explore multiple destinations and hotel tiers side by side, "
        "and others maintain rigid date and luxury requirements that trigger constraint deadlocks when preferred "
        "inventory exceeds their budget ceiling (Inaba et al., 2022; Melián-González et al., 2021)."
    )
    D.para(
        "Despite this behavioral heterogeneity, commercial large language model (LLM) travel assistants typically "
        "operate under a single static system prompt and a uniform slot-filling questionnaire. Sequentially querying "
        "one missing slot per turn or presenting a single hotel option without trade-off framing inflates conversation "
        "length, triggers repetitive slot re-asking, and drives customer abandonment before quotation agreement is "
        "reached. For hospitality operators and OTA engineering teams, excess conversational turns also inflate cloud "
        "LLM inference latency and token expenditure while degrading self-service conversion rates (Buhalis & Sinarta, "
        "2019; Melián-González et al., 2021)."
    )
    D.para(
        "Conversely, attempting to personalize an LLM assistant purely through dynamic few-shot in-context learning "
        "(ICL) introduces two severe operational hazards (Brown et al., 2020; Liu et al., 2022; Rebedea et al., 2023). "
        "First, injecting unmasked historical dialogue exemplars into the prompt induces factual entity leakage, in "
        "which the generative model copies stale hotel names, prices, dates, or promotional codes from retrieved "
        "examples into the active customer session. Second, stylistic prompt instructions compete for model attention "
        "with enterprise booking policies, causing unguarded LLMs to overlook mandatory visa lead-time windows, "
        "passport validity rules, group occupancy thresholds, discount ceilings, or minimum package budgets (Yao "
        "et al., 2024). Resolving the tension between stylistic adaptability, policy compliance, and turn economy "
        "therefore requires a neuro-symbolic architecture that couples early-turn behavioral routing with deterministic "
        "symbolic verification."
    )

    D.heading("Problem Statement", 2)
    D.para(
        "The objective of this study is to model, predict, and optimize six quantitative dependent variables "
        "(<i>Y</i>), specifically unsupervised cluster separation Silhouette and Davies–Bouldin index (<i>Y</i><sub>1</sub>), "
        "de-lexicalized Sentence-Bidirectional Encoder Representations from Transformers (SBERT) style convergence "
        "cosine and archetype pacing calibration error in words (<i>Y</i><sub>2</sub>), policy rule adherence rate "
        "decomposed into violation enforcement sensitivity and compliant acceptance specificity (<i>Y</i><sub>3</sub>), "
        "exemplar entity leakage rate (<i>Y</i><sub>4</sub>), factual slot coverage F<sub>1</sub> (<i>Y</i><sub>5</sub>), "
        "and natural-log-transformed turns to goal completion (TGC) and redundant elicitation rate (RER; "
        "<i>Y</i><sub>6</sub>), for the unit of analysis of individual multi-turn customer–assistant travel dialogue "
        "trajectories and turn-level agent responses using four manipulated independent variables (<i>X</i>): "
        "clustering algorithm and prefix feature representation (<i>X</i><sub>1</sub>, research question 1 [RQ1]), "
        "in-context prompting strategy (<i>X</i><sub>2</sub>, RQ2), declarative rule-engine governance mode crossed "
        "with prompting strategy (<i>X</i><sub>3</sub>, RQ3), and prompting strategy crossed with refined user "
        "archetype (<i>X</i><sub>4</sub>, RQ4) over the archival 2016–2017 Microsoft Frames corpus (<i>N</i> = 1,334 "
        "analytic dialogues) and 2020 MultiWOZ 2.2 benchmark (<i>N</i> = 1,499 analytic dialogues) evaluated during "
        "the 2026 experimental window. Success is evaluated at the α = .05 significance level using analysis of "
        "variance (ANOVA) <i>F</i>-tests, partial eta-squared (η<sub><i>p</i></sub><sup>2</sup>) effect sizes, "
        "bootstrap Adjusted Rand Index (ARI ≥ .60), held-out Cohen's κ and multi-class ROC-AUC, dual-judge "
        "inter-rater κ, and percentage reductions in conversational turns and redundant slot requests."
    )

    D.heading("Purpose of the Study", 2)
    D.para(
        "The purpose of this quantitative experimental study is fourfold: (1) to segment multi-turn travel shoppers "
        "into stable, interpretable behavioral archetypes using opening-prefix embeddings and structured LLM "
        "behavioral ratings, while quantifying feature importance to construct an accurate early-turn prefix classifier; "
        "(2) to evaluate whether routing test prefixes into archetype-partitioned Facebook AI Similarity Search (FAISS) "
        "exemplar sub-indices and pacing directives improves discourse style convergence and word-length calibration; "
        "(3) to test in a 2 × 2 factorial design how a declarative YAML Ain't Markup Language (YAML) rule engine and "
        "slot masking interact with cluster-adaptive prompting to govern policy compliance, factual slot grounding, "
        "and entity leakage; and "
        "(4) to quantify in a 2 × 3 closed-loop simulation how pairing a persistent informed-slot ledger with "
        "archetype-tailored trade-off policies compresses turns to package agreement across distinct traveler personas."
    )

    D.heading("Research Problems and Research Questions", 2)
    D.para(
        "To operationalize the problem statement across the four-stage <b>RQ1-Identify → RQ2-Personalize → "
        "RQ3-Govern → RQ4-Optimize</b> architecture, the study investigates four linked research questions:"
    )
    D.items([
        "<b>Research Question 1 (RQ1-Identify Stage):</b> Which unsupervised clustering algorithm (<i>K</i>-Means, Ward "
        "agglomerative clustering, or Hierarchical Density-Based Spatial Clustering of Applications with Noise "
        "[HDBSCAN]) best separates multi-turn travel dialogue representations, which semantic and behavioral features "
        "carry the highest discriminative importance, and how accurately can the resulting refined user archetypes be "
        "routed from early conversation prefixes (<i>M</i> ∈ {3, 5, 7, 9} user messages)?",
        "<b>Research Question 2 (RQ2-Personalize Stage):</b> Does dynamic cluster-adaptive few-shot prompting, combining "
        "archetype-partitioned, slot-masked FAISS exemplar retrieval with routed archetype pacing directives, significantly "
        "increase de-lexicalized SBERT style convergence and reduce archetype pacing calibration error relative to "
        "zero-shot and static few-shot baselines?",
        "<b>Research Question 3 (RQ3-Govern Stage):</b> In a 2 × 2 factorial design crossing declarative rule-engine mode "
        "(<i>Rules Off</i> vs. <i>Rules Active</i>) with prompting strategy (<i>Zero-Shot</i> vs. <i>Cluster-Adaptive "
        "Few-Shot</i>), what are the main and interaction effects on policy rule adherence (violation sensitivity and "
        "compliant specificity), exemplar entity leakage rate (ELR), factual slot coverage F<sub>1</sub>, and style "
        "alignment?",
        "<b>Research Question 4 (RQ4-Optimize Stage):</b> In a 2 × 3 factorial multi-turn simulation crossing prompting "
        "policy (<i>Zero-Shot</i> vs. <i>Cluster-Adaptive Few-Shot</i> with a <i>Verified Informed Slot Ledger</i>) "
        "and refined user archetype (<i>Decisive Booker</i>, <i>Open Explorer</i>, <i>Rigid-Constraint Seeker</i>), "
        "what are the main and interaction effects on log-transformed turns to goal completion (TGC) and redundant "
        "elicitation rate (RER)?",
    ], numbered=False)
    D.para(
        "Table 1 maps each research question to its formal null (<i>H</i><sub>0</sub>) and alternative "
        "(<i>H</i><sub>a</sub>) hypotheses, experimental design, and statistical testing framework."
    )
    D.table(
        "Research Questions, Null and Alternative Hypotheses, and Analytical Framework",
        ["RQ", "Research question", "Null and alternative hypotheses", "Experimental design and statistical test"],
        [
            [
                "RQ1",
                "Which clustering algorithm best separates dialogue embeddings, which features drive separation, and "
                "which early-routable archetypes emerge?",
                "<i>H</i><sub>01</sub>: μ<sub>KM</sub> = μ<sub>Ward</sub> = μ<sub>HDB</sub> on Silhouette; prefix "
                "routing κ ≤ 0. <i>H</i><sub>a1</sub>: At least one algorithm mean differs, and hybrid prefix "
                "features yield stable (ARI ≥ .60), routable archetypes (κ > 0).",
                "Resampling benchmark (<i>N</i> = 159 runs across 53 matched <i>n</i> = 500 seeds: one-way ANOVA, "
                "matched RM-ANOVA, Friedman, Welch, Kruskal–Wallis) + feature importance (η<sup>2</sup>, Δκ) + "
                "Train/CV/Test prefix routing",
            ],
            [
                "RQ2",
                "Does cluster-adaptive few-shot prompting improve style convergence and pacing calibration over "
                "zero-shot and static few-shot baselines?",
                "<i>H</i><sub>02</sub>: μ<sub>ZS</sub> = μ<sub>Static</sub> = μ<sub>Adaptive</sub> on style cosine "
                "and pacing error. <i>H</i><sub>a2</sub>: μ<sub>Adaptive</sub> > μ<sub>Static</sub>, μ<sub>ZS</sub> "
                "on style cosine and μ<sub>Adaptive</sub> < μ<sub>Static</sub>, μ<sub>ZS</sub> on pacing error.",
                "One-way repeated-measures ANOVA (RM-ANOVA; <i>N</i> = 33 held-out dialogues × 3 conditions = 99 "
                "generations; Greenhouse–Geisser correction, Friedman test, Holm-adjusted paired <i>t</i> contrasts)",
            ],
            [
                "RQ3",
                "How do a declarative rule engine and cluster-adaptive prompting interact to govern rule adherence, "
                "entity leakage, slot F<sub>1</sub>, and style alignment?",
                "<i>H</i><sub>03</sub>: α<sub>Rules</sub> = β<sub>Prompt</sub> = (αβ)<sub>Rules×Prompt</sub> = 0 "
                "across RAR, ELR, Slot F<sub>1</sub>, and style cosine. <i>H</i><sub>a3</sub>: Active rules raise "
                "RAR and Slot F<sub>1</sub> and interact with prompting to eliminate few-shot entity leakage.",
                "2 × 2 factorial ANOVA (<i>N</i> = 144 evaluations across 36 stratified held-out dialogues, "
                "<i>n</i> = 36/cell; ordinary least squares [OLS], heteroscedasticity-consistent [HC3], Aligned Rank "
                "Transform [ART], sensitivity/specificity split; dual-LLM judge κ)",
            ],
            [
                "RQ4",
                "Does cluster-adaptive prompting with an informed-slot ledger reduce turns to goal completion and "
                "redundant elicitation across user archetypes?",
                "<i>H</i><sub>04</sub>: α<sub>Prompt</sub> = β<sub>Arch</sub> = (αβ)<sub>Prompt×Arch</sub> = 0 on "
                "ln(TGC) and RER. <i>H</i><sub>a4</sub>: Cluster-adaptive prompting reduces ln(TGC) and RER with a "
                "significant prompting × archetype interaction.",
                "2 × 3 between-subjects factorial ANOVA on ln(TGC) and RER (<i>N</i> = 180 unique held-out seed "
                "dialogues, <i>n</i> = 30/cell; OLS, HC3, ART, Welch <i>t</i>, Mann–Whitney <i>U</i>; blind persona κ)",
            ],
        ],
        note="RQ = research question; KM = K-Means; HDB = HDBSCAN; ARI = adjusted Rand index; RM-ANOVA = repeated-measures "
             "analysis of variance; RAR = rule adherence rate; ELR = exemplar leakage rate; TGC = turns to goal completion; "
             "RER = redundant elicitation rate. All hypothesis tests are evaluated at α = .05.",
        widths=[0.42, 1.88, 2.10, 2.10],
        align=["l", "l", "l", "l"],
        split=True,
    )

    D.heading("Contributions and Expected Value", 2)
    D.lead_para(
        "Practical contribution",
        "This study delivers a deployable neuro-symbolic conversational blueprint that eliminates the 35.9% exemplar "
        "entity leakage rate (55.6% session incidence) of unguarded few-shot prompting while raising policy-violation "
        "enforcement sensitivity from 5.6% to 98.6% and compressing multi-turn package negotiations by 29.5% to 42.7% "
        "without redundant slot questions.",
    )
    D.lead_para(
        "Technical contribution",
        "Methodologically, the study (1) proves that truncating dialogues to opening user prefixes (<i>M</i> = 9) and "
        "fusing 20 Gemini semantic principal components with 26 encoded LLM behavioral columns (<i>Blocks</i>) resolves "
        "end-of-dialogue outcome confounding and yields high bootstrap stability (ARI = .89/.87); (2) establishes a "
        "three-part feature-importance methodology (cluster variance explained η<sup>2</sup>, standardized logistic "
        "regression coefficient norms, and held-out permutation drop Δκ) that directly governs feature selection, "
        "centroid naming, and prefix routing (70.1% accuracy, κ = .535, ROC-AUC = .871 at <i>M</i> = 5); and (3) "
        "provides rigorous parametric (ordinary least squares [OLS], Greenhouse–Geisser), heteroscedasticity-consistent "
        "(Welch, MacKinnon–White HC3), and non-parametric (Kruskal–Wallis, Friedman, Mann–Whitney <i>U</i>, Aligned Rank "
        "Transform [ART]) triangulation across all four stages.",
    )
    D.lead_para(
        "Value to stakeholders and target users",
        "For travelers, the system provides concise, non-repetitive consultations tailored to their decision style: rapid "
        "confirmation for <i>Decisive Bookers</i>, side-by-side package comparisons for <i>Open Explorers</i>, and "
        "immediate budget-feasible trade-offs for <i>Rigid-Constraint Seekers</i>. For OTA engineering teams, tour "
        "operators, and compliance officers, the architecture reduces LLM inference compute by roughly one-third while "
        "enforcing deterministic visa, passport, occupancy, discount, and minimum-budget rules prior to response delivery.",
    )

    # ================================================================== 2. LITERATURE REVIEW
    D.heading("Literature Review", 1)
    D.heading("Literature Review Approach", 2)
    D.para(
        "A systematic search of peer-reviewed literature was conducted across the Association for Computational "
        "Linguistics (ACL) Anthology, Association for Computing Machinery (ACM) Digital Library, Institute of "
        "Electrical and Electronics Engineers (IEEE) Xplore, ScienceDirect, Emerald Insight, and Google Scholar using "
        "Boolean combinations of <i>travel and hospitality chatbots</i>, <i>conversational recommender systems</i>, "
        "<i>task-oriented dialogue corpora</i>, <i>deep learning sentence embeddings</i>, <i>unsupervised trajectory "
        "clustering</i>, <i>in-context exemplar retrieval</i>, and <i>agentic LLM guardrails</i>. Studies were included "
        "if they provided empirical datasets, mathematical clustering or embedding methods, agentic LLM prompting or "
        "guardrail architectures, or statistical power and evaluation frameworks applicable to multi-turn dialogue. "
        "Thirty relevant sources, comprising 28 peer-reviewed journal articles, conference proceedings, and reference "
        "monographs alongside two explicitly labeled technical preprints, were synthesized to establish the theoretical "
        "and methodological foundation for RQ1 through RQ4."
    )

    D.heading("Summary of Key Literature", 2)
    D.para(
        "Table 2 presents the literature relevance matrix across fourteen foundational entries, detailing each study's "
        "author and year, domain context, dataset or experimental setting, analytical methods, key empirical findings, "
        "and the exact operational inspiration derived for each stage of the <b>RQ1-Identify → RQ2-Personalize → "
        "RQ3-Govern → RQ4-Optimize</b> research framework."
    )
    D.table(
        "Literature Relevance Matrix Across Travel, Deep Learning, Clustering, and Agentic LLM Domains",
        [
            "Author (Year)",
            "Domain / Context",
            "Dataset / Setting",
            "Method(s)",
            "Key Findings",
            "RQ Linkage & Stage Operationalization",
        ],
        [
            [
                "Buhalis & Sinarta (2019); Ivanov & Webster (2019)",
                "Tourism & hospitality service automation",
                "Enterprise hospitality & travel service ecosystems",
                "Real-time 'nowness' co-creation & AI economic framework",
                "Self-service AI creates ROI only when resolving complex inquiries rapidly without human escalation",
                "<b>RQ4-Optimize Stage & Overarching Goal:</b> Inspires operationalizing turn economy (TGC) and policy compliance as the end-to-end business target",
            ],
            [
                "Melián-González et al. (2021)",
                "Consumer travel chatbot adoption",
                "Survey of <i>N</i> = 1,476 travel & tourism consumers",
                "Structural equation modeling of behavioral intention",
                "Perceived task fit and low interaction effort are primary drivers of travel chatbot adoption",
                "<b>RQ2-Personalize → RQ4-Optimize Stages:</b> Inspires operationalizing persona pacing calibration and zero redundant slot asks (RER)",
            ],
            [
                "Jannach et al. (2021); Inaba et al. (2022)",
                "Conversational recommender systems (CRS)",
                "100+ CRS studies & multi-turn travel agency corpus",
                "Taxonomy of preference elicitation & dialogue act analysis",
                "Travelers differ sharply in exploration breadth and constraint rigidity; static policies cause churn",
                "<b>RQ1-Identify → RQ4-Optimize Stages:</b> Inspires operationalizing the 3-archetype taxonomy and persona trade-off policies",
            ],
            [
                "El Asri et al. (2017)",
                "Goal-oriented travel package dialogue",
                "Microsoft Frames (1,369 human Wizard-of-Oz dialogues)",
                "Multi-frame slot tracking & frame-switching annotation",
                "Captures nonlinear budget trade-offs, slot revisions, and multi-offer vacation package comparisons",
                "<b>All Four Stages (RQ1-Identify to RQ4-Optimize):</b> Inspires operationalizing multi-offer package negotiation on the primary corpus (<i>N</i> = 1,334; 933 gold / 401 test)",
            ],
            [
                "Budzianowski et al. (2018); Zang et al. (2020)",
                "Multi-domain task-oriented dialogue",
                "MultiWOZ & MultiWOZ 2.2 (10,438 dialogues across 7 domains)",
                "Corrected turn-level slot state tracking benchmarks",
                "Standardizes slot annotations for hotel, train, attraction, and taxi bookings without airfare packages",
                "<b>RQ1-Identify Stage:</b> Operationalizes external cross-corpus domain-shift validation (<i>N</i> = 1,499) before locking Frames centroids",
            ],
            [
                "Reimers & Gurevych (2019); Lee et al. (2025)",
                "Deep learning semantic embeddings",
                "SNLI, STS, & multilingual retrieval benchmarks",
                "Siamese BERT (<i>all-MiniLM-L6-v2</i>, 384-d) & <i>gemini-embedding-001</i> (3,072-d)",
                "Contrastive transformer embeddings map semantically equivalent utterances into cosine space",
                "<b>RQ1-Identify → RQ2-Personalize Stages:</b> Operationalizes 3,072-d PCA-20 prefix embeddings in the RQ1-Identify stage and de-lexicalized SBERT style cosine in the RQ2-Personalize stage",
            ],
            [
                "Rousseeuw (1987); Davies & Bouldin (1979); McInnes et al. (2017, 2018)",
                "Unsupervised clustering & manifold learning",
                "High-dimensional metric & density clustering benchmarks",
                "Cosine Silhouette, Davies–Bouldin index, HDBSCAN density clustering, & UMAP projection",
                "Silhouette and DB quantify partition compactness; HDBSCAN isolates dense cores but rejects noise",
                "<b>RQ1-Identify Stage:</b> Operationalizes 159-run algorithm selection, proving why noise-dropping HDBSCAN is dropped and 100%-coverage <i>K</i>-Means (<i>k</i>=3) is carried to the RQ2-Personalize stage",
            ],
            [
                "Hennig (2007); Hubert & Arabie (1985); Pedregosa et al. (2011)",
                "Cluster stability & machine learning",
                "Bootstrap resampling & <i>scikit-learn</i> ML suite",
                "Chance-corrected Adjusted Rand Index (ARI) across 80% subsamples & L2 logistic classification",
                "ARI ≥ .60 confirms reproducible structure; regularized linear routers generalize on compact features",
                "<b>RQ1-Identify → RQ2-Personalize Stages:</b> Operationalizes bootstrap stability (ARI = .89) and the L2 logistic prefix router handed off to the RQ2-Personalize stage",
            ],
            [
                "Gilardi et al. (2023)",
                "LLM behavioral text annotation",
                "Political & social science coding benchmarks",
                "Zero-temperature LLM structured codebook annotation vs. human crowd workers",
                "Zero-temperature LLMs achieve higher inter-coder reliability than crowd workers on structured scales",
                "<b>RQ1-Identify & RQ4-Optimize Stages:</b> Operationalizes the 16-field temperature-0 LLM behavioral codebook (κ<sub><i>w</i></sub> = .87–.96) fused with prefix embeddings",
            ],
            [
                "Brown et al. (2020); Liu et al. (2022); Johnson et al. (2021)",
                "Deep learning & agentic in-context learning",
                "GPT-3 few-shot NLP benchmarks & billion-scale vector search",
                "Few-shot prompting, KATE <i>k</i>-NN exemplar selection, & FAISS <i>IndexFlatIP</i> search",
                "Semantically matched in-context examples outperform static prompts in sub-millisecond vector lookup",
                "<b>RQ2-Personalize Stage:</b> Inspires operationalizing three archetype-partitioned FAISS sub-indices (<i>k</i> = 3) handed off to the RQ3-Govern stage",
            ],
            [
                "Rebedea et al. (2023); Yao et al. (2024)",
                "Agentic LLM guardrails & policy safety",
                "NeMo Guardrails & τ-bench airline/retail policy suite",
                "Programmable symbolic rails & multi-turn tool-agent policy compliance evaluation",
                "Prompt-only LLM agents violate domain rules in > 40% of complex multi-turn interactions",
                "<b>RQ3-Govern Stage:</b> Inspires operationalizing deterministic YAML rule checks and [SLOT] masking on top of RQ2-Personalize adaptive prompts before the RQ4-Optimize stage",
            ],
            [
                "Acikgoz et al. (2025); Zhang et al. (2020)",
                "Dialogue & neural generation evaluation",
                "TD-EVAL multi-turn benchmarks & WMT generation tasks",
                "Turn-level factual precision + dialogue comparisons & contextual BERTScore F<sub>1</sub>",
                "Multi-turn evaluation requires pairing contextual similarity with fine-grained factual slot audits",
                "<b>RQ2-Personalize → RQ4-Optimize Stages:</b> Operationalizes multi-dimensional stage gatekeeping (SBERT style, BERTScore, Slot F<sub>1</sub>, ELR, RER)",
            ],
            [
                "Cohen (1988); Faul et al. (2007); Greenhouse & Geisser (1959)",
                "Statistical power & repeated-measures design",
                "Behavioral & experimental design methodology",
                "Noncentral-<i>F</i> sample size derivation (G*Power) & sphericity-corrected RM-ANOVA",
                "Noncentral <i>F</i> ensures 1 − β ≥ .80 at α = .05; ε correction prevents Type I error inflation",
                "<b>All Four Stages (RQ1-Identify to RQ4-Optimize):</b> Operationalizes a priori sample size power (Table 8) and Greenhouse–Geisser RM-ANOVA in the RQ1-Identify and RQ2-Personalize stages",
            ],
            [
                "Seabold & Perktold (2010); Wobbrock et al. (2011)",
                "Econometric & non-parametric factorial ANOVA",
                "Python <i>Statsmodels</i> suite & skewed factorial data",
                "OLS Type II/III ANOVA, White/MacKinnon HC3 robust covariance, & Aligned Rank Transform (ART)",
                "HC3 and rank-based ART preserve valid factorial inference under variance heterogeneity and floor bounds",
                "<b>RQ3-Govern → RQ4-Optimize Stages:</b> Operationalizes parametric, HC3, and ART factorial validation for the 2×2 and 2×3 cascades",
            ],
        ],
        note="CRS = conversational recommender system; ARI = adjusted Rand index; FAISS = Facebook AI Similarity Search; "
             "RM-ANOVA = repeated-measures ANOVA; HC3 = heteroscedasticity-consistent standard error; ART = aligned rank transform.",
        widths=[0.98, 0.86, 0.92, 1.12, 1.22, 1.40],
        align=["l", "l", "l", "l", "l", "l"],
        split=True,
    )

    D.heading("Thematic Synthesis and Research Gaps", 2)
    D.para(
        "<i>Operationalizing the overarching framework and the RQ4-Optimize stage from hospitality and CRS literature.</i> "
        "The four-stage <b>RQ1-Identify → RQ2-Personalize → RQ3-Govern → RQ4-Optimize</b> progression was derived directly "
        "by synthesizing operational gaps across four distinct literature streams and translating their theoretical "
        "constructs into an integrated LLM-and-clustering pipeline. In digital travel and hospitality commerce, "
        "competitive differentiation relies on real-time itinerary co-creation ('nowness' service; Buhalis & Sinarta, "
        "2019). Ivanov and Webster (2019) established that automated conversational agents generate net economic value "
        "only when they resolve consultative inquiries rapidly without human escalation, while Melián-González et al. "
        "(2021) demonstrated across 1,476 consumers that travel chatbot adoption is governed by perceived task fit and "
        "low interaction effort. Corpus studies of conversational recommender systems (CRS) further revealed that human "
        "travel agents achieve efficiency by adapting their turn pacing and recommendation strategy to three recurring "
        "shopper postures: confirming bookings concisely for decisive buyers, curating side-by-side comparisons for "
        "exploratory shoppers, and negotiating date or hotel-tier trade-offs for constraint-bound travelers (Inaba "
        "et al., 2022; Jannach et al., 2021). These hospitality and CRS studies provided the direct inspiration for the "
        "<b>RQ4-Optimize stage</b>: operationalizing business optimization through <i>Turns to Goal Completion (TGC)</i>, "
        "<i>Redundant Elicitation Rate (RER)</i>, a persistent <i>Verified Informed Slot Ledger</i>, and "
        "archetype-tailored trade-off framing. However, because prior tourism studies relied on post-hoc consumer "
        "surveys or manual dialogue-act coding, operationalizing this vision in a live LLM assistant required first "
        "building an algorithmic mechanism to identify customer archetypes early in an active session (<b>RQ1-Identify "
        "stage</b>), personalize generation style (<b>RQ2-Personalize stage</b>), and enforce enterprise booking rules "
        "(<b>RQ3-Govern stage</b>)."
    )
    D.para(
        "<i>Operationalizing the RQ1-Identify stage by fusing deep learning embeddings, clustering theory, and LLM "
        "behavioral coding.</i> To operationalize early-turn archetype identification for the <b>RQ1-Identify stage</b>, "
        "this study drew inspiration from task-oriented dialogue corpora, dense transformer encoders, unsupervised "
        "clustering theory, and zero-temperature LLM annotation. While MultiWOZ (Budzianowski et al., 2018) and "
        "MultiWOZ 2.2 (Zang et al., 2020) standardize single-service slot tracking, Microsoft Frames (El Asri et al., "
        "2017) uniquely captures multi-turn flight-and-hotel package negotiations under budget ceilings and frame "
        "switches, inspiring its selection as the primary discovery and simulation corpus alongside MultiWOZ 2.2 for "
        "cross-corpus transfer testing. Siamese Sentence-BERT encoders (Reimers & Gurevych, 2019) and 3,072-dimensional "
        "Gemini embeddings (Lee et al., 2025) inspired mapping variable-length dialogue prefixes into cosine space, "
        "while clustering validation theory, including Cosine Silhouette (Rousseeuw, 1987), Davies–Bouldin scatter ratios (Davies "
        "& Bouldin, 1979), HDBSCAN density estimation (McInnes et al., 2017), UMAP manifold projection (McInnes et al., "
        "2018; Pedregosa et al., 2011), and bootstrap ARI stability (Hennig, 2007; Hubert & Arabie, 1985), inspired the "
        "159-run algorithm benchmark and the 100%-coverage selection gate that drops noise-rejecting HDBSCAN in favor "
        "of full-coverage <i>K</i>-Means. Crucially, because embedding complete transcripts confounds opening shopper "
        "behavior with end-of-session outcomes, Gilardi et al.'s (2023) finding that zero-temperature LLMs outperform "
        "human crowd workers on structured codebooks inspired operationalizing the 16-field temperature-0 LLM behavioral "
        "schema on opening user prefixes (<i>M</i> ≤ 9) and fusing its 13 non-outcome behavioral fields (26 encoded "
        "columns) with 20 Gemini prefix principal components into the 46-dimensional <i>Blocks</i> representation, using "
        "feature importance (η<sup>2</sup>, ‖<b>β</b>‖<sub>2</sub>, Δκ) to prune outcome-confounded fields and train the "
        "L2 logistic prefix router handed off to the <b>RQ2-Personalize stage</b>."
    )
    D.para(
        "<i>Operationalizing the RQ2-Personalize and RQ3-Govern stages from in-context learning and neuro-symbolic "
        "guardrail literature.</i> Once the <b>RQ1-Identify stage</b> hands off a live prefix router and three archetype "
        "partitions, the <b>RQ2-Personalize stage</b> draws direct operational inspiration from Brown et al.'s (2020) "
        "few-shot in-context learning paradigm, Liu et al.'s (2022) KATE nearest-neighbor exemplar selection, and "
        "Johnson et al.'s (2021) FAISS inner-product vector indexing: rather than querying a single monolithic example "
        "pool (Static Few-Shot), the <b>RQ2-Personalize stage</b> operationalizes three archetype-partitioned "
        "<i>faiss.IndexFlatIP</i> sub-indices paired with routed persona pacing directives so that a shopper classified "
        "at message 5 receives exemplars and word-length norms matched to their exact behavioral archetype. However, "
        "multi-turn agent benchmarks by Yao et al. (2024; τ-bench) and Acikgoz et al. (2025; TD-EVAL) demonstrated that "
        "prompt-only LLM agents violate domain policies in over 40% of sessions and copy stale entities from retrieved "
        "examples. Those failure modes, combined with Rebedea et al.'s (2023) NeMo Guardrails architecture, directly "
        "inspired operationalizing the <b>RQ3-Govern stage</b>: decoupling probabilistic style prompting from a "
        "deterministic YAML rule engine and regex <i>[SLOT]</i> exemplar masking in a 2 × 2 factorial design to "
        "eliminate entity leakage and enforce 98.6% of policy violations before handing the governed agent to the "
        "<b>RQ4-Optimize stage</b>."
    )
    D.para(
        "<i>Operationalizing cross-stage statistical gatekeeping and cascading synthesis.</i> Finally, to ensure that "
        "the four stages function as a rigorous causal cascade rather than disconnected experiments, the statistical "
        "evaluation literature inspired strict quantitative handoff gates at every stage boundary. Contextual similarity "
        "metrics (BERTScore; Zhang et al., 2020) and multi-turn factual audits (TD-EVAL; Acikgoz et al., 2025) inspired "
        "pairing de-lexicalized SBERT style cosine with factual Slot F<sub>1</sub> and Exemplar Leakage Rate; a priori "
        "noncentral-<i>F</i> power derivations (Cohen, 1988; Faul et al., 2007) and Greenhouse–Geisser sphericity "
        "corrections (Greenhouse & Geisser, 1959) governed sample allocation across all four stages; and "
        "heteroscedasticity-consistent (HC3) and non-parametric Aligned Rank Transform (ART) factorial models in "
        "<i>Statsmodels</i> (Seabold & Perktold, 2010; Wobbrock et al., 2011) verified every 2 × 2 (<b>RQ3-Govern</b>) "
        "and 2 × 3 (<b>RQ4-Optimize</b>) interaction under boundary floors. Operationalizing these four literature "
        "streams into a unified pipeline directly bridges four sequential research gaps: (1) prefix-truncated LLM-hybrid "
        "archetype discovery and early routing (<b>RQ1-Identify stage</b>) → (2) archetype-partitioned FAISS style and "
        "pacing personalization (<b>RQ2-Personalize stage</b>) → (3) 2 × 2 neuro-symbolic YAML rule governance and slot "
        "masking (<b>RQ3-Govern stage</b>) → (4) 2 × 3 multi-turn turn-economy optimization via informed-slot ledgers "
        "and persona trade-offs (<b>RQ4-Optimize stage</b>)."
    )

    # ================================================================== 3. MATERIALS AND METHODS
    D.heading("Materials and Methods", 1)
    D.heading("Data Sources, Acquisition, and Inclusion Criteria", 2)
    D.para(
        f"This study utilizes two publicly available, peer-reviewed English task-oriented dialogue corpora (Table 3): "
        f"Microsoft Frames (El Asri et al., 2017; {n2(ctx['n_frames_raw'], 0)} raw dialogues collected in August–September "
        f"2016 and published in 2017; {n2(fq.n_analytic, 0)} analytic dialogues) and MultiWOZ 2.2 (Budzianowski et al., "
        f"2018; Zang et al., 2020; 10,438 raw dialogues published in 2020, from which a seeded travel-domain sample of "
        f"{n2(mq.n_raw, 0)} dialogues yielded {n2(mq.n_analytic, 0)} analytic dialogues). No proprietary web scraping "
        "was required; raw JavaScript Object Notation (JSON) archives were acquired programmatically via "
        "<i>src/ingestion.py</i> from the official Microsoft Research Open Data / Hugging Face repository "
        "(https://huggingface.co/datasets/google/frames-benchmark) and the official MultiWOZ 2.2 GitHub repository "
        "(https://github.com/budzianowski/multiwoz). Both datasets were collected under institutional research consent, "
        "assign anonymized alphanumeric role-player identifiers, and contain zero personally identifiable information."
    )
    D.para(
        "Explicit <b>inclusion and exclusion criteria</b> were enforced programmatically during ingestion "
        "(<i>src/final_pipeline/step1_prepare_data.py</i>; Table 5). Dialogues were <i>included</i> if they (a) "
        "contained valid dialogue and speaker identifiers, (b) involved vacation package negotiation (Frames) or "
        "travel/local hospitality services (hotel, train, attraction, or taxi in MultiWOZ 2.2), and (c) comprised at "
        "least three alternating turns (<i>total_turns</i> ≥ 3, ensuring at least two user turns and one assistant "
        "turn for prefix routing). Dialogues were <i>excluded</i> if they (a) were exact duplicate transcripts "
        "detected via SHA-256 text hashing (1 excluded in Frames; 0 in MultiWOZ) or (b) were aborted fragments with "
        "fewer than three turns (34 excluded in Frames, leaving 1,334 analytic dialogues; 1 excluded in MultiWOZ, "
        "leaving 1,499 analytic dialogues). Table 4 defines all analytical variables and measurement units (raw corpus "
        "fields and canonical schema mappings are documented in Appendix A, Table A3)."
    )
    D.table(
        "Dataset Overview, Public Acquisition URLs, Timeframes, and Analytical Roles",
        ["Attribute", "Microsoft Frames (primary corpus)", "MultiWOZ 2.2 (comparison corpus)"],
        [
            [
                "Citation & timeframe",
                "El Asri et al. (2017); dialogues recorded Aug–Sep 2016, published 2017; analyzed 2026",
                "Budzianowski et al. (2018); Zang et al. (2020); corrected release published 2020; analyzed 2026",
            ],
            [
                "Public acquisition URL & format",
                "https://huggingface.co/datasets/google/frames-benchmark (single <i>frames.json</i> archive)",
                "https://github.com/budzianowski/multiwoz (sharded <i>dialogues_*.json</i> archives)",
            ],
            [
                "Sample size & unit of analysis",
                f"{n2(ctx['n_frames_raw'], 0)} raw; {n2(fq.n_analytic, 0)} analytic multi-turn dialogue trajectories "
                f"(golden <i>D</i><sub>gold</sub> = {s1['n_gold']}, held-out <i>D</i><sub>test</sub> = {s1['n_test']})",
                f"10,438 raw; seeded travel sample of {n2(mq.n_raw, 0)}; {n2(mq.n_analytic, 0)} analytic multi-turn "
                "dialogue trajectories",
            ],
            [
                "Domain & task setting",
                "Consultative flight + hotel vacation package negotiation under budget, date, and star-rating constraints",
                "Multi-domain city services (hotel, train, taxi, attraction) slot-filling without flight packages",
            ],
            [
                "Annotations extracted",
                "Utterance text, speaker role, dialogue acts, slot–value arguments, wizard task success, user 1–5 rating",
                "Utterance text, speaker role, active service domains, turn-level belief-state slot dictionaries",
            ],
            [
                "Analytical role in study",
                "RQ1 clustering, feature importance, & prefix router; RQ2 prompting; RQ3 2×2 governance; RQ4 2×3 simulation",
                "External structural comparison in EDA (Tables 5–6, Figure 1) and cross-corpus projection test in RQ1",
            ],
        ],
        widths=[1.30, 2.70, 2.50],
        align=["l", "l", "l"],
        split=True,
    )
    D.table(
        "Data Dictionary of Analytical Variables With Units and Operational Definitions",
        ["Variable", "Role", "Type and unit", "Operational definition and scale", "RQ"],
        [
            ["Clustering algorithm", "Primary IV", "Categorical (3 levels)", "<i>K</i>-Means (<i>k</i>=3), Ward agglomerative (<i>k</i>=3), HDBSCAN", "1"],
            ["Silhouette & Davies–Bouldin", "Primary/Sec. DV", "Continuous (unitless / ratio)", "Cosine Silhouette [−1, 1] and cluster scatter ratio (≥ 0)", "1"],
            ["Adjusted Rand index (ARI)", "Diagnostic DV", "Continuous [−1, 1] (unitless)", "Chance-corrected partition stability across 80% subsamples", "1"],
            ["LLM behavioral profile (16 fields)", "Clustering / Audit", "10 ordinal (1–5) + 6 cat./bool.", "10 Likert scales + 3 goal/tone clustering fields + 3 audit fields (Table C1)", "1, 4"],
            ["Feature importance (η<sup>2</sup>, ‖β‖<sub>2</sub>, Δκ)", "Explanatory metric", "Proportion [0, 1] / L2 norm / Δκ", "Cluster variance explained η<sup>2</sup>, router weight norm, & test permutation κ drop", "1, 2"],
            ["Refined user archetype", "IV / Moderator", "Categorical (3 levels)", "<i>Decisive Booker</i>, <i>Open Explorer</i>, <i>Rigid-Constraint Seeker</i>", "1–4"],
            ["Prefix routing κ & ROC-AUC", "Validation DV", "Continuous [−1, 1] / [0, 1]", "Chance-corrected Cohen's κ and macro One-vs-Rest area under ROC curve", "1"],
            ["Prompting strategy", "Primary IV", "Categorical (2 or 3 levels)", "Zero-Shot, Static Few-Shot (<i>k</i>=3), Cluster-Adaptive Few-Shot (<i>k</i>=3)", "2–4"],
            ["Style convergence & Pacing err.", "Primary/Sec. DV", "Cosine [−1, 1] / Words (count)", "De-lexicalized SBERT cosine to archetype centroid; |words<sub>gen</sub> − μ<sub>words,<i>a</i></sub>|", "2, 3"],
            ["Rule-engine mode", "Primary IV", "Binary (2 levels)", "<i>Rules Off</i> (unguarded) vs. <i>Rules Active</i> (YAML check + [SLOT] mask + guard)", "3"],
            ["Rule adherence rate (RAR)", "Primary DV", "Proportion [0, 1] (rate)", "Violation enforcement sensitivity (<i>n</i>=18/cell), specificity (<i>n</i>=18/cell), & overall", "3"],
            ["Exemplar leakage rate (ELR)", "Primary DV", "Proportion [0, 1] (rate)", "Share of response entities originating strictly from prompt exemplars", "3"],
            ["Factual slot coverage F<sub>1</sub>", "Primary DV", "Proportion [0, 1] (F<sub>1</sub> score)", "Harmonic mean of precision and recall over active booking state slots", "3"],
            ["Turns to goal (ln TGC) & RER", "Primary/Sec. DV", "Log count (ln turns) / Rate [0, 1]", "Natural log of total turns until [ACCEPT_BOOKING]; redundant asks / agent turns", "4"],
        ],
        note="IV = independent variable; DV = dependent variable; ROC-AUC = receiver operating characteristic area under curve. Raw and canonical schema fields are in Appendix A, Table A3.",
        widths=[1.50, 0.85, 1.20, 2.45, 0.50],
        align=["l", "l", "l", "l", "c"],
        split=True,
    )
    D.table(
        "Data Cleaning, Inclusion/Exclusion Criteria, and Quality Audit Log",
        ["Audit check or criterion", "Target fields", "Detection rule", "Frames", "MultiWOZ", "Treatment and analytical rationale"],
        [
            ["Exact duplicate transcripts", "Utterance text", "SHA-256 full-text hash", str(int(fq.duplicate_text)), str(int(mq.duplicate_text)), "Excluded duplicate record to prevent double-weighting in clustering"],
            ["Minimum turn floor (< 3 turns)", "total_turns", "Turn count < 3", str(int(fq.excluded_lt_min_turns)), str(int(mq.excluded_lt_min_turns)), "Excluded aborted fragments; ≥ 3 turns required for prefix routing"],
            ["Upper-tail turn outliers", "total_turns", "> Q<sub>3</sub> + 1.5 × IQR", f"{int(fq.turn_outliers_iqr)} (> {n2(fq.outlier_threshold, 1)})", f"{int(mq.turn_outliers_iqr)} (> {n2(mq.outlier_threshold, 1)})", "Retained as authentic complex negotiations; natural-log transformed in RQ4"],
            ["Unobserved optional slots", "Tier 1 & Tier 2 slots", "Slot never stated in chat", "Table E1", "Table E1", "Preserved semantically as None; never mean/mode-imputed"],
            ["Missing post-chat user rating", "user_rating", "Null survey field", "3 (11 raw)", "N/A", "Retained for unsupervised clustering; excluded only from rating checks"],
            ["Surface entity values", "Utterance text", "Slot & numeric regex", "All", "All", "Replaced with [SLOT] tags in FAISS exemplars to prevent entity leakage"],
            ["Final analytic sample", "All schema fields", "Post-cleaning count", f"{n2(fq.n_analytic, 0)} (933/401)", n2(mq.n_analytic, 0), "Locked with stratified 70/30 golden/test split (seed = 42)"],
        ],
        note="IQR = interquartile range. Zero duplicate dialogue IDs or empty utterances occurred in either cleaned corpus.",
        widths=[1.30, 0.95, 1.05, 0.80, 0.65, 1.75],
        align=["l", "l", "l", "c", "c", "l"],
        split=True,
    )

    D.heading("Database Setup, Vector Indexing, and Data Access", 2)
    D.para(
        "To support reproducible offline experimentation and sub-millisecond online retrieval, the data layer is "
        "organized into a four-component storage architecture accessed via typed Python loaders (<i>src/ingestion.py</i>, "
        "<i>src/final_pipeline/common.py</i>, and <i>src/final_pipeline/routing.py</i>):"
    )
    D.items([
        "<b>Canonical Document Database (JSON Lines [JSONL] & Pydantic):</b> Raw JSON corpora are normalized into a two-tier "
        "<i>Pydantic</i> 2.9 schema (<i>src/canonical_schema.py</i>) and persisted as line-delimited JSON "
        "(<i>data/canonical/canonical_corpus.jsonl</i>) alongside indexed tabular views (<i>data/interim/frames_clean.csv</i> "
        "and <i>multiwoz_clean.csv</i>). Tier 1 stores nine core travel slots (origin city, destination city, departure "
        "date, return date, duration in nights, adult count, child count, budget in United States dollars [USD], and "
        "accommodation star tier), and Tier 2 stores five enterprise policy attributes (visa lead window in days, "
        "passport expiry in months, package class [Free Independent Traveler (FIT) vs. Group], room-sharing basis, and "
        "promotional discount percentage).",
        "<b>Partitioned Vector Database (FAISS IndexFlatIP):</b> Dense embedding matrices are stored as memory-mapped "
        "NumPy arrays (<i>data/interim/*.npy</i> and content-addressed SHA-1 caches in <i>data/embeddings/gemini/cache/</i>). "
        "At runtime, <i>RefinedArchetypeRouter</i> indexes L2-normalized 46-dimensional <i>Blocks</i> vectors from "
        "successful golden-partition dialogues into one global baseline index and three archetype-partitioned "
        "<i>faiss.IndexFlatIP</i> inner-product sub-indices (<i>Decisive Booker</i>, <i>Open Explorer</i>, and "
        "<i>Rigid-Constraint Seeker</i>), executing exact cosine nearest-neighbor exemplar lookup in under 2 ms.",
        "<b>Declarative Policy Store & Session State Ledger:</b> Enterprise business rules are externalized in a "
        "version-controlled YAML database (<i>rules/rules_enterprise.yaml</i>) evaluated deterministically by "
        "<i>DeclarativeRuleEngine</i> (<i>src/rule_engine.py</i>). Active multi-turn sessions maintain a structured "
        "<i>Verified Informed Slot Ledger</i> in memory (or Redis in production) paired with content-addressed "
        "JSONL response caches (<i>data/final/*.jsonl</i>) that guarantee 100% deterministic replay.",
    ], numbered=True)
    D.para(
        f"<i>Data splitting procedure.</i> To prevent any information leakage between archetype discovery and downstream "
        f"evaluation, the {n2(fq.n_analytic, 0)} analytic Frames dialogues were partitioned once prior to modeling "
        f"(random seed = 42, stratified on binary wizard task completion) into a <b>70% golden discovery and training "
        f"partition (<i>D</i><sub>gold</sub>, <i>n</i> = {s1['n_gold']})</b> and a <b>30% held-out test partition "
        f"(<i>D</i><sub>test</sub>, <i>n</i> = {s1['n_test']})</b>. Every unsupervised and supervised parameter, including "
        "<i>StandardScaler</i> means and variances, 20-component Gemini principal component analysis (PCA) projection "
        "matrices, <i>K</i>-Means cluster centroids, L2 multinomial logistic regression router weights, FAISS exemplar "
        "pools, and target archetype word-length norms, was fitted strictly on <i>D</i><sub>gold</sub>. The held-out "
        "partition <i>D</i><sub>test</sub> was accessed exclusively for out-of-sample prefix routing evaluation (RQ1) and "
        "downstream prompting and simulation experiments (RQ2–RQ4)."
    )

    D.heading("Exploratory Data Analysis", 2)
    D.heading("Univariate and Outcome-Stratified Analysis", 3)
    b_st = eda_ext["budget_stats"]
    bal = eda_ext["balance_checks"]
    out_an = eda_ext["outcome_anova"]
    D.para(
        f"Table 6 and Figure 1 summarize the univariate distributions across corpora, partitions, commercial trip "
        f"attributes, and session outcomes. Microsoft Frames and MultiWOZ 2.2 exhibit comparable mean conversation "
        f"lengths (<i>M</i> = {n2(fd.turns_M)} vs. {n2(md.turns_M)} turns; Panel A), but Frames displays substantially "
        f"wider standard deviation dispersion (<i>SD</i> = {n2(fd.turns_SD)} vs. {n2(md.turns_SD)}, range 3–48 vs. 4–32 "
        f"turns) and higher assistant verbosity (<i>M</i> = {n2(fd.agent_words_M, 1)} vs. {n2(md.agent_words_M, 1)} "
        "words/turn; Panel B), reflecting complex multi-package comparisons. Covariate balance checks between "
        f"<i>D</i><sub>gold</sub> (<i>n</i> = {s1['n_gold']}) and <i>D</i><sub>test</sub> (<i>n</i> = {s1['n_test']}) "
        f"confirm zero statistically significant differences across dialogue turns (<i>t</i> = {n2(bal['total_turns']['t'])}, "
        f"<i>p</i> = {nz(bal['total_turns']['p'], 3)}), slot revisions (<i>t</i> = {n2(bal['revisions_count']['t'])}, "
        f"<i>p</i> = {nz(bal['revisions_count']['p'], 3)}), package offers (<i>t</i> = {n2(bal['agent_offers']['t'])}, "
        f"<i>p</i> = {nz(bal['agent_offers']['p'], 3)}), user words per turn (<i>p</i> = {nz(bal['mean_user_words']['p'], 3)}), "
        f"or behavioral ratings (<i>p</i> ≥ {nz(min(bal['decisiveness']['p'], bal['exploration_breadth']['p']), 3)}). "
        f"Across stated numeric trip budgets in Frames (<i>n</i> = {b_st['n']}; Figure 1, Panel C), budgets span "
        f"${n2(b_st['min'], 0)} to ${n2(b_st['max'], 0)} USD with a right-skewed mean of <b>${n2(b_st['M'], 0)}</b> "
        f"(<i>SD</i> = ${n2(b_st['SD'], 0)}) and median of <b>${n2(b_st['Mdn'], 0)}</b> (interquartile range [IQR] = "
        f"${n2(b_st['IQR'], 0)}). "
        f"Traveler parties average {n2(eda_ext['adults_M'])} adults (<i>SD</i> = {n2(eda_ext['adults_SD'])}; solo = "
        f"{pct(eda_ext['party_pct']['solo'])}, group = {pct(eda_ext['party_pct']['group'])}, family = "
        f"{pct(eda_ext['party_pct']['family'])}, couple = {pct(eda_ext['party_pct']['couple'])}), and post-chat user "
        f"satisfaction averages {n2(eda_ext['user_rating_M'])}/5.0 (<i>SD</i> = {n2(eda_ext['user_rating_SD'])}, "
        f"<i>n</i> = {eda_ext['user_rating_n']}). Canonical slot completeness (Appendix E, Table E1 and Figure E1) "
        "exceeds 70%–99% for core Tier-1 slots in Frames (origin 99.3%, destination 99.0%, departure date 85.0%, "
        "budget 73.1%, hotel tier 72.9%) but is <b>0.0%</b> for Tier-2 visa, passport, and discount rules in both "
        "archival corpora, directly motivating controlled Tier-2 state injection in RQ3."
    )
    D.para(
        "Crucially, stratifying the Frames corpus by session outcome (Table 6, bottom rows; Figure 1, Panel D) reveals "
        "two distinct negotiation failure modes across <i>Booked Package</i> (65.6%, <i>n</i> = 875), <i>No Suitable "
        "Option</i> (28.1%, <i>n</i> = 375), and <i>Undecided / Left</i> (6.2%, <i>n</i> = 83). One-way ANOVA and "
        "Kruskal–Wallis tests confirm highly significant differences across outcomes in total turns "
        f"(<i>F</i>(2, 1330) = {n2(out_an['total_turns']['F'])}, <i>p</i> < .001), slot revisions (<i>F</i> = "
        f"{n2(out_an['revisions_count']['F'])}, <i>p</i> < .001), package offers (<i>F</i> = "
        f"{n2(out_an['agent_offers']['F'])}, <i>p</i> < .001), destination flexibility (<i>F</i> = "
        f"{n2(out_an['destination_flexibility']['F'])}, <i>p</i> < .001), exploration breadth (<i>F</i> = "
        f"{n2(out_an['exploration_breadth']['F'])}, <i>p</i> < .001), and decisiveness (<i>F</i> = "
        f"{n2(out_an['decisiveness']['F'])}, <i>p</i> < .001). Specifically, <i>No Suitable Option</i> sessions "
        "involve rigid, low-flexibility shoppers (destination flexibility = 2.18 vs. 2.77 for booked) who receive only "
        "<b>1.03 package offers</b> before hitting an impasse at 10.23 turns, whereas <i>Undecided / Left</i> sessions "
        "involve high-exploration, low-decisiveness shoppers (exploration = 2.69, decisiveness = 2.35 vs. 3.71 for "
        "booked) who churn through 17.00 revisions and 3.87 offers without closing, directly motivating persona-specific "
        "trade-off and comparison policies."
    )
    desc_rows = [
        [
            r.corpus, n2(r.N, 0), f"{n2(r.turns_M)} ({n2(r.turns_SD)})", n2(r.turns_Mdn, 0),
            f"{int(r.turns_min)}–{int(r.turns_max)}", n2(r.user_words_M, 1), n2(r.agent_words_M, 1),
            "N/A" if pd.isna(r.success_pct) else f"{n2(r.success_pct, 1)}%",
        ]
        for _, r in desc.iterrows()
    ]
    for _, orow in t_out.iterrows():
        desc_rows.append([
            f"Frames Outcome: {orow.outcome_label}",
            f"{int(orow.n)} ({n2(orow.pct, 1)}%)",
            f"{n2(orow.turns_M)} ({n2(orow.turns_SD)})",
            f"Rev: {n2(orow.revisions_M, 1)}",
            f"Off: {n2(orow.offers_M, 2)}",
            f"Flex: {n2(orow.dest_flex_M)}",
            f"Dec: {n2(orow.decisive_M)}",
            f"${n2(orow.budget_Mdn, 0)}",
        ])
    D.table(
        "Univariate and Outcome-Stratified Descriptive Statistics of the Analytic Samples",
        ["Sample or outcome stratum", "<i>N</i> (%)", "Turns <i>M</i> (<i>SD</i>)", "<i>Mdn</i> / Rev.", "Range / Offers", "User wds / Flex.", "Agent wds / Dec.", "Success / Budget"],
        desc_rows,
        note="Top four rows report corpus/partition distributions (user/agent words per turn and wizard task success %). Bottom three rows report Frames outcome strata (<i>N</i> = 1,333 excluding 1 unclear session): Rev. = mean slot revisions; Offers = mean package offers; Flex. = destination flexibility (1–5); Dec. = decisiveness (1–5); Budget = median stated budget (USD).",
        widths=[1.85, 0.78, 0.92, 0.65, 0.65, 0.55, 0.55, 0.55],
        align=["l", "c", "c", "c", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "Univariate Dialogue Length, Utterance Length, Stated Trip Budget, and Session Outcome Dynamics",
        os.path.join(FIG_FIN, "fig_eda_turns.png"),
        note=f"Frames <i>N</i> = {n2(fq.n_analytic, 0)} (stated budgets <i>n</i> = {b_st['n']}); MultiWOZ 2.2 <i>N</i> = {n2(mq.n_analytic, 0)}.",
    )

    D.heading("Bivariate Analysis", 3)
    b0, b1, b3, b4, b5, b8 = (t_biv.iloc[i] for i in (0, 1, 3, 4, 5, 8))
    D.para(
        "Parametric (Pearson <i>r</i>) and non-parametric (Spearman ρ) bivariate correlations across all "
        f"{n2(fq.n_analytic, 0)} Frames dialogues (Table 7; Figure 2) demonstrate that conversation length is heavily "
        f"driven by cumulative slot revisions (<i>r</i> = {nz(b0.pearson_r)}, ρ = {nz(b0.spearman_rho)}, <i>p</i> < "
        f".001; Panel A) and assistant package offers (<i>r</i> = {nz(b1.pearson_r)}, ρ = {nz(b1.spearman_rho)}, "
        "<i>p</i> < .001). Cross-checking structural dialogue counts against the opening LLM behavioral ratings "
        "establishes strong construct validity: slot revisions correlate positively with exploration breadth "
        f"(<i>r</i> = {nz(b3.pearson_r)}, ρ = {nz(b3.spearman_rho)}, <i>p</i> < .001), user words per turn correlate "
        f"positively with upfront information provision (<i>r</i> = {nz(b5.pearson_r)}, ρ = {nz(b5.spearman_rho)}, "
        f"<i>p</i> < .001), and user decisiveness correlates negatively with dialogue length (<i>r</i> = "
        f"{nz(b4.pearson_r)}, ρ = {nz(b4.spearman_rho)}, <i>p</i> < .001) and positively with package booking "
        f"completion (<i>r</i> = {nz(b8.pearson_r)}, ρ = {nz(b8.spearman_rho)}, <i>p</i> < .001). Across archetypes "
        "(Figure 2, Panel B), <i>Open Explorers</i> average 24.9 slot revisions and 5.0 package offers per session, "
        "whereas <i>Rigid-Constraint Seekers</i> average only 7.7 revisions and 1.3 offers."
    )
    biv_rows = [
        [r.pair_label, nz(r.pearson_r, 3), pv_cell(r.pearson_p), nz(r.spearman_rho, 3), pv_cell(r.spearman_p)]
        for _, r in t_biv.iterrows()
    ]
    D.table(
        "Bivariate Parametric and Non-Parametric Correlations of Dialogue Dynamics (Frames, N = 1,334)",
        ["Variable pair", "Pearson <i>r</i>", "<i>p</i> (Pearson)", "Spearman ρ", "<i>p</i> (Spearman)"],
        biv_rows,
        widths=[3.10, 0.85, 0.85, 0.85, 0.85],
        align=["l", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "Bivariate Relationships Between Dialogue Length, Slot Revisions, and Archetype Negotiation Intensity",
        os.path.join(FIG_FIN, "fig_eda_bivariate.png"),
        note="Panel A: Dialogue turns vs. slot revisions with OLS regression trend. Panel B: Mean revisions and package offers by refined archetype (error bars = 95% confidence interval [CI]).",
    )

    D.heading("Multivariate Analysis", 3)
    pve = eda_ext["pca_var_explained"]
    D.para(
        "Multivariate structure across ten structural and behavioral variables was analyzed via Spearman rank "
        "correlation and principal component analysis (PCA; Figure 3; full component loadings in Appendix E, Table E2). "
        f"The first three principal components account for {pct(100 * sum(pve), 1)} of total variance: PC1 "
        f"({pct(100 * pve[0], 1)}) represents an <i>Exploration vs. Constraint Rigidity</i> axis loaded on slot "
        "revisions (.42), total turns (.39), exploration breadth (.39), and question asking (.34); PC2 "
        f"({pct(100 * pve[1], 1)}) represents a <i>Decisiveness and Politeness</i> axis (−.51, −.46); and PC3 "
        f"({pct(100 * pve[2], 1)}) isolates <i>User Utterance Verbosity</i> (.89). Projecting dialogues onto the "
        "(PC1, PC2) plane (Figure 3, Panel B) confirms that the three refined archetypes occupy distinct regions of a "
        "continuous behavioral manifold rather than isolated clusters. <b><i>EDA → RQ1-Identify & RQ3-Govern stage "
        "handoff (dropped vs. carried forward):</i></b> Because whole-dialogue turn counts, cumulative revisions, and "
        "end-of-session booking outcomes are endogenous consequences of negotiation failure rather than observable at "
        "session start, they are <b>dropped</b> as clustering inputs to prevent circular outcome confounding; instead, "
        "opening-prefix utterance representations (<i>M</i> ≤ 9 user messages) and non-outcome behavioral scales are "
        "<b>carried forward into the RQ1-Identify stage</b>, while controlled Tier-2 policy state injection is "
        "<b>carried forward into the RQ3-Govern stage</b> to overcome the 0.0% archival Tier-2 slot coverage."
    )
    D.figure(
        "Multivariate Spearman Correlation Matrix and Principal Component Biplot of Behavioral Features",
        os.path.join(FIG_FIN, "fig_eda_multivariate.png"),
        note="Panel A: 10 × 10 Spearman rank correlation matrix. Panel B: PCA biplot colored by refined archetype with top loading vectors.",
    )

    D.heading("Research Design, Hypotheses, and Sample Size Justification", 2)
    D.para(
        "All four research questions are evaluated at a two-tailed significance level of <b>α = .05</b> against the "
        "formal null (<i>H</i><sub>01</sub>–<i>H</i><sub>04</sub>) and alternative (<i>H</i><sub>a1</sub>–<i>H</i><sub>a4</sub>) "
        "hypotheses specified in Table 1. Minimum sample sizes were derived a priori using Cohen's medium effect size "
        "<i>f</i> = .25 (Cohen, 1988), α = .05, and target statistical power 1 − β ≥ .80 via the noncentral <i>F</i> "
        "distribution (Faul et al., 2007):",
        keep_next=True,
    )
    D.equation(
        "1 − β = 1 − <i>F</i><sub>nc</sub>(<i>F</i><sub>crit</sub>; <i>df</i><sub>1</sub>, "
        "<i>df</i><sub>2</sub>, λ),   <i>F</i><sub>crit</sub> = <i>F</i><sub>1−α</sub>"
        "(<i>df</i><sub>1</sub>, <i>df</i><sub>2</sub>)",
        "1",
    )
    D.para(
        "where λ = <i>f</i><sup>2</sup><i>N</i> for between-subjects designs (RQ1, RQ3, RQ4) and λ = "
        "<i>f</i><sup>2</sup><i>Nm</i>ε / (1 − ρ) for repeated-measures RQ2 (<i>m</i> = 3 conditions, ρ = .50, ε = 1.0). "
        "Table 8 reports the exact degrees of freedom, noncentrality parameter λ, critical value <i>F</i><sub>crit</sub>, "
        "minimum sample size <i>N</i><sub>min</sub>, and buffered balanced sample size <i>N</i><sub>final</sub> "
        "(achieving actual power of .805–.878). Crucially, these computed sample sizes directly justify how the "
        f"collected corpus volume (<i>N</i> = {n2(fq.n_analytic, 0)} analytic Frames dialogues) is allocated across "
        "the four stages: (1) in the <b>RQ1-Identify</b> stage, <i>N</i><sub>min</sub> = 159 evaluations across 3 "
        f"algorithms is satisfied by drawing 53 matched subsamples of <i>n</i> = 500 dialogues from <i>D</i><sub>gold</sub> "
        f"(<i>n</i> = {s1['n_gold']}, a 53.6% finite-population fraction paired with matched repeated-measures ANOVA and "
        "Friedman tests across the 53 shared seeds); (2) in the <b>RQ2-Personalize</b> stage, <i>N</i><sub>min</sub> = 28 "
        "repeated-measures subjects is exceeded by sampling <i>N</i><sub>final</sub> = 33 stratified held-out dialogues "
        "from <i>D</i><sub>test</sub> (11 per archetype × 3 conditions = 99 generations); (3) in the <b>RQ3-Govern</b> "
        "stage, <i>N</i><sub>min</sub> = 128 evaluations for a 1-<i>df</i> numerator effect in a 2 × 2 design is exceeded "
        "by evaluating <i>N</i><sub>final</sub> = 144 units (36 stratified held-out dialogues, comprising 18 policy-violating "
        "and 18 compliant cases at 12 per archetype, tested across all four cells, <i>n</i> = 36/cell); and (4) in the <b>RQ4-Optimize</b> "
        "stage, <i>N</i><sub>min</sub> = 158 episodes for a 2-<i>df</i> prompting × archetype interaction in a 2 × 3 "
        "design is exceeded by allocating <b><i>N</i><sub>final</sub> = 180 distinct, non-overlapping held-out seed "
        "dialogues</b> from <i>D</i><sub>test</sub> (<i>n</i> = 401; 60 per archetype, partitioned into <i>n</i> = 30 "
        "unique dialogues for <i>Zero-Shot</i> and <i>n</i> = 30 unique dialogues for <i>Cluster-Adaptive Few-Shot</i>), "
        "ensuring strict between-subjects independence (<i>df</i><sub>error</sub> = 174).",
        indent=False,
    )
    ss_rows = [
        [
            rq, ss.loc[rq].Design.replace(" x ", " × "), f"{int(ss.loc[rq].df1)}, {int(ss.loc[rq].df2_at_Nmin)}",
            n2(ss.loc[rq].lambda_at_Nmin, 2), n2(ss.loc[rq].F_crit, 2), str(int(ss.loc[rq].N_min)),
            nz(ss.loc[rq].power_at_Nmin, 3), f"{int(ss.loc[rq].N_final)} ({int(ss.loc[rq].per_group)})",
            nz(ss.loc[rq].power_final, 3),
        ]
        for rq in ["RQ1", "RQ2", "RQ3", "RQ4"]
    ]
    D.table(
        "Sample Size and Noncentral-F Power Calculations Matched to Each Planned Analysis",
        ["RQ", "Planned experimental design", "<i>df</i> at <i>N</i><sub>min</sub>", "λ", "<i>F</i><sub>crit</sub>", "<i>N</i><sub>min</sub>", "Power", "<i>N</i><sub>final</sub> (per cell)", "Final power"],
        ss_rows,
        note="Computed for medium effect size <i>f</i> = .25 at α = .05 and target power 1 − β ≥ .80 (<i>src/final_pipeline/step0_sample_size.py</i>).",
        widths=[0.42, 1.78, 0.65, 0.50, 0.50, 0.50, 0.55, 0.95, 0.65],
        align=["l", "l", "c", "c", "c", "c", "c", "c", "c"],
        split=True,
    )

    D.heading("Model Selection, Feature Importance Assessment, and Evaluation Metrics", 2)
    D.para(
        "<i>Model selection justification and hybrid representation (RQ1-Identify stage).</i> Three clustering families "
        "representing distinct geometric assumptions were selected for benchmarking: centroid-based <i>K</i>-Means (spherical Voronoi "
        "cells guaranteeing 100% point assignment), hierarchical Ward agglomerative clustering (bottom-up variance "
        "minimization), and density-based HDBSCAN (arbitrary-shape density cores with noise rejection). Primary "
        "whole-dialogue vectors pool de-lexicalized turn embeddings <b>e</b><sub><i>t</i></sub> with exponential recency "
        "decay (λ<sub>d</sub> = 0.15):",
        keep_next=True,
    )
    D.equation(
        "<b>v</b> = Σ<sub><i>t</i>=1</sub><sup><i>T</i></sup> <i>w</i><sub><i>t</i></sub><b>e</b><sub><i>t</i></sub>,   "
        "<i>w</i><sub><i>t</i></sub> = exp[−λ<sub>d</sub>(<i>T</i> − <i>t</i>)] / "
        "Σ<sub><i>j</i>=1</sub><sup><i>T</i></sup> exp[−λ<sub>d</sub>(<i>T</i> − <i>j</i>)]",
        "2",
    )
    D.para(
        "To eliminate end-of-dialogue outcome confounding, the refined representation (<i>Blocks</i>) concatenates two "
        "variance-equalized blocks computed strictly on the first <i>M</i> user messages: (1) the top 20 principal "
        "components (<i>PCA-20</i>, fitted on <i>D</i><sub>gold</sub>) of the 3,072-dimensional Gemini embedding "
        "(<i>gemini-embedding-001</i>; Lee et al., 2025), and (2) a standardized 26-column LLM behavioral matrix "
        "encoding 13 clustering fields from the 16-field <i>UserBehaviour</i> schema (ten 1–5 ordinal scales, six "
        "primary-goal indicators, six secondary-goal indicators, and four emotional-tone indicators; three outcome/party "
        "audit fields are excluded from clustering; Appendix C, Tables C1–C2; test–retest weighted κ = "
        f"{nz(min(r1h['reliability'][x] for x in ORDS))}–{nz(max(r1h['reliability'][x] for x in ORDS))}; revision "
        f"criterion correlation ρ = {nz(cv_['revision_tendency~user_revisions']['rho'])}).",
        indent=False,
    )
    D.para(
        "<i>Feature importance assessment and analytical utilization.</i> To state explicitly how feature importance is "
        "assessed and used across the pipeline, every dimension <i>j</i> ∈ {1, ..., 46} of the golden-fitted <i>Blocks</i> "
        "representation is evaluated using three complementary importance metrics (<i>src/final_pipeline/step5_figures_and_eda.py</i>; "
        "results in Table 13 and Figure 6):"
    )
    D.items([
        "<b>Unsupervised Cluster-Discriminative Importance (η<sup>2</sup> and ANOVA <i>F</i> on <i>D</i><sub>gold</sub>):</b> "
        "For each feature <i>j</i>, one-way ANOVA across the three <i>K</i>-Means reference clusters on <i>D</i><sub>gold</sub> "
        "(<i>n</i> = 933) computes the proportion of total variance explained by cluster membership, η<sub><i>j</i></sub><sup>2</sup> "
        "= <i>SS</i><sub>between,<i>j</i></sub> / <i>SS</i><sub>total,<i>j</i></sub>.",
        "<b>Supervised Router Coefficient Norm (‖<b>β</b><sub><i>j</i></sub>‖<sub>2</sub> on <i>D</i><sub>gold</sub>):</b> "
        "In the L2-regularized multinomial logistic regression router (<i>C</i> = 1.0) fitted on standardized golden "
        "features, the Euclidean norm across the three class weight vectors, ‖<b>β</b><sub><i>j</i></sub>‖<sub>2</sub> = "
        "(Σ<sub><i>c</i>=1</sub><sup>3</sup> β<sub><i>c</i>,<i>j</i></sub><sup>2</sup>)<sup>1/2</sup>, quantifies feature "
        "<i>j</i>'s direct leverage on the classification decision boundary at prefix horizons <i>M</i> = 5 and <i>M</i> = 9.",
        "<b>Out-of-Sample Permutation Importance (Δκ on Held-Out <i>D</i><sub>test</sub>):</b> To measure predictive "
        "generalization without training bias, each feature (and each of the four feature blocks: <i>20 Gemini Semantic "
        "PCs</i>, <i>10 Ordinal Behavioral Scales</i>, <i>12 Primary/Secondary Goals</i>, and <i>4 Emotional Tone "
        "Indicators</i>) is randomly permuted 50 times on held-out <i>D</i><sub>test</sub> (<i>n</i> = 401), recording "
        "the mean drop in chance-corrected routing agreement Δκ = κ<sub>baseline</sub> − κ<sub>permuted</sub>.",
    ], numbered=True)
    D.para(
        "These feature importance results are used directly in four analytical decisions: (a) <i>representation pruning "
        "and block weighting (RQ1-Identify stage)</i>, confirming that both the Gemini semantic block (Δκ = .310 at <i>M</i> = 5; "
        ".674 at <i>M</i> = 9) and the LLM behavioral block (Δκ = .215 at <i>M</i> = 5; .394 at <i>M</i> = 9) are "
        "essential while excluding the three outcome/party audit fields prevents target leakage; (b) <i>deterministic "
        "cluster naming (RQ1-Identify stage, Appendix F)</i>, where the top orthogonal behavioral features (<i>exploration_breadth</i> / "
        "<i>destination_flexibility</i>, η<sup>2</sup> = .304/.150, and <i>decisiveness</i>, η<sup>2</sup> = .280) define "
        "the programmatic centroid-labeling rules in Table F1; (c) <i>prefix router calibration (RQ1-Identify → RQ2-Personalize stages)</i>, where "
        "separated training (<i>D</i><sub>gold</sub>), 5-fold cross-validation, and held-out test (<i>D</i><sub>test</sub>) "
        "evaluations verify that high-importance features generalize without overfitting; and (d) <i>persona policy and "
        "simulator design (RQ2-Personalize & RQ4-Optimize stages)</i>, where the highest-η<sup>2</sup> features per cluster parameterize the "
        "assistant's pacing directives and the RQ4 blind persona validation rubric. Tables 9 and 10 define the five "
        "declarative YAML policy rules and all evaluation metrics."
    )
    D.table(
        "Declarative Enterprise Policy Rules Evaluated in RQ3",
        ["Rule ID and name", "Trigger condition", "Required action", "Severity"],
        [
            [
                f"{r['rule_id']}: {r['name']}",
                r["condition"].replace("budget_amount is not None and ", "budget stated; ").replace("==", "=").replace(" and ", "; "),
                r["action"].replace("_", " ").lower(),
                r["severity"].lower(),
            ]
            for _, r in rules.iterrows()
        ],
        widths=[1.90, 2.50, 1.30, 0.80],
        align=["l", "l", "l", "c"],
        split=True,
    )
    D.table(
        "Evaluation Metrics, Mathematical Formulae, and Analytical Interpretation",
        ["Metric", "Mathematical formula", "RQ", "Analytical interpretation"],
        [
            ["Silhouette & DB index", "<i>s</i>(<i>i</i>) = [<i>b</i>(<i>i</i>)−<i>a</i>(<i>i</i>)]/max{<i>a</i>,<i>b</i>}; <i>DB</i> = (1/<i>k</i>)Σ max(σ<sub><i>i</i></sub>+σ<sub><i>j</i></sub>)/<i>d</i>(<b>c</b><sub><i>i</i></sub>,<b>c</b><sub><i>j</i></sub>)", "1", "Higher Silhouette [−1, 1] and lower DB (≥ 0) indicate superior separation"],
            ["ARI, Cohen's κ, & ROC-AUC", "<i>ARI</i> = (<i>RI</i>−E[<i>RI</i>])/(max <i>RI</i>−E[<i>RI</i>]); κ = (<i>p</i><sub>o</sub>−<i>p</i><sub>e</sub>)/(1−<i>p</i><sub>e</sub>); OvR AUC", "1, 3, 4", "Bootstrap stability (ARI ≥ .60), chance-corrected routing/judge κ, & class discrimination"],
            ["Feature importance", "η<sub><i>j</i></sub><sup>2</sup> = <i>SS</i><sub>B,<i>j</i></sub>/<i>SS</i><sub>T,<i>j</i></sub>; ‖<b>β</b><sub><i>j</i></sub>‖<sub>2</sub> = √Σβ<sub><i>c,j</i></sub><sup>2</sup>; Δκ<sub><i>j</i></sub> = κ − κ<sub>perm,<i>j</i></sub>", "1, 2", "Cluster variance explained, router weight magnitude, & held-out permutation κ drop"],
            ["Style cosine & Pacing err.", "cos(<b>r</b>, <b>c</b><sub><i>a</i></sub>) = (<b>r</b>·<b>c</b><sub><i>a</i></sub>)/(‖<b>r</b>‖‖<b>c</b><sub><i>a</i></sub>‖); |<i>W</i><sub>gen</sub> − μ<sub><i>W</i>,<i>a</i></sub>|", "2, 3", "De-lexicalized SBERT structural style cosine and word-count pacing error"],
            ["Rule adherence (RAR)", "Sens. = |<i>R</i><sub>enf</sub> ∩ <i>R</i><sub>viol</sub>|/|<i>R</i><sub>viol</sub>| (<i>n</i>=18/cell); Spec. = 1 − false_block (<i>n</i>=18/cell)", "3", "Decomposed into Violation Enforcement Sensitivity, Compliant Specificity, & Overall"],
            ["Exemplar leakage (ELR)", "|<i>E</i><sub>resp</sub> ∩ (<i>E</i><sub>ex</sub> \\ <i>E</i><sub>diag</sub>)| / max(1, |<i>E</i><sub>resp</sub>|)", "3", "Proportion [0, 1] of response entities leaked from prompt exemplars"],
            ["Slot coverage F<sub>1</sub>", "2 · Precision · Recall / (Precision + Recall) over active state slots", "3", "Proportion [0, 1] of active booking slots grounded in generated response"],
            ["Turns to goal & RER", "TGC = total turns (user + assistant) to [ACCEPT_BOOKING] (min = 5); RER = <i>A</i><sub>red</sub> / <i>A</i><sub>tot</sub>", "4", "Lower total/log conversational turns and lower RER indicate superior turn economy"],
        ],
        note="Parametric ANOVAs are paired with Welch/HC3 robust tests and non-parametric (Kruskal–Wallis, Friedman, Mann–Whitney, ART; Wobbrock et al., 2011) checks.",
        widths=[1.45, 2.85, 0.50, 1.70],
        align=["l", "l", "c", "l"],
        split=True,
    )

    # ================================================================== 4. ARCHITECTURE AND WORKFLOW
    D.heading("Architecture and Workflow", 1)
    D.heading("System Overview", 2)
    D.para(
        "The proposed neuro-symbolic conversational system is structured as an end-to-end seven-stage pipeline that "
        "strictly separates offline discovery and training on the golden partition (<i>D</i><sub>gold</sub>, "
        f"<i>n</i> = {s1['n_gold']}) from online adaptive inference, policy governance, and evaluation on the held-out "
        f"test partition (<i>D</i><sub>test</sub>, <i>n</i> = {s1['n_test']}). The purpose of the pipeline is to "
        "resolve the core trade-off identified in the research problem: adapting assistant style and recommendation "
        "pacing to heterogeneous traveler archetypes early in a conversation while guaranteeing zero exemplar entity "
        "leakage, deterministic booking-policy compliance, and minimal turns to quotation agreement."
    )

    D.heading("Architecture Diagram", 2)
    D.para(
        "As shown in Figure 4, the system architecture progresses through seven explicit stages: (1) <i>Data Stage</i>, "
        "(2) <i>Preprocessing Stage</i>, (3) <i>Exploratory Data Analysis (EDA) Stage</i>, (4) <i>Feature Engineering "
        "Stage</i>, (5) <i>Model Stage</i>, (6a/6b) <i>Policy Guardrail and Evaluation Stage</i>, and (7) <i>Deployment "
        "Stage</i>, with color-coded functional legends distinguishing data processing, EDA, feature engineering, "
        "modeling, symbolic verification, and production serving. Figure 5 details the corresponding four-step "
        "experimental execution workflows for RQ1 (Panel A), RQ2 (Panel B), RQ3 (Panel C), and RQ4 (Panel D)."
    )
    D.figure(
        "End-to-End Neuro-Symbolic Cluster-Adaptive System Architecture Across All Seven Pipeline Blocks",
        os.path.join(FIG_FIN, "fig_system_architecture.png"),
        note="Pipeline blocks (1)–(4) execute offline on the golden discovery partition (<i>D</i><sub>gold</sub>, <i>n</i> = 933); pipeline blocks (5)–(7) execute online on held-out test dialogues (<i>D</i><sub>test</sub>, <i>n</i> = 401) and in production deployment.",
    )
    D.figure(
        "Algorithmic Execution Workflows Across Research Questions RQ1 to RQ4",
        os.path.join(FIG_FIN, "fig_rq_workflows_4panel.png"),
        note="Step-by-step experimental pipelines and statistical hypothesis tests for RQ1 (Panel A), RQ2 (Panel B), RQ3 (Panel C), and RQ4 (Panel D).",
    )

    D.heading("Workflow Components", 2)
    D.lead_para(
        "Data ingestion",
        "Raw JSON dialogue archives from Microsoft Frames (1,369 dialogues) and MultiWOZ 2.2 (1,500 seeded travel "
        "dialogues) are ingested by <i>src/ingestion.py</i>, which parses turn-level speaker tags, utterances, dialogue "
        "acts, and belief-state slot dictionaries into validated two-tier <i>Pydantic</i> objects stored in "
        "<i>data/canonical/canonical_corpus.jsonl</i>.",
    )
    D.lead_para(
        "Data preprocessing, scaling, and encoding",
        "In <i>src/final_pipeline/step1_prepare_data.py</i> and <i>step2f_rq1_llm_hybrid.py</i>, utterance texts are "
        "de-lexicalized via slot-value regular expressions that replace specific city names, dates, star ratings, and "
        "dollar amounts with generic <i>[SLOT]</i> tokens. Numerical scaling and categorical encoding follow a strict "
        "leakage-free protocol fitted on <i>D</i><sub>gold</sub>: (a) 384-d Sentence-BERT and 3,072-d Gemini embedding "
        "vectors are L2 unit-norm scaled; (b) the 20 Gemini principal components (<i>PCA-20</i>) are centered and "
        "projected using golden-partition eigenvectors; (c) the ten 1–5 ordinal LLM behavioral scales are standardized "
        "to zero mean and unit variance via <i>StandardScaler</i> fitted on <i>D</i><sub>gold</sub>; (d) categorical "
        "behavioral fields are one-hot or multi-hot encoded into 16 binary columns (6 <i>primary_goal</i>, 6 "
        "<i>secondary_goals</i>, and 4 <i>emotional_tone</i> indicators); and (e) in the <i>Blocks</i> transformer, the "
        "20-d semantic block and 26-d behavioral block are each scaled by the inverse square root of their golden "
        "block trace variance so both modalities contribute exactly equal total variance prior to L2 row normalization.",
    )
    D.lead_para(
        "Missing value and outlier handling",
        "Unobserved optional trip and policy slots (such as <i>traveler_count_children</i> or Tier-2 visa/passport "
        "fields in archival sessions) represent genuine conversational state absence and are preserved as explicit "
        "<i>None</i> values in the Pydantic schema rather than imputed, preventing fabricated customer constraints. "
        "Missing post-session user ratings (3 analytic Frames dialogues) are retained in clustering and excluded only "
        "from rating correlations. Degenerate fragments with fewer than 3 turns (34 in Frames; 1 in MultiWOZ) are "
        "removed during cleaning. Upper-tail turn-length outliers exceeding <i>Q</i><sub>3</sub> + 1.5 × IQR (> 29.5 "
        "turns in Frames, <i>n</i> = 30 [2.2%]; > 28.0 turns in MultiWOZ, <i>n</i> = 8 [0.5%]) are retained as "
        "authentic complex negotiations; to prevent positive skewness from biasing parametric inference, turn counts "
        "are natural-log transformed (ln TGC) in RQ4 and paired with rank-based Kruskal–Wallis, Friedman, Mann–Whitney "
        "<i>U</i>, and ART tests across all research questions.",
    )
    D.lead_para(
        "Exploratory data analysis and feature engineering",
        "Univariate, outcome-stratified, bivariate, and multivariate PCA diagnostics (Tables 6–7, Figures 1–3) "
        "characterize negotiation bottlenecks and motivate combining opening user prefix embeddings (<i>M</i> ≤ 9 "
        "user messages) with the 16-field LLM behavioral codebook (<i>step2e_llm_user_annotation.py</i>). Feature "
        "importance is then quantified via golden cluster η<sup>2</sup>, standardized router coefficient norms "
        "‖<b>β</b><sub><i>j</i></sub>‖<sub>2</sub>, and held-out permutation Δκ (Table 13, Figure 6).",
    )
    D.lead_para(
        "Model development, evaluation, and deployment",
        "Offline model development in the <b>RQ1-Identify</b> stage fits <i>K</i>-Means (<i>k</i> = 3), Ward, and "
        "HDBSCAN across 159 resampling runs, locks the three 46-d <i>Blocks</i> reference centroids and FAISS "
        "<i>IndexFlatIP</i> sub-indices on <i>D</i><sub>gold</sub>, and trains L2-regularized multinomial logistic "
        "prefix routers (<i>C</i> = 1.0) verified via 5-fold stratified cross-validation (CV) on <i>D</i><sub>gold</sub> "
        "and out-of-sample testing on <i>D</i><sub>test</sub>. Online evaluation executes the <b>RQ2-Personalize</b> "
        "repeated-measures prompting harness, the <b>RQ3-Govern</b> 2 × 2 rule-governance harness (cross-checked by an "
        "independent <i>gemini-2.5-pro</i> judge), and the <b>RQ4-Optimize</b> 2 × 3 closed-loop turn-economy simulator, "
        "which packages into a stateless Python/FastAPI and Redis microservice for live OTA chat gateways.",
    )

    D.heading("Tools and Technologies", 2)
    D.para(
        "The experimental pipeline and report automation suite are implemented in Python 3.11 on an Apple M-series "
        "workstation (8-core central processing unit [CPU], 16 gigabytes [GB] unified memory) paired with Google Cloud "
        "tensor and graphics processing unit (TPU/GPU) inference via the official <i>google-genai</i> software "
        "development kit (SDK). Data manipulation and schema validation use "
        "<i>pandas</i> 2.2, <i>numpy</i> 1.26, and <i>pydantic</i> 2.9. Deep learning embeddings and contextual scoring "
        "use <i>sentence-transformers</i> (<i>all-MiniLM-L6-v2</i>), PyTorch 2.4, and <i>gemini-embedding-001</i>; "
        "generative experiments and independent validation audits use <i>gemini-2.5-flash</i> and <i>gemini-2.5-pro</i>; "
        "and vector indexing uses <i>faiss-cpu</i> 1.8. Unsupervised clustering and manifold projection use "
        "<i>scikit-learn</i> 1.5 (Pedregosa et al., 2011), <i>hdbscan</i> (McInnes et al., 2017), and <i>umap-learn</i> "
        "(McInnes et al., 2018). Parametric OLS, Greenhouse–Geisser RM-ANOVA, White/MacKinnon HC3 "
        "heteroscedasticity-consistent standard errors, and Aligned Rank Transform (ART) factorial models are computed "
        "using <i>scipy.stats</i> 1.14 and <i>Statsmodels</i> 0.14 (Seabold & Perktold, 2010), while publication figures "
        "and American Psychological Association Seventh Edition (APA 7) Word and Portable Document Format (PDF) "
        "compilation use <i>matplotlib</i> 3.9, <i>python-docx</i>, and <i>PyMuPDF</i>."
    )
