import re
import pandas as pd
from PyPDF2 import PdfReader
from datetime import datetime

def parse_lahdot(pdf_path):
    reader = PdfReader(pdf_path)
    
    # Pre-compile regex patterns for better performance
    tasuri_pattern = re.compile(r"\d{1,2},\d(?=[A-Za-z]{2}\b)")
    auto_pattern = re.compile(r"\d{1,2},\d(?=[A-Za-z]{3})")
    date_pattern = re.compile(r'\d{2}\.\d{2}')
    # Pattern for runs: matches date like T05.02, J18.02, L24.04, etc. followed by time
    run_pattern = re.compile(r'[A-ZÄÖÅ][a-zäöå]?(\d{2}\.\d{2})')
    
    # Initialize lists for final data (one row per run)
    all_data = []
    
    for page in reader.pages:
        # Extract text once per page and split into lines
        lines = page.extract_text().split('\n')
        
        # Get title once per page (assuming it's always on line 1)
        page_title = lines[1] if len(lines) > 1 else ""
        
        x = 1
        for i, line in enumerate(lines):
            if "Yht:" not in line:
                continue
                
            # Extract horse basic information
            horse_name = lines[i + 1] if i + 1 < len(lines) else ""
            
            # Age extraction
            horse_age = None
            if i + 2 < len(lines):
                age_str = lines[i + 2]
                age_str = age_str[len(str(x)):]
                age_end = age_str.find("v ")
                age_text = age_str[:age_end] if age_end != -1 else age_str
                horse_age = parse_age(age_text)
            
            # Process records - search in horse name line
            auto_match = auto_pattern.search(horse_name)
            tasuri_match = tasuri_pattern.search(horse_name)
            
            # Auto record processing
            auto_record = None
            auto_record_date = None
            if auto_match:
                auto_time = auto_match.group()
                auto_record = float(auto_time.replace(",", "."))
                auto_date = find_date_for_time(lines, i + 2, auto_time, date_pattern)
                auto_record_date = parse_date(auto_date)
            
            # Tasuri record processing
            tasuri_record = None
            tasuri_record_date = None
            if tasuri_match:
                tasuri_time = tasuri_match.group()
                tasuri_record = float(tasuri_time.replace(",", "."))
                tasuri_date = find_date_for_time(lines, i + 2, tasuri_time, date_pattern)
                tasuri_record_date = parse_date(tasuri_date)
            
            # Extract all runs for this horse
            runs = extract_all_runs(lines, i + 1, run_pattern)
            
            # If no runs found, still add one row with horse basic info
            if not runs:
                all_data.append({
                    "Lähtö": page_title,
                    "Hevonen": horse_name,
                    "Ikä": horse_age,
                    "Ennätys (a)": auto_record,
                    "Ennätys (t)": tasuri_record,
                    "Ennätys pvm (a)": auto_record_date,
                    "Ennätys pvm (t)": tasuri_record_date,
                    "Juoksu pvm": None,
                    "Juoksu aika": None
                })
            else:
                # Add one row for each run, duplicating horse basic info
                for run_date, run_time in runs:
                    all_data.append({
                        "Lähtö": page_title,
                        "Hevonen": horse_name,
                        "Ikä": horse_age,
                        "Ennätys (a)": auto_record,
                        "Ennätys (t)": tasuri_record,
                        "Ennätys pvm (a)": auto_record_date,
                        "Ennätys pvm (t)": tasuri_record_date,
                        "Juoksu pvm": run_date,
                        "Juoksu aika": run_time
                    })
            
            x += 1
    
    return pd.DataFrame(all_data)

def extract_all_runs(lines, start_idx, run_pattern):
    """Extract all runs (date and time) for a horse"""
    runs = []
    
    # Look through the lines following the horse name until we hit the next horse
    for i in range(start_idx, min(start_idx + 20, len(lines))):
        line = lines[i]
        
        # If we hit another "Yht:" line, we've reached the next horse
        if "Yht:" in line:
            break
        
        # Check if this line contains run information
        date_match = run_pattern.search(line)
        if date_match:
            # Extract date
            run_date_str = date_match.group(1)
            run_date = parse_date(run_date_str)
            
            # Extract time - look for time patterns after the date
            # Find all time patterns in the line (format: digits,digits)
            time_matches = re.findall(r'\d{1,2},\d+', line)
            
            if time_matches:
                # Take the last time match in the line (most likely the race time)
                last_time_str = time_matches[-1][:4]
                try:
                    run_time = float(last_time_str.replace(',', '.'))
                    runs.append((run_date, run_time))
                except ValueError:
                    runs.append((run_date, None))
            else:
                runs.append((run_date, None))
    
    return runs

def parse_age(age_text):
    """Convert age text to number"""
    if not age_text or not age_text.strip():
        return None
    
    # Remove any non-digit characters and convert to int
    age_digits = re.findall(r'\d+', age_text.strip())
    if age_digits:
        return int(age_digits[0])
    return None

def parse_date(date_str):
    """Parse date string (DD.MM format) to datetime, handling year logic"""
    if not date_str:
        return None
    
    try:
        # Parse DD.MM format
        day, month = map(int, date_str.split('.'))
        
        # Get current date
        today = datetime.now()
        current_year = today.year
        
        # Try current year first
        try_date = datetime(current_year, month, day)
        
        # If the date is in the future, use last year
        if try_date > today:
            try_date = datetime(current_year - 1, month, day)
        
        return try_date
    except (ValueError, AttributeError):
        return None

def find_date_for_time(lines, start_idx, time_str, date_pattern, max_search=15):
    """Helper function to find date for a given time record"""
    for y in range(2, min(max_search, len(lines) - start_idx)):
        try:
            line = lines[start_idx + y]
            if time_str in line:
                date_match = date_pattern.search(line)
                return date_match.group() if date_match else None
        except IndexError:
            break
    return None


def find_matching_hevonen(result_hevonen, score_hevoset):
	for hevonen in score_hevoset:
		if hevonen in result_hevonen:
			return hevonen
	return None
