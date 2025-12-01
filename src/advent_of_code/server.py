import time

import requests
from loguru import logger

from advent_of_code.constants import AOC_SESSION, DATA_DIR, LATEST_AOC_YEAR
from advent_of_code.helpers import validate_year_and_day
from advent_of_code.exceptions import AOCLoginException

USER_AGENT_STRING = "github.com/cyrii42/advent_of_code by zvaughan@gmail.com"

# def do_initial_pull():
#     for year in range(2020, 2024):
#         for day in range(1, 26):
#             puzzle = Puzzle.from_server(year, day)
#             puzzle.write_data_files()
#             time.sleep(2)

def download_html_file(year: int, day: int) -> None:
    url = f"https://adventofcode.com/{year}/day/{day}"
    resp = requests.get(url, headers={"Cookie": f"session={AOC_SESSION}", 
                                      "User-Agent": USER_AGENT_STRING})
    resp.raise_for_status()

    html = resp.text

    filename = f"aoc_{year}_day_{day}.html"
    filepath = DATA_DIR / str(year) / str(day) / filename

    if isinstance(html, str):
        with open(filepath, 'w') as f:
            f.write(html)
        logger.info(f"{year} DAY {day:02d} | Writing new file: {filepath}")

def download_all_html_files():
    for year in range(2015, LATEST_AOC_YEAR+1):
        for day in range(1, 26):
            download_html_file(year, day)
            time.sleep(5)

def get_raw_html_from_server(year: int, day: int) -> str:
    validate_year_and_day(year, day)
        
    url = f"https://adventofcode.com/{year}/day/{day}"
    resp = requests.get(url, headers={"Cookie": f"session={AOC_SESSION}", 
                                      "User-Agent": USER_AGENT_STRING})
    resp.raise_for_status()
    return resp.text

def get_input_from_server(year: int, day: int) -> str:
    validate_year_and_day(year, day)
    
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    resp = requests.get(url, headers={"Cookie": f"session={AOC_SESSION}", 
                                      "User-Agent": USER_AGENT_STRING})
    if 'Please log in to get your puzzle input.' in resp.text:
        raise AOCLoginException('Please log in to get your puzzle input.')
    else:
        return resp.text.removesuffix('\n')

