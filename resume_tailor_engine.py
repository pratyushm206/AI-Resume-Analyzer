import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_tailored_resume(resume_text: str, job_description: str, missing_skills: list) -> str:
    """
    Rewrites the candidate's resume to better align with the given job
    description: re-prioritizing and rephrasing existing content, without
    inventing experience or skills the candidate doesn't actually have.
    Returns plain text.
    """

    missing_skills_text = ", ".join(missing_skills) if missing_skills else "None identified"

    prompt = f"""
    You are an expert resume writer helping a candidate tailor their resume to a specific job description.

    Original Resume:
    {resume_text}

    Job Description:
    {job_description}

    Skills the job description asks for that are NOT clearly present in the resume:
    {missing_skills_text}

    Instructions:
    - Rewrite the resume so it's better aligned with this job description.
    - Reorder and re-emphasize existing bullet points so the most relevant experience
      appears first within each section.
    - Rephrase bullet points to use language and keywords from the job description,
      but ONLY where the underlying experience genuinely supports it.
    - Do NOT invent projects, employers, tools, certifications, or skills that aren't
      already present in the original resume, even from the "missing skills" list above.
    - If a missing skill is plausibly implied by existing experience (e.g. resume shows
      Express.js and JD wants "Node.js backend development"), make that connection explicit
      in the wording. If it is not genuinely supported by the resume, leave it out entirely.
    - Keep the candidate's real job titles, dates, companies, and degree information unchanged.
    - Preserve the original resume's overall section structure (e.g. Summary, Skills,
      Experience, Projects, Education) and keep section headings in capital letters.
    - Keep formatting as plain text: section headings on their own line, bullet points
      starting with "-".
    - No markdown, no code fences, no commentary before or after the resume.
    - Output ONLY the rewritten resume text.
    """

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt,
    )

    return response.text.strip()