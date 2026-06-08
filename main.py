from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pypdf import PdfReader

from database import engine, SessionLocal
from models import Base, Candidate

import os

app = FastAPI()

Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class CandidateCreate(BaseModel):
    name: str
    email: str


@app.get("/")
def home():
    return {"message": "Resume Parser API Running"}


@app.post("/candidate")
def create_candidate(candidate: CandidateCreate):

    db = SessionLocal()

    try:
        new_candidate = Candidate(
            name=candidate.name,
            email=candidate.email
        )

        db.add(new_candidate)
        db.commit()
        db.refresh(new_candidate)

        return {
            "id": new_candidate.id,
            "name": new_candidate.name,
            "email": new_candidate.email
        }

    finally:
        db.close()


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    # Save uploaded file
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Read PDF
    reader = PdfReader(file_path)

    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            extracted_text += text + "\n"

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "text": extracted_text
    }