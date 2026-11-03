"""
Step 2g - Does defining archetypes on the OPENING of the conversation (first M user messages) give
more stable archetypes than the whole conversation?

For M in {3, 5, 7, 9} and the whole conversation:
  * Gemini user-side embedding of the truncated conversation (gemini-embedding-001, CLUSTERING;
    texts already embedded in step 2c are reused from the cache)
  * Gemini behavioural annotation of the truncated conversation (step 2e --max-user-msgs M)
  * Hybrid representation H = embedding (PCA-20) + LLM behavioural profile (step 2f), k = 3..8

Metrics per (M, k): stability ARI, null-calibrated Silhouette, smallest cluster, role-player V,
routing kappa (fixed router input, identical to step 2f), outcome contamination (Cramer's V between
cluster and the whole-conversation booking outcome; lower = archetypes describe the user rather than
the result), and the share of "core" members (same archetype in >= 90% of 30 resampled fits).

Pre-declared selection rule (fixed before results were inspected)
  per M: the step 2f rule (k in 3..8, stability ARI >= .60, smallest cluster >= 5%, max kappa at N = 5);
  across M: the highest stability ARI among the per-M winners; ties (|diff| < .01) broken by kappa at N = 5.
"""

import glob
import hashlib
import json
import os
import sys
import time
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import dotenv_values
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import adjusted_rand_score, cohen_kappa_score, silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import (FIG_DIR, ROOT, SEED, TABLE_DIR, WORK_DIR, delexicalize, dialogue_slot_values,
                    load_canonical, load_frames_raw, speaker_tag)
from step2b_rq1_representation import FEATURES, cramers_v, user_features
from step2e_llm_user_annotation import truncate
from step2f_rq1_llm_hybrid import Blocks, llm_matrix, load_ann

warnings.filterwarnings("ignore")
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                     "font.size": 10})
GDIR = os.path.join(ROOT, "data", "embeddings", "gemini")
CACHE = os.path.join(GDIR, "cache")
MS = [3, 5, 7, 9, None]
KS = range(3, 9)
DOC_N = (3, 5, 7, 10)
B_STAB, N_NULL, B_CORE = 50, 10, 30
MIN_ARI, MIN_CLUSTER = 0.60, 0.05


def h(t):
    return hashlib.sha1(t.encode("utf-8")).hexdigest()


def load_cache():
    lookup = {}
    for fp in glob.glob(os.path.join(CACHE, "*.json")):
        E = np.load(fp[:-5] + ".npy")
        for hh, v in zip(json.load(open(fp)), E):
            lookup[hh] = v
    return lookup


def embed_missing(texts, lookup):
    miss = sorted({t for t in texts if h(t) not in lookup})
    if not miss:
        return
    from google import genai
    from google.genai import types
    key = dotenv_values(os.path.join(ROOT, ".env")).get("GEMINI_API_KEY")
    client = genai.Client(api_key=key, vertexai=False)
    cfg = types.EmbedContentConfig(task_type="CLUSTERING")
    print(f"embedding {len(miss)} new texts", flush=True)
    for i in range(0, len(miss), 100):
        chunk = miss[i:i + 100]
        tag = h("".join(chunk))[:12]
        for attempt in range(15):
            try:
                r = client.models.embed_content(model="gemini-embedding-001", contents=chunk, config=cfg)
                E = np.array([e.values for e in r.embeddings], dtype=np.float32)
                np.save(os.path.join(CACHE, f"x_{tag}.npy"), E)
                json.dump([h(t) for t in chunk], open(os.path.join(CACHE, f"x_{tag}.json"), "w"))
                for t, v in zip(chunk, E):
                    lookup[h(t)] = v
                break
            except Exception as e:
                time.sleep(min(60, 2 ** attempt))
        else:
            sys.exit("embedding failed permanently")


def match(ref, lab, k):
    C = pd.crosstab(ref, lab).reindex(index=range(k), columns=range(k), fill_value=0).values
    r, c = linear_sum_assignment(-C)
    m = dict(zip(c, r))
    return np.array([m.get(x, -1) for x in lab])


def main():
    df = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    gold = (df.partition == "gold").values
    raw = load_frames_raw()
    can = {d["dialogue_id"]: d for d in load_canonical(("frames",))}
    raw_turns = [raw[i]["turns"] for i in df.dialogue_id]
    user_id = np.array([raw[i]["user_id"] for i in df.dialogue_id])
    n_turns = df.total_turns.values
    rng = np.random.default_rng(SEED)
    full_ann = load_ann(os.path.join(WORK_DIR, "llm_user_annotations.jsonl")).loc[df.dialogue_id]
    outcome = full_ann.outcome.values

    # ---- user-side texts per cut-off (same text format as step 2c) ------------------------
    tx_all = []
    for did in df.dialogue_id:
        d = can[did]
        sv = dialogue_slot_values(d, raw)
        tx_all.append([f"{speaker_tag(t.get('speaker'))}: {delexicalize(t.get('utterance', ''), sv)}"
                       for t in d["turns"]])
    docs = {}
    for M in MS:
        out = []
        for tx, rt in zip(tx_all, raw_turns):
            L = len(rt) if M is None else len(truncate(rt, M))
            out.append("\n".join(x for x in tx[:L] if x.startswith("USER:")) or tx[0])
        docs[M] = out
    lookup = load_cache()
    embed_missing([t for M in MS for t in docs[M]], lookup)
    EMB = {M: np.array([lookup[h(t)] for t in docs[M]]) for M in MS}
    full_doc = np.load(os.path.join(GDIR, "doc_user_all.npy"))
    emb_check = float(np.mean(np.sum(EMB[None] * full_doc, 1)))  # ~1: whole-conversation texts match step 2c

    # router input: identical for every M (as in step 2f)
    route_in = {}
    for n in DOC_N:
        A_n = pd.DataFrame([user_features(r[:n]) for r in raw_turns])[FEATURES].values.astype(float)
        route_in[n] = np.hstack([np.load(os.path.join(GDIR, f"doc_user_{n}.npy")), A_n])

    rows, store, ann_info = [], {}, {}
    for M in MS:
        fp = os.path.join(WORK_DIR, "llm_user_annotations.jsonl" if M is None else f"llm_user_annotations_u{M}.jsonl")
        ann = load_ann(fp).loc[df.dialogue_id]
        ann_info[str(M)] = dict(n=len(ann), truncated_pct=float(100 * np.mean(
            [len(truncate(r, M)) < len(r) for r in raw_turns])) if M else 0.0)
        Eb = PCA(20, random_state=SEED).fit(EMB[M][gold]).transform(EMB[M])
        Lb = llm_matrix(ann).values
        X = Blocks().fit([Eb[gold], Lb[gold]], [False, True]).transform([Eb, Lb])
        Xg, Xt = X[gold], X[~gold]
        for k in KS:
            km = KMeans(n_clusters=k, n_init=20, random_state=SEED).fit(Xg)
            lg, lt = km.labels_, km.predict(Xt)
            lab = np.empty(len(df), int)
            lab[gold], lab[~gold] = lg, lt
            sil = silhouette_score(Xg, lg)
            nulls = [silhouette_score(Xp, KMeans(n_clusters=k, n_init=5, random_state=b).fit_predict(Xp))
                     for b in range(N_NULL) for Xp in [np.column_stack([rng.permutation(c) for c in Xg.T])]]
            aris = []
            for b in range(B_STAB):
                i1 = rng.choice(len(Xg), int(.8 * len(Xg)), replace=False)
                i2 = rng.choice(len(Xg), int(.8 * len(Xg)), replace=False)
                a1 = KMeans(n_clusters=k, n_init=5, random_state=b).fit(Xg[i1]).predict(Xg)
                a2 = KMeans(n_clusters=k, n_init=5, random_state=b + 999).fit(Xg[i2]).predict(Xg)
                aris.append(adjusted_rand_score(a1, a2))
            core = []
            for b in range(B_CORE):
                i1 = rng.choice(len(Xg), int(.8 * len(Xg)), replace=False)
                core.append(match(lg, KMeans(n_clusters=k, n_init=5, random_state=500 + b).fit(Xg[i1]).predict(Xg), k))
            same = (np.array(core) == lg[None, :]).mean(0)
            kap = {}
            for n in DOC_N:
                ok = n_turns > n
                tr, te = gold & ok, (~gold) & ok
                clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, C=0.5))
                clf.fit(route_in[n][tr], lab[tr])
                kap[n] = cohen_kappa_score(lab[te], clf.predict(route_in[n][te]))
            rows.append(dict(M="whole" if M is None else M, k=k, silhouette=sil,
                             calibrated_silhouette=sil - float(np.mean(nulls)),
                             stability_ari=float(np.mean(aris)), core_pct=float(100 * (same >= .9).mean()),
                             min_core_pct=float(min(100 * (same[lg == c] >= .9).mean() for c in range(k))),
                             min_cluster_pct=100 * np.bincount(lg).min() / len(lg),
                             roleplayer_v=cramers_v(lab, user_id), outcome_v=cramers_v(lab, outcome),
                             kappa_N3=kap[3], kappa_N5=kap[5], kappa_N7=kap[7], kappa_N10=kap[10]))
            store[(rows[-1]["M"], k)] = (lab, ann)
            print(f"M={rows[-1]['M']} k={k}: ARI={np.mean(aris):.3f} core={rows[-1]['core_pct']:.0f}% "
                  f"kappa5={kap[5]:.3f} outcomeV={rows[-1]['outcome_v']:.3f} min={rows[-1]['min_cluster_pct']:.1f}%",
                  flush=True)

    grid = pd.DataFrame(rows)
    grid["eligible"] = (grid.stability_ari >= MIN_ARI) & (grid.min_cluster_pct >= 100 * MIN_CLUSTER)
    grid.to_csv(os.path.join(TABLE_DIR, "t_rq1_truncation_grid.csv"), index=False)
    per_m = []
    for M, g in grid.groupby("M", sort=False):
        e = g[g.eligible].sort_values(["kappa_N5", "calibrated_silhouette"], ascending=False)
        if len(e):
            per_m.append(e.iloc[0])
    per_m = pd.DataFrame(per_m)
    best = per_m.sort_values("stability_ari", ascending=False)
    top = best.iloc[0]
    if len(best) > 1 and abs(best.iloc[0].stability_ari - best.iloc[1].stability_ari) < .01:
        top = best.iloc[:2].sort_values("kappa_N5", ascending=False).iloc[0]
    per_m.to_csv(os.path.join(TABLE_DIR, "t_rq1_truncation_winners.csv"), index=False)

    # profile of the overall winner
    lab, ann = store[(top.M, int(top.k))]
    ORD = ["price_sensitivity", "destination_flexibility", "date_flexibility", "exploration_breadth", "decisiveness",
           "detail_orientation", "information_upfront", "revision_tendency", "question_asking", "politeness"]
    P = pd.DataFrame(dict(cluster=lab, gold=gold, turns=n_turns, outcome=outcome, goal=ann.primary_goal.values,
                          **{c: ann[c].values for c in ORD}))
    g = P[P.gold]
    prof = g.groupby("cluster").agg(n=("turns", "size"), turns_M=("turns", "mean"), **{c: (c, "mean") for c in ORD})
    prof["pct"] = 100 * prof.n / prof.n.sum()
    for col in ("goal", "outcome"):
        ct = pd.crosstab(g.cluster, g[col], normalize="index") * 100
        for c in ct.columns:
            prof[f"{col}_{c}_pct"] = ct[c]
    prof.reset_index().to_csv(os.path.join(TABLE_DIR, "t_rq1_truncation_winner_profile.csv"), index=False)
    pd.DataFrame(dict(dialogue_id=df.dialogue_id, partition=df.partition, cluster=lab)).to_csv(
        os.path.join(WORK_DIR, "frames_archetypes_truncation_winner.csv"), index=False)

    # figure
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.7), dpi=300)
    order = ["3", "5", "7", "9", "whole"]
    for k, c in zip(KS, plt.cm.viridis(np.linspace(0, .9, len(KS)))):
        gg = grid[grid.k == k].set_index(grid[grid.k == k].M.astype(str)).loc[order]
        for ax, col in zip(axes, ["stability_ari", "core_pct", "kappa_N5", "outcome_v"]):
            ax.plot(order, gg[col], marker="o", color=c, label=f"k = {k}")
    titles = ["A. Stability (ARI)", "B. Core members (%)", "C. Routing κ (N = 5)", "D. Outcome contamination (V)"]
    for ax, t in zip(axes, titles):
        ax.set(title=t, xlabel="User messages used")
    axes[0].axhline(MIN_ARI, color="k", ls=":", lw=0.8)
    axes[0].legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_rq1_truncation.png"))
    plt.close(fig)

    summary = dict(emb_check_whole_vs_step2c=emb_check, annotations=ann_info,
                   winner=dict(M=str(top.M), k=int(top.k), **{c: float(top[c]) for c in
                               ["stability_ari", "core_pct", "min_core_pct", "calibrated_silhouette", "kappa_N3",
                                "kappa_N5", "kappa_N7", "kappa_N10", "outcome_v", "roleplayer_v", "min_cluster_pct"]}))
    json.dump(summary, open(os.path.join(WORK_DIR, "rq1_truncation_summary.json"), "w"), indent=2)
    pd.set_option("display.width", 250)
    print(grid.round(3).to_string(index=False))
    print(per_m.round(3).to_string(index=False))
    print(json.dumps(summary, indent=2))
    print(prof.round(2).T.to_string())


if __name__ == "__main__":
    main()
