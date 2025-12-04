"""
Stock impact analysis module.

Maps extracted entities (companies, sectors, regulators)
to impacted stocks with confidence scores.
"""

from typing import List, Dict
from .config import company_to_symbol, company_to_sector


def map_stock_impact(
    companies: List[str],
    sectors: List[str],
    regulators: List[str],
) -> List[Dict]:
    """
    Given lists of companies, sectors, and regulators for a news item,
    return a list of impacted stocks with confidence and impact type.

    Rules:
    - Direct company mention       -> confidence 1.0,   type "direct"
    - Sector-wide news             -> confidence 0.7,   type "sector"
    - RBI / regulator-driven news  -> confidence 0.6,   type "regulatory"
    """
    impacts: List[Dict] = []

    # 1) Direct company impacts
    for comp in companies:
        symbol = company_to_symbol.get(comp)
        if symbol:
            impacts.append({
                "symbol": symbol,
                "confidence": 1.0,
                "type": "direct",
                "source": comp,
            })

    # 2) Sector-wide impacts
    if sectors:
        for sector in sectors:
            for comp, sec in company_to_sector.items():
                if sec == sector:
                    symbol = company_to_symbol.get(comp)
                    if symbol:
                        impacts.append({
                            "symbol": symbol,
                            "confidence": 0.7,
                            "type": "sector",
                            "source": sector,
                        })

    # 3) Regulator impacts (example: RBI -> affects all banking stocks)
    if regulators:
        for reg in regulators:
            if reg == "RBI":
                for comp, sec in company_to_sector.items():
                    if sec == "Banking":
                        symbol = company_to_symbol.get(comp)
                        if symbol:
                            impacts.append({
                                "symbol": symbol,
                                "confidence": 0.6,
                                "type": "regulatory",
                                "source": reg,
                            })

    return impacts


def add_impacts_to_df(df):
    """
    Given a DataFrame with extracted entity columns,
    add 'impacted_stocks' as a new column.
    """
    df["impacted_stocks"] = df.apply(
        lambda row: map_stock_impact(
            row.get("companies", []),
            row.get("sectors", []),
            row.get("regulators", []),
        ),
        axis=1,
    )
    return df
