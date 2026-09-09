from pydantic import BaseModel, Field
from typing import Optional, List


class ActionItem(BaseModel):
    task: str = Field(description="The task that needs to be completed")
    owner: Optional[str] = Field(
        default=None,
        description="Person responsible for the task"
    )
    deadline: Optional[str] = Field(
        default=None,
        description="Deadline if mentioned in the meeting"
    )


class Decision(BaseModel):
    decision: str = Field(
        description="A key decision made during the meeting"
    )
    context: Optional[str] = Field(
        default=None,
        description="Brief context explaining the decision"
    )


class OpenQuestion(BaseModel):
    question: str = Field(
        description="An unresolved question or follow-up topic"
    )
    context: Optional[str] = Field(
        default=None,
        description="Relevant context from the meeting"
    )


class MeetingInsights(BaseModel):
    action_items: List[ActionItem] = Field(default_factory=list)
    decisions: List[Decision] = Field(default_factory=list)
    open_questions: List[OpenQuestion] = Field(default_factory=list)