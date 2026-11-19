
from pydantic import BaseModel, Field


class ToneImprovement(BaseModel):
    original_text: str
    detected_tone: str
    target_tone: str
    improved_text: str
    explanation: str
    changes_made: list[str] = Field(
        description="List of changes made to improve the tone"
    )
