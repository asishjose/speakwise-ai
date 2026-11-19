from typing import Literal
from pydantic import BaseModel, Field

ToolName = Literal[
    "grammar_tool",
    "tone_tool",
    "email_tool",
    "interview_tool",
    "conversation_tool",
    "scoring_tool"
]

class PlannedAction(BaseModel):

    tool_name: ToolName

    action: str

    required_information: list[str]

class CommunicationPlan(BaseModel):

    user_goal: str

    primary_intent: str

    actions: list[PlannedAction]

    execution_strategy: Literal[
        "single", 
        "sequential",
        "parallel"
    ]

    missing_information: list[str]

    needs_clarification: bool

    clarfication_questions: str | None = None

    reasoning: str
    