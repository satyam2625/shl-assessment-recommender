
def recommend(query, catalog, top_k=3):
    from sklearn.metrics.pairwise import cosine_similarity
    from sentence_transformers import SentenceTransformer
    import numpy as np

    model = SentenceTransformer('all-MiniLM-L6-v2')

    query_embedding = model.encode([query])
    catalog_embeddings = model.encode([item['description'] for item in catalog])

    similarities = cosine_similarity(query_embedding, catalog_embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    recommendations = [catalog[i] for i in top_indices]
    return recommendations

import json
import os

def load_catalog():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "catalog.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

