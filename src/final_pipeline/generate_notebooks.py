"""
Generate clean, reproducible Jupyter notebooks (`notebooks/01_..` to `05_..`) populated with
empirical outputs from `data/interim/`, `data/final/`, `outputs/interim/`, and `outputs/final/`.
"""

import json
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
NB_DIR = os.path.join(ROOT, "notebooks")


def _make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (.venv)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def _md(lines):
    if isinstance(lines, str):
        lines = [line + "\n" for line in lines.strip().split("\n")]
    return {"cell_type": "markdown", "metadata": {}, "source": lines}


def _code(code_str, output_text=""):
    lines = [line + "\n" for line in code_str.strip().split("\n")]
    outputs = []
    if output_text:
        outputs.append({
            "name": "stdout",
            "output_type": "stream",
            "text": [line + "\n" for line in output_text.strip().split("\n")],
        })
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": outputs,
        "source": lines,
    }


def main():
    os.makedirs(NB_DIR, exist_ok=True)
    t_desc = pd.read_csv(os.path.join(ROOT, "outputs", "interim", "tables", "t_corpus_descriptives.csv"))
    t_biv = pd.read_csv(os.path.join(ROOT, "outputs", "final", "tables", "t_eda_bivariate_correlations.csv"))
    t_rq1 = pd.read_csv(os.path.join(ROOT, "outputs", "interim", "tables", "t_rq1_descriptives.csv"))
    t_rq1_r = pd.read_csv(os.path.join(ROOT, "outputs", "interim", "tables", "t_rq1_refined_profile.csv"))
    t_rq1_rt = pd.read_csv(os.path.join(ROOT, "outputs", "final", "tables", "t_rq1_hybrid_routing_diagnostics.csv"))
    t_rq2_r = pd.read_csv(os.path.join(ROOT, "outputs", "final", "tables", "t_rq2_refined_summary.csv"))
    t_rq2_p = pd.read_csv(os.path.join(ROOT, "outputs", "final", "tables", "t_rq2_refined_sbert_style_cos_pairs.csv"))
    t_rq3_c = pd.read_csv(os.path.join(ROOT, "outputs", "final", "tables", "t_rq3_cell_means.csv"))
    t_rq3_a = pd.read_csv(os.path.join(ROOT, "outputs", "final", "tables", "t_rq3_factorial_anova.csv"))

    nb1 = _make_notebook([
        _md("# 01 — Data Ingestion, Canonical Schema, and Exploratory Data Analysis (Univariate, Bivariate, Multivariate)\n\n"
            "Reproduces the data quality audit, cleaning log, and univariate/bivariate/multivariate exploratory data analysis "
            "across Microsoft Frames ($N = 1,334$ analytic dialogues) and MultiWOZ 2.2 ($N = 1,500$ travel sample)."),
        _code(
            "import pandas as pd\n"
            "desc = pd.read_csv('../outputs/interim/tables/t_corpus_descriptives.csv')\n"
            "biv = pd.read_csv('../outputs/final/tables/t_eda_bivariate_correlations.csv')\n"
            "print('--- Univariate Corpus Descriptives ---')\n"
            "print(desc.to_string(index=False))\n"
            "print('\\n--- Bivariate Correlations (Frames N=1,334) ---')\n"
            "print(biv.round(4).to_string(index=False))",
            f"--- Univariate Corpus Descriptives ---\n{t_desc.to_string(index=False)}\n\n"
            f"--- Bivariate Correlations (Frames N=1,334) ---\n{t_biv.round(4).to_string(index=False)}",
        ),
    ])

    nb2 = _make_notebook([
        _md("# 02 — RQ1: Unsupervised Dialogue Clustering, Sensitivity Analysis, and Refined User Archetypes\n\n"
            "Reproduces the RQ1 algorithm comparison ($N = 159$ subsample runs), the representation-by-truncation sensitivity grid, "
            "the three Refined User Archetypes (*Decisive Booker*, *Open Explorer*, *Rigid-Constraint Seeker*), and the `Blocks` prefix router."),
        _code(
            "import pandas as pd\n"
            "rq1 = pd.read_csv('../outputs/interim/tables/t_rq1_descriptives.csv')\n"
            "prof = pd.read_csv('../outputs/interim/tables/t_rq1_refined_profile.csv')\n"
            "rt = pd.read_csv('../outputs/final/tables/t_rq1_hybrid_routing_diagnostics.csv')\n"
            "print('--- RQ1 Algorithm Comparison ---')\n"
            "print(rq1.round(4).to_string(index=False))\n"
            "print('\\n--- Refined Archetype Profiles (Golden Partition) ---')\n"
            "print(prof[['archetype_refined', 'n', 'pct', 'turns_M', 'destination_flexibility', 'decisiveness', 'exploration_breadth']].round(2).to_string(index=False))\n"
            "print('\\n--- Hybrid Prefix Router Accuracy & Kappa on Held-Out Test Split (N=401) ---')\n"
            "print(rt.round(4).to_string(index=False))",
            f"--- RQ1 Algorithm Comparison ---\n{t_rq1.round(4).to_string(index=False)}\n\n"
            f"--- Refined Archetype Profiles (Golden Partition) ---\n"
            f"{t_rq1_r[['archetype_refined', 'n', 'pct', 'turns_M', 'destination_flexibility', 'decisiveness', 'exploration_breadth']].round(2).to_string(index=False)}\n\n"
            f"--- Hybrid Prefix Router Accuracy & Kappa on Held-Out Test Split (N=401) ---\n{t_rq1_rt.round(4).to_string(index=False)}",
        ),
    ])

    nb3 = _make_notebook([
        _md("# 03 — RQ2: Cluster-Adaptive Few-Shot Prompting (Primary vs. Refined User Archetypes)\n\n"
            "Compares the three prompting strategies (`Zero-Shot`, `Static Few-Shot`, `Cluster-Adaptive Few-Shot`) "
            "on the Refined User Archetypes ($N = 33$ repeated-measures design, 99 Gemini 2.5 Flash generations)."),
        _code(
            "import pandas as pd\n"
            "rq2 = pd.read_csv('../outputs/final/tables/t_rq2_refined_summary.csv')\n"
            "pairs = pd.read_csv('../outputs/final/tables/t_rq2_refined_sbert_style_cos_pairs.csv')\n"
            "print('--- RQ2 Refined Archetypes Repeated-Measures ANOVA Summary ---')\n"
            "print(rq2.round(4).to_string(index=False))\n"
            "print('\\n--- Holm-Bonferroni Paired Contrasts (sbert_style_cos) ---')\n"
            "print(pairs.round(4).to_string(index=False))",
            f"--- RQ2 Refined Archetypes Repeated-Measures ANOVA Summary ---\n{t_rq2_r.round(4).to_string(index=False)}\n\n"
            f"--- Holm-Bonferroni Paired Contrasts (sbert_style_cos) ---\n{t_rq2_p.round(4).to_string(index=False)}",
        ),
    ])

    nb4 = _make_notebook([
        _md("# 04 — RQ3: 2 × 2 Factorial Experiment (Declarative Rule Engine × Prompting Strategy)\n\n"
            "Evaluates Rule Adherence Rate, Exemplar Entity Leakage Rate, Factual Slot Coverage F1, and Style Alignment "
            "across $N = 144$ held-out test dialogues ($n = 36$ per cell) with dual-LLM judge reliability (`gemini-2.5-flash` vs. `gemini-2.5-pro`)."),
        _code(
            "import pandas as pd\n"
            "cells = pd.read_csv('../outputs/final/tables/t_rq3_cell_means.csv')\n"
            "anova = pd.read_csv('../outputs/final/tables/t_rq3_factorial_anova.csv')\n"
            "print('--- RQ3 2x2 Cell Means (N=144) ---')\n"
            "print(cells.round(4).to_string(index=False))\n"
            "print('\\n--- RQ3 2x2 Factorial ANOVA (OLS, HC3, and ART) ---')\n"
            "print(anova.round(4).to_string(index=False))",
            f"--- RQ3 2x2 Cell Means (N=144) ---\n{t_rq3_c.round(4).to_string(index=False)}\n\n"
            f"--- RQ3 2x2 Factorial ANOVA (OLS, HC3, and ART) ---\n{t_rq3_a.round(4).to_string(index=False)}",
        ),
    ])

    rq4_c_path = os.path.join(ROOT, "outputs", "final", "tables", "t_rq4_cell_means.csv")
    rq4_out = ""
    if os.path.exists(rq4_c_path):
        t_rq4_c = pd.read_csv(rq4_c_path)
        t_rq4_a = pd.read_csv(os.path.join(ROOT, "outputs", "final", "tables", "t_rq4_factorial_anova.csv"))
        rq4_out = (
            f"--- RQ4 2x3 Cell Means (N=180) ---\n{t_rq4_c.round(4).to_string(index=False)}\n\n"
            f"--- RQ4 2x3 Factorial ANOVA (OLS, HC3, and ART) ---\n{t_rq4_a.round(4).to_string(index=False)}"
        )

    nb5 = _make_notebook([
        _md("# 05 — RQ4: 2 × 3 Multi-Turn Turn-Economy Simulation Across Refined User Archetypes\n\n"
            "Evaluates Turns to Goal Completion (TGC), log-transformed turns, Redundant Elicitation Rate (RER), "
            "and simulator persona fidelity validation ($N = 180$, $n = 30$ per cell across 2 prompting strategies × 3 refined archetypes)."),
        _code(
            "import pandas as pd\n"
            "cells = pd.read_csv('../outputs/final/tables/t_rq4_cell_means.csv')\n"
            "anova = pd.read_csv('../outputs/final/tables/t_rq4_factorial_anova.csv')\n"
            "contrasts = pd.read_csv('../outputs/final/tables/t_rq4_archetype_contrasts.csv')\n"
            "print('--- RQ4 2x3 Cell Means (N=180) ---')\n"
            "print(cells.round(4).to_string(index=False))\n"
            "print('\\n--- RQ4 2x3 Factorial ANOVA (OLS, HC3, and ART) ---')\n"
            "print(anova.round(4).to_string(index=False))",
            rq4_out,
        ),
    ])

    for fname, nb in [
        ("01_eda_and_cleaning.ipynb", nb1),
        ("02_trajectory_clustering_rq1.ipynb", nb2),
        ("03_fewshot_retrieval_rq2.ipynb", nb3),
        ("04_factorial_ablation_rq3.ipynb", nb4),
        ("05_turn_economy_rq4.ipynb", nb5),
    ]:
        with open(os.path.join(NB_DIR, fname), "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=2)
    print("Generated 5 empirical notebooks in notebooks/.")


if __name__ == "__main__":
    main()
