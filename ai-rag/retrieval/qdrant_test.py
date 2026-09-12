from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# 1. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Create a local Qdrant database
client = QdrantClient(path="ai-rag/data/qdrant_db")

collection_name = "cybersecurity_knowledge"

# 3. Create collection
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

# 4. Example cybersecurity knowledge
documents = [
    "PowerShell is commonly used by attackers to execute commands and scripts.",
    "Phishing attacks use fraudulent messages to trick users into revealing information.",
    "Ransomware encrypts files and demands payment from the victim.",
    "Attackers may use credential dumping to obtain usernames and passwords.",
]

# 5. Convert documents into embeddings
embeddings = model.encode(documents)

# 6. Store documents in Qdrant
points = []

for i, (document, embedding) in enumerate(zip(documents, embeddings)):
    points.append(
        PointStruct(
            id=i,
            vector=embedding.tolist(),
            payload={"text": document}
        )
    )

client.upsert(
    collection_name=collection_name,
    points=points
)

# 7. Search using a new query
query = "attacker used PowerShell to run commands"

query_embedding = model.encode(query).tolist()

results = client.query_points(
    collection_name=collection_name,
    query=query_embedding,
    limit=2
)

# 8. Display results
print("\nQuery:")
print(query)

print("\nMost relevant results:")

for result in results.points:
    print(f"\nScore: {result.score:.4f}")
    print(f"Text: {result.payload['text']}")
client.close()    