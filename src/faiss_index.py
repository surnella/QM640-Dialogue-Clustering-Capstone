"""
FAISS Vector Index for Archetype-Guided In-Context Exemplar Retrieval.
Uses IndexFlatIP for exact cosine similarity search over S-BERT trajectory embeddings.
"""

import os
import faiss
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple


class ArchetypeFaissIndex:
    def __init__(self, embedding_dim: int = 384):
        self.embedding_dim = embedding_dim
        # Global index
        self.global_index = faiss.IndexFlatIP(embedding_dim)
        # Cluster-specific sub-indices
        self.cluster_indices: Dict[str, faiss.IndexFlatIP] = {}
        self.cluster_metadata: Dict[str, List[Dict[str, Any]]] = {}
        self.all_metadata: List[Dict[str, Any]] = []

    def build_index(
        self,
        embeddings_path: str = "data/embeddings/trajectory_embeddings.npy",
        clustered_metadata_path: str = "data/embeddings/clustered_trajectories.csv"
    ):
        print(f"Loading embeddings for FAISS indexing from {embeddings_path}...")
        X = np.load(embeddings_path).astype(np.float32)
        df_meta = pd.read_csv(clustered_metadata_path)

        # Ensure L2 normalization for inner-product cosine similarity
        faiss.normalize_L2(X)
        self.global_index.add(X)
        self.all_metadata = df_meta.to_dict('records')

        # Build archetype-specific partitions
        unique_archetypes = df_meta['archetype'].dropna().unique()
        for arch in unique_archetypes:
            sub_mask = (df_meta['archetype'] == arch).values
            X_sub = X[sub_mask].copy()
            idx = faiss.IndexFlatIP(self.embedding_dim)
            idx.add(X_sub)
            self.cluster_indices[arch] = idx
            self.cluster_metadata[arch] = df_meta[sub_mask].to_dict('records')
            print(f"Indexed {idx.ntotal} exemplars for archetype: '{arch}'")

        print(f"FAISS Global Index contains {self.global_index.ntotal} total trajectories.")

    def search_cluster_exemplars(
        self,
        query_vector: np.ndarray,
        target_archetype: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top-k closest exemplars from the specific target archetype partition.
        """
        if target_archetype not in self.cluster_indices:
            raise ValueError(f"Archetype '{target_archetype}' not found in index.")

        q = query_vector.reshape(1, -1).astype(np.float32).copy()
        faiss.normalize_L2(q)

        D, I = self.cluster_indices[target_archetype].search(q, top_k)
        results = []
        meta_list = self.cluster_metadata[target_archetype]

        for dist, idx in zip(D[0], I[0]):
            if idx < len(meta_list):
                res = meta_list[idx].copy()
                res['retrieval_similarity'] = float(dist)
                results.append(res)
        return results

    def search_nearest_archetype(
        self,
        query_vector: np.ndarray
    ) -> Tuple[str, float]:
        """
        Matches a query conversation to the nearest overall trajectory archetype.
        """
        q = query_vector.reshape(1, -1).astype(np.float32).copy()
        faiss.normalize_L2(q)
        D, I = self.global_index.search(q, 1)
        best_idx = I[0][0]
        best_meta = self.all_metadata[best_idx]
        return best_meta.get('archetype', 'Unknown'), float(D[0][0])
