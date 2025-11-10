from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.recommender import recommend
from pydantic import BaseModel
from typing import List

# --- CRITICAL: This is the 'app' object Uvicorn is looking for ---
app = FastAPI(
    title="SHL Assessment Recommender API",
    description="Recommends SHL assessments based on job roles or skills."
)
# ----------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendationItem(BaseModel):
    title: str
    tags: List[str]

class RecommendationResponse(BaseModel):
    query: str
    results: List[RecommendationItem]

@app.get("/")
def root():
    return {"message": "SHL Assessment Recommender API is running", "status": "ok"}

@app.get("/recommend", response_model=RecommendationResponse)
def get_recommendations(query: str, k: int = 5):
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    try:
        results = recommend(query, k=k)
    except Exception as e:
         print(f"Error during recommendation: {e}")
         # Return an empty list on error instead of crashing, for better UX
         return {"query": query, "results": []}

    return {"query": query, "results": results}