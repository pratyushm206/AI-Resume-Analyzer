import re

from ai_engine import calculate_match_score

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
    scores = {}

    for name, text in sections.items():
        if not text.strip():
            continue
        try:
            score = float(calculate_match_score(text, job_description))
            score = max(0.0, min(100.0, score))
            scores[name] = score
        except Exception:
            # If scoring a tiny/odd section fails, skip it rather than
            # breaking the whole analysis.
            continue

    return scores