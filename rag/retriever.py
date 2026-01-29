import chromadb
import time
from rag.embedder import get_embeddings
from rag.document_loader import load_pdf
client = chromadb.PersistentClient(path="./chroma_db")

def index_documents(documents: list[dict]):
    """Indexes documents into a ChromaDB collection."""
    collection = client.get_or_create_collection("rag")
    print(collection)
    for doc in documents:
        collection.add(
            embeddings=get_embeddings(doc["text"]),
            documents=doc["text"],
            metadatas=[{"source": doc["name"]}]*len(doc["text"]),
            ids=[str(indice)+" - " + doc["name"] for indice in range(len(doc["text"]))],
        )


def search(query: str, n_results: int = 3) :# -> list[str]
    """Searches for similar documents to the query."""
    collection = client.get_collection("rag")
    results = collection.query(
        query_embeddings=get_embeddings([query]),
        n_results=n_results,
        include=["metadatas", "documents"],
    )
    return results["documents"][0]

if __name__ == "__main__":
    docs = load_pdf(["pdfs/rubiks_cube.pdf"])
    index_documents(docs)
    
    results = search("Comment résoudre le cube ?")
    print(f"Nombre de chunks trouvés : {len(results)}")
    for i, chunk in enumerate(results):
        print(f"\n--- Chunk {i+1} ---")
        print(chunk[:300] + "...")
