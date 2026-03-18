<div align="center">

<br/>

```
  ███████╗██████╗ ██╗   ██╗████████╗██╗   ██╗████████╗ ██████╗ ██████╗
  ██╔════╝██╔══██╗██║   ██║╚══██╔══╝██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗
  █████╗  ██║  ██║██║   ██║   ██║   ██║   ██║   ██║   ██║   ██║██████╔╝
  ██╔══╝  ██║  ██║██║   ██║   ██║   ██║   ██║   ██║   ██║   ██║██╔══██╗
  ███████╗██████╔╝╚██████╔╝   ██║   ╚██████╔╝   ██║   ╚██████╔╝██║  ██║
  ╚══════╝╚═════╝  ╚═════╝    ╚═╝    ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝
```

### 🎓 Education Tutor for Remote India

**Personalized, curriculum-aligned AI tutoring for CBSE / ICSE / State Board students**
**Built on the free Gemini API — ₹0 cost to run — ~98% cheaper than a standard RAG system**

<br/>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)
[![Cost](https://img.shields.io/badge/API%20Cost-₹0%20Free%20Tier-00B894?style=for-the-badge&logo=googleplay&logoColor=white)](https://aistudio.google.com/app/apikey)
[![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)](LICENSE)

<br/>

[✨ Features](#-features) • [🚀 Quick Start](#-quick-start) • [🏗️ How It Works](#️-how-it-works) • [📖 Add Textbooks](#-adding-your-own-textbooks) • [🐛 Troubleshooting](#-troubleshooting)

<br/>

</div>

---

## 🌏 The Problem

Personalized AI tutors are revolutionizing education globally — but they are **expensive**. In rural India, where:

- 📡 Internet connectivity is **unreliable and slow**
- 💻 Computing power is **limited**
- 💸 Students **cannot afford** ₹80–₹500 per AI query

A standard RAG system blindly sends the **entire textbook (~100,000 tokens)** to the LLM on every single question. At even $0.01 per 1K tokens, that's **$1 per question** — completely unaffordable.

---

## ✅ The Solution — Context Pruning

EduTutor AI uses **Context Pruning**: a technique that finds only the 3–4 most relevant textbook chapters for each question using **local TF-IDF** (no paid embedding API), and sends *only those* to Gemini.

```
❌  Naive RAG:       ~100,000 tokens/query  →  expensive, slow, re-reads full book every time
✅  EduTutor AI:       ~2,000 tokens/query  →  98% cheaper, fast, retrieval runs locally in ms
```

> **The key insight:** You don't need to send the whole textbook if you can *identify the right pages first* — for free, locally.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Context Pruning** | Local TF-IDF ranks chunks by relevance — zero API cost for retrieval |
| 📚 **PDF Ingestion** | Upload any textbook PDF; it's split into topic chunks once, never re-processed |
| 🎨 **Streamlit Web UI** | Dark-themed chat interface with bubble messages, sidebar, and live stats |
| 💻 **Terminal Agent** | Fallback CLI with Rich colored output for zero-browser environments |
| 📊 **Token Savings Badge** | Every answer shows exactly how many words/tokens were saved |
| 🇮🇳 **India-first Prompt** | Answers use Indian examples (farms, cricket, monsoon, markets) |
| 🆓 **Completely Free** | Runs on Gemini 2.5 Flash free tier — no credit card, no billing |
| 📁 **Multi-subject** | Load as many textbooks as needed across subjects and classes |


---

## 📁 Project Structure

```
edututor-ai/
│
├── 🚀 app.py                           ← Streamlit Web UI (run this)
├── 💻 genAi_edututor_agent.py          ← Terminal chat agent
├── ✂️  context_pruner.py               ← Context Pruning engine (TF-IDF)
├── 📖 pdf_ingestor.py                  ← PDF → smart chunks converter
│
├── requirements.txt                    ← Python dependencies
├── .env                                ← Your API key goes here (you create this)
├── README.md
│
└── _data/                              ← All textbook content lives here
    ├── finalDataset0.2.exam.txt            Exam tips & strategies
    ├── finalDataset0.2.teach.txt           Science (Physics / Chemistry / Biology)
    ├── finalDataset0.2.lab.txt             Lab experiments & safety
    ├── finalDataset0.2.library.txt         Library & research skills
    ├── finalDataset0.2.extracurricular.txt Student development & scholarships
    └── [your ingested PDF chunks]          Added automatically when you ingest PDFs
```

---

## 🚀 Quick Start

### Step 1 — Clone the repository

```bash
git clone https://github.com/M-das2004/edututor-ai.git
cd edututor-ai
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Get your FREE Gemini API key

> ⚡ No credit card needed. Takes 60 seconds.

1. Go to → **[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key 

### Step 4 — Add your API key

Create a file named `.env` in the project root:

```env
GEMINI_API_KEY=your_actual_key
```

> ⚠️ Never commit this file to Git. Add `.env` to your `.gitignore`.

### Step 5 — Run the app

**🌐 Web UI (recommended):**
```bash
streamlit run app.py
```
Opens at **http://localhost:8501** automatically.

**💻 Terminal version (for low-bandwidth environments):**
```bash
python genAi_edututor_agent.py
```

---

## 🏗️ How It Works

### Phase 1 — Ingest *(run once per textbook)*

```
📄 PDF Textbook
      │
      ▼  [pdf_ingestor.py]
  PyPDF2 extracts all pages as text
      │
      ▼
  Chapter boundary detection via regex
  (detects "Chapter 1", "Unit 3", "Section 2.1" patterns)
      │
      ▼
  Pages grouped into topic chunks
  Small chunks (< 200 words) merged with neighbours
      │
      ▼
  💾 Saved as .txt files in _data/
  📋 Manifest JSON saved for metadata lookup
```

> This step runs **ONCE**. The PDF is never re-processed again.

---

### Phase 2 — Query *(every student question)*

```
🎓 Student types: "What is photosynthesis?"
      │
      ▼  [context_pruner.py — LOCAL, zero API cost]
  Tokenize query → build TF vector
  Compute cosine similarity vs all chunks
  Rank chunks by relevance score
      │
      ▼
  Top 4 chunks selected  (~2,000 words)   ← Context Pruning happens here
      │
      ▼  [Gemini API — ~2K tokens sent, not 100K]
  Structured prompt built and sent to Gemini 2.5 Flash
      │
      ▼
  📝 Curriculum-aligned answer returned
  🖥️ Rendered in Streamlit chat UI with token-savings badge
```

---

### The Math Behind Context Pruning

For every chunk in `_data/`, we compute a **TF (Term Frequency) vector**:

```
TF(word, chunk) = occurrences of word in chunk / total words in chunk
```

Then we compute **cosine similarity** between the query TF vector and each chunk TF vector:

```
similarity = (query_TF · chunk_TF) / (|query_TF| × |chunk_TF|)
```

Chunks are ranked by this score. The top `k=4` are selected. Each chunk is truncated to **800 words** before being sent to Gemini, capping total context at ~3,200 words per query.

> **Why TF-IDF instead of a paid embedding API?**
> Embedding APIs cost money, require internet for every retrieval, and add latency. TF-IDF runs locally in milliseconds with zero cost — and for keyword-rich textbook content, it achieves excellent retrieval accuracy.

---

## 📖 Adding Your Own Textbooks

### Option A — Drop a `.txt` file into `_data/`

Create any plain text file and place it in `_data/`. Use this naming pattern:

```
_data/finalDataset.class10_mathematics.txt
_data/finalDataset.class12_chemistry.txt
_data/finalDataset.history_class9.txt
```

Restart the app — the content is automatically loaded.

### Option B — Upload PDF via the Streamlit UI

1. Open the app at `http://localhost:8501`
2. In the **sidebar**, find **"📖 Add Textbook"**
3. Upload your PDF
4. Enter a subject name (e.g. `Class 10 Mathematics`)
5. Click **"📥 Ingest PDF"**
6. The app reloads with the new content — no restart needed

### Option C — Command line ingest

```bash
python pdf_ingestor.py path/to/textbook.pdf "Class 10 Mathematics"
```

> 📎 Download free NCERT textbooks from: **[ncert.nic.in/textbook.php](https://ncert.nic.in/textbook.php)**

---

## 🧠 AI System Prompt Design

The system prompt passed to Gemini is structured in **three priority layers**:

### Layer 1 — Accuracy Rules *(highest priority)*
- Use the `[TEXTBOOK CONTEXT]` as the primary source
- If a topic is **not** in the context, answer from model knowledge and prefix with `📌 General answer (not in loaded textbook):`
- For science/math: **always** include the formula, unit, and a worked example
- Never fabricate facts or truncate mid-answer

### Layer 2 — Response Format *(enforced on every answer)*

```
**[Direct answer — one bold sentence]**

**Explanation:**
• Point 1 with detail
• Point 2 with detail
• Point 3 if needed

**Example:** [Real-life Indian context — farm, cricket, monsoon, market, train...]

**Formula / Key fact:** [with units, if applicable]

💬 *Follow-up: [one question to check student understanding]*
```

### Layer 3 — Tone Rules
- Simple English (Class 8–10 reading level)
- Warm, patient, encouraging — every question is a great question
- Answers between 180–380 words; never cut off mid-sentence

---

## ⚙️ Configuration Reference

**Model settings** in `app.py` and `genAi_edututor_agent.py`:

```python
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",     # Current free-tier model
    generation_config={
        "temperature": 0.3,            # Low = factual, deterministic answers
        "max_output_tokens": 1024,     # Allows complete 380-word answers
        "top_p": 0.85,                 # Nucleus sampling for natural language
    }
)
```

**Context Pruner settings** in `context_pruner.py`:

```python
top_k      = 4    # Number of chunks sent to Gemini per query
max_words  = 800  # Max words per chunk before truncation
min_words  = 200  # Chunks smaller than this are merged during ingest
```

**Environment variables** (`.env`):

```env
GEMINI_API_KEY=your_key_here    # Required. Get free at aistudio.google.com
```

---

## 📊 Gemini Free Tier Limits

| Model | Rate Limit | Daily Limit | Notes |
|-------|-----------|-------------|-------|
| `gemini-2.5-flash` ✅ **used** | 10 req/min | 500 req/day | Best balance of speed & quality |
| `gemini-2.5-flash-lite` | 15 req/min | 1,000 req/day | Faster, good for higher volume |
| `gemini-2.5-pro` | 5 req/min | 100 req/day | Best for complex/hard questions |

> At 500 free queries/day, a student asking 20 questions/day gets **25 days of free tutoring** without spending a single rupee.

---

## 🐛 Troubleshooting

| Error / Symptom | Cause | Fix |
|----------------|-------|-----|
| `404 model not found` | `gemini-1.5-flash` was retired in 2026 | Set model to `gemini-2.5-flash` in `app.py` |
| `GEMINI_API_KEY not set` | No `.env` file or blank value | Create `.env` with your key |
| `No module named google.generativeai` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `No textbook data found` | `_data/` folder is empty | Add `.txt` files or ingest a PDF |
| Raw HTML visible in chat | Using an older `app.py` | Update to the latest version |
| `429 Too Many Requests` | Hit the 10 req/min free tier rate limit | Wait 60 seconds, or switch to `gemini-2.5-flash-lite` |
| PDF ingest gives empty chunks | PDF is a scanned image, not text | Use a text-based PDF (scanned books need OCR — not included) |
| Answer cuts off mid-sentence | `max_output_tokens` is too low | Increase to `1024` in the model config |

---

## 🛠️ Tech Stack

| Layer | Technology | Reason chosen |
|-------|-----------|---------------|
| **LLM** | Google Gemini 2.5 Flash | Free tier, fast, excellent instruction-following |
| **AI SDK** | `google-generativeai` | Official Python SDK for Gemini |
| **Retrieval** | Custom TF-IDF (pure Python) | Zero cost, works offline, no heavy model download |
| **Web UI** | Streamlit 1.32+ | Fast to build, chat widgets, sidebar, file upload |
| **PDF Parsing** | PyPDF2 | Lightweight, no external dependencies |
| **Terminal UI** | Rich | Colored panels, markdown, tables in the CLI |
| **Config** | python-dotenv | Secure `.env` key management |
| **Language** | Python 3.9+ | Core backend language |
| **Storage** | Plain `.txt` files | Simple, portable, zero database overhead |

---

## 🗺️ Roadmap

- [ ] OCR support for scanned PDF textbooks (Tesseract)
- [ ] Hindi and regional language support (Bengali, Tamil, Telugu...)
- [ ] Voice input — ask questions by speaking (Web Speech API)
- [ ] Offline answer cache — store frequent answers locally
- [ ] Auto quiz generator from loaded textbook chapters
- [ ] Student progress tracking and weak-topic detection
- [ ] BM25 retrieval upgrade (better than TF-IDF for short queries)
- [ ] Teacher dashboard to upload content and monitor usage
- [ ] Deploy to Streamlit Community Cloud (free hosting)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/hindi-support`
3. Commit your changes: `git commit -m "Add Hindi tokenizer for TF-IDF"`
4. Push and open a Pull Request

Please keep the **zero-cost principle** in mind — avoid adding dependencies that require paid APIs.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Google AI Studio](https://aistudio.google.com) — for the free Gemini API that makes this possible
- [Streamlit](https://streamlit.io) — for making beautiful Python web apps effortless
- [NCERT](https://ncert.nic.in/textbook.php) — for free, high-quality textbooks for all classes
- Built as a submission for **Project 1: The Education Tutor for Remote India**

---

## 👥 Developers

| Name | Email |
|---|---|---|
| **Meghma Das** | meghmadas@mcsinfo.in |
| **Argha Pal** | a1910pal@gmail.com |

**Instructor:** Mr. Sachin Balo (`sachin.balo@mckvie.edu.in`)  
HOD & Assistant Professor, Information Technology  
MCKV Institute of Engineering

---
<div align="center">

<br/>

**Made with ❤️ for students in rural India**

*Every question deserves an answer — regardless of where you live or what you can afford.*

<br/>

[![Star this repo](https://img.shields.io/github/stars/M-das2004/edututor-ai?style=social)](https://github.com/YOUR_USERNAME/edututor-ai)

</div>
