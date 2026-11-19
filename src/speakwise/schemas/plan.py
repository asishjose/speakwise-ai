
from typing import Literal
from pydantic import BaseModel, Field

from speakwise.schemas.intent import IntentName


ToolName = Literal[
    "grammar_tool",
    "tone_tool",
    "email_tool",
    "interview_tool",
    "conversation_tool",
    "scoring_tool"
]


class ToolArguments(BaseModel):
    # Grammar Tool
    user_input: str = ""

    # Tone Tool
    target_tone: str = ""

    # Email Tool
    recipient: str = ""
    purpose: str = ""
    context: str = ""
    tone: str = ""

    # Interview Tool
    role: str = ""
    mode: str = ""
    question: str = ""
    candidate_answer: str = ""
    experience_level: str = ""

    # Conversation Tool
    conversation_context: str = ""
    original_response: str = ""
    communication_goal: str = ""


class PlannedAction(BaseModel):
    tool_name: ToolName
    action: str
    required_information: list[str]

    arguments: ToolArguments = Field(
        default_factory=ToolArguments
    )

    use_previous_output: bool = False


class CommunicationPlan(BaseModel):
    user_goal: str
    primary_intent: IntentName
    actions: list[PlannedAction]

    execution_strategy: Literal[
        "single",
        "sequential",
        "parallel"
    ]

    missing_information: list[str]
    needs_clarification: bool
    clarification_question: str | None = None
    reasoning: str
