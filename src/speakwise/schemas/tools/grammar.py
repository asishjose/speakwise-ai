
from pydantic import BaseModel, Field


class GrammarCorrection(BaseModel):
    original_text: str

    corrected_text: str

    errors_found: list[str] = Field(
        description="List of grammatical errors identified"
    )

    explanations: list[str] = Field(
        description="Explanation of the corrections"
    )

    has_errors: bool
