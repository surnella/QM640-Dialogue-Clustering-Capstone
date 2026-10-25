"""
Step 2f - Deeper archetype breakdown: cluster users on LLM behavioural annotations combined with
Gemini embeddings (k = 3..8), detect unusual conversations, and evaluate everything with the same
criteria used in step 2b.

Representations (fitted on the golden partition only)
  E   Gemini user-side conversation embedding (gemini-embedding-001, CLUSTERING), PCA-20
  L   LLM behavioural profile: 11 ordinal ratings + primary-goal one-hot + secondary-goal multi-hot
      + emotional-tone one-hot (outcome, party type and the "unusual" flag are NOT used for clustering;
      they are kept for validation)
  H   Hybrid E + L, each block scaled to equal total variance
  H3  Hybrid E + L + dialogue-act behavioural features (step 2b R2), three equal blocks

Evaluation (comparable across representations)
  stability ARI (B = 50 pairs of 80% subsamples), null-calibrated Silhouette (10 column-permuted nulls),
  smallest cluster, role-player Cramer's V, and early routing: one fixed router input for every target
  (Gemini embedding of the user's first-N-turn prefix + prefix act features), multinomial logistic
  regression trained on golden prefixes and scored on held-out prefixes (Cohen's kappa, N = 3/5/7/10).

Pre-declared selection rule (fixed before results were inspected)
  k restricted to 3..8 (the study requires more than two archetypes);
  eligible: stability ARI >= .60 and smallest cluster >= 5% of D_gold;
  winner: highest routing kappa at N = 5, ties broken by null-calibrated Silhouette.

Unusual conversations: dialogues whose distance to their nearest centroid exceeds the 95th percentile
of golden-partition distances are flagged as an "Unusual" group; agreement with the LLM's
unusual_conversation flag and HDBSCAN noise is reported.

Annotation reliability: quadratic-weighted kappa (ordinal) / Cohen's kappa (categorical) between the
temperature-0 annotation and an independent temperature-0.7 re-annotation of 100 dialogues; criterion
validity: Spearman correlations between LLM ratings and corpus dialogue-act counts.
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
from sklearn.cluster import HDBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import adjusted_rand_score, cohen_kappa_score, silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import FIG_DIR, ROOT, SEED, TABLE_DIR, WORK_DIR, load_frames_raw
from step2b_rq1_representation import FEATURES, cramers_v, eta2, user_features

warnings.filterwarnings("ignore")
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                     "font.size": 10})

GDIR = os.path.join(ROOT, "data", "embeddings", "gemini")
KS = range(3, 9)
DOC_N = (3, 5, 7, 10)
B_STAB, N_NULL = 50, 10
MIN_ARI, MIN_CLUSTER = 0.60, 0.05
ORD = ["price_sensitivity", "destination_flexibility", "date_flexibility", "exploration_breadth",
       "decisiveness", "detail_orientation", "information_upfront", "revision_tendency", "question_asking",
       "politeness"]
GOALS = ["explore_destinations", "price_shopping", "specific_trip_booking", "compare_options",
         "information_only", "other"]
TONES = ["positive", "neutral", "impatient", "frustrated"]
REPS = {"E": "Gemini user embedding", "L": "LLM behavioural profile", "H": "Hybrid: embedding + LLM profile",
        "H3": "Hybrid: embedding + LLM profile + dialogue acts"}


def load_ann(fp):
    recs = [json.loads(l) for l in open(fp) if l.strip()]
    return pd.DataFrame([r for r in recs if "error" not in r]).drop_duplicates("dialogue_id").set_index("dialogue_id")


def llm_matrix(a):
    cols = {c: a[c].astype(float) for c in ORD}
    for g in GOALS:
        cols[f"goal_{g}"] = (a.primary_goal == g).astype(float)
        cols[f"sec_{g}"] = a.secondary_goals.apply(lambda s: float(g in s))
    for t in TONES:
        cols[f"tone_{t}"] = (a.emotional_tone == t).astype(float)
    return pd.DataFrame(cols)


class Blocks:
    """Give each block unit total variance so blocks weigh equally.

    Feature blocks (different units) are standardized per column; embedding blocks are only centred
    and scaled as a whole, so the relative variance of their principal components is preserved
    (whitening would give noise components the same weight as the dominant ones).
    """

    def fit(self, blocks, per_column):
        self.p = []
        for B, pc in zip(blocks, per_column):
            mu = B.mean(0)
            if pc:
                self.p.append((mu, B.std(0) + 1e-9, np.sqrt(B.shape[1])))
            else:
                self.p.append((mu, np.ones(B.shape[1]), np.sqrt(B.var(0).sum()) + 1e-9))
        return self

    def transform(self, blocks):
        return np.hstack([(B - mu) / sd / s for B, (mu, sd, s) in zip(blocks, self.p)])


def wkappa(a, b):
    return cohen_kappa_score(a, b, weights="quadratic")


def main():
    df = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    ann = load_ann(os.path.join(WORK_DIR, "llm_user_annotations.jsonl"))
    keep = df.dialogue_id.isin(ann.index).values
    n_missing = int((~keep).sum())
    df = df[keep].reset_index(drop=True)
    ann = ann.loc[df.dialogue_id]
    gold = (df.partition == "gold").values
    raw = load_frames_raw()
    raw_turns = [raw[i]["turns"] for i in df.dialogue_id]
    user_id = np.array([raw[i]["user_id"] for i in df.dialogue_id])
    rng = np.random.default_rng(SEED)

    D1 = {n: np.load(os.path.join(GDIR, f"doc_user_{'all' if n is None else n}.npy"))[keep] for n in (None,) + DOC_N}
    pca = PCA(20, random_state=SEED).fit(D1[None][gold])
    Eb = pca.transform(D1[None])
    Lb = llm_matrix(ann).values
    Ab = pd.DataFrame([user_features(r) for r in raw_turns])[FEATURES].values.astype(float)
    sc_e = Blocks().fit([Eb[gold]], [False])
    sc_l = Blocks().fit([Lb[gold]], [True])
    sc_h = Blocks().fit([Eb[gold], Lb[gold]], [False, True])
    sc_h3 = Blocks().fit([Eb[gold], Lb[gold], Ab[gold]], [False, True, True])
    X = {"E": sc_e.transform([Eb]), "L": sc_l.transform([Lb]), "H": sc_h.transform([Eb, Lb]),
         "H3": sc_h3.transform([Eb, Lb, Ab])}

    # router inputs: identical for every target (prefix embedding + prefix act features)
    route_in = {}
    for n in DOC_N:
        A_n = pd.DataFrame([user_features(r[:n]) for r in raw_turns])[FEATURES].values.astype(float)
        route_in[n] = np.hstack([D1[n], A_n])
    n_turns = df.total_turns.values

    rows, route_rows, store = [], [], {}
    for r in REPS:
        Xg, Xt = X[r][gold], X[r][~gold]
        for k in KS:
            km = KMeans(n_clusters=k, n_init=20, random_state=SEED).fit(Xg)
            lg, lt = km.labels_, km.predict(Xt)
            store[(r, k)] = (km, lg, lt)
            sil = silhouette_score(Xg, lg)
            nulls = []
            for b in range(N_NULL):
                Xp = np.column_stack([rng.permutation(c) for c in Xg.T])
                nulls.append(silhouette_score(Xp, KMeans(n_clusters=k, n_init=5, random_state=b).fit_predict(Xp)))
            aris = []
            for b in range(B_STAB):
                i1 = rng.choice(len(Xg), int(.8 * len(Xg)), replace=False)
                i2 = rng.choice(len(Xg), int(.8 * len(Xg)), replace=False)
                a1 = KMeans(n_clusters=k, n_init=5, random_state=b).fit(Xg[i1]).predict(Xg)
                a2 = KMeans(n_clusters=k, n_init=5, random_state=b + 999).fit(Xg[i2]).predict(Xg)
                aris.append(adjusted_rand_score(a1, a2))
            lab = np.empty(len(df), int)
            lab[gold], lab[~gold] = lg, lt
            kap = {}
            for n in DOC_N:
                ok = n_turns > n
                tr, te = gold & ok, (~gold) & ok
                clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, C=0.5))
                clf.fit(route_in[n][tr], lab[tr])
                pred = clf.predict(route_in[n][te])
                kap[n] = cohen_kappa_score(lab[te], pred)
                route_rows.append(dict(rep=r, k=k, N=n, n_test=int(te.sum()),
                                       accuracy=float((pred == lab[te]).mean()), kappa=float(kap[n])))
            rows.append(dict(rep=r, k=k, silhouette=sil, calibrated_silhouette=sil - float(np.mean(nulls)),
                             stability_ari=float(np.mean(aris)), stability_ari_sd=float(np.std(aris, ddof=1)),
                             min_cluster_pct=100 * np.bincount(lg).min() / len(lg),
                             roleplayer_v=cramers_v(lab, user_id),
                             eta2_turns=eta2(df.total_turns.values, lab),
                             eta2_success=eta2(df.task_success.eq(True).astype(float).values, lab),
                             kappa_N3=kap[3], kappa_N5=kap[5], kappa_N7=kap[7], kappa_N10=kap[10]))
            print(f"{r} k={k}: ARI={np.mean(aris):.3f} calSil={rows[-1]['calibrated_silhouette']:.3f} "
                  f"kappa5={kap[5]:.3f} min={rows[-1]['min_cluster_pct']:.1f}%", flush=True)

    grid = pd.DataFrame(rows)
    grid["eligible"] = (grid.stability_ari >= MIN_ARI) & (grid.min_cluster_pct >= 100 * MIN_CLUSTER)
    elig = grid[grid.eligible].sort_values(["kappa_N5", "calibrated_silhouette"], ascending=False)
    winner = elig.iloc[0] if len(elig) else grid.sort_values("stability_ari", ascending=False).iloc[0]
    grid.to_csv(os.path.join(TABLE_DIR, "t_rq1_llm_hybrid_grid.csv"), index=False)
    route = pd.DataFrame(route_rows)
    route.to_csv(os.path.join(TABLE_DIR, "t_rq1_llm_hybrid_routing.csv"), index=False)

    # ---- winner: profiles + unusual group ------------------------------------------------
    wr, wk = winner.rep, int(winner.k)
    km, lg, lt = store[(wr, wk)]
    lab = np.empty(len(df), int)
    lab[gold], lab[~gold] = lg, lt
    dist = np.linalg.norm(X[wr] - km.cluster_centers_[lab], axis=1)
    thr = np.percentile(dist[gold], 95)
    unusual = dist > thr
    hd = HDBSCAN(min_cluster_size=15, min_samples=5).fit_predict(X[wr][gold])
    hd_noise = np.zeros(len(df), bool)
    hd_noise[np.where(gold)[0]] = hd == -1
    llm_unusual = ann.unusual_conversation.values.astype(bool)
    prof = pd.DataFrame(dict(cluster=lab, unusual=unusual, gold=gold, turns=df.total_turns.values,
                             success=df.task_success.eq(True).values, **{c: ann[c].values for c in ORD},
                             goal=ann.primary_goal.values, outcome=ann.outcome.values, party=ann.party_type.values,
                             tone=ann.emotional_tone.values))
    g = prof[prof.gold]
    out = g.groupby("cluster").agg(n=("turns", "size"), turns_M=("turns", "mean"), success_pct=("success", "mean"),
                                   **{c: (c, "mean") for c in ORD})
    out["pct"] = 100 * out.n / out.n.sum()
    out["success_pct"] *= 100
    for col, cats in (("goal", GOALS), ("outcome", ["booked", "no_suitable_option", "undecided_or_left", "unclear"])):
        ct = pd.crosstab(g.cluster, g[col], normalize="index") * 100
        for c in cats:
            out[f"{col}_{c}_pct"] = ct[c] if c in ct else 0.0
    out = out.reset_index()
    out.to_csv(os.path.join(TABLE_DIR, "t_rq1_llm_hybrid_profiles.csv"), index=False)
    un = g[g.unusual]
    unusual_profile = dict(n=int(len(un)), pct=float(100 * len(un) / len(g)), turns_M=float(un.turns.mean()),
                           llm_flag_pct=float(100 * llm_unusual[gold & unusual].mean()),
                           llm_flag_pct_rest=float(100 * llm_unusual[gold & ~unusual].mean()),
                           hdbscan_noise_overlap_pct=float(100 * hd_noise[gold & unusual].mean()),
                           hdbscan_noise_share=float(100 * (hd == -1).mean()),
                           goal_mix=(un.goal.value_counts(normalize=True) * 100).round(1).to_dict(),
                           tone_mix=(un.tone.value_counts(normalize=True) * 100).round(1).to_dict())
    labs = df[["dialogue_id", "partition"]].copy()
    labs["cluster"], labs["unusual"] = lab, unusual
    labs.to_csv(os.path.join(WORK_DIR, "frames_archetypes_llm_hybrid.csv"), index=False)

    # ---- annotation reliability + criterion validity -------------------------------------
    rel = {}
    fp_rt = os.path.join(WORK_DIR, "llm_user_annotations_retest.jsonl")
    if os.path.exists(fp_rt):
        rt = load_ann(fp_rt)
        common_ids = [i for i in rt.index if i in ann.index]
        a0, a1 = ann.loc[common_ids], rt.loc[common_ids]
        rel = {c: float(wkappa(a0[c], a1[c])) for c in ORD}
        for c in ("primary_goal", "emotional_tone", "outcome", "party_type"):
            rel[c] = float(cohen_kappa_score(a0[c], a1[c]))
        rel["n"] = len(common_ids)
    A = pd.DataFrame(Ab, columns=FEATURES)
    pairs = [("revision_tendency", "user_revisions"), ("question_asking", "request_rate"),
             ("exploration_breadth", "switch_rate"), ("exploration_breadth", "compare_rate"),
             ("information_upfront", "front_loading"), ("price_sensitivity", "budget_stated"),
             ("detail_orientation", "preference_keys")]
    validity = {f"{a}~{b}": dict(rho=float(stats.spearmanr(ann[a].values, A[b].values)[0]),
                                 p=float(stats.spearmanr(ann[a].values, A[b].values)[1])) for a, b in pairs}

    # ---- figure ----------------------------------------------------------------------------
    pal = {"E": "#7f7f7f", "L": "#dd8452", "H": "#4c72b0", "H3": "#55a868"}
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.9), dpi=300)
    for r in REPS:
        gg = grid[grid.rep == r]
        axes[0].plot(gg.k, gg.stability_ari, marker="o", color=pal[r], label=f"{r}: {REPS[r]}")
        axes[1].plot(gg.k, gg.calibrated_silhouette, marker="o", color=pal[r])
        axes[2].plot(gg.k, gg.kappa_N5, marker="o", color=pal[r])
    axes[0].axhline(MIN_ARI, color="k", ls=":", lw=0.8)
    axes[0].set(xlabel="Number of clusters (k)", ylabel="Stability (mean ARI)", title="A. Stability")
    axes[1].set(xlabel="Number of clusters (k)", ylabel="Silhouette minus null", title="B. Separation beyond chance")
    axes[2].set(xlabel="Number of clusters (k)", ylabel="Routing Cohen's κ (N = 5)", title="C. Early routing")
    axes[0].legend(frameon=False, fontsize=7, loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_rq1_llm_hybrid.png"))
    plt.close(fig)

    summary = dict(n_dialogues=len(df), n_missing_annotation=n_missing,
                   rule=dict(k_range=[3, 8], min_ari=MIN_ARI, min_cluster_pct=100 * MIN_CLUSTER, route_N=5),
                   winner=dict(rep=wr, k=wk, **{c: float(winner[c]) for c in
                               ["stability_ari", "calibrated_silhouette", "silhouette", "kappa_N3", "kappa_N5",
                                "kappa_N7", "kappa_N10", "roleplayer_v", "min_cluster_pct", "eta2_turns"]}),
                   unusual=unusual_profile, reliability=rel, criterion_validity=validity,
                   llm_distributions={c: (ann[c].value_counts(normalize=True) * 100).round(1).to_dict()
                                      for c in ("primary_goal", "emotional_tone", "outcome", "party_type")},
                   llm_unusual_pct=float(100 * llm_unusual.mean()))
    with open(os.path.join(WORK_DIR, "rq1_llm_hybrid_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)
    pd.set_option("display.width", 250)
    print(grid.round(3).to_string(index=False))
    print(json.dumps(summary, indent=2, default=str))
    print(out.round(2).T.to_string())


if __name__ == "__main__":
    main()
