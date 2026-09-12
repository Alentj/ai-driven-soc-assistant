from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient


QDRANT_PATH = "ai-rag/data/qdrant_db"
COLLECTION_NAME = "mitre_attack"


def main():

    # Load embedding model
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Connect to Qdrant
    client = QdrantClient(path=QDRANT_PATH)

    # User's cybersecurity query
    query = "An attacker executed an encoded PowerShell command"

    print("\nQuery:")
    print(query)

    # Convert query into embedding
    query_embedding = model.encode(query).tolist()

    # Search Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=5
    )

    print("\nTop MITRE ATT&CK results:")

    for i, result in enumerate(results.points, start=1):

        print(f"\n{i}. Score: {result.score:.4f}")
        print(f"ID: {result.payload['id']}")
        print(f"Name: {result.payload['name']}")
        print(f"URL: {result.payload['url']}")

    client.close()


if __name__ == "__main__":
    main()