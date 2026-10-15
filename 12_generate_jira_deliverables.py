
from pathlib import Path
import pandas as pd
import zipfile

# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "livestock_population_historical_updated.csv"
OUTPUT_DIR = BASE_DIR / "jira_deliverables"

OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================
# 2. LOAD AND VALIDATE SOURCE CSV
# ==========================================

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Cannot find {INPUT_FILE.name} in {BASE_DIR}"
    )

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "Year", "Indicator", "Value",
    "Unit", "Frequency", "Source"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

df["Year"] = pd.to_numeric(df["Year"], errors="raise").astype(int)
df["Value"] = pd.to_numeric(df["Value"], errors="raise")

if df[required_columns].isna().any().any():
    raise ValueError("Missing data found. Fix the input CSV first.")

if df.duplicated(["Year", "Indicator"]).any():
    raise ValueError("Duplicate Year + Indicator records found.")

expected_indicators = {
    "Total Livestock Population",
    "Population Of Buffalo",
    "Population Of Donkeys",
}

if set(df["Indicator"].unique()) != expected_indicators:
    raise ValueError("The indicator names do not match the expected names.")

if len(df) != 42:
    raise ValueError(f"Expected 42 records; found {len(df)}.")

print("PASS: Input CSV validation")
print(f"Records loaded: {len(df)}")

# ==========================================
# 3. PRESERVE ORIGINAL VALUES
# ==========================================
# Source values are expressed in millions.
# Converting rounded millions does NOT guarantee
# an exact original census count.

df["Source_Value_Millions"] = df["Value"]
df["Source_Unit"] = df["Unit"]

df["Derived_Count"] = (
    df["Source_Value_Millions"] * 1_000_000
).round().astype("int64")

df["Conversion_Note"] = (
    "Derived from rounded million-number source value; "
    "not independently verified as an exact census count."
)

# Save a master copy that preserves source values.
master_path = OUTPUT_DIR / "livestock_master_source_values.csv"
df.to_csv(master_path, index=False)

# ==========================================
# 4. CREATE THREE TASK-SPECIFIC CSV FILES
# ==========================================

tasks = {
    "Total Livestock Population": "total_livestock_population.csv",
    "Population Of Buffalo": "population_of_buffalo.csv",
    "Population Of Donkeys": "population_of_donkeys.csv",
}

for indicator, filename in tasks.items():
    subset = df[df["Indicator"] == indicator].copy()

    result = pd.DataFrame({
        "Year": subset["Year"],
        "Indicator": subset["Indicator"],
        "Value": subset["Derived_Count"],
        "Unit": "Number",
        "Source_Value_Millions": subset["Source_Value_Millions"],
        "Source_Unit": subset["Source_Unit"],
        "Frequency": subset["Frequency"],
        "Source": subset["Source"],
        "Conversion_Note": subset["Conversion_Note"],
    })

    result = result.sort_values("Year")

    output_path = OUTPUT_DIR / filename
    result.to_csv(output_path, index=False)

    print(f"Created {filename}: {len(result)} rows")

# ==========================================
# 5. CREATE COMBINED DATASET
# ==========================================

combined = pd.DataFrame({
    "Year": df["Year"],
    "Indicator": df["Indicator"],
    "Value": df["Derived_Count"],
    "Unit": "Number",
    "Source_Value_Millions": df["Source_Value_Millions"],
    "Source_Unit": df["Source_Unit"],
    "Frequency": df["Frequency"],
    "Source": df["Source"],
    "Conversion_Note": df["Conversion_Note"],
})

combined = combined.sort_values(
    ["Year", "Indicator"]
)

combined.to_csv(
    OUTPUT_DIR / "livestock_population_all_indicators.csv",
    index=False,
)

# ==========================================
# 6. DOCUMENT SOURCES AND LIMITATIONS
# ==========================================

readme = """
LIVESTOCK POPULATION DATA - JIRA WORKING FILES
==============================================

Generated locally using Python from the existing project CSV.

Official source organisation:
Department of Animal Husbandry and Dairying (DAHD),
Government of India.

Official statistics page:
https://dahd.gov.in/schemes/programmes/animal-husbandry-statistics

Later figures:
Basic Animal Husbandry Statistics 2022, Table 44,
printed page 91.

1951 figures:
Basic Animal Husbandry Statistics 2015, Table 30,
printed page 65. The values were manually transcribed
from indexed official table content. The PDF download
failed during this workflow, so independently verify
the original document before audited submission.

UNIT CONVERSION:
Source_Value_Millions preserves the published value.
Source_Unit preserves the published unit.
Value is a derived count calculated by multiplying
the published million-number value by 1,000,000.

Because published values may be rounded, derived counts
may not equal exact census counts.

OBSERVATION YEARS:
1951, 1956, 1961, 1966, 1972, 1977, 1982, 1987,
1992, 1997, 2003, 2007, 2012, 2019.

No values were invented for missing years.

These CSV files are locally assembled working files,
not official government-issued documents.
"""

readme_path = OUTPUT_DIR / "README_sources_and_method.txt"
readme_path.write_text(readme.strip() + "\n", encoding="utf-8")

# ==========================================
# 7. CREATE ZIP ARCHIVE
# ==========================================

zip_path = BASE_DIR / "livestock_jira_deliverables.zip"

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in OUTPUT_DIR.iterdir():
        if path.is_file():
            archive.write(path, arcname=path.name)

# ==========================================
# 8. PRINT SUMMARY
# ==========================================

print("\n" + "=" * 45)
print("LOCAL GENERATION COMPLETE")
print("=" * 45)

print("Output folder:", OUTPUT_DIR)
print("ZIP archive:", zip_path)
print("Total records:", len(df))
print("Years:", sorted(df["Year"].unique().tolist()))

print("\nRecords per indicator:")
print(df.groupby("Indicator").size().to_string())

print("\nOriginal CSV was not modified.")
print("Review the README before submitting to Jira.")
