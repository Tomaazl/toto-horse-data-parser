# Horse Racing Data Parser

A Python script for parsing horse racing data from "käsiohjelma" PDF files downloaded from Veikkaus.fi and converting it to Excel format. The parser extracts horse information, race records, and run history from Finnish horse racing programs.

## Features

- Extracts horse names, ages, and race records from PDF files
- Parses both auto (a) and tasuri (t) record times
- Extracts run history with dates and times
- Handles date parsing with intelligent year detection
- Outputs data to Excel format for easy analysis
- Processes multiple horses and races from a single PDF

## Requirements

Install the required dependencies:

```bash
pip install pandas PyPDF2 openpyxl
```

## Usage

### Basic Usage

```python
from horse_parser import parse_lahdot

# Parse the PDF file
hevosdata = parse_lahdot("ohjelmatiedot.R_13.07.2025.pdf")

# Save to Excel
hevosdata.to_excel("Hevosdata_Riihimaki.xlsx", index=False)
```

### Command Line Usage

Run the script directly:

```bash
python horse_parser.py
```

This will process the default file `ohjelmatiedot.R_13.07.2025.pdf` and create `Hevosdata_Riihimaki.xlsx`.

## Input Format

The parser expects PDF files containing Finnish horse racing program data with the following structure:

- Horse names and basic information
- Race records marked with time patterns (e.g., "1,5" for 1.5 seconds)
- Run history with dates in DD.MM format
- Race titles and program information

## Output Format

The parser generates an Excel file with the following columns:

| Column | Description |
|--------|-------------|
| **Lähtö** | Race/start information |
| **Hevonen** | Horse name |
| **Ikä** | Horse age |
| **Ennätys (a)** | Auto record time |
| **Ennätys (t)** | Tasuri record time |
| **Ennätys pvm (a)** | Auto record date |
| **Ennätys pvm (t)** | Tasuri record date |
| **Juoksu pvm** | Run date |
| **Juoksu aika** | Run time |

## Data Structure

The output contains one row per horse run, with horse basic information duplicated for each run. If a horse has no recorded runs, one row with basic information is still included.

## Key Functions

### `parse_lahdot(pdf_path)`
Main parsing function that processes the entire PDF file.

**Parameters:**
- `pdf_path` (str): Path to the PDF file to parse

**Returns:**
- `pandas.DataFrame`: Parsed horse racing data

### `extract_all_runs(lines, start_idx, run_pattern)`
Extracts all runs for a specific horse from the text lines.

### `parse_age(age_text)`
Converts age text to numeric format.

### `parse_date(date_str)`
Parses DD.MM format dates with intelligent year detection.

### `find_date_for_time(lines, start_idx, time_str, date_pattern, max_search=15)`
Helper function to find the date associated with a specific time record.

## Date Handling

The parser uses intelligent date parsing:
- Dates are expected in DD.MM format
- If a parsed date would be in the future, the previous year is used
- This handles year-end transitions correctly

## Error Handling

The parser includes robust error handling for:
- Missing or malformed data
- Invalid date formats
- PDF parsing errors
- Missing horse information

## Customization

To modify the parser for different PDF formats:

1. **Regex Patterns**: Update the regex patterns in `parse_lahdot()` to match your PDF format
2. **Column Names**: Modify the column names in the data dictionary
3. **Search Parameters**: Adjust `max_search` parameters to control how far the parser looks for related data

## Example

```python
import pandas as pd
from horse_parser import parse_lahdot

# Parse the PDF
data = parse_lahdot("my_race_program.pdf")

# Display basic statistics
print(f"Total horses: {data['Hevonen'].nunique()}")
print(f"Total runs: {len(data)}")

# Save to Excel
data.to_excel("race_data.xlsx", index=False)
```

## Troubleshooting

**Common Issues:**

1. **No data extracted**: Check that the PDF format matches the expected structure
2. **Date parsing errors**: Verify that dates are in DD.MM format
3. **Missing records