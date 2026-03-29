-- Initial schema for AI Technical Recruiter MVP

create table if not exists public.scan_jobs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  github_url text not null,
  plan text not null check (plan in ('single', 'pro')),
  status text not null default 'queued',
  scorecard jsonb,
  pdf_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists scan_jobs_user_id_idx on public.scan_jobs(user_id);
create index if not exists scan_jobs_status_idx on public.scan_jobs(status);
