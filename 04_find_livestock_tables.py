
from pathlib import Path
import pdfplumber
import re

pdf_path = Path("dahd_publication.pdf")

if not pdf_path.exists():
    raise FileNotFoundError(f"PDF not found: {pdf_path.resolve()}")

keywords = [
    "livestock population",
    "total livestock",
    "population of buffalo",
    "buffalo population",
    "donkey",
    "donkeys",
]

matches = []

with pdfplumber.open(pdf_path) as pdf:
    print("Total pages:", len(pdf.pages))

    for page_number, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        normalized = re.sub(r"\s+", " ", text).lower()

        found = [
            keyword
            for keyword in keywords
            if keyword in normalized
        ]

        if found:
            matches.append((page_number, found, text))

for page_number, found, text in matches:
    print(f"\n{'=' * 60}")
    print(f"PDF page: {page_number}")
    print("Matched keywords:", ", ".join(found))
    print("-" * 60)
    print(text[:1800])

print("\nPages containing relevant keywords:", len(matches))
