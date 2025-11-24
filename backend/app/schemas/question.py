from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class QuestionBase(BaseModel):
    title: str
    body: Optional[str] = None


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class Question(QuestionBase):
    id: int
    user_id: int
    view_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Computed fields
    vote_score: int = 0
    answer_count: int = 0
    author_username: str = ""

    class Config:
        from_attributes = True
