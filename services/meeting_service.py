from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_meeting_insights
from core.rag_engine import build_rag_chain


class MeetingService:
    """
    Application service responsible for running the
    end-to-end MeetingMind processing pipeline.
    """

    def process_meeting(
        self,
        source: str,
        language: str = "english"
    ) -> dict:

        if not source or not source.strip():
            raise ValueError("Meeting source cannot be empty.")

        # 1. Audio processing
        chunks = process_input(source)

        # 2. Transcription
        transcript = transcribe_all(
            chunks,
            language=language
        )

        if not transcript.strip():
            raise ValueError("No transcript was generated.")

        # 3. Meeting title
        title = generate_title(transcript)

        # 4. Meeting summary
        summary = summarize(transcript)

        # 5. Structured meeting intelligence
        insights = extract_meeting_insights(transcript)

        # 6. Build RAG pipeline
        rag_chain = build_rag_chain(transcript)

        return {
            "title": title,
            "transcript": transcript,
            "summary": summary,
            "action_items": insights.action_items,
            "key_decisions": insights.decisions,
            "open_questions": insights.open_questions,
            "rag_chain": rag_chain,
        }