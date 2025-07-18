from typing import Annotated
import datetime as dt

import typer
from loguru import logger
from rich import print

from advent_of_code.constants import LATEST_AOC_YEAR, SOLUTIONS_DIR, TZ
from advent_of_code.models import Puzzle, PuzzleAnswer
from advent_of_code.exceptions import PuzzleNotFound, PuzzleAnswerAlreadySubmitted
from advent_of_code.logging_config import setup_logging

setup_logging()
app = typer.Typer()

@app.command(help='Make \"solutions\" subdirectories for 2015 through the latest AOC year (if not already created)')
def makedirs():
    for x in range(2015, LATEST_AOC_YEAR+1):
        new_dir = SOLUTIONS_DIR / f"{x}"
        if not new_dir.exists():
            new_dir.mkdir()

@app.command(help='XXXXXXXXXXXXXXXXXXXXXXXXXXXX')
def description(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
                day: Annotated[int, typer.Argument(min=1, max=26)]):
    try:
        puzzle = Puzzle.from_database(year, day)
    except PuzzleNotFound:
        puzzle = Puzzle.from_server(year, day)
        
    print(puzzle.title + '\n')
    print(puzzle.part_1_description)
    if puzzle.part_2_description:
        print('--- Part Two ---\n')
        print(puzzle.part_2_description)

@app.command(help='XXXXXXXXXXXXXXXXXXXXXXXXXXXX')
def pull(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
         day: Annotated[int, typer.Argument(min=1, max=26)]):
    print("NOT IMPLEMENTED YET")

@app.command(help='Submit an answer to the Advent of Code server')
def submit(year: Annotated[int, typer.Argument(min=2015, max=LATEST_AOC_YEAR)], 
           day: Annotated[int, typer.Argument(min=1, max=26)], 
           answer: Annotated[str, typer.Argument()]):
    try:
        puzzle = Puzzle.from_database(year, day)
    except PuzzleNotFound:
        puzzle = Puzzle.from_server(year, day)

    level = 2 if puzzle.part_1_solved else 1

    answer_obj = PuzzleAnswer(puzzle_id=puzzle.id,
                              year=year,
                              day=day,
                              level=level,
                              answer=answer)

    try:
        answer_obj.submit()
    except PuzzleAnswerAlreadySubmitted:
        answer_obj.get_info_from_sql()
        print(answer_obj)
        print(f"Answer {answer} already submitted on",
              f"{answer_obj.timestamp_dt.strftime("%Y-%m-%d @ %-I:%M:%S %p")}",
              f"({((dt.datetime.now(tz=TZ) - answer_obj.timestamp_dt).seconds) // 60} minutes ago)")
    else:
        print(answer_obj)
        print(answer_obj.raw_response)

if __name__ == "__main__":
    app()
