"""
Entity extraction module.

Responsible for converting raw news text into structured entities:
- companies
- sectors
- regulators
"""

from typing import Dict, List
import spacy

from .config import (
    company_to_symbol,
    company_to_sector,
    sector_keywords,
    regulator_keywords,
)

# Load spaCy model once at import time
nlp = spacy.load("en_core_web_sm")


def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract companies, sectors and regulators from a news title/paragraph.

    Returns a dict with keys: companies, sectors, regulators
    """
    doc = nlp(text)

    companies = set()
    sectors = set()
    regulators = set()

    lower_text = text.lower()

    # 1) spaCy NER: detect companies
    for ent in doc.ents:
        if ent.label_ == "ORG":
            for comp in company_to_symbol.keys():
                if comp.lower() in ent.text.lower():
                    companies.add(comp)

    # 2) Substring search backup
    for comp in company_to_symbol.keys():
        if comp.lower() in lower_text:
            companies.add(comp)

    # 3) Sector keywords
    for kw, sector in sector_keywords.items():
        if kw in lower_text:
            sectors.add(sector)

    # 4) Regulator keywords
    for kw, reg in regulator_keywords.items():
        if kw.lower() in lower_text:
            regulators.add(reg)

    return {
        "companies": list(companies),
        "sectors": list(sectors),
        "regulators": list(regulators),
    }


def add_entities_to_df(df):
    """
    Convenience helper: adds extracted entity columns to dataframe.
    """
    entity_results = df["title"].apply(extract_entities)
    df["companies"] = entity_results.apply(lambda x: x["companies"])
    df["sectors"] = entity_results.apply(lambda x: x["sectors"])
    df["regulators"] = entity_results.apply(lambda x: x["regulators"])
    return df
