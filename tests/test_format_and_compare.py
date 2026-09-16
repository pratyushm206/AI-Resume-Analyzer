from format_checker import analyze_resume_format
from tailor_compare import compare_tailored_resume


def test_format_checker_scores_text_resume():
    text = """Jane Doe
jane@example.com 555-123-4567
Summary
Python engineer
Experience
Jan 2024 Backend Engineer
Education
BS
Skills
Python, Docker"""

    result = analyze_resume_format(text, file_size_bytes=1000)

    assert result["format_score"] >= 70
    assert all("name" in item for item in result["checks"])


def test_tailored_compare_reports_delta(mocker):
    mocker.patch("tailor_compare.analyze_ats_match", side_effect=[
        {"overall_score": 50.0, "breakdown": {"skill_match": 50.0}},
        {"overall_score": 70.0, "breakdown": {"skill_match": 75.0}},
    ])

    result = compare_tailored_resume("Python", "Python Docker", "Python Docker")

    assert result["score_delta"] == 20.0
    assert result["component_deltas"]["skill_match"] == 25.0
