from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
import os

from models.meeting import (
    ActionItem,
    Decision,
    OpenQuestion,
    MeetingInsights,
)


def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.2,
    )


def extract_meeting_insights(transcript: str) -> MeetingInsights:
    """
    Extract structured meeting intelligence from a transcript.

    The LLM output is validated against Pydantic models so that
    downstream application components receive predictable data.
    """

    llm = get_llm()

    structured_llm = llm.with_structured_output(MeetingInsights)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert meeting intelligence analyst.

Analyze the meeting transcript and extract:

1. Action items
   - The task that needs to be completed
   - The responsible owner, if mentioned
   - The deadline, if mentioned

2. Key decisions
   - The decision that was made
   - Brief context explaining it

3. Open questions
   - Unresolved questions
   - Topics requiring follow-up
   - Brief context when useful

Rules:
- Only extract information supported by the transcript.
- Never invent an owner or deadline.
- If an owner or deadline is not mentioned, use null.
- Do not treat general discussion as a decision.
- Do not treat resolved questions as open questions.
""",
            ),
            (
                "human",
                "Meeting transcript:\n\n{transcript}",
            ),
        ]
    )

    chain = prompt | structured_llm

    return chain.invoke({"transcript": transcript})


def extract_action_items(transcript: str) -> list[ActionItem]:
    """Return structured action items."""
    insights = extract_meeting_insights(transcript)
    return insights.action_items


def extract_key_decisions(transcript: str) -> list[Decision]:
    """Return structured meeting decisions."""
    insights = extract_meeting_insights(transcript)
    return insights.decisions


def extract_questions(transcript: str) -> list[OpenQuestion]:
    """Return structured open questions."""
    insights = extract_meeting_insights(transcript)
    return insights.open_questions