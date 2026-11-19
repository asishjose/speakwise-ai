
from typing import Literal
from pydantic import BaseModel, Field


class InterviewResult(BaseModel):
    mode: Literal["ask_question", "evaluate_answer"]

    interview_question: str

    answer_feedback: str

    improved_answer: str

    strengths: list[str] = Field(
        description="Strengths identified in the candidate's answer"
    )

    areas_to_improve: list[str] = Field(
        description="Areas where the candidate can improve"
    )

    follow_up_question: str
