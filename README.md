# 📚 AI Study Assistant

An AI-powered learning companion for college students, built with **Python, Google Gemini AI, Streamlit, and PyPDF**.

## Features

1. **AI Topic Explainer** – explains a topic in simple English with headings and examples.
2. **PDF Summarizer** – extracts text from a study PDF and generates a summary.
3. **Ask AI** – answers questions using the extracted PDF notes.
4. **MCQ Quiz Generator** – creates five multiple-choice questions with answers and explanations.

## Requirements

- Windows 10/11
- Python 3.10 or newer
- Internet connection
- Gemini API key

## Quick start on Windows

1. Extract the ZIP file.
2. Open the extracted `AI-Study-Assistant` folder.
3. Make a copy of `.env.example` and rename the copy to `.env`.
4. Open `.env` in Notepad and replace `PASTE_YOUR_GEMINI_API_KEY_HERE` with your Gemini API key.
5. Save the file.
6. Double-click **`run.bat`**.

The first run creates a virtual environment and installs the required packages. This may take a few minutes. When installation finishes, Streamlit opens the application in your browser.

### Run manually (optional)

Open a terminal in this folder and run:

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Get a Gemini API key

Create or manage a key using Google AI Studio: https://aistudio.google.com/app/apikey

Keep your API key private. Do not upload `.env` to GitHub.

## How to use

- Open **Topic Explainer**, enter a topic, and click **Explain Topic**.
- Open **PDF Summarizer**, upload a text-based PDF, and click **Extract and Summarize PDF**.
- Open **Ask AI** and ask a question about the uploaded PDF.
- Open **Quiz Generator**, enter a topic, and click **Generate 5 MCQs**.

**Note:** Scanned PDFs that contain only images may not have extractable text. This project does not include OCR.

## Project structure

```text
AI-Study-Assistant/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── run.bat
└── README.md
```

## Technologies used

- Python
- Google Gemini API (`google-genai`)
- Streamlit
- PyPDF
- python-dotenv

## Internship mini-project

Developed as an AI Tools & Mini Project learning activity for **Codomax Digital Solutions**.

## Troubleshooting

- **API key warning:** Check that `.env` is in the same folder as `app.py`, and that the key is entered after `GEMINI_API_KEY=`.
- **Model not found:** Change `GEMINI_MODEL` in `.env` to a Gemini model available to your API key.
- **Package installation is slow:** The first run needs to download Python packages. Keep the terminal open until it finishes.
- **Port already in use:** Close the earlier Streamlit terminal, then run `run.bat` again.
