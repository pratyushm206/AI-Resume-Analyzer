import streamlit as st
import fitz

from ai_engine import calculate_match_score
from gemini_engine import analyze_resume_with_gemini

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")

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

        score = calculate_match_score(
            resume_text,
            job_description
        )

        analysis = analyze_resume_with_gemini(
            resume_text,
            job_description
        )

    st.success("Analysis Complete")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "🎯 Match Score",
            f"{score}%"
        )

    with c2:
        st.metric(
            "📊 Matching Skills",
            len(analysis["matching_skills"])
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("✅ Matching Skills")

        for skill in analysis["matching_skills"]:
            st.success(skill)

    with right:

        st.subheader("❌ Missing Skills")

        for skill in analysis["missing_skills"]:
            st.error(skill)

    st.divider()

    st.subheader("💡 Suggestions")

    for suggestion in analysis["suggestions"]:
        st.info(suggestion)