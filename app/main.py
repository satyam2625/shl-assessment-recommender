from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.recommender import recommend, load_catalog
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="SHL Assessment Recommender API",
    description="Recommends SHL assessments based on job roles or skills."
)

# Enable CORS (Cross-Origin Resource Sharing)
# This allows your Streamlit frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, list your specific Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the catalog once at startup to save time
CATALOG = load_catalog()

# Define the response models for documentation
class RecommendationItem(BaseModel):
    title: str
    tags: List[str]

class RecommendationResponse(BaseModel):
    query: str
    results: List[RecommendationItem]

@app.get("/")
def root():
    """Root endpoint to check if the API is running."""
    return {"message": "SHL Assessment Recommender API is running"}

@app.get("/recommend", response_model=RecommendationResponse)
def get_recommendations(query: str, k: int = 5):
    """
    Get assessment recommendations based on a query string.
    
    - **query**: The job role or skill (e.g., "python backend", "data analysis").
    - **k**: The number of recommendations to return (default is 5).
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    if not CATALOG.get('recommendations'):
         raise HTTPException(status_code=500, detail="Catalog is empty or not loaded")

    # Call the fixed recommend function
    results = recommend(query, k=k, catalog=CATALOG)
    
    return {"query": query, "results": results}