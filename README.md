# 📚 AI Study Assistant

Your personal AI-powered learning companion built using Python, Google Gemini AI and Streamlit.

## 🚀 Features

1. **AI Topic Explainer** – Explains academic topics in simple English with examples.
2. **PDF Summarizer** – Extracts and summarizes uploaded study PDFs.
3. **Ask AI** – Answers questions using uploaded study notes.
4. **MCQ Quiz Generator** – Generates five multiple-choice questions with answers and explanations.

## 🛠️ Technologies Used

- Python
- Google Gemini AI
- Streamlit
- PyPDF
- python-dotenv

## ▶️ How to Run

1. Download or clone this repository.
2. Install Python 3.10 or newer.
3. Copy `.env.example` and rename the copy to `.env`.
4. Add your Gemini API key inside `.env`.
5. Open CMD in the project folder.
6. Run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

7. Open `http://localhost:8501` in your browser.

On Windows, you can also double-click `run.bat` after configuring `.env`.

## 📂 Project Structure

```text
AI-Study-Assistant/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── run.bat
└── README.md
```

## 🎯 Learning Outcomes

- Learned to integrate Google Gemini AI with Python.
- Explored AI tools for learning and productivity.
- Practiced PDF text extraction.
- Developed an interactive AI-powered application.

## Internship

Codomax Digital Solutions – Module 05: AI Tools & Mini Project.

**Note:** Keep your Gemini API key private. Never upload your `.env` file to GitHub.