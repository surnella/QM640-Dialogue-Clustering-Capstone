"""
Step 2b - RQ1 sensitivity analysis: does a USER-ONLY representation (embeddings
and/or behavioural features) give better archetypes than the original
full-dialogue (user + agent) embedding?

Representations (all clustered with K-Means, k = 2..6, on the Frames golden partition)
  R0  Full-dialogue embedding (user + agent turns)       - the original RQ1 representation
  R1  User-only embedding (user turns only)
  R2  User behavioural features (Frames user dialogue acts + user text; agent ignored)
  R3  Hybrid: R1 (PCA-20) + R2, each block scaled to equal total variance

Evaluation criteria (comparable across representations, because Silhouette values
computed in different feature spaces are not directly comparable)
  * Stability          mean adjusted Rand index (ARI) between K-Means solutions fitted on
                       pairs of independent 80% subsamples (B = 50 pairs)
  * Null-calibrated Silhouette  Silhouette minus the mean Silhouette obtained after
                       independently permuting every column (no joint structure), 10 nulls
  * Role-player confound  Cramer's V between cluster and Frames user_id (lower = better)
  * Early routing      a multinomial logistic-regression router is trained on golden-partition
                       prefixes (first N turns, N = 1..10) to predict the full-dialogue archetype
                       and evaluated on held-out prefixes; Cohen's kappa corrects for k
  * External validity  eta-squared of agent offers and user rating (variables not used by
                       any user-only representation)

Pre-declared selection rule (fixed before results were inspected)
  eligible   smallest cluster >= 10% of D_gold and stability ARI >= .60
  winner     highest held-out routing kappa at N = 5 among eligible configurations
             (ties broken by null-calibrated Silhouette)
The original R0 / k = 3 solution remains the primary RQ1 result; this step is a sensitivity
analysis whose winner is carried forward to RQ3 and RQ4 only if it outperforms R0.

No LLM calls are made. Public data only (Microsoft Frames).
"""

import json
import os
import re
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import adjusted_rand_score, cohen_kappa_score, silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import (FIG_DIR, SBERT_MODEL, SEED, TABLE_DIR, WORK_DIR, decay_weights,
                    delexicalize, dialogue_slot_values, load_canonical, load_frames_raw,
                    speaker_tag)

warnings.filterwarnings("ignore")
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                     "font.size": 11})

KS = range(2, 7)
PREFIXES = range(1, 11)
B_STAB = 50
N_NULL = 10
ROUTE_N = 5
MIN_CLUSTER = 0.10
MIN_ARI = 0.60
REPS = {"R0": "Full-dialogue embedding (user + agent)", "R1": "User-only embedding",
        "R2": "User behavioural features", "R3": "Hybrid: user embedding + user features"}

HESITATION = re.compile(r"\b(um+|uh+|hmm+|maybe|not sure|i guess|perhaps|i think|probably|possibly|"
                        r"i don'?t know|either)\b", re.I)
NON_SLOT = {"intent", "ref", "ref_anaphora", "impl_anaphora", "read", "write", "action", "id"}
PREF_KEYS = {"amenities", "vicinity", "breakfast", "beach", "park", "wifi", "spa", "downtown", "parking",
             "museum", "shopping", "seat", "category", "gst_rating", "dep_time_or", "dep_time_dst",
             "arr_time_dst", "arr_time_or"}
FEATURES = ["log_user_turns", "user_words", "slots_per_turn", "distinct_slots", "user_revisions",
            "switch_rate", "request_rate", "compare_rate", "negate_rate", "affirm_rate",
            "hesitation_rate", "budget_stated", "flex_stated", "preference_keys", "front_loading"]


# ----------------------------------------------------------------------------- features
def user_features(raw_turns):
    """Behavioural features from USER turns only (agent turns are ignored)."""
    ut = [t for t in raw_turns if t["author"] == "user"]
    n = max(len(ut), 1)
    words = [len(t["text"].split()) for t in ut] or [0]
    last, revisions, informs, keys, first_keys = {}, 0, 0, set(), set()
    cnt = dict(switch=0, request=0, compare=0, negate=0, affirm=0)
    budget = flex = 0
    hes = 0
    for i, t in enumerate(ut):
        hes += len(HESITATION.findall(t["text"]))
        for a in t["labels"]["acts"]:
            nm = a["name"]
            if nm == "switch_frame":
                cnt["switch"] += 1
            elif nm in ("request", "moreinfo"):
                cnt["request"] += 1
            elif nm in ("request_compare", "request_alts"):
                cnt["compare"] += 1
            elif nm == "negate":
                cnt["negate"] += 1
            elif nm in ("affirm", "confirm"):
                cnt["affirm"] += 1
            for g in a.get("args", []):
                k = g.get("key")
                if k in NON_SLOT or "val" not in g:
                    continue
                v = str(g["val"]).strip().lower()
                informs += 1
                keys.add(k)
                if i == 0:
                    first_keys.add(k)
                if k in last and last[k] != v:
                    revisions += 1
                last[k] = v
                budget |= k == "budget"
                flex |= k == "flex"
    return dict(log_user_turns=np.log1p(len(ut)), user_words=float(np.mean(words)),
                slots_per_turn=informs / n, distinct_slots=len(keys), user_revisions=revisions,
                switch_rate=cnt["switch"] / n, request_rate=cnt["request"] / n,
                compare_rate=cnt["compare"] / n, negate_rate=cnt["negate"] / n,
                affirm_rate=cnt["affirm"] / n, hesitation_rate=hes / n, budget_stated=int(budget),
                flex_stated=int(flex), preference_keys=len(keys & PREF_KEYS),
                front_loading=len(first_keys) / max(len(keys), 1))


def pooled(E, speakers, n_turns=None, user_only=False):
    """Decay-weighted mean of turn embeddings (same weighting as the original RQ1 vectors)."""
    E, sp = (E, speakers) if n_turns is None else (E[:n_turns], speakers[:n_turns])
    if user_only:
        m = np.array([s == "USER" for s in sp])
        E = E[m] if m.any() else E[:1] * 0
    w = decay_weights(len(E))
    v = (E * w[:, None]).sum(0)
    return v / (np.linalg.norm(v) + 1e-12)


# ----------------------------------------------------------------------------- representation builders
class Hybrid:
    """PCA-20 of the user embedding + standardized features, equal total variance per block."""

    def fit(self, Xe, Xf):
        self.pca = PCA(20, random_state=SEED).fit(Xe)
        Pe = self.pca.transform(Xe)
        self.e_mu, self.e_sd = Pe.mean(0), Pe.std(0) + 1e-9
        self.f_mu, self.f_sd = Xf.mean(0), Xf.std(0) + 1e-9
        return self

    def transform(self, Xe, Xf):
        Pe = (self.pca.transform(Xe) - self.e_mu) / self.e_sd / np.sqrt(20)
        Pf = (Xf - self.f_mu) / self.f_sd / np.sqrt(Xf.shape[1])
        return np.hstack([Pe, Pf])


def cramers_v(a, b):
    ct = pd.crosstab(a, b)
    chi = stats.chi2_contingency(ct)[0]
    return float(np.sqrt(chi / (ct.values.sum() * (min(ct.shape) - 1))))


def eta2(y, g):
    d = pd.DataFrame(dict(y=y, g=g)).dropna()
    grand = d.y.mean()
    ssb = sum(len(x) * (x.mean() - grand) ** 2 for _, x in d.groupby("g").y)
    sst = ((d.y - grand) ** 2).sum()
    return float(ssb / sst) if sst > 0 else np.nan


def main(emb="minilm"):
    sfx = "" if emb == "minilm" else f"_{emb}"
    df = pd.read_csv(os.path.join(WORK_DIR, "frames_clean.csv"))
    X0_saved = np.load(os.path.join(WORK_DIR, "frames_emb.npy"))
    raw = load_frames_raw()
    can = {d["dialogue_id"]: d for d in load_canonical(("frames",))}
    dialogues = [can[i] for i in df.dialogue_id]
    gold = (df.partition == "gold").values
    rng = np.random.default_rng(SEED)

    # ---- encode every turn once; all representations are pooled from these -----------------
    texts, spans, speakers = [], [], []
    for d in dialogues:
        sv = dialogue_slot_values(d, raw)
        tx = [f"{speaker_tag(t.get('speaker'))}: {delexicalize(t.get('utterance', ''), sv)}" for t in d["turns"]]
        spans.append((len(texts), len(tx)))
        speakers.append([speaker_tag(t.get("speaker")) for t in d["turns"]])
        texts.extend(tx)
    doc = {}
    if emb == "minilm":
        allE = SentenceTransformer(SBERT_MODEL).encode(texts, batch_size=64, show_progress_bar=False,
                                                       convert_to_numpy=True)
        TE = [allE[s:s + n] for s, n in spans]
        reps = {r: v for r, v in REPS.items()}
    else:
        gdir = os.path.join(os.path.dirname(WORK_DIR), "embeddings", "gemini")
        flat, off = np.load(os.path.join(gdir, "turn_emb.npy")), np.load(os.path.join(gdir, "turn_offsets.npy"))
        TE = [flat[off[i]:off[i + 1]] for i in range(len(df))]
        assert all(len(e) == n for e, (_, n) in zip(TE, spans)), "Gemini turn cache does not match dialogues"
        for kind, code in (("full", "D0"), ("user", "D1")):
            doc[code] = {n: np.load(os.path.join(gdir, f"doc_{kind}_{'all' if n is None else n}.npy"))
                         for n in (None, 3, 5, 7, 10)}
        reps = {"R0": REPS["R0"] + " [turn-pooled]", "R1": REPS["R1"] + " [turn-pooled]",
                "R3": REPS["R3"], "D0": "Whole-conversation document (user + agent)",
                "D1": "Whole-conversation document (user turns only)"}
    raw_turns = [raw[i]["turns"] for i in df.dialogue_id]
    n_turns = df.total_turns.values
    mismatch = int(sum(len(r) != len(d["turns"]) for r, d in zip(raw_turns, dialogues)))

    def build(n=None):
        """Return (E_full, E_user, F) for prefixes of n turns (None = whole dialogue)."""
        E0 = np.array([pooled(e, s, n) for e, s in zip(TE, speakers)])
        E1 = np.array([pooled(e, s, n, user_only=True) for e, s in zip(TE, speakers)])
        F = pd.DataFrame([user_features(r if n is None else r[:n]) for r in raw_turns])[FEATURES].values
        return E0, E1, F.astype(float)

    E0, E1, F = build()
    repro = float(np.mean(np.sum(E0 * X0_saved, 1))) if emb == "minilm" else None

    # representation spaces fitted on D_gold only
    f_sc = StandardScaler().fit(F[gold])
    hyb = Hybrid().fit(E1[gold], F[gold])
    space = {"R0": lambda e0, e1, f: e0, "R1": lambda e0, e1, f: e1,
             "R2": lambda e0, e1, f: f_sc.transform(f), "R3": lambda e0, e1, f: hyb.transform(e1, f)}
    space = {r: fn for r, fn in space.items() if r in reps}
    metric = {"R0": "cosine", "R1": "cosine", "R2": "euclidean", "R3": "euclidean", "D0": "cosine",
              "D1": "cosine"}
    X = {r: fn(E0, E1, F) for r, fn in space.items()}
    for code in doc:
        X[code] = doc[code][None]
    prefix_X = {}
    for n in PREFIXES:
        p0, p1, pf = build(n)
        prefix_X[n] = {r: fn(p0, p1, pf) for r, fn in space.items()}
        for code in doc:
            if n in doc[code]:
                prefix_X[n][code] = doc[code][n]
    print("embeddings + prefixes built", flush=True)

    user_id = df.dialogue_id.map(lambda i: raw[i]["user_id"]).values
    rows, route_rows, labels_store = [], [], {}
    for r in reps:
        Xg, Xt = X[r][gold], X[r][~gold]
        for k in KS:
            km = KMeans(n_clusters=k, n_init=20, random_state=SEED).fit(Xg)
            lg, lt = km.labels_, km.predict(Xt)
            labels_store[(r, k)] = (km, lg, lt)
            sil = silhouette_score(Xg, lg, metric=metric[r])
            nulls = []
            for b in range(N_NULL):
                Xp = np.column_stack([rng.permutation(c) for c in Xg.T])
                lp = KMeans(n_clusters=k, n_init=5, random_state=b).fit_predict(Xp)
                nulls.append(silhouette_score(Xp, lp, metric=metric[r]))
            aris = []
            for b in range(B_STAB):
                i1 = rng.choice(len(Xg), int(.8 * len(Xg)), replace=False)
                i2 = rng.choice(len(Xg), int(.8 * len(Xg)), replace=False)
                a1 = KMeans(n_clusters=k, n_init=5, random_state=b).fit(Xg[i1]).predict(Xg)
                a2 = KMeans(n_clusters=k, n_init=5, random_state=b + 999).fit(Xg[i2]).predict(Xg)
                aris.append(adjusted_rand_score(a1, a2))
            lab_all = np.empty(len(df), int)
            lab_all[gold], lab_all[~gold] = lg, lt
            kap = {}
            for n in PREFIXES:
                if r not in prefix_X[n]:
                    continue
                ok = n_turns > n  # prefix must be a strict part of the dialogue
                tr, te = gold & ok, (~gold) & ok
                clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, C=1.0))
                clf.fit(prefix_X[n][r][tr], lab_all[tr])
                pred = clf.predict(prefix_X[n][r][te])
                kap[n] = cohen_kappa_score(lab_all[te], pred)
                route_rows.append(dict(rep=r, k=k, N=n, n_test=int(te.sum()),
                                       accuracy=float((pred == lab_all[te]).mean()), kappa=float(kap[n])))
            rows.append(dict(rep=r, k=k, silhouette=sil, null_silhouette=float(np.mean(nulls)),
                             calibrated_silhouette=sil - float(np.mean(nulls)),
                             stability_ari=float(np.mean(aris)), stability_ari_sd=float(np.std(aris, ddof=1)),
                             min_cluster_pct=100 * np.bincount(lg).min() / len(lg),
                             roleplayer_v=cramers_v(lab_all, user_id),
                             eta2_offers=eta2(df.offers.values, lab_all),
                             eta2_rating=eta2(pd.to_numeric(df.user_rating, errors="coerce").values, lab_all),
                             kappa_N3=kap[3], kappa_N5=kap[5], kappa_N7=kap[7], kappa_N10=kap[10]))
            print(f"{r} k={k}: ARI={np.mean(aris):.3f} kappa5={kap[5]:.3f}", flush=True)

    grid = pd.DataFrame(rows)
    grid["eligible"] = (grid.min_cluster_pct >= 100 * MIN_CLUSTER) & (grid.stability_ari >= MIN_ARI)
    elig = grid[grid.eligible].sort_values(["kappa_N5", "calibrated_silhouette"], ascending=False)
    winner = elig.iloc[0] if len(elig) else grid.sort_values("kappa_N5", ascending=False).iloc[0]
    grid.to_csv(os.path.join(TABLE_DIR, f"t_rq1_rep_grid{sfx}.csv"), index=False)
    route = pd.DataFrame(route_rows)
    route.to_csv(os.path.join(TABLE_DIR, f"t_rq1_rep_routing{sfx}.csv"), index=False)

    # ---- profile of the winning configuration and of the best k = 3 user-only solution ------
    def profile(r, k):
        km, lg, lt = labels_store[(r, k)]
        lab_all = np.empty(len(df), int)
        lab_all[gold], lab_all[~gold] = lg, lt
        d = df.copy()
        d["cluster"] = lab_all
        Fd = pd.DataFrame(F, columns=FEATURES)
        Fd["cluster"] = lab_all
        p = d[gold].groupby("cluster").agg(n=("dialogue_id", "size"), turns_M=("total_turns", "mean"),
                                           offers=("offers", "mean"),
                                           success_pct=("task_success", lambda s: 100 * s.eq(True).mean()))
        f = Fd[gold].groupby("cluster")[FEATURES].mean()
        out = p.join(f)
        out["pct"] = 100 * out.n / out.n.sum()
        return out.reset_index(), lab_all

    win_prof, win_lab = profile(winner.rep, int(winner.k))
    win_prof.to_csv(os.path.join(TABLE_DIR, f"t_rq1_rep_winner_profile{sfx}.csv"), index=False)
    agree_r0 = adjusted_rand_score(labels_store[("R0", 3)][1], labels_store[(winner.rep, int(winner.k))][1])
    out_lab = df[["dialogue_id", "partition"]].copy()
    out_lab["cluster"] = win_lab
    out_lab.to_csv(os.path.join(WORK_DIR, f"frames_archetypes_user{sfx}.csv"), index=False)

    # ---- figure --------------------------------------------------------------------------
    pal = {"R0": "#7f7f7f", "R1": "#4c72b0", "R2": "#dd8452", "R3": "#55a868", "D0": "#c44e52",
           "D1": "#8172b2"}
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.0), dpi=300)
    for r in reps:
        g = grid[grid.rep == r]
        axes[0].plot(g.k, g.stability_ari, marker="o", color=pal[r], label=f"{r}: {reps[r]}")
        axes[1].plot(g.k, g.kappa_N5, marker="o", color=pal[r])
        rr = route[(route.rep == r) & (route.k == int(winner.k))]
        axes[2].plot(rr.N, rr.kappa, marker="o", color=pal[r])
    axes[0].axhline(MIN_ARI, color="k", ls=":", lw=0.8)
    axes[0].set(xlabel="Number of clusters (k)", ylabel="Stability (mean ARI)", title="A. Cluster stability")
    axes[1].set(xlabel="Number of clusters (k)", ylabel="Routing Cohen's κ", title="B. Routing after 5 turns")
    axes[2].set(xlabel="Turns observed (N)", ylabel="Routing Cohen's κ",
                title=f"C. Routing curve (k = {int(winner.k)})")
    for ax in axes:
        ax.axhline(0, color="grey", lw=0.6)
    axes[0].legend(frameon=False, fontsize=7.5, loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, f"fig_rq1_rep_sensitivity{sfx}.png"))
    plt.close(fig)

    summary = dict(embedding=emb, turn_alignment_mismatches=mismatch, r0_reproduction_cosine=repro,
                   rule=dict(min_cluster_pct=100 * MIN_CLUSTER, min_ari=MIN_ARI, route_N=ROUTE_N),
                   winner=dict(rep=winner.rep, k=int(winner.k), **{c: float(winner[c]) for c in
                               ["stability_ari", "kappa_N3", "kappa_N5", "kappa_N7", "calibrated_silhouette",
                                "roleplayer_v", "min_cluster_pct"]}),
                   r0_k3={c: float(grid[(grid.rep == "R0") & (grid.k == 3)][c].iloc[0]) for c in
                          ["stability_ari", "kappa_N3", "kappa_N5", "kappa_N7", "calibrated_silhouette",
                           "roleplayer_v"]},
                   ari_winner_vs_r0k3=float(agree_r0), n_eligible=int(grid.eligible.sum()))
    with open(os.path.join(WORK_DIR, f"rq1_rep_summary{sfx}.json"), "w") as f:
        json.dump(summary, f, indent=2)
    pd.set_option("display.width", 200)
    print(grid.round(3).to_string(index=False))
    print(json.dumps(summary, indent=2))
    print(win_prof.round(2).to_string(index=False))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--emb", choices=["minilm", "gemini"], default="minilm")
    main(ap.parse_args().emb)
