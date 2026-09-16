from docx import Document
from pypdf import PdfReader

import doc_export
from report_generator import generate_pdf_report


def test_cover_letter_exports_contain_text(tmp_path):
    text = "Dear hiring team,\n\nI build Python systems.\n\nSincerely,\nJane Doe"

    pdf_path = tmp_path / "cover.pdf"
    pdf_path.write_bytes(doc_export.cover_letter_to_pdf(text))
    docx_path = tmp_path / "cover.docx"
    docx_path.write_bytes(doc_export.cover_letter_to_docx(text))

    assert pdf_path.stat().st_size > 100
    assert "Python systems" in "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages)
    assert "Jane Doe" in "\n".join(p.text for p in Document(str(docx_path)).paragraphs)


def test_report_generation_contains_key_text(tmp_path):
    pdf_path = tmp_path / "report.pdf"
    pdf_path.write_bytes(generate_pdf_report(
        resume_filename="resume.pdf",
        score=82.5,
        matching_skills=["Python"],
        missing_skills=["Docker"],
        suggestions=["Add metrics."],
        verdict="Good match.",
        section_scores={"Skills": 90},
    ))

    text = "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages)
    assert pdf_path.stat().st_size > 100
    assert "AI Resume Analyzer" in text
    assert "Python" in text
