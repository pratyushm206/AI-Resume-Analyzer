import re
import time
from pathlib import Path

import fitz
import streamlit as st
from PIL import Image

from report_generator import generate_pdf_report
import doc_export
from format_checker import analyze_resume_format

from frontend.styles import load_css
from frontend import components

LOGO_PATH = Path(__file__).resolve().parent / "frontend" / "assets" / "logo.png"
PAGE_ICON = Image.open(LOGO_PATH) if LOGO_PATH.exists() else "📄"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon=PAGE_ICON,
    layout="wide"
)

# -----------------------------
# Load CSS
# -----------------------------
st.markdown(load_css(), unsafe_allow_html=True)

# -----------------------------
# Hero
# -----------------------------
components.hero()
components.workflow_strip()

def _text_stats(text: str) -> dict:
    words = re.findall(r"[A-Za-z][A-Za-z0-9+#.\-/]*", text or "")
    return {
        "words": len(words),
        "characters": len(text or ""),
        "estimated_read_minutes": max(1, round(len(words) / 220)) if words else 0,
    }


def _extract_pdf_text(file_bytes: bytes) -> tuple[str, fitz.Document]:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    resume_text = ""
    for page in doc:
        resume_text += page.get_text()
    return resume_text, doc


def _set_progress(status, label: str, delay: float = 5.0):
    status.write(label)
    status.update(label=label, state="running")
    time.sleep(delay)


def _read_uploaded_jd_pdf(jd_pdf_file) -> str:
    if jd_pdf_file is None:
        return ""
    cache_key = f"{jd_pdf_file.name}:{jd_pdf_file.size}"
    if st.session_state.get("jd_pdf_cache_key") == cache_key:
        return st.session_state.get("jd_pdf_text", "")
    jd_text, _doc = _extract_pdf_text(jd_pdf_file.getvalue())
    st.session_state["jd_pdf_cache_key"] = cache_key
    st.session_state["jd_pdf_text"] = jd_text
    return jd_text


if "jd_draft" not in st.session_state:
    st.session_state["jd_draft"] = ""

# -----------------------------
# Inputs
# -----------------------------
input_left, input_right = st.columns([1.5, 0.95], gap="large")

with input_left:
    with st.container(border=False):
        uploaded_file = st.file_uploader(
            "Resume (PDF)",
            type=["pdf"],
            help="Limit 10MB. Upload a text-based PDF resume. Scanned/image-only PDFs may not extract cleanly.",
        )

        jd_input_mode = st.radio(
            "Job description",
            ["Paste text", "Upload PDF"],
            horizontal=True,
        )

        jd_pdf_file = None
        if jd_input_mode == "Upload PDF":
            jd_pdf_file = st.file_uploader(
                "Job description PDF",
                type=["pdf"],
                help="Limit 10MB. Upload a text-based JD PDF.",
            )
            current_jd_text = _read_uploaded_jd_pdf(jd_pdf_file)
            if current_jd_text:
                with st.expander("Extracted JD text", expanded=False):
                    st.text_area(
                        "Extracted JD",
                        value=current_jd_text,
                        height=180,
                        label_visibility="collapsed",
                        disabled=True,
                    )
        else:
            job_description = st.text_area(
                "Paste Job Description",
                key="jd_draft",
                height=250,
                placeholder="Paste the full JD here. Include responsibilities, required skills, years of experience, and nice-to-have qualifications for the best match analysis.",
            )
            current_jd_text = job_description

        action_primary, action_secondary = st.columns([1.3, 1], gap="small")
        with action_primary:
            analyze_clicked = st.button("Analyze Resume", type="primary", use_container_width=True)
        with action_secondary:
            format_clicked = st.button("Check ATS format only", use_container_width=True)

with input_right:
    components.input_helper_panel()
    jd_stats = _text_stats(current_jd_text)
    components.jd_quality_panel(jd_stats)

# -----------------------------
# Analyze
# -----------------------------
if format_clicked:
    if uploaded_file is None:
        st.warning("Upload a resume.")
        st.stop()

    file_bytes = uploaded_file.getvalue()
    resume_text, doc = _extract_pdf_text(file_bytes)
    st.session_state["resume_text"] = resume_text
    st.session_state["resume_filename"] = uploaded_file.name
    st.session_state["resume_stats"] = _text_stats(resume_text)
    st.session_state["format_result"] = analyze_resume_format(
        resume_text,
        pdf_doc=doc,
        file_size_bytes=len(file_bytes),
    )
    st.toast("ATS format check completed!", icon="✅")

if analyze_clicked:

    if uploaded_file is None:
        st.warning("Upload a resume.")
        st.stop()

    if jd_input_mode == "Upload PDF" and jd_pdf_file is None:
        st.warning("Upload a Job Description PDF or switch to pasted text.")
        st.stop()

    if jd_input_mode == "Paste text" and not st.session_state.get("jd_draft", "").strip():
        st.warning("Enter Job Description.")
        st.stop()

    with st.status("Preparing analysis...", expanded=True) as status:
        from ats_engine import analyze_ats_match
        from gemini_engine import analyze_resume_with_gemini
        from resume_sections import split_resume_sections, score_sections

        _set_progress(status, "Extracting resume text...")
        file_bytes = uploaded_file.getvalue()
        resume_text, doc = _extract_pdf_text(file_bytes)

        if len(resume_text.strip()) < 80:
            status.update(label="Resume text extraction failed.", state="error")
            st.error("This PDF did not yield enough readable text. Try exporting the resume as a text-based PDF, then upload it again.")
            st.stop()

        if jd_input_mode == "Upload PDF":
            _set_progress(status, "Extracting JD text...")
            job_description = _read_uploaded_jd_pdf(jd_pdf_file)
            if len(job_description.strip()) < 40:
                status.update(label="JD text extraction failed.", state="error")
                st.error("This JD PDF did not yield enough readable text. Try a text-based PDF or paste the JD manually.")
                st.stop()
        else:
            _set_progress(status, "Reading pasted JD...")
            job_description = st.session_state.get("jd_draft", "")

        _set_progress(status, "Analyzing resume sections...")
        sections = split_resume_sections(resume_text)
        section_scores = score_sections(sections, job_description)

        _set_progress(status, "Analyzing JD requirements...")
        format_result = analyze_resume_format(
            resume_text,
            pdf_doc=doc,
            file_size_bytes=len(file_bytes),
        )

        _set_progress(status, "Comparing resume with JD...")
        ats_result = analyze_ats_match(
            resume_text,
            job_description,
            section_scores=section_scores,
        )
        score = ats_result["overall_score"]

        _set_progress(status, "Matching skills and constructing feedback...")
        analysis = analyze_resume_with_gemini(
            resume_text,
            job_description
        )

        _set_progress(status, "Constructing the result...")
        pdf_report_bytes = generate_pdf_report(
            resume_filename=uploaded_file.name,
            score=score,
            matching_skills=analysis.get("matching_skills", []),
            missing_skills=analysis.get("missing_skills", []),
            suggestions=analysis.get("suggestions", []),
            verdict=analysis.get("recruiter_verdict", ""),
            section_scores=section_scores,
        )
        status.update(label="Analysis completed.", state="complete", expanded=False)

    st.toast("Analysis completed successfully!", icon="✅")

    # Persisted in session_state because the PDF-download and
    # cover-letter buttons below trigger their own Streamlit reruns,
    # which would otherwise wipe out these results since they only
    # exist inside this "Analyze Resume" click block.
    st.session_state["resume_text"] = resume_text
    st.session_state["resume_filename"] = uploaded_file.name
    st.session_state["job_description"] = job_description
    st.session_state["resume_stats"] = _text_stats(resume_text)
    st.session_state["jd_stats"] = _text_stats(job_description)
    st.session_state["score"] = score
    st.session_state["ats_result"] = ats_result
    st.session_state["format_result"] = format_result
    st.session_state["analysis"] = analysis
    st.session_state["section_scores"] = section_scores
    st.session_state["pdf_report_bytes"] = pdf_report_bytes
    st.session_state.pop("cover_letter", None)
    st.session_state.pop("cover_letter_pdf", None)
    st.session_state.pop("cover_letter_docx", None)
    st.session_state.pop("tailored_resume", None)
    st.session_state.pop("tailored_resume_pdf", None)
    st.session_state.pop("tailored_resume_docx", None)
    st.session_state.pop("tailored_comparison", None)

# -----------------------------
# Results (persisted across reruns)
# -----------------------------
if "format_result" in st.session_state and "analysis" not in st.session_state:
    format_placeholder = st.empty()
    with format_placeholder.container():
        components.analysis_hero(
            filename=st.session_state.get("resume_filename", "Resume"),
            resume_stats=st.session_state.get("resume_stats", {}),
            jd_stats={},
            match_label=st.session_state["format_result"].get("label", "Format Check"),
            score=st.session_state["format_result"].get("format_score", 0),
            matching_count=0,
            missing_count=0,
        )
        components.format_checker_card(st.session_state["format_result"])

if "analysis" in st.session_state:

    # Wrapping the whole results section in a single empty() container
    # makes Streamlit clear and redraw it as one atomic block on every
    # rerun, instead of streaming it in top-to-bottom while the previous
    # run's stale content is still visible further down the page.
    results_placeholder = st.empty()

    with results_placeholder.container():

        score = st.session_state["score"]
        ats_result = st.session_state["ats_result"]
        analysis = st.session_state["analysis"]
        section_scores = st.session_state["section_scores"]

        # -----------------------------
        # Dashboard
        # -----------------------------
        matched_skills = ats_result.get("matched_skills", [])
        missing_skills = ats_result.get("missing_skills", [])
        matching_count = len(matched_skills)
        missing_count = len(missing_skills)

        components.analysis_hero(
            filename=st.session_state.get("resume_filename", "Resume"),
            resume_stats=st.session_state.get("resume_stats", {}),
            jd_stats=st.session_state.get("jd_stats", {}),
            match_label=ats_result.get("match_label", "Match"),
            score=score,
            matching_count=matching_count,
            missing_count=missing_count,
        )

        tabs = st.tabs(["Summary", "Score Drivers", "Sections", "Skills Diff", "ATS Format"])
        with tabs[0]:
            components.verdict_card(
                analysis.get(
                    "recruiter_verdict",
                    "No recruiter verdict available."
                )
            )
            components.suggestions_card(analysis.get("suggestions", []))
        with tabs[1]:
            components.score_drivers(ats_result)
        with tabs[2]:
            components.section_breakdown(section_scores)
        with tabs[3]:
            components.skills_diff(matched_skills, missing_skills)
            components.sanity_note(matching_count, missing_count)
        with tabs[4]:
            components.format_checker_card(st.session_state.get("format_result", {}))

        st.divider()

        # -----------------------------
        # PDF report + cover letter + tailored resume actions
        # -----------------------------
        action_left, action_mid, action_right = st.columns(3)

        with action_left:
            st.download_button(
                "⬇️ Download PDF Report",
                data=st.session_state["pdf_report_bytes"],
                file_name="resume_analysis_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        with action_mid:
            if st.button("✉️ Generate Cover Letter", use_container_width=True):
                with st.spinner("Writing cover letter..."):
                    from llm_utils import LLMProviderError, LLMTimeoutError
                    from cover_letter_engine import generate_cover_letter

                    try:
                        cover_letter = generate_cover_letter(
                            st.session_state["resume_text"],
                            st.session_state["job_description"],
                        )
                    except LLMTimeoutError:
                        st.error("The cover letter request took more than 45 seconds. Please try again.")
                        st.stop()
                    except LLMProviderError as exc:
                        st.error(str(exc))
                        st.stop()
                    # Rendered once here, not on every future rerun --
                    # the download buttons below just read these bytes.
                    st.session_state["cover_letter"] = cover_letter
                    st.session_state["cover_letter_pdf"] = doc_export.cover_letter_to_pdf(cover_letter)
                    st.session_state["cover_letter_docx"] = doc_export.cover_letter_to_docx(cover_letter)
                st.toast("Cover letter ready!", icon="✅")
                st.rerun()

        with action_right:
            if st.button("📝 Modify Resume for JD", use_container_width=True):
                with st.spinner("Tailoring resume to this job description..."):
                    from llm_utils import LLMProviderError, LLMTimeoutError
                    from resume_tailor_engine import generate_tailored_resume
                    from resume_sections import split_resume_sections, score_sections
                    from tailor_compare import compare_tailored_resume

                    try:
                        tailored_resume = generate_tailored_resume(
                            st.session_state["resume_text"],
                            st.session_state["job_description"],
                            analysis.get("missing_skills", []),
                        )
                    except LLMTimeoutError:
                        st.error("The tailored resume request took more than 45 seconds. Please try again.")
                        st.stop()
                    except LLMProviderError as exc:
                        st.error(str(exc))
                        st.stop()
                    tailored_sections = split_resume_sections(tailored_resume)
                    tailored_section_scores = score_sections(
                        tailored_sections,
                        st.session_state["job_description"],
                    )
                    st.session_state["tailored_resume"] = tailored_resume
                    st.session_state["tailored_resume_pdf"] = doc_export.tailored_resume_to_pdf(tailored_resume)
                    st.session_state["tailored_resume_docx"] = doc_export.tailored_resume_to_docx(tailored_resume)
                    st.session_state["tailored_comparison"] = compare_tailored_resume(
                        st.session_state["resume_text"],
                        tailored_resume,
                        st.session_state["job_description"],
                        original_result=st.session_state["ats_result"],
                        original_section_scores=st.session_state["section_scores"],
                        tailored_section_scores=tailored_section_scores,
                    )
                st.toast("Tailored resume ready!", icon="✅")
                st.rerun()

        if "cover_letter" in st.session_state:
            st.divider()
            components.cover_letter_card(st.session_state["cover_letter"])

            cl_txt, cl_pdf, cl_docx = st.columns(3)
            with cl_txt:
                st.download_button(
                    "⬇️ .TXT",
                    data=st.session_state["cover_letter"],
                    file_name="cover_letter.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with cl_pdf:
                st.download_button(
                    "⬇️ .PDF",
                    data=st.session_state["cover_letter_pdf"],
                    file_name="cover_letter.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            with cl_docx:
                st.download_button(
                    "⬇️ .DOCX",
                    data=st.session_state["cover_letter_docx"],
                    file_name="cover_letter.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )

        if "tailored_resume" in st.session_state:
            st.divider()
            if "tailored_comparison" in st.session_state:
                components.tailored_comparison_card(st.session_state["tailored_comparison"])
            components.tailored_resume_card(st.session_state["tailored_resume"])

            tr_txt, tr_pdf, tr_docx = st.columns(3)
            with tr_txt:
                st.download_button(
                    "⬇️ .TXT",
                    data=st.session_state["tailored_resume"],
                    file_name="tailored_resume.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with tr_pdf:
                st.download_button(
                    "⬇️ .PDF",
                    data=st.session_state["tailored_resume_pdf"],
                    file_name="tailored_resume.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            with tr_docx:
                st.download_button(
                    "⬇️ .DOCX",
                    data=st.session_state["tailored_resume_docx"],
                    file_name="tailored_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )

components.site_footer()
