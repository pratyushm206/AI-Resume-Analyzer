import json
from google import genai
from llm_utils import LLMProviderError, LLMTimeoutError, run_with_timeout
from secrets_config import get_secret


client = genai.Client(
    api_key=get_secret("GEMINI_API_KEY")
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

    try:
        response = run_with_timeout(
            lambda: client.models.generate_content(
                model="models/gemini-3.5-flash",
                contents=prompt,
            )
        )
    except LLMTimeoutError:
        return {
            "matching_skills": [],
            "missing_skills": [],
            "suggestions": [
                "AI analysis timed out. Please try again with a shorter resume or job description."
            ],
            "recruiter_verdict": "Analysis unavailable because the AI request did not answer in time."
        }
    except LLMProviderError as exc:
        return {
            "matching_skills": [],
            "missing_skills": [],
            "suggestions": [str(exc)],
            "recruiter_verdict": "AI feedback is temporarily unavailable, but the deterministic ATS score still completed."
        }

    response_text = (response.text or "").strip()

    response_text = (
        response_text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        analysis = json.loads(response_text)
        return {
            "matching_skills": analysis.get("matching_skills", []) if isinstance(analysis, dict) else [],
            "missing_skills": analysis.get("missing_skills", []) if isinstance(analysis, dict) else [],
            "suggestions": analysis.get("suggestions", []) if isinstance(analysis, dict) else [],
            "recruiter_verdict": analysis.get("recruiter_verdict", "") if isinstance(analysis, dict) else "",
        }

    except json.JSONDecodeError:
        return {
            "matching_skills": [],
            "missing_skills": [],
            "suggestions": [
                "AI could not generate a valid analysis. Please try again."
            ],
            "recruiter_verdict": "Analysis unavailable due to an AI response formatting error."
        }
