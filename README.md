# ✦ AI Study Assistant — Module 06 Final Project

A polished AI-powered study companion built with **Python, Streamlit, Google Gemini API and PyPDF**. It helps students understand topics, summarize lecture PDFs, ask questions from their notes, and practice interactive MCQ quizzes.

## ✨ Features

- **AI Topic Explainer:** simple explanations with definitions, workflows, examples, advantages and exam-ready conclusions.
- **PDF Summarizer:** extracts selectable text from PDFs, summarizes long documents in sections, and lets users download summaries.
- **Ask Your Notes:** chat-style question answering grounded in the uploaded PDF. It tells the user when an answer is not present in the notes.
- **Quiz Studio:** creates 5, 8 or 10 MCQs, supports difficulty levels, interactive answer selection, scoring and explanations.
- **Premium interface:** dark space-inspired background, violet/cyan gradients, glass-style feature cards and sidebar navigation.
- **API resilience:** configurable Gemini model, retry handling for temporary service/rate-limit errors, and readable error messages.

## 🧰 Tech Stack

- Python 3.10+
- Streamlit
- Google GenAI SDK (`google-genai`)
- PyPDF
- python-dotenv

## 🚀 Run on Windows

1. Install Python 3.10 or newer.
2. Extract this ZIP folder.
3. Open the extracted `AI-Study-Assistant-Module06` folder.
4. Copy `.env.example` and rename the copy to `.env`.
5. Open `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

6. Double-click `run.bat`, or open CMD in the project folder and run:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

7. Open the local URL shown in CMD (usually `http://localhost:8501`).

## 🔐 API Key Safety

- Never paste your API key into `app.py`.
- Never upload `.env` to GitHub.
- `.env` is excluded by `.gitignore`.
- If you publish to a hosting provider, configure `GEMINI_API_KEY` as a secret/environment variable.

## 📁 Project Structure

```text
AI-Study-Assistant-Module06/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── run.bat
├── README.md
└── .streamlit/
    └── config.toml
```

## 🧪 Testing Checklist

- [ ] Dashboard opens without errors.
- [ ] Topic Explainer generates an explanation.
- [ ] A text-based PDF can be uploaded and summarized.
- [ ] Ask Your Notes answers from the uploaded PDF.
- [ ] Quiz Studio generates questions, accepts answers and calculates a score.
- [ ] App displays a useful message when API quota/service is unavailable.
- [ ] `.env` is not committed to GitHub.

## ⚠️ Notes and Limitations

- The app uses the Gemini API and therefore requires a valid API key and available API quota.
- Gemini service availability and quotas are controlled by Google. Retry logic can handle temporary failures but cannot guarantee service availability.
- Scanned/image-only PDFs are not OCR processed in this version; use a selectable-text PDF.
- Ask Your Notes sends a bounded portion of extracted text to the model. Very large documents may require more focused questions.

## 🎓 Internship Milestone

Prepared as an upgraded final AI/ML project for **Codomax Digital Solutions — Module 06 (Day 21–Day 24)**.
