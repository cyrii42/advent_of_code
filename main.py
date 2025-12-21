import datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo

import sqlalchemy as db
from loguru import logger
from rich import print

from advent_of_code.constants import SQLITE_URL, TZ
from advent_of_code.local import get_puzzle_from_local
from advent_of_code.models import Puzzle, PuzzleAnswer
from advent_of_code.sql_functions import get_puzzle_from_db_by_year_and_day
from advent_of_code.sql_schema import answers_table, puzzles_table


def main():
    puzzle = Puzzle.from_database(2015, 6)
    print(puzzle)
    
if __name__ == "__main__":
    main()
