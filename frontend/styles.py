def load_css():
    return """
<style>

/* ===========================
   GLOBAL
=========================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

.stApp{
    background:#f4f7fb;
}

.block-container{
    max-width:1200px;
    padding-top:2rem;
    padding-bottom:3rem;
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* ===========================
   HERO
=========================== */

.hero{
    background:linear-gradient(135deg,#2563eb,#4f46e5);
    border-radius:22px;
    padding:42px;
    color:white;
    margin-bottom:30px;
    box-shadow:0 18px 40px rgba(37,99,235,.25);
}

.hero-title{
    font-size:42px;
    font-weight:800;
    margin-bottom:10px;
}

.hero-subtitle{
    font-size:17px;
    opacity:.92;
    line-height:1.8;
}

/* ===========================
   SCORE CARD
=========================== */

.score-card{

    background:white;

    border-radius:20px;

    padding:30px;

    box-shadow:0 10px 30px rgba(0,0,0,.08);

    border:1px solid #e5e7eb;
}

.score-label{

    color:#64748b;

    text-transform:uppercase;

    letter-spacing:1px;

    font-size:13px;

    font-weight:700;
}

.score-number{

    font-size:64px;

    font-weight:800;

    color:#2563eb;

    margin-top:15px;
}

.progress{

    height:14px;

    width:100%;

    background:#e5e7eb;

    border-radius:100px;

    overflow:hidden;

    margin-top:20px;
}

.progress-fill{

    height:100%;

    border-radius:100px;

    background:linear-gradient(90deg,#2563eb,#7c3aed);
}

/* ===========================
   SMALL CARDS
=========================== */

.small-card{

    background:white;

    border-radius:18px;

    padding:24px;

    text-align:center;

    margin-bottom:18px;

    border:1px solid #e5e7eb;

    box-shadow:0 8px 25px rgba(0,0,0,.08);
}

.small-title{

    color:#64748b;

    font-size:13px;

    text-transform:uppercase;

    letter-spacing:1px;

    font-weight:600;
}

.small-value{

    margin-top:12px;

    font-size:38px;

    font-weight:700;
}

.green{

    color:#16a34a;
}

.red{

    color:#dc2626;
}

/* ===========================
   SECTION
=========================== */

.section{

    margin-top:35px;
}

.section-heading{

    font-size:28px;

    font-weight:700;

    margin-bottom:20px;

    color:#0f172a;
}

/* ===========================
   BADGES
=========================== */

.badge{

    display:inline-block;

    padding:10px 18px;

    border-radius:100px;

    margin:6px;

    font-size:14px;

    font-weight:600;
}

.badge-green{

    background:#dcfce7;

    color:#15803d;
}

.badge-red{

    background:#fee2e2;

    color:#b91c1c;
}

/* ===========================
   CARDS
=========================== */

.card{

    background:white;

    border-radius:18px;

    padding:25px;

    border:1px solid #e5e7eb;

    box-shadow:0 8px 25px rgba(0,0,0,.08);

    margin-bottom:20px;
}

.card-title{

    font-size:22px;

    font-weight:700;

    margin-bottom:15px;

    color:#0f172a;
}

.suggestion{

    padding:14px;

    border-left:4px solid #2563eb;

    background:#eff6ff;

    border-radius:10px;

    margin-bottom:14px;
}

.verdict{

    font-size:16px;

    line-height:1.8;

    color:#334155;
}

</style>
"""