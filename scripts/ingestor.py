import json
from pathlib import Path

from app.db import collection


def insert_extracted_data(base_path):
    extracted_path = Path(base_path) / "data" / "extracted"
    
    for folder in extracted_path.iterdir():
        if folder.is_dir():
            metadata_path = folder / "metadata.json"
            metadata = {}
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)

            data_path = folder / "data.txt"
            
            with open(data_path, 'r') as f:
                content = f.read()
            
            ids = [f"{folder.name}"]
            documents = [content]
            metadatas = [
                {
                    "name": metadata["name"],
                    "url": metadata["url"],
                }
            ]

            collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas, # type: ignore
            )

    print("Inserted documents count:", collection.count())

if __name__ == "__main__":
    base_directory = "./"
    insert_extracted_data(base_directory)