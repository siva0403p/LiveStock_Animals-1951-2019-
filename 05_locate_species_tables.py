
import pdfplumber
import re

PDF_PATH = "dahd_publication.pdf"

terms = [
    "donkey",
    "donkeys",
    "asses",
    "buffalo",
    "buffaloes",
    "total livestock",
    "livestock census",
]

with pdfplumber.open(PDF_PATH) as pdf:
    for page_no, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        normalized = re.sub(r"\s+", " ", text).lower()

        found = [term for term in terms if term in normalized]

        if found:
            print(f"\nPDF page {page_no}")
            print("Matches:", ", ".join(found))
            print(text[:1200])
