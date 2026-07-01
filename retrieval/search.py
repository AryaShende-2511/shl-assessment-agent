import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("data/catalog.index")

# Load metadata
with open("data/metadata.pkl", "rb") as f:
    catalog = pickle.load(f)


def search_catalog(query, top_k=10):
    """
    Semantic search over SHL catalog.
    """

    query_vector = model.encode([query])

    distances, indices = index.search(query_vector, top_k)

    results = []

    for i in indices[0]:
        results.append({
        "name": catalog[i]["name"],
        "url": catalog[i]["link"],
        "description": catalog[i]["description"],
        "job_levels": catalog[i].get("job_levels", []),
        "duration": catalog[i].get("duration"),
        "keys": catalog[i].get("keys", [])
    })

    return results


if __name__ == "__main__":

    query = input("Enter query: ")

    results = search_catalog(query)

    print("\nTop Results\n")

    for i, r in enumerate(results, 1):

        print("=" * 60)
        print(i)
        print(r["name"])
        print(r["url"])
        print(r["description"])