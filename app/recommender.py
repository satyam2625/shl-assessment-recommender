import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- Global State ---
# Load model once
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
CATALOG = {}
CATALOG_EMBEDDINGS = None

def load_catalog_and_embeddings():
    """Loads catalog and pre-computes embeddings on startup."""
    global CATALOG, CATALOG_EMBEDDINGS
    
    # Robust path to data/catalog.json
    base_dir = Path(__file__).resolve().parent.parent
    catalog_path = base_dir / "data" / "catalog.json"
    
    try:
        with open(catalog_path, "r", encoding="utf-8") as f:
            CATALOG = json.load(f)
            print(f"✅ Catalog loaded from {catalog_path}")
    except FileNotFoundError:
        print(f"❌ Error: catalog.json not found at {catalog_path}")
        CATALOG = {"recommendations": []}

    # Pre-compute embeddings if catalog exists
    recs = CATALOG.get("recommendations", [])
    if recs:
        descriptions = [f"{item['title']} {' '.join(item.get('tags', []))}" for item in recs]
        CATALOG_EMBEDDINGS = MODEL.encode(descriptions)
        print("✅ Catalog embeddings pre-computed")
    else:
        CATALOG_EMBEDDINGS = np.array([])

# Initialize on module import
load_catalog_and_embeddings()

def recommend(query: str, k: int = 5):
    """Recommends items using pre-computed embeddings."""
    if not CATALOG.get("recommendations") or CATALOG_EMBEDDINGS.size == 0:
        return []

    # 1. Encode the user query
    query_embedding = MODEL.encode([query])

    # 2. Calculate similarity using pre-computed embeddings
    sims = cosine_similarity(query_embedding, CATALOG_EMBEDDINGS)[0]

    # 3. Get top k indices
    top_indices = np.argsort(sims)[::-1][:k]

    # 4. Return results
    recs = CATALOG["recommendations"]
    return [recs[i] for i in top_indices]