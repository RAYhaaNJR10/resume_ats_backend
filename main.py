from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Candidate(BaseModel):
    name: str
    email: str

@app.get("/")
def home():
    return {"message": "Resume Parser API Running"}

@app.post("/candidate")
def create_candidate(candidate: Candidate):
    return {
        "name": candidate.name,
        "email": candidate.email
    }