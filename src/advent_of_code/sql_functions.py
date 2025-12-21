import sqlalchemy as db
from sqlalchemy.orm import Session
from loguru import logger

from advent_of_code.constants import SQLITE_URL
from advent_of_code.models import Puzzle, PuzzleAnswer
from advent_of_code.sql_schema import answers_table, metadata_obj, puzzles_table
from advent_of_code.helpers import validate_year_and_day
from advent_of_code.local import get_puzzle_from_local, get_all_puzzles_from_local
from advent_of_code.exceptions import PuzzleNotFound, PuzzleAnswerNotFound

SQL_ENGINE = db.create_engine(SQLITE_URL)

def create_all_tables() -> None:
    metadata_obj.create_all(SQL_ENGINE, checkfirst=True)

def create_puzzles_table() -> None:
    puzzles_table.create(SQL_ENGINE, checkfirst=True)

def create_answers_table() -> None:
    answers_table.create(SQL_ENGINE, checkfirst=True)

def drop_all_tables() -> None:
    metadata_obj.drop_all(SQL_ENGINE)

def drop_puzzles_table() -> None:
    puzzles_table.drop(SQL_ENGINE)

def drop_answers_table() -> None:
    answers_table.drop(SQL_ENGINE)


def delete_and_replace_all_puzzles_on_db() -> None:
    drop_puzzles_table()
    create_puzzles_table()
    write_all_puzzles_to_db()
    
def write_all_puzzles_to_db() -> None:
    puzzle_list = get_all_puzzles_from_local()
    with Session(SQL_ENGINE) as session:
        for puzzle in puzzle_list:
            sql_puzzle = puzzle.get_sql_object()
            session.add(sql_puzzle)
        session.commit()     

def sql_tests():
    metadata_obj.create_all(SQL_ENGINE)
    with Session(SQL_ENGINE) as session:
        for year in range(2015, 2025):
            for day in range(1, 26):
                puzzle = get_puzzle_from_local(year, day)
                sql_puzzle = puzzle.get_sql_object()
                session.add(sql_puzzle)
                session.commit()     



def get_all_puzzles_from_db() -> list[Puzzle]:
    with SQL_ENGINE.connect() as conn:
        stmt = db.select(puzzles_table)
        response = conn.execute(stmt).fetchall()
        if not response:
            raise PuzzleNotFound("No puzzles found in database")
        return [Puzzle(**row._asdict()) for row in response]

def get_puzzle_from_db_by_id(id: int) -> Puzzle:
    with SQL_ENGINE.connect() as conn:
        stmt = (db.select(puzzles_table)
                  .where(puzzles_table.c.id == id))
        row = conn.execute(stmt).fetchone()
        if not row:
            raise PuzzleNotFound(f"No puzzle found in database with ID {id}")
        return Puzzle(**row._asdict())

def get_puzzle_from_db_by_year_and_day(year: int, day: int) -> Puzzle:
    validate_year_and_day(year, day)
    with SQL_ENGINE.connect() as conn:
        stmt = (db.select(puzzles_table)
                  .where(puzzles_table.c.year == year)
                  .where(puzzles_table.c.day == day))
        row = conn.execute(stmt).fetchone()
        if not row:
            raise PuzzleNotFound(f"No puzzle found in database for {year} DAY {day:02f}")
        return Puzzle(**row._asdict())




def get_all_answers_from_db() -> list[PuzzleAnswer]:
    with SQL_ENGINE.connect() as conn:
        stmt = db.select(answers_table)
        response = conn.execute(stmt).fetchall()
        if not response:
            raise PuzzleAnswerNotFound("No puzzle answers found in database")
        return [PuzzleAnswer(**row._asdict()) for row in response]

def get_answer_by_id(id: int) -> PuzzleAnswer:
    with SQL_ENGINE.connect() as conn:
        stmt = (db.select(answers_table)
                  .where(answers_table.c.id == id))
        row = conn.execute(stmt).fetchone()
        if not row:
            raise PuzzleAnswerNotFound(f"No puzzle answer found in database with ID {id}")
        return PuzzleAnswer(**row._asdict())

def get_answers_by_year_and_day(year: int, day: int) -> list[PuzzleAnswer]:
    validate_year_and_day(year, day)
    puzzle = get_puzzle_from_db_by_year_and_day(year, day)
    with SQL_ENGINE.connect() as conn:
        stmt = (db.select(answers_table)
                  .where(answers_table.c.puzzle_id == puzzle.id))
        rows = conn.execute(stmt).fetchall()
        return [PuzzleAnswer(**row._asdict()) for row in rows]

def fix_manual_raw_responses():
    old = "Added from results of parsing raw HTML response."
    new = "Found in HTML response from AOC server."
    answer_list = [x for x in get_all_answers_from_db() if x.raw_response == old]

    for answer in answer_list:
        answer.raw_response = new
        answer.update_info_on_db()
        
def find_answers_in_html_text_on_db() -> None:
    puzzle_list = get_all_puzzles_from_db()
    for puzzle in puzzle_list:
        puzzle.find_answers_in_raw_html()
        puzzle.update_answers_in_db_answer_table()

def delete_blank_answers_on_db():
    with SQL_ENGINE.connect() as conn:
        stmt = db.delete(answers_table).where(answers_table.c.answer == "")
        conn.execute(stmt)
        conn.commit()
