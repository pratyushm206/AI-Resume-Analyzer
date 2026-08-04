import streamlit as st
import fitz

from ai_engine import calculate_match_score
from gemini_engine import analyze_resume_with_gemini

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.markdown(
    """
# 📄 AI Resume Analyzer

### AI-powered ATS Resume Screening System

Upload a resume, compare it against a job description, and receive an AI-powered recruiter analysis.

---
"""
)

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button("Analyze Resume"):

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

    score_col, stats_col = st.columns([2, 1])

    with score_col:

        st.subheader("🎯 ATS Match Score")

        st.metric(
        label="Overall Match",
        value=f"{score:.1f}%"
    )

    st.progress(score / 100)

    with stats_col:

        st.subheader("📊 Summary")

        st.metric(
            "Matching Skills",
            len(analysis.get("matching_skills", []))
        )

        st.metric(
            "Missing Skills",
            len(analysis.get("missing_skills", []))
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("✅ Matching Skills")

        matching_skills = analysis.get("matching_skills", [])

        if matching_skills:
            for skill in matching_skills:
                st.success(skill)
        else:
            st.info("No matching skills found.")

    with right:

        st.subheader("❌ Missing Skills")

        missing_skills = analysis.get("missing_skills", [])

        if missing_skills:
            for skill in missing_skills:
                st.error(skill)
        else:
            st.info("No missing skills identified.")

    st.divider()

    st.subheader("💡 Suggestions")

    suggestions = analysis.get("suggestions", [])

    if suggestions:
        for suggestion in suggestions:
            st.info(suggestion)
    else:
        st.info("No suggestions available.")

    st.divider()

    st.subheader("👨‍💼 Recruiter Verdict")

    st.markdown(
        f"""
> {analysis.get("recruiter_verdict", "No recruiter verdict available.")}
"""
    )