"""
Query engine module.

Provides:
- understand_query: extract intent entities from user query
- search_news: combine entity filters + semantic similarity to rank news
"""

from typing import Dict, List
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .config import (
    company_to_symbol,
    company_to_sector,
    sector_keywords,
    regulator_keywords,
)

# Reuse the same model name as in deduplication
_model = SentenceTransformer("all-MiniLM-L6-v2")


def understand_query(query: str) -> Dict[str, List[str]]:
    """
    Parse a natural language query and detect target entities:
    - companies
    - sectors
    - regulators

    Example:
    "HDFC Bank news"           -> companies=["HDFC Bank"], sectors=["Banking"]
    "Banking sector update"    -> sectors=["Banking"]
    "RBI policy changes"       -> regulators=["RBI"]
    """
    q_lower = query.lower()

    q_companies: List[str] = []
    q_sectors: List[str] = []
    q_regulators: List[str] = []

    # Company mentions
    for comp in company_to_symbol.keys():
        if comp.lower() in q_lower:
            q_companies.append(comp)

    # Sector keywords
    for kw, sector in sector_keywords.items():
        if kw in q_lower:
            q_sectors.append(sector)

    # Regulator keywords
    for kw, reg in regulator_keywords.items():
        if kw.lower() in q_lower:
            q_regulators.append(reg)

    # If a company is mentioned, also consider its sector (company -> sector news)
    for comp in q_companies:
        sec = company_to_sector.get(comp)
        if sec and sec not in q_sectors:
            q_sectors.append(sec)

    return {
        "companies": q_companies,
        "sectors": q_sectors,
        "regulators": q_regulators,
    }


def _filter_by_entities(df: pd.DataFrame, ents: Dict[str, List[str]]) -> pd.DataFrame:
    """
    Filter DataFrame rows based on query entities.
    If nothing matches, returns the original df.
    """
    q_companies = set(ents["companies"])
    q_sectors = set(ents["sectors"])
    q_regulators = set(ents["regulators"])

    if not (q_companies or q_sectors or q_regulators):
        # No entity info -> do not filter, just rely on semantic search
        return df

    def row_matches(row) -> bool:
        has_company = bool(q_companies.intersection(row.get("companies", [])))
        has_sector = bool(q_sectors.intersection(row.get("sectors", [])))
        has_reg = bool(q_regulators.intersection(row.get("regulators", [])))
        return has_company or has_sector or has_reg

    mask = df.apply(row_matches, axis=1)
    filtered = df[mask]

    # If nothing matched entities, fall back to full df
    if filtered.empty:
        return df
    return filtered


def search_news(query: str, df: pd.DataFrame, top_k: int = 5) -> pd.DataFrame:
    """
    Main search function.

    Steps:
    1. Understand query (detect companies/sectors/regulators)
    2. Filter DataFrame rows based on entities
    3. Compute semantic similarity between query and news titles
    4. Return top_k most relevant rows with a 'similarity' column
    """
    if "title" not in df.columns:
        raise ValueError("DataFrame must have a 'title' column for search.")

    ents = understand_query(query)
    candidates = _filter_by_entities(df, ents)

    # Semantic similarity on candidate titles
    q_emb = _model.encode([query], convert_to_numpy=True)
    cand_titles = candidates["title"].tolist()
    cand_embs = _model.encode(cand_titles, convert_to_numpy=True)

    sims = cosine_similarity(q_emb, cand_embs)[0]
    candidates = candidates.copy()
    candidates["similarity"] = sims

    # Sort by similarity (highest first)
    results = candidates.sort_values(by="similarity", ascending=False).head(top_k)

    # Reorder columns nicely if present
    cols = [c for c in ["id", "story_id", "title", "companies", "sectors", "regulators", "impacted_stocks", "similarity"] if c in results.columns]
    return results[cols]
