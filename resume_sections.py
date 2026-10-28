import re

from ai_engine import _term_frequency_cosine, cosine_similarity, embed_texts

# Heading name -> regex that matches common variants of that heading.
# Matched against short lines only, so body text won't accidentally trigger it.
SECTION_PATTERNS = {
    "Summary": r"(summary|objective|profile)",
    "Skills": r"(skills|technical skills|core competencies)",
    "Experience": r"(experience|work experience|employment history|internship)",
    "Projects": r"(projects|personal projects|academic projects)",
    "Education": r"(education|academic background|qualifications)",
    "Certifications": r"(certifications|licenses|certificates)",
}


def split_resume_sections(resume_text: str) -> dict:
    """
    Best-effort split of resume text into named sections based on common
    heading keywords. Resumes vary a lot in formatting, so this is a
    heuristic, not a guaranteed-correct parser -- sections it can't
    confidently identify are simply left out of the result.
    """
    lines = resume_text.split("\n")
    headings = []

    for i, line in enumerate(lines):
        clean = line.strip()

        # Headings are short lines, not paragraph text.
        if not clean or len(clean) > 60 or len(clean.split()) > 5:
            continue

        for section_name, pattern in SECTION_PATTERNS.items():
            if re.fullmatch(pattern, clean, re.IGNORECASE):
                headings.append((i, section_name))
                break

    sections = {}

    for idx, (line_no, name) in enumerate(headings):
        start = line_no + 1
        end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        content = "\n".join(lines[start:end]).strip()

        if content:
            sections[name] = (sections.get(name, "") + "\n" + content).strip()

    return sections


def score_sections(sections: dict, job_description: str) -> dict:
    """
    Runs the existing match-scoring function against each resume section
    individually (instead of just the whole resume) so the UI can show
    where a candidate is strong or weak, not just one aggregate number.
    """
    valid_sections = [(name, text) for name, text in sections.items() if text.strip()]
    if not valid_sections:
        return {}
    try:
        vectors = embed_texts([text for _, text in valid_sections] + [job_description])
        jd_vector = vectors[-1]
        return {
            name: round(max(0.0, min(100.0, cosine_similarity(vector, jd_vector) * 100)), 2)
            for (name, _), vector in zip(valid_sections, vectors[:-1])
        }
    except Exception:
        return {
            name: round(max(0.0, min(100.0, _term_frequency_cosine(text, job_description) * 100)), 2)
            for name, text in valid_sections
        }
