from typing import Literal
from pydantic import BaseModel, Field


class IntentClassification(BaseModel):

    intent: Literal[
        "email_writing",
        "interview_practice",
        "grammar_correction",
        "tone_improvement",
        "public_speaking",
        "conflict_resolution",
        "customer_communication",
        "other"
    ]

    confidence: float = Field(
        ge=0,
        le=1
    )

    reasoning: str