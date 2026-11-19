from typing import Any

from pydantic import BaseModel, Field


class AnalyzeResponse(BaseModel):
    intent: str
    confidence: float = Field(ge=0, le=1)
    reasoning: str


class ToolResultResponse(BaseModel):
    tool_name: str
    output: dict[str, Any] | str | list[Any] | None


class CoachResponse(BaseModel):
    session_id: str
    intent: str
    plan: dict[str, Any]
    status: str
    response: str
    results: list[ToolResultResponse]


class ImproveResponse(BaseModel):
    session_id: str
    improved_text: str
    explanation: str | None = None
    selected_tools: list[str]


class InteractionResponse(BaseModel):
    id: int
    session_id: str
    user_query: str
    detected_intent: str
    selected_tools: list[str]
    generated_response: str
    communication_score: dict[str, Any] | None = None
    created_at: str


class HistoryResponse(BaseModel):
    session_id: str
    interactions: list[InteractionResponse]
    communication_scores: list[dict[str, Any]] = Field(default_factory=list)
