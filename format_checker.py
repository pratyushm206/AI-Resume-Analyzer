"""
Deterministic ATS format and parseability checks.

This module intentionally does not look at a job description. It scores
whether a resume PDF is likely to parse cleanly in an ATS: readable text,
standard sections, contact details, dates, page count, file size, and
layout features that commonly confuse parsers.
"""

from __future__ import annotations

import re
from typing import Any


SECTION_ALIASES = {
    "Summary": ["summary", "professional summary", "profile", "objective"],
    "Experience": ["experience", "work experience", "employment history", "internship"],
    "Education": ["education", "academic background", "qualifications"],
    "Skills": ["skills", "technical skills", "core competencies"],
}

DATE_PATTERNS = [
    re.compile(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{4}\b", re.I),
    re.compile(r"\b\d{1,2}/\d{4}\b"),
    re.compile(r"\b\d{4}\s*[-–]\s*(?:\d{4}|present|current)\b", re.I),
]


def _check(name: str, passed: bool, points: int, earned: int, explanation: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "points": points,
        "earned": earned if passed else 0,
        "explanation": explanation,
    }


def _has_section(text: str, aliases: list[str]) -> bool:
    for alias in aliases:
        pattern = re.compile(rf"^\s*{re.escape(alias)}\s*$", re.I | re.M)
        if pattern.search(text):
            return True
    return False


def _date_style_count(text: str) -> int:
    return sum(1 for pattern in DATE_PATTERNS if pattern.search(text))


def analyze_resume_format(
    resume_text: str,
    *,
    pdf_doc: Any | None = None,
    file_size_bytes: int | None = None,
) -> dict[str, Any]:
    text = resume_text or ""
    stripped = text.strip()
    checks: list[dict[str, Any]] = []

    word_count = len(re.findall(r"[A-Za-z][A-Za-z0-9+#.\-/]*", text))
    checks.append(_check(
        "Extractable text",
        word_count >= 80,
        20,
        20,
        "Resume text is readable by the PDF parser." if word_count >= 80 else "Too little selectable text was extracted; the file may be scanned or image-only.",
    ))

    missing_sections = [
        section for section, aliases in SECTION_ALIASES.items()
        if not _has_section(text, aliases)
    ]
    checks.append(_check(
        "Standard section headers",
        not missing_sections,
        20,
        20,
        "Summary, Experience, Education, and Skills headings are present." if not missing_sections else f"Missing or non-standard headings: {', '.join(missing_sections)}.",
    ))

    email_found = bool(re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text))
    phone_found = bool(re.search(r"(?:\+?\d[\s().-]*){10,}", text))
    checks.append(_check(
        "Plain-text contact info",
        email_found and phone_found,
        15,
        15,
        "Email and phone number are present in extractable text." if email_found and phone_found else "Add an email and phone number as ordinary text, not only inside headers, footers, or graphics.",
    ))

    date_styles = _date_style_count(text)
    checks.append(_check(
        "Consistent date formats",
        date_styles <= 1,
        10,
        10,
        "Dates appear to use one consistent style." if date_styles <= 1 else "Multiple date styles were detected; use one style such as Jan 2025 or 01/2025 throughout.",
    ))

    page_count = len(pdf_doc) if pdf_doc is not None else None
    page_ok = page_count is None or 1 <= page_count <= 3
    checks.append(_check(
        "Reasonable page count",
        page_ok,
        10,
        10,
        "Page count is within the typical ATS-friendly range." if page_ok else f"{page_count} pages detected; most ATS resumes should stay between 1 and 3 pages.",
    ))

    size_ok = file_size_bytes is None or file_size_bytes <= 5 * 1024 * 1024
    checks.append(_check(
        "Reasonable file size",
        size_ok,
        5,
        5,
        "File size is comfortably below 5 MB." if size_ok else "File is larger than 5 MB; compress or simplify it before applying.",
    ))

    has_images = False
    has_tables = False
    if pdf_doc is not None:
        for page in pdf_doc:
            has_images = has_images or bool(page.get_images(full=True))
            try:
                has_tables = has_tables or bool(page.find_tables().tables)
            except Exception:
                has_tables = False

    checks.append(_check(
        "No parser-hostile tables",
        not has_tables,
        10,
        10,
        "No PDF table structures were detected." if not has_tables else "Tables were detected; many ATS parsers read table cells out of order.",
    ))
    checks.append(_check(
        "No essential graphics",
        not has_images,
        5,
        5,
        "No embedded images were detected." if not has_images else "Embedded images were detected; keep all essential resume content as selectable text.",
    ))

    replacement_chars = text.count("\ufffd")
    encoding_ok = bool(stripped) and replacement_chars <= max(1, len(text) // 500)
    checks.append(_check(
        "Font and encoding sanity",
        encoding_ok,
        5,
        5,
        "Extracted text has no obvious encoding problems." if encoding_ok else "Extracted text includes unusual replacement characters or no readable text.",
    ))

    earned = sum(item["earned"] for item in checks)
    total = sum(item["points"] for item in checks)
    score = round((earned / total) * 100, 1) if total else 0.0

    if score >= 85:
        label = "ATS Friendly"
    elif score >= 65:
        label = "Mostly Parseable"
    elif score >= 40:
        label = "Needs Cleanup"
    else:
        label = "High Parse Risk"

    return {"format_score": score, "label": label, "checks": checks}
