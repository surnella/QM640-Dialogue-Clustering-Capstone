"""
Step 0 - A-priori sample size determination for RQ1-RQ4.

Every calculation uses the same verifiable rule: the smallest N for which the
power of the planned F test, computed from the noncentral F distribution, is at
least .80 at alpha = .05 (two-sided omnibus F) with Cohen's (1988) medium effect
f = 0.25. These are the formulas implemented by G*Power 3 (Faul et al., 2007).

    Fcrit = F^{-1}(1 - alpha; df1, df2)
    power = 1 - F_ncf(Fcrit; df1, df2, lambda)

Design-specific noncentrality and degrees of freedom:
    RQ1 one-way between-subjects ANOVA (k = 3):   lambda = f^2 N,                    df1 = 2, df2 = N - 3
    RQ2 one-way repeated-measures ANOVA (m = 3):  lambda = f^2 N m / (1 - rho) * eps, df1 = (m-1) eps, df2 = (N-1)(m-1) eps
    RQ3 2 x 2 between-subjects factorial ANOVA:   lambda = f^2 N,                    df1 = 1, df2 = N - 4
    RQ4 2 x 3 between-subjects factorial ANOVA:   lambda = f^2 N,                    df1 = 2, df2 = N - 6
"""

import json
import math
import os

import pandas as pd
from scipy import stats

from common import TABLE_DIR, WORK_DIR

ALPHA, POWER, F_EFFECT = 0.05, 0.80, 0.25
RHO, EPS, M_LEVELS = 0.50, 1.0, 3
BUFFER = 0.10  # generation-failure buffer for LLM-executed experiments (RQ2-RQ4)


def power_for(N, df1_fn, df2_fn, lam_fn):
    df1, df2, lam = df1_fn(N), df2_fn(N), lam_fn(N)
    if df2 <= 0:
        return 0.0, df1, df2, lam, float("nan")
    fcrit = stats.f.ppf(1 - ALPHA, df1, df2)
    return 1 - stats.ncf.cdf(fcrit, df1, df2, lam), df1, df2, lam, fcrit


def min_n(df1_fn, df2_fn, lam_fn, start=6):
    N = start
    while True:
        p, df1, df2, lam, fcrit = power_for(N, df1_fn, df2_fn, lam_fn)
        if p >= POWER:
            return N, p, df1, df2, lam, fcrit
        N += 1


def round_up(x, multiple):
    return int(math.ceil(x / multiple) * multiple)


def main():
    f2 = F_EFFECT ** 2
    designs = {
        "RQ1": dict(label="One-way ANOVA (3 algorithms)", groups=3, buffer=0.0,
                    df1=lambda N: 2, df2=lambda N: N - 3, lam=lambda N: f2 * N,
                    unit="bootstrap clustering runs"),
        "RQ2": dict(label="One-way repeated-measures ANOVA (3 conditions)", groups=3, buffer=BUFFER,
                    df1=lambda N: (M_LEVELS - 1) * EPS, df2=lambda N: (N - 1) * (M_LEVELS - 1) * EPS,
                    lam=lambda N: f2 * N * M_LEVELS / (1 - RHO) * EPS,
                    unit="test dialogues (each scored under all 3 conditions)"),
        "RQ3": dict(label="2 x 2 factorial ANOVA", groups=4, buffer=BUFFER,
                    df1=lambda N: 1, df2=lambda N: N - 4, lam=lambda N: f2 * N,
                    unit="test dialogues"),
        "RQ4": dict(label="2 x 3 factorial ANOVA", groups=6, buffer=BUFFER,
                    df1=lambda N: 2, df2=lambda N: N - 6, lam=lambda N: f2 * N,
                    unit="test dialogues"),
    }
    rows, detail = [], {}
    for rq, d in designs.items():
        N, p, df1, df2, lam, fcrit = min_n(d["df1"], d["df2"], d["lam"])
        balanced = round_up(N, d["groups"])
        buffered = round_up(balanced * (1 + d["buffer"]), d["groups"])
        p_final, *_ = power_for(buffered, d["df1"], d["df2"], d["lam"])
        detail[rq] = dict(design=d["label"], unit=d["unit"], N_min=N, power_at_N_min=p,
                          df1=df1, df2=df2, lambda_=lam, F_crit=fcrit,
                          N_balanced=balanced, buffer=d["buffer"], N_final=buffered,
                          per_group=buffered // d["groups"], power_final=p_final)
        rows.append({"RQ": rq, "Design": d["label"], "f": F_EFFECT, "alpha": ALPHA,
                     "df1": round(df1, 2), "df2_at_Nmin": round(df2, 2), "lambda_at_Nmin": round(lam, 3),
                     "F_crit": round(fcrit, 3), "N_min": N, "power_at_Nmin": round(p, 4),
                     "buffer": d["buffer"], "N_final": buffered, "per_group": buffered // d["groups"],
                     "power_final": round(p_final, 4), "unit": d["unit"]})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(TABLE_DIR, "t_sample_size.csv"), index=False)
    with open(os.path.join(WORK_DIR, "sample_size.json"), "w") as f:
        json.dump(detail, f, indent=2)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
