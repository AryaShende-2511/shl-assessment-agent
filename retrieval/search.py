import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("data/metadata.pkl", "rb") as f:
    catalog = pickle.load(f)

documents = []

for item in catalog:
    text = (
        item["name"] + " "
        + item.get("description", "") + " "
        + " ".join(item.get("keys", []))
    )
    documents.append(text)

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(documents)


def search_catalog(query, top_k=5):

    query_vec = vectorizer.transform([query])

    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    top_idx = scores.argsort()[::-1][:top_k]

    results = []

    for i in top_idx:
        results.append(catalog[i])

    return results