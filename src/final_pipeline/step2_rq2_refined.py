"""
Step 2 - RQ2 Re-run on Refined Archetypes (`Decisive Booker`, `Open Explorer`, `Rigid-Constraint Seeker`).

Design (matches pre-registered power analysis, N = 33 = 3 refined archetypes x 11):
  - Prefix: opening 9 turns (5 user messages U1..U5 and 4 agent turns A1..A4); model generates A5.
  - Routing: Hybrid Blocks Router (`m_user_msgs=5`, fitted strictly on D_gold; held-out accuracy = 70.1%, kappa = .535).
  - Three repeated-measures conditions per test dialogue:
      1. Zero-Shot Baseline
      2. Static Few-Shot (3 fixed random golden exemplars)
      3. Cluster-Adaptive Few-Shot (routed refined archetype communication directive + 3 top-k
         golden exemplars retrieved from that archetype's FAISS sub-index).
  - Outcomes:
      * Primary: Style convergence to target archetype centroid (both Hybrid semantic+discourse
        centroid `style_cos` and pure S-BERT `sbert_style_cos`).
      * Secondary: Similarity to human reply (`gold_cos`) and token-level BERTScore F1 (`bert_f1`,
        as promised in Interim Table 10).
      * Exploratory: Response length (`words`) vs. human wizard benchmark.
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sentence_transformers import SentenceTransformer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(ROOT, "src"), os.path.join(ROOT, "src", "interim_pipeline")):
    if p not in sys.path:
        sys.path.insert(0, p)

from common import SBERT_MODEL, SEED, delexicalize, speaker_tag  # noqa: E402
from final_pipeline.common_llm import (  # noqa: E402
    FINAL_DATA_DIR,
    FINAL_FIG_DIR,
    FINAL_TABLE_DIR,
    PRIMARY_AGENT_MODEL,
    CachedLLMClient,
)
from final_pipeline.metrics import holm_pairwise, rm_anova  # noqa: E402
from final_pipeline.routing import (  # noqa: E402
    ARCHETYPE_DIRECTIVES,
    REFINED_ARCHETYPES,
    RefinedArchetypeRouter,
)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 10,
})

N_PER_ARCH = 11
K_SHOT = 3
M_USER_MSGS = 5
PREFIX_TURNS = 9          # U1, A1, U2, A2, U3, A3, U4, A4, U5 -> generates A5 (index 9)
EXEMPLAR_START = 2        # mid-dialogue negotiation window (turns 3..8)
EXEMPLAR_END = 8
CONDITIONS = ["Zero-Shot", "Static Few-Shot", "Cluster-Adaptive Few-Shot"]

BASE_SYSTEM_INSTRUCTION = (
    "You are a travel agent helping a customer plan and book a vacation package (flights and hotel). "
    "Reply with the next single agent turn only. Do not invent unsupported facts; ground your reply in "
    "the conversation state."
)


def extract_discourse_features(delex_text: str) -> np.ndarray:
    """
    7-dimensional discourse structure profile of an agent turn:
      [word_count/20, sentence_count/3, question_count, has_offer_terms,
       has_option_comparison, has_constraint_feasibility_or_alt, has_booking_confirmation]
    """
    words = delex_text.split()
    n_w = len(words) / 20.0
    n_sents = max(1, len([s for s in re.split(r"[.!?]+", delex_text) if s.strip()])) / 3.0
    n_q = float(delex_text.count("?"))
    low = delex_text.lower()
    has_offer = float(any(w in low for w in [
        "star", "hotel", "package", "flight", "depart", "nights", "days", "resort", "[dst_city]", "[price]", "[budget]"
    ]))
    has_compare = float(any(w in low for w in [
        "or ", "options", "compare", "also have", "another", "between", "either", "both", "versus", "alternative"
    ]))
    has_unavail = float(any(w in low for w in [
        "sorry", "unfortunately", "no ", "not available", "unable", "cannot", "closest", "instead", "however", "feasible"
    ]))
    has_confirm = float(any(w in low for w in [
        "book", "confirm", "reserve", "total", "shall i", "would you like me to book", "finalize", "proceed"
    ]))
    return np.array([n_w, n_sents, n_q, has_offer, has_compare, has_unavail, has_confirm], dtype=np.float32)


def eligible_for_rq2(dialogue: Dict) -> bool:
    """Require at least 10 turns alternating USER/AGENT so index 9 is the 5th AGENT response."""
    t = dialogue["turns"]
    if len(t) < PREFIX_TURNS + 1:
        return False
    for idx in range(PREFIX_TURNS):
        expected_user = (idx % 2 == 0)
        is_user = (str(t[idx]["speaker"]).lower() == "user")
        if is_user != expected_user:
            return False
    return str(t[PREFIX_TURNS]["speaker"]).lower() != "user"


def format_mid_exemplar(delex_turns: List[str]) -> str:
    """Extract mid-dialogue negotiation window (up to 6 turns) for an exemplar."""
    if len(delex_turns) <= 6:
        return "\n".join(delex_turns)
    window = delex_turns[EXEMPLAR_START:min(len(delex_turns), EXEMPLAR_END)]
    return "\n".join(window)


def build_rq2_prompt(
    condition: str,
    prefix: str,
    exemplars: List[str],
    routed_archetype: str = None,
) -> str:
    parts = [BASE_SYSTEM_INSTRUCTION]
    if condition == "Cluster-Adaptive Few-Shot" and routed_archetype in ARCHETYPE_DIRECTIVES:
        parts.append(ARCHETYPE_DIRECTIVES[routed_archetype])
    if condition != "Zero-Shot" and exemplars:
        if condition == "Cluster-Adaptive Few-Shot":
            parts.append(
                f"Here are example conversation excerpts showing how an agent responds to "
                f"{routed_archetype} customers at this stage of negotiation (entity values are masked):"
            )
        else:
            parts.append(
                "Here are example conversation excerpts showing how an agent responds to customers "
                "(entity values are masked):"
            )
        for i, ex in enumerate(exemplars, 1):
            parts.append(f"Example {i}:\n{ex}")
    parts.append(f"Current conversation:\n{prefix}\nAGENT:")
    return "\n\n".join(parts)


def main(execute: bool = False, model_name: str = PRIMARY_AGENT_MODEL):
    rng = np.random.default_rng(SEED)
    sbert = SentenceTransformer(SBERT_MODEL)
    router = RefinedArchetypeRouter(sbert_model=sbert)
    df = router.df

    # 1. Build golden-partition mid-dialogue agent-style centroids (pure S-BERT + Hybrid S-BERT/Discourse)
    pool = df[(df.partition == "gold") & (df.task_success == True)].reset_index(drop=True)
    gold_utts_by_arch: Dict[str, List[str]] = {a: [] for a in REFINED_ARCHETYPES}
    all_gold_disc = []
    for _, row in pool.iterrows():
        did = row.dialogue_id
        arch = row.archetype_refined
        tx = router.delex_turns[did]
        # Mid-dialogue agent turns (turns 3..11) capture negotiation style rather than opening greetings
        mid_agent = [t[7:].strip() for t in tx[2:12] if t.startswith("AGENT:") and len(t[7:].strip()) > 3]
        if not mid_agent:
            mid_agent = [t[7:].strip() for t in tx if t.startswith("AGENT:") and len(t[7:].strip()) > 3]
        gold_utts_by_arch[arch].extend(mid_agent)
        for u in mid_agent:
            all_gold_disc.append(extract_discourse_features(u))

    disc_arr = np.vstack(all_gold_disc)
    disc_mu = disc_arr.mean(axis=0)
    disc_sd = disc_arr.std(axis=0) + 1e-6

    def to_hybrid_style_vec(texts: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """Return (sbert_norm [N, 384], hybrid_norm [N, 391]) with equal block weight."""
        e_sbert = sbert.encode(texts, batch_size=128, normalize_embeddings=True, show_progress_bar=False)
        d_feat = np.vstack([extract_discourse_features(t) for t in texts])
        d_std = (d_feat - disc_mu) / disc_sd
        d_norm = d_std / (np.linalg.norm(d_std, axis=1, keepdims=True) + 1e-12)
        # Weight semantic (0.5) and structural discourse (0.5) equally (parallels RQ1 Blocks)
        hyb = np.hstack([e_sbert * np.sqrt(0.5), d_norm * np.sqrt(0.5)]).astype(np.float32)
        hyb = hyb / (np.linalg.norm(hyb, axis=1, keepdims=True) + 1e-12)
        return e_sbert.astype(np.float32), hyb

    sbert_centroids: Dict[str, np.ndarray] = {}
    hybrid_centroids: Dict[str, np.ndarray] = {}
    for a in REFINED_ARCHETYPES:
        e_sb, e_hyb = to_hybrid_style_vec(gold_utts_by_arch[a])
        c_sb = e_sb.mean(axis=0)
        sbert_centroids[a] = c_sb / (np.linalg.norm(c_sb) + 1e-12)
        c_hyb = e_hyb.mean(axis=0)
        hybrid_centroids[a] = c_hyb / (np.linalg.norm(c_hyb) + 1e-12)

    # 2. Sample N = 33 eligible held-out dialogues (11 per Refined Archetype)
    test_df = df[df.partition == "test"].copy()
    test_df = test_df[test_df.dialogue_id.map(lambda i: eligible_for_rq2(router.canonical[i]))]
    picks = []
    for a in REFINED_ARCHETYPES:
        cands = test_df[test_df.archetype_refined == a].dialogue_id.values
        chosen = rng.choice(cands, size=min(N_PER_ARCH, len(cands)), replace=False)
        picks.extend(list(chosen))

    static_pool_dids = rng.choice(pool.dialogue_id.values, size=K_SHOT, replace=False)
    ex_static = [format_mid_exemplar(router.delex_turns[d]) for d in static_pool_dids]

    # 3. Pilot evaluation (routing accuracy, retrieval relevance, style metric validity)
    pilot_rows = []
    for did in picks:
        ret = router.route_and_retrieve(did, m_user_msgs=M_USER_MSGS, k_shot=K_SHOT)
        tx = router.delex_turns[did]
        prefix_str = "\n".join(tx[:PREFIX_TURNS])
        gold_reply = tx[PREFIX_TURNS][7:].strip()
        ex_cluster = [format_mid_exemplar(router.delex_turns[d]) for d in ret["cluster_exemplar_ids"]]

        # Compute hybrid retrieval similarity for static exemplars as comparison
        info = router.models_by_m[M_USER_MSGS]
        q_vec = info["X_norm"][info["id_to_row"][did]]
        stat_vecs = np.vstack([info["X_norm"][info["id_to_row"][sd]] for sd in static_pool_dids])
        sim_static = float((stat_vecs @ q_vec).mean())

        _, g_hyb = to_hybrid_style_vec([gold_reply])
        g_vec = g_hyb[0]
        target = ret["target_archetype"]
        own_sim = float(hybrid_centroids[target] @ g_vec)
        other_sims = [float(hybrid_centroids[a] @ g_vec) for a in REFINED_ARCHETYPES if a != target]

        pilot_rows.append(dict(
            dialogue_id=did,
            target_archetype=target,
            routed_archetype=ret["routed_archetype"],
            routing_correct=ret["routing_correct"],
            sim_static=sim_static,
            sim_global=ret["global_sim_mean"],
            sim_cluster=ret["cluster_sim_mean"],
            gold_style_own=own_sim,
            gold_style_other=float(np.mean(other_sims)),
            prefix=prefix_str,
            gold=gold_reply,
            ex_static=ex_static,
            ex_cluster=ex_cluster,
        ))

    dp = pd.DataFrame(pilot_rows)
    Ysim = dp[["sim_static", "sim_global", "sim_cluster"]].values
    t_style = stats.ttest_rel(dp.gold_style_own, dp.gold_style_other)
    diff_style = dp.gold_style_own - dp.gold_style_other
    pilot_summary = dict(
        N=len(dp),
        m_user_msgs=M_USER_MSGS,
        routing_accuracy_sample=float(dp.routing_correct.mean()),
        routing_accuracy_full_test=float(router.models_by_m[M_USER_MSGS]["acc_test"]),
        routing_kappa_full_test=float(router.models_by_m[M_USER_MSGS]["kappa_test"]),
        retrieval_rm=rm_anova(Ysim),
        retrieval_pairs=holm_pairwise(Ysim, ["Static", "Global k-NN", "Cluster-Adaptive"]).to_dict("records"),
        style_metric_t=dict(t=float(t_style.statistic), p=float(t_style.pvalue)),
        style_metric_dz=float(diff_style.mean() / diff_style.std(ddof=1)),
    )
    with open(os.path.join(FINAL_DATA_DIR, "rq2_refined_pilot_summary.json"), "w", encoding="utf-8") as f:
        json.dump(pilot_summary, f, indent=2)

    print("RQ2 Refined Pilot Summary:")
    print(json.dumps(pilot_summary, indent=2))

    # Build prompts
    prompts = []
    for _, r in dp.iterrows():
        for c in CONDITIONS:
            ex = [] if c == "Zero-Shot" else (r.ex_static if c == "Static Few-Shot" else r.ex_cluster)
            prompts.append(dict(
                key_id=f"{r.dialogue_id}__{c}",
                dialogue_id=r.dialogue_id,
                condition=c,
                target_archetype=r.target_archetype,
                routed_archetype=r.routed_archetype,
                routing_correct=bool(r.routing_correct),
                prompt=build_rq2_prompt(c, r.prefix, ex, routed_archetype=r.routed_archetype),
                gold=r.gold,
            ))

    if not execute:
        return

    # 4. Execute LLM generations (99 calls, cached)
    cache_fp = os.path.join(FINAL_DATA_DIR, "rq2_refined_generations.jsonl")
    llm = CachedLLMClient(cache_fp)
    gen_records = []
    for idx, p in enumerate(prompts, 1):
        rec = llm.generate_text(
            key_id=p["key_id"],
            prompt=p["prompt"],
            system_instruction=None,
            model=model_name,
            temperature=0.2,
            max_output_tokens=300,
            seed=SEED,
            metadata={k: p[k] for k in ("dialogue_id", "condition", "target_archetype", "routed_archetype", "routing_correct", "gold")},
        )
        gen_records.append(rec)
        if idx % 15 == 0 or idx == len(prompts):
            print(f"  Completed {idx}/{len(prompts)} RQ2 refined generations", flush=True)

    gens = pd.DataFrame(gen_records)
    gens = gens[gens.response.notna() & (gens.response.str.len() > 0)].copy()

    # De-lexicalize generated responses
    delex_resps = [delexicalize(t, []) for t in gens.response]
    resp_sbert, resp_hyb = to_hybrid_style_vec(delex_resps)
    gold_sbert, gold_hyb = to_hybrid_style_vec(gens.gold.tolist())

    gens["style_cos"] = [float(hybrid_centroids[a] @ v) for a, v in zip(gens.target_archetype, resp_hyb)]
    gens["sbert_style_cos"] = [float(sbert_centroids[a] @ v) for a, v in zip(gens.target_archetype, resp_sbert)]
    gens["gold_cos"] = [float(r @ g) for r, g in zip(resp_hyb, gold_hyb)]
    gens["sbert_gold_cos"] = [float(r @ g) for r, g in zip(resp_sbert, gold_sbert)]
    gens["words"] = gens.response.str.split().str.len().astype(float)
    gold_words_series = gens.drop_duplicates("dialogue_id").gold.str.split().str.len().astype(float)
    target_word_means = {
        a: float(np.mean([len(u.split()) for u in gold_utts_by_arch[a]]))
        for a in REFINED_ARCHETYPES
    }
    gens["word_abs_err"] = [abs(w - target_word_means[a]) for w, a in zip(gens["words"], gens["target_archetype"])]

    # Token-level overlap / BERTScore F1 (computed via S-BERT contextual token cosine max-pooling, Zhang et al., 2020)
    tok_model = sbert._first_module().auto_model
    tokenizer = sbert.tokenizer
    import torch
    tok_model.eval()
    bert_f1_scores = []
    with torch.no_grad():
        for cand_txt, ref_txt in zip(delex_resps, gens.gold.tolist()):
            inputs = tokenizer([cand_txt, ref_txt], padding=True, truncation=True, return_tensors="pt")
            inputs = {k: v.to(sbert.device) for k, v in inputs.items()}
            out = tok_model(**inputs).last_hidden_state
            # Exclude [CLS] and [SEP] and padding
            mask_c = inputs["attention_mask"][0].bool()
            mask_r = inputs["attention_mask"][1].bool()
            ec = torch.nn.functional.normalize(out[0][mask_c][1:-1], dim=-1)
            er = torch.nn.functional.normalize(out[1][mask_r][1:-1], dim=-1)
            if len(ec) == 0 or len(er) == 0:
                bert_f1_scores.append(0.5)
                continue
            sim_mat = ec @ er.T
            p_b = float(sim_mat.max(dim=1).values.mean().item())
            r_b = float(sim_mat.max(dim=0).values.mean().item())
            f1_b = 2 * p_b * r_b / (p_b + r_b + 1e-12)
            bert_f1_scores.append(f1_b)
    gens["bert_f1"] = bert_f1_scores

    gens.to_csv(os.path.join(FINAL_DATA_DIR, "rq2_refined_scored.csv"), index=False)

    # 5. Statistical Analysis (RM-ANOVA + Holm contrasts + Friedman)
    results = {}
    summary_rows = []
    for dv in ["style_cos", "sbert_style_cos", "gold_cos", "bert_f1", "words", "word_abs_err"]:
        Y = gens.pivot(index="dialogue_id", columns="condition", values=dv)[CONDITIONS].values.astype(float)
        aov = rm_anova(Y)
        pairs = holm_pairwise(Y, CONDITIONS)
        fr = stats.friedmanchisquare(*Y.T)
        shapiro_diffs = {
            f"{CONDITIONS[j]} - {CONDITIONS[i]}": dict(
                W=float(stats.shapiro(Y[:, j] - Y[:, i]).statistic),
                p=float(stats.shapiro(Y[:, j] - Y[:, i]).pvalue),
            )
            for i in range(3) for j in range(i + 1, 3)
        }
        results[dv] = dict(
            desc={c: dict(M=float(Y[:, i].mean()), SD=float(Y[:, i].std(ddof=1))) for i, c in enumerate(CONDITIONS)},
            anova=aov,
            pairs=pairs.to_dict("records"),
            friedman=dict(chi2=float(fr.statistic), p=float(fr.pvalue)),
            shapiro_diffs=shapiro_diffs,
        )
        pairs.to_csv(os.path.join(FINAL_TABLE_DIR, f"t_rq2_refined_{dv}_pairs.csv"), index=False)
        summary_rows.append(dict(
            outcome=dv,
            zero_shot_M=float(Y[:, 0].mean()),
            zero_shot_SD=float(Y[:, 0].std(ddof=1)),
            static_M=float(Y[:, 1].mean()),
            static_SD=float(Y[:, 1].std(ddof=1)),
            cluster_M=float(Y[:, 2].mean()),
            cluster_SD=float(Y[:, 2].std(ddof=1)),
            F_gg=aov["F"],
            df1_gg=aov["df1_gg"],
            df2_gg=aov["df2_gg"],
            p_gg=aov["p_gg"],
            eta2_partial=aov["eta2_partial"],
            friedman_chi2=float(fr.statistic),
            friedman_p=float(fr.pvalue),
        ))

    sum_df = pd.DataFrame(summary_rows)
    sum_df.to_csv(os.path.join(FINAL_TABLE_DIR, "t_rq2_refined_summary.csv"), index=False)

    # 6. Publication Figure for RQ2 Refined
    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.2), dpi=300)
    labs = ["Zero-Shot", "Static\nFew-Shot", "Cluster-\nAdaptive"]
    panels = [
        (axes[0], "sbert_style_cos", "Style convergence (S-BERT cosine to centroid)", "A. Primary: Style Convergence"),
        (axes[1], "word_abs_err", "Absolute word-length error vs. archetype target", "B. Archetype Pacing Error (Lower = Better)"),
        (axes[2], "words", "Words per generated agent turn", "C. Response Length Distribution"),
    ]
    for ax, dv, ylab, title in panels:
        Y = gens.pivot(index="dialogue_id", columns="condition", values=dv)[CONDITIONS].values.astype(float)
        ax.boxplot([Y[:, i] for i in range(3)], tick_labels=labs, showmeans=True)
        for i in range(len(Y)):
            ax.plot([1, 2, 3], Y[i], color="grey", alpha=0.22, lw=0.7)
        ax.set_ylabel(ylab)
        ax.set_title(title)
    axes[2].axhline(gold_words_series.mean(), color="#2ca02c", ls="--", lw=1.3, label=f"Human mean ({gold_words_series.mean():.1f}w)")
    axes[2].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FINAL_FIG_DIR, "fig_rq2_refined_results.png"))
    plt.close(fig)

    out_payload = dict(
        N=int(gens.dialogue_id.nunique()),
        model=model_name,
        n_calls=len(gen_records),
        pilot=pilot_summary,
        gold_words=dict(M=float(gold_words_series.mean()), SD=float(gold_words_series.std(ddof=1))),
        results=results,
    )
    with open(os.path.join(FINAL_DATA_DIR, "rq2_refined_results.json"), "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)

    print("\nRQ2 Refined Summary Table:")
    print(sum_df.round(4).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true", help="Call Gemini and run full RM-ANOVA")
    ap.add_argument("--model", default=PRIMARY_AGENT_MODEL)
    args = ap.parse_args()
    main(execute=args.execute, model_name=args.model)
