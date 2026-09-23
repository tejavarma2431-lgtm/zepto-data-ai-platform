import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "zepto_policies"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = client.get_collection(COLLECTION_NAME)


query = "How much is the delivery fee for orders below INR 149?"

query_embedding = model.encode([query]).tolist()


results = collection.query(
    query_embeddings=query_embedding,
    n_results=3,
    include=["documents", "metadatas", "distances"]
)


print("\nQUERY:")
print(query)

print("\nTOP RESULTS:")

for i in range(3):
    print("\n-----------------------------")
    print("Result:", i + 1)
    print("Source:", results["metadatas"][0][i]["source"])
    print("Distance:", results["distances"][0][i])
    print("Document:")
    print(results["documents"][0][i])