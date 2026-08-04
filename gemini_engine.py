import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_resume_with_gemini(resume_text, job_description):

    prompt = f"""
    You are an experienced ATS (Applicant Tracking System) and Senior Technical Recruiter.

    Analyze the following resume against the given job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Instructions:
    - Compare the resume against the job description.
    - Infer skills semantically. Do NOT rely only on exact keyword matches.
    - Keep the analysis concise.
    - Do not invent technologies not mentioned in either text.

    Return ONLY valid JSON.

    Schema:

    {{
    "matching_skills": [
        "..."
    ],
    "missing_skills": [
        "..."
    ],
    "suggestions": [
        "..."
    ],
    "recruiter_verdict": "..."
    }}

    Rules:
    - matching_skills: maximum 10 items
    - missing_skills: maximum 10 items
    - suggestions: maximum 5 items
    - recruiter_verdict:
        One short paragraph (2-4 sentences)
    - No markdown.
    - No code fences.
    - No explanations.
    - Output ONLY JSON.
    """

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt,
    )

    response_text = response.text.strip()

    response_text = (
        response_text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        analysis = json.loads(response_text)
        return analysis

    except json.JSONDecodeError:
        return {
            "matching_skills": [],
            "missing_skills": [],
            "suggestions": [
                "AI could not generate a valid analysis. Please try again."
            ],
            "recruiter_verdict": "Analysis unavailable due to an AI response formatting error."
        }