from chromadb.config import Settings
import chromadb

# Initialize Chroma client with DuckDB (safe for Streamlit Cloud)
chroma_client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./chromadb_store"
    )
)

# Create or get a collection
collection = chroma_client.get_or_create_collection(name="book_versions")

# Save a version for a user
def save_version(book, chapter, content, user_id):
    uid = f"{user_id}:{book}:{chapter}"
    collection.add(
        documents=[content],
        ids=[uid],
        metadatas=[{
            "user_id": user_id,
            "book": book,
            "chapter": chapter
        }]
    )

# List all saved versions for a user
def list_versions(user_id):
    results = collection.get(where={"user_id": user_id})
    versions = []
    for doc, meta in zip(results['documents'], results['metadatas']):
        versions.append({
            "book": meta['book'],
            "chapter": meta['chapter'],
            "content": doc
        })
    return versions
