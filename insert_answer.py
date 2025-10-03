import datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo

import sqlalchemy as db
from loguru import logger
from rich import print

from advent_of_code.constants import SQLITE_URL, TZ
from advent_of_code.local import get_puzzle_from_local
from advent_of_code.logging_config import setup_logging
from advent_of_code.models import Puzzle, PuzzleAnswer
from advent_of_code.enums import ResponseType
from advent_of_code.sql_functions import get_puzzle_from_db_by_year_and_day
from advent_of_code.sql_schema import answers_table, puzzles_table

setup_logging()

def write_answer():
    answer = PuzzleAnswer(
            puzzle_id=82,
            year=2018,
            day=7,
            timestamp='2025-10-02T16:43:12-04:00',
            level=2,
            answer='ABLDNFWMCJRVHQITXKEUZOSYPG',
            correct=False,
            raw_response="That's not the right answer.  If you're stuck, make sure you're using the full input data; there are also some general tips on the about page, or you can ask for hints on the subreddit.  Please wait one minute before trying again. [Return to Day 7]",
            response_type=ResponseType.INCORRECT)

    answer.write_to_sql()

if __name__ == '__main__':
    pass