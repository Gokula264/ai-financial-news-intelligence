# 🧠 AI Financial News Intelligence System

This project is a **LangGraph-based multi-agent system** that transforms raw financial news into actionable market intelligence.  
It identifies which banks and sectors are affected by policy moves, market updates, and corporate announcements — helping investors gain insights quickly.

---

## 🚀 Key Features

- 🔹 News ingestion – Loads financial headlines and creates embeddings  
- 🔹 Deduplication – Groups similar articles to avoid redundancy  
- 🔹 Entity extraction – Detects companies, sectors, regulators from text  
- 🔹 Impact analysis – Maps news to impacted stocks with confidence scores  
- 🔹 Query engine – Semantic search powered by embeddings  
- 🔹 LangGraph orchestration – Six specialized agents working together  

---

## 📂 Project Structure

```
ai-financial-news-intelligence/
│
├── data/
│   └── mock_news.csv              → 30+ financial news samples
│
├── src/
│   ├── config.py                  → Constants & mappings
│   ├── ingestion.py               → Load dataset + embeddings
│   ├── deduplication.py           → Cluster similar headlines
│   ├── entities.py                → Extract companies/sectors/regulators
│   ├── impact_analysis.py         → Stock impact scoring
│   ├── query_engine.py            → Semantic similarity search
│   └── graph.py                   → LangGraph pipeline (6 agents)
│
└── financial_news_system.ipynb    → End-to-end demo notebook
```

---

## ⚙️ Installation

```bash
git clone https://github.com/Gokula264/ai-financial-news-intelligence.git
cd ai-financial-news-intelligence

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## ▶️ How to Run the System

Inside Python or Jupyter Notebook:

```python
from src.graph import process_all_news, run_query

# Run full multi-agent pipeline
df = process_all_news()
df.head()

# Ask any financial question
run_query("RBI policy rate hike impact")
```

---

### 📌 Output Example

```
Query → “RBI policy change”
→ HDFCBANK  (Confidence 0.6)
→ ICICIBANK (Confidence 0.6)
```

---

## 🧠 Multi-Agent Architecture (LangGraph)

```
News → Ingestion → Deduplication → Entity Extraction
     → Impact Analysis → Final Intelligence Table → Query Engine
```

Each agent handles one stage, and passes results forward automatically.

---

## 📊 What This System Solves

- Understand **which news impacts which stocks**
- Identify and remove **duplicate** headlines
- Get results from **natural language queries**
- Helps traders and analysts react quickly

---

## 🧪 Testing

```bash
pytest -q
```

Covers:
- Entity extraction verification  
- Query relevance scoring  

---

## 🏗 Tech Stack

- LangGraph — Multi-agent orchestration  
- Sentence Transformers — Text embeddings  
- spaCy — Named Entity Recognition  
- Pandas / NumPy / sklearn — Data processing  
- Python 3.10+  

---

## 👨‍💻 Author

**Gokula Chintalapudi (Gokula264)**  
Tradl Hackathon — December 2025  

---

⭐ If you like this project — please star the repository!
