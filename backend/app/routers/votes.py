from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer
from app.models.vote import Vote
from app.schemas.vote import VoteCreate, VoteResponse
from app.core.deps import get_current_user

router = APIRouter(tags=["Votes"])


def calculate_vote_score(db: Session, question_id: int = None, answer_id: int = None) -> int:
    """Calculate vote score."""
    if question_id:
        upvotes = db.query(Vote).filter(
            Vote.question_id == question_id,
            Vote.vote_type == "upvote"
        ).count()
        downvotes = db.query(Vote).filter(
            Vote.question_id == question_id,
            Vote.vote_type == "downvote"
        ).count()
    else:
        upvotes = db.query(Vote).filter(
            Vote.answer_id == answer_id,
            Vote.vote_type == "upvote"
        ).count()
        downvotes = db.query(Vote).filter(
            Vote.answer_id == answer_id,
            Vote.vote_type == "downvote"
        ).count()

    return upvotes - downvotes


@router.post("/questions/{question_id}/vote", response_model=VoteResponse)
def vote_question(
    question_id: int,
    vote_data: VoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Vote on a question."""
    # Check if question exists
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    # Check if user already voted
    existing_vote = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.question_id == question_id
    ).first()

    if existing_vote:
        # Update existing vote
        if existing_vote.vote_type == vote_data.vote_type:
            # Remove vote if clicking same button
            db.delete(existing_vote)
            db.commit()
            new_score = calculate_vote_score(db, question_id=question_id)
            return VoteResponse(message="Vote removed", new_score=new_score)
        else:
            # Change vote type
            existing_vote.vote_type = vote_data.vote_type
            db.commit()
            new_score = calculate_vote_score(db, question_id=question_id)
            return VoteResponse(message="Vote updated", new_score=new_score)
    else:
        # Create new vote
        new_vote = Vote(
            user_id=current_user.id,
            question_id=question_id,
            vote_type=vote_data.vote_type
        )
        db.add(new_vote)
        db.commit()
        new_score = calculate_vote_score(db, question_id=question_id)
        return VoteResponse(message="Vote added", new_score=new_score)


@router.post("/answers/{answer_id}/vote", response_model=VoteResponse)
def vote_answer(
    answer_id: int,
    vote_data: VoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Vote on an answer."""
    # Check if answer exists
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )

    # Check if user already voted
    existing_vote = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.answer_id == answer_id
    ).first()

    if existing_vote:
        # Update existing vote
        if existing_vote.vote_type == vote_data.vote_type:
            # Remove vote if clicking same button
            db.delete(existing_vote)
            db.commit()
            new_score = calculate_vote_score(db, answer_id=answer_id)
            return VoteResponse(message="Vote removed", new_score=new_score)
        else:
            # Change vote type
            existing_vote.vote_type = vote_data.vote_type
            db.commit()
            new_score = calculate_vote_score(db, answer_id=answer_id)
            return VoteResponse(message="Vote updated", new_score=new_score)
    else:
        # Create new vote
        new_vote = Vote(
            user_id=current_user.id,
            answer_id=answer_id,
            vote_type=vote_data.vote_type
        )
        db.add(new_vote)
        db.commit()
        new_score = calculate_vote_score(db, answer_id=answer_id)
        return VoteResponse(message="Vote added", new_score=new_score)
