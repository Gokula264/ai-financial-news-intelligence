"""
Shared configuration and mapping tables for the AI Financial News system.
"""

# Known companies and their stock symbols 
company_to_symbol = {
    "HDFC Bank": "HDFCBANK",
    "ICICI Bank": "ICICIBANK",
}

# Sector mapping for each company
company_to_sector = {
    "HDFC Bank": "Banking",
    "ICICI Bank": "Banking",
}

# Simple sector keywords found in headlines
sector_keywords = {
    "banking sector": "Banking",
    "banking": "Banking",
}

# Simple regulator keywords
regulator_keywords = {
    "RBI": "RBI",
    "Reserve Bank": "RBI",
    "Central bank": "RBI",
    "central bank": "RBI",
}
