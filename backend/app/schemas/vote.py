from pydantic import BaseModel
from typing import Literal


class VoteCreate(BaseModel):
    vote_type: Literal["upvote", "downvote"]


class VoteResponse(BaseModel):
    message: str
    new_score: int
