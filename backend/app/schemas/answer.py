from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AnswerBase(BaseModel):
    body: str


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(BaseModel):
    body: Optional[str] = None


class Answer(AnswerBase):
    id: int
    question_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Computed fields
    vote_score: int = 0
    author_username: str = ""

    class Config:
        from_attributes = True
