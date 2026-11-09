import json
import os
import re
import time
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pypdf import PdfReader

# --------------------------- APP CONFIGURATION ---------------------------
load_dotenv()
st.set_page_config(
    page_title="AI Study Assistant | Learn Smarter",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------- PREMIUM UI THEME ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #080b18;
    --panel: rgba(19, 25, 48, .78);
    --line: rgba(154, 166, 255, .18);
    --text: #eef1ff;
    --muted: #a7b0d0;
    --purple: #9b8cff;
    --cyan: #62d8ef;
}
html, body, [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(ellipse at 12% 8%, rgba(105, 74, 220, .25), transparent 34%),
      radial-gradient(ellipse at 88% 18%, rgba(34, 169, 210, .16), transparent 30%),
      radial-gradient(ellipse at 50% 100%, rgba(89, 63, 173, .18), transparent 38%),
      #080b18 !important;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: .28;
    z-index: 0;
    background-image:
      radial-gradient(1px 1px at 8% 18%, #fff 99%, transparent),
      radial-gradient(1px 1px at 28% 72%, #b8c5ff 99%, transparent),
      radial-gradient(2px 2px at 72% 28%, #fff 99%, transparent),
      radial-gradient(1px 1px at 91% 66%, #a9cfff 99%, transparent),
      radial-gradient(1px 1px at 56% 88%, #fff 99%, transparent);
    background-size: 260px 220px;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(17, 22, 45, .98), rgba(10, 14, 30, .98));
    border-right: 1px solid var(--line);
}
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1250px; }
h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; color: #f4f5ff !important; }
p, li, label, .stMarkdown { color: #dce2ff; }
.hero {
    padding: 2.2rem 2.2rem 2rem;
    border: 1px solid rgba(164, 151, 255, .28);
    border-radius: 26px;
    background: linear-gradient(120deg, rgba(89, 66, 180, .28), rgba(27, 115, 151, .16) 55%, rgba(23, 29, 58, .72));
    box-shadow: 0 22px 70px rgba(0,0,0,.26);
    position: relative;
    overflow: hidden;
}
.hero:after {
    content: "✦";
    position: absolute; right: 7%; top: 5%;
    font-size: 8rem; color: rgba(205, 199, 255, .10);
}
.hero-kicker { color: #a9eafa; text-transform: uppercase; letter-spacing: .18em; font-size: .75rem; font-weight: 700; }
.hero h1 { font-size: clamp(2.1rem, 5vw, 3.6rem); line-height: 1.08; margin: .6rem 0; }
.hero p { color: #c5cbed; font-size: 1.05rem; max-width: 720px; }
.glass-card {
    border: 1px solid var(--line);
    background: linear-gradient(145deg, rgba(25, 33, 63, .82), rgba(14, 19, 39, .82));
    border-radius: 20px;
    padding: 1.15rem 1.25rem;
    min-height: 145px;
    box-shadow: 0 12px 35px rgba(0,0,0,.14);
}
.glass-card .icon { font-size: 1.65rem; }
.glass-card h3 { font-size: 1.05rem; margin: .5rem 0 .25rem; }
.glass-card p { color: var(--muted); font-size: .9rem; margin: 0; }
.section-label { color: #9eafff; font-size: .75rem; letter-spacing: .15em; font-weight: 700; text-transform: uppercase; }
div.stButton > button, div.stFormSubmitButton > button {
    background: linear-gradient(100deg, #7868e8, #3cafd0);
    color: white; border: 0; border-radius: 12px; font-weight: 700;
    padding: .62rem 1.15rem; transition: .2s ease;
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    border: 1px solid rgba(255,255,255,.4); transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(94, 111, 231, .28);
}
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    background: rgba(12, 17, 36, .9) !important;
    color: #f3f5ff !important; border-color: rgba(153, 166, 255, .28) !important;
    border-radius: 11px !important;
}
[data-testid="stFileUploader"] {
    border: 1px dashed rgba(144, 158, 255, .42);
    border-radius: 16px; background: rgba(19, 25, 48, .48); padding: .5rem;
}
div[data-testid="stMetric"] {
    background: rgba(24, 32, 62, .72); border: 1px solid var(--line);
    padding: 1rem; border-radius: 16px;
}
.stTabs [data-baseweb="tab-list"] { gap: .45rem; }
.stTabs [data-baseweb="tab"] {
    background: rgba(25, 31, 58, .65); border-radius: 10px 10px 0 0;
    color: #c7ceef; padding: .65rem 1rem;
}
.stTabs [aria-selected="true"] { background: rgba(112, 96, 220, .28) !important; color: white !important; }
hr { border-color: rgba(151, 164, 255, .16); }
.small-muted { color: #929dbf; font-size: .82rem; }
</style>
""", unsafe_allow_html=True)

# --------------------------- SESSION STATE ---------------------------
DEFAULTS = {
    "pdf_text": "",
    "pdf_name": "",
    "chat_history": [],
    "quiz_data": [],
    "quiz_submitted": False,
    "quiz_topic": "",
    "quiz_answers": {},
    "last_summary": "",
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------- GEMINI CLIENT ---------------------------
api_key = os.getenv("GEMINI_API_KEY", "").strip()
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip() or "gemini-2.5-flash"

@st.cache_resource(show_spinner=False)
def get_client(key: str):
    return genai.Client(api_key=key)

def friendly_api_error(error: Exception) -> str:
    msg = str(error)
    low = msg.lower()
    if "503" in msg or "unavailable" in low or "overloaded" in low:
        return ("The Gemini service is temporarily busy. Wait a little and try again. "
                "Your uploaded notes and answers are still saved in this session.")
    if "429" in msg or "resource_exhausted" in low or "quota" in low:
        return ("The Gemini API rate limit or free quota has been reached. "
                "Wait for the quota to reset, check your Google AI Studio usage, or try later.")
    if "401" in msg or "403" in msg or "api key" in low or "permission" in low:
        return "The API key may be invalid or restricted. Check GEMINI_API_KEY in your local .env file."
    if "404" in msg or "not found" in low:
        return f"The model '{model_name}' was not found for this API key. Set GEMINI_MODEL to a model available in Google AI Studio (for example, gemini-2.5-flash)."
    return f"Gemini request failed: {msg[:500]}"

def generate_ai(prompt: str, temperature: float = 0.4, max_retries: int = 3) -> str:
    if not api_key:
        return "API_KEY_MISSING"
    try:
        client = get_client(api_key)
    except Exception as exc:
        return friendly_api_error(exc)

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=4096,
                ),
            )
            answer = getattr(response, "text", None)
            if answer and answer.strip():
                return answer.strip()
            return "The AI returned an empty response. Please try again."
        except Exception as exc:
            message = str(exc)
            retryable = any(x in message.lower() for x in ["503", "unavailable", "overloaded", "429", "resource_exhausted", "rate"])
            if retryable and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return friendly_api_error(exc)
    return "The request could not be completed. Please try again."

def require_api_key() -> bool:
    if not api_key:
        st.error("Gemini API key not found. Add GEMINI_API_KEY to your .env file, then restart the app.")
        st.code("GEMINI_API_KEY=your_actual_api_key_here\nGEMINI_MODEL=gemini-2.5-flash", language="bash")
        return False
    return True

def split_text(text: str, chunk_size: int = 9000) -> list[str]:
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)] or []

def parse_quiz(raw: str) -> list[dict[str, Any]]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.I)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("The AI did not return valid quiz JSON. Please generate the quiz again.")
        data = json.loads(cleaned[start:end + 1])
    questions = data.get("questions", []) if isinstance(data, dict) else []
    valid = []
    for q in questions[:10]:
        options = q.get("options", {})
        if isinstance(options, list):
            options = {chr(65+i): v for i, v in enumerate(options[:4])}
        if not isinstance(options, dict) or len(options) < 2:
            continue
        answer = str(q.get("answer", q.get("correct_answer", "A"))).strip().upper()
        if answer not in options:
            answer = next(iter(options))
        valid.append({
            "question": str(q.get("question", "Question")),
            "options": {str(k).upper(): str(v) for k, v in options.items()},
            "answer": answer,
            "explanation": str(q.get("explanation", "")),
        })
    if not valid:
        raise ValueError("No usable questions were returned. Please try again.")
    return valid

# --------------------------- SIDEBAR ---------------------------
with st.sidebar:
    st.markdown("## ✦ STUDYSPACE AI")
    st.caption("Your personal learning companion")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["🏠 Dashboard", "📖 Topic Explainer", "📄 PDF Summarizer", "💬 Ask Your Notes", "🧠 Quiz Studio"],
        label_visibility="visible",
    )
    st.markdown("---")
    st.markdown("**SESSION STATUS**")
    st.markdown("🟢 App interface ready")
    st.markdown("🔵 Gemini connected" if api_key else "🟡 Gemini API key needed")
    if st.session_state.pdf_text:
        st.success(f"Notes loaded: {st.session_state.pdf_name or 'Study PDF'}")
    else:
        st.caption("No study PDF loaded yet.")
    st.markdown("---")
    st.markdown('<p class="small-muted">Built with Python · Streamlit · Gemini AI</p>', unsafe_allow_html=True)

# --------------------------- DASHBOARD ---------------------------
if page == "🏠 Dashboard":
    st.markdown("""
    <div class="hero">
      <div class="hero-kicker">✦ YOUR SMARTER STUDY WORKSPACE</div>
      <h1>Learn smarter.<br>Understand deeper.</h1>
      <p>One focused space to explain difficult topics, turn PDFs into clear notes,
      ask questions from your material, and test what you have learned.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.markdown('<div class="section-label">YOUR LEARNING TOOLS</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    cards = [
        ("📖", "Topic Explainer", "Understand complex concepts in simple student-friendly language."),
        ("📄", "PDF Summarizer", "Convert long study documents into organized revision notes."),
        ("💬", "Ask Your Notes", "Get answers grounded in the PDF you uploaded."),
        ("🧠", "Quiz Studio", "Practice MCQs and review your score with explanations."),
    ]
    for col, (icon, title, desc) in zip(cols, cards):
        with col:
            st.markdown(f'<div class="glass-card"><div class="icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
    st.write("")
    a, b, c = st.columns(3)
    a.metric("Learning tools", "4")
    b.metric("Study document", "Loaded" if st.session_state.pdf_text else "Not loaded")
    c.metric("Quiz questions", str(len(st.session_state.quiz_data)) if st.session_state.quiz_data else "Ready")
    st.markdown("---")
    st.subheader("🚀 Quick start")
    st.write("Choose a tool from the left navigation. For document-based questions, upload a text-based PDF in **PDF Summarizer** first.")
    if not api_key:
        st.warning("Add your Gemini API key to activate AI generation. The interface can still be explored without it.")

# --------------------------- TOPIC EXPLAINER ---------------------------
elif page == "📖 Topic Explainer":
    st.markdown("## 📖 AI Topic Explainer")
    st.caption("Turn a difficult concept into an easy-to-understand lesson.")
    with st.form("topic_form"):
        topic = st.text_input("What would you like to learn?", placeholder="Example: Convolutional Neural Networks")
        level = st.selectbox("Explanation level", ["College student", "Beginner", "Exam preparation", "Interview preparation"])
        detail = st.select_slider("Explanation length", options=["Short", "Medium", "Detailed"], value="Medium")
        submitted = st.form_submit_button("✨ Explain this topic")
    if submitted:
        if not topic.strip():
            st.warning("Please enter a topic.")
        elif require_api_key():
            prompt = f"""
Explain "{topic}" for a {level.lower()} in simple, clear English.
Length: {detail.lower()}.
Use this structure:
1. Simple definition
2. Why it is used
3. Step-by-step working
4. Important components or types (if relevant)
5. A simple real-life or academic example
6. Advantages and limitations (if relevant)
7. Short exam-ready conclusion
Use clear headings and avoid unsupported claims.
"""
            with st.spinner("Preparing your lesson..."):
                answer = generate_ai(prompt)
            if answer:
                st.markdown(answer)

# --------------------------- PDF SUMMARIZER ---------------------------
elif page == "📄 PDF Summarizer":
    st.markdown("## 📄 PDF Summarizer")
    st.caption("Upload lecture notes or a textbook PDF and create revision-friendly notes.")
    uploaded = st.file_uploader("Choose a PDF file", type=["pdf"], help="Text-based PDFs work best. Scanned image-only PDFs need OCR.")
    if uploaded:
        st.info(f"Selected: **{uploaded.name}** · {uploaded.size / 1024:.1f} KB")
        if st.button("📥 Extract and summarize PDF", type="primary"):
            try:
                reader = PdfReader(uploaded)
                pages = []
                progress = st.progress(0, text="Reading PDF pages...")
                for idx, p in enumerate(reader.pages):
                    pages.append(p.extract_text() or "")
                    progress.progress((idx + 1) / max(len(reader.pages), 1), text=f"Reading page {idx+1} of {len(reader.pages)}")
                extracted = "\n\n".join(pages).strip()
                progress.empty()
                if not extracted:
                    st.error("No selectable text was found. This may be a scanned PDF. Please use a text-based PDF.")
                else:
                    st.session_state.pdf_text = extracted
                    st.session_state.pdf_name = uploaded.name
                    chunks = split_text(extracted)
                    if require_api_key():
                        summaries = []
                        with st.spinner(f"Summarizing {len(chunks)} section(s)..."):
                            for i, chunk in enumerate(chunks, 1):
                                part = generate_ai(
                                    f"Summarize section {i} of {len(chunks)} from these study notes. "
                                    "Use simple English, headings, key definitions, important points and examples. "
                                    "Do not invent details.\n\n" + chunk,
                                    temperature=0.3,
                                )
                                if part.startswith("The Gemini") or part.startswith("Gemini request") or part.startswith("The Gemini API"):
                                    st.error(part)
                                    break
                                summaries.append(part)
                        if summaries:
                            if len(summaries) > 1:
                                final_summary = generate_ai(
                                    "Combine these section summaries into one organized revision guide. "
                                    "Remove repetition and retain important facts:\n\n" + "\n\n".join(summaries),
                                    temperature=0.3,
                                )
                            else:
                                final_summary = summaries[0]
                            st.session_state.last_summary = final_summary
                            st.success(f"Extracted {len(extracted):,} characters from {len(reader.pages)} page(s). Notes are ready for Ask Your Notes.")
            except Exception as exc:
                st.error(f"Could not process this PDF: {exc}")
    if st.session_state.last_summary:
        st.markdown("---")
        st.subheader("✨ Your study summary")
        st.markdown(st.session_state.last_summary)
        st.download_button(
            "⬇️ Download summary as TXT",
            data=st.session_state.last_summary,
            file_name="ai_study_summary.txt",
            mime="text/plain",
        )
    if st.session_state.pdf_text:
        with st.expander("Preview extracted text"):
            st.text(st.session_state.pdf_text[:5000] + ("\n\n[Preview shortened]" if len(st.session_state.pdf_text) > 5000 else ""))

# --------------------------- ASK YOUR NOTES ---------------------------
elif page == "💬 Ask Your Notes":
    st.markdown("## 💬 Ask AI from your study notes")
    st.caption("Answers are based on the PDF loaded in this session.")
    if not st.session_state.pdf_text:
        st.info("Upload and extract a PDF in **PDF Summarizer** first.")
    else:
        st.success(f"Using: {st.session_state.pdf_name or 'Uploaded study notes'}")
        for item in st.session_state.chat_history:
            with st.chat_message(item["role"]):
                st.markdown(item["content"])
        question = st.chat_input("Ask a question about your uploaded notes...")
        if question:
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
            with st.chat_message("assistant"):
                with st.spinner("Searching your notes..."):
                    answer = generate_ai(
                        "Answer the student's question using only the study notes below. "
                        "If the answer is not present, say clearly that it was not found in the uploaded notes. "
                        "Use simple English and cite page numbers only if page labels are included in the notes.\n\n"
                        f"STUDY NOTES:\n{st.session_state.pdf_text[:50000]}\n\n"
                        f"QUESTION:\n{question}",
                        temperature=0.2,
                    )
                st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
        if st.button("Clear chat history"):
            st.session_state.chat_history = []
            st.rerun()

# --------------------------- QUIZ STUDIO ---------------------------
elif page == "🧠 Quiz Studio":
    st.markdown("## 🧠 Quiz Studio")
    st.caption("Generate a multiple-choice quiz and check your understanding.")
    with st.form("quiz_form"):
        quiz_topic = st.text_input("Quiz topic", placeholder="Example: Deep Learning")
        count = st.selectbox("Number of questions", [5, 8, 10], index=0)
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"])
        make_quiz = st.form_submit_button("🎯 Generate my quiz")
    if make_quiz:
        if not quiz_topic.strip():
            st.warning("Please enter a quiz topic.")
        elif require_api_key():
            prompt = f"""
Create exactly {count} {difficulty.lower()} multiple-choice questions about "{quiz_topic}".
Return ONLY valid JSON with this exact structure:
{{
 "questions": [
  {{
   "question": "Question text",
   "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}},
   "answer": "A",
   "explanation": "Short explanation"
  }}
 ]
}}
Make one answer correct per question. Keep questions accurate and student-friendly.
"""
            with st.spinner("Creating your quiz..."):
                raw = generate_ai(prompt, temperature=0.3)
            try:
                questions = parse_quiz(raw)
                st.session_state.quiz_data = questions
                st.session_state.quiz_topic = quiz_topic
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()
            except Exception as exc:
                st.error(f"{exc}\n\nYou can try generating the quiz again.")
    if st.session_state.quiz_data:
        st.markdown("---")
        st.subheader(f"📝 {st.session_state.quiz_topic} — Practice Quiz")
        with st.form("answer_quiz"):
            for i, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"**Q{i+1}. {q['question']}**")
                keys = list(q["options"].keys())
                labels = [f"{k}. {q['options'][k]}" for k in keys]
                selected = st.radio("Choose one answer:", labels, key=f"quiz_q_{i}", index=None, label_visibility="collapsed")
                st.session_state.quiz_answers[i] = selected.split(".", 1)[0] if selected else None
                st.markdown("---")
            submit_quiz = st.form_submit_button("✅ Submit answers")
        if submit_quiz:
            st.session_state.quiz_submitted = True
            st.rerun()
        if st.session_state.quiz_submitted:
            score = 0
            for i, q in enumerate(st.session_state.quiz_data):
                chosen = st.session_state.quiz_answers.get(i)
                correct = chosen == q["answer"]
                score += int(correct)
                st.markdown(f"**Q{i+1}: {'✅ Correct' if correct else '❌ Incorrect'}**")
                if not correct:
                    st.write(f"Your answer: {chosen or 'Not answered'} · Correct answer: {q['answer']}. {q['options'].get(q['answer'], '')}")
                if q["explanation"]:
                    st.caption(q["explanation"])
            st.success(f"Your score: {score} / {len(st.session_state.quiz_data)} ({score/len(st.session_state.quiz_data)*100:.0f}%)")
            if st.button("🔄 Create another quiz"):
                st.session_state.quiz_data = []
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()

# --------------------------- FOOTER ---------------------------
st.markdown("---")
st.markdown(
    '<p class="small-muted" style="text-align:center;">✦ STUDYSPACE AI · Learn at your pace, one concept at a time · Built with Python, Streamlit & Google Gemini</p>',
    unsafe_allow_html=True,
)
