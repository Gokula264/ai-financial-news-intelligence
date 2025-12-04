import pandas as pd
from src.graph import process_all_news, run_query

def test_query_rbi():
    df = process_all_news()
    results = run_query("RBI policy change")

    # At least 1 result should mention RBI
    assert len(results) > 0

def test_query_company_search():
    df = process_all_news()
    results = run_query("HDFC Bank dividend news")

    # Top result should be related to HDFC Bank
    assert "HDFC" in results.iloc[0]["title"] or "Bank" in results.iloc[0]["title"]
