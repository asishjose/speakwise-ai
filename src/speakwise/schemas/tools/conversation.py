
from pydantic import BaseModel, Field


class ConversationImprovement(BaseModel):
    original_response: str
    improved_response: str
    explanation: str
    suggestions: list[str] = Field(
        description="Suggestions for better conversational communication"
    )
