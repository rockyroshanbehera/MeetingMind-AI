# 🧠 MeetingMind-AI

**AI-powered meeting intelligence platform** — turn long meeting recordings (or YouTube links) into structured, searchable intelligence: transcripts, summaries, action items, decisions, open questions, and a chat interface to ask questions about the meeting.

---

## ✨ Features

- 🎙️ **Transcription** — Local speech-to-text using OpenAI Whisper, with support for English and Hinglish (Hindi → English translation via `deep-translator`)
- 📥 **Flexible input** — Analyze a meeting from a **YouTube URL** (downloaded via `yt-dlp`) or an **uploaded recording** (`mp4`, `mkv`, `avi`, `mov`, `mp3`, `wav`, `m4a`, `webm`)
- 📝 **Automatic summaries** — LLM-generated meeting titles and structured summaries
- 📌 **Action item extraction** — Tasks with owner and deadline (when mentioned)
- ✅ **Key decision detection** — Captures decisions made during the meeting, with context
- ❓ **Open question tracking** — Surfaces unresolved questions raised in the meeting
- 🔎 **Semantic Q&A (RAG)** — Ask natural-language questions about the meeting and get answers grounded in the transcript, powered by a local vector store
- 🖥️ **Streamlit UI** — Simple web interface with a live pipeline status tracker

---

## 🔄 Pipeline

```
Recording / YouTube URL
        ↓
  Audio Processing
        ↓
 Whisper Transcription
        ↓
   LLM Analysis
        ↓
Structured Meeting Intelligence
 (Summary · Action Items · Decisions · Questions)
        ↓
   Vector Database
        ↓
   Semantic Q&A
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| UI | [Streamlit](https://streamlit.io/), `streamlit-extras` |
| Audio/Video acquisition | `yt-dlp`, `pydub`, `ffmpeg-python` |
| Speech-to-Text | [OpenAI Whisper](https://github.com/openai/whisper) (local), PyTorch |
| Translation | `deep-translator` (Hindi → English) |
| LLM Orchestration | [LangChain](https://www.langchain.com/) (LCEL) + [Mistral AI](https://mistral.ai/) |
| RAG / Vector Store | [ChromaDB](https://www.trychroma.com/), `sentence-transformers`, HuggingFace embeddings |
| Export | `reportlab`, `fpdf2` |

---

## 📂 Project Structure

```
MeetingMind-AI/
├── app.py                 # Streamlit application entry point (UI, pipeline, chat)
├── main.py                # Core pipeline / CLI entry point
├── config.py               # App settings loaded from environment variables
├── core/                   # RAG engine and core AI logic
├── services/                # Meeting processing service (orchestrates the pipeline)
├── models/models/           # Data models (action items, decisions, questions, etc.)
├── utils/                   # Helper utilities
├── test.py                  # Tests
├── Requirements.txt          # Python dependencies
└── .gitignore
```

> Note: the exact contents of `core/`, `services/`, `models/models/`, and `utils/` may evolve — see the repository for the latest structure.

---

## ⚙️ Prerequisites

- Python **>= 3.10**
- [FFmpeg](https://ffmpeg.org/download.html) installed and available on your system (or configured via `FFMPEG_PATH`)
- A [Mistral AI](https://mistral.ai/) API key (for LLM orchestration)
- (Optional) A [Sarvam AI](https://www.sarvam.ai/) API key, if using Sarvam-based transcription

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/rockyroshanbehera/MeetingMind-AI.git
cd MeetingMind-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r Requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key
WHISPER_MODEL=small
FFMPEG_PATH=C:\ffmpeg\bin
CHROMA_DIR=vector_db
```

| Variable | Description | Default |
|---|---|---|
| `MISTRAL_API_KEY` | API key for Mistral AI (LLM orchestration) | — |
| `SARVAM_API_KEY` | API key for Sarvam AI (optional) | — |
| `WHISPER_MODEL` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large`) | `small` |
| `FFMPEG_PATH` | Path to your local FFmpeg installation | `C:\ffmpeg\bin` |
| `CHROMA_DIR` | Directory for the local Chroma vector store | `vector_db` |

### 5. Run the app

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (typically `http://localhost:8501`) in your browser.

---

## 🖥️ Usage

1. In the sidebar, choose your input type — **YouTube URL** or **Local File**.
2. Select the transcription language (**English** or **Hinglish**).
3. Click **🚀 Analyze Meeting** and watch the pipeline progress through audio processing, transcription, title generation, summarization, intelligence extraction, and RAG indexing.
4. Review the generated **title, summary, action items, key decisions, open questions**, and the **full transcript**.
5. Use the **💬 Ask Your Meeting** chat box to ask questions about the meeting — answers are generated using semantic search over the transcript.

---

## 🗺️ Roadmap Ideas

- [ ] Export meeting intelligence to PDF/TXT (`reportlab` / `fpdf2` are already in the dependency list)
- [ ] Multi-language support beyond English/Hinglish
- [ ] Speaker diarization
- [ ] Cloud vector store option

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## 📄 License

No license has been specified yet for this repository. Please check with the repository owner before reuse.
