"""
Ingestion module.

Loads financial news data from a CSV file or falls back to a small mock dataset.
"""

from pathlib import Path
from typing import Optional
import pandas as pd

# Default path for mock dataset
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "mock_news.csv"


def load_news_dataset(path: Optional[str] = None) -> pd.DataFrame:
    """
    Load the news dataset from CSV.

    If `path` is not provided, it tries to load from:
        data/mock_news.csv

    If the file does not exist, it returns a small in-memory
    mock dataset (6 rows) so that the rest of the pipeline still works.
    """
    csv_path = Path(path) if path else DATA_PATH

    if csv_path.exists():
        df = pd.read_csv(csv_path)
        # Ensure required columns exist
        if "id" not in df.columns:
            df["id"] = [f"N{i+1}" for i in range(len(df))]
        if "title" not in df.columns:
            raise ValueError("CSV must contain a 'title' column.")
        return df

    # Fallback: tiny mock dataset (same as in your notebook)
    data = [
        {"id": "N1", "title": "HDFC Bank announces 15% dividend, board approves stock buyback"},
        {"id": "N2", "title": "RBI raises repo rate by 25bps to 6.75%, citing inflation concerns"},
        {"id": "N3", "title": "Reserve Bank hikes interest rates by 0.25% to fight rising prices"},
        {"id": "N4", "title": "ICICI Bank opens 500 new branches across Tier-2 cities"},
        {"id": "N5", "title": "Central bank increases policy rate by 25 basis points, signals hawkish stance"},
        {"id": "N6", "title": "Banking sector NPAs decline to 5-year low, credit growth at 16%"},
    ]
    df = pd.DataFrame(data)
    return df
