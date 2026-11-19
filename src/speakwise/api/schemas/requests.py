from pydantic import BaseModel, Field, field_validator


class _TextRequest(BaseModel):
    @field_validator("user_input", check_fields=False)
    @classmethod
    def user_input_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("user_input cannot be blank")
        return value


class AnalyzeRequest(_TextRequest):
    user_input: str = Field(min_length=1, max_length=20_000)
    session_id: str | None = Field(default=None, min_length=1, max_length=200)


class CoachRequest(_TextRequest):
    user_input: str = Field(min_length=1, max_length=20_000)
    session_id: str | None = Field(default=None, min_length=1, max_length=200)


class ImproveRequest(_TextRequest):
    user_input: str = Field(min_length=1, max_length=20_000)
    instructions: str | None = Field(default=None, max_length=5_000)
    session_id: str | None = Field(default=None, min_length=1, max_length=200)
