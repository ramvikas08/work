# AI Technical Recruiter MVP (Standalone Repo)

This directory is a standalone repository layout extracted from the `work` monorepo.

## Included
- `frontend/` (Next.js + Tailwind + Lucide)
- `backend/` (FastAPI + PyGithub + PDF scorecard generation)
- `supabase/` (initial migrations)
- `docs/` (project structure guidance)
- `AGENTS.md` (coordination + milestone plan)

## Quickstart
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Set:
- `frontend/.env.example` -> `.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`
- `backend/.env.example` -> `.env` with at least `GITHUB_TOKEN` (recommended for rate limits)

## Recommended next step
Initialize this folder as a separate git repository and push to a new remote:

```bash
cd ai-technical-recruiter-mvp
git init
git add .
git commit -m "Initial import from work repo"
# create remote repo in your git provider, then:
git remote add origin <new-repo-url>
git branch -M main
git push -u origin main
```
