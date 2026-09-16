import ats_engine


def test_scoring_is_deterministic():
    resume = "SUMMARY\nPython engineer\nSKILLS\nPython, React.js, AWS\nEXPERIENCE\n3 years"
    jd = "Need Python, React, AWS with minimum 2 years of experience."

    first = ats_engine.analyze_ats_match(resume, jd)
    second = ats_engine.analyze_ats_match(resume, jd)

    assert first == second


def test_weighting_math(monkeypatch):
    monkeypatch.setattr(ats_engine, "_semantic_relevance", lambda *_: 80.0)
    monkeypatch.setattr(ats_engine, "_keyword_coverage", lambda *_: 60.0)
    result = ats_engine.analyze_ats_match(
        "SUMMARY\nPython\nSKILLS\nPython\nEXPERIENCE\n2 years\nEDUCATION\nBS",
        "Python minimum 2 years",
        section_scores={"Summary": 70.0},
    )

    expected = (80 * 0.30) + (100 * 0.30) + (60 * 0.15) + (100 * 0.15) + (70 * 0.10)
    assert result["overall_score"] == round(expected, 1)


def test_empty_inputs_do_not_crash():
    result = ats_engine.analyze_ats_match("", "")

    assert 0 <= result["overall_score"] <= 100
    assert result["matched_skills"] == []


def test_no_skill_overlap():
    result = ats_engine.analyze_ats_match("Python developer", "Java Spring Boot")

    assert result["breakdown"]["skill_match"] == 0.0
    assert "Java" in result["missing_skills"]
