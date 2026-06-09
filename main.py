from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    JSONResponse,
    FileResponse
)
from pydantic import BaseModel
from pypdf import PdfReader

from database import engine, SessionLocal
from models import Base, Candidate

from resume_parser import (
    parse_resume,
    extract_jd_skills
)

import csv
import os

app = FastAPI()

# ==================================
# CORS
# ==================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================
# DB INIT
# ==================================

Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# ==================================
# REQUEST MODELS
# ==================================

class CandidateCreate(BaseModel):
    name: str
    email: str


class JobDescription(BaseModel):
    job_description: str


# ==================================
# FRONTEND ROUTES
# ==================================

@app.get("/")
def home_page():
    return FileResponse("index.html")


@app.get("/script.js")
def js_file():
    return FileResponse("script.js")


@app.get("/style.css")
def css_file():
    return FileResponse("style.css")


# ==================================
# HEALTH CHECK
# ==================================

@app.get("/api")
def api_home():

    return {
        "message":
        "Resume ATS Running"
    }


# ==================================
# GET ALL CANDIDATES
# ==================================

@app.get("/candidates")
def get_candidates():

    db = SessionLocal()

    try:

        candidates = (
            db.query(Candidate)
            .order_by(
                Candidate.id.desc()
            )
            .all()
        )

        results = []

        for c in candidates:

            results.append({

                "id": c.id,

                "filename":
                c.filename,

                "name":
                c.name,

                "email":
                c.email,

                "phone":
                c.phone,

                "skills":
                c.skills,

                "education":
                c.education,

                "experience":
                c.experience,

                "linkedin":
                c.linkedin,

                "github":
                c.github,

                "projects":
                c.projects,

                "certifications":
                c.certifications,

                "ats_score":
                c.ats_score
            })

        return results

    finally:
        db.close()


# ==================================
# SEARCH BY SKILL
# ==================================

@app.get("/search")
def search_candidates(skill: str):

    db = SessionLocal()

    try:

        candidates = (
            db.query(Candidate)
            .filter(
                Candidate.skills.ilike(
                    f"%{skill}%"
                )
            )
            .all()
        )

        results = []

        for c in candidates:

            results.append({

                "id": c.id,

                "name": c.name,

                "email": c.email,

                "phone": c.phone,

                "skills": c.skills,

                "ats_score":
                c.ats_score
            })

        return results

    finally:
        db.close()


# ==================================
# SINGLE RESUME UPLOAD
# ==================================

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(
        ".pdf"
    ):
        return JSONResponse(
            status_code=400,
            content={
                "error":
                "Only PDF files allowed"
            }
        )

    db = SessionLocal()

    try:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(
                await file.read()
            )

        reader = PdfReader(file_path)

        extracted_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:

                extracted_text += (
                    text + "\n"
                )

        parsed_data = parse_resume(
            extracted_text
        )

        existing = (
            db.query(Candidate)
            .filter(
                Candidate.email ==
                parsed_data.get(
                    "email"
                )
            )
            .first()
        )

        if existing:

            return JSONResponse(
                status_code=400,
                content={
                    "error":
                    "Candidate already exists"
                }
            )

        candidate = Candidate(

            filename=file.filename,

            name=parsed_data.get(
                "name"
            ),

            email=parsed_data.get(
                "email"
            ),

            phone=parsed_data.get(
                "phone"
            ),

            skills=", ".join(
                parsed_data.get(
                    "skills",
                    []
                )
            ),

            education=parsed_data.get(
                "education"
            ),

            experience=parsed_data.get(
                "experience"
            ),

            linkedin=parsed_data.get(
                "linkedin"
            ),

            github=parsed_data.get(
                "github"
            ),

            projects=", ".join(
                parsed_data.get(
                    "projects",
                    []
                )
            ),

            certifications=", ".join(
                parsed_data.get(
                    "certifications",
                    []
                )
            )
        )

        db.add(candidate)

        db.commit()

        db.refresh(candidate)

        return {

            "id":
            candidate.id,

            "name":
            candidate.name,

            "email":
            candidate.email,

            "phone":
            candidate.phone,

            "skills":
            parsed_data.get(
                "skills",
                []
            )
        }

    finally:
        db.close()


# ==================================
# BULK UPLOAD
# ==================================

@app.post("/upload-bulk")
async def upload_bulk(
    files: list[UploadFile] = File(...)
):

    db = SessionLocal()

    results = []

    try:

        for file in files:

            try:

                if not file.filename.lower().endswith(
                    ".pdf"
                ):

                    results.append({
                        "file":
                        file.filename,

                        "status":
                        "invalid_file"
                    })

                    continue

                file_path = os.path.join(
                    UPLOAD_FOLDER,
                    file.filename
                )

                with open(
                    file_path,
                    "wb"
                ) as buffer:

                    buffer.write(
                        await file.read()
                    )

                reader = PdfReader(
                    file_path
                )

                extracted_text = ""

                for page in reader.pages:

                    page_text = (
                        page.extract_text()
                    )

                    if page_text:

                        extracted_text += (
                            page_text +
                            "\n"
                        )

                parsed_data = parse_resume(
                    extracted_text
                )

                existing = (
                    db.query(Candidate)
                    .filter(
                        Candidate.email ==
                        parsed_data.get(
                            "email"
                        )
                    )
                    .first()
                )

                if existing:

                    results.append({

                        "file":
                        file.filename,

                        "status":
                        "duplicate"
                    })

                    continue

                candidate = Candidate(

                    filename=file.filename,

                    name=parsed_data.get(
                        "name"
                    ),

                    email=parsed_data.get(
                        "email"
                    ),

                    phone=parsed_data.get(
                        "phone"
                    ),

                    skills=", ".join(
                        parsed_data.get(
                            "skills",
                            []
                        )
                    ),

                    education=parsed_data.get(
                        "education"
                    ),

                    experience=parsed_data.get(
                        "experience"
                    ),

                    linkedin=parsed_data.get(
                        "linkedin"
                    ),

                    github=parsed_data.get(
                        "github"
                    ),

                    projects=", ".join(
                        parsed_data.get(
                            "projects",
                            []
                        )
                    ),

                    certifications=", ".join(
                        parsed_data.get(
                            "certifications",
                            []
                        )
                    )
                )

                db.add(candidate)

                results.append({

                    "file":
                    file.filename,

                    "status":
                    "success"
                })

            except Exception as e:

                results.append({

                    "file":
                    file.filename,

                    "status":
                    "failed",

                    "error":
                    str(e)
                })

        db.commit()

        return results

    finally:
        db.close()


# ==================================
# ATS RANKING
# ==================================

@app.post("/rank-candidates")
def rank_candidates(
    jd: JobDescription
):

    db = SessionLocal()

    try:

        jd_result = (
            extract_jd_skills(
                jd.job_description
            )
        )

        jd_skills = set(

            skill.lower()

            for skill in
            jd_result.get(
                "skills",
                []
            )
        )

        rankings = []

        candidates = (
            db.query(Candidate)
            .all()
        )

        for candidate in candidates:

            candidate_skills = set(

                skill.strip().lower()

                for skill in
                candidate.skills.split(",")
                if skill.strip()
            )

            matched = (
                candidate_skills
                &
                jd_skills
            )

            score = 0

            if len(jd_skills) > 0:

                score = round(
                    (
                        len(matched)
                        /
                        len(jd_skills)
                    )
                    * 100,
                    2
                )

            candidate.ats_score = score

            rankings.append({

                "candidate_id":
                candidate.id,

                "name":
                candidate.name,

                "email":
                candidate.email,

                "score":
                score,

                "matched_skills":
                list(matched)
            })

        db.commit()

        rankings.sort(
            key=lambda x:
            x["score"],
            reverse=True
        )

        return {

            "jd_skills":
            list(jd_skills),

            "rankings":
            rankings
        }

    finally:
        db.close()


# ==================================
# CSV EXPORT
# ==================================

@app.get("/export-csv")
def export_csv():

    db = SessionLocal()

    try:

        candidates = (
            db.query(Candidate)
            .all()
        )

        csv_filename = (
            "candidates.csv"
        )

        with open(
            csv_filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow([
                "Name",
                "Email",
                "Phone",
                "Skills",
                "ATS Score"
            ])

            for c in candidates:

                writer.writerow([

                    c.name,

                    c.email,

                    c.phone,

                    c.skills,

                    c.ats_score
                ])

        return FileResponse(
            csv_filename,
            filename=
            "candidates.csv"
        )

    finally:
        db.close()