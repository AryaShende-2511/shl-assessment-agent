import os
import pickle
import faiss

from embeddings import create_embeddings

# Create embeddings
catalog, embeddings = create_embeddings()

# Get vector dimension
dimension = embeddings.shape[1]

# Build FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Create output folder if needed
os.makedirs("data", exist_ok=True)

# Save index
faiss.write_index(index, "data/catalog.index")

# Save metadata
with open("data/metadata.pkl", "wb") as f:
    pickle.dump(catalog, f)

print("✅ FAISS index saved.")
print("Vectors:", index.ntotal)