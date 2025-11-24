from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer
from app.models.vote import Vote
from app.schemas.answer import Answer as AnswerSchema, AnswerCreate, AnswerUpdate
from app.core.deps import get_current_user

router = APIRouter(tags=["Answers"])


def calculate_answer_vote_score(db: Session, answer_id: int) -> int:
    """Calculate vote score for an answer."""
    upvotes = db.query(Vote).filter(
        Vote.answer_id == answer_id,
        Vote.vote_type == "upvote"
    ).count()

    downvotes = db.query(Vote).filter(
        Vote.answer_id == answer_id,
        Vote.vote_type == "downvote"
    ).count()

    return upvotes - downvotes


@router.get("/questions/{question_id}/answers", response_model=List[AnswerSchema])
def get_answers(question_id: int, db: Session = Depends(get_db)):
    """Get all answers for a question."""
    # Check if question exists
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    answers = db.query(Answer).filter(Answer.question_id == question_id).all()

    # Enrich with vote scores
    result = []
    for a in answers:
        answer_dict = {
            "id": a.id,
            "body": a.body,
            "question_id": a.question_id,
            "user_id": a.user_id,
            "created_at": a.created_at,
            "updated_at": a.updated_at,
            "vote_score": calculate_answer_vote_score(db, a.id),
            "author_username": a.author.username
        }
        result.append(AnswerSchema(**answer_dict))

    return result


@router.post("/questions/{question_id}/answers", response_model=AnswerSchema, status_code=status.HTTP_201_CREATED)
def create_answer(
    question_id: int,
    answer_data: AnswerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new answer for a question."""
    # Check if question exists
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    new_answer = Answer(
        body=answer_data.body,
        question_id=question_id,
        user_id=current_user.id
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    # Return with enriched data
    answer_dict = {
        "id": new_answer.id,
        "body": new_answer.body,
        "question_id": new_answer.question_id,
        "user_id": new_answer.user_id,
        "created_at": new_answer.created_at,
        "updated_at": new_answer.updated_at,
        "vote_score": 0,
        "author_username": current_user.username
    }

    return AnswerSchema(**answer_dict)


@router.put("/answers/{answer_id}", response_model=AnswerSchema)
def update_answer(
    answer_id: int,
    answer_data: AnswerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an answer (only by owner)."""
    answer = db.query(Answer).filter(Answer.id == answer_id).first()

    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )

    if answer.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this answer"
        )

    if answer_data.body is not None:
        answer.body = answer_data.body

    db.commit()
    db.refresh(answer)

    # Return with enriched data
    answer_dict = {
        "id": answer.id,
        "body": answer.body,
        "question_id": answer.question_id,
        "user_id": answer.user_id,
        "created_at": answer.created_at,
        "updated_at": answer.updated_at,
        "vote_score": calculate_answer_vote_score(db, answer.id),
        "author_username": current_user.username
    }

    return AnswerSchema(**answer_dict)


@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    answer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an answer (only by owner)."""
    answer = db.query(Answer).filter(Answer.id == answer_id).first()

    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )

    if answer.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this answer"
        )

    db.delete(answer)
    db.commit()

    return None
