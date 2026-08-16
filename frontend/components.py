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


_BREAKDOWN_LABELS = {
    "semantic_relevance": "Semantic Relevance",
    "skill_match": "Skill Match",
    "keyword_coverage": "Keyword Coverage",
    "experience_match": "Experience Match",
    "section_relevance": "Section Relevance",
}


def why_score_card(ats_result: dict):
    """
    Explainable breakdown behind the overall ATS score: the weighted
    component scores, the top skills driving the score up/down, and
    (when the JD specifies one) the required-vs-candidate experience gap.

    Expects the dict shape returned by ats_engine.analyze_ats_match().
    """

    breakdown = ats_result.get("breakdown", {})
    weights = ats_result.get("weights", {})

    rows = ""
    for key, label in _BREAKDOWN_LABELS.items():
        if key not in breakdown:
            continue
        score = breakdown[key]
        weight_pct = int(weights.get(key, 0) * 100)
        _, status_class = _score_status(score)
        rows += f"""
        <div class="section-bar-row">
            <div class="section-bar-top">
                <span class="section-bar-label">{label} <span class="card-empty">({weight_pct}% weight)</span></span>
                <span class="section-bar-value">{score:.1f}%</span>
            </div>
            <div class="section-bar-track">
                <div class="section-bar-fill {status_class}" style="width:{score}%;"></div>
            </div>
        </div>
"""

    boosters = ats_result.get("score_boosters", [])
    blockers = ats_result.get("score_blockers", [])

    boosters_html = ""
    if boosters:
        for skill in boosters:
            boosters_html += f"""
        <div class="diff-row plus">
            <span class="diff-marker">+</span>
            <span class="diff-text">{skill}</span>
        </div>
"""
    else:
        boosters_html = """<p class="card-empty">No matched requirements detected.</p>"""

    blockers_html = ""
    if blockers:
        for skill in blockers:
            blockers_html += f"""
        <div class="diff-row minus">
            <span class="diff-marker">-</span>
            <span class="diff-text">{skill}</span>
        </div>
"""
    else:
        blockers_html = """<p class="card-empty">No missing requirements detected.</p>"""

    experience = ats_result.get("experience", {})
    required_years = experience.get("required_years")
    candidate_years = experience.get("candidate_years")

    experience_line = ""
    if required_years is not None:
        candidate_display = (
            f"{candidate_years:.0f} years found on resume"
            if candidate_years is not None
            else "no explicit years-of-experience figure found on resume"
        )
        experience_line = f"""
        <p class="card-empty" style="margin-top:14px;">
            JD requires {required_years:.0f}+ years of experience &mdash; {candidate_display}.
        </p>
"""

    render_html(f"""
<div class="section">
    <div class="card">
        <div class="card-title">
            <span class="tag-bracket tip">SCORE</span>
            Why This Score?
        </div>
        {rows}
        {experience_line}
    </div>
</div>
<div class="section">
    <div style="display:flex; gap:24px; flex-wrap:wrap;">
        <div class="card" style="flex:1; min-width:260px;">
            <div class="card-title tag-ok">
                <span class="tag-bracket ok">OK</span>
                Score Boosters
            </div>
            {boosters_html}
        </div>
        <div class="card" style="flex:1; min-width:260px;">
            <div class="card-title tag-miss">
                <span class="tag-bracket miss">MISS</span>
                Score Blockers
            </div>
            {blockers_html}
        </div>
    </div>
</div>
""")


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