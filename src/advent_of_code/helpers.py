import datetime as dt

from rich import print

from advent_of_code.constants import LATEST_AOC_YEAR, SOLUTIONS_DIR, TZ
from advent_of_code.logging_config import setup_logging

setup_logging()

def get_now_string():
    return dt.datetime.now(tz=TZ).strftime("%Y-%m-%dT%H:%M:%S%:z")

def validate_year_and_day(year: int|str, day: int|str) -> None:
    if isinstance(year, str):
        try:
            year = int(year)
        except ValueError:
            raise ValueError(f"Invalid year: {year} (must be between 2015 and {LATEST_AOC_YEAR})")
    if isinstance(day, str):
        try:
            day = int(day)
        except ValueError:
            raise ValueError(f"Invalid day: {day} (must be between 1 and 25)")
        
    if year < 2015 or year > LATEST_AOC_YEAR:
        raise ValueError(f"Invalid year: {year} (must be between 2015 and {LATEST_AOC_YEAR})")
    if day < 1 or day > 25: 
        raise ValueError(f"Invalid day: {day} (must be between 1 and 25)")
    return None

def make_solution_dirs():
    for x in range(2015, LATEST_AOC_YEAR+1):
        new_dir = SOLUTIONS_DIR / f"{x}"
        if not new_dir.exists():
            new_dir.mkdir()

def rename_2022_files():
    ''' Renames files from "2022_dayX.py" to "dayX.py" '''
    DIR = SOLUTIONS_DIR / '2022'
    for file in DIR.iterdir():
        print(file)
        current_stem = file.stem
        new_stem = current_stem[5:]
        new_path = file.with_stem(new_stem)
        file.rename(new_path)




    
    

