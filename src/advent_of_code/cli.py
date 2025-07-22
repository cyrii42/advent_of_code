from typing import Annotated
import datetime as dt

import typer
from loguru import logger
from rich import print
from rich.table import Table
from bs4 import BeautifulSoup

from advent_of_code.constants import LATEST_AOC_YEAR, SOLUTIONS_DIR, TZ
from advent_of_code.models import Puzzle, PuzzleAnswer, ResponseType
from advent_of_code.exceptions import (PuzzleNotFound, PuzzleAnswerAlreadySubmitted, 
                                       PuzzleLevelAlreadySolved, AOCLoginException, ElementNotFound)
from advent_of_code.logging_config import setup_logging

setup_logging()
app = typer.Typer()

def get_puzzle(year: int, day: int) -> Puzzle:
    try:
        return Puzzle.from_database(year, day)
    except PuzzleNotFound:
        return Puzzle.from_server(year, day)

@app.command(help='Make \"solutions\" subdirectories for 2015 through the latest AOC year (if not already created)')
def makedirs():
    for x in range(2015, LATEST_AOC_YEAR+1):
        new_dir = SOLUTIONS_DIR / f"{x}"
        if not new_dir.exists():
            new_dir.mkdir()

@app.command(help="Refresh puzzle data from the AOC server")
def refresh(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
            day: Annotated[int, typer.Argument(min=1, max=25)]):
    try:
        puzzle = Puzzle.from_server(year, day)
    except (AOCLoginException, ElementNotFound):
        print("Refresh failed.")
        return None
        
    if puzzle:
        puzzle.update_info_on_db()
        print("Puzzle data refreshed!")

@app.command(help='Print puzzle description')
def description(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
                day: Annotated[int, typer.Argument(min=1, max=25)]):
    puzzle = get_puzzle(year, day)
        
    print(puzzle.title + '\n')
    print(puzzle.part_1_description)
    if puzzle.part_2_description:
        print('--- Part Two ---\n')
        print(puzzle.part_2_description)
 
@app.command(help='Print the Advent of Code URL')
def url(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
         day: Annotated[int, typer.Argument(min=1, max=25)]):
    puzzle = get_puzzle(year, day)

    print(puzzle.url)

@app.command(help='Print info about the answers already given to a puzzle')
def answers(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
         day: Annotated[int, typer.Argument(min=1, max=25)]):
    puzzle = get_puzzle(year, day)

    table = Table()
    table.add_column('Timestamp')
    table.add_column('Part', justify='center')
    table.add_column('Answer')
    table.add_column('Response')
    for i, answer in enumerate(puzzle.answers, start=1):
        table.add_row(answer.timestamp_dt.strftime('%b %-d %-I:%M %p'),
                      str(answer.level),
                      answer.answer,
                      str(answer.raw_response))
        if i < len(puzzle.answers):
            table.add_row()
    print(table)

@app.command(help='Print the full dataclass repr for a given puzzle')
def repr(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
         day: Annotated[int, typer.Argument(min=1, max=25)]):
    puzzle = get_puzzle(year, day)

    print(puzzle)

@app.command(help='Print information about a given puzzle')
def info(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
         day: Annotated[int, typer.Argument(min=1, max=25)]):
    puzzle = get_puzzle(year, day)

    table = Table(show_header=False)
    table.add_column()
    table.add_column()
    table.add_row('Year', str(puzzle.year))
    table.add_row('Day', str(puzzle.day))
    table.add_row('Title', str(puzzle.title))
    table.add_row()
    table.add_row('Part One', str(puzzle.part_1_description))
    if puzzle.part_1_solved:
        table.add_row('Answer', str(puzzle.part_1_answer))
        table.add_row()
        table.add_row('Part Two', str(puzzle.part_2_description))
        if puzzle.part_2_solved:
            table.add_row('Answer', str(puzzle.part_2_answer))

    print(table)

@app.command(help='Print the example for a given puzzle')
def example(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
         day: Annotated[int, typer.Argument(min=1, max=25)]):
    puzzle = get_puzzle(year, day)

    print(puzzle.example_text)

@app.command(help='Print the input for a given puzzle')
def input(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
         day: Annotated[int, typer.Argument(min=1, max=25)]):
    puzzle = get_puzzle(year, day)

    print(puzzle.input_text)

@app.command(help='Print the full raw HTML for a given puzzle')
def html(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
         day: Annotated[int, typer.Argument(min=1, max=25)]):
    puzzle = get_puzzle(year, day)
    soup = BeautifulSoup(puzzle.raw_html, 'html.parser')
    print(soup.prettify())

# @app.command(help='XXXXXXXXXXXXXXXXXXXXXXXXXXXX')
# def pull(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
#          day: Annotated[int, typer.Argument(min=1, max=25)]):
#     print("NOT IMPLEMENTED YET")

@app.command(help='Submit an answer to the Advent of Code server')
def submit(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
           day: Annotated[int, typer.Argument(min=1, max=25)], 
           answer: Annotated[str, typer.Argument()]):
    puzzle = get_puzzle(year, day)

    try:
        answer_obj = puzzle.submit_answer(answer)
    except (PuzzleAnswerAlreadySubmitted, PuzzleLevelAlreadySolved) as e:
        print(e)
    else:
        print(answer_obj.raw_response)
        if answer_obj.correct:
            refresh(year, day)

if __name__ == "__main__":
    app()
