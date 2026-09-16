import types

import cover_letter_engine
import gemini_engine
import resume_tailor_engine


def test_gemini_partial_json_response(mocker):
    mocker.patch.object(
        gemini_engine.client.models,
        "generate_content",
        return_value=types.SimpleNamespace(text='{"matching_skills": ["Python"]}'),
    )

    result = gemini_engine.analyze_resume_with_gemini("resume", "jd")

    assert result["matching_skills"] == ["Python"]
    assert result["missing_skills"] == []
    assert result["recruiter_verdict"] == ""


def test_gemini_malformed_json_response(mocker):
    mocker.patch.object(
        gemini_engine.client.models,
        "generate_content",
        return_value=types.SimpleNamespace(text="not json"),
    )

    result = gemini_engine.analyze_resume_with_gemini("resume", "jd")

    assert result["matching_skills"] == []
    assert result["suggestions"]


def test_cover_letter_empty_response(mocker):
    mocker.patch.object(
        cover_letter_engine.client.models,
        "generate_content",
        return_value=types.SimpleNamespace(text=None),
    )

    assert cover_letter_engine.generate_cover_letter("resume", "jd") == ""


def test_tailored_resume_empty_response(mocker):
    mocker.patch.object(
        resume_tailor_engine.client.models,
        "generate_content",
        return_value=types.SimpleNamespace(text=None),
    )

    assert resume_tailor_engine.generate_tailored_resume("resume", "jd", []) == ""
