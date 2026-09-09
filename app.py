import streamlit as st
import time
from dotenv import load_dotenv

from core.rag_engine import ask_question
from services.meeting_service import MeetingService


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

meeting_service = MeetingService()

st.set_page_config(
    page_title="MeetingMind",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "pipeline_done" not in st.session_state:
    st.session_state.pipeline_done = False

if "pipeline_steps" not in st.session_state:
    st.session_state.pipeline_steps = {
        "audio": "pending",
        "transcript": "pending",
        "title": "pending",
        "summary": "pending",
        "extract": "pending",
        "rag": "pending"
    }

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def update_step(step, status):
    st.session_state.pipeline_steps[step] = status


def step_icon(status):
    if status == "done":
        return "✅"
    elif status == "active":
        return "🔄"
    elif status == "error":
        return "❌"
    return "⏳"


def display_action_items(action_items):
    if not action_items:
        st.info("No action items found.")
        return

    for i, item in enumerate(action_items, 1):
        st.markdown(f"### {i}. {item.task}")

        col1, col2 = st.columns(2)

        with col1:
            if item.owner:
                st.write(f"👤 **Owner:** {item.owner}")
            else:
                st.write("👤 **Owner:** Not specified")

        with col2:
            if item.deadline:
                st.write(f"📅 **Deadline:** {item.deadline}")
            else:
                st.write("📅 **Deadline:** Not specified")


def display_decisions(decisions):
    if not decisions:
        st.info("No key decisions found.")
        return

    for i, decision in enumerate(decisions, 1):
        st.markdown(f"### {i}. {decision.decision}")

        if decision.context:
            st.write(f"**Context:** {decision.context}")


def display_questions(questions):
    if not questions:
        st.info("No open questions found.")
        return

    for i, question in enumerate(questions, 1):
        st.markdown(f"### {i}. {question.question}")

        if question.context:
            st.write(f"**Context:** {question.context}")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🧠 MeetingMind")

    st.caption(
        "AI-powered meeting intelligence platform"
    )

    st.divider()

    st.subheader("📥 Meeting Input")

    source_type = st.radio(
        "Choose input type",
        ["YouTube URL", "Local File"]
    )

    if source_type == "YouTube URL":

        source = st.text_input(
            "YouTube URL",
            placeholder="https://youtube.com/..."
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload meeting recording",
            type=[
                "mp4",
                "mkv",
                "avi",
                "mov",
                "mp3",
                "wav",
                "m4a",
                "webm"
            ]
        )

        source = None

        if uploaded_file:

            import os

            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(
                upload_dir,
                uploaded_file.name
            )

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            source = file_path

    st.divider()

    language = st.selectbox(
        "🎙️ Transcription Language",
        [
            "english",
            "hinglish"
        ]
    )

    st.divider()

    analyze_button = st.button(
        "🚀 Analyze Meeting",
        use_container_width=True,
        type="primary"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🧠 MeetingMind")

st.markdown(
    """
### AI Meeting Intelligence Platform

Turn long meetings into **structured, searchable intelligence**.

MeetingMind can:
- 🎙️ Transcribe meetings
- 📝 Generate summaries
- 📌 Extract action items
- ✅ Identify key decisions
- ❓ Find unresolved questions
- 🔎 Enable semantic Q&A over the meeting
"""
)

st.divider()


# ============================================================
# PIPELINE STATUS
# ============================================================

progress_placeholder = st.empty()


if analyze_button:

    if not source:
        st.error("Please provide a meeting recording or YouTube URL.")

    else:

        st.session_state.result = None
        st.session_state.pipeline_done = False
        st.session_state.chat_history = []

        for step in st.session_state.pipeline_steps:
            st.session_state.pipeline_steps[step] = "pending"

        try:

            with progress_placeholder.container():

                st.info(
                    "⚙️ MeetingMind pipeline is running..."
                )

                st.markdown(
                    f"""
                    {step_icon("active")} **Audio Processing**

                    {step_icon("pending")} **Transcription**

                    {step_icon("pending")} **Title Generation**

                    {step_icon("pending")} **Meeting Summary**

                    {step_icon("pending")} **Meeting Intelligence Extraction**

                    {step_icon("pending")} **Semantic Search / RAG**
                    """
                )

            # ------------------------------------------------
            # PROCESS MEETING
            # ------------------------------------------------

            update_step("audio", "active")

            result = meeting_service.process_meeting(
                source=source,
                language=language
            )

            # ------------------------------------------------
            # MARK PIPELINE COMPLETE
            # ------------------------------------------------

            for step in [
                "audio",
                "transcript",
                "title",
                "summary",
                "extract",
                "rag"
            ]:
                update_step(step, "done")

            st.session_state.result = result
            st.session_state.pipeline_done = True

            progress_placeholder.success(
                "✅ Meeting analysis completed successfully!"
            )

            time.sleep(0.5)

            progress_placeholder.empty()

            st.rerun()

        except Exception as e:

            for step in st.session_state.pipeline_steps:

                if (
                    st.session_state.pipeline_steps[step]
                    == "active"
                ):
                    st.session_state.pipeline_steps[step] = "error"

            progress_placeholder.error(
                f"❌ Error while processing meeting: {e}"
            )


# ============================================================
# RESULTS
# ============================================================

if st.session_state.result:

    result = st.session_state.result

    # --------------------------------------------------------
    # MEETING TITLE
    # --------------------------------------------------------

    st.header(
        f"📋 {result['title']}"
    )

    st.divider()

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.subheader("📝 Meeting Summary")

    st.markdown(
        result["summary"]
    )

    st.divider()

    # --------------------------------------------------------
    # ACTION ITEMS
    # --------------------------------------------------------

    st.subheader("📌 Action Items")

    display_action_items(
        result["action_items"]
    )

    st.divider()

    # --------------------------------------------------------
    # DECISIONS
    # --------------------------------------------------------

    st.subheader("✅ Key Decisions")

    display_decisions(
        result["key_decisions"]
    )

    st.divider()

    # --------------------------------------------------------
    # OPEN QUESTIONS
    # --------------------------------------------------------

    st.subheader("❓ Open Questions")

    display_questions(
        result["open_questions"]
    )

    st.divider()

    # --------------------------------------------------------
    # TRANSCRIPT
    # --------------------------------------------------------

    with st.expander("📜 View Full Transcript"):

        st.text_area(
            "Meeting Transcript",
            result["transcript"],
            height=400
        )

    st.divider()

    # ========================================================
    # RAG CHAT
    # ========================================================

    st.header("💬 Ask Your Meeting")

    st.caption(
        "Ask questions about the meeting transcript."
    )

    # --------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.chat_history:

        if message["role"] == "user":

            with st.chat_message("user"):
                st.write(message["content"])

        else:

            with st.chat_message("assistant"):
                st.write(message["content"])

    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask something about this meeting..."
    )

    if question:

        # Add user message
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        # Generate answer
        with st.chat_message("assistant"):

            with st.spinner(
                "Searching the meeting..."
            ):

                try:

                    answer = ask_question(
                        result["rag_chain"],
                        question
                    )

                    st.write(answer)

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except Exception as e:

                    error_message = (
                        f"Unable to answer the question: {e}"
                    )

                    st.error(error_message)

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": error_message
                        }
                    )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.info(
        "👈 Add a YouTube meeting or upload a recording "
        "from the sidebar to begin."
    )

    st.markdown(
        """
        ### 🔄 MeetingMind Pipeline

        **Recording**
        ↓  
        **Audio Processing**
        ↓  
        **Whisper / Sarvam Transcription**
        ↓  
        **LLM Analysis**
        ↓  
        **Structured Meeting Intelligence**
        ↓  
        **Vector Database**
        ↓  
        **Semantic Q&A**
        """
    )