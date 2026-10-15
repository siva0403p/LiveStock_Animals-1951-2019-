
from pathlib import Path
import pandas as pd

folder = Path(__file__).parent
csv_path = folder / "livestock_population_historical_updated.csv"

df = pd.read_csv(csv_path)

required_columns = [
    "Year", "Indicator", "Value",
    "Unit", "Frequency", "Source"
]

print("UPDATED DATASET VALIDATION")
print("-" * 40)

# 1. File structure and row count
assert all(col in df.columns for col in required_columns), \
    "Required columns are missing"

assert len(df) == 42, f"Expected 42 rows, found {len(df)}"
print("PASS: Required columns and 42 records")

# 2. Check missing values and numeric values
assert df[required_columns].notna().all().all(), \
    "Missing values detected"

df["Year"] = pd.to_numeric(df["Year"], errors="raise")
df["Value"] = pd.to_numeric(df["Value"], errors="raise")

print("PASS: No missing values; Year and Value are numeric")

# 3. Check duplicates
assert not df.duplicated(["Year", "Indicator"]).any(), \
    "Duplicate year-indicator records found"

print("PASS: No duplicate year-indicator records")

# 4. Verify the 1951 and 2019 values
expected = {
    (1951, "Total Livestock Population"): 292.80,
    (1951, "Population Of Buffalo"): 43.40,
    (1951, "Population Of Donkeys"): 1.30,
    (2019, "Total Livestock Population"): 536.76,
    (2019, "Population Of Buffalo"): 109.85,
    (2019, "Population Of Donkeys"): 0.12,
}

for (year, indicator), expected_value in expected.items():
    rows = df[
        (df["Year"] == year)
        & (df["Indicator"] == indicator)
    ]

    assert len(rows) == 1, (
        f"Missing or duplicate record: {year}, {indicator}"
    )

    actual = float(rows.iloc[0]["Value"])

    assert abs(actual - expected_value) < 0.001, (
        f"Incorrect value for {year}, {indicator}: {actual}"
    )

    print(f"PASS: {year} | {indicator} = {actual}")

print("\nYears:", sorted(df["Year"].unique().tolist()))
print("Indicators:", sorted(df["Indicator"].unique().tolist()))
print("\nAll validation checks passed.")
