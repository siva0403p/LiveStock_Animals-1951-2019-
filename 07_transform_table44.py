
import pdfplumber
import pandas as pd
from pathlib import Path

PDF_PATH = Path("dahd_publication.pdf")
OUTPUT_PATH = Path("livestock_population_historical.csv")

TARGET_INDICATORS = {
    "Total Livestock": "Total Livestock Population",
    "Buffaloes": "Population Of Buffalo",
    "Donkeys": "Population Of Donkeys",
}

YEARS = [
    "1956", "1961", "1966", "1972", "1977", "1982",
    "1987", "1992", "1997", "2003", "2007", "2012", "2019"
]

def extract_table44(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[111]  # PDF page 112

        for table in page.extract_tables():
            for row in table:
                cells = [str(cell or "").strip() for cell in row]

                if (
                    len(cells) >= 15
                    and cells[1].strip().lower() == "species"
                    and cells[2:15] == YEARS
                ):
                    return table

    raise ValueError(
        "Table 44 header not found. Inspect the PDF extraction output."
    )


def transform_table44(table):
    records = []

    for row in table:
        if not row or len(row) < 15:
            continue

        species = " ".join(
            str(row[1] or "").split()
        ).strip()

        if species not in TARGET_INDICATORS:
            continue

        for year, raw_value in zip(YEARS, row[2:15]):
            raw_value = str(raw_value or "").strip()

            if not raw_value or raw_value.upper() == "NC":
                value = None
            else:
                try:
                    value = float(raw_value)
                except ValueError as exc:
                    raise ValueError(
                        f"Unexpected value {raw_value!r} "
                        f"for {species}, {year}"
                    ) from exc

            records.append({
                "Year": int(year),
                "Indicator": TARGET_INDICATORS[species],
                "Value": value,
                "Unit": "Million Numbers",
                "Frequency": "Quinquennial",
                "Source": (
                    "Basic Animal Husbandry Statistics 2022, "
                    "Table 44, printed page 91"
                ),
            })

    df = pd.DataFrame(records)

    expected_rows = len(TARGET_INDICATORS) * len(YEARS)

    if len(df) != expected_rows:
        raise ValueError(
            f"Expected {expected_rows} records, got {len(df)}. "
            "Check the source table and species labels."
        )

    if df.duplicated(["Year", "Indicator"]).any():
        raise ValueError("Duplicate Year + Indicator records found.")

    return df.sort_values(
        ["Indicator", "Year"]
    ).reset_index(drop=True)


def main():
    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"PDF not found: {PDF_PATH.resolve()}"
        )

    table = extract_table44(PDF_PATH)
    df = transform_table44(table)

    df.to_csv(OUTPUT_PATH, index=False)

    print("\nExtraction and transformation successful.")
    print("Output:", OUTPUT_PATH.resolve())
    print("Rows:", len(df))
    print("Unique years:", df["Year"].nunique())
    print("\nRecords per indicator:")
    print(df.groupby("Indicator").size())
    print("\n2019 validation:")
    print(df[df["Year"] == 2019].to_string(index=False))
    print("\nFirst 10 records:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
