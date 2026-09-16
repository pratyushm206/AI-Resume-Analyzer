import base64
import html as html_lib
from pathlib import Path

import streamlit as st

_ASSET_DIR = Path(__file__).resolve().parent / "assets"
_LOGO_PATH = _ASSET_DIR / "logo.png"


def render_html(html: str):
    lines = [line.strip() for line in html.strip("\n").split("\n")]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


def _logo_data_uri():
    if not _LOGO_PATH.exists():
        return ""
    encoded = base64.b64encode(_LOGO_PATH.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _score_status(score):
    if score >= 75:
        return "Strong match"
    if score >= 45:
        return "Partial match"
    return "Weak match"


def _tier_class(score):
    if score > 70:
        return "fill-good"
    if score >= 40:
        return "fill-warn"
    return "fill-bad"


def score_gauge_html(score, label=None, note=None, display_value=None, preview=False):
    score = max(0.0, min(100.0, float(score or 0.0)))
    label = html_lib.escape(str(label or _score_status(score)))
    note = html_lib.escape(str(note or "Linear score gauge"))
    value_html = display_value if display_value is not None else f"{score:.1f}<span>%</span>"
    preview_class = " gauge-preview" if preview else ""
    return f"""
<div class="gauge-wrap{preview_class}" style="--score-pct:{score:.1f};">
    <svg viewBox="0 0 200 125" width="100%" style="max-width:230px; overflow:visible;">
        <path d="M15,115 A85,85 0 0 1 185,115" pathLength="100" fill="none" stroke="var(--line)" stroke-width="11" stroke-linecap="round"/>
        <path class="g-arc-fg" d="M15,115 A85,85 0 0 1 185,115" pathLength="100" fill="none" stroke="var(--brass)" stroke-width="11" stroke-linecap="round"/>
        <g stroke="var(--line-strong)" stroke-width="2">
            <line x1="15" y1="115" x2="5" y2="115"/>
            <line x1="39.9" y1="54.9" x2="32.8" y2="47.8"/>
            <line x1="100" y1="30" x2="100" y2="20"/>
            <line x1="160.1" y1="54.9" x2="167.2" y2="47.8"/>
            <line x1="185" y1="115" x2="195" y2="115"/>
        </g>
        <g fill="var(--ink-faint)" font-family="IBM Plex Mono, monospace" font-size="8">
            <text x="12" y="104" text-anchor="middle">0</text>
            <text x="36" y="45" text-anchor="middle">25</text>
            <text x="100" y="14" text-anchor="middle">50</text>
            <text x="164" y="45" text-anchor="middle">75</text>
            <text x="188" y="104" text-anchor="middle">100</text>
        </g>
        <line class="g-needle" x1="100" y1="115" x2="100" y2="38" stroke="var(--ink)" stroke-width="2.5"/>
        <circle cx="100" cy="115" r="5" fill="var(--ink)"/>
    </svg>
    <div class="g-num">{value_html}</div>
    <div class="g-tag">{label}</div>
    <div class="verdict-line">{note}</div>
</div>
"""


def hero():
    logo_src = _logo_data_uri()
    logo_html = (
        f'<img class="brand-logo" src="{logo_src}" alt="AI Resume Analyzer logo">'
        if logo_src
        else '<span class="mark-dot"></span>'
    )
    render_html(f"""
<div class="site-top">
    <div class="mark">
        {logo_html}
        <span class="brand-text">AI Resume Analyzer</span>
        <span class="mark-sub">/ scan engine</span>
    </div>
</div>
<section class="hero">
    <div>
        <h1 class="hero-h">A resume score you can actually explain.</h1>
        <p class="lede">Five weighted signals — <b>semantic relevance, skill match, keyword coverage, experience, and section strength</b> — combine into one deterministic number. Gemini writes prose around the result, never the score itself.</p>
        <div class="readouts">
            <div class="r"><div class="n">5</div><div class="l">signals scored</div></div>
            <div class="r"><div class="n">3</div><div class="l">export formats</div></div>
            <div class="r"><div class="n">0</div><div class="l">AI influence on score</div></div>
        </div>
    </div>
    <div class="gauge-card">
        {score_gauge_html(53.8, "Know your score", "Calculated from 5 weighted signals", display_value="?", preview=True)}
    </div>
</section>
""")


def workflow_strip():
    return None


def input_helper_panel():
    render_html("""
<div class="panel">
    <p class="side-title">Calibration notes</p>
    <p class="side-sub">What actually moves the score.</p>
    <ul class="cal-list">
        <li><span class="cal-idx">i</span><div><p class="cal-t">Use a text PDF</p><p class="cal-d">Export from Word, Docs, Canva, or LaTeX. A scanned image cannot be parsed for meaningful scoring.</p></div></li>
        <li><span class="cal-idx">ii</span><div><p class="cal-t">Paste the full JD</p><p class="cal-d">Responsibilities and requirements, not just the title, drive skill and keyword coverage.</p></div></li>
        <li><span class="cal-idx">iii</span><div><p class="cal-t">Include seniority</p><p class="cal-d">Years of experience and role level let the engine explain the experience component correctly.</p></div></li>
    </ul>
</div>
""")


def jd_quality_panel(stats: dict):
    words = int(stats.get("words", 0) or 0)
    if words >= 120:
        label, hint, on = "Detailed", "Enough context for a meaningful comparison.", 5
    elif words >= 40:
        label, hint, on = "Usable", "Add responsibilities or requirements for sharper results.", 3
    else:
        label, hint, on = "Needs detail", "Paste a fuller JD before analyzing.", 1
    ticks = "".join('<span class="on"></span>' if i < on else "<span></span>" for i in range(5))
    render_html(f"""
<div class="panel">
    <div class="signal-box" style="border-top:0; padding-top:0;">
        <div class="signal-row"><span class="lbl">Signal strength</span><span class="val">{label}</span></div>
        <div class="tickbar">{ticks}</div>
        <p class="signal-note"><b style="color:var(--ink-dim)">{words} words</b> extracted from the JD. {html_lib.escape(hint)}</p>
    </div>
</div>
""")


def analysis_overview(filename, resume_stats, jd_stats, match_label):
    analysis_hero(filename, resume_stats, jd_stats, match_label, 0, 0, 0)


def analysis_hero(filename, resume_stats, jd_stats, match_label, score, matching_count, missing_count):
    safe_filename = html_lib.escape(filename)
    resume_words = int(resume_stats.get("words", 0) or 0)
    jd_words = int(jd_stats.get("words", 0) or 0)
    read_time = int(resume_stats.get("estimated_read_minutes", 0) or 0)
    total = matching_count + missing_count
    render_html(f"""
<section class="analysis-hero">
    {score_gauge_html(score, match_label, safe_filename)}
    <div class="readout-grid">
        <div class="readout"><div class="n">{resume_words}</div><div class="l">resume words</div></div>
        <div class="readout"><div class="n">{jd_words}</div><div class="l">JD words</div></div>
        <div class="readout"><div class="n">{read_time} min</div><div class="l">read time</div></div>
        <div class="readout wide">
            <div><span class="n good" style="font-size:20px; display:inline;">{matching_count}</span> <span class="l" style="display:inline;">matching skills</span></div>
            <div><span class="n bad" style="font-size:20px; display:inline;">{missing_count}</span> <span class="l" style="display:inline;">missing skills</span></div>
            <div><span class="l">total considered: {total}</span></div>
        </div>
    </div>
</section>
""")


def score_dashboard(score, matching_count, missing_count):
    analysis_hero("Resume", {}, {}, _score_status(score), score, matching_count, missing_count)


def meter_row(label, score, weight=None):
    score = max(0.0, min(100.0, float(score or 0.0)))
    safe_label = html_lib.escape(str(label))
    weight_html = f'<span class="driver-weight">{int(weight * 100)}% weight</span>' if weight is not None else ""
    return f"""
<div class="driver">
    <div class="driver-top"><span class="driver-name">{safe_label}{weight_html}</span><span class="driver-val">{score:.1f}%</span></div>
    <div class="meter"><div class="fill {_tier_class(score)}" style="--pct:{score}%;"></div><div class="ticks"><span></span><span></span><span></span><span></span><span></span></div></div>
</div>
"""


_BREAKDOWN_LABELS = {
    "semantic_relevance": "Semantic Relevance",
    "skill_match": "Skill Match",
    "keyword_coverage": "Keyword Coverage",
    "experience_match": "Experience Match",
    "section_relevance": "Section Relevance",
}


def score_drivers(ats_result: dict):
    breakdown = ats_result.get("breakdown", {})
    weights = ats_result.get("weights", {})
    rows = "".join(
        meter_row(label, breakdown[key], weights.get(key, 0))
        for key, label in _BREAKDOWN_LABELS.items()
        if key in breakdown
    )
    boosters = "".join(
        f'<span class="skill-chip good">↑ {html_lib.escape(str(skill))}</span>'
        for skill in ats_result.get("score_boosters", [])
    ) or '<p class="card-empty">No matched requirements detected.</p>'
    blockers = "".join(
        f'<span class="skill-chip bad">↓ {html_lib.escape(str(skill))}</span>'
        for skill in ats_result.get("score_blockers", [])
    ) or '<p class="card-empty">No missing requirements detected.</p>'
    render_html(f"""
<div>
    {rows or '<p class="card-empty">No score-driver data available.</p>'}
    <div class="chiprow">
        <div class="chip-col"><h4>Score boosters</h4>{boosters}</div>
        <div class="chip-col"><h4>Score blockers</h4>{blockers}</div>
    </div>
</div>
""")


def why_score_card(ats_result: dict):
    score_drivers(ats_result)


def section_breakdown(section_scores: dict):
    rows = ""
    for name, score in (section_scores or {}).items():
        score = max(0.0, min(100.0, float(score or 0.0)))
        rows += f"""
<div class="sec-row">
    <span class="name">{html_lib.escape(str(name))}</span>
    <div class="meter"><div class="fill {_tier_class(score)}" style="--pct:{score}%;"></div><div class="ticks"><span></span><span></span><span></span><span></span><span></span></div></div>
    <span class="pct">{score:.0f}%</span>
</div>
"""
    render_html(rows or '<p class="card-empty">No section data available.</p>')


def verdict_card(verdict):
    safe_verdict = html_lib.escape(str(verdict or "No recruiter verdict available."))
    render_html(f"""
<div class="verdict-wrap">
    <div class="card-title">// recruiter verdict</div>
    <div class="verdict">{safe_verdict}</div>
</div>
""")


def suggestions_card(suggestions):
    rows = ""
    for i, suggestion in enumerate(suggestions or [], start=1):
        rows += f'<li><span class="si">{i:02d}</span><p>{html_lib.escape(str(suggestion))}</p></li>'
    if not rows:
        rows = '<li><span class="si">--</span><p>No suggestions available.</p></li>'
    render_html(f'<ul class="suggest-list">{rows}</ul>')


def skills_diff(matching_skills, missing_skills):
    html = '<div class="diff-grid">'
    html += _skill_column("Matching", matching_skills, True)
    html += _skill_column("Missing", missing_skills, False)
    html += "</div>"
    render_html(html)


def skill_section(title, skills, positive=True):
    render_html(_skill_column(title, skills, positive))


def _skill_column(title, skills, positive=True):
    marker = "✓" if positive else "x"
    col_class = "good" if positive else "bad"
    html = f'<div class="diff-col {col_class}"><h4>{html_lib.escape(title)} <span class="count">{len(skills or [])}</span></h4>'
    if skills:
        for skill in skills:
            html += f'<div class="diff-item"><span class="m">{marker}</span>{html_lib.escape(str(skill))}</div>'
    else:
        html += '<p class="card-empty">No data available.</p>'
    html += "</div>"
    return html


def sanity_note(matching_count, missing_count):
    total = matching_count + missing_count
    render_html(f'<p class="card-empty" style="margin-top:10px;">Sanity check: {matching_count} matching + {missing_count} missing = {total} total skills considered.</p>')


def format_checker_card(format_result: dict):
    score = float(format_result.get("format_score", 0.0) or 0.0)
    label = html_lib.escape(str(format_result.get("label") or "data unavailable"))
    rows = ""
    for item in format_result.get("checks", []):
        passed = bool(item.get("passed"))
        marker = "✓" if passed else "!"
        state = "pass" if passed else "warn"
        name = html_lib.escape(str(item.get("name") or "data unavailable"))
        explanation = html_lib.escape(str(item.get("explanation") or "data unavailable"))
        earned = html_lib.escape(str(item.get("earned", "data unavailable")))
        points = html_lib.escape(str(item.get("points", "data unavailable")))
        rows += f'<li><span class="mk {state}">{marker}</span><div><p class="ct">{name} <span class="card-empty">({earned}/{points})</span></p><p class="cd">{explanation}</p></div></li>'
    if not rows:
        rows = '<li><span class="mk warn">!</span><div><p class="ct">data unavailable</p><p class="cd">data unavailable</p></div></li>'
    render_html(f"""
<div>
    <div class="parse-score"><span class="l">{label}</span><span class="v">{score:.1f}%</span></div>
    <div class="meter"><div class="fill {_tier_class(score)}" style="--pct:{score}%;"></div><div class="ticks"><span></span><span></span><span></span><span></span><span></span></div></div>
    <ul class="check-list">{rows}</ul>
</div>
""")


def tailored_comparison_card(comparison: dict):
    before = comparison.get("before", {})
    after = comparison.get("after", {})
    delta = float(comparison.get("score_delta", 0.0) or 0.0)
    before_score = float(before.get("overall_score", 0.0) or 0.0)
    after_score = float(after.get("overall_score", 0.0) or 0.0)
    rows = ""
    for key, label in _BREAKDOWN_LABELS.items():
        value = comparison.get("component_deltas", {}).get(key, 0.0)
        rows += f'<div class="diff-item"><span class="m">{value:+.1f}</span>{html_lib.escape(label)}</div>'
    warnings = "".join(
        f'<div class="diff-item"><span class="m">!</span>{html_lib.escape(str(warning))}</div>'
        for warning in comparison.get("warnings", [])
    )
    render_html(f"""
<div class="section">
    <div class="comparison-grid">
        <div><span>Original</span><strong>{before_score:.1f}%</strong></div>
        <div><span>Tailored</span><strong>{after_score:.1f}%</strong></div>
        <div><span>Change</span><strong>{delta:+.1f}</strong></div>
    </div>
    <div class="diff-col good">{rows}</div>
    <div class="diff-col bad">{warnings}</div>
</div>
""")


def cover_letter_card(text: str):
    safe_text = html_lib.escape(text).replace("\n", "<br>")
    render_html(f'<div class="section"><div class="card-title">// cover letter</div><div class="cover-letter-text">{safe_text}</div></div>')


def tailored_resume_card(text: str):
    safe_text = html_lib.escape(text).replace("\n", "<br>")
    render_html(f'<div class="section"><div class="card-title">// tailored resume</div><div class="cover-letter-text">{safe_text}</div></div>')


def empty_state(message):
    render_html(f'<p class="card-empty">{html_lib.escape(message)}</p>')


def site_footer():
    logo_src = _logo_data_uri()
    logo_html = (
        f'<img class="footer-logo" src="{logo_src}" alt="AI Resume Analyzer logo">'
        if logo_src
        else '<span class="footer-logo-fallback"></span>'
    )
    render_html(f"""
<footer class="site-footer">
    <div class="footer-main">
        <div class="footer-brand">
            <div class="footer-brand-row">
                {logo_html}
                <span class="footer-name">AI Resume Analyzer</span>
            </div>
            <p>Deterministic scoring engine · Gemini used for prose only, never for the number.</p>
        </div>
        <nav class="footer-links" aria-label="Footer links">
            <p class="footer-label">Connect</p>
            <a href="mailto:pratyushm206@gmail.com">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M4 6h16v12H4z"/>
                    <path d="m4 7 8 6 8-6"/>
                </svg>
                <span>pratyushm206@gmail.com</span>
            </a>
            <a href="https://github.com/pratyushm206" target="_blank" rel="noopener noreferrer">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 2.8a9.2 9.2 0 0 0-2.9 17.9c.5.1.7-.2.7-.5v-1.9c-2.9.6-3.5-1.2-3.5-1.2-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.6 1.1 1.6 1.1.9 1.6 2.4 1.1 2.9.9.1-.7.4-1.1.7-1.4-2.3-.3-4.7-1.2-4.7-5.1 0-1.1.4-2.1 1.1-2.8-.1-.3-.5-1.3.1-2.8 0 0 .9-.3 2.9 1.1a9.8 9.8 0 0 1 5.2 0c2-1.4 2.9-1.1 2.9-1.1.6 1.5.2 2.5.1 2.8.7.7 1.1 1.7 1.1 2.8 0 4-2.4 4.8-4.7 5.1.4.3.8 1 .8 2v2.6c0 .3.2.6.8.5A9.2 9.2 0 0 0 12 2.8Z"/>
                </svg>
                <span>github.com/pratyushm206</span>
            </a>
            <a href="https://www.linkedin.com/in/pratyushm206" target="_blank" rel="noopener noreferrer">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M6.5 10v8"/>
                    <path d="M6.5 6.5v.1"/>
                    <path d="M11 18v-8"/>
                    <path d="M11 13.4c0-2.2 1.2-3.6 3.1-3.6 2 0 3.4 1.4 3.4 4V18"/>
                    <path d="M4 4h16v16H4z"/>
                </svg>
                <span>LinkedIn</span>
            </a>
            <a href="https://github.com/pratyushm206/AI-Resume-Analyzer" target="_blank" rel="noopener noreferrer">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M8 7H5a2 2 0 0 0-2 2v10h18V9a2 2 0 0 0-2-2h-3"/>
                    <path d="M8 7a4 4 0 0 1 8 0"/>
                    <path d="M9 13h6"/>
                </svg>
                <span>View source</span>
            </a>
        </nav>
    </div>
    <div class="footer-bottom">
        <p>© 2026 Designed &amp; coded by <strong>Pratyush Mishra</strong></p>
    </div>
</footer>
""")
