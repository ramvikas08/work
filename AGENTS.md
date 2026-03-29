# AGENTS.md — AI Technical Recruiter MVP

## Mission
Build an MVP that accepts a GitHub profile/repository URL and produces a **Technical Talent Scorecard** PDF.

## Target Architecture
- **Frontend:** Next.js (App Router), Tailwind CSS, Lucide Icons.
- **Backend:** FastAPI (Python).
- **Data/Auth:** Supabase.
- **GitHub Access:** PyGithub.
- **Payments:** Stripe Checkout with:
  - `$19` Single Scan (one-time)
  - `$99` Pro (monthly subscription)

## Working Agreement
1. Keep the project split by boundary:
   - `frontend/` for UI and client-side API orchestration.
   - `backend/` for ingestion, analysis orchestration, scoring, and PDF generation.
   - `supabase/` for schema/migrations and auth-related SQL.
2. Add environment variables to `.env.example` files before introducing runtime dependencies.
3. Use feature branches and small commits tied to one milestone at a time.
4. Prefer typed interfaces/schemas (TypeScript types + Pydantic models) for every API contract.
5. Add basic tests for each new backend route and score calculation module.

## Milestone Plan

### M0 — Scaffolding (current)
- [x] Create baseline folder structure.
- [x] Define integration contracts and TODO stubs.
- [x] Add this coordination file.

### M1 — Input + Scan Trigger
- [ ] Frontend page with a single GitHub URL input and **Scan Candidate** button.
- [ ] FastAPI `POST /api/v1/scan` endpoint accepting URL + plan context.
- [ ] Supabase table for scan jobs + user ownership.

### M2 — GitHub Data Collection
- [ ] Validate and normalize GitHub URL.
- [ ] Use PyGithub to fetch top 3 repositories.
- [ ] Pull README + selected top files per repository.

### M3 — AI Analysis + Scoring
- [ ] Prompt pipeline for code quality, consistency, and complexity (1–10).
- [ ] Aggregate into a "Technical Talent Scorecard" JSON artifact.
- [ ] Persist scorecard metadata in Supabase.

### M4 — PDF Output
- [ ] Render scorecard to downloadable PDF.
- [ ] Expose secure download endpoint.

### M5 — Payments + Access Control
- [ ] Stripe Checkout integration for `$19 Single Scan` and `$99 Pro`.
- [ ] Webhook handling for payment success + subscription state.
- [ ] Enforce scan quotas by plan.

## Contracts (initial)
- Frontend -> Backend:
  - `POST /api/v1/scan` with `{ github_url: string, plan: "single" | "pro" }`
- Backend -> Frontend:
  - `202 Accepted` with `{ scan_id: string, status: "queued" }`
  - `200 OK` result endpoint includes score breakdown and `pdf_url`.

## Definition of Done (MVP)
- User can submit a GitHub URL.
- System analyzes top 3 repos with READMEs/top files.
- System returns scorecard + downloadable PDF.
- Stripe payment path gates scan usage.

## Notes for Agents
- Keep secrets out of VCS.
- Never hardcode API keys.
- If unsure about analysis quality, preserve intermediate artifacts for observability.
