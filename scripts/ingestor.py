import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.db import collection


# Split the texts into smaller chunks to ensure that the documents are not too large and have predictable sizes.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)

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
            
            documents = text_splitter.create_documents([content])

            metadatas = [
                {
                    "name": metadata["name"],
                    "url": metadata["url"],
                }
            ]

            for index, document in enumerate(documents):
                collection.upsert(
                    ids=[f"{folder.name}-{index}"],
                    documents=[document.page_content],
                    metadatas=metadatas, # type: ignore
                )

    print("Inserted documents count:", collection.count())

if __name__ == "__main__":
    base_directory = "./"
    insert_extracted_data(base_directory)