import streamlit as st
import fitz

from ai_engine import calculate_match_score
from gemini_engine import analyze_resume_with_gemini

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

    st.toast("Analysis completed successfully!", icon="✅")

    # -----------------------------
    # Dashboard
    # -----------------------------
    components.score_dashboard(
        score=score,
        matching_count=len(analysis.get("matching_skills", [])),
        missing_count=len(analysis.get("missing_skills", []))
    )

    st.divider()

    # -----------------------------
    # Skills
    # -----------------------------
    left, right = st.columns(2)

    with left:
        components.skill_section(
            "✅ Matching Skills",
            analysis.get("matching_skills", []),
            positive=True
        )

    with right:
        components.skill_section(
            "❌ Missing Skills",
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