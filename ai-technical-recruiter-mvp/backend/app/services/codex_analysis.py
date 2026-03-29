"""Scoring helpers for candidate repository analysis."""

from __future__ import annotations

from statistics import mean

from app.services.github_ingest import RepoSnapshot


def _complexity_from_text(text: str) -> float:
    if not text.strip():
        return 1.0

    lines = [line for line in text.splitlines() if line.strip()]
    long_lines = sum(1 for line in lines if len(line) > 100)
    branching = sum(text.count(keyword) for keyword in ["if ", "for ", "while ", "switch", "case ", "try:"])

    score = 3.0 + min(4.0, branching / 25) + min(3.0, long_lines / 40)
    return max(1.0, min(10.0, score))


def _consistency_score(text: str) -> float:
    if not text.strip():
        return 3.0

    snake_case = text.count("_")
    camel_case = sum(1 for token in text.split() if any(ch.isupper() for ch in token[1:]))
    ratio = (snake_case + 1) / (camel_case + 1)
    closeness = 1 / (1 + abs(1 - ratio))
    return round(max(1.0, min(10.0, 4 + closeness * 6)), 2)


def _quality_score(readme: str, files_count: int, stars: int) -> float:
    readme_bonus = 2.0 if len(readme) > 500 else 0.8
    file_bonus = min(3.0, files_count)
    star_bonus = min(3.0, stars / 100)
    return round(max(1.0, min(10.0, 2.0 + readme_bonus + file_bonus + star_bonus)), 2)


def build_scorecard(profile_url: str, repos: list[RepoSnapshot]) -> dict:
    repo_cards = []
    quality_scores = []
    consistency_scores = []
    complexity_scores = []

    for repo in repos:
        corpus = "\n\n".join([repo.readme_text] + [file["content"] for file in repo.top_files])
        quality = _quality_score(repo.readme_text, len(repo.top_files), repo.stars)
        consistency = _consistency_score(corpus)
        complexity = round(_complexity_from_text(corpus), 2)

        quality_scores.append(quality)
        consistency_scores.append(consistency)
        complexity_scores.append(complexity)

        repo_cards.append(
            {
                "name": repo.name,
                "url": repo.html_url,
                "language": repo.language,
                "stars": repo.stars,
                "quality_score": quality,
                "consistency_score": consistency,
                "complexity_score": complexity,
            }
        )

    overall = round(mean(quality_scores + consistency_scores + complexity_scores), 2) if repo_cards else 0.0

    return {
        "profile_url": profile_url,
        "overall_score": overall,
        "quality_score": round(mean(quality_scores), 2) if quality_scores else 0.0,
        "consistency_score": round(mean(consistency_scores), 2) if consistency_scores else 0.0,
        "complexity_score": round(mean(complexity_scores), 2) if complexity_scores else 0.0,
        "repositories": repo_cards,
        "summary": "Automated heuristic analysis (MVP mode).",
    }
