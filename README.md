# India Livestock Population — Historical Data Engineering Pipeline

**Internship Project | Government Data Collection, PDF Processing, Data Validation & CSV Automation**

## 1. About the Project

This project focuses on collecting and preparing historical livestock population statistics for India using government-published statistical reports.

As part of an internship data-processing task, three historical indicators were required:

- Total Livestock Population
- Population of Buffalo
- Population of Donkeys

The data is published by the Department of Animal Husbandry and Dairying (DAHD), Government of India, in its *Basic Animal Husbandry Statistics* reports.

These reports contain valuable historical statistics, but the information is presented in lengthy PDF documents. Finding the correct tables, extracting the relevant values, organizing them consistently, checking data quality, and preparing separate datasets can require significant manual effort.

This project addresses that problem by using Python to build a structured data-processing workflow that turns selected government-published statistics into organized CSV deliverables.

The objective is not simply to create spreadsheets. It is to establish a workflow that can be inspected, validated, maintained, and reproduced.

## 2. Business Problem

Historical government data is not always available in a ready-to-use tabular format. Relevant information may be spread across different reports, tables, and pages.

Collecting it manually introduces several challenges:

- Locating the correct historical table in a large PDF.
- Identifying the required indicators and observation years.
- Extracting numerical values without changing their meaning.
- Maintaining consistent column names and measurement units.
- Detecting missing values and duplicate records.
- Preserving the connection between each value and its original source.
- Preparing separate datasets for different business requirements.

A repeatable data pipeline helps reduce repetitive manual work and makes the resulting data easier to review and maintain.

## 3. Project Objectives

The main objectives of this internship task are to:

1. Identify official government sources containing the required livestock statistics.
2. Inspect and locate relevant historical tables within PDF reports.
3. Extract the required population values and observation years.
4. Transform the extracted information into a structured dataset.
5. Validate the dataset using Python and pandas.
6. Preserve source references, units, and transformation details.
7. Generate separate CSV files for the three Jira indicators.
8. Produce a combined dataset and package the deliverables.
9. Document the workflow, assumptions, limitations, and execution steps.

## 4. Official Data Sources

### Primary organisation

**Department of Animal Husbandry and Dairying (DAHD), Government of India**

Official statistics page:

https://dahd.gov.in/schemes/programmes/animal-husbandry-statistics

### Publications referenced

**Basic Animal Husbandry Statistics 2022**

- Table 44: *Livestock & Poultry Population During 1956–2019 — All India*
- Printed page 91.
- Used for the historical observations from 1956 through 2019.
- The published population values are expressed in million numbers.

**Basic Animal Husbandry Statistics 2015**

- Table 30: *Livestock & Poultry Population During 1951–2012 — All India*
- Printed page 65.
- Referenced for the additional 1951 observations.

**Source limitation:** The attempted PDF downloads for the 2015 publication returned HTTP 404. The 1951 values were transcribed from indexed official table content and have not yet been independently checked against the original PDF table. This verification remains outstanding.

The CSV files produced by this project are locally assembled deliverables, not official government-issued datasets.

## 5. Data Coverage

The current working dataset contains 42 records, covering three indicators across 14 observation years.

| Attribute | Details |
|---|---|
| Country | India |
| Geographic coverage | All India |
| Start year | 1951 |
| End year | 2019 |
| Observation years | 14 |
| Indicators | 3 |
| Total records | 42 |
| Original measurement unit | Million numbers |
| Output format | CSV |
| Processing language | Python |

### Observation years

1951, 1956, 1961, 1966, 1972, 1977, 1982, 1987, 1992, 1997, 2003, 2007, 2012, 2019.

Only the available observation years are included. Missing years have not been filled with estimated or interpolated population values.

Although the Jira task specifies a quinquennial frequency, the actual observation years are not uniformly five years apart. The source's reported years are preserved rather than forcing the data into a regular five-year sequence.

## 6. The Complete A–Z Data Pipeline

The project follows an end-to-end workflow, from discovering the data source to generating the final deliverables.

### Phase 1 — Source discovery and inspection

**Scripts:** `01_discover_source.py`, `02_test_report.py`, `03_verify_pdf.py`

The initial scripts explore the government source, test report accessibility, and verify whether a downloaded document is a valid PDF.

The purpose of these steps is to establish the source document before attempting data extraction.

### Phase 2 — Table discovery and identification

**Scripts:** `04_find_livestock_tables.py`, `05_locate_species_tables.py`

These scripts help identify relevant livestock tables and locate the required population indicators within the report.

This reduces the need to inspect every page manually.

### Phase 3 — Historical data extraction

**Script:** `06_extract_table44.py`

The extraction step retrieves the relevant historical population table from the downloaded PDF and prepares its contents for further processing.

The extracted data becomes the input for the transformation stage.

### Phase 4 — Data transformation

**Script:** `07_transform_table44.py`

The transformation script converts the extracted table into a structured CSV with standardized fields.

The dataset includes:

- Year
- Indicator
- Value
- Unit
- Frequency
- Source

This structure makes the data easier to filter, validate, analyze, and export.

### Phase 5 — Initial validation

**Script:** `08_validate_csv.py`

The initial validation script checks:

- Required columns.
- Expected record count.
- Numeric population values.
- Missing values.
- Duplicate year–indicator combinations.
- Selected reference values for 2019.

The purpose is to identify structural problems before adding more historical records.

### Phase 6 — Historical data extension

**Script:** `10_add_1951_records.py`

The existing dataset begins in 1956. This step adds three 1951 records, one for each required indicator, and writes a new updated CSV.

The original CSV is preserved.

Because the historical PDF could not be downloaded, the 1951 values were manually transcribed from indexed official table content. They must be independently verified before the dataset is considered fully audited.

### Phase 7 — Updated dataset validation

**Script:** `11_validate_updated_csv.py`

The updated dataset is checked for:

- Required columns and 42 records.
- Missing values.
- Numeric year and population fields.
- Duplicate year–indicator combinations.
- Expected values for the three indicators in 1951 and 2019.

The reported validation run passed these programmed checks.

These checks establish structural consistency and agreement with the selected expected values. They do not independently verify every historical observation against the original government publications.

### Phase 8 — Deliverable generation

**Script:** `12_generate_jira_deliverables.py`

The final generation script reads the updated CSV, validates its structure, prepares separate indicator datasets, creates a combined dataset, writes source documentation, and packages the output files into a ZIP archive.

The original input CSV remains unchanged.

### Pipeline summary

**Official source → PDF inspection → Table identification → Data extraction → Data transformation → Validation → Historical data extension → Revalidation → Jira-specific CSV generation → Documentation and packaging**

This sequence separates the major processing stages, making it easier to investigate errors and maintain the workflow.

## 7. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Implements the data-processing workflow |
| pandas | Structures, transforms, validates, and exports tabular data |
| pdfplumber | Inspects PDF text and extracts table information |
| requests | Handles HTTP requests and report-access checks |
| BeautifulSoup | Inspects HTML during source discovery |
| Git | Tracks changes to code and documentation |
| GitHub | Hosts the project repository and supports review |

## 8. Data Structure and Units

The source dataset uses a consistent tabular structure.

| Column | Meaning |
|---|---|
| `Year` | Published observation year |
| `Indicator` | Requested livestock population measure |
| `Value` | Population value in the source scale |
| `Unit` | Published measurement unit |
| `Frequency` | Frequency metadata associated with the task |
| `Source` | Reference to the report and table |

### Handling the measurement unit

The source reports values in million numbers, while the Jira tasks specify `Number`.

The pipeline derives an individual-count value by multiplying the source value by one million.

For example:

A source value of 536.76 million produces a derived value of 536,760,000.

The published source value is preserved separately for traceability. Since the original values may be rounded, the derived count is not necessarily the exact number recorded in the original census.

Exact counts should be obtained from the detailed official census tables if the Jira task requires that level of precision.

## 9. Validation and Data Quality

The validation scripts provide automated checks to detect common data problems.

| Check | Purpose |
|---|---|
| Required columns | Confirms the expected dataset structure |
| Record count | Checks the expected number of records |
| Numeric values | Detects non-numeric population values |
| Missing values | Identifies incomplete records |
| Duplicate records | Prevents repeated year–indicator combinations |
| Reference values | Compares selected records with expected values |
| Observation years | Confirms the years represented in the dataset |

The current dataset contains 42 records: 14 observation years multiplied by three indicators.

**Important:** Successful validation means the programmed checks passed. It does not establish that every source figure has been independently audited.

## 10. Project Directory Structure

The repository is intended to be organized as follows:

```text
LiveStock_Animals/
├── scripts/
│   ├── 04_find_livestock_tables.py
│   ├── 05_locate_species_tables.py
│   ├── 06_extract_table44.py
│   ├── 07_transform_table44.py
│   ├── 08_validate_csv.py
│   ├── 10_add_1951_records.py
│   ├── 11_validate_updated_csv.py
│   └── 12_generate_jira_deliverables.py
├── data/
│   ├── livestock_population_historical.csv
│   └── livestock_population_historical_updated.csv
├── jira_deliverables/
│   ├── total_livestock_population.csv
│   ├── population_of_buffalo.csv
│   ├── population_of_donkeys.csv
│   ├── livestock_population_all_indicators.csv
│   ├── livestock_master_source_values.csv
│   └── README_sources_and_method.txt
├── README.md
├── requirements.txt
└── .gitignore
```

This is the intended organization. Move the files into these directories before representing the repository as matching this layout. The initial discovery and troubleshooting scripts can be retained in a separate archive or excluded from the final repository if they are no longer needed.

## 11. Installation and Execution

Install the required Python libraries:

```bash
python -m pip install pandas pdfplumber requests beautifulsoup4
```

Run the scripts from the project root in their dependency order.

```bash
python 04_find_livestock_tables.py
python 05_locate_species_tables.py
python 06_extract_table44.py
python 07_transform_table44.py
python 08_validate_csv.py
python 10_add_1951_records.py
python 11_validate_updated_csv.py
python 12_generate_jira_deliverables.py
```

The extraction steps require the appropriate source PDF and intermediate files to be present. The historical 1951 records currently depend on manual transcription, as described above.

The failed download script is not included in the successful execution sequence.

## 12. Final Deliverables

The output directory contains:

| File | Purpose |
|---|---|
| `total_livestock_population.csv` | Total livestock population data |
| `population_of_buffalo.csv` | Buffalo population data |
| `population_of_donkeys.csv` | Donkey population data |
| `livestock_population_all_indicators.csv` | Combined dataset |
| `livestock_master_source_values.csv` | Master data preserving source values |
| `README_sources_and_method.txt` | Source references and processing notes |

A ZIP archive groups the deliverables for convenient transfer and review.

## 13. Internship Learning Outcomes

This project demonstrates practical experience in:

- Working with official statistical publications.
- Inspecting and extracting information from PDF documents.
- Automating data transformation with Python.
- Using pandas to structure and validate datasets.
- Preserving source information and documenting assumptions.
- Generating reproducible, task-specific CSV deliverables.
- Maintaining a clear distinction between source data and derived values.
- Preparing a project for version control and technical review.

## 14. Current Status and Next Steps

### Completed

- Identified relevant official government publications.
- Extracted the later historical livestock population table.
- Structured the historical dataset.
- Added three 1951 records to the working CSV.
- Passed the programmed structural and selected-value validation checks.
- Generated the three indicator-specific CSVs and combined deliverables.
- Created source and methodology documentation.

### Remaining

- Independently verify the 1951 figures against the original government table.
- Confirm whether Jira requires exact animal counts or accepts counts derived from rounded million-number values.
- Confirm the final output schema with the task owner.
- Organize the repository and test the complete pipeline from a clean environment.

## 15. Conclusion

This internship project develops a repeatable workflow for preparing historical livestock population statistics from government publications.

It brings source discovery, PDF table extraction, data transformation, validation, documentation, and deliverable generation into one Python-based process.

The result is a structured working dataset and a documented workflow that can be reviewed and extended. Final source verification and unit-precision checks remain necessary before the data is treated as fully audited.

---

**Project type:** Data Engineering and Historical Data Processing

**Domain:** Agriculture and Livestock Statistics

**Geographic scope:** India — All India

**Period:** 1951–2019

**Project status:** Working deliverables generated; final source and unit verification pending.#   L i v e S t o c k _ A n i m a l s - 1 9 5 1 - 2 0 1 9 -  
 #   L i v e S t o c k _ A n i m a l s - 1 9 5 1 - 2 0 1 9 -  
 