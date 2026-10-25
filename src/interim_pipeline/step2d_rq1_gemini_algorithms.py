"""
Step 2d - RQ1 algorithm comparison repeated with Gemini embeddings (sensitivity analysis).

Identical protocol to step 2 (K-Means / agglomerative / HDBSCAN, 53 independent subsamples of
n = 500 golden dialogues each, k = 3, permutation baseline, ANOVA + Welch + Kruskal-Wallis), applied
to two Gemini representations of the whole dialogue (user + agent):
  G-pooled  decay-weighted mean of per-turn gemini-embedding-001 vectors (same pooling as MiniLM)
  G-doc     the whole conversation embedded as one document
Writes outputs/interim/tables/t_rq1_gemini_algorithms.csv and data/interim/rq1_gemini_summary.json.
"""

import json
import os
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.oneway import anova_oneway

from common import ROOT, SEED, TABLE_DIR, WORK_DIR, decay_weights
from step2_rq1_clustering import K, N_PER_ALGO, SUB_N, hdbscan_labels, score

warnings.filterwarnings("ignore")
GDIR = os.path.join(ROOT, "data", "embeddings", "gemini")
ALGOS = ["K-Means", "Agglomerative", "HDBSCAN"]


def pooled_full():
    flat, off = np.load(os.path.join(GDIR, "turn_emb.npy")), np.load(os.path.join(GDIR, "turn_offsets.npy"))
    out = []
    for i in range(len(off) - 1):
        E = flat[off[i]:off[i + 1]]
        v = (E * decay_weights(len(E))[:, None]).sum(0)
        out.append(v / (np.linalg.norm(v) + 1e-12))
    return np.array(out, dtype=np.float32)


def compare(Xg, label):
    rng = np.random.default_rng(SEED)
    k_rows = []
    for k in range(2, 7):
        km = KMeans(n_clusters=k, n_init=20, random_state=SEED).fit(Xg)
        k_rows.append(dict(rep=label, k=k, silhouette=silhouette_score(Xg, km.labels_, metric="cosine"),
                           smallest_cluster_pct=100 * np.bincount(km.labels_).min() / len(Xg)))
    recs, redraws, hk, hn = [], 0, [], []
    for algo in ALGOS:
        done = 0
        while done < N_PER_ALGO:
            idx = rng.choice(len(Xg), size=SUB_N, replace=False)
            Xs = Xg[idx]
            if algo == "K-Means":
                lab = KMeans(n_clusters=K, n_init=10, random_state=int(rng.integers(1e9))).fit_predict(Xs)
            elif algo == "Agglomerative":
                lab = AgglomerativeClustering(n_clusters=K, linkage="ward").fit_predict(Xs)
            else:
                lab, kk, ns = hdbscan_labels(Xs)
                if lab is None:
                    redraws += 1
                    if redraws > 300:
                        break
                    continue
                hk.append(kk)
                hn.append(ns)
            s, db = score(Xs, lab)
            recs.append(dict(rep=label, algorithm=algo, silhouette=s, davies_bouldin=db))
            done += 1
        print(f"{label} {algo}: {done} runs", flush=True)
    perm = []
    for i in range(N_PER_ALGO):
        idx = rng.choice(len(Xg), size=SUB_N, replace=False)
        lab = KMeans(n_clusters=K, n_init=5, random_state=i).fit_predict(Xg[idx])
        perm.append(silhouette_score(Xg[idx], rng.permutation(lab), metric="cosine"))
    de = pd.DataFrame(recs)
    algos_ok = [a for a in ALGOS if (de.algorithm == a).sum() == N_PER_ALGO]
    dd = de[de.algorithm.isin(algos_ok)]
    groups = [dd.loc[dd.algorithm == a, "silhouette"].values for a in algos_ok]
    res = dict(rep=label, algorithms=algos_ok, hdbscan_redraws=redraws,
               hdbscan_noise_M=float(np.mean(hn)) if hn else None,
               hdbscan_k=dict(pd.Series(hk).value_counts().sort_index().astype(int)) if hk else {},
               permutation_M=float(np.mean(perm)), permutation_SD=float(np.std(perm, ddof=1)),
               desc={a: dict(M=float(g.mean()), SD=float(g.std(ddof=1)),
                             DB_M=float(dd.loc[dd.algorithm == a, "davies_bouldin"].mean()))
                     for a, g in zip(algos_ok, groups)})
    if len(groups) >= 2:
        aov = anova_lm(ols("silhouette ~ C(algorithm)", data=dd).fit(), typ=2)
        ssb, ssw = aov["sum_sq"].iloc[0], aov["sum_sq"].iloc[1]
        w = anova_oneway(dd.silhouette, dd.algorithm, use_var="unequal")
        res.update(anova=dict(F=float(aov["F"].iloc[0]), df1=float(aov["df"].iloc[0]), df2=float(aov["df"].iloc[1]),
                              p=float(aov["PR(>F)"].iloc[0]), eta2=float(ssb / (ssb + ssw))),
                   welch=dict(F=float(w.statistic), p=float(w.pvalue)),
                   kruskal=dict(H=float(stats.kruskal(*groups).statistic), p=float(stats.kruskal(*groups).pvalue)),
                   levene_p=float(stats.levene(*groups, center="median").pvalue))
    return de, pd.DataFrame(k_rows), res


def main():
    df = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    gold = (df.partition == "gold").values
    reps = {"G-pooled": pooled_full()[gold],
            "G-doc": np.load(os.path.join(GDIR, "doc_full_all.npy"))[gold]}
    all_runs, all_k, summ = [], [], {}
    for lab, Xg in reps.items():
        de, dk, res = compare(Xg, lab)
        all_runs.append(de)
        all_k.append(dk)
        summ[lab] = res
    pd.concat(all_runs).to_csv(os.path.join(WORK_DIR, "rq1_gemini_subsample_scores.csv"), index=False)
    pd.concat(all_k).to_csv(os.path.join(TABLE_DIR, "t_rq1_gemini_k_selection.csv"), index=False)
    with open(os.path.join(WORK_DIR, "rq1_gemini_summary.json"), "w") as f:
        json.dump(summ, f, indent=2, default=lambda o: int(o) if isinstance(o, np.integer) else float(o))
    print(json.dumps(summ, indent=2, default=lambda o: int(o) if isinstance(o, np.integer) else float(o)))
    print(pd.concat(all_k).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
