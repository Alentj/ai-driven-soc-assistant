from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Example cybersecurity text
text = "An attacker executed an encoded PowerShell command."

# Convert text into an embedding vector
embedding = model.encode(text)

print("Original text:")
print(text)

print("\nEmbedding vector:")
print(embedding)

print("\nVector dimensions:")
print(len(embedding))