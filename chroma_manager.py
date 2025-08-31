# chroma_manager.py
from chromadb import PersistentClient

# Initialize ChromaDB persistent client
client = PersistentClient(path="./chroma_data")

def save_version(book, chapter, content, user_id):
    """
    Save a final version of a chapter into ChromaDB.
    Each saved version is tied to a specific user_id.
    """
    collection = client.get_or_create_collection("books")
    doc_id = f"{user_id}_{book}_{chapter}"

    # Add or update
    try:
        collection.add(
            documents=[content],
            metadatas=[{"book": book, "chapter": chapter, "user_id": user_id}],
            ids=[doc_id]
        )
    except Exception:
        # If doc_id already exists, update instead
        collection.update(
            documents=[content],
            metadatas=[{"book": book, "chapter": chapter, "user_id": user_id}],
            ids=[doc_id]
        )

def list_versions(user_id):
    """
    List all saved versions of books & chapters for a given user_id.
    Returns a list of dicts with {book, chapter, content}.
    """
    collection = client.get_or_create_collection("books")
    results = collection.get(where={"user_id": user_id})

    return [
        {
            "book": m["book"],
            "chapter": m["chapter"],
            "content": d
        }
        for d, m in zip(results["documents"], results["metadatas"])
    ]
