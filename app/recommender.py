import json, os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def load_catalog():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'catalog.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def recommend_assessment(query: str):
    catalog = load_catalog()
    titles = [item["title"] for item in catalog]
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(titles + [query])
    sims = cosine_similarity([embeddings[-1]], embeddings[:-1])[0]
    best = int(np.argmax(sims))
    return catalog[best]


