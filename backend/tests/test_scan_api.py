from fastapi.testclient import TestClient

from app.main import app
from app.services.github_ingest import RepoSnapshot

client = TestClient(app)


def test_run_scan_success(monkeypatch) -> None:
    def fake_fetch(*_args, **_kwargs):
        return [
            RepoSnapshot(
                name="demo-repo",
                html_url="https://github.com/octocat/demo-repo",
                stars=42,
                language="Python",
                readme_text="A sample README for testing." * 40,
                top_files=[{"path": "main.py", "content": "def main():\n    return 1\n"}],
            )
        ]

    monkeypatch.setattr("app.api.v1.scan.fetch_top_repositories", fake_fetch)
    monkeypatch.setattr("app.api.v1.scan.generate_scorecard_pdf", lambda *_args, **_kwargs: "generated_reports/test.pdf")

    response = client.post(
        "/api/v1/scan",
        json={"github_url": "https://github.com/octocat", "plan": "single"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["pdf_path"] == "generated_reports/test.pdf"
    assert body["repositories"][0]["name"] == "demo-repo"


def test_run_scan_not_found(monkeypatch) -> None:
    monkeypatch.setattr("app.api.v1.scan.fetch_top_repositories", lambda *_args, **_kwargs: [])

    response = client.post(
        "/api/v1/scan",
        json={"github_url": "https://github.com/octocat", "plan": "single"},
    )

    assert response.status_code == 404
