from resume_sections import split_resume_sections


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
