from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vote_type = Column(String, nullable=False)  # 'upvote' or 'downvote'

    # Nullable foreign keys - only one will be set
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="votes")
    question = relationship("Question", back_populates="votes")
    answer = relationship("Answer", back_populates="votes")

    # Ensure a user can only vote once per question/answer
    __table_args__ = (
        UniqueConstraint('user_id', 'question_id', name='unique_question_vote'),
        UniqueConstraint('user_id', 'answer_id', name='unique_answer_vote'),
    )
