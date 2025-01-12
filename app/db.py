from pathlib import Path

import chromadb
from chromadb.config import Settings

from app.settings import COLLECTION_NAME, DATA_BASE_PATH, DB_NAME

chroma_client = chromadb.PersistentClient(
    path=str(Path(DATA_BASE_PATH) / Path(DB_NAME)),
    settings=Settings(anonymized_telemetry=False)
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)

def query(question, n_results):
    query_result = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    return query_result
