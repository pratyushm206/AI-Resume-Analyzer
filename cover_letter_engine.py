import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_cover_letter(resume_text: str, job_description: str) -> str:
    """
    Generates a tailored cover letter from the candidate's actual resume
    content and the target job description. Returns plain text.
    """

    prompt = f"""
    You are a professional career coach writing a cover letter on behalf of a candidate.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Instructions:
    - Write a concise, professional cover letter (250-350 words).
    - Base it only on the candidate's actual resume content.
    - Do not invent experience, companies, or skills that aren't in the resume.
    - Avoid cliches like "I am writing to express my interest."
    - If the hiring company's name isn't known, address it to "the hiring team"
      rather than using a placeholder like [Company Name].
    - No markdown, no headers, no preamble, no code fences.
    - Output ONLY the cover letter text.
    """

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt,
    )

    return response.text.strip()