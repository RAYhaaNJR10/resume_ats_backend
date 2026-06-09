from openai import OpenAI
from dotenv import load_dotenv

import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


# ==================================
# RESUME PARSER
# ==================================

def parse_resume(text):

    prompt = f"""
You are an enterprise ATS parser.

Extract information from the resume.

Rules:

1. Return ONLY valid JSON.
2. No markdown.
3. No explanations.
4. Extract concise skills only.
5. Remove duplicate skills.
6. Normalize skill names.
7. Skills must be short.

Return EXACTLY:

{{
    "name": "",
    "email": "",
    "phone": "",
    "skills": [],
    "education": "",
    "experience": "",
    "linkedin": "",
    "github": "",
    "projects": [],
    "certifications": []
}}

Resume:

{text}
"""

    response = (
        client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )
    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        parsed = json.loads(
            content
        )

        return parsed

    except Exception:

        return {

            "name": "",

            "email": "",

            "phone": "",

            "skills": [],

            "education": "",

            "experience": "",

            "linkedin": "",

            "github": "",

            "projects": [],

            "certifications": []
        }


# ==================================
# JOB DESCRIPTION PARSER
# ==================================

def extract_jd_skills(
    job_description
):

    prompt = f"""
You are an ATS system.

Extract only the important skills
from this Job Description.

Rules:

1. Return ONLY JSON.
2. No explanations.
3. No markdown.
4. Remove duplicates.
5. Normalize skills.
6. Keep skills concise.

Return:

{{
    "skills": []
}}

Job Description:

{job_description}
"""

    response = (
        client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )
    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        return json.loads(
            content
        )

    except Exception:

        return {
            "skills": []
        }