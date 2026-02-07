# Fix for sqlite version issue on Streamlit Cloud
try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

from chromadb import PersistentClient

# Initialize ChromaDB persistent client
client = PersistentClient(path="./chromadb_store")

# Embedding dimension used by the default embedding function
EMBEDDING_DIM = 384


def _get_dummy_embeddings(n: int) -> list:
    """Return dummy embeddings for n documents.
    
    Since we use ChromaDB as a simple document store (not for similarity search),
    we don't need actual embeddings. This avoids the need to download ONNX models
    while still satisfying ChromaDB's embedding requirement for the collection.
    """
    return [[0.0] * EMBEDDING_DIM for _ in range(n)]


def save_version(book, chapter, content, user_id):
    """
    Save a final version of a chapter into ChromaDB.
    Each saved version is tied to a specific user_id.
    """
    collection = client.get_or_create_collection("books")
    doc_id = f"{user_id}_{book}_{chapter}"

    # Use upsert with pre-computed embeddings to avoid downloading ONNX models
    collection.upsert(
        documents=[content],
        metadatas=[{"book": book, "chapter": chapter, "user_id": user_id}],
        ids=[doc_id],
        embeddings=_get_dummy_embeddings(1)
    )


def list_versions(user_id):
    """
    List all saved versions of books & chapters for a given user_id.
    Returns a list of dicts with {book, chapter, content}.
    """
    collection = client.get_or_create_collection("books")
    results = collection.get(where={"user_id": user_id})

    if not results["documents"] or not results["metadatas"]:
        return []

    return [
        {
            "book": m["book"],
            "chapter": m["chapter"],
            "content": d
        }
        for d, m in zip(results["documents"], results["metadatas"])
    ]


def delete_version(book, chapter, user_id):
    """
    Delete a specific chapter from the user's collection.
    """
    collection = client.get_or_create_collection("books")
    doc_id = f"{user_id}_{book}_{chapter}"
    collection.delete(ids=[doc_id])
