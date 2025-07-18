from pathlib import Path

from bs4 import BeautifulSoup
from loguru import logger
from rich.table import Table

from advent_of_code.constants import SOLUTIONS_DIR, CODE_TEMPLATE, LATEST_AOC_YEAR, DATA_DIR
from advent_of_code.models import Puzzle
from advent_of_code.exceptions import ElementNotFound
from advent_of_code.html_parsing import (get_example_from_soup, 
                                         get_puzzle_description_from_soup, 
                                         get_puzzle_title_from_soup, 
                                         get_solved_statuses_from_soup)

def write_code_template(year: int, day: int, overwrite: bool = False) -> None:
    solution_dir = Path(SOLUTIONS_DIR / str(year))

    if solution_dir.exists() and not overwrite:
        return None
    if not solution_dir.exists():
        solution_dir.mkdir()
        
    with open(CODE_TEMPLATE, 'r') as f:
        template_text = f.read()
    with open(solution_dir / f"day{day}.py", 'w') as f:
        f.write(template_text.removesuffix('\n'))

def get_puzzle_from_local(year: int, day: int) -> Puzzle:
    if year < 2015 or year > LATEST_AOC_YEAR:
        raise ValueError(f"Invalid year: {year}")
    if day < 1 or day > 31: 
        raise ValueError(f"Invalid day: {day}")

    filename = f"aoc_{year}_day_{day}.html"
    filepath = DATA_DIR / str(year) / str(day) / filename

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r') as f:
        raw_html = f.read()

    soup = BeautifulSoup(raw_html, 'html.parser')

    part_1_solved, part_2_solved = get_solved_statuses_from_soup(soup)
    
    part_1_description, part_2_description = get_puzzle_description_from_soup(soup)

    title = get_puzzle_title_from_soup(soup)
    part_1_description = part_1_description.replace(title, '')
    part_2_description = part_2_description.replace('--- Part Two ---', '')

    try:
        example_text = get_example_from_soup(soup)
    except ElementNotFound as e:
        logger.debug(f"{year} DAY {day:02d} | {e}")
        example_text = ''

    input_filepath = DATA_DIR / str(year) / str(day) / 'input.txt'
    if input_filepath.exists():
        with open(input_filepath, 'r') as f:
            input_text = f.read()
    else:
        input_text = ''

    return Puzzle(year=year, 
                day=day, 
                title=title,
                part_1_description=part_1_description,
                part_1_solved=part_1_solved,
                part_2_description=part_2_description,
                part_2_solved=part_2_solved,
                example_text=example_text,
                input_text=input_text,
                raw_html=raw_html)

def get_all_puzzles_from_local() -> list[Puzzle]:
    output_list = []
    for year in range(2015, LATEST_AOC_YEAR+1):
        for day in range(1, 26):
            puzzle = get_puzzle_from_local(year, day)
            output_list.append(puzzle)
    return output_list

def assess_examples():
    for year in range(2015, 2021):
        table = Table(title=str(year))
        table.add_column('Day')
        table.add_column('Title')
        table.add_column('Example?')
        for day in range(1, 26):
            puzzle = get_puzzle_from_local(year, day)
            filepath = DATA_DIR / str(year) / str(day) / 'example.txt'
            if not filepath.exists():
                table.add_row(str(day), puzzle.title, str(filepath.exists()))
        print(table)
