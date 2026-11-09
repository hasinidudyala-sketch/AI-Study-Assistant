import time
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

load_dotenv()

st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")

st.title("📚 AI Study Assistant")
st.caption("Your personal AI-powered learning companion")

api_key = os.getenv("GEMINI_API_KEY", "").strip()

if not api_key:
    st.warning("Gemini API key not found. Add GEMINI_API_KEY=your_key in the .env file.")
    st.info("Copy .env.example to .env and paste your Gemini API key.")
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as exc:
    st.error(f"Could not initialize Gemini: {exc}")
    st.stop()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

def ask_gemini(prompt: str) -> str:

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            return response.text or "No response generated."

        except Exception as error:

            error_message = str(error)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < 2:
                    time.sleep(3 * (attempt + 1))
                    continue

                return "Gemini is temporarily busy. Please wait a few minutes and try again."

            return f"Gemini error: {error_message}"

    return "Please try again later."

tabs = st.tabs([
    "🏠 Home",
    "📖 Topic Explainer",
    "📄 PDF Summarizer",
    "💬 Ask AI",
    "📝 Quiz Generator"
])

with tabs[0]:
    st.subheader("Welcome!")
    st.write("Use this application to understand topics, summarize your study PDFs, ask questions from your notes, and practice MCQs.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Features")
        st.write("- AI Topic Explainer\n- PDF Summarizer\n- Ask AI using uploaded notes\n- 5-question MCQ Quiz Generator")
    with col2:
        st.markdown("### Technologies")
        st.write("- Python\n- Google Gemini AI\n- Streamlit\n- PyPDF")

with tabs[1]:
    st.subheader("AI Topic Explainer")
    topic = st.text_input("Enter a topic", placeholder="Example: Convolutional Neural Networks")
    if st.button("Explain Topic", key="explain"):
        if topic.strip():
            with st.spinner("Generating explanation..."):
                st.markdown(ask_gemini(
                    f"Explain {topic} to a college student in simple English. "
                    "Use headings: Definition, How it works, Key points, Example, and Conclusion."
                ))
        else:
            st.warning("Please enter a topic.")

with tabs[2]:
    st.subheader("PDF Summarizer")
    uploaded_pdf = st.file_uploader("Upload your study PDF", type=["pdf"])
    if uploaded_pdf is not None:
        if st.button("Extract and Summarize PDF", key="summarize"):
            try:
                reader = PdfReader(uploaded_pdf)
                extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
                if not extracted.strip():
                    st.error("No selectable text was found. This may be a scanned/image-only PDF.")
                else:
                    st.session_state.pdf_text = extracted
                    with st.spinner("Summarizing your PDF..."):
                        summary = ask_gemini(
                            "Summarize these study notes in simple English. "
                            "Use clear headings and important exam points:\n\n" + extracted[:25000]
                        )
                    st.markdown(summary)
                    st.success("PDF text extracted. You can now use the Ask AI tab.")
            except Exception as exc:
                st.error(f"Could not read this PDF: {exc}")

with tabs[3]:
    st.subheader("Ask AI from Your Study Notes")
    if st.session_state.pdf_text:
        st.success("Study notes are loaded.")
        question = st.text_input("Enter your question", placeholder="Example: What is pooling?")
        if st.button("Ask Question", key="ask"):
            if question.strip():
                with st.spinner("Finding the answer..."):
                    answer = ask_gemini(
                        "Answer the student's question using only the study notes below. "
                        "If the answer is not present, clearly say that it is not available in the notes. "
                        "Use simple English.\n\n"
                        f"STUDY NOTES:\n{st.session_state.pdf_text[:25000]}\n\n"
                        f"QUESTION:\n{question}"
                    )
                st.markdown(answer)
            else:
                st.warning("Please enter a question.")
    else:
        st.info("Upload a PDF and click 'Extract and Summarize PDF' in the PDF Summarizer tab first.")

with tabs[4]:
    st.subheader("MCQ Quiz Generator")
    quiz_topic = st.text_input("Enter a topic for your quiz", placeholder="Example: Deep Learning")
    if st.button("Generate 5 MCQs", key="quiz"):
        if quiz_topic.strip():
            with st.spinner("Creating your quiz..."):
                st.markdown(ask_gemini(
                    f"Create exactly 5 multiple-choice questions about {quiz_topic}. "
                    "For each question provide four options (A, B, C, D), the correct answer, "
                    "and a short explanation. Keep the language student-friendly."
                ))
        else:
            st.warning("Please enter a topic.")

st.divider()
st.caption("AI Study Assistant | Student Mini Project")
