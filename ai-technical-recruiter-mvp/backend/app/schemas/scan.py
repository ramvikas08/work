from typing import Literal

from pydantic import BaseModel, HttpUrl


class ScanRequest(BaseModel):
    github_url: HttpUrl
    plan: Literal["single", "pro"]


class RepositoryScore(BaseModel):
    name: str
    url: HttpUrl
    language: str | None = None
    stars: int
    quality_score: float
    consistency_score: float
    complexity_score: float


class ScanResultResponse(BaseModel):
    scan_id: str
    status: Literal["completed"]
    pdf_path: str
    overall_score: float
    quality_score: float
    consistency_score: float
    complexity_score: float
    repositories: list[RepositoryScore]
    summary: str
