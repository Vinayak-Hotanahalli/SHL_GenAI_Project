from fastapi import FastAPI
from pydantic import BaseModel
from models.retrieve import get_candidates

app = FastAPI(title="SHL Assessment Recommendation")

class RecRequest(BaseModel):
    query: str
    k: int = 5

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(req: RecRequest):
    results = get_candidates(req.query, req.k)
    return {"query": req.query, "recommendations": results}
