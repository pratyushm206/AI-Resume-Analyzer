import streamlit as st
import fitz

from ats_engine import analyze_ats_match
from gemini_engine import analyze_resume_with_gemini
from cover_letter_engine import generate_cover_letter
from resume_tailor_engine import generate_tailored_resume
from resume_sections import split_resume_sections, score_sections
from report_generator import generate_pdf_report
import doc_export

from frontend.styles import load_css
from frontend import components

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
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

# -----------------------------
# Inputs
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

# -----------------------------
# Analyze
# -----------------------------
if st.button("🚀 Analyze Resume", use_container_width=True):

    if uploaded_file is None:
        st.warning("Upload a resume.")
        st.stop()

    if not job_description.strip():
        st.warning("Enter Job Description.")
        st.stop()

    doc = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    resume_text = ""

    for page in doc:
        resume_text += page.get_text()

    with st.spinner("Analyzing Resume..."):

        sections = split_resume_sections(resume_text)
        section_scores = score_sections(sections, job_description)

        ats_result = analyze_ats_match(
            resume_text,
            job_description,
            section_scores=section_scores,
        )
        score = ats_result["overall_score"]

        analysis = analyze_resume_with_gemini(
            resume_text,
            job_description
        )

        # Generated once here rather than on every rerun -- see note
        # above the download buttons for why this matters.
        pdf_report_bytes = generate_pdf_report(
            resume_filename=uploaded_file.name,
            score=score,
            matching_skills=analysis.get("matching_skills", []),
            missing_skills=analysis.get("missing_skills", []),
            suggestions=analysis.get("suggestions", []),
            verdict=analysis.get("recruiter_verdict", ""),
            section_scores=section_scores,
        )

    st.toast("Analysis completed successfully!", icon="✅")

    # Persisted in session_state because the PDF-download and
    # cover-letter buttons below trigger their own Streamlit reruns,
    # which would otherwise wipe out these results since they only
    # exist inside this "Analyze Resume" click block.
    st.session_state["resume_text"] = resume_text
    st.session_state["resume_filename"] = uploaded_file.name
    st.session_state["job_description"] = job_description
    st.session_state["score"] = score
    st.session_state["ats_result"] = ats_result
    st.session_state["analysis"] = analysis
    st.session_state["section_scores"] = section_scores
    st.session_state["pdf_report_bytes"] = pdf_report_bytes
    st.session_state.pop("cover_letter", None)
    st.session_state.pop("cover_letter_pdf", None)
    st.session_state.pop("cover_letter_docx", None)
    st.session_state.pop("tailored_resume", None)
    st.session_state.pop("tailored_resume_pdf", None)
    st.session_state.pop("tailored_resume_docx", None)

# -----------------------------
# Results (persisted across reruns)
# -----------------------------
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
        components.score_dashboard(
            score=score,
            matching_count=len(analysis.get("matching_skills", [])),
            missing_count=len(analysis.get("missing_skills", []))
        )

        # -----------------------------
        # Why this score? (deterministic breakdown from ats_engine)
        # -----------------------------
        st.divider()
        components.why_score_card(ats_result)

        # -----------------------------
        # Section breakdown
        # -----------------------------
        if section_scores:
            st.divider()
            components.section_breakdown(section_scores)

        st.divider()

        # -----------------------------
        # Skills
        # -----------------------------
        left, right = st.columns(2)

        with left:
            components.skill_section(
                "Matching Skills",
                analysis.get("matching_skills", []),
                positive=True
            )

        with right:
            components.skill_section(
                "Missing Skills",
                analysis.get("missing_skills", []),
                positive=False
            )

        st.divider()

        # -----------------------------
        # Suggestions
        # -----------------------------
        components.suggestions_card(
            analysis.get("suggestions", [])
        )

        st.divider()

        # -----------------------------
        # Recruiter Verdict
        # -----------------------------
        components.verdict_card(
            analysis.get(
                "recruiter_verdict",
                "No recruiter verdict available."
            )
        )

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
                    cover_letter = generate_cover_letter(
                        st.session_state["resume_text"],
                        st.session_state["job_description"],
                    )
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
                    tailored_resume = generate_tailored_resume(
                        st.session_state["resume_text"],
                        st.session_state["job_description"],
                        analysis.get("missing_skills", []),
                    )
                    st.session_state["tailored_resume"] = tailored_resume
                    st.session_state["tailored_resume_pdf"] = doc_export.tailored_resume_to_pdf(tailored_resume)
                    st.session_state["tailored_resume_docx"] = doc_export.tailored_resume_to_docx(tailored_resume)
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