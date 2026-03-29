"""GitHub data ingestion utilities using PyGithub."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from github import Github
from github.GithubException import GithubException


@dataclass
class RepoSnapshot:
    name: str
    html_url: str
    stars: int
    language: str | None
    readme_text: str
    top_files: list[dict[str, str]]


def parse_github_profile_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc not in {"github.com", "www.github.com"}:
        raise ValueError("Only github.com URLs are supported")

    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        raise ValueError("GitHub username is missing in URL")
    return parts[0]


def _read_file(repo: Any, path: str, max_chars: int = 8_000) -> str:
    try:
        content = repo.get_contents(path)
    except GithubException:
        return ""

    if isinstance(content, list):
        return ""

    decoded = content.decoded_content.decode("utf-8", errors="ignore")
    return decoded[:max_chars]


def fetch_top_repositories(profile_url: str, github_token: str = "", top_n: int = 3) -> list[RepoSnapshot]:
    username = parse_github_profile_url(profile_url)
    client = Github(github_token or None)

    user = client.get_user(username)
    repos = sorted(user.get_repos(), key=lambda repo: (repo.stargazers_count, repo.pushed_at), reverse=True)[:top_n]

    snapshots: list[RepoSnapshot] = []
    for repo in repos:
        readme_text = ""
        try:
            readme = repo.get_readme()
            readme_text = readme.decoded_content.decode("utf-8", errors="ignore")[:10_000]
        except GithubException:
            pass

        top_file_candidates = ["main.py", "app.py", "index.js", "index.ts", "src/main.py", "README.md"]
        top_files: list[dict[str, str]] = []
        for path in top_file_candidates:
            text = _read_file(repo, path)
            if text:
                top_files.append({"path": path, "content": text})
            if len(top_files) >= 3:
                break

        snapshots.append(
            RepoSnapshot(
                name=repo.name,
                html_url=repo.html_url,
                stars=repo.stargazers_count,
                language=repo.language,
                readme_text=readme_text,
                top_files=top_files,
            )
        )

    return snapshots
