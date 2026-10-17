# Personalized and Context-Adaptive Conversational AI Through Goal-Oriented Dialogue Clustering, Dynamic Few-Shot Prompting, and Decoupled Declarative Verification

**Course**: QM640 - Data Analytics Capstone  
**Institution**: Walsh College  
**Student**: Surnella Sandeep  
**Faculty Mentor**: Prof. Javad Katibai & Academic Advisory Committee  
**GitHub Repository**: [https://github.com/surnella/QM640-Dialogue-Clustering-Capstone](https://github.com/surnella/QM640-Dialogue-Clustering-Capstone)

---

## 1. Project Overview & Research Architecture
State-of-the-art commercial conversational AI systems in consultative domains (such as travel advisory and package booking) rely primarily on static, one-size-fits-all prompts. This creates conversational friction, repetitive turns, and high session abandonment when interacting across heterogeneous user archetypes (hesitant first-time buyers vs. fast corporate planners). Conversely, naive prompt-based style steering introduces severe factual hallucinations, exemplar leakage, and policy violations.

This project delivers a four-stage data-driven framework:
1. **Unsupervised Trajectory Clustering (RQ1)**: Identifies 3 distinct conversational behavioral archetypes (*Hesitant Explorer / Consultative*, *Budget Negotiator / Value-Conscious*, and *Rapid Transactional / Corporate*) from multi-turn dialogues embedded via Sentence-BERT with temporal decay pooling.
2. **Dynamic In-Context Few-Shot Style Convergence (RQ2)**: Retrieves archetype-matched golden exemplars via FAISS vector indexing with slot masking to steer agent tone and pacing dynamically without model fine-tuning.
3. **Decoupled Declarative Rule Verification (RQ3)**: Interposes external deterministic policy checks (e.g., minimum 15-day visa lead times, passport validity > 6 months, adult pax limits) preventing policy drift and eliminating factual exemplar leakage.
4. **Dialogue Turn Economy Optimization (RQ4)**: Reduces redundant elicitation questions and achieves 19–24% reductions in Turns to Goal Completion (TGC).

---

## 2. Repository Layout

```
QM640-Dialogue-Clustering-Capstone/
├── data/
│   ├── raw/                 # Microsoft Frames, MultiWOZ 2.2 corpora
│   ├── canonical/           # Normalized 2-tier canonical dialogue trajectories (2,893 dialogues)
│   ├── embeddings/          # 384-dim S-BERT trajectory embeddings & cluster metadata
│   └── enterprise_sample/   # 102 PII-sanitized golden enterprise counseling sessions
├── notebooks/
│   ├── 01_eda_and_cleaning.ipynb          # Exploratory data analysis & cleaning logs
│   ├── 02_trajectory_clustering_rq1.ipynb # RQ1 K-Means, Agglomerative, HDBSCAN ANOVA
│   ├── 03_fewshot_retrieval_rq2.ipynb     # RQ2 FAISS vector indexing & style convergence
│   ├── 04_factorial_ablation_rq3.ipynb    # RQ3 2x2 Factorial ANOVA (Rules vs. Drift)
│   └── 05_turn_economy_rq4.ipynb          # RQ4 Turn economy & friction statistics
├── src/
│   ├── canonical_schema.py  # Pydantic schemas for Tier-1 and Tier-2 slots
│   ├── ingestion.py         # Microsoft Frames, MultiWOZ 2.2, and Enterprise parsers
│   ├── vectorizer.py        # S-BERT embeddings with temporal decay pooling
│   ├── clustering.py        # K-Means, Agglomerative, HDBSCAN pipelines & ANOVA testing
│   ├── faiss_index.py       # FAISS L2/Cosine vector indexing for exemplar retrieval
│   ├── prompt_assembler.py  # Dynamic few-shot prompt construction with slot masking
│   ├── rule_engine.py       # Decoupled declarative business rule validator
│   └── evaluation.py        # Hypothesis testing & evaluation harnesses (RQ2, RQ3, RQ4)
├── rules/
│   └── rules_enterprise.yaml # Declarative business constraints (visa, passport, pax, budget)
├── outputs/
│   ├── figures/             # UMAP projections, Silhouette plots, style convergence charts
│   └── tables/              # Exported ANOVA summary tables and CSV evaluation logs
├── requirements.txt         # Pinned Python package dependencies
├── README.md                # Project documentation and replication guide
└── docs/                    # Capstone guidelines, rubric checklists, and templates
```

---

## 3. Quickstart & Replication Instructions

To replicate all data ingestion, trajectory vectorization, clustering, and evaluation pipelines:

```bash
# 1. Clone repository
git clone https://github.com/surnella/QM640-Dialogue-Clustering-Capstone.git
cd QM640-Dialogue-Clustering-Capstone

# 2. Install dependencies
pip install -r requirements.txt

# 3. Ingest and canonicalize dialogue datasets
python src/ingestion.py

# 4. Generate dense trajectory embeddings with temporal decay pooling
python src/vectorizer.py

# 5. Run RQ1 clustering analysis and hypothesis testing
python src/clustering.py

# 6. Run RQ2, RQ3, and RQ4 evaluation pipelines
python src/evaluation.py
```

---

## 4. Key Empirical Findings (Interim Report Stage)

### RQ1: Unsupervised Trajectory Clustering Quality
* **ANOVA Test**: $F(2, 153) = 37.36, p = 6.13 \times 10^{-14}, \eta^2 = 0.328$ (Statistically Significant at $p < .001$).
* **Model Separation**: Agglomerative Hierarchical ($s = 0.431$) and K-Means ($s = 0.426$) significantly outperformed HDBSCAN ($s = 0.360, p < .001$).
* **Discovered Archetypes**:
  1. *Hesitant Explorer / Consultative*: Mean 17.7 turns, 2.66 hesitation markers, 3.68 revisions.
  2. *Budget Negotiator / Value-Conscious*: Mean 16.1 turns, 16.87 revisions, 72.8% budget constraint focus.
  3. *Rapid Transactional / Corporate*: Mean 15.0 turns, 0.19 revisions, 0.89 hesitation markers, rapid slot saturation.

### RQ2: Dynamic In-Context Style Convergence
* **ANOVA Test**: $F(2, 123) = 58.28, p = 1.57 \times 10^{-18}, \eta^2 = 0.487$ (Statistically Significant at $p < .001$).
* **Pairwise Comparison (Tukey HSD)**:
  * Cluster-Adaptive Few-Shot ($\mu = 0.884$) significantly outperformed Static Few-Shot ($\mu = 0.772$, difference $+0.112, p < .001$) and Zero-Shot Baseline ($\mu = 0.705$, difference $+0.179, p < .001$).
* **Null Hypothesis**: Decisively rejected ($H_0: \mu_{\text{cluster}} = \mu_{\text{baseline}}$); dynamic few-shot conditioning steers agent pacing towards target reference archetypes.

### RQ3 Groundwork: Rules vs. Drift Factorial Ablation
* Unconstrained Cluster Few-Shot without rules exhibits an **Exemplar Factual Leakage Rate of 14.2%** and rule adherence of 68.4%.
* Activating the Decoupled Declarative Rule Engine achieves **97.7% Rule Adherence** and suppresses leakage to **1.5%** while maintaining superior Factual Slot F1 (**0.932**).

### RQ4 Groundwork: Turn Economy & Friction Analysis
* Cluster-adaptive prompting delivers significant turn efficiency gains:
  * **Hesitant Explorer**: 24.4% turn reduction (21.4 $\to$ 16.2 turns).
  * **Budget Negotiator**: 22.6% turn reduction (15.8 $\to$ 12.1 turns).
  * **Rapid Transactional**: 19.3% turn reduction (7.2 $\to$ 5.8 turns).
* Redundant Elicitation Rate (RER) drops from **14–18%** down to **1–3%**.
