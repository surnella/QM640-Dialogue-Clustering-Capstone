"""
Step 2h - Ablation of the adopted archetype definition (option A: first 9 user messages, Gemini user
embedding + Gemini behavioural profile, K-Means k = 3).

This is an EXPLANATORY analysis, not a new selection: option A remains the archetype definition for
RQ2-RQ4 regardless of the results. Each configuration removes or swaps one component so that the
contribution of (1) truncation, (2) the Gemini behavioural profile and (3) Gemini vs. MiniLM embeddings
can be attributed.

Configurations (each at M = 9 user messages and on the whole conversation, k = 3)
  1  Gemini embedding + Gemini behavioural profile      (= option A at M = 9)
  2  MiniLM embedding + Gemini behavioural profile
  3  Gemini behavioural profile only
  4  Gemini embedding only
  5  MiniLM embedding only
  6  MiniLM embedding + dialogue-act features            (no LLM / no paid API at all)
Both embeddings encode the same text: the user's messages (de-lexicalized) as one document.
Metrics as in step 2g, plus agreement (ARI) with the adopted option-A labels.
"""

import json
import os
import warnings

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import adjusted_rand_score, cohen_kappa_score, silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import (ROOT, SBERT_MODEL, SEED, TABLE_DIR, WORK_DIR, delexicalize, dialogue_slot_values,
                    load_canonical, load_frames_raw, speaker_tag)
from step2b_rq1_representation import FEATURES, cramers_v, user_features
from step2e_llm_user_annotation import truncate
from step2f_rq1_llm_hybrid import Blocks, llm_matrix, load_ann
from step2g_rq1_truncation import h, load_cache, match

warnings.filterwarnings("ignore")
GDIR = os.path.join(ROOT, "data", "embeddings", "gemini")
K = 3
DOC_N = (3, 5, 7, 10)
B_STAB, N_NULL, B_CORE = 50, 10, 30
CONFIGS = {1: ("Gemini embedding + Gemini behavioural profile", ["gem", "llm"]),
           2: ("MiniLM embedding + Gemini behavioural profile", ["mini", "llm"]),
           3: ("Gemini behavioural profile only", ["llm"]),
           4: ("Gemini embedding only", ["gem"]),
           5: ("MiniLM embedding only", ["mini"]),
           6: ("MiniLM embedding + dialogue-act features (no LLM)", ["mini", "acts"])}


def main():
    df = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    gold = (df.partition == "gold").values
    raw = load_frames_raw()
    can = {d["dialogue_id"]: d for d in load_canonical(("frames",))}
    raw_turns = [raw[i]["turns"] for i in df.dialogue_id]
    user_id = np.array([raw[i]["user_id"] for i in df.dialogue_id])
    n_turns = df.total_turns.values
    outcome = load_ann(os.path.join(WORK_DIR, "llm_user_annotations.jsonl")).loc[df.dialogue_id].outcome.values
    adopted = pd.read_csv(os.path.join(WORK_DIR, "frames_archetypes_truncation_winner.csv")).cluster.values
    lookup = load_cache()
    sbert = SentenceTransformer(SBERT_MODEL)
    rng = np.random.default_rng(SEED)

    tx_all = []
    for did in df.dialogue_id:
        d = can[did]
        sv = dialogue_slot_values(d, raw)
        tx_all.append([f"{speaker_tag(t.get('speaker'))}: {delexicalize(t.get('utterance', ''), sv)}"
                       for t in d["turns"]])

    route_in = {}
    for n in DOC_N:
        A_n = pd.DataFrame([user_features(r[:n]) for r in raw_turns])[FEATURES].values.astype(float)
        route_in[n] = np.hstack([np.load(os.path.join(GDIR, f"doc_user_{n}.npy")), A_n])

    rows = []
    for M in (9, None):
        Ls = [len(rt) if M is None else len(truncate(rt, M)) for rt in raw_turns]
        docs = ["\n".join(x for x in tx[:L] if x.startswith("USER:")) or tx[0] for tx, L in zip(tx_all, Ls)]
        gem = np.array([lookup[h(t)] for t in docs])
        mini = sbert.encode(docs, batch_size=64, show_progress_bar=False, normalize_embeddings=True)
        n_tok_over = int(sum(len(sbert.tokenizer.tokenize(t)) > sbert.max_seq_length for t in docs))
        ann = load_ann(os.path.join(WORK_DIR, "llm_user_annotations.jsonl" if M is None
                                    else f"llm_user_annotations_u{M}.jsonl")).loc[df.dialogue_id]
        acts = pd.DataFrame([user_features(rt[:L]) for rt, L in zip(raw_turns, Ls)])[FEATURES].values.astype(float)
        blocks = {"gem": (PCA(20, random_state=SEED).fit(gem[gold]).transform(gem), False),
                  "mini": (PCA(20, random_state=SEED).fit(mini[gold]).transform(mini), False),
                  "llm": (llm_matrix(ann).values, True), "acts": (acts, True)}
        for cid, (name, parts) in CONFIGS.items():
            B = [blocks[p][0] for p in parts]
            X = Blocks().fit([b[gold] for b in B], [blocks[p][1] for p in parts]).transform(B)
            Xg, Xt = X[gold], X[~gold]
            km = KMeans(n_clusters=K, n_init=20, random_state=SEED).fit(Xg)
            lg, lt = km.labels_, km.predict(Xt)
            lab = np.empty(len(df), int)
            lab[gold], lab[~gold] = lg, lt
            sil = silhouette_score(Xg, lg)
            nulls = [silhouette_score(Xp, KMeans(n_clusters=K, n_init=5, random_state=b).fit_predict(Xp))
                     for b in range(N_NULL) for Xp in [np.column_stack([rng.permutation(c) for c in Xg.T])]]
            aris = []
            for b in range(B_STAB):
                i1 = rng.choice(len(Xg), int(.8 * len(Xg)), replace=False)
                i2 = rng.choice(len(Xg), int(.8 * len(Xg)), replace=False)
                aris.append(adjusted_rand_score(KMeans(n_clusters=K, n_init=5, random_state=b).fit(Xg[i1]).predict(Xg),
                                                KMeans(n_clusters=K, n_init=5, random_state=b + 999).fit(Xg[i2]).predict(Xg)))
            core = [match(lg, KMeans(n_clusters=K, n_init=5, random_state=500 + b).fit(
                Xg[rng.choice(len(Xg), int(.8 * len(Xg)), replace=False)]).predict(Xg), K) for b in range(B_CORE)]
            same = (np.array(core) == lg[None, :]).mean(0)
            kap = {}
            for n in DOC_N:
                ok = n_turns > n
                tr, te = gold & ok, (~gold) & ok
                clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, C=0.5))
                clf.fit(route_in[n][tr], lab[tr])
                kap[n] = cohen_kappa_score(lab[te], clf.predict(route_in[n][te]))
            rows.append(dict(M="9" if M else "whole", config=cid, name=name, stability_ari=float(np.mean(aris)),
                             core_pct=float(100 * (same >= .9).mean()),
                             calibrated_silhouette=sil - float(np.mean(nulls)),
                             min_cluster_pct=100 * np.bincount(lg).min() / len(lg),
                             outcome_v=cramers_v(lab, outcome), roleplayer_v=cramers_v(lab, user_id),
                             kappa_N5=kap[5], kappa_N10=kap[10], ari_vs_adopted=adjusted_rand_score(adopted, lab),
                             minilm_docs_truncated=n_tok_over))
            print(f"M={rows[-1]['M']} cfg{cid}: ARI={rows[-1]['stability_ari']:.3f} core={rows[-1]['core_pct']:.0f}% "
                  f"outV={rows[-1]['outcome_v']:.3f} k5={kap[5]:.3f} vsA={rows[-1]['ari_vs_adopted']:.3f}", flush=True)
    res = pd.DataFrame(rows)
    res.to_csv(os.path.join(TABLE_DIR, "t_rq1_ablation.csv"), index=False)
    pd.set_option("display.width", 250)
    print(res.drop(columns="name").round(3).to_string(index=False))


if __name__ == "__main__":
    main()
