"""
Trajectory Vectorizer using Sentence-BERT (all-MiniLM-L6-v2)
and Temporal Decay Weighted Mean Pooling.
Produces dense 384-dimensional trajectory embeddings for dialogue clustering.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

try:
    from src.canonical_schema import CanonicalDialogueTrajectory
except ModuleNotFoundError:
    from canonical_schema import CanonicalDialogueTrajectory


def compute_temporal_decay_weights(num_turns: int, decay_lambda: float = 0.15) -> np.ndarray:
    """
    Computes exponential temporal decay weights across conversational turns:
    w_t = exp(-lambda * (T - t)) / sum(exp(-lambda * (T - j)))
    Later turns (negotiation culmination and slot commitments) receive higher weights,
    while early turns maintain foundational contextual grounding.
    """
    if num_turns == 1:
        return np.array([1.0])
    
    t_indices = np.arange(1, num_turns + 1)
    # T - t
    deltas = num_turns - t_indices
    raw_weights = np.exp(-decay_lambda * deltas)
    return raw_weights / np.sum(raw_weights)


class TrajectoryVectorizer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        print(f"Loading SentenceTransformer model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = 384

    def vectorize_trajectories(
        self,
        canonical_json_path: str = "data/canonical/canonical_dialogues.json",
        output_embeddings_npy: str = "data/embeddings/trajectory_embeddings.npy",
        output_metadata_csv: str = "data/embeddings/metadata.csv",
        max_samples: int = 1500,
        decay_lambda: float = 0.15
    ):
        """
        Embeds dialogue sessions using turn-level S-BERT embeddings combined with
        temporal decay weighting.
        """
        if not os.path.exists(canonical_json_path):
            raise FileNotFoundError(f"Canonical data not found: {canonical_json_path}")

        print(f"Reading canonical trajectories from {canonical_json_path}...")
        with open(canonical_json_path, 'r', encoding='utf-8') as f:
            raw_dialogues = json.load(f)

        if max_samples and len(raw_dialogues) > max_samples:
            print(f"Subsampling to {max_samples} dialogues for balanced benchmarking...")
            # Sample across sources: Frames (all 1369), enterprise (all 24), and balance
            frames_dialogues = [d for d in raw_dialogues if d.get('source_dataset') == 'frames']
            ent_dialogues = [d for d in raw_dialogues if d.get('source_dataset') == 'enterprise']
            mwoz_dialogues = [d for d in raw_dialogues if d.get('source_dataset') == 'multiwoz']
            
            selected = frames_dialogues + ent_dialogues + mwoz_dialogues[:max(0, max_samples - len(frames_dialogues) - len(ent_dialogues))]
            raw_dialogues = selected

        print(f"Vectorizing {len(raw_dialogues)} dialogue trajectories...")
        
        trajectory_vectors = []
        metadata_records = []

        # Process in batches
        for idx, d in enumerate(raw_dialogues):
            turns = d.get('turns', [])
            if not turns:
                continue

            turn_texts = [f"{t.get('speaker', 'user')}: {t.get('utterance', '')}" for t in turns]
            weights = compute_temporal_decay_weights(len(turns), decay_lambda=decay_lambda)

            # Turn-level embeddings
            turn_embs = self.model.encode(turn_texts, show_progress_bar=False, batch_size=32)
            
            # Weighted average across turns
            weighted_traj_emb = np.sum(turn_embs * weights[:, np.newaxis], axis=0)
            
            # L2 normalize
            norm = np.linalg.norm(weighted_traj_emb)
            if norm > 0:
                weighted_traj_emb = weighted_traj_emb / norm

            trajectory_vectors.append(weighted_traj_emb)
            
            metadata_records.append({
                "dialogue_id": d.get("dialogue_id"),
                "source_dataset": d.get("source_dataset"),
                "total_turns": d.get("total_turns"),
                "user_turns": d.get("user_turns"),
                "wizard_turns": d.get("wizard_turns"),
                "revisions_count": d.get("revisions_count", 0),
                "hesitation_markers_count": d.get("hesitation_markers_count", 0),
                "budget_specified": d.get("budget_specified", False),
                "turn_ratio": d.get("user_turns", 1) / max(1, d.get("wizard_turns", 1))
            })

            if (idx + 1) % 200 == 0 or (idx + 1) == len(raw_dialogues):
                print(f"Processed {idx + 1}/{len(raw_dialogues)} trajectories.")

        X = np.array(trajectory_vectors, dtype=np.float32)
        df_meta = pd.DataFrame(metadata_records)

        os.makedirs(os.path.dirname(output_embeddings_npy), exist_ok=True)
        np.save(output_embeddings_npy, X)
        df_meta.to_csv(output_metadata_csv, index=False)
        print(f"Cached {X.shape[0]} trajectory embeddings (dim={X.shape[1]}) to {output_embeddings_npy}")
        print(f"Saved metadata to {output_metadata_csv}")
        return X, df_meta


if __name__ == "__main__":
    vectorizer = TrajectoryVectorizer()
    X, df_meta = vectorizer.vectorize_trajectories(
        canonical_json_path="data/canonical/canonical_dialogues.json",
        max_samples=1500
    )
    print("Vectorization complete.")
