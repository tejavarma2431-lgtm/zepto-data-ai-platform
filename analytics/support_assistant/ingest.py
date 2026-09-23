from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DOCS_DIR = Path("docs")
CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "zepto_policies"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


documents = []
ids = []
metadatas = []


for file_path in sorted(DOCS_DIR.glob("doc_*.txt")):
    text = file_path.read_text(encoding="utf-8").strip()

    documents.append(text)
    ids.append(file_path.stem)
    metadatas.append({
        "source": file_path.name
    })


embeddings = model.encode(documents).tolist()


collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)


print(f"Documents loaded: {len(documents)}")
print(f"Collection: {COLLECTION_NAME}")
print(f"Stored items: {collection.count()}")