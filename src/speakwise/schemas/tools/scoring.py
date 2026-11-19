
from pydantic import BaseModel, Field


class CommunicationScore(BaseModel):
    grammar_score: float = Field(ge=0, le=10)
    clarity_score: float = Field(ge=0, le=10)
    tone_score: float = Field(ge=0, le=10)
    relevance_score: float = Field(ge=0, le=10)

    overall_score: float = Field(ge=0, le=10)

    strengths: list[str]

    weaknesses: list[str]

    recommendations: list[str]

    evaluation_summary: str
