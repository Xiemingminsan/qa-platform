from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from app.db.database import get_db
from app.models.user import User
from app.models.question import Question
from app.models.vote import Vote
from app.schemas.question import Question as QuestionSchema, QuestionCreate, QuestionUpdate
from app.core.deps import get_current_user

router = APIRouter(prefix="/questions", tags=["Questions"])


def calculate_vote_score(db: Session, question_id: int) -> int:
    """Calculate vote score for a question."""
    upvotes = db.query(Vote).filter(
        Vote.question_id == question_id,
        Vote.vote_type == "upvote"
    ).count()

    downvotes = db.query(Vote).filter(
        Vote.question_id == question_id,
        Vote.vote_type == "downvote"
    ).count()

    return upvotes - downvotes


@router.get("/", response_model=List[QuestionSchema])
def get_questions(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all questions with optional search."""
    query = db.query(Question)

    if search:
        query = query.filter(Question.title.ilike(f"%{search}%"))

    questions = query.order_by(desc(Question.created_at)).offset(skip).limit(limit).all()

    # Enrich with vote scores and answer counts
    result = []
    for q in questions:
        question_dict = {
            "id": q.id,
            "title": q.title,
            "body": q.body,
            "user_id": q.user_id,
            "view_count": q.view_count,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
            "vote_score": calculate_vote_score(db, q.id),
            "answer_count": len(q.answers),
            "author_username": q.author.username
        }
        result.append(QuestionSchema(**question_dict))

    return result


@router.get("/{question_id}", response_model=QuestionSchema)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Get a specific question by ID."""
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    # Increment view count
    question.view_count += 1
    db.commit()

    # Return with enriched data
    question_dict = {
        "id": question.id,
        "title": question.title,
        "body": question.body,
        "user_id": question.user_id,
        "view_count": question.view_count,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
        "vote_score": calculate_vote_score(db, question.id),
        "answer_count": len(question.answers),
        "author_username": question.author.username
    }

    return QuestionSchema(**question_dict)


@router.post("/", response_model=QuestionSchema, status_code=status.HTTP_201_CREATED)
def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new question."""
    new_question = Question(
        title=question_data.title,
        body=question_data.body,
        user_id=current_user.id
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    # Return with enriched data
    question_dict = {
        "id": new_question.id,
        "title": new_question.title,
        "body": new_question.body,
        "user_id": new_question.user_id,
        "view_count": new_question.view_count,
        "created_at": new_question.created_at,
        "updated_at": new_question.updated_at,
        "vote_score": 0,
        "answer_count": 0,
        "author_username": current_user.username
    }

    return QuestionSchema(**question_dict)


@router.put("/{question_id}", response_model=QuestionSchema)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a question (only by owner)."""
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    if question.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this question"
        )

    # Update fields
    if question_data.title is not None:
        question.title = question_data.title
    if question_data.body is not None:
        question.body = question_data.body

    db.commit()
    db.refresh(question)

    # Return with enriched data
    question_dict = {
        "id": question.id,
        "title": question.title,
        "body": question.body,
        "user_id": question.user_id,
        "view_count": question.view_count,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
        "vote_score": calculate_vote_score(db, question.id),
        "answer_count": len(question.answers),
        "author_username": current_user.username
    }

    return QuestionSchema(**question_dict)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a question (only by owner)."""
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    if question.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this question"
        )

    db.delete(question)
    db.commit()

    return None
