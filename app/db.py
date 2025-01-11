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

def query(question, n_results, threshold):
    query_result = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    count = len(query_result["ids"][0])

    formatted_result = []

    for match_index in range(count):
        id = query_result["ids"][0][match_index]
        document = query_result["documents"][0][match_index] # type: ignore
        metadata = query_result["metadatas"][0][match_index] # type: ignore
        distance = query_result["distances"][0][match_index] # type: ignore

        if distance < threshold:
            formatted_result.append({
                "id": id,
                "content": document,
                "metadata": metadata,
            })

    return formatted_result
