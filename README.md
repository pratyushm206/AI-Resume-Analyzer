# 📄 AI Resume Analyzer

An AI-powered ATS Resume Analyzer that scores a resume against a Job Description using a **deterministic, explainable hybrid scoring engine**, then layers **Google Gemini** on top for qualitative feedback — matching/missing skills, suggestions, and a recruiter-style verdict. It can also generate a tailored cover letter and rewrite the resume itself for a specific JD.

---

## ✨ Features

- 📄 Upload Resume (PDF)
- 📝 Paste Job Description
- 🎯 Hybrid ATS Match Score — deterministic and reproducible (same resume + same JD → same score, every time)
- 🔍 Explainable "Why This Score?" breakdown — semantic relevance, skill match, keyword coverage, experience match, and section relevance, each shown with its weight
- 📊 Section-wise Resume Scoring (Summary, Education, Projects, Skills, Certifications)
- ✅ Matching Skills / ❌ Missing Skills
- 💡 AI-generated Improvement Suggestions
- 🧑‍💼 AI-generated Recruiter Verdict
- ⬇️ Downloadable PDF Analysis Report
- ✉️ AI-generated Cover Letter
- 📝 AI Resume Tailoring — rewrites the resume for a specific JD without inventing skills or experience
- 💾 Session-persisted results across Streamlit reruns
- 🖤 Custom dark, terminal-inspired dashboard UI

---

## 🛠 Tech Stack

### Frontend
- Streamlit
- Custom CSS + component library (`frontend/styles.py`, `frontend/components.py`)

### ATS Scoring Engine (`ats_engine.py`)
A deterministic scoring pipeline — this is what actually produces the numeric score. Gemini is used only for interpretation and prose, never for the number itself, so the score stays reproducible.

| Component | Weight | Method |
|---|---|---|
| Semantic Relevance | 30% | Sentence Transformers embeddings + cosine similarity |
| Skill Match | 30% | Curated skill vocabulary with alias/variant matching (e.g. "React", "React.js", "reactjs" → one canonical skill) |
| Keyword Coverage | 15% | Frequency-ranked JD keyword overlap |
| Experience Match | 15% | Regex-based extraction of required vs. candidate years of experience |
| Section Relevance | 10% | Per-section resume scoring (via `resume_sections.py`) |

### AI / NLP
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Google Gemini API — matching/missing skills, suggestions, recruiter verdict, cover letter generation, resume tailoring

### Backend
- Python

### PDF Processing
- PyMuPDF — resume text extraction
- ReportLab — analysis report generation

---

## 🏗 Project Architecture

```
Resume PDF
      │
      ▼
   PyMuPDF
      │
Extracted Text
      │
      ├─────────────────────────────┐
      │                             │
      ▼                             ▼
  ATS Engine                Google Gemini
  (deterministic)            (qualitative)
      │                             │
      ├── Semantic Relevance        ├── Matching Skills
      ├── Skill Match                ├── Missing Skills
      ├── Keyword Coverage           ├── Suggestions
      ├── Experience Match           └── Recruiter Verdict
      ├── Section Relevance
      │
      ▼
 Weighted ATS Score
 + Explainable Breakdown
      │
      ▼
   Dashboard UI
      │
      ├── PDF Report (ReportLab)
      ├── Cover Letter (Gemini)
      └── Tailored Resume (Gemini)
```

---

## 📂 Project Structure

```
AI-Resume-Analyzer/
│
├── app.py                     # Streamlit entry point
├── ats_engine.py               # Deterministic hybrid ATS scoring engine
├── ai_engine.py                 # Sentence-transformers model + cosine similarity (used by ats_engine and resume_sections)
├── gemini_engine.py            # Gemini-based qualitative analysis
├── cover_letter_engine.py      # Gemini-based cover letter generation
├── resume_tailor_engine.py     # Gemini-based resume tailoring
├── resume_sections.py          # Resume section splitting + per-section scoring
├── report_generator.py         # PDF report generation (ReportLab)
├── frontend/
│   ├── styles.py                # CSS
│   └── components.py            # UI components
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/pratyushm206/AI-Resume-Analyzer.git
```

Go to the project directory

```bash
cd AI-Resume-Analyzer
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run the Project

```bash
streamlit run app.py
```

---

## 🔮 Roadmap

Not yet built — planned next, roughly in priority order:

- ATS compatibility / resume format analysis (formatting, structure, ATS-parseability, independent of any specific JD)
- PDF/DOCX export for the tailored resume and cover letter (currently `.txt` only)
- Re-analysis of the tailored resume with a before/after score comparison
- Expanded skill vocabulary coverage (the curated skill list in `ats_engine.py` grows as new job descriptions surface terms it doesn't yet recognize)
- Automated tests (`ats_engine.py` scoring, section splitting, PDF report generation, Gemini response parsing)
- Deployment (Streamlit Cloud or similar)

---

## 📸 Demo

> Screenshots will be added after the UI is finalized.

---

## 👨‍💻 Author

**Pratyush Mishra**

- GitHub: https://github.com/pratyushm206
- LinkedIn: https://www.linkedin.com/in/pratyush-mishra-211327296

---

⭐ If you found this project useful, consider giving it a star.