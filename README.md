# 📄 AI Resume Analyzer

An AI-powered Resume Analyzer that compares a resume with a Job Description using **Sentence Transformers** for semantic similarity and **Google Gemini** for intelligent skill analysis.

---

## ✨ Features

- 📄 Upload Resume (PDF)
- 📝 Paste Job Description
- 🧠 Semantic Resume-JD Matching
- 🎯 Resume Match Score
- ✅ Matching Skills
- ❌ Missing Skills
- 💡 Improvement Suggestions
- ⚡ Fast Streamlit Interface

---

## 🛠 Tech Stack

### Frontend
- Streamlit

### AI / NLP
- Sentence Transformers
- Google Gemini API

### Machine Learning
- all-MiniLM-L6-v2
- Cosine Similarity (Scikit-learn)

### Backend
- Python

### PDF Processing
- PyMuPDF

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
      ├──────────────┐
      │              │
      ▼              ▼
SentenceTransformer  Job Description
      │              │
      └──────┬───────┘
             ▼
      Cosine Similarity
             │
      Resume Match Score
             │
             ▼
 Google Gemini Analysis
             │
             ├── Matching Skills
             ├── Missing Skills
             └── Suggestions
```

---

## 📂 Project Structure

```
AI-Resume-Analyzer/
│
├── app.py
├── ai_engine.py
├── gemini_engine.py
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

## 🚀 Current Features

- Resume Parsing
- Semantic Similarity Score
- AI-powered Skill Matching
- Missing Skill Detection
- Resume Improvement Suggestions

---

## 🔮 Upcoming Features

- ATS Score
- Recruiter Verdict
- Resume Section Analysis
- Beautiful Dashboard
- Resume Improvement Report
- Deployment on Streamlit Cloud

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