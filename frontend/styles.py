def load_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

:root{
    --bg:#0d0d0f;
    --surface:#17171b;
    --surface-raised:#1e1e23;
    --border:#2b2b30;
    --border-soft:#212126;
    --text:#f3f1ec;
    --text-muted:#8d8b86;
    --text-dim:#504f4b;

    --accent:#c9a34a;
    --accent-soft:rgba(201,163,74,.10);

    --info:#7c93a6;
    --info-bg:rgba(124,147,166,.10);

    --success:#5fae86;
    --success-bg:rgba(95,174,134,.10);

    --danger:#c26b63;
    --danger-bg:rgba(194,107,99,.10);

    --mono:'JetBrains Mono', monospace;
    --sans:'Inter', sans-serif;
}

/* ===========================
   GLOBAL
=========================== */

html, body, .stApp, [data-testid="stAppViewContainer"]{
    font-family: var(--sans);
    color: var(--text);
}

.stApp{
    background: var(--bg);
}

/* Streamlit's default top gradient bar doesn't belong to this palette */
div[data-testid="stDecoration"]{
    display: none;
}

.block-container{
    max-width: 1180px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

#MainMenu, footer, header{
    visibility: hidden;
}

::selection{
    background: var(--accent);
    color: #14140f;
}

/* ===========================
   STREAMLIT NATIVE WIDGETS
=========================== */

[data-testid="stWidgetLabel"] p{
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: var(--text-muted);
    font-weight: 600;
}

[data-testid="stFileUploaderDropzone"]{
    background: var(--surface);
    border: 1.5px dashed var(--border);
    border-radius: 14px;
    transition: border-color .2s ease;
}
[data-testid="stFileUploaderDropzone"]:hover{
    border-color: var(--text-muted);
}
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] p{
    color: var(--text) !important;
}
[data-testid="stFileUploaderDropzone"] small{
    color: var(--text-muted) !important;
}
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stBaseButton-secondary"]{
    background: var(--surface-raised) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: var(--sans) !important;
}
[data-testid="stFileUploaderFile"]{
    background: var(--surface);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    color: var(--text);
}

.stTextArea textarea{
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    font-family: var(--mono) !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}
.stTextArea textarea:focus{
    border-color: var(--text-muted) !important;
    box-shadow: 0 0 0 1px var(--text-muted) !important;
}

div[data-testid="stButton"] button{
    background: var(--text) !important;
    color: #14140f !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: var(--mono) !important;
    font-weight: 700 !important;
    letter-spacing: .04em !important;
    padding: 14px 0 !important;
    box-shadow: 0 1px 0 rgba(255,255,255,.06) inset, 0 14px 30px rgba(0,0,0,.35) !important;
    transition: transform .15s ease, background .15s ease !important;
}
div[data-testid="stButton"] button:hover{
    background: #ffffff !important;
    transform: translateY(-1px);
}
div[data-testid="stButton"] button p{
    color: #14140f !important;
    font-family: var(--mono) !important;
    font-weight: 700 !important;
}

[data-testid="stAlert"]{
    background: var(--info-bg) !important;
    border: 1px solid rgba(124,147,166,.25) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}

hr, [data-testid="stDivider"]{
    border-color: var(--border) !important;
}

/* ===========================
   HERO
=========================== */

.hero{
    position: relative;
    background: var(--surface);
    background-image: repeating-linear-gradient(
        135deg,
        rgba(255,255,255,.015) 0px,
        rgba(255,255,255,.015) 1px,
        transparent 1px,
        transparent 34px
    );
    border: 1px solid var(--border-soft);
    border-radius: 20px;
    padding: 44px 46px;
    margin-bottom: 34px;
}

.hero-eyebrow{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .12em;
    color: var(--text-muted);
    padding: 0 0 16px 0;
    margin-bottom: 18px;
    border-bottom: 1px solid var(--border);
}

.hero-eyebrow::before{
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    display: inline-block;
}

.hero-title{
    font-family: var(--sans);
    font-size: 40px;
    font-weight: 800;
    letter-spacing: -.02em;
    color: var(--text);
    margin-bottom: 14px;
}

.hero-subtitle{
    font-size: 15.5px;
    color: var(--text-muted);
    line-height: 1.85;
    max-width: 640px;
}

.hero-subtitle strong{
    color: var(--text);
    font-weight: 600;
}

/* ===========================
   SCORE GAUGE
=========================== */

.score-card{
    background: var(--surface);
    border: 1px solid var(--border-soft);
    border-radius: 20px;
    padding: 32px;
    display: flex;
    align-items: center;
    gap: 30px;
}

.score-label{
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .1em;
    color: var(--text-muted);
    text-transform: uppercase;
}

.gauge-wrap{
    flex-shrink: 0;
}

/* Mirrored horizontally so the conic-gradient (which only draws
   clockwise) reads as filling counter-clockwise from 12 o'clock. */
.gauge-ring{
    width: 148px;
    height: 148px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transform: scaleX(-1);
}

.gauge-inner{
    width: 118px;
    height: 118px;
    border-radius: 50%;
    background: var(--surface);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    transform: scaleX(-1); /* cancels parent mirror so text reads normally */
}

.gauge-number{
    font-family: var(--mono);
    font-size: 27px;
    font-weight: 700;
    color: var(--text);
}

.gauge-percent{
    font-size: 15px;
    color: var(--text-muted);
}

.score-status{
    display: inline-block;
    font-family: var(--mono);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .08em;
    padding: 5px 12px;
    border-radius: 6px;
    margin-top: 10px;
}

.status-strong{ background: var(--success-bg); color: var(--success); }
.status-partial{ background: var(--info-bg); color: var(--info); }
.status-weak{ background: var(--danger-bg); color: var(--danger); }

/* ===========================
   SMALL CARDS
=========================== */

.small-card{
    background: var(--surface);
    border: 1px solid var(--border-soft);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.small-title{
    font-family: var(--mono);
    color: var(--text-muted);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: .08em;
}

.small-value{
    font-family: var(--mono);
    font-size: 30px;
    font-weight: 700;
}

.green{ color: var(--success); }
.red{ color: var(--danger); }

/* ===========================
   SECTION / CARD SHELL
=========================== */

.section{
    margin-top: 28px;
}

.card{
    background: var(--surface);
    border: 1px solid var(--border-soft);
    border-radius: 18px;
    padding: 26px 28px;
}

.card-title{
    font-family: var(--mono);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--text);
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-title .tag-bracket{
    font-family: var(--mono);
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 11px;
}
.tag-bracket.ok{ background: var(--success-bg); color: var(--success); }
.tag-bracket.miss{ background: var(--danger-bg); color: var(--danger); }
.tag-bracket.tip{ background: var(--info-bg); color: var(--info); }
.tag-bracket.verdict{ background: var(--accent-soft); color: var(--accent); }

.card-empty{
    color: var(--text-dim);
    font-size: 14px;
    font-style: italic;
}

/* ===========================
   DIFF-STYLE SKILL ROWS
=========================== */

.diff-row{
    display: flex;
    align-items: baseline;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 6px;
    font-family: var(--mono);
    font-size: 13.5px;
}

.diff-row.plus{
    background: var(--success-bg);
    border-left: 2px solid var(--success);
}
.diff-row.minus{
    background: var(--danger-bg);
    border-left: 2px solid var(--danger);
}

.diff-marker{
    font-weight: 700;
    flex-shrink: 0;
}
.diff-row.plus .diff-marker{ color: var(--success); }
.diff-row.minus .diff-marker{ color: var(--danger); }

.diff-text{
    color: var(--text);
}

/* ===========================
   SUGGESTIONS (LOG STYLE)
=========================== */

.log-line{
    display: flex;
    gap: 14px;
    padding: 13px 16px;
    background: var(--surface-raised);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    margin-bottom: 10px;
}

.log-index{
    font-family: var(--mono);
    color: var(--info);
    font-weight: 700;
    font-size: 13px;
    flex-shrink: 0;
}

.log-text{
    color: var(--text);
    font-size: 14.5px;
    line-height: 1.65;
}

/* ===========================
   VERDICT
=========================== */

.verdict-wrap{
    position: relative;
    padding-left: 18px;
    border-left: 2px solid var(--accent);
}

.verdict{
    font-size: 15px;
    line-height: 1.85;
    color: var(--text-muted);
}

</style>
"""