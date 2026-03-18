"""
app.py
------
EduTutor AI — Streamlit Web UI
A beautiful, student-friendly interface for the Education Tutor.

Run: streamlit run app.py
"""

import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

import streamlit as st

# ── Page config (MUST be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="EduTutor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load env ────────────────────────────────────────────────────────────────
load_dotenv()

# ── Inject custom CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700;800&family=Hind:wght@300;400;500;600&display=swap');

/* ── Root variables ── */
:root {
    --saffron:   #FF6B35;
    --deep:      #1A1A2E;
    --mid:       #16213E;
    --card:      #0F3460;
    --accent:    #E94560;
    --green:     #00B894;
    --yellow:    #FDCB6E;
    --text:      #E8EAF0;
    --muted:     #8892A4;
    --radius:    14px;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Hind', sans-serif;
    background-color: var(--deep) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Main container ── */
.main .block-container {
    padding: 1.5rem 2rem 3rem;
    max-width: 1100px;
}

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #FF6B35 0%, #E94560 50%, #0F3460 100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.hero h1 {
    font-family: 'Baloo 2', cursive;
    font-size: 2.4rem;
    font-weight: 800;
    color: white !important;
    margin: 0 0 0.3rem;
    line-height: 1.1;
}
.hero p {
    color: rgba(255,255,255,0.85) !important;
    font-size: 1rem;
    margin: 0;
}
.hero .badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    color: white !important;
    margin-bottom: 0.6rem;
    backdrop-filter: blur(8px);
}

/* ── Stat cards ── */
.stat-row {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.stat-card {
    flex: 1;
    min-width: 130px;
    background: var(--mid);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: var(--radius);
    padding: 0.9rem 1rem;
    text-align: center;
}
.stat-card .stat-num {
    font-family: 'Baloo 2', cursive;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--saffron);
    line-height: 1;
}
.stat-card .stat-label {
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 3px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Chat messages ── */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1rem;
}
.msg-user {
    display: flex;
    justify-content: flex-end;
    gap: 0.6rem;
    align-items: flex-start;
}
.msg-bot {
    display: flex;
    justify-content: flex-start;
    gap: 0.6rem;
    align-items: flex-start;
}
.bubble-user {
    background: linear-gradient(135deg, var(--saffron), var(--accent));
    color: white !important;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 70%;
    font-size: 0.95rem;
    line-height: 1.5;
    box-shadow: 0 4px 15px rgba(255,107,53,0.25);
}
.bubble-bot {
    background: var(--card);
    border: 1px solid rgba(255,255,255,0.08);
    color: var(--text) !important;
    border-radius: 18px 18px 18px 4px;
    padding: 0.85rem 1.2rem;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.bubble-bot p { margin: 0.3rem 0; }
.bubble-bot strong { color: var(--yellow); }
.bubble-bot code {
    background: rgba(255,255,255,0.1);
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 0.88em;
}
.avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
    margin-top: 2px;
}
.avatar-user { background: linear-gradient(135deg, var(--saffron), var(--accent)); }
.avatar-bot  { background: linear-gradient(135deg, var(--green), var(--card)); }

/* ── Pruning info badge ── */
.prune-badge {
    background: rgba(0,184,148,0.12);
    border: 1px solid rgba(0,184,148,0.3);
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 0.72rem;
    color: var(--green) !important;
    display: inline-block;
    margin-top: 6px;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: var(--mid) !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'Hind', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--saffron) !important;
    box-shadow: 0 0 0 3px rgba(255,107,53,0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--saffron), var(--accent)) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Baloo 2', cursive !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(255,107,53,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(255,107,53,0.45) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--mid) !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Baloo 2', cursive;
    color: var(--saffron) !important;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--mid) !important;
    border: 1.5px dashed rgba(255,107,53,0.4) !important;
    border-radius: var(--radius) !important;
}
[data-testid="stFileUploader"] label { color: var(--text) !important; }

/* ── Select / radio ── */
.stRadio label, .stSelectbox label { color: var(--text) !important; }
.stRadio > div > div > label { color: var(--muted) !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--mid) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'Baloo 2', cursive;
}
.streamlit-expanderContent {
    background: var(--mid) !important;
    border-radius: 0 0 var(--radius) var(--radius);
}

/* ── Topic pill ── */
.topic-pill {
    display: inline-block;
    background: rgba(255,107,53,0.15);
    border: 1px solid rgba(255,107,53,0.3);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    color: var(--saffron) !important;
    margin: 2px;
    cursor: pointer;
}

/* ── Success / info boxes ── */
.stSuccess { background: rgba(0,184,148,0.1) !important; border-color: var(--green) !important; }
.stInfo    { background: rgba(15,52,96,0.6) !important; }
.stWarning { background: rgba(253,203,110,0.1) !important; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--saffron) !important; }

/* ── Welcome screen ── */
.welcome-card {
    background: var(--mid);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
}
.welcome-card .emoji { font-size: 3rem; display: block; margin-bottom: 0.5rem; }
.welcome-card h3 {
    font-family: 'Baloo 2', cursive;
    color: var(--yellow) !important;
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}
.welcome-card p { color: var(--muted) !important; font-size: 0.9rem; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--deep); }
::-webkit-scrollbar-thumb { background: var(--card); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Lazy imports (after page config) ────────────────────────────────────────
DATA_DIR = Path("_data")
DATA_DIR.mkdir(exist_ok=True)


def load_gemini_model():
    """Setup and return Gemini model."""
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or api_key == "your_gemini_api_key_here":
        return None, "not_set"
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction="""You are EduTutor AI — a highly accurate, expert tutor for Indian school and university students (CBSE, ICSE, and State Board curriculum).

═══ ACCURACY RULES (highest priority) ═══
1. Read the [TEXTBOOK CONTEXT] carefully before answering. If the answer is in the context, use it as the primary source.
2. If the topic is NOT in the context, use your own deep knowledge to give a fully correct answer. Say: "📌 General answer (not in loaded textbook):" before it.
3. NEVER guess or make up facts. If uncertain, say so clearly.
4. For science/math: always include the correct formula, unit, and a worked example.
5. For history/social science: always include correct dates, names, and causes/effects.

═══ FORMAT RULES ═══
6. Structure every answer exactly like this:

**[Direct answer in one sentence]**

**Explanation:**
• Point 1 (with detail)
• Point 2 (with detail)
• Point 3 if needed

**Example:** A simple real-life Indian example (farm, cricket, market, monsoon, train journey, etc.)

**Formula / Key fact:** (if applicable — include unit)

💬 *Follow-up: [One simple question to check understanding]*

7. Use **bold** for every key term the first time it appears.
8. Use bullet points (•) for lists — never numbered lists unless it is a step-by-step process.
9. Write in simple English (Class 8–10 reading level). Short sentences. No jargon without explanation.
10. Length: 180–380 words. NEVER truncate mid-sentence. ALWAYS finish the full answer.

═══ TONE RULES ═══
11. Be warm, encouraging, and patient. Every question is a great question.
12. Never say "I cannot help" or "I don't know" — always give the best answer possible.
13. Never repeat the question back to the student.""",
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 1024,
                "top_p": 0.85,
            },
        )
        return model, "ok"
    except Exception as e:
        return None, str(e)


@st.cache_resource(show_spinner=False)
def get_pruner():
    """Load context pruner (cached — loads once)."""
    sys.path.insert(0, str(Path(__file__).parent))
    from context_pruner import ContextPruner
    return ContextPruner()


def ask_tutor(model, question: str):
    """Call Gemini with pruned context. Returns (answer, stats_dict)."""
    pruner = get_pruner()

    # Measure tokens before/after pruning
    all_words = sum(len(c["text"].split()) for c in pruner.chunks)
    relevant = pruner.prune(question, top_k=4)
    pruned_words = sum(len(c["text"].split()) for c in relevant)
    savings_pct = int((1 - pruned_words / max(all_words, 1)) * 100)

    context = pruner.build_context(question, top_k=4)
    prompt = f"""Below are the most relevant sections from the student's textbook (selected by Context Pruning):

[TEXTBOOK CONTEXT — use this as primary source]
{context}

[STUDENT QUESTION]
{question}

Instructions:
- If the answer is clearly in the TEXTBOOK CONTEXT above, base your answer on it.
- If the answer is NOT in the context, use your own knowledge and prefix with "📌 General answer (not in loaded textbook):"
- Follow the structured format from your system instructions exactly.
- Complete the full answer — do not stop early."""

    response = model.generate_content(prompt)
    stats = {
        "total_words": all_words,
        "sent_words": pruned_words,
        "savings_pct": savings_pct,
        "chunks_used": len(relevant),
        "topics": [c.get("title", "?")[:30] for c in relevant],
    }
    return response.text, stats


def ingest_pdf_streamlit(uploaded_file, subject_name: str):
    """Ingest an uploaded PDF file."""
    import tempfile
    from pdf_ingestor import ingest_pdf

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    ingest_pdf(tmp_path, subject_name)
    os.unlink(tmp_path)
    # Clear the cache so new chunks are loaded
    get_pruner.clear()


def count_data_files():
    txt_files = list(DATA_DIR.glob("*.txt"))
    json_files = list(DATA_DIR.glob("*.json"))
    return len(txt_files), len(json_files)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0
if "tokens_saved" not in st.session_state:
    st.session_state.tokens_saved = 0
if "api_key_input" not in st.session_state:
    st.session_state.api_key_input = os.getenv("GEMINI_API_KEY", "")


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1rem;">
        <span style="font-size:2.5rem">🎓</span>
        <h2 style="font-family:'Baloo 2',cursive; color:#FF6B35; margin:0.2rem 0 0;">EduTutor AI</h2>
        <p style="color:#8892A4; font-size:0.78rem; margin:0;">Education for Rural India</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # API Key
    st.markdown("### 🔑 Gemini API Key")
    api_key = st.text_input(
        "API Key",
        value=st.session_state.api_key_input,
        type="password",
        placeholder="AIza...",
        label_visibility="collapsed",
    )
    if api_key != st.session_state.api_key_input:
        st.session_state.api_key_input = api_key
        os.environ["GEMINI_API_KEY"] = api_key
        # Update .env file
        env_path = Path(".env")
        env_path.write_text(f"GEMINI_API_KEY={api_key}\n")

    if not api_key or api_key == "your_gemini_api_key_here":
        st.markdown("""
        <div style="background:rgba(233,69,96,0.1);border:1px solid rgba(233,69,96,0.3);
        border-radius:10px;padding:0.6rem 0.8rem;margin-top:0.5rem;font-size:0.78rem;color:#E94560;">
        ⚠️ No API key set.<br>
        <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#FF6B35;">
        Get FREE key →</a>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(0,184,148,0.1);border:1px solid rgba(0,184,148,0.3);
        border-radius:10px;padding:0.5rem 0.8rem;margin-top:0.5rem;font-size:0.78rem;color:#00B894;">
        ✅ API key set
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Upload PDF
    st.markdown("### 📖 Add Textbook (PDF)")
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    subject_name = st.text_input("Subject name", placeholder="e.g. Class 10 Science")
    if st.button("📥 Ingest PDF", use_container_width=True):
        if uploaded_pdf and subject_name:
            with st.spinner("Processing PDF..."):
                try:
                    ingest_pdf_streamlit(uploaded_pdf, subject_name)
                    st.success(f"✅ '{subject_name}' ingested!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please upload a PDF and enter a subject name.")

    st.divider()

    # Loaded topics
    st.markdown("### 📚 Loaded Topics")
    try:
        pruner = get_pruner()
        if pruner.chunks:
            subjects = {}
            for c in pruner.chunks:
                s = c.get("subject", "Unknown")
                subjects[s] = subjects.get(s, 0) + 1
            for subj, count in subjects.items():
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                padding:0.35rem 0.5rem;background:rgba(255,255,255,0.04);
                border-radius:8px;margin-bottom:4px;">
                    <span style="font-size:0.82rem;color:#E8EAF0;">{subj[:22]}</span>
                    <span style="font-size:0.72rem;color:#FF6B35;font-weight:600;">{count} chunks</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#8892A4;font-size:0.82rem;'>No data loaded yet.<br>Add .txt files to _data/ or upload a PDF above.</p>", unsafe_allow_html=True)
    except Exception:
        st.markdown("<p style='color:#8892A4;font-size:0.82rem;'>Loading...</p>", unsafe_allow_html=True)

    st.divider()

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
    <p style="text-align:center;color:#8892A4;font-size:0.7rem;margin-top:1rem;">
    Gemini 2.5 Flash · Free Tier<br>Context Pruning · ~98% cost saving
    </p>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero">
    <span class="badge">🇮🇳 Built for Rural India</span>
    <h1>🎓 EduTutor AI</h1>
    <p>Personalized, curriculum-aligned tutoring · Lowest cost per query · Powered by Context Pruning</p>
</div>
""", unsafe_allow_html=True)

# Stats row
txt_count, json_count = count_data_files()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-num">{st.session_state.total_queries}</div>
        <div class="stat-label">Questions Asked</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-num">{txt_count}</div>
        <div class="stat-label">Data Files</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-num">{st.session_state.tokens_saved:,}</div>
        <div class="stat-label">Words Saved</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-num" style="color:#00B894;">FREE</div>
        <div class="stat-label">API Cost</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Quick-question chips
st.markdown("""
<p style="font-size:0.8rem;color:#8892A4;margin-bottom:0.4rem;">💡 Try asking:</p>
""", unsafe_allow_html=True)

quick_qs = [
    "What is Ohm's Law?",
    "Explain photosynthesis",
    "How do acids differ from bases?",
    "Tips for board exam preparation",
    "How to write a lab report?",
    "What scholarships are available?",
]

q_cols = st.columns(len(quick_qs))
for i, (col, q) in enumerate(zip(q_cols, quick_qs)):
    with col:
        if st.button(q, key=f"quick_{i}", use_container_width=True):
            st.session_state["prefill_question"] = q

st.divider()

# ── Chat history display ──────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <span class="emoji">📚</span>
        <h3>Welcome to EduTutor AI!</h3>
        <p>Ask any question from your textbook. I'm here to help you learn.<br>
        <em>Whether it's Ohm's Law, photosynthesis, history, or exam tips — just ask!</em></p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            # User bubble — fully self-contained single HTML block
            st.markdown(f"""
            <div class="msg-user">
                <div class="bubble-user">{msg["content"]}</div>
                <div class="avatar avatar-user">👤</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            # ── Bot message ──
            # Rule: NEVER split an HTML block across multiple st.markdown calls.
            # Streamlit flushes each call independently — unclosed tags render as raw text.
            # Solution: render the avatar/layout in a column, answer via st.markdown (native markdown),
            # and the prune badge as a completely separate self-contained block AFTER.

            col_av, col_ans = st.columns([1, 11])
            with col_av:
                st.markdown('<div class="avatar avatar-bot" style="margin-top:6px;">🤖</div>',
                            unsafe_allow_html=True)
            with col_ans:
                # Native st.markdown renders **bold**, bullet points, headers etc. properly
                # Wrap in a CSS class via a container trick — background via st.container style
                with st.container():
                    st.markdown(
                        '<div class="bubble-bot">',
                        unsafe_allow_html=True,
                    )
                    # Render the actual answer as native Streamlit markdown (correct bold/bullets)
                    st.markdown(msg["content"])
                    st.markdown('</div>', unsafe_allow_html=True)

                # Prune badge — fully self-contained block, rendered AFTER bubble closes
                stats = msg.get("stats", {})
                if stats and stats.get("total_words", 0) > 0:
                    topics_str = ", ".join(stats.get("topics", [])[:2])
                    st.markdown(
                        f'<div class="prune-badge">'
                        f'✂️ Sent {stats.get("sent_words", 0):,} / {stats.get("total_words", 0):,} words '
                        f'&nbsp;·&nbsp; {stats.get("savings_pct", 0)}% tokens saved'
                        f'&nbsp;·&nbsp; Topics: {topics_str}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Input area ───────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

prefill = st.session_state.pop("prefill_question", "")

col_input, col_btn = st.columns([5, 1])
with col_input:
    user_input = st.text_input(
        "Ask your question",
        value=prefill,
        placeholder="e.g. What is Newton's third law of motion?",
        label_visibility="collapsed",
        key="chat_input",
    )
with col_btn:
    send = st.button("Ask →", use_container_width=True)

# ── Process question ──────────────────────────────────────────────────────────
if (send or prefill) and user_input.strip():
    question = user_input.strip()

    # Check API key
    current_key = os.getenv("GEMINI_API_KEY", st.session_state.api_key_input)
    if not current_key or current_key == "your_gemini_api_key_here":
        st.error("⚠️ Please set your Gemini API key in the sidebar first. Get it free at https://aistudio.google.com/app/apikey")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})

    # Get answer
    with st.spinner("🤔 Finding relevant content and thinking..."):
        try:
            os.environ["GEMINI_API_KEY"] = current_key
            model, status = load_gemini_model()
            if model is None:
                answer = f"❌ Could not connect to Gemini API: {status}"
                stats = {}
            else:
                answer, stats = ask_tutor(model, question)
                st.session_state.total_queries += 1
                st.session_state.tokens_saved += stats.get("total_words", 0) - stats.get("sent_words", 0)
        except Exception as e:
            answer = f"❌ Error: {str(e)}\n\nCheck your API key and internet connection."
            stats = {}

    st.session_state.messages.append({"role": "assistant", "content": answer, "stats": stats})
    st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("ℹ️ About Context Pruning — How we save 98% API cost"):
    st.markdown("""
    <div style="color:#E8EAF0;font-size:0.9rem;line-height:1.7;">
    <strong style="color:#FF6B35;">The Problem:</strong> Sending an entire textbook to Gemini on every query
    costs thousands of tokens — unaffordable for rural students.<br><br>
    <strong style="color:#00B894;">Context Pruning Solution:</strong>
    <ol>
    <li>Your textbook is split into topic chunks and saved locally in <code>_data/</code> — done once.</li>
    <li>When you ask a question, <strong>local TF-IDF scoring</strong> (no API call!) ranks all chunks by relevance.</li>
    <li>Only the <strong>top 3–4 most relevant chunks</strong> (~2,000 words) are sent to Gemini.</li>
    <li>Gemini answers using only that pruned context — accurate, fast, and cheap.</li>
    </ol>
    <strong style="color:#FDCB6E;">Result:</strong> Instead of 100,000 tokens per query, we send ~2,000.
    That's a <strong style="color:#00B894;">~98% reduction</strong> in API usage.
    </div>
    """, unsafe_allow_html=True)
