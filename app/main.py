from fastapi import FastAPI
from pydantic import BaseModel
from app.recommender import load_catalog, recommend_assessment

# ✅ THIS IS WHAT Uvicorn NEEDS
app = FastAPI()

# Load catalog once at startup
catalog = load_catalog()

# Define input model
class UserInput(BaseModel):
    query: str

# Define API route
@app.post("/recommend")
def recommend(input: UserInput):
    result = recommend_assessment(input.query, catalog)
    return {"recommended_assessment": result}

