import html as html_lib

import streamlit as st


def render_html(html: str):
    """
    Strip leading whitespace from every line before passing to st.markdown.

    Streamlit's markdown renderer treats any line indented 4+ spaces as a
    code block. textwrap.dedent() only removes whitespace that's common to
    ALL lines, so if outer tags sit at column 0 while nested tags are
    indented, dedent() does nothing and the nested HTML renders as raw text.
    Stripping per-line avoids that entirely.
    """
    lines = [line.strip() for line in html.strip("\n").split("\n")]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


def hero():
    render_html("""
<div class="hero">
    <span class="hero-eyebrow">// ATS_SCAN_ENGINE</span>
    <div class="hero-title">
        AI Resume Analyzer
    </div>
    <div class="hero-subtitle">
        AI-powered ATS resume screening using
        <strong>Sentence Transformers</strong> and
        <strong>Google Gemini</strong>.
        Upload your resume, drop in a job description, and get a match
        score, a skill-level diff, and recruiter-style feedback &mdash;
        the way an ATS actually reads you.
    </div>
</div>
""")


def _score_status(score):
    if score >= 75:
        return "STRONG MATCH", "status-strong"
    if score >= 45:
        return "PARTIAL MATCH", "status-partial"
    return "WEAK MATCH", "status-weak"


def score_dashboard(score, matching_count, missing_count):

    left, right = st.columns([2.2, 1])

    with left:
        status_label, status_class = _score_status(score)
        deg = max(0.0, min(100.0, score)) * 3.6

        render_html(f"""
<div class="score-card">
    <div class="gauge-wrap">
        <div class="gauge-ring" style="background: conic-gradient(var(--accent) {deg}deg, var(--border) 0deg);">
            <div class="gauge-inner">
                <div class="gauge-number">{score:.1f}<span class="gauge-percent">%</span></div>
            </div>
        </div>
    </div>
    <div>
        <div class="score-label">ATS MATCH SCORE</div>
        <div class="score-status {status_class}">{status_label}</div>
    </div>
</div>
""")

    with right:
        render_html(f"""
<div class="small-card">
    <div class="small-title">Matching</div>
    <div class="small-value green">{matching_count}</div>
</div>
<div class="small-card">
    <div class="small-title">Missing</div>
    <div class="small-value red">{missing_count}</div>
</div>
""")


def skill_section(title, skills, positive=True):

    marker = "+" if positive else "-"
    row_class = "plus" if positive else "minus"
    tag_class = "ok" if positive else "miss"
    title_class = "tag-ok" if positive else "tag-miss"
    bracket_label = "OK" if positive else "MISS"

    html = f"""
<div class="section">
    <div class="card">
        <div class="card-title {title_class}">
            <span class="tag-bracket {tag_class}">{bracket_label}</span>
            {title}
        </div>
"""

    if skills:
        for skill in skills:
            html += f"""
        <div class="diff-row {row_class}">
            <span class="diff-marker">{marker}</span>
            <span class="diff-text">{skill}</span>
        </div>
"""
    else:
        html += """
        <p class="card-empty">No data available.</p>
"""

    html += """
    </div>
</div>
"""

    render_html(html)


def suggestions_card(suggestions):

    html = """
<div class="section">
    <div class="card">
        <div class="card-title tag-tip">
            <span class="tag-bracket tip">TIP</span>
            Suggestions
        </div>
"""

    if suggestions:
        for i, suggestion in enumerate(suggestions, start=1):
            html += f"""
        <div class="log-line">
            <span class="log-index">{i:02d}</span>
            <span class="log-text">{suggestion}</span>
        </div>
"""
    else:
        html += """
        <p class="card-empty">No suggestions available.</p>
"""

    html += """
    </div>
</div>
"""

    render_html(html)


def section_breakdown(section_scores: dict):

    if not section_scores:
        return

    rows = ""

    for name, score in section_scores.items():
        _, status_class = _score_status(score)
        rows += f"""
        <div class="section-bar-row">
            <div class="section-bar-top">
                <span class="section-bar-label">{name}</span>
                <span class="section-bar-value">{score:.0f}%</span>
            </div>
            <div class="section-bar-track">
                <div class="section-bar-fill {status_class}" style="width:{score}%;"></div>
            </div>
        </div>
"""

    html = f"""
<div class="section">
    <div class="card">
        <div class="card-title">
            <span class="tag-bracket tip">SECTIONS</span>
            Section Breakdown
        </div>
        {rows}
    </div>
</div>
"""

    render_html(html)


def cover_letter_card(text: str):

    safe_text = html_lib.escape(text).replace("\n", "<br>")

    render_html(f"""
<div class="section">
    <div class="card">
        <div class="card-title tag-verdict">
            <span class="tag-bracket verdict">LETTER</span>
            Cover Letter
        </div>
        <div class="cover-letter-text">
            {safe_text}
        </div>
    </div>
</div>
""")


def tailored_resume_card(text: str):

    safe_text = html_lib.escape(text).replace("\n", "<br>")

    render_html(f"""
<div class="section">
    <div class="card">
        <div class="card-title tag-verdict">
            <span class="tag-bracket verdict">TAILORED</span>
            Resume Rewritten for This JD
        </div>
        <div class="cover-letter-text">
            {safe_text}
        </div>
    </div>
</div>
""")


def verdict_card(verdict):
    render_html(f"""
<div class="section">
    <div class="card">
        <div class="card-title tag-verdict">
            <span class="tag-bracket verdict">VERDICT</span>
            Recruiter Verdict
        </div>
        <div class="verdict-wrap">
            <div class="verdict">
                {verdict}
            </div>
        </div>
    </div>
</div>
""")