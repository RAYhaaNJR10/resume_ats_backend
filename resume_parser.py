from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def parse_resume(text):

    prompt = f"""
You are an ATS resume parser.

Extract candidate information and return ONLY valid JSON.

Rules:

1. Extract concise professional skill names only.
2. Do NOT return full sentences.
3. Do NOT include explanations.
4. Each skill should be 1-3 words maximum.
5. Remove duplicates.
6. Normalize skill names.
7. Use Title Case.

Examples:

GOOD:
[
    "Python",
    "FastAPI",
    "MySQL",
    "Communication",
    "Teamwork",
    "Problem Solving"
]

BAD:
[
    "Strong ability to work as part of a team developed through participating in soccer since the age of eight",
    "Highly developed communication skills shown by receiving positive feedback from supervisors"
]

Return JSON in this exact format:

{{
    "name": "",
    "email": "",
    "phone": "",
    "skills": []
}}

Resume:

{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    return json.loads(content)