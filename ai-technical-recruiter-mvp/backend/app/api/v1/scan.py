from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.schemas.scan import ScanRequest, ScanResultResponse
from app.services.codex_analysis import build_scorecard
from app.services.github_ingest import fetch_top_repositories
from app.services.pdf_report import generate_scorecard_pdf

router = APIRouter()


@router.post("/scan", response_model=ScanResultResponse, status_code=status.HTTP_200_OK)
def run_scan(payload: ScanRequest) -> ScanResultResponse:
    """Run a synchronous MVP scan for a GitHub profile URL."""
    try:
        repos = fetch_top_repositories(str(payload.github_url), github_token=settings.github_token)
    except Exception as exc:  # pragma: no cover - defensive boundary
        raise HTTPException(status_code=400, detail=f"Failed to fetch GitHub data: {exc}") from exc

    if not repos:
        raise HTTPException(status_code=404, detail="No repositories found for this GitHub profile")

    scorecard = build_scorecard(str(payload.github_url), repos)
    scan_id = str(uuid4())
    pdf_path = generate_scorecard_pdf(scan_id, scorecard)

    return ScanResultResponse(
        scan_id=scan_id,
        status="completed",
        pdf_path=pdf_path,
        overall_score=scorecard["overall_score"],
        quality_score=scorecard["quality_score"],
        consistency_score=scorecard["consistency_score"],
        complexity_score=scorecard["complexity_score"],
        repositories=scorecard["repositories"],
        summary=scorecard["summary"],
    )
