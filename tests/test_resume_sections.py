from resume_sections import score_sections, split_resume_sections


def test_split_resume_sections_basic():
    text = """Jane Doe
Summary
Backend engineer
Skills
Python, Docker
Experience
Built APIs
Education
BS Computer Science"""

    sections = split_resume_sections(text)

    assert sections["Summary"] == "Backend engineer"
    assert "Python" in sections["Skills"]
    assert "Built APIs" in sections["Experience"]


def test_split_resume_sections_variants():
    text = """Profile
Full stack developer
Core Competencies
React and Node.js
Academic Background
B.Tech"""

    sections = split_resume_sections(text)

    assert "Full stack" in sections["Summary"]
    assert "React" in sections["Skills"]
    assert "B.Tech" in sections["Education"]


def test_score_sections_batches_texts_and_jd(monkeypatch):
    import resume_sections

    calls = []
    monkeypatch.setattr(resume_sections, "embed_texts", lambda texts: (
        calls.append(list(texts)) or [[1.0, 0.0], [0.0, 1.0], [1.0, 0.0]]
    ))

    scores = score_sections({"Summary": "Python developer", "Skills": "SQL"}, "Python role")

    assert len(calls) == 1
    assert calls[0] == ["Python developer", "SQL", "Python role"]
    assert scores == {"Summary": 100.0, "Skills": 0.0}
