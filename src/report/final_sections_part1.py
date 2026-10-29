"""
Part 1 of the QM640 Final Report builder (calibrated for <= 30 core pages, zero markdown artifacts, strict APA 7):
  - Front Matter (Title Page, GitHub Repository, Table of Contents)
  - Abstract (1 page, ~320 words)
  - Section 1: Introduction (Background, Business/Technical/Measurable Problem Statement, Purpose & RQs Table 1, Contributions)
  - Section 2: Literature Review (Approach, Relevance Matrix Table 2, Business & Technical Synthesis, Research Gaps)
  - Section 3: Materials and Methods (Data Sources Table 3, Data Dictionary Table 4, Cleaning Log Table 5, Univariate/Bivariate/Multivariate EDA Tables 6–7 & Figures 1–3, Power Analysis Eq. 1 & Table 8, Models & Metrics Eq. 2 & Tables 9–10)
  - Section 4: Architecture and Workflow (System Architecture Figure 4, Per-RQ Workflows Figure 5, Pipeline Components & Tech Stack)
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
    r4_rer_p = r4_fin["anova"]["rer"]["effects"]["prompt_mode"]

    # ------------------------------------------------------------------ Title Page
    D.title_page(
        [TITLE, "Final Report"],
        [
            "Surnella Sandeep",
            "Department of Data Analytics, Walsh College",
            "QM640: Data Analytics Capstone",
            "Mr. Smitraj Raut",
            "October 28, 2026",
        ],
    )

    # ------------------------------------------------------------------ Repository + TOC
    D.para(f"<b>GitHub repository:</b> {REPO}", indent=False)
    D.toc(toc_pages[0] if toc_pages else [], toc_pages[1] if toc_pages else None)

    # ================================================================== ABSTRACT
    D.heading("Abstract", 1)
    abstract_text = (
        "Online travel agencies increasingly deploy large language model (LLM) assistants for package booking, "
        "yet static prompts ignore traveler decision-making heterogeneity, while naive few-shot prompting leaks stale "
        "entities and violates booking policies. This study evaluates a neuro-symbolic, cluster-adaptive framework "
        "coupling early-turn behavioral-semantic archetype routing and slot-masked FAISS retrieval with a declarative "
        f"rule engine. Using {n2(ctx['n_frames_raw'], 0)} Microsoft Frames dialogues ({n2(fq.n_analytic, 0)} analytic: "
        f"golden <i>n</i> = {s1['n_gold']}, test <i>n</i> = {s1['n_test']}) and {n2(mq.n_analytic, 0)} MultiWOZ 2.2 "
        "dialogues, four hypotheses were tested with Sentence-BERT, Gemini 3,072-d embeddings, Gemini 2.5 Flash, "
        "and Gemini 2.5 Pro. For RQ1, clustering algorithms differed across 159 runs, "
        f"<i>F</i>(2, 156) = {n2(an1['F'])}, <i>p</i> < .001, η<sup>2</sup> = {nz(an1['eta2'])}, and combining Gemini "
        "prefix embeddings with a 16-field behavioral profile on the first nine user messages yielded three stable "
        "refined archetypes—<i>Decisive Booker</i>, <i>Open Explorer</i>, and <i>Rigid-Constraint Seeker</i> "
        f"(ARI = .76; held-out routing κ = {nz(rt_diag.loc[5, 'cohen_kappa'], 3)} at "
        f"<i>M</i> = 5 to {nz(rt_diag.loc[9, 'cohen_kappa'], 3)} at <i>M</i> = 9). For RQ2 (<i>N</i> = {r2_ref['N']} "
        f"repeated-measures), cluster-adaptive prompting increased style convergence, <i>F</i>({n2(r2_sa['df1_gg'])}, "
        f"{n2(r2_sa['df2_gg'])}) = {n2(r2_sa['F'])}, <i>p</i> < .001, η<sub><i>p</i></sub><sup>2</sup> = "
        f"{nz(r2_sa['eta2_partial'])}, and cut pacing error to "
        f"{n2(r2_ref['results']['word_abs_err']['desc']['Cluster-Adaptive Few-Shot'][0])} words, <i>F</i> = "
        f"{n2(r2_we['F'])}, <i>p</i> {pv(r2_we['p_gg'])}. For RQ3 (<i>N</i> = {r3_fin['N']} 2 × 2 factorial; "
        f"dual-judge κ = {nz(r3_fin['judge_reliability_flash_vs_pro']['cohen_kappa'], 3)}), active rules raised "
        f"violation enforcement from 5.6% to 98.6%, <i>F</i>(1, 140) = {n2(r3_rar_a['F'])}, <i>p</i> < .001, "
        f"eliminated 35.9% entity leakage to 0.0%, interaction <i>F</i>(1, 140) = {n2(r3_elr_i['F'])}, "
        f"<i>p</i> < .001, and raised slot F<sub>1</sub> to .952, <i>F</i>(1, 140) = {n2(r3_sf1_a['F'])}, <i>p</i> < "
        f".001. For RQ4 (<i>N</i> = {r4_fin['N']} 2 × 3 simulation; persona κ = "
        f"{nz(r4_fin['persona_validation']['cohen_kappa'], 3)}), cluster-adaptive prompting cut turns by "
        f"29.5%–42.7%, <i>F</i>(1, 174) = {n2(r4_lt_p['F'])}, <i>p</i> < .001, interaction "
        f"<i>F</i>(2, 174) = {n2(r4_lt_i['F'])}, <i>p</i> < .001, and eliminated redundant slot elicitation, "
        f"<i>F</i>(1, 174) = {n2(r4_rer_p['F'])}, <i>p</i> < .001."
    )
    D.para(abstract_text, indent=False)
    D.para(
        "<i>Keywords:</i> conversational AI, travel chatbots, trajectory clustering, few-shot learning, guardrails",
        indent=True,
    )

    # ================================================================== 1. INTRODUCTION
    D.heading("Introduction", 1, new_page=True)
    D.heading("Background and Context", 2)
    D.para(
        "Conversational artificial intelligence (AI) assistants have become a core digital channel in travel, "
        "tourism, and hospitality, supporting destination discovery, package comparison, and itinerary booking "
        "(Buhalis & Sinarta, 2019; Ivanov & Webster, 2019; Jannach et al., 2021). Unlike single-turn question "
        "answering, vacation package booking is a consultative, multi-turn negotiation in which travelers balance "
        "competing constraints across origin, destination, dates, duration, hotel tier, and budget (El Asri et al., "
        "2017). Empirical analyses of human travel dialogues demonstrate that travelers converse in distinct "
        "behavioral styles: some state fixed parameters up front and seek immediate confirmation, others explore "
        "multiple destinations and hotel tiers side by side, and others insist on rigid date and luxury constraints "
        "that require proactive trade-off resolution when preferred inventory exceeds their budget ceiling (Inaba "
        "et al., 2022; Melián-González et al., 2021)."
    )
    D.para(
        "Despite this behavioral diversity, commercial large language model (LLM) travel assistants typically use "
        "one static system prompt and a uniform sequential intake script. Asking clarifying questions one slot at a "
        "time or offering a single hotel option per turn creates repetitive turns and session abandonment. "
        "Conversely, adapting an LLM's style purely through in-context few-shot examples introduces two severe "
        "reliability hazards (Liu et al., 2022; Rebedea et al., 2023): first, unmasked retrieved examples cause "
        "factual entity leakage, where the model copies stale hotel names, airfares, or promo codes from the "
        "examples into the active session; second, stylistic prompt instructions compete with business rules, "
        "causing the assistant to overlook mandatory visa windows, passport validity thresholds, party-size limits, "
        "or discount caps (Yao et al., 2024). Resolving both personalization and compliance requires a neuro-symbolic "
        "architecture that decouples behavioral style adaptation from deterministic policy verification."
    )

    D.heading("Problem Statement", 2)
    D.lead_para(
        "Business problem statement",
        "Online travel agencies (OTAs), tour operators, and hospitality contact centers suffer from low self-service "
        "conversion and elevated session abandonment because static conversational assistants fail to adapt their "
        "information density and recommendation strategy to distinct customer decision-making styles, while "
        "unverified generative responses expose enterprises to financial and regulatory liability from booking "
        "policy violations and hallucinated package terms (Buhalis & Sinarta, 2019; Ivanov & Webster, 2019; "
        "Melián-González et al., 2021).",
    )
    D.lead_para(
        "Technical problem statement",
        "Existing LLM dialogue systems lack (a) an empirically validated representation for clustering multi-turn "
        "user behavior into stable archetypes that can be routed accurately from early dialogue prefixes without "
        "end-of-dialogue outcome leakage, (b) a slot-masked exemplar retrieval mechanism that achieves target "
        "archetype style convergence without inducing entity leakage, and (c) formal factorial evidence quantifying "
        "the main and interaction effects of external declarative rule verification and cluster-adaptive prompting "
        "on slot fidelity, policy adherence, and multi-turn turn economy (Acikgoz et al., 2025; Liu et al., 2022; "
        "Rebedea et al., 2023).",
    )
    D.lead_para(
        "Measurable research formulation",
        "This study models six quantitative dependent variables (<i>Y</i>)—cluster separation Silhouette "
        "(<i>Y</i><sub>1</sub>), style convergence cosine and pacing error (<i>Y</i><sub>2</sub>), policy rule "
        "adherence rate (<i>Y</i><sub>3</sub>), exemplar entity leakage rate (<i>Y</i><sub>4</sub>), factual slot "
        "F<sub>1</sub> (<i>Y</i><sub>5</sub>), and log-transformed turns to goal completion and redundant elicitation "
        "rate (<i>Y</i><sub>6</sub>)—as functions of four manipulated independent variables (<i>X</i>): clustering "
        "algorithm and trajectory representation (<i>X</i><sub>1</sub>, RQ1), in-context conditioning strategy "
        "(<i>X</i><sub>2</sub>, RQ2), rule-engine mode crossed with prompting strategy (<i>X</i><sub>3</sub>, RQ3), "
        "and prompting strategy crossed with refined user archetype (<i>X</i><sub>4</sub>, RQ4).",
    )

    D.heading("Purpose of the Study and Research Questions", 2)
    D.para(
        "The purpose of this quantitative study is to develop and evaluate an end-to-end neuro-symbolic, "
        "cluster-adaptive conversational framework on public human travel dialogues across four linked research "
        "questions (Table 1)."
    )
    D.table(
        "Research Questions, Hypotheses, and Analytical Framework",
        ["RQ", "Research question", "Null and alternative hypotheses", "Experimental design and statistical test"],
        [
            [
                "RQ1",
                "Which clustering algorithm (K-Means, Ward agglomerative, HDBSCAN) best separates dialogue embeddings, "
                "and which stable, early-routable user archetypes emerge?",
                "<i>H</i><sub>01</sub>: Equal mean Silhouette across algorithms. <i>H</i><sub>a1</sub>: At least one "
                "differs, and truncated behavioral-semantic prefixes yield stable (ARI ≥ .60), routable archetypes.",
                "One-way ANOVA across <i>N</i> = 159 runs (Welch & Kruskal–Wallis checks; Tukey & Games–Howell post "
                "hoc) + representation × truncation grid",
            ],
            [
                "RQ2",
                "Does cluster-adaptive few-shot prompting increase style convergence and pacing calibration relative "
                "to zero-shot and static few-shot prompting?",
                "<i>H</i><sub>02</sub>: Equal mean style cosine across conditions. <i>H</i><sub>a2</sub>: "
                "Cluster-adaptive > static and zero-shot on refined user archetypes.",
                "One-way repeated-measures ANOVA (<i>N</i> = 33 dialogues × 3 conditions = 99 calls; "
                "Greenhouse–Geisser, Friedman, Holm contrasts)",
            ],
            [
                "RQ3",
                "How do a declarative rule engine and cluster-adaptive prompting interact to govern rule adherence, "
                "exemplar leakage, slot F<sub>1</sub>, and style alignment?",
                "<i>H</i><sub>03</sub>: No main or interaction effects. <i>H</i><sub>a3</sub>: Active rules raise "
                "adherence and slot F<sub>1</sub> and eliminate few-shot entity leakage.",
                "2 × 2 factorial ANOVA (<i>N</i> = 144, <i>n</i> = 36/cell; OLS, HC3, and ART checks; dual-LLM judge "
                "κ)",
            ],
            [
                "RQ4",
                "Does cluster-adaptive prompting with an informed-slot ledger reduce turns to goal completion and "
                "redundant elicitation differently across user archetypes?",
                "<i>H</i><sub>04</sub>: No prompting or prompting × archetype interaction effects. "
                "<i>H</i><sub>a4</sub>: Cluster-adaptive prompting reduces log turns and RER with an archetype "
                "interaction.",
                "2 × 3 factorial ANOVA on log turns and RER (<i>N</i> = 180, <i>n</i> = 30/cell; OLS, HC3, ART, "
                "Welch <i>t</i>, Mann–Whitney <i>U</i>; persona κ)",
            ],
        ],
        note="RQ = research question; ARI = adjusted Rand index; HC3 = heteroscedasticity-consistent SE; ART = aligned "
             "rank transform; RER = redundant elicitation rate. All tests use α = .05.",
        widths=[0.45, 1.95, 2.05, 2.05],
        align=["l", "l", "l", "l"],
        split=True,
    )

    D.heading("Contributions and Expected Value", 2)
    D.para(
        "This study delivers four contributions: (1) proving that truncating dialogues to the first nine user "
        "messages and combining Gemini prefix embeddings with structured LLM behavioral ratings yields stable "
        "user archetypes (ARI = .76) with high held-out prefix routing agreement (κ = .535 at five messages to .958 "
        "at nine messages); (2) contrasting primary versus refined archetypes in RQ2 to demonstrate that "
        "cluster-adaptive prompting succeeds significantly (<i>p</i> < .001) once upstream routing is coherent; "
        "(3) demonstrating in RQ3 that external declarative verification eliminates the 35.9% entity leakage of "
        "unguarded few-shot prompting while raising policy violation enforcement from 5.6% to 98.6%; and (4) showing "
        "in RQ4 that archetype-adaptive turn-economy policies cut turns to booking completion by 29.5% to 42.7% and "
        "eliminate redundant slot questions."
    )

    # ================================================================== 2. LITERATURE REVIEW
    D.heading("Literature Review", 1)
    D.heading("Literature Review Approach and Relevance Matrix", 2)
    D.para(
        "Peer-reviewed studies were retrieved from the ACL Anthology, ACM Digital Library, IEEE Xplore, ScienceDirect, "
        "Google Scholar, and arXiv using Boolean combinations of <i>travel and hospitality chatbots</i>, "
        "<i>conversational recommender systems</i>, <i>task-oriented dialogue corpora</i>, <i>trajectory clustering</i>, "
        "<i>in-context exemplar retrieval</i>, and <i>LLM guardrails</i>. Twenty-six sources spanning business "
        "adoption, dialogue datasets, unsupervised clustering, retrieval-augmented prompting, and statistical "
        "methodology were synthesized. Table 2 maps the core literature streams to the gaps addressed in RQ1–RQ4."
    )
    D.table(
        "Literature Relevance Matrix Across Business and Technical Domains",
        ["Study and stream", "Methodology and dataset", "Key findings", "Gap addressed in this study"],
        [
            [
                "Buhalis & Sinarta (2019); Ivanov & Webster (2019); Melián-González et al. (2021) — Travel AI business value",
                "Service-automation frameworks and consumer adoption modeling (<i>N</i> = 1,476) in tourism and hospitality",
                "Real-time personalization and low interaction effort drive chatbot booking conversion and ROI",
                "Measures perceptions via surveys rather than instrumenting turn economy, slot redundancy, or policy compliance in LLM dialogues (RQ3, RQ4)",
            ],
            [
                "Jannach et al. (2021); Inaba et al. (2022) — Conversational recommenders & traveler styles",
                "CRS architectural taxonomy; collection and analysis of multi-turn travel agency dialogues",
                "Travelers differ in initiative, exploration breadth, and constraint rigidity; static policies cause repetitive turns",
                "Describes traveler diversity qualitatively without unsupervised archetype clustering or prefix routing (RQ1, RQ2)",
            ],
            [
                "El Asri et al. (2017); Budzianowski et al. (2018); Zang et al. (2020) — Dialogue corpora",
                "Microsoft Frames (1,369 package negotiations) and MultiWOZ 2.2 (10,438 multi-domain dialogues)",
                "Frames captures nonlinear frame-switching and budget trade-offs; MultiWOZ standardizes slot tracking",
                "Built for supervised state tracking; neither clusters user archetypes nor evaluates few-shot leakage or policy rules (RQ1–RQ4)",
            ],
            [
                "Reimers & Gurevych (2019); Lee et al. (2025); McInnes et al. (2017, 2018); Hennig (2007) — Embeddings & clustering",
                "Sentence-BERT (384-d), Gemini embeddings (3,072-d), HDBSCAN, UMAP, and bootstrap ARI stability",
                "Cosine geometry supports semantic clustering; bootstrap ARI and Silhouette quantify partition stability",
                "Clusters static texts rather than prefix-truncated user trajectories paired with LLM behavioral ratings (RQ1)",
            ],
            [
                "Brown et al. (2020); Liu et al. (2022); Johnson et al. (2021) — In-context learning & FAISS",
                "Few-shot prompting; <i>k</i>-NN exemplar selection (KATE); FAISS vector indexing",
                "Nearest-neighbor in-context examples outperform random static examples on single-turn NLP tasks",
                "Retrieves from one global pool without archetype partitioning, slot masking, or style/leakage evaluation (RQ2, RQ3)",
            ],
            [
                "Rebedea et al. (2023); Yao et al. (2024); Acikgoz et al. (2025); Gilardi et al. (2023) — Guardrails & evaluation",
                "NeMo Guardrails; τ-bench policy benchmark; TD-EVAL metrics; LLM annotation reliability",
                "Prompt-only LLMs violate domain rules; programmable rails and turn-level factual audits are essential",
                "Does not test the 2 × 2 factorial interaction between declarative rules and cluster-adaptive style prompting (RQ3)",
            ],
        ],
        note="CRS = conversational recommender system; ARI = adjusted Rand index; FAISS = Facebook AI Similarity Search.",
        widths=[1.45, 1.55, 1.65, 1.85],
        align=["l", "l", "l", "l"],
        split=True,
    )

    D.heading("Thematic Synthesis and Research Gaps", 2)
    D.lead_para(
        "Business context: Hospitality service automation and conversational friction",
        "In digital travel and hospitality commerce, competitive differentiation depends on real-time itinerary "
        "co-creation ('nowness' service; Buhalis & Sinarta, 2019). Ivanov and Webster (2019) showed that automated "
        "service agents generate financial value only when they resolve consultative inquiries without human "
        "escalation, while Melián-González et al. (2021) demonstrated that consumer intention to use travel chatbots "
        "depends on interaction efficiency and task fit. Empirical studies of travel agency dialogues confirm that "
        "human consultants adapt their pacing—confirming bookings rapidly for decisive buyers while presenting "
        "side-by-side comparisons for exploratory shoppers (Inaba et al., 2022; Jannach et al., 2021).",
    )
    D.lead_para(
        "Task-oriented corpora and unsupervised trajectory clustering",
        "While MultiWOZ (Budzianowski et al., 2018) and MultiWOZ 2.2 (Zang et al., 2020) benchmark slot tracking "
        "across local services, they lack flight routing and multi-package price negotiation. Microsoft Frames "
        "(El Asri et al., 2017) directly captures multi-turn flight-and-hotel negotiation under budget constraints, "
        "making it the ideal primary corpus and MultiWOZ 2.2 an external structural comparison. Representing "
        "dialogues with Sentence-BERT (Reimers & Gurevych, 2019) and Gemini embeddings (Lee et al., 2025) enables "
        "rigorous comparison of K-Means, Ward agglomerative clustering, and HDBSCAN (McInnes et al., 2017) using "
        "Silhouette (Rousseeuw, 1987), Davies–Bouldin (Davies & Bouldin, 1979), bootstrap ARI stability (Hennig, "
        "2007; Hubert & Arabie, 1985), and UMAP (McInnes et al., 2018; Pedregosa et al., 2011), augmented by "
        "reliable zero-temperature LLM behavioral ratings (Gilardi et al., 2023).",
    )
    D.lead_para(
        "Dynamic in-context learning, neuro-symbolic guardrails, and research gaps",
        "Few-shot prompting (Brown et al., 2020) and similarity-based FAISS retrieval (Johnson et al., 2021; Liu "
        "et al., 2022) improve single-turn task accuracy but risk entity contamination and policy drift in multi-turn "
        "dialogues. Programmable guardrails (Rebedea et al., 2023), policy benchmarks (τ-bench; Yao et al., 2024), "
        "and turn-level evaluation frameworks (TD-EVAL and BERTScore; Acikgoz et al., 2025; Zhang et al., 2020) "
        "motivate decoupling style from policy verification. Four research gaps follow: (1) discovering early-routable "
        "travel user archetypes free of outcome confounding (RQ1); (2) testing archetype-matched, slot-masked "
        "exemplar retrieval for style convergence (RQ2); (3) isolating the 2 × 2 factorial interaction between "
        "declarative rule verification and adaptive prompting (RQ3); and (4) quantifying multi-turn turn economy "
        "and redundant elicitation reductions across traveler personas (RQ4).",
    )

    # ================================================================== 3. MATERIALS AND METHODS
    D.heading("Materials and Methods", 1)
    D.heading("Data Sources, Access, and Ethical Governance", 2)
    D.para(
        f"This study uses two public English dialogue corpora (Table 3): Microsoft Frames (El Asri et al., 2017; "
        f"{n2(ctx['n_frames_raw'], 0)} raw dialogues, {n2(fq.n_analytic, 0)} analytic) and MultiWOZ 2.2 (Zang et al., "
        f"2020; seeded sample of {n2(mq.n_raw, 0)} travel dialogues, {n2(mq.n_analytic, 0)} analytic). Both datasets "
        "were collected with research consent, use anonymized role-player IDs, and contain no personally identifiable "
        "information."
    )
    D.table(
        "Dataset Overview",
        ["Attribute", "Microsoft Frames (primary corpus)", "MultiWOZ 2.2 (comparison corpus)"],
        [
            ["Records", f"{n2(ctx['n_frames_raw'], 0)} raw; {n2(fq.n_analytic, 0)} analytic (golden <i>D</i><sub>gold</sub> = {s1['n_gold']}, held-out <i>D</i><sub>test</sub> = {s1['n_test']})", f"10,438 raw; travel sample of {n2(mq.n_raw, 0)}; {n2(mq.n_analytic, 0)} analytic"],
            ["Domain setting", "Multi-turn flight + hotel package negotiation under budget and date constraints", "Multi-domain city services (hotel, train, taxi, attraction) without flights"],
            ["Annotations used", "Utterance text, speaker, dialogue acts, slot–value arguments, wizard task success, user rating", "Utterance text, speaker, active services, turn-level slot state dictionaries"],
            ["Analytical role", "RQ1 clustering & refined archetypes, RQ2 prompting, RQ3 2×2 experiment, RQ4 2×3 simulation", "External descriptive comparison in EDA and cross-corpus projection check in RQ1"],
        ],
        widths=[1.3, 2.75, 2.45],
        align=["l", "l", "l"],
        split=True,
    )

    D.heading("Data Dictionary and Data Cleaning", 2)
    D.para(
        "Both corpora were normalized into a two-tier Pydantic schema (<i>src/canonical_schema.py</i>): Tier 1 stores nine "
        "universal travel slots (origin, destination, departure/return dates, duration in nights, adults, children, "
        "budget in USD, and hotel tier), and Tier 2 stores five policy slots evaluated by the rule engine (visa "
        "window in days, passport validity in months, package type, room sharing, and discount percentage). Table 4 "
        "defines the analytical variables and units (raw source fields and canonical schema fields are listed in "
        "Appendix A, Table A3). Table 5 documents the programmatic quality audit and cleaning log. To prevent data "
        f"leakage, the {n2(fq.n_analytic, 0)} analytic Frames dialogues were split once (seed 42, stratified on task "
        f"success) into a 70% golden discovery partition (<i>D</i><sub>gold</sub>, <i>n</i> = {s1['n_gold']}) used to "
        "fit clusters, PCA transformations, routers, and FAISS indices, and a 30% held-out test partition "
        f"(<i>D</i><sub>test</sub>, <i>n</i> = {s1['n_test']}) used strictly for out-of-sample evaluation."
    )
    D.table(
        "Data Dictionary of Analytical Variables With Units and Operational Definitions",
        ["Variable", "Role", "Type and unit", "Operational definition and scale", "RQ"],
        [
            ["Clustering algorithm", "Primary IV", "Categorical (3 levels)", "K-Means (<i>k</i>=3), Ward agglomerative (<i>k</i>=3), HDBSCAN", "1"],
            ["Silhouette & Davies–Bouldin", "Primary/Sec. DV", "Continuous (unitless / ratio)", "Cosine Silhouette [−1, 1] and cluster scatter ratio (≥ 0)", "1"],
            ["Adjusted Rand index (ARI)", "Diagnostic DV", "Continuous [−1, 1] (unitless)", "Chance-corrected partition stability across 80% subsamples", "1"],
            ["LLM behavioral profile (16 fields)", "Clustering / Audit", "10 ordinal (1–5) + 6 cat./bool.", "10 Likert scales + 3 goal/tone clustering fields + 3 audit fields (Table C1)", "1, 4"],
            ["Refined user archetype", "IV / Moderator", "Categorical (3 levels)", "<i>Decisive Booker</i>, <i>Open Explorer</i>, <i>Rigid-Constraint Seeker</i>", "1–4"],
            ["Prompting strategy", "Primary IV", "Categorical (2 or 3 levels)", "Zero-Shot, Static Few-Shot (<i>k</i>=3), Cluster-Adaptive Few-Shot (<i>k</i>=3)", "2–4"],
            ["Style convergence & Pacing err.", "Primary/Sec. DV", "Cosine [−1, 1] / Words (count)", "Cosine to target archetype agent centroid; |words<sub>gen</sub> − μ<sub>words,<i>a</i></sub>|", "2, 3"],
            ["Rule-engine mode", "Primary IV", "Binary (2 levels)", "Rules Off (unguarded) vs. Rules Active (pre-check + verification)", "3"],
            ["Rule adherence rate (RAR)", "Primary DV", "Proportion [0, 1] (rate)", "Share of violated policy rules enforced (and compliant states unblocked)", "3"],
            ["Exemplar leakage rate (ELR)", "Primary DV", "Proportion [0, 1] (rate)", "Share of response entities originating from prompt exemplars", "3"],
            ["Factual slot coverage F<sub>1</sub>", "Primary DV", "Proportion [0, 1] (F<sub>1</sub> score)", "Harmonic mean of precision and recall over active booking state slots", "3"],
            ["Turns to goal (log) & RER", "Primary/Sec. DV", "Log count (ln turns) / Rate [0, 1]", "Log turns until [ACCEPT_BOOKING]; redundant slot requests / agent turns", "4"],
        ],
        note="IV = independent variable; DV = dependent variable; RER = redundant elicitation rate. Raw and canonical fields are in Table A3.",
        widths=[1.5, 0.85, 1.2, 2.45, 0.5],
        align=["l", "l", "l", "l", "c"],
        split=True,
    )
    D.table(
        "Data Cleaning and Quality Audit Log",
        ["Issue", "Variables", "Detection", "Frames", "MultiWOZ", "Treatment and rationale"],
        [
            ["Duplicate full text", "Utterances", "SHA-256 text hash", str(int(fq.duplicate_text)), str(int(mq.duplicate_text)), "Removed duplicate to prevent double-weighting"],
            ["Fewer than 3 turns", "total_turns", "Turn count < 3", str(int(fq.excluded_lt_min_turns)), str(int(mq.excluded_lt_min_turns)), "Excluded; minimum 3 turns needed for prefix routing"],
            ["Turn-count outliers", "total_turns", "> Q3 + 1.5 × IQR", f"{int(fq.turn_outliers_iqr)} (> {n2(fq.outlier_threshold, 1)})", f"{int(mq.turn_outliers_iqr)} (> {n2(mq.outlier_threshold, 1)})", "Retained as genuine negotiations; log-transformed in RQ4"],
            ["Unobserved slots", "Tier 1 & 2 slots", "Never mentioned", "Table E1", "Table E1", "Preserved as null (None); never imputed"],
            ["Entity values in text", "Utterance text", "Slot/number regex", "All", "All", "Masked with [SLOT] tokens in exemplars to prevent leakage"],
            ["Analytic sample", "All fields", "Post-cleaning count", f"{n2(fq.n_analytic, 0)} (933/401)", n2(mq.n_analytic, 0), "Locked with stratified 70/30 split (seed 42)"],
        ],
        note="Zero duplicate IDs or empty utterances occurred in either corpus. Missing user ratings (11 in Frames) were retained.",
        widths=[1.25, 1.0, 1.1, 0.85, 0.65, 1.65],
        align=["l", "l", "l", "c", "c", "l"],
        split=True,
    )

    D.heading("Exploratory Data Analysis (Univariate, Bivariate, and Multivariate)", 2)
    D.heading("Univariate Analysis", 3)
    D.para(
        f"Table 6 and Figure 1 summarize the univariate distributions. Frames and MultiWOZ 2.2 have similar mean "
        f"lengths (<i>M</i> = {n2(fd.turns_M)} vs. {n2(md.turns_M)} turns), but Frames exhibits greater dispersion "
        f"(<i>SD</i> = {n2(fd.turns_SD)} vs. {n2(md.turns_SD)}) and a heavier right tail due to multi-offer package "
        "comparisons. Golden and held-out partitions are nearly identical across all metrics. Slot completeness "
        "(Appendix E, Table E1 and Figure E1) confirms high coverage of origin (98.4%), destination (99.1%), dates "
        "(96.0%), and budget (78.5%) in Frames, but 0.0% coverage of visa, passport, and discount rules in both "
        "corpora, motivating synthetic Tier-2 injection in RQ3."
    )
    desc_rows = [
        [
            r.corpus, n2(r.N, 0), f"{n2(r.turns_M)} ({n2(r.turns_SD)})", n2(r.turns_Mdn, 0),
            f"{int(r.turns_min)}–{int(r.turns_max)}", n2(r.user_words_M, 1), n2(r.agent_words_M, 1),
            "—" if pd.isna(r.success_pct) else n2(r.success_pct, 1),
        ]
        for _, r in desc.iterrows()
    ]
    D.table(
        "Univariate Descriptive Statistics of the Analytic Samples",
        ["Sample", "<i>N</i>", "Turns <i>M</i> (<i>SD</i>)", "<i>Mdn</i>", "Range", "User words", "Agent words", "Task success (%)"],
        desc_rows,
        widths=[1.95, 0.55, 1.0, 0.45, 0.6, 0.65, 0.65, 0.65],
        align=["l", "c", "c", "c", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "Univariate Distribution of Dialogue Length by Corpus",
        os.path.join(FIG_INT, "fig_eda_turns.png"),
        note=f"Frames <i>N</i> = {n2(fq.n_analytic, 0)}; MultiWOZ <i>N</i> = {n2(mq.n_analytic, 0)}.",
        width=4.4,
    )

    D.heading("Bivariate Analysis", 3)
    b0, b1, b3, b4 = t_biv.iloc[0], t_biv.iloc[1], t_biv.iloc[3], t_biv.iloc[4]
    D.para(
        "Parametric (Pearson <i>r</i>) and non-parametric (Spearman ρ) bivariate correlations across all "
        f"{n2(fq.n_analytic, 0)} Frames dialogues (Table 7; Figure 2) show that dialogue length is strongly driven by "
        f"slot revisions (<i>r</i> = {nz(b0.pearson_r)}, ρ = {nz(b0.spearman_rho)}, <i>p</i> < .001) and agent package "
        f"offers (<i>r</i> = {nz(b1.pearson_r)}, ρ = {nz(b1.spearman_rho)}, <i>p</i> < .001). Linking structural "
        "counts to LLM behavioral ratings confirms construct validity: slot revisions correlate strongly with user "
        f"exploration breadth (<i>r</i> = {nz(b3.pearson_r)}, ρ = {nz(b3.spearman_rho)}, <i>p</i> < .001), whereas "
        f"decisiveness correlates negatively with dialogue length (<i>r</i> = {nz(b4.pearson_r)}, "
        f"ρ = {nz(b4.spearman_rho)}, <i>p</i> < .001)."
    )
    biv_rows = [[r.pair_label, nz(r.pearson_r, 3), pv_cell(r.pearson_p), nz(r.spearman_rho, 3), pv_cell(r.spearman_p)] for _, r in t_biv.iterrows()]
    D.table(
        "Bivariate Parametric and Non-Parametric Correlations of Dialogue Dynamics (Frames)",
        ["Variable pair", "Pearson <i>r</i>", "<i>p</i> (Pearson)", "Spearman ρ", "<i>p</i> (Spearman)"],
        biv_rows,
        widths=[3.1, 0.85, 0.85, 0.85, 0.85],
        align=["l", "c", "c", "c", "c"],
        split=True,
    )
    D.figure(
        "Bivariate Relationships Between Dialogue Length, Slot Revisions, and Archetype Negotiation Intensity",
        os.path.join(FIG_FIN, "fig_eda_bivariate.png"),
        note="Panel A: Turns vs. slot revisions with OLS trend. Panel B: Mean revisions and package offers by refined archetype (95% CI).",
        width=4.4,
    )

    D.heading("Multivariate Analysis", 3)
    pve = eda_ext["pca_var_explained"]
    D.para(
        "Multivariate structure across ten structural and behavioral variables was examined via Spearman rank "
        "correlation and principal component analysis (PCA; Figure 3; full loadings in Appendix E, Table E2). The "
        f"first three components explain {pct(100 * sum(pve), 1)} of total variance: PC1 ({pct(100 * pve[0], 1)}%) "
        "captures <i>Exploration vs. Rigidity</i> (revisions .42, turns .39, exploration breadth .39), PC2 "
        f"({pct(100 * pve[1], 1)}%) captures <i>Decisiveness & Politeness</i> (−.51, −.46), and PC3 "
        f"({pct(100 * pve[2], 1)}%) isolates <i>User Verbosity</i> (.89), separating the three refined archetypes across "
        "a continuous behavioral manifold."
    )
    D.figure(
        "Multivariate Spearman Correlation Matrix and Principal Component Biplot of Behavioral Features",
        os.path.join(FIG_FIN, "fig_eda_multivariate.png"),
        note="Panel A: Rank correlation matrix. Panel B: PCA biplot colored by refined archetype with top loading vectors.",
        width=4.5,
    )

    D.heading("Research Design, Hypotheses, and Statistical Power Analysis", 2)
    D.para(
        "Sample sizes were computed a priori for each planned analysis using Cohen's medium effect <i>f</i> = .25 "
        "(Cohen, 1988), α = .05, and target power 1 − β ≥ .80 via the noncentral <i>F</i> distribution (Faul et al., "
        "2007):",
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
        "<i>f</i><sup>2</sup><i>Nm</i>ε / (1 − ρ) for repeated-measures RQ2 (<i>m</i> = 3, ρ = .50, ε = 1). Minimum "
        "sample sizes were rounded to balanced cells with a 10% buffer (Table 8), yielding final power of .835–.865.",
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
        "Sample Size and Power Calculations Matched to Each Planned Analysis",
        ["RQ", "Planned analysis", "<i>df</i> at <i>N</i><sub>min</sub>", "λ", "<i>F</i><sub>crit</sub>", "<i>N</i><sub>min</sub>", "Power", "<i>N</i><sub>final</sub> (per group)", "Final power"],
        ss_rows,
        widths=[0.45, 1.75, 0.65, 0.5, 0.5, 0.5, 0.55, 0.95, 0.65],
        align=["l", "l", "c", "c", "c", "c", "c", "c", "c"],
        split=True,
    )

    D.heading("Model Selection, Mathematical Formulation, and Evaluation Metrics", 2)
    D.para(
        "<i>Trajectory and hybrid user representations (RQ1).</i> Primary trajectory vectors pool de-lexicalized "
        "turn embeddings <b>e</b><sub><i>t</i></sub> with exponential decay (λ<sub>d</sub> = 0.15):",
        keep_next=True,
    )
    D.equation(
        "<b>v</b> = Σ<sub><i>t</i>=1</sub><sup><i>T</i></sup> <i>w</i><sub><i>t</i></sub><b>e</b><sub><i>t</i></sub>,   "
        "<i>w</i><sub><i>t</i></sub> = exp[−λ<sub>d</sub>(<i>T</i> − <i>t</i>)] / "
        "Σ<sub><i>j</i>=1</sub><sup><i>T</i></sup> exp[−λ<sub>d</sub>(<i>T</i> − <i>j</i>)]",
        "2",
    )
    D.para(
        "To prevent end-of-dialogue outcome confounding, the refined archetype representation (<i>Blocks</i>) "
        "concatenates two L2-normalized blocks computed strictly on the first <i>M</i> user messages: (1) the top 20 "
        "principal components (fitted on <i>D</i><sub>gold</sub>) of the 3,072-dimensional Gemini embedding "
        "(<i>gemini-embedding-001</i>; Lee et al., 2025), and (2) a standardized 16-field LLM behavioral schema "
        "comprising 13 clustering fields (ten 1–5 ordinal rating scales plus primary goal, secondary goals, and "
        "emotional tone) and three audit-only fields (session outcome, party type, and unusual-conversation flag, "
        "excluded from clustering input; Table C1; test–retest weighted κ = "
        f"{nz(min(r1h['reliability'][x] for x in ORDS))}–{nz(max(r1h['reliability'][x] for x in ORDS))} across the 10 "
        "ordinal scales and κ = .75–.98 across the 6 categorical/boolean fields; revision correlation ρ = "
        f"{nz(cv_['revision_tendency~user_revisions']['rho'])}, Table C2). In RQ2–RQ4, "
        "<i>RefinedArchetypeRouter</i> projects each test dialogue's opening user prefix into this golden-fitted "
        "<i>Blocks</i> space, predicts the user archetype via L1-regularized logistic regression, and retrieves "
        "<i>k</i> = 3 slot-masked exemplars from that archetype's FAISS sub-index. In RQ3, the deterministic rule "
        "engine (<i>src/rule_engine.py</i>, 14/14 boundary tests passed) evaluates five YAML policy rules (Table 9). "
        "Table 10 defines all evaluation metrics."
    )
    D.table(
        "Declarative Policy Rules Used in RQ3",
        ["Rule ID and name", "Trigger condition", "Action", "Severity"],
        [
            [
                f"{r['rule_id']}: {r['name']}",
                r["condition"].replace("budget_amount is not None and ", "budget stated; ").replace("==", "=").replace(" and ", "; "),
                r["action"].replace("_", " ").lower(),
                r["severity"].lower(),
            ]
            for _, r in rules.iterrows()
        ],
        widths=[1.9, 2.5, 1.3, 0.8],
        align=["l", "l", "l", "c"],
        split=True,
    )
    D.table(
        "Evaluation Metrics, Mathematical Formulae, and Interpretation",
        ["Metric", "Formula", "RQ", "Interpretation"],
        [
            ["Silhouette & DB index", "<i>s</i>(<i>i</i>) = [<i>b</i>(<i>i</i>)−<i>a</i>(<i>i</i>)]/max{<i>a</i>,<i>b</i>}; <i>DB</i> = (1/<i>k</i>)Σ max(σ<sub><i>i</i></sub>+σ<sub><i>j</i></sub>)/<i>d</i>(<b>c</b><sub><i>i</i></sub>,<b>c</b><sub><i>j</i></sub>)", "1", "Higher Silhouette [−1, 1] and lower DB (≥ 0) indicate better separation"],
            ["ARI & Cohen's κ", "<i>ARI</i> = (<i>RI</i>−E[<i>RI</i>])/(max <i>RI</i>−E[<i>RI</i>]); κ = (<i>p</i><sub>o</sub>−<i>p</i><sub>e</sub>)/(1−<i>p</i><sub>e</sub>)", "1, 3, 4", "Resampling stability (ARI ≥ .60) and routing/judge agreement"],
            ["Style cosine & Pacing err.", "cos(<b>r</b>, <b>c</b><sub><i>a</i></sub>) = (<b>r</b>·<b>c</b><sub><i>a</i></sub>)/(‖<b>r</b>‖‖<b>c</b><sub><i>a</i></sub>‖); |<i>W</i><sub>gen</sub> − μ<sub><i>W</i>,<i>a</i></sub>|", "2, 3", "Higher cosine and lower word error indicate better style alignment"],
            ["Rule adherence (RAR)", "|<i>R</i><sub>enforced</sub> ∩ <i>R</i><sub>violated</sub>| / |<i>R</i><sub>violated</sub>| (or 1 − false_block)", "3", "Proportion [0, 1] of active policy rules properly enforced"],
            ["Exemplar leakage (ELR)", "|<i>E</i><sub>resp</sub> ∩ (<i>E</i><sub>ex</sub> \\ <i>E</i><sub>diag</sub>)| / max(1, |<i>E</i><sub>resp</sub>|)", "3", "Proportion [0, 1] of response entities leaked from prompt exemplars"],
            ["Slot coverage F<sub>1</sub>", "2 · Precision · Recall / (Precision + Recall) over active state slots", "3", "Proportion [0, 1] of active booking slots grounded in response"],
            ["Turns to goal & RER", "TGC = turns to [ACCEPT_BOOKING]; RER = <i>A</i><sub>redundant</sub> / <i>A</i><sub>total</sub>", "4", "Lower log turns and lower RER indicate superior turn economy"],
        ],
        note="Parametric ANOVAs are paired with Welch/HC3 and non-parametric (Kruskal–Wallis, Friedman, Mann–Whitney, ART; Wobbrock et al., 2011) checks.",
        widths=[1.45, 2.85, 0.5, 1.7],
        align=["l", "l", "c", "l"],
        split=True,
    )

    # ================================================================== 4. ARCHITECTURE AND WORKFLOW
    D.heading("Architecture and Workflow", 1)
    D.heading("System Architecture and Algorithmic Workflows", 2)
    D.para(
        "Figure 4 illustrates the five-layer neuro-symbolic system architecture, and Figure 5 details the step-by-step "
        "execution workflows for RQ1 through RQ4. Offline discovery and indexing (Layers 1–2) operate strictly on "
        "the golden partition (<i>D</i><sub>gold</sub>, <i>n</i> = 933): raw dialogues are parsed into two-tier "
        "Pydantic trajectories, prefix embeddings (<i>gemini-embedding-001</i>) and 16-field LLM behavioral profiles "
        "are combined into the <i>Blocks</i> representation on the first <i>M</i> = 9 user messages, and three "
        "<i>K</i>-Means centroids, three archetype-specific FAISS <i>IndexFlatIP</i> sub-indices, and the "
        "L1-regularized prefix router are frozen. Online runtime and evaluation (Layers 3–5) operate on held-out "
        "test dialogues (<i>D</i><sub>test</sub>, <i>n</i> = 401): incoming prefixes are projected into the golden "
        "<i>Blocks</i> space and routed to their predicted archetype, <i>k</i> = 3 slot-masked exemplars are retrieved, "
        "the Verified Informed Slot Ledger and declarative YAML rule engine evaluate state constraints, "
        "<i>gemini-2.5-flash</i> generates the response with post-generation entity-leakage sanitization, and "
        "outputs are scored and cross-validated by an independent <i>gemini-2.5-pro</i> judge."
    )
    D.figure(
        "End-to-End Neuro-Symbolic Cluster-Adaptive Conversational System Architecture",
        os.path.join(FIG_FIN, "fig_system_architecture.png"),
        note="Offline fitting uses <i>D</i><sub>gold</sub> (<i>n</i> = 933); online routing, retrieval, rule verification, and evaluation use <i>D</i><sub>test</sub> (<i>n</i> = 401).",
        width=4.5,
    )
    D.figure(
        "Algorithmic Execution Workflows Across Research Questions RQ1 to RQ4",
        os.path.join(FIG_FIN, "fig_rq_workflows_4panel.png"),
        note="Step-by-step experimental pipelines and statistical hypothesis tests for RQ1 (Panel A), RQ2 (Panel B), RQ3 (Panel C), and RQ4 (Panel D).",
        width=4.5,
    )

    D.heading("Pipeline Component Specifications and Technology Stack", 2)
    D.para(
        "The software stack is implemented in Python 3.11 across <i>src/interim_pipeline/</i> and <i>src/final_pipeline/</i> "
        "using <i>pandas</i> 2.2, <i>numpy</i> 1.26, and <i>pydantic</i> 2.9 for data validation; <i>sentence-transformers</i> "
        "(<i>all-MiniLM-L6-v2</i>), Google <i>genai</i> SDK (<i>gemini-embedding-001</i>, <i>gemini-2.5-flash</i>, "
        "<i>gemini-2.5-pro</i>), and <i>faiss-cpu</i> for vector indexing and generation; <i>scikit-learn</i> 1.5, <i>hdbscan</i>, "
        "and <i>umap-learn</i> for clustering; <i>scipy.stats</i> and <i>statsmodels</i> (Seabold & Perktold, 2010) for OLS, HC3, "
        "and Aligned Rank Transform ANOVA; and <i>python-docx</i> and <i>pymupdf</i> for automated APA 7 document compilation."
    )
