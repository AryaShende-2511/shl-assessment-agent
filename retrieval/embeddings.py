import json
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def build_text(product):
    """
    Convert one assessment into searchable text.
    """

    text = f"""
    Name: {product.get('name', '')}

    Description:
    {product.get('description', '')}

    Category:
    {", ".join(product.get('keys', []))}

    Job Levels:
    {", ".join(product.get('job_levels', []))}

    Languages:
    {", ".join(product.get('languages', []))}

    Duration:
    {product.get('duration', '')}

    Features:
    {" ".join(product.get('features', []))}

    """

    return text


def load_catalog(path="data/catalog.json"):

    with open(path, encoding="utf8") as f:
        catalog = json.load(f)

    return catalog


def create_embeddings():

    catalog = load_catalog()

    texts = [build_text(p) for p in catalog]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return catalog, embeddings


if __name__ == "__main__":

    catalog, embeddings = create_embeddings()

    print("Products:", len(catalog))
    print("Embedding shape:", embeddings.shape)