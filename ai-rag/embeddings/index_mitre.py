import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance


INPUT_FILE = Path(
    "ai-rag/data/processed/mitre_techniques.json"
)

QDRANT_PATH = "ai-rag/data/qdrant_db"

COLLECTION_NAME = "mitre_attack"


def main():

    # Load MITRE techniques
    print("Loading MITRE techniques...")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        techniques = json.load(file)

    print(f"Techniques loaded: {len(techniques)}")

    # Load embedding model
    print("\nLoading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create local Qdrant database
    client = QdrantClient(path=QDRANT_PATH)

    # Create collection if it doesn't exist
    if not client.collection_exists(COLLECTION_NAME):

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print("Qdrant collection created.")

    else:
        print("Qdrant collection already exists.")

    # Prepare text for embedding
    texts = []

    for technique in techniques:

        text = (
            f"MITRE ATT&CK Technique ID: {technique['id']}\n"
            f"Technique Name: {technique['name']}\n"
            f"Description: {technique['description']}"
        )

        texts.append(text)

    # Generate embeddings
    print("\nGenerating embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    # Create Qdrant points
    points = []

    for index, (technique, embedding) in enumerate(
        zip(techniques, embeddings)
    ):

        points.append(
            PointStruct(
                id=index,
                vector=embedding.tolist(),
                payload={
                    "id": technique["id"],
                    "name": technique["name"],
                    "description": technique["description"],
                    "url": technique["url"]
                }
            )
        )

    # Insert into Qdrant
    print("\nInserting techniques into Qdrant...")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Inserted {len(points)} techniques.")

    client.close()

    print("\nMITRE ATT&CK RAG knowledge base is ready!")


if __name__ == "__main__":
    main()