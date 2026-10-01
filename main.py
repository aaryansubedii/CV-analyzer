from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os
import io

load_dotenv()

app = FastAPI()

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


@app.post("/analyze")
async def analyze_cv(
    job_description: str = Form(...),
    cv_file: UploadFile = File(...)
):
    file_bytes = await cv_file.read()
    cv_text = extract_text_from_pdf(file_bytes)


    prompt = f"""You are an expert recruiter and career advisor. Compare the following CV against the job description.

JOB DESCRIPTION:
{job_description}

CV:
{cv_text}

Provide your analysis in this exact format:

MATCH SCORE: [a number from 0-100]

MATCHING SKILLS:
- [list skills/keywords from the CV that match the job description]

MISSING SKILLS:
- [list important skills/keywords in the job description that are NOT in the CV]

SUGGESTIONS:
- [2-4 specific, actionable suggestions to improve the CV for this role]
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    analysis = response.choices[0].message.content

    return {"analysis": analysis}


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")