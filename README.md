# Q&A Platform (Final Submission)

StackOverflow-style Q&A app with auth, questions/answers, voting, and search. Backend (FastAPI + PostgreSQL) and frontend (React + Vite) are live and tested end-to-end.

## Live URLs
- Frontend: https://qa-platform-kohl.vercel.app
- Backend: https://qa-platform-production.up.railway.app
- Swagger: https://qa-platform-production.up.railway.app/docs

## Repository
- Public GitHub: https://github.com/Xiemingminsan/qa-platform

## Local Quick Start
Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set DATABASE_URL and JWT_SECRET
uvicorn main:app --reload
```
Frontend
```bash
cd frontend
npm install
cp .env.example .env  # set VITE_API_URL=http://localhost:8000
npm run dev
```

## Notes
- Tested via the deployed frontend against the production API.
- Tech stack details: see docs/TECH_STACK.md
