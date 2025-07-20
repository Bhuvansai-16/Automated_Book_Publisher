import sys
import pysqlite3

sys.modules["sqlite3"] = pysqlite3

from chromadb import PersistentClient
from chromadb.config import Settings

client = PersistentClient(path="./chromadb_store")
collection = client.get_or_create_collection(name="book_versions")

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
