from typing import Literal
from pydantic import BaseModel, Field

ToolName = Literal[
    "email_writer",
    "interview_coach",
    "grammar_checker",
    "tone_improver",
    "speech_coach",
    "conflict_resolution_coach",
    "customer_communication_writer"
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
    