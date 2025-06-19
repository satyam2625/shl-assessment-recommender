from fastapi import FastAPI
from pydantic import BaseModel
from app.recommender import recommend_assessment

app = FastAPI()

class UserInput(BaseModel):
    query: str

@app.post("/recommend")
def recommend(input: UserInput):
    rec = recommend_assessment(input.query)
    return {"recommendations": [rec]}
