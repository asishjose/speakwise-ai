
from pydantic import BaseModel, Field


class EmailGeneration(BaseModel):
    subject: str
    body: str
    key_points: list[str] = Field(
        description="Main points covered in the email"
    )
