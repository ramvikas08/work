# AI Technical Recruiter MVP — Project Structure

```text
.
├── AGENTS.md
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── router.py
│   │   │       └── scan.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── schemas/
│   │   │   └── scan.py
│   │   ├── services/
│   │   │   ├── codex_analysis.py
│   │   │   ├── github_ingest.py
│   │   │   ├── pdf_report.py
│   │   │   └── stripe_billing.py
│   │   ├── workers/
│   │   │   └── scan_worker.py
│   │   └── main.py
│   ├── tests/
│   │   └── test_scan_api.py
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── api/
│   │   │   └── scan/route.ts
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   └── github-scan-form.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   └── types.ts
│   ├── .env.example
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   └── tsconfig.json
└── supabase/
    └── migrations/
        └── 0001_init_scan_jobs.sql
```

## Notes
- The existing legacy Django project can coexist during migration; MVP implementation should happen in `frontend/`, `backend/`, and `supabase/`.
- Start with M1 by implementing the scan form + `POST /api/v1/scan` integration.
