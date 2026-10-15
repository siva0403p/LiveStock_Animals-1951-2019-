
from pathlib import Path
import pandas as pd

folder = Path(__file__).parent
csv_path = folder / "livestock_population_historical.csv"
output_path = folder / "livestock_population_historical_updated.csv"

df = pd.read_csv(csv_path)

# Values transcribed from the official DAHD
# BAHS-2015, Table 30, 1951 column.
new_records = pd.DataFrame([
    {
        "Year": 1951,
        "Indicator": "Total Livestock Population",
        "Value": 292.80,
        "Unit": "Million Numbers",
        "Frequency": "Quinquennial",
        "Source": "DAHD, Basic Animal Husbandry Statistics 2015, Table 30, printed page 65",
    },
    {
        "Year": 1951,
        "Indicator": "Population Of Buffalo",
        "Value": 43.40,
        "Unit": "Million Numbers",
        "Frequency": "Quinquennial",
        "Source": "DAHD, Basic Animal Husbandry Statistics 2015, Table 30, printed page 65",
    },
    {
        "Year": 1951,
        "Indicator": "Population Of Donkeys",
        "Value": 1.30,
        "Unit": "Million Numbers",
        "Frequency": "Quinquennial",
        "Source": "DAHD, Basic Animal Husbandry Statistics 2015, Table 30, printed page 65",
    },
])

# Prevent accidental duplicate records.
existing = set(zip(df["Year"], df["Indicator"]))
new_records = new_records[
    ~new_records.apply(
        lambda row: (row["Year"], row["Indicator"]) in existing,
        axis=1,
    )
]

updated = pd.concat([df, new_records], ignore_index=True)
updated = updated.sort_values(
    ["Year", "Indicator"]
).reset_index(drop=True)

updated.to_csv(output_path, index=False)

print("Original CSV preserved:", csv_path.name)
print("Updated CSV saved:", output_path.name)
print("Total rows:", len(updated))
print("\n1951 records:")
print(
    updated[updated["Year"] == 1951][
        ["Year", "Indicator", "Value", "Unit", "Source"]
    ].to_string(index=False)
)
