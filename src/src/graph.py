"""
LangGraph multi-agent workflow for News Intelligence System.
"""

from langgraph.graph import StateGraph, END
from typing import Dict, Any
import pandas as pd

from .ingestion import load_news_dataset
from .deduplication import add_story_ids
from .entities import add_entities_to_df
from .impact_analysis import add_impacts_to_df
from .query_engine import search_news


# 🔹 GLOBAL MEMORY — store processed news
NEWS_MEMORY: pd.DataFrame = None


# --------------------
# 1️⃣ AGENT FUNCTIONS
# --------------------

def ingestion_agent(state: Dict[str, Any]):
    global NEWS_MEMORY
    df = load_news_dataset()
    state["df"] = df
    return state


def dedup_agent(state: Dict[str, Any]):
    df = add_story_ids(state["df"])
    state["df"] = df
    return state


def entity_agent(state: Dict[str, Any]):
    df = add_entities_to_df(state["df"])
    state["df"] = df
    return state


def impact_agent(state: Dict[str, Any]):
    df = add_impacts_to_df(state["df"])
    state["df"] = df
    return state


def storage_agent(state: Dict[str, Any]):
    global NEWS_MEMORY
    NEWS_MEMORY = state["df"].copy()
    return state


def query_agent(state: Dict[str, Any]):
    global NEWS_MEMORY
    query = state.get("query", "")
    if not query:
        state["results"] = pd.DataFrame()
    else:
        state["results"] = search_news(query, NEWS_MEMORY)
    return state


# --------------------
# 2️⃣ GRAPH WORKFLOW
# --------------------

def build_graph():
    graph = StateGraph(dict)

    # Add nodes
    graph.add_node("ingestion", ingestion_agent)
    graph.add_node("dedup", dedup_agent)
    graph.add_node("entities", entity_agent)
    graph.add_node("impact", impact_agent)
    graph.add_node("store", storage_agent)
    graph.add_node("query", query_agent)

    # Edges (pipeline)
    graph.set_entry_point("ingestion")
    graph.add_edge("ingestion", "dedup")
    graph.add_edge("dedup", "entities")
    graph.add_edge("entities", "impact")
    graph.add_edge("impact", "store")

    # After storing, diverge based on request
    graph.add_edge("store", "query")
    graph.add_edge("query", END)

    return graph.compile()


# --------------------
# 3️⃣ CONVENIENCE RUNNERS
# --------------------

def process_all_news():
    """Run ETL pipeline (no query)"""
    graph = build_graph()
    final_state = graph.invoke({"query": None})
    return final_state["df"]


def run_query(query: str):
    """Run query agent after ETL"""
    graph = build_graph()
    final_state = graph.invoke({"query": query})
    return final_state.get("results", pd.DataFrame())
