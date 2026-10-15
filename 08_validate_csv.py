
from pathlib import Path
import pandas as pd

# Locate the CSV in the current project folder
csv_path = Path(__file__).parent / "livestock_population_historical.csv"

# Check whether the file exists
if not csv_path.exists():
    print(f"ERROR: CSV file not found: {csv_path}")
    raise SystemExit(1)

# Load the dataset
df = pd.read_csv(csv_path)

print("DATASET VALIDATION")
print("-" * 40)

# 1. Check columns
required_columns = [
    "Year",
    "Indicator",
    "Value",
    "Unit",
    "Frequency",
    "Source",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("FAIL: Missing columns:", missing_columns)
    raise SystemExit(1)

print("PASS: Required columns exist")

# 2. Check expected row count
print(f"Total rows: {len(df)}")
if len(df) == 39:
    print("PASS: Expected 39 rows found")
else:
    print("CHECK: Expected 39 rows; verify the dataset")

# 3. Check years and indicators
print("\nYears found:")
print(sorted(df["Year"].dropna().unique().tolist()))

print("\nIndicators found:")
print(sorted(df["Indicator"].dropna().unique().tolist()))

# 4. Check missing and non-numeric values
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

print("\nMissing values per column:")
print(df[required_columns].isnull().sum())

if df["Value"].isna().any():
    print("FAIL: Some values are missing or non-numeric")
else:
    print("PASS: All values are numeric")

# 5. Check duplicate year-indicator combinations
duplicates = df[df.duplicated(
    subset=["Year", "Indicator"], keep=False
)]

if duplicates.empty:
    print("PASS: No duplicate year-indicator records")
else:
    print("FAIL: Duplicate records found")
    print(duplicates[["Year", "Indicator", "Value"]])

# 6. Verify 2019 values against Table 44

expected_2019 = {
    "Total Livestock Population": 536.76,
    "Population Of Buffalo": 109.85,
    "Population Of Donkeys": 0.12,
}


print("\n2019 source-value checks:")

for indicator, expected_value in expected_2019.items():
    matches = df[
        (df["Year"] == 2019)
        & (df["Indicator"] == indicator)
    ]

    if len(matches) == 1:
        actual_value = matches.iloc[0]["Value"]

        if abs(actual_value - expected_value) < 0.001:
            print(f"PASS: {indicator} = {actual_value}")
        else:
            print(
                f"FAIL: {indicator}; expected {expected_value}, "
                f"found {actual_value}"
            )
    else:
        print(f"FAIL: Missing or duplicate 2019 record for {indicator}")

print("\nValidation finished.")
