"""
Before/after ATS comparison for generated tailored resumes.
"""

from __future__ import annotations

from ats_engine import analyze_ats_match, extract_terms


def compare_tailored_resume(
    original_resume: str,
    tailored_resume: str,
    job_description: str,
    *,
    original_result: dict | None = None,
    original_section_scores: dict | None = None,
    tailored_section_scores: dict | None = None,
) -> dict:
    before = original_result or analyze_ats_match(
        original_resume,
        job_description,
        section_scores=original_section_scores,
    )
    after = analyze_ats_match(
        tailored_resume,
        job_description,
        section_scores=tailored_section_scores,
    )

    before_breakdown = before.get("breakdown", {})
    after_breakdown = after.get("breakdown", {})
    deltas = {
        key: round(after_breakdown.get(key, 0.0) - before_breakdown.get(key, 0.0), 1)
        for key in before_breakdown
    }

    original_skills = extract_terms(original_resume)
    tailored_skills = extract_terms(tailored_resume)
    jd_skills = extract_terms(job_description)
    added_skills = sorted(tailored_skills - original_skills)
    unsupported_added_skills = sorted(set(added_skills) - jd_skills)
    skill_jump = deltas.get("skill_match", 0.0)

    warnings = []
    if unsupported_added_skills:
        warnings.append(
            "Tailored resume contains skills not detected in the original resume or JD: "
            + ", ".join(unsupported_added_skills)
        )
    elif added_skills and skill_jump > 20:
        warnings.append(
            "Skill Match increased sharply because newly detected JD skills appeared in the tailored resume. Review to confirm these are reworded existing experience, not invented claims: "
            + ", ".join(added_skills)
        )

    return {
        "before": before,
        "after": after,
        "score_delta": round(after.get("overall_score", 0.0) - before.get("overall_score", 0.0), 1),
        "component_deltas": deltas,
        "added_skills": added_skills,
        "warnings": warnings,
    }
