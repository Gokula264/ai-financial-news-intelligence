import pandas as pd
from src.entities import extract_entities

def test_entity_extraction_rbi():
    text = "RBI raises repo rate to control inflation"
    result = extract_entities(text)
    assert "RBI" in result["regulators"]

def test_entity_extraction_company():
    text = "HDFC Bank announces quarterly earnings"
    result = extract_entities(text)
    assert "HDFC Bank" in result["companies"]
