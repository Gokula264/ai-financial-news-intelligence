"""
Deduplication module.

Uses sentence-transformer embeddings + cosine similarity
to cluster semantically similar news items into story groups.
"""

from typing import List, Dict
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load model once
_model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_embeddings(df: pd.DataFrame, text_col: str = "title") -> np.ndarray:
    """
    Compute sentence embeddings for the given text column.
    """
    texts = df[text_col].tolist()
    embeddings = _model.encode(texts, convert_to_numpy=True)
    return embeddings


def cluster_articles(sim_matrix: np.ndarray, ids: List[str], threshold: float = 0.8) -> List[List[str]]:
    """
    Simple clustering based on similarity threshold.

    Articles whose pairwise cosine similarity >= threshold
    are grouped into the same cluster.
    """
    visited = set()
    clusters: List[List[str]] = []

    for i, id_i in enumerate(ids):
        if id_i in visited:
            continue
        cluster = [id_i]
        visited.add(id_i)

        for j, id_j in enumerate(ids):
            if id_j in visited:
                continue
            if sim_matrix[i, j] >= threshold:
                cluster.append(id_j)
                visited.add(id_j)

        clusters.append(cluster)

    return clusters


def add_story_ids(df: pd.DataFrame, threshold: float = 0.8) -> pd.DataFrame:
    """
    Compute embeddings, similarity matrix, clusters, and assign story_ids
    to the DataFrame.

    Returns the same DataFrame with a new 'story_id' column.
    """
    if "id" not in df.columns:
        raise ValueError("DataFrame must have an 'id' column for deduplication.")

    embeddings = compute_embeddings(df, text_col="title")
    sim_matrix = cosine_similarity(embeddings)

    ids = df["id"].tolist()
    clusters = cluster_articles(sim_matrix, ids, threshold=threshold)

    # Map news id -> story_id (story_1, story_2, ...)
    cluster_map: Dict[str, str] = {}
    for i, group in enumerate(clusters):
        story_id = f"story_{i + 1}"
        for news_id in group:
            cluster_map[news_id] = story_id

    df["story_id"] = df["id"].map(cluster_map)
    return df
