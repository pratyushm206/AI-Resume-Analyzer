def load_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root{
    --bg:#0d0c0a;
    --bg-raised:#151310;
    --bg-card:#1a1712;
    --line:rgba(237,229,210,0.10);
    --line-strong:rgba(237,229,210,0.20);
    --ink:#f3ede0;
    --ink-dim:#a89d86;
    --ink-faint:#6e6555;
    --brass:#c99a4e;
    --brass-bright:#e2b568;
    --brass-tint:rgba(201,154,78,0.12);
    --good:#8caa74;
    --good-tint:rgba(140,170,116,0.14);
    --bad:#b56a52;
    --bad-tint:rgba(181,106,82,0.14);
    --shadow:0 1px 0 rgba(255,244,222,.05) inset, 0 14px 30px -16px rgba(0,0,0,.65), 0 2px 8px rgba(0,0,0,.4);
    --radius-s:4px;
    --radius-m:10px;
    --display:'Fraunces', serif;
    --sans:'IBM Plex Sans', sans-serif;
    --mono:'IBM Plex Mono', monospace;
}

html, body, .stApp, [data-testid="stAppViewContainer"]{
    font-family:var(--sans);
    color:var(--ink);
}

.stApp{
    background:
        radial-gradient(ellipse 900px 500px at 85% -10%, rgba(201,154,78,.07), transparent 60%),
        repeating-linear-gradient(0deg, rgba(237,229,210,.018) 0px, rgba(237,229,210,.018) 1px, transparent 1px, transparent 48px),
        repeating-linear-gradient(90deg, rgba(237,229,210,.018) 0px, rgba(237,229,210,.018) 1px, transparent 1px, transparent 48px),
        var(--bg);
}

div[data-testid="stDecoration"], #MainMenu, footer, header{ display:none; }
.block-container{
    max-width:1180px;
    padding-top:3.5rem;
    padding-bottom:4rem;
}
::selection{ background:var(--brass-tint); color:var(--brass-bright); }

[data-testid="stWidgetLabel"] p{
    font-family:var(--mono);
    font-size:12.5px;
    color:var(--ink-faint);
    letter-spacing:0;
}

[data-testid="stFileUploaderDropzone"]{
    background:var(--bg-card);
    border:1px dashed var(--line-strong);
    border-radius:var(--radius-s);
    padding:18px 16px;
    transition:border-color .18s ease, background .18s ease, box-shadow .18s ease;
}
[data-testid="stFileUploaderDropzone"]:hover{
    border-color:var(--brass);
    background:var(--brass-tint);
    box-shadow:var(--shadow);
}
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] p{ color:var(--ink) !important; }
[data-testid="stFileUploaderDropzone"] small{ color:var(--ink-faint) !important; }
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stBaseButton-secondary"]{
    background:transparent !important;
    color:var(--ink) !important;
    border:1px solid var(--line-strong) !important;
    border-radius:var(--radius-s) !important;
    font-family:var(--sans) !important;
    font-weight:500 !important;
}
[data-testid="stFileUploaderFile"]{
    background:var(--bg-raised);
    border:1px solid var(--line);
    border-radius:var(--radius-s);
    color:var(--ink);
}

.stTextArea textarea{
    background:var(--bg-card) !important;
    color:var(--ink) !important;
    border:1px solid var(--line) !important;
    border-radius:var(--radius-s) !important;
    font-family:var(--mono) !important;
    font-size:13.5px !important;
    line-height:1.7 !important;
}
.stTextArea textarea:focus{
    border-color:var(--brass) !important;
    box-shadow:0 0 0 1px var(--brass) !important;
}

[data-testid="stRadio"] [role="radiogroup"]{
    display:inline-flex;
    gap:0;
    border:1px solid var(--line-strong);
    border-radius:var(--radius-s);
    overflow:hidden;
    width:max-content;
}
[data-testid="stRadio"] label{
    padding:8px 16px;
    margin:0 !important;
    border-left:1px solid var(--line-strong);
}
[data-testid="stRadio"] label:first-child{ border-left:0; }
[data-testid="stRadio"] p{ color:var(--ink-dim) !important; font-size:13.5px; }

div[data-testid="stButton"] button{
    border-radius:var(--radius-s) !important;
    font-family:var(--sans) !important;
    font-weight:600 !important;
    font-size:14.5px !important;
    padding:13px 20px !important;
    transition:transform .15s ease, box-shadow .15s ease, border-color .15s ease, color .15s ease !important;
}
div[data-testid="stButton"] button[kind="primary"],
div[data-testid="stButton"]:first-of-type button{
    background:linear-gradient(180deg, var(--brass-bright), var(--brass)) !important;
    color:#1a1204 !important;
    border:0 !important;
    box-shadow:0 1px 0 rgba(255,255,255,.3) inset, 0 8px 18px -8px rgba(201,154,78,.55) !important;
}
div[data-testid="stButton"] button:hover{ transform:translateY(-1px); }
div[data-testid="stButton"] button p{ font-family:var(--sans) !important; font-weight:600 !important; }
div[data-testid="stDownloadButton"] button{
    background:transparent !important;
    color:var(--ink-dim) !important;
    border:1px solid var(--line-strong) !important;
    border-radius:var(--radius-s) !important;
    font-family:var(--sans) !important;
    font-weight:600 !important;
}
div[data-testid="stDownloadButton"] button:hover{
    color:var(--brass-bright) !important;
    border-color:var(--brass) !important;
}

[data-testid="stAlert"]{
    background:var(--brass-tint) !important;
    border:1px solid rgba(201,154,78,.35) !important;
    border-radius:var(--radius-s) !important;
    color:var(--ink) !important;
}
hr, [data-testid="stDivider"]{ border-color:var(--line) !important; }

.site-top{
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 0 22px;
    border-bottom:1px solid var(--line);
}
.mark{
    display:flex;
    align-items:center;
    gap:.68em;
    font-weight:600;
    font-size:15px;
    min-width:0;
}
.brand-logo{
    width:auto;
    height:2.85em;
    max-width:2.85em;
    aspect-ratio:1 / 1;
    object-fit:contain;
    flex:0 0 auto;
    border-radius:50%;
    box-shadow:0 0 0 1px var(--line), 0 8px 18px -12px rgba(201,154,78,.75);
}
.brand-text{
    color:var(--ink);
    font-weight:600;
    line-height:1;
    white-space:nowrap;
}
.mark-dot{
    width:9px;
    height:9px;
    border-radius:2px;
    background:var(--brass);
    transform:rotate(45deg);
    box-shadow:0 0 0 3px var(--brass-tint);
}
.mark-sub{ color:var(--ink-faint); font-size:12px; font-family:var(--mono); }

.hero{
    padding:64px 0 54px;
    display:grid;
    grid-template-columns:1.15fr .85fr;
    gap:56px;
    align-items:center;
}
.hero-h{
    font-family:var(--display);
    font-weight:600;
    font-size:clamp(34px,4.6vw,54px);
    line-height:1.08;
    letter-spacing:0;
    margin:0 0 22px;
}
.hero p.lede{
    color:var(--ink-dim);
    font-size:17px;
    max-width:52ch;
    margin:0 0 30px;
}
.hero p.lede b{ color:var(--ink); font-weight:600; }
.readouts{ display:flex; border-top:1px solid var(--line); padding-top:18px; }
.readouts .r{ flex:1; padding:0 22px; border-left:1px solid var(--line); }
.readouts .r:first-child{ border-left:0; padding-left:0; }
.readouts .n{ font-family:var(--display); font-size:26px; color:var(--brass-bright); font-weight:600; }
.readouts .l{ font-size:12.5px; color:var(--ink-faint); margin-top:2px; }

.panel{
    background:var(--bg-card);
    border:1px solid var(--line);
    border-radius:var(--radius-m);
    box-shadow:var(--shadow);
    padding:30px;
}
.panel-grid{ display:grid; grid-template-columns:1.5fr .95fr; gap:26px; padding-bottom:42px; }
.side-title{ font-size:15px; font-weight:600; margin:0 0 4px; }
.side-sub{ font-size:13px; color:var(--ink-faint); margin:0 0 20px; }
.cal-list{ list-style:none; margin:0 0 26px; padding:0; }
.cal-list li{ padding:16px 0; border-top:1px solid var(--line); display:flex; gap:14px; }
.cal-list li:first-child{ border-top:0; padding-top:0; }
.cal-idx{ font-family:var(--mono); font-size:12px; color:var(--brass); flex-shrink:0; padding-top:2px; }
.cal-t{ font-size:14px; font-weight:500; margin:0 0 4px; }
.cal-d{ font-size:13px; color:var(--ink-faint); margin:0; line-height:1.55; }
.signal-box{ border-top:1px solid var(--line); padding-top:22px; }
.signal-row{ display:flex; align-items:baseline; justify-content:space-between; margin-bottom:10px; }
.signal-row .lbl{ font-size:13px; color:var(--ink-faint); }
.signal-row .val{ font-family:var(--display); color:var(--good); font-weight:600; font-size:15px; }
.tickbar{ height:6px; background:var(--bg-raised); border-radius:3px; overflow:hidden; display:flex; gap:2px; padding:1px; }
.tickbar span{ flex:1; background:var(--line); }
.tickbar span.on{ background:var(--good); }
.signal-note{ font-size:12.5px; color:var(--ink-faint); margin-top:10px; line-height:1.6; }

.analysis-hero{
    display:grid;
    grid-template-columns:.8fr 1.2fr;
    gap:44px;
    align-items:center;
    padding:42px 0 38px;
    border-bottom:1px solid var(--line);
}
.gauge-card{ background:var(--bg-card); border:1px solid var(--line); border-radius:var(--radius-m); box-shadow:var(--shadow); padding:26px 26px 20px; text-align:center; }
.gauge-wrap{ text-align:center; }
.g-num{ font-family:var(--display); font-size:52px; font-weight:600; margin-top:-52px; }
.g-num span{ font-size:22px; }
.g-tag{
    display:inline-block;
    margin-top:8px;
    font-size:12px;
    letter-spacing:.04em;
    padding:4px 12px;
    border-radius:20px;
    background:var(--brass-tint);
    color:var(--brass-bright);
    border:1px solid rgba(201,154,78,.35);
}
.verdict-line{ font-size:13.5px; color:var(--ink-faint); margin-top:14px; }
.g-arc-fg{
    stroke-dasharray:100;
    stroke-dashoffset:calc(100 - var(--score-pct));
    animation:gaugeArc 1.15s cubic-bezier(.22,.9,.3,1) both;
}
.g-needle{
    transform-origin:100px 115px;
    transform:rotate(calc(-90deg + (var(--score-pct) * 1.8deg)));
    animation:gaugeNeedle 1.15s cubic-bezier(.22,.9,.3,1) both;
}
@keyframes gaugeArc{ from{ stroke-dashoffset:100; } }
@keyframes gaugeNeedle{ from{ transform:rotate(-90deg); } }
.gauge-preview .g-arc-fg{
    animation:gaugeArcSweep 3.6s cubic-bezier(.45,0,.2,1) infinite alternate;
}
.gauge-preview .g-needle{
    animation:gaugeNeedleSweep 3.6s cubic-bezier(.45,0,.2,1) infinite alternate;
}
@keyframes gaugeArcSweep{
    from{ stroke-dashoffset:82; }
    to{ stroke-dashoffset:2; }
}
@keyframes gaugeNeedleSweep{
    from{ transform:rotate(-57.6deg); }
    to{ transform:rotate(86.4deg); }
}

.readout-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:0; border:1px solid var(--line); border-radius:var(--radius-m); overflow:hidden; }
.readout{ padding:20px 22px; border-left:1px solid var(--line); background:var(--bg-card); }
.readout:first-child{ border-left:0; }
.readout .n{ font-family:var(--display); font-size:26px; font-weight:600; }
.readout .n.good{ color:var(--good); }
.readout .n.bad{ color:var(--bad); }
.readout .l{ font-size:12px; color:var(--ink-faint); margin-top:4px; }
.readout.wide{ grid-column:span 3; display:flex; align-items:center; justify-content:space-between; border-top:1px solid var(--line); border-left:0; }

.stTabs [data-baseweb="tab-list"]{
    gap:2px;
    border-bottom:1px solid var(--line);
    overflow-x:auto;
}
.stTabs [data-baseweb="tab"]{
    background:transparent;
    border:0;
    border-bottom:2px solid transparent;
    border-radius:0;
    color:var(--ink-faint);
    font-family:var(--sans);
    font-size:14px;
    padding:12px 18px;
    white-space:nowrap;
}
.stTabs [aria-selected="true"]{
    color:var(--brass-bright) !important;
    border-color:var(--brass) !important;
}

.section{ margin-top:28px; }
.card{ padding:0; }
.card-title{
    font-family:var(--mono);
    font-size:12px;
    color:var(--ink-faint);
    margin:0 0 12px;
}
.card-empty{ color:var(--ink-faint); font-size:13px; margin:0; line-height:1.55; }
.verdict-wrap{ border-left:2px solid var(--brass); padding:4px 0 4px 22px; margin-bottom:30px; }
.verdict{ font-family:var(--display); font-size:18px; line-height:1.55; color:var(--ink); }
.suggest-list{ list-style:none; margin:0; padding:0; }
.suggest-list li{ display:flex; gap:16px; padding:16px 0; border-top:1px solid var(--line); }
.suggest-list li:first-child{ border-top:0; }
.suggest-list .si{ font-family:var(--mono); color:var(--brass); font-size:13px; flex-shrink:0; padding-top:2px; }
.suggest-list p{ margin:0; font-size:14.5px; color:var(--ink-dim); line-height:1.6; }

.driver,.section-bar-row{ margin-bottom:22px; }
.driver-top,.section-bar-top{ display:flex; justify-content:space-between; align-items:baseline; margin-bottom:8px; gap:16px; }
.driver-name,.section-bar-label{ font-size:14.5px; font-weight:500; color:var(--ink); }
.driver-weight{ font-size:12px; color:var(--ink-faint); margin-left:8px; }
.driver-val,.section-bar-value{ font-family:var(--display); font-size:16px; font-weight:600; color:var(--ink); }
.meter{ position:relative; height:8px; background:var(--bg-raised); border-radius:4px; overflow:visible; }
.meter .fill{
    position:absolute;
    inset:0 auto 0 0;
    width:var(--pct);
    border-radius:4px;
    animation:meterFill 1s cubic-bezier(.22,.9,.3,1) both;
}
.meter .ticks{ position:absolute; top:-3px; left:0; right:0; display:flex; justify-content:space-between; }
.meter .ticks span{ width:1px; height:14px; background:var(--line-strong); }
@keyframes meterFill{ from{ width:0; } }
.fill-good{ background:var(--good); }
.fill-warn{ background:var(--brass); }
.fill-bad{ background:var(--bad); }

.chiprow,.diff-grid{ display:grid; grid-template-columns:1fr 1fr; gap:28px; margin-top:28px; }
.chip-col h4,.diff-col h4{ font-size:14px; font-weight:600; margin:0 0 14px; }
.chip,.skill-chip{
    display:inline-flex;
    align-items:center;
    gap:6px;
    font-size:13px;
    padding:7px 12px;
    border-radius:20px;
    margin:0 8px 8px 0;
}
.chip.good,.skill-chip.good{ background:var(--good-tint); color:var(--good); border:1px solid rgba(140,170,116,.3); }
.chip.bad,.skill-chip.bad{ background:var(--bad-tint); color:var(--bad); border:1px solid rgba(181,106,82,.3); }
.diff-col h4 .count{ font-family:var(--mono); font-size:12px; padding:2px 8px; border-radius:10px; margin-left:6px; }
.diff-col.good h4 .count{ background:var(--good-tint); color:var(--good); }
.diff-col.bad h4 .count{ background:var(--bad-tint); color:var(--bad); }
.diff-item{ display:flex; align-items:baseline; gap:10px; padding:10px 0; border-top:1px solid var(--line); font-size:14px; color:var(--ink-dim); }
.diff-item:first-of-type{ border-top:0; }
.diff-col.good .m{ color:var(--good); }
.diff-col.bad .m{ color:var(--bad); }

.sec-row{ display:grid; grid-template-columns:140px 1fr 54px; align-items:center; gap:16px; padding:12px 0; border-top:1px solid var(--line); }
.sec-row:first-child{ border-top:0; }
.sec-row .name{ font-size:14px; color:var(--ink-dim); }
.sec-row .pct{ font-family:var(--mono); font-size:13px; text-align:right; }

.parse-score{ display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
.parse-score .l{ font-size:14.5px; font-weight:500; }
.parse-score .v{ font-family:var(--display); font-size:20px; color:var(--good); font-weight:600; }
.check-list{ list-style:none; margin:24px 0 0; padding:0; }
.check-list li{ display:flex; gap:14px; padding:14px 0; border-top:1px solid var(--line); }
.check-list li:first-child{ border-top:0; }
.check-list .mk{ flex-shrink:0; width:20px; height:20px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; margin-top:1px; }
.check-list .mk.pass{ background:var(--good-tint); color:var(--good); }
.check-list .mk.warn{ background:var(--bad-tint); color:var(--bad); }
.check-list .ct{ font-size:14px; font-weight:500; margin:0 0 3px; }
.check-list .cd{ font-size:13px; color:var(--ink-faint); margin:0; line-height:1.55; }

.comparison-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:0; border:1px solid var(--line); border-radius:var(--radius-m); overflow:hidden; margin-bottom:18px; }
.comparison-grid div{ background:var(--bg-card); border-left:1px solid var(--line); padding:16px; }
.comparison-grid div:first-child{ border-left:0; }
.comparison-grid span{ display:block; color:var(--ink-faint); font-size:12px; margin-bottom:6px; }
.comparison-grid strong{ color:var(--ink); font-family:var(--display); font-size:24px; }
.cover-letter-text{ font-size:14.5px; line-height:1.85; color:var(--ink-dim); }

.site-footer{
    margin-top:48px;
    background:var(--bg-card);
    border:1px solid var(--line);
    border-radius:var(--radius-m);
    box-shadow:var(--shadow);
    overflow:hidden;
}
.footer-main{
    display:grid;
    grid-template-columns:1.3fr .85fr;
    gap:42px;
    padding:26px 32px;
}
.footer-brand{ min-width:0; }
.footer-brand-row{
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:12px;
}
.footer-logo{
    width:42px;
    height:42px;
    border-radius:50%;
    object-fit:contain;
    flex:0 0 auto;
    box-shadow:0 0 0 1px var(--line), 0 8px 18px -12px rgba(201,154,78,.75);
}
.footer-logo-fallback{
    width:14px;
    height:14px;
    border-radius:3px;
    background:var(--brass);
    transform:rotate(45deg);
    box-shadow:0 0 0 4px var(--brass-tint);
    flex:0 0 auto;
}
.footer-name{
    font-family:var(--display);
    font-size:19px;
    font-weight:600;
    color:var(--ink);
    line-height:1.1;
}
.footer-brand p{
    max-width:58ch;
    margin:0;
    color:var(--ink-dim);
    font-size:13.5px;
    line-height:1.65;
}
.footer-links{
    display:grid;
    gap:10px;
    justify-items:start;
}
.footer-label{
    margin:0 0 2px;
    font-family:var(--mono);
    font-size:12px;
    color:var(--ink-faint);
}
.footer-links a{
    display:inline-flex;
    align-items:center;
    gap:10px;
    color:var(--ink-dim);
    font-size:13.5px;
    text-decoration:none;
    transition:color .15s ease;
}
.footer-links a:hover{ color:var(--brass-bright); }
.footer-links svg{
    width:16px;
    height:16px;
    flex:0 0 auto;
    fill:none;
    stroke:currentColor;
    stroke-width:1.6;
    stroke-linecap:round;
    stroke-linejoin:round;
}
.footer-bottom{
    border-top:1px solid var(--line);
    padding:14px 32px;
    text-align:center;
}
.footer-bottom p{
    margin:0;
    color:var(--ink-faint);
    font-size:12.5px;
}
.footer-bottom strong{
    color:var(--brass-bright);
    font-weight:600;
}

@media (max-width:900px){
    .hero,.analysis-hero,.panel-grid{ grid-template-columns:1fr; }
    .readouts,.readout-grid,.chiprow,.diff-grid,.comparison-grid{ grid-template-columns:1fr; }
    .site-top{ align-items:flex-start; }
    .mark{ font-size:14px; gap:.55em; }
    .brand-logo{ height:2.55em; max-width:2.55em; }
    .brand-text{ white-space:normal; line-height:1.15; }
    .mark-sub{ display:none; }
    .readouts{ display:grid; gap:14px; }
    .readouts .r{ border-left:0; padding-left:0; }
    .readout,.readout:first-child{ border-left:0; border-top:1px solid var(--line); }
    .readout:first-child{ border-top:0; }
    .readout.wide{ grid-column:auto; align-items:flex-start; gap:12px; flex-direction:column; }
    .sec-row{ grid-template-columns:1fr; gap:8px; }
    .panel{ padding:22px; }
    .footer-main{
        grid-template-columns:1fr;
        gap:24px;
        padding:24px 22px;
        text-align:center;
    }
    .footer-brand-row{ justify-content:center; }
    .footer-brand p{ margin:0 auto; }
    .footer-links{ justify-items:center; }
    .footer-links a{ justify-content:center; }
    .footer-bottom{ padding:14px 22px; }
}

@media (prefers-reduced-motion:reduce){
    html{ scroll-behavior:auto; }
    .g-arc-fg,.g-needle,.meter .fill{ animation:none !important; transition:none !important; }
    .gauge-preview .g-arc-fg{ stroke-dashoffset:46; }
    .gauge-preview .g-needle{ transform:rotate(8deg); }
}
</style>
"""
