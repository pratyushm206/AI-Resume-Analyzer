import streamlit as st


def hero():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">
                📄 AI Resume Analyzer
            </div>

            <div class="hero-subtitle">
                AI-powered ATS Resume Screening Platform using
                <b>Sentence Transformers</b> and
                <b>Google Gemini</b>.
                Analyze resumes semantically, identify missing skills,
                receive recruiter insights, and improve your chances of
                landing interviews.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def score_dashboard(score, matching_count, missing_count):

    left, right = st.columns([2.2, 1])

    with left:

        st.markdown(
            f"""
            <div class="score-card">

                <div class="score-label">
                    ATS Match Score
                </div>

                <div class="score-number">
                    {score:.1f}%
                </div>

                <div class="progress">
                    <div
                        class="progress-fill"
                        style="width:{score}%;">
                    </div>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:

        st.markdown(
            f"""
            <div class="small-card">

                <div class="small-title">
                    Matching Skills
                </div>

                <div class="small-value green">
                    {matching_count}
                </div>

            </div>

            <div class="small-card">

                <div class="small-title">
                    Missing Skills
                </div>

                <div class="small-value red">
                    {missing_count}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


def skill_section(title, skills, positive=True):

    color = "badge-green" if positive else "badge-red"

    html = f"""
    <div class="section">

        <div class="card">

            <div class="card-title">
                {title}
            </div>
    """

    if skills:

        for skill in skills:
            html += f"""
            <span class="badge {color}">
                {skill}
            </span>
            """

    else:

        html += """
        <p>No data available.</p>
        """

    html += """
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def suggestions_card(suggestions):

    html = """
    <div class="section">

        <div class="card">

            <div class="card-title">
                💡 Suggestions
            </div>
    """

    if suggestions:

        for suggestion in suggestions:

            html += f"""
            <div class="suggestion">
                {suggestion}
            </div>
            """

    else:

        html += """
        <p>No suggestions available.</p>
        """

    html += """
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def verdict_card(verdict):

    st.markdown(
        f"""
        <div class="section">

            <div class="card">

                <div class="card-title">
                    👨‍💼 Recruiter Verdict
                </div>

                <div class="verdict">
                    {verdict}
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )