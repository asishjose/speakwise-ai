
from typing import Literal
from pydantic import BaseModel, Field


IntentName = Literal[
    "email_writing",
    "interview_practice",
    "grammar_correction",
    "tone_improvement",
    "conversation_improvement",
    "communication_evaluation",
    "public_speaking",
    "conflict_resolution",
    "customer_communication",
    "other"
]


class IntentClassification(BaseModel):
    intent: IntentName

    confidence: float = Field(
        ge=0,
        le=1
    )

    reasoning: str
