import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- Global State ---
# We do NOT load the model immediately here anymore.
MODEL = None
CATALOG = {}
CATALOG_EMBEDDINGS = None

def get_model():
    """Lazy loads the model only when needed."""
    global MODEL
    if MODEL is None:
        print("⏳ Loading AI Model for the first time... (might take a few seconds)")
        MODEL = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model loaded successfully!")
    return MODEL

def load_catalog_if_needed():
    """Loads catalog and embeddings if they aren't loaded yet."""
    global CATALOG, CATALOG_EMBEDDINGS
    
    # If already loaded, skip
    if CATALOG:
        return

    base_dir = Path(__file__).resolve().parent.parent
    catalog_path = base_dir / "data" / "catalog.json"
    
    try:
        with open(catalog_path, "r", encoding="utf-8") as f:
            CATALOG = json.load(f)
            print(f"✅ Catalog loaded from {catalog_path}")
    except FileNotFoundError:
        print(f"❌ Error: catalog.json not found at {catalog_path}")
        CATALOG = {"recommendations": []}
        CATALOG_EMBEDDINGS = np.array([])
        return

    # Pre-compute embeddings
    recs = CATALOG.get("recommendations", [])
    if recs:
        # Ensure model is loaded before computing embeddings
        model = get_model()
        descriptions = [f"{item['title']} {' '.join(item.get('tags', []))}" for item in recs]
        CATALOG_EMBEDDINGS = model.encode(descriptions)
        print("✅ Catalog embeddings pre-computed")
    else:
        CATALOG_EMBEDDINGS = np.array([])

def recommend(query: str, k: int = 5):
    """Recommends items using pre-computed embeddings."""
    # Ensure everything is loaded before we try to recommend
    load_catalog_if_needed()
    
    if not CATALOG.get("recommendations") or CATALOG_EMBEDDINGS is None or CATALOG_EMBEDDINGS.size == 0:
        return []

    # 1. Get the model (will load if it's the first time)
    model = get_model()
    
    # 2. Encode the user query
    query_embedding = model.encode([query])

    # 3. Calculate similarity
    sims = cosine_similarity(query_embedding, CATALOG_EMBEDDINGS)[0]

    # 4. Get top k indices
    top_indices = np.argsort(sims)[::-1][:k]

    # 5. Return results
    recs = CATALOG["recommendations"]
    return [recs[i] for i in top_indices]