"""
Seed the Supabase/PostgreSQL database with sample data for local testing.

Run from the backend directory:
    python seed_data.py
"""

from typing import Dict, List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.database import Base, SessionLocal, engine
from app.models.answer import Answer
from app.models.question import Question
from app.models.user import User
from app.models.vote import Vote


def seed_users(db: Session) -> Dict[str, User]:
    """Create baseline users and return a username->User map."""
    user_data = [
        {"username": "sara_dev", "email": "sara@example.com", "password": "password123"},
        {"username": "mike_ops", "email": "mike@example.com", "password": "password123"},
        {"username": "lin_frontend", "email": "lin@example.com", "password": "password123"},
        {"username": "jo_api", "email": "jo@example.com", "password": "password123"},
    ]

    users: Dict[str, User] = {}
    for data in user_data:
        existing = db.query(User).filter(User.email == data["email"]).first()
        if existing:
            users[existing.username] = existing
            continue

        user = User(
            username=data["username"],
            email=data["email"],
            hashed_password=get_password_hash(data["password"]),
        )
        db.add(user)
        db.flush()  # get id before commit
        users[user.username] = user

    return users


def seed_questions(db: Session, users: Dict[str, User]) -> Dict[str, Question]:
    """Create starter questions keyed by title."""
    question_data = [
        {
            "title": "How do I deploy FastAPI on Railway with a Supabase database?",
            "body": "Looking for a simple deploy checklist. Do I need to change anything in uvicorn settings?",
            "username": "sara_dev",
            "view_count": 42,
        },
        {
            "title": "Best way to share JWT between React and FastAPI?",
            "body": "Is storing tokens in httpOnly cookies required here or is localStorage fine for this project?",
            "username": "lin_frontend",
            "view_count": 27,
        },
        {
            "title": "SQLAlchemy relationship cascade not deleting votes",
            "body": "I delete a question but votes remain. What cascade options should be set?",
            "username": "mike_ops",
            "view_count": 18,
        },
        {
            "title": "How to run Alembic migrations in CI?",
            "body": "Need a lightweight command to ensure database is up to date before tests.",
            "username": "jo_api",
            "view_count": 9,
        },
        {
            "title": "FastAPI dependency for current user fails on expired token",
            "body": "I get 401 even when token looks valid. How can I debug JWT expiry?",
            "username": "sara_dev",
            "view_count": 15,
        },
    ]

    questions: Dict[str, Question] = {}
    for data in question_data:
        author = users[data["username"]]
        existing = (
            db.query(Question)
            .filter(Question.title == data["title"], Question.user_id == author.id)
            .first()
        )
        if existing:
            questions[existing.title] = existing
            continue

        question = Question(
            title=data["title"],
            body=data["body"],
            user_id=author.id,
            view_count=data["view_count"],
        )
        db.add(question)
        db.flush()
        questions[question.title] = question

    return questions


def seed_answers(
    db: Session, users: Dict[str, User], questions: Dict[str, Question]
) -> List[Answer]:
    """Create helpful answers tied to the seeded questions."""
    answer_data = [
        {
            "question_title": "How do I deploy FastAPI on Railway with a Supabase database?",
            "username": "jo_api",
            "body": "Set DATABASE_URL from Supabase, then run `alembic upgrade head` before starting uvicorn.",
        },
        {
            "question_title": "How do I deploy FastAPI on Railway with a Supabase database?",
            "username": "mike_ops",
            "body": "Remember to add your frontend URL to CORS or Swagger will work but the app will fail.",
        },
        {
            "question_title": "Best way to share JWT between React and FastAPI?",
            "username": "sara_dev",
            "body": "For this stack localStorage is acceptable, but prefer httpOnly cookies if you add a backend session layer.",
        },
        {
            "question_title": "SQLAlchemy relationship cascade not deleting votes",
            "username": "lin_frontend",
            "body": "Set `cascade='all, delete-orphan'` on votes relationship; also ensure FK constraints are correct.",
        },
        {
            "question_title": "How to run Alembic migrations in CI?",
            "username": "mike_ops",
            "body": "Use `alembic upgrade head` against a throwaway database created in the CI job.",
        },
        {
            "question_title": "FastAPI dependency for current user fails on expired token",
            "username": "jo_api",
            "body": "Decode the JWT and check the `exp` claim; shorten ACCESS_TOKEN_EXPIRE_MINUTES to reproduce.",
        },
    ]

    answers: List[Answer] = []
    for data in answer_data:
        question = questions[data["question_title"]]
        author = users[data["username"]]
        existing = (
            db.query(Answer)
            .filter(
                Answer.question_id == question.id,
                Answer.user_id == author.id,
                Answer.body == data["body"],
            )
            .first()
        )
        if existing:
            answers.append(existing)
            continue

        answer = Answer(
            body=data["body"],
            question_id=question.id,
            user_id=author.id,
        )
        db.add(answer)
        db.flush()
        answers.append(answer)

    return answers


def seed_votes(
    db: Session,
    users: Dict[str, User],
    questions: Dict[str, Question],
    answers: List[Answer],
) -> None:
    """Seed a mix of upvotes/downvotes across questions and answers."""
    votes_data = [
        {"target": "question", "key": "How do I deploy FastAPI on Railway with a Supabase database?", "username": "lin_frontend", "vote_type": "upvote"},
        {"target": "question", "key": "Best way to share JWT between React and FastAPI?", "username": "sara_dev", "vote_type": "upvote"},
        {"target": "question", "key": "SQLAlchemy relationship cascade not deleting votes", "username": "jo_api", "vote_type": "upvote"},
        {"target": "question", "key": "FastAPI dependency for current user fails on expired token", "username": "mike_ops", "vote_type": "downvote"},
        {"target": "answer", "key": "Set DATABASE_URL from Supabase, then run `alembic upgrade head` before starting uvicorn.", "username": "sara_dev", "vote_type": "upvote"},
        {"target": "answer", "key": "Remember to add your frontend URL to CORS or Swagger will work but the app will fail.", "username": "lin_frontend", "vote_type": "upvote"},
        {"target": "answer", "key": "For this stack localStorage is acceptable, but prefer httpOnly cookies if you add a backend session layer.", "username": "jo_api", "vote_type": "upvote"},
        {"target": "answer", "key": "Set `cascade='all, delete-orphan'` on votes relationship; also ensure FK constraints are correct.", "username": "mike_ops", "vote_type": "upvote"},
    ]

    body_to_answer = {answer.body: answer for answer in answers}

    for data in votes_data:
        voter = users[data["username"]]

        if data["target"] == "question":
            question = questions[data["key"]]
            exists = (
                db.query(Vote)
                .filter(Vote.user_id == voter.id, Vote.question_id == question.id)
                .first()
            )
            if exists:
                continue

            vote = Vote(
                user_id=voter.id,
                question_id=question.id,
                vote_type=data["vote_type"],
            )
        else:
            answer = body_to_answer.get(data["key"])
            if answer is None:
                continue

            exists = (
                db.query(Vote)
                .filter(Vote.user_id == voter.id, Vote.answer_id == answer.id)
                .first()
            )
            if exists:
                continue

            vote = Vote(
                user_id=voter.id,
                answer_id=answer.id,
                vote_type=data["vote_type"],
            )

        db.add(vote)


def main() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        users = seed_users(db)
        db.commit()

        questions = seed_questions(db, users)
        db.commit()

        answers = seed_answers(db, users, questions)
        db.commit()

        seed_votes(db, users, questions, answers)
        db.commit()

    print("Database seeded successfully with users, questions, answers, and votes.")


if __name__ == "__main__":
    main()
