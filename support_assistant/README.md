# Zepto Support Assistant

A small Retrieval-Augmented Generation (RAG) support assistant for answering Zepto policy questions.

The application uses:

- Sentence Transformers for local embeddings
- ChromaDB for vector storage and retrieval
- LangGraph for query routing and orchestration
- Pydantic for structured output validation
- FastAPI for the REST API
- Uvicorn for local serving
- A deterministic `MOCK_LLM` mode as the default baseline
- An optional real LLM path when `MOCK_LLM=0`

## Project Structure

```text
support_assistant/
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
├── ingest.py
├── main.py
├── test_retrieval.py
├── requirements.txt
├── Dockerfile
└── README.md