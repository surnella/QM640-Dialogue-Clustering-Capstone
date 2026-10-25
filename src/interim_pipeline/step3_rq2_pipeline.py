"""
Step 3 - RQ2: dynamic cluster-adaptive few-shot prompting (style convergence).

Two modes
  python step3_rq2_pipeline.py            -> pilot (no LLM calls): exemplar-retrieval quality,
                                             prefix-routing accuracy, and validity of the
                                             style-convergence metric on human responses.
  python step3_rq2_pipeline.py --execute  -> full repeated-measures experiment with Gemini
                                             (requires GEMINI_API_KEY in the environment or .env).

Repeated-measures design (matches the power analysis, N = 33 = 3 archetypes x 11):
  every sampled D_test dialogue prefix (U1, A1, U2) is answered under all three conditions
  (Zero-Shot, Static Few-Shot, Cluster-Adaptive Few-Shot); the dialogue is the subject.
Primary DV  : cosine similarity between the generated agent turn and the target-archetype
              agent-style centroid (S-BERT, de-lexicalised).
Secondary DV: cosine similarity to the human (gold) agent turn.
Analysis    : one-way RM-ANOVA, Mauchly's test of sphericity, Greenhouse-Geisser correction,
              Holm-adjusted paired t-tests, partial eta squared and Cohen's d_z.
"""

import argparse
import json
import os
import time

import faiss
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sentence_transformers import SentenceTransformer

from common import (FIG_DIR, ROOT, SBERT_MODEL, SEED, TABLE_DIR, WORK_DIR, delexicalize,
                    dialogue_slot_values, embed_dialogues, load_canonical, load_frames_raw, speaker_tag)

N_PER_ARCH = 11
K_SHOT = 3
PREFIX_TURNS = 3          # U1, A1, U2  -> model generates A2
EXEMPLAR_TURNS = 6
CONDITIONS = ["Zero-Shot", "Static Few-Shot", "Cluster-Adaptive Few-Shot"]
SYSTEM_INSTRUCTION = (
    "You are a travel agent helping a customer plan and book a vacation package (flights and hotel). "
    "Reply with the next single agent turn only, in one to three sentences. Do not invent prices, "
    "dates, or availability; if information is missing, ask for it.")

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                     "font.size": 11})


# ----------------------------------------------------------------------------- statistics
def rm_anova(Y):
    """One-way repeated-measures ANOVA on an (n subjects x k conditions) array."""
    n, k = Y.shape
    gm = Y.mean()
    ss_cond = n * ((Y.mean(0) - gm) ** 2).sum()
    ss_subj = k * ((Y.mean(1) - gm) ** 2).sum()
    ss_tot = ((Y - gm) ** 2).sum()
    ss_err = ss_tot - ss_cond - ss_subj
    df1, df2 = k - 1, (k - 1) * (n - 1)
    F = (ss_cond / df1) / (ss_err / df2)
    p = stats.f.sf(F, df1, df2)
    # Mauchly's W and Greenhouse-Geisser epsilon from orthonormal contrasts
    C = np.linalg.qr(np.vstack([np.ones(k), np.eye(k)[:-1] - 1.0 / k]).T)[0][:, 1:]
    S = np.cov(Y @ C, rowvar=False)
    p_ = k - 1
    W = np.linalg.det(S) / (np.trace(S) / p_) ** p_
    dfm = p_ * (p_ + 1) / 2 - 1
    chi2 = -(n - 1 - (2 * p_ ** 2 + p_ + 2) / (6 * p_)) * np.log(W)
    p_mauchly = stats.chi2.sf(chi2, dfm)
    eps_gg = np.trace(S) ** 2 / (p_ * np.trace(S @ S))
    p_gg = stats.f.sf(F, df1 * eps_gg, df2 * eps_gg)
    return dict(F=F, df1=df1, df2=df2, p=p, eta2_partial=ss_cond / (ss_cond + ss_err),
                mauchly_W=W, mauchly_chi2=chi2, mauchly_df=dfm, mauchly_p=p_mauchly,
                eps_gg=eps_gg, df1_gg=df1 * eps_gg, df2_gg=df2 * eps_gg, p_gg=p_gg)


def holm_pairwise(Y, labels):
    rows = []
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            d = Y[:, j] - Y[:, i]
            t, p = stats.ttest_rel(Y[:, j], Y[:, i])
            rows.append(dict(contrast=f"{labels[j]} vs. {labels[i]}", mean_diff=d.mean(), t=t,
                             df=len(d) - 1, p=p, d_z=d.mean() / d.std(ddof=1)))
    df = pd.DataFrame(rows).sort_values("p").reset_index(drop=True)
    m = len(df)
    adj, running = [], 0
    for r, p in enumerate(df.p):
        running = max(running, min(1, (m - r) * p))
        adj.append(running)
    df["p_holm"] = adj
    return df


# ----------------------------------------------------------------------------- data helpers
def prefix_text(dialogue, sv, n):
    return "\n".join(f"{speaker_tag(t['speaker'])}: {delexicalize(t['utterance'], sv)}"
                     for t in dialogue["turns"][:n])


def eligible(d):
    t = d["turns"]
    return (len(t) >= PREFIX_TURNS + 1 and t[0]["speaker"] == "user" and t[1]["speaker"] != "user"
            and t[2]["speaker"] == "user" and t[3]["speaker"] != "user")


def build_prompt(condition, prefix, exemplars):
    parts = [SYSTEM_INSTRUCTION]
    if condition != "Zero-Shot":
        parts.append("Here are example conversations showing how an agent responds to customers like this one "
                     "(entity values are masked):")
        for i, ex in enumerate(exemplars, 1):
            parts.append(f"Example {i}:\n{ex}")
    parts.append(f"Current conversation:\n{prefix}\nAGENT:")
    return "\n\n".join(parts)


def load_env_key():
    key = os.environ.get("GEMINI_API_KEY")
    env = os.path.join(ROOT, ".env")
    if not key and os.path.exists(env):
        for line in open(env):
            if line.strip().startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    return key


# ----------------------------------------------------------------------------- main
def main(execute=False, model_name="gemini-2.5-flash"):
    rng = np.random.default_rng(SEED)
    frames_raw = load_frames_raw()
    can = {d["dialogue_id"]: d for d in load_canonical(("frames",))}
    arch = pd.read_csv(os.path.join(WORK_DIR, "frames_archetypes.csv"))
    names = {int(k): v for k, v in json.load(open(os.path.join(WORK_DIR, "archetypes.json"))).items()}
    archetypes = [names[k] for k in sorted(names)]
    cents = np.load(os.path.join(WORK_DIR, "archetype_centroids.npy"))
    sbert = SentenceTransformer(SBERT_MODEL)

    pool = arch[(arch.partition == "gold") & (arch.task_success == True)].reset_index(drop=True)
    pool_d = [can[i] for i in pool.dialogue_id]
    pool_sv = [dialogue_slot_values(d, frames_raw) for d in pool_d]
    # Retrieval keys use the same prefix length as the live query (no look-ahead)
    P = embed_dialogues(sbert, pool_d, frames_raw, max_turns=PREFIX_TURNS)
    pool_ex = [prefix_text(d, sv, EXEMPLAR_TURNS) for d, sv in zip(pool_d, pool_sv)]

    # Agent-style centroids from golden agent utterances (de-lexicalised)
    style_c = {}
    for a in archetypes:
        utts = [delexicalize(t["utterance"], sv) for d, sv, aa in zip(pool_d, pool_sv, pool.archetype)
                if aa == a for t in d["turns"] if t["speaker"] != "user"]
        e = sbert.encode(utts, batch_size=128, normalize_embeddings=True, show_progress_bar=False)
        c = e.mean(0)
        style_c[a] = c / np.linalg.norm(c)
    SC = np.vstack([style_c[a] for a in archetypes])

    # FAISS indices: global (unclustered k-NN baseline) and per-archetype sub-indices
    gidx = faiss.IndexFlatIP(P.shape[1]); gidx.add(P)
    sub = {}
    for a in archetypes:
        m = np.where(pool.archetype.values == a)[0]
        ix = faiss.IndexFlatIP(P.shape[1]); ix.add(P[m]); sub[a] = (ix, m)

    # Sample N = 33 eligible test dialogues, 11 per (full-dialogue) archetype
    test = arch[arch.partition == "test"].copy()
    test = test[test.dialogue_id.map(lambda i: eligible(can[i]))]
    picks = []
    for a in archetypes:
        cand = test[test.archetype == a].dialogue_id.values
        picks += list(rng.choice(cand, size=min(N_PER_ARCH, len(cand)), replace=False))
    static_ids = rng.choice(len(pool), size=K_SHOT, replace=False)

    rows = []
    for did in picks:
        d = can[did]
        sv = dialogue_slot_values(d, frames_raw)
        target = test.loc[test.dialogue_id == did, "archetype"].iloc[0]
        q = embed_dialogues(sbert, [d], frames_raw, max_turns=PREFIX_TURNS)
        routed = archetypes[int((q @ cents.T).argmax())]
        ix, m = sub[routed]
        _, I_c = ix.search(q, K_SHOT)
        cl_ids = m[I_c[0]]
        _, I_g = gidx.search(q, K_SHOT)
        gl_ids = I_g[0]
        gold = delexicalize(d["turns"][PREFIX_TURNS]["utterance"], sv)
        g_emb = sbert.encode([gold], normalize_embeddings=True)[0]
        style_sims = SC @ g_emb
        rows.append(dict(
            dialogue_id=did, target_archetype=target, routed_archetype=routed,
            routing_correct=routed == target,
            sim_static=float((P[static_ids] @ q[0]).mean()), sim_global=float((P[gl_ids] @ q[0]).mean()),
            sim_cluster=float((P[cl_ids] @ q[0]).mean()),
            arch_match_static=float((pool.archetype.values[static_ids] == target).mean()),
            arch_match_global=float((pool.archetype.values[gl_ids] == target).mean()),
            arch_match_cluster=float((pool.archetype.values[cl_ids] == target).mean()),
            gold_style_own=float(style_sims[archetypes.index(target)]),
            gold_style_other=float(np.delete(style_sims, archetypes.index(target)).mean()),
            gold_style_argmax_correct=archetypes[int(style_sims.argmax())] == target,
            prefix=prefix_text(d, sv, PREFIX_TURNS), gold=gold,
            ex_static=[pool_ex[i] for i in static_ids], ex_cluster=[pool_ex[i] for i in cl_ids]))
    dp = pd.DataFrame(rows)
    dp.drop(columns=["ex_static", "ex_cluster"]).to_csv(os.path.join(WORK_DIR, "rq2_pilot_units.csv"), index=False)

    # Pilot statistics -------------------------------------------------------
    Ysim = dp[["sim_static", "sim_global", "sim_cluster"]].values
    pilot = dict(N=len(dp), routing_accuracy=float(dp.routing_correct.mean()),
                 retrieval_rm=rm_anova(Ysim),
                 retrieval_pairs=holm_pairwise(Ysim, ["Static", "Global k-NN", "Cluster-adaptive"]).to_dict("records"),
                 style_metric_t=dict(zip(["t", "p"], stats.ttest_rel(dp.gold_style_own, dp.gold_style_other))),
                 style_metric_dz=float((dp.gold_style_own - dp.gold_style_other).mean()
                                       / (dp.gold_style_own - dp.gold_style_other).std(ddof=1)),
                 style_argmax_accuracy=float(dp.gold_style_argmax_correct.mean()))
    tab = pd.DataFrame({
        "strategy": ["Static few-shot (fixed)", "Global k-NN (unclustered)", "Cluster-adaptive (routed sub-index)"],
        "sim_M": Ysim.mean(0), "sim_SD": Ysim.std(0, ddof=1),
        "arch_match_M": dp[["arch_match_static", "arch_match_global", "arch_match_cluster"]].mean().values})
    tab.to_csv(os.path.join(TABLE_DIR, "t_rq2_pilot_retrieval.csv"), index=False)
    pd.DataFrame(pilot["retrieval_pairs"]).to_csv(os.path.join(TABLE_DIR, "t_rq2_pilot_pairs.csv"), index=False)
    with open(os.path.join(WORK_DIR, "rq2_pilot_summary.json"), "w") as f:
        json.dump(pilot, f, indent=2, default=float)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=300)
    labs = ["Static\nfew-shot", "Global\nk-NN", "Cluster-\nadaptive"]
    axes[0].boxplot([Ysim[:, i] for i in range(3)], labels=labs, showmeans=True)
    for i in range(len(dp)):
        axes[0].plot([1, 2, 3], Ysim[i], color="grey", alpha=0.25, lw=0.7)
    axes[0].set_ylabel("Mean cosine similarity: query prefix vs. exemplars")
    axes[0].set_title("A. Exemplar relevance (N = %d test prefixes)" % len(dp))
    axes[1].bar([0, 1], [dp.gold_style_own.mean(), dp.gold_style_other.mean()],
                yerr=[dp.gold_style_own.std(ddof=1), dp.gold_style_other.std(ddof=1)],
                color=["#55a868", "#c0c0c0"], capsize=6)
    axes[1].set_xticks([0, 1]); axes[1].set_xticklabels(["Own archetype\ncentroid", "Other archetype\ncentroids"])
    axes[1].set_ylabel("Cosine similarity of human agent turn")
    axes[1].set_title("B. Style-metric validity on human responses")
    lo = min(dp.gold_style_own.min(), dp.gold_style_other.min())
    axes[1].set_ylim(max(0, lo - 0.1), 1)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_rq2_pilot.png"))
    plt.close(fig)
    print(json.dumps(pilot, indent=2, default=float))
    print(tab.round(4).to_string(index=False))

    # Save the exact prompts that the experiment will send ------------------
    prompts = []
    for _, r in dp.iterrows():
        for c in CONDITIONS:
            ex = [] if c == "Zero-Shot" else (r.ex_static if c == "Static Few-Shot" else r.ex_cluster)
            prompts.append(dict(dialogue_id=r.dialogue_id, condition=c, target_archetype=r.target_archetype,
                                prompt=build_prompt(c, r.prefix, ex), gold=r.gold))
    with open(os.path.join(WORK_DIR, "rq2_prompts.jsonl"), "w") as f:
        for p in prompts:
            f.write(json.dumps(p) + "\n")
    print(f"Saved {len(prompts)} prompts to data/interim/rq2_prompts.jsonl")

    if not execute:
        return

    # Full experiment --------------------------------------------------------
    from google import genai
    from google.genai import types
    key = load_env_key()
    if not key:
        raise SystemExit("GEMINI_API_KEY not found (set it in the environment or in capstone/.env).")
    client = genai.Client(api_key=key, vertexai=False)
    cache_fp = os.path.join(WORK_DIR, "rq2_generations.jsonl")
    done = {}
    if os.path.exists(cache_fp):
        for line in open(cache_fp):
            j = json.loads(line); done[(j["dialogue_id"], j["condition"])] = j
    with open(cache_fp, "a") as f:
        for p in prompts:
            k = (p["dialogue_id"], p["condition"])
            if k in done:
                continue
            for attempt in range(5):
                try:
                    r = client.models.generate_content(
                        model=model_name, contents=p["prompt"],
                        config=types.GenerateContentConfig(
                            temperature=0.2, max_output_tokens=300, seed=SEED,
                            thinking_config=types.ThinkingConfig(thinking_budget=0)))
                    text = (r.text or "").strip()
                    finish = str(r.candidates[0].finish_reason) if r.candidates else None
                    break
                except Exception as e:  # rate limits / transient errors
                    time.sleep(2 ** attempt * 2); text = None; finish = None; err = str(e)
            rec = dict(p, response=text, model=model_name, finish_reason=finish, error=None if text else err)
            f.write(json.dumps(rec) + "\n"); f.flush(); done[k] = rec

    gens = pd.DataFrame(done.values())
    gens = gens[gens.response.notna() & (gens.response.str.len() > 0)]
    complete = gens.groupby("dialogue_id").condition.nunique()
    gens = gens[gens.dialogue_id.isin(complete[complete == 3].index)]
    resp = sbert.encode([delexicalize(t, []) for t in gens.response], normalize_embeddings=True)
    gold = sbert.encode(gens.gold.tolist(), normalize_embeddings=True)
    gens["style_cos"] = [float(style_c[a] @ e) for a, e in zip(gens.target_archetype, resp)]
    gens["gold_cos"] = (resp * gold).sum(1)
    gens["words"] = gens.response.str.split().str.len()
    gens.to_csv(os.path.join(WORK_DIR, "rq2_scored.csv"), index=False)
    res = {}
    for dv in ["style_cos", "gold_cos", "words"]:
        Y = gens.pivot(index="dialogue_id", columns="condition", values=dv)[CONDITIONS].values.astype(float)
        diffs = {f"{CONDITIONS[j]} - {CONDITIONS[i]}": stats.shapiro(Y[:, j] - Y[:, i])
                 for i in range(3) for j in range(i + 1, 3)}
        fr = stats.friedmanchisquare(*Y.T)
        res[dv] = dict(desc=dict(zip(CONDITIONS, zip(Y.mean(0), Y.std(0, ddof=1)))), anova=rm_anova(Y),
                       pairs=holm_pairwise(Y, CONDITIONS).to_dict("records"),
                       shapiro_diffs={k: dict(W=float(v.statistic), p=float(v.pvalue)) for k, v in diffs.items()},
                       friedman=dict(chi2=float(fr.statistic), p=float(fr.pvalue)))
        pd.DataFrame(res[dv]["pairs"]).to_csv(os.path.join(TABLE_DIR, f"t_rq2_{dv}_pairs.csv"), index=False)
    gold_words = gens.drop_duplicates("dialogue_id").gold.str.split().str.len()
    n_trunc = int((gens.get("finish_reason", pd.Series(dtype=str)).astype(str) != "FinishReason.STOP").sum())

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=300)
    labs = ["Zero-shot", "Static\nfew-shot", "Cluster-\nadaptive"]
    for ax, dv, ylab in [(axes[0], "style_cos", "Style convergence (cosine to target centroid)"),
                         (axes[1], "words", "Words per generated agent turn")]:
        Y = gens.pivot(index="dialogue_id", columns="condition", values=dv)[CONDITIONS].values.astype(float)
        ax.boxplot([Y[:, i] for i in range(3)], tick_labels=labs, showmeans=True)
        for i in range(len(Y)):
            ax.plot([1, 2, 3], Y[i], color="grey", alpha=0.25, lw=0.7)
        ax.set_ylabel(ylab)
    axes[1].axhline(gold_words.mean(), color="#55a868", ls="--", lw=1.2, label="Human reply mean")
    axes[1].legend(frameon=False, fontsize=8)
    axes[0].set_title("A. Primary outcome: style convergence")
    axes[1].set_title("B. Exploratory: response length")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_rq2_results.png"))
    plt.close(fig)

    with open(os.path.join(WORK_DIR, "rq2_results.json"), "w") as f:
        json.dump(dict(N=int(gens.dialogue_id.nunique()), model=model_name, n_calls=len(done),
                       n_not_stop=n_trunc, gold_words=dict(M=float(gold_words.mean()), SD=float(gold_words.std())),
                       results=res), f, indent=2, default=float)
    print(json.dumps(res, indent=2, default=float))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true", help="call Gemini and run the full RM-ANOVA")
    ap.add_argument("--model", default="gemini-2.5-flash")
    a = ap.parse_args()
    main(execute=a.execute, model_name=a.model)
