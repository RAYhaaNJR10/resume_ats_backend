from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pypdf import PdfReader
import os

from database import engine, SessionLocal
from models import Base, Candidate
from resume_parser import parse_resume

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # easier for Railway deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class CandidateCreate(BaseModel):
    name: str
    email: str


@app.get("/")
def home():
    return {
        "message": "Resume Parser API Running"
    }


@app.get("/candidates")
def get_candidates():

    db = SessionLocal()

    try:

        candidates = db.query(Candidate).all()

        result = []

        for c in candidates:
            result.append({
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "skills": c.skills
            })

        return result

    finally:
        db.close()


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

    if not file.filename.lower().endswith(".pdf"):
        return JSONResponse(
            status_code=400,
            content={
                "error": "Only PDF files are allowed"
            }
        )

    db = SessionLocal()

    try:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        reader = PdfReader(file_path)

        extracted_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

        parsed_data = parse_resume(
            extracted_text
        )

        candidate = Candidate(
            name=parsed_data.get("name"),
            email=parsed_data.get("email"),
            phone=parsed_data.get("phone"),
            skills=", ".join(
                parsed_data.get("skills", [])
            )
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        return {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "skills": parsed_data.get(
                "skills", []
            )
        }

    finally:
        db.close()