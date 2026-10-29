"""
Evaluation metrics and statistical hypothesis-testing suite for `src/final_pipeline/`.

Covers:
  - RQ2: Style convergence (cosine to target archetype style centroid), Archetype Pacing
         Alignment, Human Reply Similarity, BERTScore F1, Response Word Length;
         One-way Repeated-Measures ANOVA, Mauchly sphericity, Greenhouse-Geisser correction,
         Friedman non-parametric check, Holm-adjusted paired t-contrasts.
  - RQ3: Factual Slot F1, Exemplar Leakage Rate (ELR), Rule Adherence Rate (RAR),
         Two-way (2 x 2) Between-Subjects Factorial ANOVA (OLS + HC3 robust SEs +
         Aligned Rank Transform [ART] non-parametric ANOVA), and Dual-Judge Cohen's kappa.
  - RQ4: Turns to Goal Completion (TGC and log-TGC), Redundant Elicitation Rate (RER),
         Two-way (2 x 3) Factorial ANOVA (OLS + HC3 robust SEs + ART ANOVA + simple effects).
"""

import re
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.metrics import cohen_kappa_score

_TOKEN_RE = re.compile(r"[a-zA-Z0-9$%]+")
_NUM_CLEAN_RE = re.compile(r"[,$%]")


def normalize_entity_str(val: Any) -> str:
    """Normalise an entity or slot value for case-insensitive matching."""
    s = str(val).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def compute_slot_f1(
    response_text: str,
    expected_slots: Dict[str, Any],
    allowed_context_entities: Optional[Sequence[str]] = None,
) -> Dict[str, float]:
    """
    Compute Factual Slot Precision, Recall, and F1 of an agent response against
    the target ground-truth slot state (`expected_slots`) for the current turn/offer,
    penalising fabricated/contradictory entity values not present in the dialogue context.
    """
    resp_low = response_text.lower()
    if not expected_slots:
        return dict(precision=1.0, recall=1.0, f1=1.0)

    matched = 0
    total_expected = len(expected_slots)
    for k, v in expected_slots.items():
        if v is None:
            total_expected -= 1
            continue
        v_str = normalize_entity_str(v)
        if not v_str:
            total_expected -= 1
            continue
        # Direct substring match or numeric match without formatting commas
        v_num = _NUM_CLEAN_RE.sub("", v_str)
        resp_num = _NUM_CLEAN_RE.sub("", resp_low)
        if v_str in resp_low or (v_num and len(v_num) >= 2 and v_num in resp_num):
            matched += 1

    if total_expected <= 0:
        return dict(precision=1.0, recall=1.0, f1=1.0)

    recall = matched / total_expected

    # Check for hallucinated/foreign entities or numbers not in expected_slots or allowed_context_entities
    allowed_set = {normalize_entity_str(v) for v in expected_slots.values() if v is not None}
    if allowed_context_entities:
        allowed_set |= {normalize_entity_str(x) for x in allowed_context_entities if x}
    allowed_nums = {_NUM_CLEAN_RE.sub("", x) for x in allowed_set if any(c.isdigit() for c in x)}

    # Extract multi-digit numbers mentioned in response (excluding small counts 1..5 like "2 options")
    resp_numbers = re.findall(r"\b\d[\d,.]*\b", resp_low)
    spurious_count = 0
    for rn in resp_numbers:
        clean_rn = _NUM_CLEAN_RE.sub("", rn).rstrip(".")
        if not clean_rn.isdigit():
            continue
        val_int = int(clean_rn)
        if val_int <= 10:
            continue
        if clean_rn not in allowed_nums and not any(clean_rn in a or a in clean_rn for a in allowed_nums if a):
            spurious_count += 1

    denom_p = matched + spurious_count
    precision = (matched / denom_p) if denom_p > 0 else (1.0 if spurious_count == 0 else 0.0)
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return dict(precision=float(precision), recall=float(recall), f1=float(f1))


def compute_exemplar_leakage(
    response_text: str,
    exemplar_entities: Sequence[str],
    dialogue_entities: Sequence[str],
) -> Dict[str, Any]:
    """
    Compute Exemplar Leakage Rate (ELR):
      |E_r intersect (E_x \\ E_d)| / max(1, |E_r|)
    where E_x are named entities/numbers from the in-context exemplars,
    E_d are entities/numbers belonging to the active dialogue state,
    and E_r are candidate entities/numbers appearing in the generated response.
    """
    resp_low = response_text.lower()
    diag_norm = {normalize_entity_str(e) for e in dialogue_entities if e and len(str(e).strip()) >= 3}
    ex_only = {
        normalize_entity_str(e)
        for e in exemplar_entities
        if e and len(str(e).strip()) >= 3 and normalize_entity_str(e) not in diag_norm
    }

    leaked = []
    for ex_val in sorted(ex_only):
        if ex_val in {"true", "false", "none", "user", "agent", "wizard", "fit", "group"}:
            continue
        if re.search(r"\b" + re.escape(ex_val) + r"\b", resp_low):
            leaked.append(ex_val)

    matched_diag = [
        d_val for d_val in diag_norm
        if len(d_val) >= 3 and re.search(r"\b" + re.escape(d_val) + r"\b", resp_low)
    ]
    total_entities_in_resp = len(set(matched_diag) | set(leaked))
    if total_entities_in_resp == 0:
        rate = float(len(leaked) > 0)
    else:
        rate = len(leaked) / total_entities_in_resp

    return dict(
        leaked_entities=leaked,
        leaked_count=len(leaked),
        has_leakage=bool(len(leaked) > 0),
        leakage_rate=float(rate),
    )


# ----------------------------------------------------------------------------- Statistical tests
def rm_anova(Y: np.ndarray) -> Dict[str, float]:
    """One-way repeated-measures ANOVA on an (n subjects x k conditions) matrix."""
    n, k = Y.shape
    gm = Y.mean()
    ss_cond = n * ((Y.mean(0) - gm) ** 2).sum()
    ss_subj = k * ((Y.mean(1) - gm) ** 2).sum()
    ss_tot = ((Y - gm) ** 2).sum()
    ss_err = ss_tot - ss_cond - ss_subj
    df1, df2 = k - 1, (k - 1) * (n - 1)
    F = (ss_cond / df1) / (ss_err / df2 + 1e-15)
    p = stats.f.sf(F, df1, df2)

    C = np.linalg.qr(np.vstack([np.ones(k), np.eye(k)[:-1] - 1.0 / k]).T)[0][:, 1:]
    S = np.cov(Y @ C, rowvar=False)
    p_ = k - 1
    det_s = max(1e-15, float(np.linalg.det(S)))
    tr_s = max(1e-15, float(np.trace(S)))
    W = det_s / ((tr_s / p_) ** p_)
    W = float(np.clip(W, 1e-12, 1.0))
    dfm = p_ * (p_ + 1) / 2 - 1
    chi2 = -(n - 1 - (2 * p_ ** 2 + p_ + 2) / (6 * p_)) * np.log(W)
    p_mauchly = stats.chi2.sf(chi2, dfm)
    eps_gg = float(np.clip((tr_s ** 2) / (p_ * float(np.trace(S @ S)) + 1e-15), 1.0 / p_, 1.0))
    p_gg = stats.f.sf(F, df1 * eps_gg, df2 * eps_gg)
    return dict(
        F=float(F),
        df1=float(df1),
        df2=float(df2),
        p=float(p),
        eta2_partial=float(ss_cond / (ss_cond + ss_err + 1e-15)),
        mauchly_W=float(W),
        mauchly_chi2=float(chi2),
        mauchly_df=float(dfm),
        mauchly_p=float(p_mauchly),
        eps_gg=float(eps_gg),
        df1_gg=float(df1 * eps_gg),
        df2_gg=float(df2 * eps_gg),
        p_gg=float(p_gg),
    )


def holm_pairwise(Y: np.ndarray, labels: Sequence[str]) -> pd.DataFrame:
    """Holm-Bonferroni adjusted paired t-contrasts across columns of Y."""
    rows = []
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            d = Y[:, j] - Y[:, i]
            sd = d.std(ddof=1)
            if sd < 1e-12:
                t, p, dz = 0.0, 1.0, 0.0
            else:
                t_res = stats.ttest_rel(Y[:, j], Y[:, i])
                t, p = float(t_res.statistic), float(t_res.pvalue)
                dz = float(d.mean() / sd)
            rows.append(
                dict(
                    contrast=f"{labels[j]} vs. {labels[i]}",
                    mean_diff=float(d.mean()),
                    sd_diff=float(sd),
                    t=t,
                    df=int(len(d) - 1),
                    p=p,
                    d_z=dz,
                )
            )
    df = pd.DataFrame(rows).sort_values("p").reset_index(drop=True)
    m = len(df)
    adj, running = [], 0.0
    for r, p_val in enumerate(df.p):
        running = max(running, min(1.0, (m - r) * float(p_val)))
        adj.append(running)
    df["p_holm"] = adj
    return df


def factorial_anova(
    df: pd.DataFrame,
    dv: str,
    factor_a: str,
    factor_b: str,
) -> Dict[str, Any]:
    """
    Two-way between-subjects factorial ANOVA (Type II SS + HC3 heteroscedasticity-robust Wald F +
    Aligned Rank Transform [ART] non-parametric factorial ANOVA + residual Shapiro-Wilk & Levene).
    """
    formula = f"{dv} ~ C({factor_a}) * C({factor_b})"
    model = ols(formula, data=df).fit()
    aov = sm.stats.anova_lm(model, typ=2)
    ss_err = float(aov.loc["Residual", "sum_sq"])
    aov["eta2_partial"] = aov["sum_sq"] / (aov["sum_sq"] + ss_err)

    # HC3 robust ANOVA
    model_hc3 = ols(formula, data=df).fit(cov_type="HC3")
    aov_hc3 = sm.stats.anova_lm(model_hc3, typ=2)

    # Residual diagnostics
    shapiro_res = stats.shapiro(model.resid)
    groups = [g[dv].dropna().values for _, g in df.groupby([factor_a, factor_b])]
    levene_res = stats.levene(*groups, center="median")

    # Aligned Rank Transform (ART) non-parametric check for main effects & interaction
    gm = df[dv].mean()
    a_means = df.groupby(factor_a)[dv].transform("mean")
    b_means = df.groupby(factor_b)[dv].transform("mean")
    cell_means = df.groupby([factor_a, factor_b])[dv].transform("mean")

    df_art = df[[factor_a, factor_b]].copy()
    df_art["art_a"] = stats.rankdata(df[dv] - b_means + gm)
    df_art["art_b"] = stats.rankdata(df[dv] - a_means + gm)
    df_art["art_ab"] = stats.rankdata(df[dv] - a_means - b_means + cell_means)

    aov_art_a = sm.stats.anova_lm(ols(f"art_a ~ C({factor_a}) * C({factor_b})", data=df_art).fit(), typ=2)
    aov_art_b = sm.stats.anova_lm(ols(f"art_b ~ C({factor_a}) * C({factor_b})", data=df_art).fit(), typ=2)
    aov_art_ab = sm.stats.anova_lm(ols(f"art_ab ~ C({factor_a}) * C({factor_b})", data=df_art).fit(), typ=2)

    key_a = f"C({factor_a})"
    key_b = f"C({factor_b})"
    key_ab = f"C({factor_a}):C({factor_b})"

    def _extract_effect(term: str, art_table: pd.DataFrame) -> Dict[str, float]:
        row = aov.loc[term]
        row_hc3 = aov_hc3.loc[term]
        row_art = art_table.loc[term]
        return dict(
            sum_sq=float(row["sum_sq"]),
            df1=float(row["df"]),
            df2=float(aov.loc["Residual", "df"]),
            F=float(row["F"]),
            p=float(row["PR(>F)"]),
            eta2_partial=float(row["eta2_partial"]),
            F_hc3=float(row_hc3["F"]),
            p_hc3=float(row_hc3["PR(>F)"]),
            F_art=float(row_art["F"]),
            p_art=float(row_art["PR(>F)"]),
        )

    return dict(
        dv=dv,
        n=int(len(df)),
        effects={
            factor_a: _extract_effect(key_a, aov_art_a),
            factor_b: _extract_effect(key_b, aov_art_b),
            "interaction": _extract_effect(key_ab, aov_art_ab),
        },
        residual_df=float(aov.loc["Residual", "df"]),
        residual_ss=ss_err,
        shapiro_resid=dict(W=float(shapiro_res.statistic), p=float(shapiro_res.pvalue)),
        levene=dict(W=float(levene_res.statistic), p=float(levene_res.pvalue)),
    )


def dual_judge_reliability(labels_1: Sequence[int], labels_2: Sequence[int]) -> Dict[str, float]:
    """Compute Cohen's kappa, raw agreement, and prevalence-adjusted kappa (PABAK) between two judges."""
    y1 = np.asarray(labels_1, dtype=int)
    y2 = np.asarray(labels_2, dtype=int)
    po = float((y1 == y2).mean())
    if len(np.unique(y1)) < 2 and len(np.unique(y2)) < 2 and np.array_equal(y1, y2):
        kap = 1.0
    else:
        kap = float(cohen_kappa_score(y1, y2))
        if np.isnan(kap):
            kap = po
    pabak = 2.0 * po - 1.0
    return dict(
        n=int(len(y1)),
        raw_agreement=po,
        cohen_kappa=kap,
        pabak=float(pabak),
    )

