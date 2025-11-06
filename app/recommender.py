import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the model once when the app starts for efficiency
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_catalog():
    """Loads the assessment catalog from the JSON file."""
    # Use an absolute path to be safe in all environments
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'catalog.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: catalog.json not found.")
        return {"recommendations": []}

def recommend(query: str, k: int = 5, catalog=None):
    """Recommends top k assessments based on a query."""
    if catalog is None:
        catalog = load_catalog()
    
    # Correctly access the list of recommendations
    recommendations_list = catalog.get('recommendations', [])
    
    if not recommendations_list:
        return []

    # Extract titles and tags to create a descriptive text for each item
    descriptions = [
        f"{item['title']} {' '.join(item.get('tags', []))}" 
        for item in recommendations_list
    ]
    
    # Encode all descriptions and the query
    catalog_embeddings = model.encode(descriptions)
    query_embedding = model.encode([query])

    # Calculate similarity
    sims = cosine_similarity(query_embedding, catalog_embeddings)[0]
    
    # Get the indices of the top k most similar items
    # This replaces np.argmax which only gives 1 result
    top_indices = np.argsort(sims)[::-1][:k]
    
    # Return the corresponding full items from the catalog
    return [recommendations_list[i] for i in top_indices]