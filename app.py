import streamlit as st
import fitz

from ai_engine import calculate_match_score
from gemini_engine import analyze_resume_with_gemini
from cover_letter_engine import generate_cover_letter
from resume_tailor_engine import generate_tailored_resume
from resume_sections import split_resume_sections, score_sections
from report_generator import generate_pdf_report

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

        score = float(
            calculate_match_score(
                resume_text,
                job_description
            )
        )

        score = max(0.0, min(100.0, score))

        analysis = analyze_resume_with_gemini(
            resume_text,
            job_description
        )

        sections = split_resume_sections(resume_text)
        section_scores = score_sections(sections, job_description)

    st.toast("Analysis completed successfully!", icon="✅")

    # Persisted in session_state because the PDF-download and
    # cover-letter buttons below trigger their own Streamlit reruns,
    # which would otherwise wipe out these results since they only
    # exist inside this "Analyze Resume" click block.
    st.session_state["resume_text"] = resume_text
    st.session_state["resume_filename"] = uploaded_file.name
    st.session_state["job_description"] = job_description
    st.session_state["score"] = score
    st.session_state["analysis"] = analysis
    st.session_state["section_scores"] = section_scores
    st.session_state.pop("cover_letter", None)
    st.session_state.pop("tailored_resume", None)

# -----------------------------
# Results (persisted across reruns)
# -----------------------------
if "analysis" in st.session_state:

    score = st.session_state["score"]
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
        pdf_bytes = generate_pdf_report(
            resume_filename=st.session_state.get("resume_filename", "resume.pdf"),
            score=score,
            matching_skills=analysis.get("matching_skills", []),
            missing_skills=analysis.get("missing_skills", []),
            suggestions=analysis.get("suggestions", []),
            verdict=analysis.get("recruiter_verdict", ""),
            section_scores=section_scores,
        )

        st.download_button(
            "⬇️ Download PDF Report",
            data=pdf_bytes,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with action_mid:
        if st.button("✉️ Generate Cover Letter", use_container_width=True):
            with st.spinner("Writing cover letter..."):
                st.session_state["cover_letter"] = generate_cover_letter(
                    st.session_state["resume_text"],
                    st.session_state["job_description"],
                )

    with action_right:
        if st.button("📝 Modify Resume for JD", use_container_width=True):
            with st.spinner("Tailoring resume to this job description..."):
                st.session_state["tailored_resume"] = generate_tailored_resume(
                    st.session_state["resume_text"],
                    st.session_state["job_description"],
                    analysis.get("missing_skills", []),
                )

    if "cover_letter" in st.session_state:
        st.divider()
        components.cover_letter_card(st.session_state["cover_letter"])
        st.download_button(
            "⬇️ Download Cover Letter (.txt)",
            data=st.session_state["cover_letter"],
            file_name="cover_letter.txt",
            mime="text/plain",
        )

    if "tailored_resume" in st.session_state:
        st.divider()
        components.tailored_resume_card(st.session_state["tailored_resume"])
        st.download_button(
            "⬇️ Download Tailored Resume (.txt)",
            data=st.session_state["tailored_resume"],
            file_name="tailored_resume.txt",
            mime="text/plain",
        )