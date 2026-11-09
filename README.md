# 🤖 AI Study Assistant

An AI-powered study companion built using Python, Streamlit, and Google Gemini. It helps students understand difficult topics, summarize PDF notes, ask questions about study materials, and practice with AI-generated quizzes.

## ✨ Features

### 1. AI Topic Explainer
- Explains complex academic topics in simple language.
- Provides student-friendly explanations.

### 2. PDF Summarizer
- Upload PDF study materials.
- Extracts and summarizes the document content.
- Helps students revise important concepts quickly.

### 3. Ask Your Notes
- Upload your PDF notes.
- Ask questions based on the uploaded material.
- Get AI-generated answers using the document context.

### 4. MCQ Quiz Generator
- Generates multiple-choice questions from study topics or notes.
- Allows students to test their understanding.
- Provides quiz scoring and feedback.

## 🛠️ Technologies Used

- **Python** – Core programming language
- **Streamlit** – Interactive web application
- **Google Gemini API** – AI-powered responses
- **PyPDF** – PDF text extraction
- **Python-dotenv** – Environment variable management

## 📁 Project Structure

```text
AI-Study-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── run.bat
│
└── .streamlit/
    └── config.toml
```

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/hasinidudyala-sketch/AI-Study-Assistant.git
```

### Step 2: Open the Project Folder

```bash
cd AI-Study-Assistant
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Environment

Windows:

```bash
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Gemini API

1. Create a `.env` file in the project folder.
2. Add your Google Gemini API key.

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

**Important:** Never upload your actual `.env` file or API key to GitHub.

### Step 7: Run the Application

```bash
streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

## 🎯 Project Objective

The main objective of this project is to make learning easier and more interactive by using Generative AI. It provides students with a single platform to understand concepts, summarize notes, ask questions, and evaluate their knowledge.

## 🚀 Future Enhancements

- User login and personalized study history
- More quiz formats
- Support for additional document formats
- Improved study progress tracking

## 👩‍💻 Developed By

**Dudyala Hasini**

B.Tech – Artificial Intelligence and Machine Learning

GitHub: [hasinidudyala-sketch](https://github.com/hasinidudyala-sketch)

## 📌 Internship Project

Developed as part of the **Codomax Digital Solutions Internship – Module 06: Final AI/ML Project**.

---

⭐ If you find this project useful, consider giving the repository a star!
