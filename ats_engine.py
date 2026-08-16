"""
ats_engine.py

Deterministic, explainable ATS scoring engine.

This is intentionally separate from ai_engine.py (which stays untouched,
so app.py keeps working on the old path while this is developed and tested).

Design principle: the numeric score must be REPRODUCIBLE. Same resume +
same JD -> same score, every time. Gemini is great for interpretation and
prose feedback, but it should never be the thing computing the number.

Public entry point:

    analyze_ats_match(resume_text, job_description) -> dict

Returns:
{
    "overall_score": float (0-100),
    "match_label": "Strong Match" | "Good Match" | "Weak Match" | "Very Weak Match",
    "breakdown": {
        "semantic_relevance": float,
        "skill_match": float,
        "keyword_coverage": float,
        "experience_match": float,
        "section_relevance": float,
    },
    "weights": {...},                 # so the UI can show "30% x 72 = 21.6" etc.
    "matched_skills": [str, ...],
    "missing_skills": [str, ...],
    "score_boosters": [str, ...],     # top matched skills, ranked
    "score_blockers": [str, ...],     # top missing skills, ranked
    "experience": {
        "required_years": float | None,
        "candidate_years": float | None,
    },
}
"""

import re
from typing import Dict, List, Optional, Set

# ---------------------------------------------------------------------------
# Reuse the already-loaded sentence-transformers model from ai_engine.py
# instead of loading a second copy of the model into memory.
# ---------------------------------------------------------------------------
from sklearn.metrics.pairwise import cosine_similarity

try:
    from ai_engine import model as _semantic_model
except ImportError:
    # Allows this file to still be run/tested even if ai_engine.py is
    # unavailable in the current working directory.
    from sentence_transformers import SentenceTransformer
    _semantic_model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------------------------------------------------------
# Controlled skill vocabulary.
#
# Canonical name -> list of surface-form aliases that should map to it.
# This is what stops "using" / "development" / "experience" from being
# treated as skills, and stops "React" vs "React.js" vs "reactjs" from
# being counted as two different (mis)matches.
#
# This list is deliberately extensible -- add to it as new resumes/JDs
# surface terms it doesn't catch yet.
# ---------------------------------------------------------------------------
SKILL_VOCAB: Dict[str, List[str]] = {
    "Java": ["java"],
    "Python": ["python"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "React.js": ["react.js", "react js", "reactjs", "react"],
    "Node.js": ["node.js", "node js", "nodejs", "node"],
    "Express.js": ["express.js", "express js", "expressjs", "express"],
    "Spring Boot": ["spring boot", "springboot", "spring"],
    "Hibernate": ["hibernate"],
    "Django": ["django"],
    "Flask": ["flask"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb", "mongo"],
    "SQL": ["sql"],
    "REST API Design": ["rest api", "restful api", "rest apis", "restful apis", "rest"],
    "GraphQL": ["graphql"],
    "AWS Cloud Foundations": ["aws", "amazon web services"],
    "Amazon EKS": ["eks", "elastic kubernetes service"],
    "Amazon ECS": ["ecs", "elastic container service"],
    "Azure": ["azure"],
    "Google Cloud Platform": ["gcp", "google cloud"],
    "Docker": ["docker", "containerization"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Infrastructure as Code": ["infrastructure as code", "iac"],
    "Terraform": ["terraform"],
    "CI/CD": ["ci/cd", "ci cd", "continuous integration", "continuous deployment"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Linux Administration": ["linux administration", "linux"],
    "Networking Fundamentals": ["networking", "network security"],
    "Agile Development": ["agile", "scrum"],
    "Unit / Integration Testing": [
        "unit testing", "integration testing", "software testing",
        "junit", "jest", "mocha", "pytest",
    ],
    "JWT Authentication": ["jwt", "json web token"],
    "OAuth": ["oauth"],
    "Data Structures & Algorithms": [
        "data structures", "algorithms", "dsa",
        "data structures and algorithms",
    ],
    "Machine Learning": ["machine learning", "ml"],
    "AI API Integration": [
        "gemini api", "openai api", "llm api", "ai api integration",
        "ai coding assistants", "agentic ides", "claude",
    ],
    "Cloud Computing Concepts": ["cloud computing"],
    "Go": ["golang", "go language", "go programming language"],
    # Bare "go" is deliberately excluded as an alias -- it's too common an
    # English word to safely word-boundary-match without false positives
    # ("go live", "go through", "on the go", etc.).
    "DevOps Practices": ["devops", "dev ops"],
}

# Non-technical requirement phrases that JDs frequently ask for and that
# a pure skill-keyword match tends to miss entirely.
QUALIFICATION_VOCAB: Dict[str, List[str]] = {
    "Team Leadership / Mentoring": ["leadership", "mentoring", "mentor", "team lead"],
    "Application Performance Optimization": [
        "performance optimization", "optimize application performance",
        "application performance",
    ],
    "Troubleshooting": ["troubleshoot", "troubleshooting"],
    "Cross-functional Collaboration": ["cross-functional", "cross functional", "collaboration"],
    "Production Monitoring & Debugging": [
        "production debugging", "production-level debugging", "system monitoring",
        "monitoring", "observability", "logging and monitoring",
    ],
    "Code Review Practices": [
        "code review", "code reviews", "technical standards", "coding standards",
    ],
}

FULL_VOCAB: Dict[str, List[str]] = {**SKILL_VOCAB, **QUALIFICATION_VOCAB}

_STOPWORDS = {
    "the", "and", "for", "with", "you", "your", "our", "are", "will",
    "this", "that", "have", "has", "from", "who", "can", "able", "into",
    "using", "use", "used", "including", "such", "other", "role", "work",
    "team", "years", "year", "experience", "skills", "skill", "strong",
    "good", "knowledge", "understanding", "need", "needs", "needed",
    "also", "we're", "we", "you'll", "you're",
}


def _alias_pattern(alias: str) -> re.Pattern:
    """Build a case-insensitive, word-boundary-safe regex for an alias."""
    escaped = re.escape(alias.lower())
    return re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", re.IGNORECASE)


# Precompile every alias pattern once at import time.
_COMPILED_VOCAB = {
    canonical: [_alias_pattern(a) for a in aliases]
    for canonical, aliases in FULL_VOCAB.items()
}


def extract_terms(text: str, vocab: Optional[Dict[str, List[str]]] = None) -> Set[str]:
    """Return the set of canonical vocab terms found in `text`."""
    if not text:
        return set()
    compiled = _COMPILED_VOCAB if vocab is None else {
        c: [_alias_pattern(a) for a in aliases] for c, aliases in vocab.items()
    }
    found = set()
    for canonical, patterns in compiled.items():
        if any(p.search(text) for p in patterns):
            found.add(canonical)
    return found


# ---------------------------------------------------------------------------
# Experience matching
# ---------------------------------------------------------------------------
_YEARS_REQUIRED_PATTERNS = [
    re.compile(r"minimum\s+(\d+)\+?\s*years?", re.IGNORECASE),
    re.compile(r"at\s+least\s+(\d+)\+?\s*years?", re.IGNORECASE),
    re.compile(r"(\d+)\+?\s*years?\s+of\s+experience", re.IGNORECASE),
    re.compile(r"(\d+)\+?\s*years?\s+experience", re.IGNORECASE),
]
_YEARS_ANY_PATTERN = re.compile(r"(\d+)\+?\s*years?", re.IGNORECASE)


def _extract_required_years(job_description: str) -> Optional[float]:
    for pattern in _YEARS_REQUIRED_PATTERNS:
        match = pattern.search(job_description)
        if match:
            return float(match.group(1))
    return None


def _extract_candidate_years(resume_text: str) -> Optional[float]:
    matches = _YEARS_ANY_PATTERN.findall(resume_text)
    if not matches:
        return None
    # Heuristic: take the largest explicit "N years" figure mentioned.
    # (Education percentages like "82%" won't match this pattern at all,
    # since it requires the literal word "year(s)" adjacent to the number.)
    return float(max(int(m) for m in matches))


def _experience_match_score(required_years, candidate_years) -> float:
    if required_years is None:
        # JD doesn't specify a numeric requirement -> don't penalize.
        return 100.0
    if candidate_years is None:
        return 0.0
    if candidate_years >= required_years:
        return 100.0
    return round(max(0.0, (candidate_years / required_years) * 100), 1)


# ---------------------------------------------------------------------------
# Semantic relevance (reuses the same model/approach as ai_engine.py)
# ---------------------------------------------------------------------------
def _semantic_relevance(resume_text: str, job_description: str) -> float:
    resume_embedding = _semantic_model.encode([resume_text])
    jd_embedding = _semantic_model.encode([job_description])
    similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
    return round(max(0.0, min(1.0, float(similarity))) * 100, 1)


# ---------------------------------------------------------------------------
# Generic keyword coverage (catches JD language outside the curated vocab)
# ---------------------------------------------------------------------------
def _keyword_coverage(resume_text: str, job_description: str, top_n: int = 25) -> float:
    words = re.findall(r"[a-zA-Z][a-zA-Z\-]{3,}", job_description.lower())
    keywords = [w for w in words if w not in _STOPWORDS]
    if not keywords:
        return 100.0

    # Rank by frequency in the JD, keep the top_n most emphasized terms.
    freq: Dict[str, int] = {}
    for w in keywords:
        freq[w] = freq.get(w, 0) + 1
    top_keywords = sorted(freq, key=freq.get, reverse=True)[:top_n]

    resume_lower = resume_text.lower()
    hits = sum(1 for kw in top_keywords if kw in resume_lower)
    return round((hits / len(top_keywords)) * 100, 1)


# ---------------------------------------------------------------------------
# Section relevance
#
# Standalone-safe default: checks whether the standard resume sections are
# present at all. If you already have resume_sections.score_sections()
# output available at call time, pass it in via `section_scores` and this
# will use the real per-section numbers instead of the placeholder check.
# ---------------------------------------------------------------------------
_EXPECTED_SECTIONS = ["summary", "education", "projects", "skills", "certifications"]


def _section_relevance(resume_text: str, section_scores: Optional[Dict[str, float]]) -> float:
    if section_scores:
        values = [v for v in section_scores.values() if isinstance(v, (int, float))]
        if values:
            return round(sum(values) / len(values), 1)

    resume_lower = resume_text.lower()
    present = sum(1 for s in _EXPECTED_SECTIONS if s in resume_lower)
    return round((present / len(_EXPECTED_SECTIONS)) * 100, 1)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
WEIGHTS = {
    "semantic_relevance": 0.30,
    "skill_match": 0.30,
    "keyword_coverage": 0.15,
    "experience_match": 0.15,
    "section_relevance": 0.10,
}


def _match_label(score: float) -> str:
    if score >= 75:
        return "Strong Match"
    if score >= 55:
        return "Good Match"
    if score >= 35:
        return "Weak Match"
    return "Very Weak Match"


def analyze_ats_match(
    resume_text: str,
    job_description: str,
    section_scores: Optional[Dict[str, float]] = None,
) -> dict:
    resume_skills = extract_terms(resume_text)
    jd_skills = extract_terms(job_description)

    matched_skills = sorted(jd_skills & resume_skills)
    missing_skills = sorted(jd_skills - resume_skills)

    # Skill match is scored against what the JD actually asks for.
    # If the JD doesn't name any vocab-recognized skill, don't punish the
    # resume for it -- fall back to neutral so the metric doesn't zero out
    # the whole score on JDs written in unusual language.
    if jd_skills:
        skill_match = round((len(matched_skills) / len(jd_skills)) * 100, 1)
    else:
        skill_match = 100.0

    semantic_relevance = _semantic_relevance(resume_text, job_description)
    keyword_coverage = _keyword_coverage(resume_text, job_description)

    required_years = _extract_required_years(job_description)
    candidate_years = _extract_candidate_years(resume_text)
    experience_match = _experience_match_score(required_years, candidate_years)

    section_relevance = _section_relevance(resume_text, section_scores)

    breakdown = {
        "semantic_relevance": semantic_relevance,
        "skill_match": skill_match,
        "keyword_coverage": keyword_coverage,
        "experience_match": experience_match,
        "section_relevance": section_relevance,
    }

    overall_score = round(
        sum(breakdown[k] * WEIGHTS[k] for k in WEIGHTS), 1
    )
    overall_score = max(0.0, min(100.0, overall_score))

    return {
        "overall_score": overall_score,
        "match_label": _match_label(overall_score),
        "breakdown": breakdown,
        "weights": WEIGHTS,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score_boosters": matched_skills[:8],
        "score_blockers": missing_skills[:8],
        "experience": {
            "required_years": required_years,
            "candidate_years": candidate_years,
        },
    }


# ---------------------------------------------------------------------------
# Standalone test
#
# Run: python ats_engine.py
#
# This uses a condensed version of the JD from your screenshots so you can
# sanity-check the engine before wiring it into app.py. Swap in your real
# resume_text / job_description (e.g. read them from the same PDF you used
# for the 35.9% report) to get a real before/after comparison.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_resume = """
    Pratyush Mishra
    Full Stack Engineer (final-year B.Tech CS, AI & ML)

    SUMMARY
    Full Stack Engineer with strong foundations in Java, JavaScript, and
    cloud-first methodologies. Experienced in engineering end-to-end web
    applications, designing scalable backend systems, and crafting
    responsive user interfaces with React.js.

    PROJECTS
    NutriTrack - Full-stack nutrition app built with React and Tailwind CSS,
    a normalized PostgreSQL database using Prisma ORM, stateless RESTful
    APIs in Node.js and Express with JWT-based authentication.

    PrepSense - Secure Node.js/Express REST API using MongoDB and Mongoose,
    IDOR-protected sessions and role-based admin middleware.

    TECHNICAL SKILLS
    Java, JavaScript, Python, C, HTML, CSS, React.js, Tailwind CSS,
    Node.js, Express.js, REST API Design, JWT Authentication,
    PostgreSQL, MongoDB, Prisma ORM, MySQL,
    AWS Cloud Foundations, Linux Administration (Red Hat),
    Google Gemini API, LLM APIs, Rate-Limited AI Pipelines,
    Data Structures & Algorithms, OOP, DBMS, Computer Networks

    CERTIFICATIONS
    AWS Academy Cloud Foundations, CCNA, Cybersecurity Foundations,
    Linux System Administration I & II

    ACHIEVEMENTS
    Participated in multiple inter-college hackathons. Selected in the
    college-level Smart India Hackathon (SIH) screening. Solved 300+ DSA
    problems on LeetCode and HackerRank.
    """

    sample_jd = """
    Java Full Stack Developer

    The candidate should have minimum 3 years of experience in Java Full
    Stack Development. Required skills: Java Backend Frameworks
    (e.g., Spring Boot, Hibernate), Agile Development Practices,
    Application Performance Optimization, Mentoring and Team Leadership
    Experience. Understanding of cloud computing concepts and agile
    development practices. Ability to troubleshoot and optimize
    application performance across the stack.
    """

    result = analyze_ats_match(sample_resume, sample_jd)

    print(f"\nOverall ATS Score: {result['overall_score']}%  ({result['match_label']})\n")
    print("Breakdown:")
    for key, value in result["breakdown"].items():
        print(f"  {key:22s} {value:5.1f}%  (weight {int(WEIGHTS[key]*100)}%)")
    print(f"\nMatched skills ({len(result['matched_skills'])}): {result['matched_skills']}")
    print(f"Missing skills ({len(result['missing_skills'])}): {result['missing_skills']}")
    print(f"\nExperience: required={result['experience']['required_years']}, "
          f"candidate={result['experience']['candidate_years']}")