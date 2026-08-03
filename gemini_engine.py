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
    You are an ATS Resume Analyzer.

    Analyze the resume against the job description.

    Return ONLY valid JSON.

    Do not use markdown.
    Do not use ```json.
    Do not explain anything.

    The JSON schema is:

    {{
        "matching_skills": [
            "..."
        ],
        "missing_skills": [
            "..."
        ],
        "suggestions": [
            "..."
        ]
    }}

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt,
    )

    text = response.text.strip()

    text = (
        text.replace("```json", "")
            .replace("```", "")
            .strip()
    )

    print(text)

    return json.loads(text)