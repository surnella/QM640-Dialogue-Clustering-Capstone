"""
Refined-archetype prefix routing, FAISS exemplar sub-index retrieval, and
cluster-adaptive prompt construction for `src/final_pipeline/`.

All parameters (PCA, block scaling, logistic router, FAISS sub-indices, and
agent-style centroids) are fitted strictly on the golden partition (`partition == 'gold'`)
to prevent any data leakage into the held-out test partition (`partition == 'test'`).
"""

import glob
import hashlib
import json
import os
import sys
from typing import Dict, List, Optional, Tuple

import faiss
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, cohen_kappa_score

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.path.join(ROOT, "src", "interim_pipeline") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "src", "interim_pipeline"))

from common import (  # noqa: E402
    SEED,
    WORK_DIR,
    delexicalize,
    dialogue_slot_values,
    embed_dialogues,
    load_canonical,
    load_frames_raw,
    speaker_tag,
)
from step2e_llm_user_annotation import truncate  # noqa: E402
from step2f_rq1_llm_hybrid import Blocks, llm_matrix, load_ann  # noqa: E402

REFINED_ARCHETYPES: List[str] = [
    "Decisive Booker",
    "Open Explorer",
    "Rigid-Constraint Seeker",
]

# Empirically derived communication directives from golden-partition wizard discourse
# (see Table 14 and golden-partition dialogue-act profile):
ARCHETYPE_DIRECTIVES: Dict[str, str] = {
    "Decisive Booker": (
        "Customer Archetype: Decisive Booker (high decisiveness, specific trip goal, low revision rate). "
        "Style & Pacing Directive: Respond concisely in 12-16 words (1-2 sentences). Directly confirm matching "
        "package details (dates, hotel tier, price) and move straight toward booking confirmation without "
        "unnecessary open-ended exploration."
    ),
    "Open Explorer": (
        "Customer Archetype: Open Explorer (high destination/date flexibility, broad option comparison). "
        "Style & Pacing Directive: Respond consultatively in 14-18 words (1-2 sentences). Present or compare "
        "concrete destination/package options side-by-side (highlighting star rating, duration, or budget trade-offs) "
        "and invite the customer to narrow their preference."
    ),
    "Rigid-Constraint Seeker": (
        "Customer Archetype: Rigid-Constraint Seeker (strict fixed destination/dates, low flexibility, high constraint conflict rate). "
        "Style & Pacing Directive: Respond crisply in 10-14 words (1-2 sentences). Directly address the exact "
        "availability or constraint feasibility first; if the strict constraint cannot be met, immediately propose "
        "the closest feasible alternative date, duration, or package."
    ),
}

GDIR = os.path.join(ROOT, "data", "embeddings", "gemini")
CACHE_DIR = os.path.join(GDIR, "cache")


def _sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def load_gemini_embedding_cache() -> Dict[str, np.ndarray]:
    """Load pre-cached 3,072-d Gemini embeddings from `data/embeddings/gemini/cache/`."""
    lookup: Dict[str, np.ndarray] = {}
    for fp in glob.glob(os.path.join(CACHE_DIR, "*.json")):
        npy_path = fp[:-5] + ".npy"
        if not os.path.exists(npy_path):
            continue
        arr = np.load(npy_path)
        with open(fp, "r", encoding="utf-8") as f:
            keys = json.load(f)
        for k, v in zip(keys, arr):
            lookup[k] = v
    return lookup


class RefinedArchetypeRouter:
    """
    Routes a conversation prefix (first M user messages, M in {3, 5, 7, 9}) to one of the
    three Refined Archetypes (`Decisive Booker`, `Open Explorer`, `Rigid-Constraint Seeker`)
    using the exact Hybrid Blocks representation (PCA-20 Gemini user prefix embedding +
    opening LLM behavioral profile) fitted strictly on the golden partition (`D_gold`).
    Also builds per-archetype FAISS retrieval indices on `D_gold`.
    """

    def __init__(self, sbert_model=None):
        self.df = pd.read_csv(os.path.join(WORK_DIR, "frames_archetypes_refined.csv"))
        self.gold_mask = (self.df.partition == "gold").values
        self.test_mask = (self.df.partition == "test").values
        self.frames_raw = load_frames_raw()
        self.canonical = {d["dialogue_id"]: d for d in load_canonical(("frames",))}
        self.emb_lookup = load_gemini_embedding_cache()
        self.sbert = sbert_model

        # Precompute de-lexicalised turn texts for all 1,334 analytic Frames dialogues
        self.delex_turns: Dict[str, List[str]] = {}
        self.slot_vals: Dict[str, List[tuple]] = {}
        for did in self.df.dialogue_id:
            d = self.canonical[did]
            sv = dialogue_slot_values(d, self.frames_raw)
            self.slot_vals[did] = sv
            self.delex_turns[did] = [
                f"{speaker_tag(t.get('speaker'))}: {delexicalize(t.get('utterance', ''), sv)}"
                for t in d["turns"]
            ]

        self.models_by_m: Dict[int, Dict] = {}
        for m in (3, 5, 7, 9):
            self._fit_prefix_router(m)

    def _fit_prefix_router(self, m_user_msgs: int) -> None:
        docs = []
        for did in self.df.dialogue_id:
            rt = self.frames_raw[did]["turns"]
            tx = self.delex_turns[did]
            l_cut = len(truncate(rt, m_user_msgs))
            user_tx = "\n".join(x for x in tx[:l_cut] if x.startswith("USER:")) or tx[0]
            docs.append(user_tx)

        emb = np.array([self.emb_lookup[_sha1(t)] for t in docs], dtype=np.float32)
        ann_path = os.path.join(WORK_DIR, f"llm_user_annotations_u{m_user_msgs}.jsonl")
        ann = load_ann(ann_path).loc[self.df.dialogue_id]

        pca = PCA(20, random_state=SEED).fit(emb[self.gold_mask])
        eb = pca.transform(emb)
        lb = llm_matrix(ann).values
        blocks = Blocks().fit([eb[self.gold_mask], lb[self.gold_mask]], [False, True])
        X = blocks.transform([eb, lb]).astype(np.float32)

        y = self.df.archetype_refined.values
        clf = LogisticRegression(max_iter=3000, C=1.0, random_state=SEED)
        clf.fit(X[self.gold_mask], y[self.gold_mask])

        pred_test = clf.predict(X[self.test_mask])
        acc_test = float(accuracy_score(y[self.test_mask], pred_test))
        kap_test = float(cohen_kappa_score(y[self.test_mask], pred_test))

        # L2-normalised hybrid vectors for cosine similarity & FAISS retrieval
        norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-12
        X_norm = (X / norms).astype(np.float32)

        # Build FAISS indices on successful golden-partition dialogues
        gold_success_mask = self.gold_mask & (self.df.task_success.values == True)
        gold_indices = np.where(gold_success_mask)[0]
        X_pool = X_norm[gold_indices]
        y_pool = y[gold_indices]
        dids_pool = self.df.dialogue_id.values[gold_indices]

        global_index = faiss.IndexFlatIP(X_pool.shape[1])
        global_index.add(X_pool)

        sub_indices = {}
        centroids = {}
        for arch in REFINED_ARCHETYPES:
            sub_m = np.where(y_pool == arch)[0]
            ix = faiss.IndexFlatIP(X_pool.shape[1])
            ix.add(X_pool[sub_m])
            sub_indices[arch] = (ix, gold_indices[sub_m], dids_pool[sub_m])
            c = X_pool[sub_m].mean(axis=0)
            centroids[arch] = c / (np.linalg.norm(c) + 1e-12)

        id_to_row = {did: i for i, did in enumerate(self.df.dialogue_id.values)}
        self.models_by_m[m_user_msgs] = dict(
            pca=pca,
            blocks=blocks,
            clf=clf,
            X_norm=X_norm,
            pred_all=clf.predict(X),
            proba_all=clf.predict_proba(X),
            acc_test=acc_test,
            kappa_test=kap_test,
            global_index=global_index,
            gold_indices=gold_indices,
            dids_pool=dids_pool,
            sub_indices=sub_indices,
            centroids=centroids,
            id_to_row=id_to_row,
        )

    def routing_diagnostics_table(self) -> pd.DataFrame:
        """Return held-out routing accuracy and Cohen's kappa across prefix cut-offs M in {3, 5, 7, 9}."""
        rows = []
        for m in (3, 5, 7, 9):
            info = self.models_by_m[m]
            rows.append(
                dict(
                    user_messages_m=m,
                    approx_dialogue_turns=m * 2 - 1,
                    test_n=int(self.test_mask.sum()),
                    routing_accuracy=info["acc_test"],
                    routing_kappa=info["kappa_test"],
                )
            )
        return pd.DataFrame(rows)

    def route_and_retrieve(
        self,
        dialogue_id: str,
        m_user_msgs: int = 5,
        k_shot: int = 3,
        exemplar_turns: int = 6,
        use_oracle_archetype: bool = False,
    ) -> Dict:
        """
        Route `dialogue_id` using its first `m_user_msgs` user messages and retrieve
        top-k golden exemplars from the routed archetype sub-index (and global k-NN).
        """
        info = self.models_by_m[m_user_msgs]
        row_idx = info["id_to_row"][dialogue_id]
        target_arch = str(self.df.archetype_refined.iloc[row_idx])
        routed_arch = target_arch if use_oracle_archetype else str(info["pred_all"][row_idx])
        q = info["X_norm"][row_idx : row_idx + 1]

        # Sub-index retrieval for routed archetype
        ix, pool_rows, pool_dids = info["sub_indices"][routed_arch]
        sims_c, idx_c = ix.search(q, k_shot + 1)
        chosen_c_dids, chosen_c_sims = [], []
        for s, j in zip(sims_c[0], idx_c[0]):
            cand_did = str(pool_dids[j])
            if cand_did != dialogue_id and len(chosen_c_dids) < k_shot:
                chosen_c_dids.append(cand_did)
                chosen_c_sims.append(float(s))

        # Global k-NN retrieval
        sims_g, idx_g = info["global_index"].search(q, k_shot + 1)
        chosen_g_dids, chosen_g_sims = [], []
        for s, j in zip(sims_g[0], idx_g[0]):
            cand_did = str(info["dids_pool"][j])
            if cand_did != dialogue_id and len(chosen_g_dids) < k_shot:
                chosen_g_dids.append(cand_did)
                chosen_g_sims.append(float(s))

        return dict(
            dialogue_id=dialogue_id,
            target_archetype=target_arch,
            routed_archetype=routed_arch,
            routing_correct=(routed_arch == target_arch),
            cluster_exemplar_ids=chosen_c_dids,
            cluster_exemplar_texts=[self.format_exemplar(d, exemplar_turns, delex=True) for d in chosen_c_dids],
            cluster_exemplar_raw_texts=[self.format_exemplar(d, exemplar_turns, delex=False) for d in chosen_c_dids],
            cluster_sim_mean=float(np.mean(chosen_c_sims)),
            global_exemplar_ids=chosen_g_dids,
            global_exemplar_texts=[self.format_exemplar(d, exemplar_turns, delex=True) for d in chosen_g_dids],
            global_sim_mean=float(np.mean(chosen_g_sims)),
        )

    def format_exemplar(self, dialogue_id: str, max_turns: int = 6, delex: bool = True) -> str:
        """Format a golden dialogue prefix as a de-lexicalised or raw exemplar."""
        if delex:
            return "\n".join(self.delex_turns[dialogue_id][:max_turns])
        d = self.canonical[dialogue_id]
        return "\n".join(
            f"{speaker_tag(t.get('speaker'))}: {t.get('utterance', '')}"
            for t in d["turns"][:max_turns]
        )

