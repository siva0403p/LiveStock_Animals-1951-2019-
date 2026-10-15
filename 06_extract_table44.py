
import pdfplumber
from pathlib import Path

pdf_path = Path("dahd_publication.pdf")

# PDF page 112 is index 111 because Python starts at zero.
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[111]

    print("PDF page:", 112)
    print("Extracted text:")
    print(page.extract_text() or "No extractable text")

    print("\nDetected tables:")
    tables = page.extract_tables()

    print("Number of tables:", len(tables))

    for table_number, table in enumerate(tables, start=1):
        print(f"\nTable {table_number}")

        for row in table:
            print(row)
