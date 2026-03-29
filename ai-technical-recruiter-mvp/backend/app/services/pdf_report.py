"""PDF generation for Technical Talent Scorecard."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas


def generate_scorecard_pdf(scan_id: str, scorecard: dict, output_dir: str = "generated_reports") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(output_dir) / f"{scan_id}.pdf"

    pdf = canvas.Canvas(str(output_path), pagesize=LETTER)
    width, height = LETTER

    y = height - 50
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, y, "Technical Talent Scorecard")

    y -= 30
    pdf.setFont("Helvetica", 11)
    pdf.drawString(40, y, f"Profile: {scorecard['profile_url']}")
    y -= 20
    pdf.drawString(40, y, f"Overall Score: {scorecard['overall_score']}/10")

    y -= 30
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, "Repository Breakdown")

    pdf.setFont("Helvetica", 10)
    for repo in scorecard.get("repositories", []):
        y -= 20
        if y < 80:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 10)
        line = (
            f"{repo['name']} | Q:{repo['quality_score']} "
            f"Cns:{repo['consistency_score']} Cx:{repo['complexity_score']}"
        )
        pdf.drawString(40, y, line)

    pdf.save()
    return str(output_path)
