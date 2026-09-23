# Zepto Data & AI Platform

An end-to-end AI/ML engineering capstone project containing three connected capabilities:

1. **Data Pipeline** — scrape, clean, enrich, store, and query catalog data.
2. **Analytics & ML** — perform EDA, preprocessing, classification, imbalance handling, tuning, and regression.
3. **GenAI Support Assistant** — build a grounded RAG-based support service using LangGraph, ChromaDB, Sentence Transformers, and FastAPI.

All three modules are maintained in a single public GitHub repository.

---

## Project Structure

```text
zepto-data-ai-platform/
│
├── data_pipeline/
│   ├── scraper.py
│   ├── database.py
│   ├── queries.py
│   ├── queries.sql
│   ├── books_cleaned.csv
│   ├── books.db
│   ├── query_outputs/
│   └── README.md
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── titanic.csv
│   ├── titanic_cleaned.csv
│   ├── titanic_final_pipeline.joblib
│   └── README.md
│
├── support_assistant/
│   ├── docs/
│   │   ├── doc_01.txt
│   │   ├── doc_02.txt
│   │   ├── doc_03.txt
│   │   ├── doc_04.txt
│   │   ├── doc_05.txt
│   │   ├── doc_06.txt
│   │   ├── doc_07.txt
│   │   └── doc_08.txt
│   ├── ingest.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .gitignore
│   └── README.md
│
└── README.md