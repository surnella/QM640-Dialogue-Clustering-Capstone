# Cluster-Adaptive Prompting for Multi-Turn Travel and Tourism Conversational Systems

**Course**: QM640 — Data Analytics Capstone  
**Institution**: Department of Data Analytics, Walsh College  
**Author**: Surnella Sandeep  
**Instructor / Mentor**: Mr. Smitraj Raut  
**GitHub Repository**: [https://github.com/surnella/QM640-Dialogue-Clustering-Capstone](https://github.com/surnella/QM640-Dialogue-Clustering-Capstone)

---

## 1. Project Overview & Research Architecture

Commercial conversational AI assistants in travel and tourism rely predominantly on static, one-size-fits-all system prompts. When interacting with travelers who exhibit heterogeneous decision-making behaviors—ranging from decisive buyers who want immediate package confirmation to exploratory shoppers who compare multiple alternatives and rigid-constraint seekers who push back on budget/tier trade-offs—a static prompt creates repetitive slot elicitation, mismatched conversational pacing, and session abandonment. Conversely, adapting agent style solely via unguarded in-context examples risks factual entity leakage (copying stale hotel names, fares, or promo codes from retrieved exemplars) and policy drift (violating visa lead-time, passport validity, party-size capacity, or discount rules).

This quantitative study designs, implements, and empirically evaluates a **neuro-symbolic cluster-adaptive conversational framework** across four linked research questions:

1. **RQ1 — Unsupervised Dialogue Clustering & Refined User Archetypes**: Compares K-Means, Ward agglomerative clustering, and HDBSCAN across 159 independent subsample runs on Microsoft Frames ($N = 1,334$ analytic dialogues) and MultiWOZ 2.2 ($N = 1,500$ travel dialogues), followed by a pre-declared representation-by-truncation sensitivity analysis combining Gemini embeddings (`gemini-embedding-001`) with a 16-field LLM behavioral profile on the first $M = 9$ user messages to discover three stable **Refined User Archetypes**: *Decisive Booker*, *Open Explorer*, and *Rigid-Constraint Seeker*.
2. **RQ2 — Cluster-Adaptive Few-Shot Prompting**: Evaluates whether routing an opening conversation prefix to its nearest Refined User Archetype and retrieving archetype-matched, slot-masked FAISS exemplars increases conversational style convergence and pacing calibration relative to `Zero-Shot` and `Static Few-Shot` baselines ($N = 33$ repeated-measures design, 99 Gemini 2.5 Flash generations).
3. **RQ3 — Decoupled Declarative Rule Verification vs. Prompt Conditioning**: Executes a $2 \times 2$ between-subjects factorial experiment ($N = 144$, $n = 36$ per cell: `Rules Off` vs. `Rules Active` $\times$ `Zero-Shot` vs. `Cluster-Adaptive Few-Shot`) to isolate main and interaction effects on Policy Rule Adherence Rate, Exemplar Entity Leakage Rate, Factual Slot Coverage F1, and Style Alignment, validated by dual-LLM judge reliability (`gemini-2.5-flash` vs. `gemini-2.5-pro`).
4. **RQ4 — Multi-Turn Turn Economy Across User Archetypes**: Executes a $2 \times 3$ factorial multi-turn simulation ($N = 180$, $n = 30$ per cell: `Zero-Shot` vs. `Cluster-Adaptive Few-Shot` $\times$ three Refined User Archetypes) to test whether cluster-adaptive prompting with a Verified Informed Slot Ledger reduces Turns to Goal Completion (TGC) and Redundant Elicitation Rate (RER) differentially across user archetypes, validated via an independent `gemini-2.5-pro` persona fidelity check.

---

## 2. Repository Structure

```text
QM640-Dialogue-Clustering-Capstone/
├── data/
│   ├── raw/                        # Downloaded Microsoft Frames (N=1,369) & MultiWOZ 2.2 corpora (excluded from Git)
│   ├── canonical/                  # Normalized two-tier canonical dialogue trajectories (canonical_corpus.jsonl)
│   ├── interim/                    # Cleaned Frames (N=1,334) & MultiWOZ (N=1,500) partitions, embeddings,
│   │                               # primary/refined archetypes, LLM behavior annotations, and RQ1/RQ2 results
│   └── final/                      # Empirical caches & JSON/CSV outputs for refined RQ2, RQ3 (N=144), RQ4 (N=180), & EDA
├── src/
│   ├── canonical_schema.py         # Pydantic data models for Tier-1 travel slots and Tier-2 policy slots
│   ├── ingestion.py                # Corpus parsers for Microsoft Frames and MultiWOZ 2.2
│   ├── rule_engine.py              # Deterministic declarative business rule evaluator (5 policy rules)
│   ├── interim_pipeline/           # Steps 0–4 + Steps 2b–2i (power analysis, cleaning, RQ1 clustering,
│   │                               # Gemini embeddings, LLM behavioral annotations, truncation & ablation grids)
│   ├── final_pipeline/             # Final empirical pipeline:
│   │   ├── common_llm.py           # Thread-safe JSONL-cached Gemini client (gemini-2.5-flash & gemini-2.5-pro)
│   │   ├── routing.py              # RefinedArchetypeRouter (Blocks prefix router + per-archetype FAISS indices)
│   │   ├── metrics.py              # Slot F1, exemplar leakage, RM-ANOVA, 2x2/2x3 OLS+HC3+ART ANOVA, Cohen's kappa
│   │   ├── test_step1_harness.py   # End-to-end verification tests for routing and statistical harness
│   │   ├── step2_rq2_refined.py    # RQ2 repeated-measures experiment on Refined Archetypes (N=33, 99 calls)
│   │   ├── step3_rq3_experiment.py # RQ3 2x2 factorial experiment (N=144) + dual-judge reliability (n=48)
│   │   ├── step4_rq4_simulation.py # RQ4 2x3 multi-turn simulation (N=180) + persona validation (n=45)
│   │   └── step5_figures_and_eda.py# Bivariate/multivariate EDA + system architecture & workflow diagrams
│   ├── report/                     # APA 7 Word/PDF document engine (docx_apa.py) and verified reference list
│   ├── build_interim_submission.py # Reproducible builder for the Interim Report
│   └── build_final_report.py       # Reproducible builder for the Final Report (.docx and .pdf)
├── rules/
│   └── rules_enterprise.yaml       # Declarative policy rules (visa lead time, passport validity, FIT pax, discount, budget)
├── notebooks/
│   ├── 01_eda_and_cleaning.ipynb          # Univariate, bivariate, and multivariate EDA & cleaning log
│   ├── 02_trajectory_clustering_rq1.ipynb # RQ1 clustering, sensitivity grid, refined archetypes, & prefix routing
│   ├── 03_fewshot_retrieval_rq2.ipynb     # RQ2 cluster-adaptive prompting results & Holm contrasts
│   ├── 04_factorial_ablation_rq3.ipynb    # RQ3 2x2 factorial ANOVA (Rules x Prompting) & dual-judge kappa
│   └── 05_turn_economy_rq4.ipynb          # RQ4 2x3 multi-turn simulation & persona fidelity check
├── outputs/
│   ├── interim/                    # Tables (CSV) and figures (PNG) from Steps 0–4 and 2b–2i
│   └── final/                      # Tables (CSV) and publication figures (PNG) for EDA, Architecture, RQ2, RQ3, & RQ4
├── interim/
│   └── QM_640_Interim_Report_Sandeep_Surnella.pdf
├── final/
│   ├── QM_640_Final_Report_Sandeep_Surnella.docx
│   └── QM_640_Final_Report_Sandeep_Surnella.pdf
├── requirements.txt                # Pinned Python 3.11 dependencies
└── README.md                       # Project documentation and replication guide
```

---

## 3. End-to-End Replication Instructions

All random operations are seeded (`SEED = 42`), and every LLM generation and annotation call is persisted in JSONL caches under `data/interim/` and `data/final/` so that full re-runs execute deterministically without redundant API calls.

```bash
# 1. Create Python 3.11 virtual environment and install dependencies
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Run Foundations & RQ1 Pipeline (Steps 0–4 and Sensitivity Steps 2b–2i)
python src/interim_pipeline/step0_sample_size.py
python src/interim_pipeline/step1_prepare_data.py
python src/interim_pipeline/step2_rq1_clustering.py
python src/interim_pipeline/step2g_rq1_truncation.py
python src/interim_pipeline/step2h_rq1_ablation.py
python src/interim_pipeline/step2i_rq1_refined_archetypes.py
python src/interim_pipeline/step3_rq2_pipeline.py --execute
python src/interim_pipeline/step4_rq3_rq4_groundwork.py

# 3. Run Final Empirical Pipeline (Refined RQ1 Routing, Refined RQ2, RQ3 2x2, RQ4 2x3, and EDA/Architecture Figures)
python src/final_pipeline/test_step1_harness.py
python src/final_pipeline/step2_rq2_refined.py --execute
python src/final_pipeline/step3_rq3_experiment.py --execute
python src/final_pipeline/step4_rq4_simulation.py --execute
python src/final_pipeline/step5_figures_and_eda.py

# 4. Build Submission-Ready Final Report (.docx and .pdf)
python src/build_final_report.py
```

---

## 4. Summary of Empirical Findings Across RQ1–RQ4

| Research Question | Experimental Design & Sample | Primary Statistical Result | Hypothesis Outcome |
| :--- | :--- | :--- | :--- |
| **RQ1: Dialogue Clustering & Refined User Archetypes** | $N = 159$ subsample runs ($n=53$ per algorithm on $D_{\text{gold}} = 933$) + representation $\times$ truncation grid ($M \in \{3,5,7,9,\text{whole}\}$) | Primary ANOVA: $F(2, 156) = 321.18, p < .001, \eta^2 = .805$ (Gemini embeddings: $F = 813.09, p < .001, \eta^2 = .912$). Refined $k=3$ solution at $M=9$ (*Decisive Booker*, *Open Explorer*, *Rigid-Constraint Seeker*) achieves bootstrap $\text{ARI} = .76$, $74.8\%$ core membership, and held-out `Blocks` prefix routing $\kappa = .359$ ($M=3$), $.535$ ($M=5$), $.722$ ($M=7$), and **$.958$ ($97.3\%$ accuracy) at $M=9$**. | **$H_{01}$ Rejected** ($p < .001$) |
| **RQ2: Cluster-Adaptive Few-Shot Prompting** | Repeated-measures $1 \times 3$ design ($N = 33$ held-out dialogues $\times 3$ conditions = 99 generations) on Refined Archetypes | Style convergence (`sbert_style_cos`): RM-ANOVA $F(1.88, 60.29) = 9.79, p < .001, \eta_p^2 = .234$ (Friedman $\chi^2(2) = 12.50, p = .002$). `Cluster-Adaptive` ($M = .597, SD = .086$) outperforms `Static Few-Shot` ($M = .453, p_{\text{Holm}} < .001, d_z = 0.74$) and `Zero-Shot` ($M = .530, p_{\text{Holm}} = .049, d_z = 0.41$). Pacing error drops from $10.12$ (`Zero-Shot`) and $6.33$ (`Static`) to **$3.87$ words** ($F = 7.10, p = .007$). | **$H_{02}$ Rejected** on Refined Archetypes ($p < .001$) |
| **RQ3: Declarative Rule Engine $\times$ Prompting** | $2 \times 2$ between-subjects factorial experiment ($N = 144$, $n = 36$ per cell); dual-judge reliability $n = 48$ (`gemini-2.5-flash` vs. `gemini-2.5-pro`, $\kappa = .917$) | **Rule Adherence**: Main effect of Rules $F(1, 140) = 43.92, p < .001, \eta_p^2 = .239$ (violating-scenario enforcement leaps from **$5.6\%$ to $98.6\%$**). **Exemplar Leakage**: Rules $\times$ Prompting interaction $F(1, 140) = 34.82, p < .001, \eta_p^2 = .199$ (ART $F = 2148.81, p < .001$), eliminating the $35.9\%$ entity leakage of unguarded few-shot prompting (**$0.0\%$ leakage** under `Rules Active`). **Slot F1**: Main effect of Rules $F(1, 140) = 489.52, p < .001, \eta_p^2 = .778$ ($.485 \to .952$) while preserving style alignment ($M = .506, F_{\text{prompt}} = 24.00, p < .001$). | **$H_{03}$ Rejected** ($p < .001$) |
| **RQ4: Multi-Turn Turn Economy Across Archetypes** | $2 \times 3$ between-subjects factorial simulation ($N = 180$, $n = 30$ per cell); persona fidelity validation $n = 45$ (`gemini-2.5-pro`, $95.6\%$ accuracy, $\kappa = .933, p < .001$) | **Log Turns to Goal Completion**: Main effect of Prompting $F(1, 174) = 664.43, p < .001, \eta_p^2 = .793$; **Prompting $\times$ Archetype Interaction $F(2, 174) = 10.89, p < .001, \eta_p^2 = .111$** (HC3 $F = 8.58, p < .001$). Turn reductions: **$-42.7\%$** for *Rigid-Constraint Seeker* ($8.73 \to 5.00$ turns), **$-34.2\%$** for *Decisive Booker* ($7.60 \to 5.00$ turns), and **$-29.5\%$** for *Open Explorer* ($7.47 \to 5.27$ turns). **Redundant Elicitation Rate (RER)** drops from $M = .109$ (`Zero-Shot`) to **$0.000$** ($F(1, 174) = 63.02, p < .001, \eta_p^2 = .266$). | **$H_{04}$ Rejected** ($p < .001$) |
