import pdfplumber
from pathlib import Path

def extract_pdf_text(pdf_path: Path) -> list[dict]:
    """Returns a list of {'page': int, 'text': str} per page."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages.append({"page": i, "text": text})
    return pages