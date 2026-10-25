"""
Step 2 - RQ1: unsupervised trajectory clustering on the Frames golden partition.

Design (matches the one-way ANOVA power analysis, N = 159 = 3 x 53):
  * Each algorithm receives 53 *independent* subsamples (without replacement,
    n = 500) of D_gold, so the 159 Silhouette scores are independent units.
  * HDBSCAN subsamples that yield fewer than two clusters are redrawn (no
    imputed or synthetic scores); the redraw count is reported.
  * Assumptions are tested (Shapiro-Wilk, Levene). Welch ANOVA and
    Kruskal-Wallis are reported as robustness checks.
  * A label-permutation baseline gives the Silhouette expected with no structure.
  * Final archetypes: K-Means (k = 3) on all of D_gold; centroids are frozen and
    used to assign D_test and to project MultiWOZ 2.2 (cross-corpus check).
"""

import json
import os
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import HDBSCAN, AgglomerativeClustering, KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.oneway import anova_oneway

from common import FIG_DIR, SEED, TABLE_DIR, WORK_DIR

warnings.filterwarnings("ignore")
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                     "font.size": 11})

K = 3
N_PER_ALGO = 53
SUB_N = 500


def hdbscan_labels(X, mcs=5, ms=2):
    lab = HDBSCAN(min_cluster_size=mcs, min_samples=ms).fit_predict(X)
    valid = lab != -1
    if valid.sum() < 10 or len(set(lab[valid])) < 2:
        return None, 0, 1 - valid.mean()
    noise_share = 1 - valid.mean()
    clusters = sorted(set(lab[valid]))
    cents = np.array([X[lab == c].mean(axis=0) for c in clusters])
    noise = np.where(~valid)[0]
    if len(noise):
        d = ((X[noise, None, :] - cents[None, :, :]) ** 2).sum(-1)
        lab[noise] = np.array(clusters)[d.argmin(1)]
    return lab, len(clusters), noise_share


def score(X, lab):
    return silhouette_score(X, lab, metric="cosine"), davies_bouldin_score(X, lab)


def main():
    df = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    X_all = np.load(os.path.join(WORK_DIR, "frames_emb.npy"))
    gold = (df.partition == "gold").values
    Xg, dg = X_all[gold], df[gold].reset_index(drop=True)
    Xt, dt = X_all[~gold], df[~gold].reset_index(drop=True)
    X_mw = np.load(os.path.join(WORK_DIR, "multiwoz_emb.npy"))
    d_mw = pd.read_csv(os.path.join(WORK_DIR, "multiwoz_clean.csv"))

    # ---- k-selection diagnostics on full D_gold (K-Means) -------------------
    krows = []
    for k in range(2, 7):
        lab = KMeans(n_clusters=k, n_init=20, random_state=SEED).fit(Xg)
        s, db = score(Xg, lab.labels_)
        krows.append(dict(k=k, silhouette=s, davies_bouldin=db, inertia=lab.inertia_,
                          smallest_cluster_pct=100 * np.bincount(lab.labels_).min() / len(Xg)))
    dk = pd.DataFrame(krows)
    dk.to_csv(os.path.join(TABLE_DIR, "t_rq1_k_selection.csv"), index=False)

    # ---- independent subsample evaluation (N = 159) -------------------------
    rng = np.random.default_rng(SEED)
    # Diagnostic: default-style HDBSCAN setting (min_cluster_size = 15) on 53 subsamples
    default_fail = 0
    for _ in range(N_PER_ALGO):
        idx = rng.choice(len(Xg), size=SUB_N, replace=False)
        if hdbscan_labels(Xg[idx], 15, 5)[0] is None:
            default_fail += 1
    recs, hdb_redraws, hdb_k, hdb_noise = [], 0, [], []
    for algo in ["K-Means", "Agglomerative", "HDBSCAN"]:
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
                    hdb_redraws += 1
                    if hdb_redraws > 2000:
                        raise RuntimeError("HDBSCAN failed on too many subsamples")
                    continue
                hdb_k.append(kk)
                hdb_noise.append(ns)
            s, db = score(Xs, lab)
            recs.append(dict(algorithm=algo, run=done + 1, silhouette=s, davies_bouldin=db))
            done += 1
        print(f"{algo}: {done} subsamples scored", flush=True)
    de = pd.DataFrame(recs)
    de.to_csv(os.path.join(WORK_DIR, "rq1_subsample_scores.csv"), index=False)

    # Permutation baseline: K-Means labels shuffled within each subsample
    perm = []
    for i in range(N_PER_ALGO):
        idx = rng.choice(len(Xg), size=SUB_N, replace=False)
        lab = KMeans(n_clusters=K, n_init=5, random_state=i).fit_predict(Xg[idx])
        perm.append(silhouette_score(Xg[idx], rng.permutation(lab), metric="cosine"))

    # ---- assumptions + inferential tests -----------------------------------
    groups = [de.loc[de.algorithm == a, "silhouette"].values for a in ["K-Means", "Agglomerative", "HDBSCAN"]]
    shapiro = {a: stats.shapiro(g) for a, g in zip(["K-Means", "Agglomerative", "HDBSCAN"], groups)}
    levene = stats.levene(*groups, center="median")
    model = ols("silhouette ~ C(algorithm)", data=de).fit()
    aov = anova_lm(model, typ=2)
    ss_b, ss_w = aov["sum_sq"].iloc[0], aov["sum_sq"].iloc[1]
    eta2 = ss_b / (ss_b + ss_w)
    welch = anova_oneway(de.silhouette, de.algorithm, use_var="unequal")
    kw = stats.kruskal(*groups)
    tukey = pairwise_tukeyhsd(de.silhouette, de.algorithm, alpha=0.05)
    dtk = pd.DataFrame(tukey._results_table.data[1:], columns=tukey._results_table.data[0])
    dtk.to_csv(os.path.join(TABLE_DIR, "t_rq1_tukey.csv"), index=False)
    desc = de.groupby("algorithm").agg(n=("silhouette", "size"), sil_M=("silhouette", "mean"),
                                       sil_SD=("silhouette", "std"), db_M=("davies_bouldin", "mean"),
                                       db_SD=("davies_bouldin", "std")).reset_index()
    desc.to_csv(os.path.join(TABLE_DIR, "t_rq1_descriptives.csv"), index=False)
    aov_out = pd.DataFrame({"source": ["Algorithm", "Residual"], "SS": [ss_b, ss_w],
                            "df": aov["df"].values, "MS": aov["sum_sq"].values / aov["df"].values,
                            "F": [aov["F"].iloc[0], np.nan], "p": [aov["PR(>F)"].iloc[0], np.nan],
                            "eta2": [eta2, np.nan]})
    aov_out.to_csv(os.path.join(TABLE_DIR, "t_rq1_anova.csv"), index=False)

    # ---- final archetypes: K-Means k = 3 on all of D_gold --------------------
    km = KMeans(n_clusters=K, n_init=50, random_state=SEED).fit(Xg)
    dg["cluster"] = km.labels_
    cents = km.cluster_centers_ / np.linalg.norm(km.cluster_centers_, axis=1, keepdims=True)
    prof = dg.groupby("cluster").agg(n=("dialogue_id", "size"), turns_M=("total_turns", "mean"),
                                     turns_SD=("total_turns", "std"), user_words=("mean_user_words", "mean"),
                                     agent_words=("mean_agent_words", "mean"), revisions=("revisions", "mean"),
                                     hesitations=("hesitations", "mean"), offers=("offers", "mean"),
                                     budget_pct=("budget_specified", "mean"),
                                     success_pct=("task_success", lambda s: s.eq(True).mean()),
                                     rer=("rer_proxy", "mean")).reset_index()
    prof["pct"] = 100 * prof.n / prof.n.sum()
    prof["budget_pct"] *= 100
    prof["success_pct"] *= 100

    # Data-driven naming rule (documented in the report):
    #   most revisions per dialogue      -> "Constraint Negotiator"
    #   longest agent utterances / most offers among the rest -> "Guided Explorer"
    #   remaining (fewest turns)          -> "Direct Transactional"
    order = list(prof.sort_values("revisions", ascending=False).cluster)
    rest = prof[prof.cluster.isin(order[1:])].sort_values("turns_M", ascending=False)
    names = {order[0]: "Constraint Negotiator", int(rest.cluster.iloc[0]): "Guided Explorer",
             int(rest.cluster.iloc[1]): "Direct Transactional"}
    prof["archetype"] = prof.cluster.map(names)
    prof.to_csv(os.path.join(TABLE_DIR, "t_rq1_profiles.csv"), index=False)
    dg["archetype"] = dg.cluster.map(names)

    # Assign D_test and project MultiWOZ by nearest frozen centroid (cosine)
    def assign(X):
        sims = X @ cents.T
        return sims.argmax(1), sims.max(1)
    t_lab, t_sim = assign(Xt)
    m_lab, m_sim = assign(X_mw)
    g_sim = (Xg @ cents.T).max(1)
    dt["cluster"], dt["centroid_sim"] = t_lab, t_sim
    dt["archetype"] = dt.cluster.map(names)
    d_mw["cluster"], d_mw["centroid_sim"] = m_lab, m_sim
    d_mw["archetype"] = d_mw.cluster.map(names)
    dg["centroid_sim"] = g_sim
    cross = []
    for nm, dd in [("Frames D_gold", dg), ("Frames D_test", dt), ("MultiWOZ 2.2", d_mw)]:
        r = dict(set=nm, N=len(dd), sim_M=dd.centroid_sim.mean(), sim_SD=dd.centroid_sim.std())
        for c, a in names.items():
            r[a] = 100 * (dd.cluster == c).mean()
        cross.append(r)
    dcross = pd.DataFrame(cross)
    dcross.to_csv(os.path.join(TABLE_DIR, "t_rq1_cross_corpus.csv"), index=False)
    shift = stats.ttest_ind(dt.centroid_sim, d_mw.centroid_sim, equal_var=False)
    gt_shift = stats.ttest_ind(dg.centroid_sim, dt.centroid_sim, equal_var=False)

    pd.concat([dg, dt]).to_csv(os.path.join(WORK_DIR, "frames_archetypes.csv"), index=False)
    d_mw.to_csv(os.path.join(WORK_DIR, "multiwoz_projected.csv"), index=False)
    np.save(os.path.join(WORK_DIR, "archetype_centroids.npy"), cents)
    with open(os.path.join(WORK_DIR, "archetypes.json"), "w") as f:
        json.dump({str(k): v for k, v in names.items()}, f, indent=2)

    # ---- figures -------------------------------------------------------------
    pal = {"Constraint Negotiator": "#4c72b0", "Guided Explorer": "#dd8452", "Direct Transactional": "#55a868"}
    try:
        import umap
        red = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine", random_state=SEED).fit(Xg)
        Eg, Em = red.embedding_, red.transform(X_mw)
        method = "UMAP"
    except Exception:
        from sklearn.decomposition import PCA
        red = PCA(2, random_state=SEED).fit(Xg)
        Eg, Em = red.transform(Xg), red.transform(X_mw)
        method = "PCA"
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300, sharex=True, sharey=True)
    for a, c in pal.items():
        m = dg.archetype.values == a
        axes[0].scatter(Eg[m, 0], Eg[m, 1], s=6, alpha=0.6, c=c, label=f"{a} (n = {m.sum()})")
    axes[0].set_title("A. Frames golden partition by archetype")
    axes[0].legend(frameon=False, fontsize=8, markerscale=2.5, loc="best")
    axes[1].scatter(Eg[:, 0], Eg[:, 1], s=4, c="#d0d0d0", alpha=0.5, label="Frames (reference)")
    for a, c in pal.items():
        m = d_mw.archetype.values == a
        if m.any():
            axes[1].scatter(Em[m, 0], Em[m, 1], s=6, alpha=0.7, c=c, label=f"MultiWOZ -> {a} (n = {m.sum()})")
    axes[1].set_title("B. MultiWOZ 2.2 projected onto frozen Frames space")
    axes[1].legend(frameon=False, fontsize=8, markerscale=2.5, loc="best")
    for ax in axes:
        ax.set_xlabel(f"{method} dimension 1")
    axes[0].set_ylabel(f"{method} dimension 2")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_rq1_umap.png"))
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    algos = ["K-Means", "Agglomerative", "HDBSCAN"]
    ax.boxplot([de.loc[de.algorithm == a, "silhouette"] for a in algos] + [perm],
               labels=algos + ["Permutation\nbaseline"], showmeans=True)
    for i, a in enumerate(algos):
        y = de.loc[de.algorithm == a, "silhouette"].values
        ax.scatter(np.random.default_rng(i).normal(i + 1, 0.05, len(y)), y, s=8, alpha=0.4, c="k")
    ax.axhline(0, color="grey", lw=0.8, ls=":")
    ax.set_ylabel("Silhouette coefficient (cosine)")
    ax.set_xlabel("Clustering algorithm (53 independent subsamples each, n = 500)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_rq1_silhouette.png"))
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), dpi=300)
    for ax, col, lab in zip(axes, ["silhouette", "davies_bouldin", "inertia"],
                            ["Silhouette (higher = better)", "Davies-Bouldin (lower = better)",
                             "Inertia / WSS (elbow)"]):
        ax.plot(dk.k, dk[col], marker="o", color="#4c72b0")
        ax.axvline(3, color="grey", ls="--", lw=1)
        ax.set_xlabel("Number of clusters (k)")
        ax.set_title(lab, fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_rq1_k_selection.png"))
    plt.close(fig)

    summary = dict(
        n_gold=len(dg), n_test=len(dt), n_multiwoz=len(d_mw), hdbscan_redraws=hdb_redraws,
        hdbscan_default_fail=default_fail, hdbscan_noise_M=float(np.mean(hdb_noise)),
        hdbscan_noise_SD=float(np.std(hdb_noise, ddof=1)),
        hdbscan_k_found=dict(pd.Series(hdb_k).value_counts().sort_index().astype(int)),
        shapiro={a: dict(W=float(r.statistic), p=float(r.pvalue)) for a, r in shapiro.items()},
        levene=dict(W=float(levene.statistic), p=float(levene.pvalue)),
        anova=dict(F=float(aov["F"].iloc[0]), df1=float(aov["df"].iloc[0]), df2=float(aov["df"].iloc[1]),
                   p=float(aov["PR(>F)"].iloc[0]), eta2=float(eta2)),
        welch=dict(F=float(welch.statistic), df1=float(welch.df[0]), df2=float(welch.df[1]), p=float(welch.pvalue)),
        kruskal=dict(H=float(kw.statistic), p=float(kw.pvalue)),
        permutation_baseline=dict(M=float(np.mean(perm)), SD=float(np.std(perm, ddof=1))),
        cross_corpus_t=dict(t=float(shift.statistic), df=float(shift.df), p=float(shift.pvalue)),
        gold_vs_test_t=dict(t=float(gt_shift.statistic), df=float(gt_shift.df), p=float(gt_shift.pvalue)),
        umap_method=method)
    with open(os.path.join(WORK_DIR, "rq1_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=lambda o: int(o) if isinstance(o, np.integer) else float(o))
    print(json.dumps(summary, indent=2, default=lambda o: int(o) if isinstance(o, np.integer) else float(o)))
    print(dk.round(4).to_string(index=False))
    print(desc.round(4).to_string(index=False))
    print(dtk.to_string(index=False))
    print(prof.round(2).to_string(index=False))
    print(dcross.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
