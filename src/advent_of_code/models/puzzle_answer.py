import re
import time
import random
import datetime as dt
from dataclasses import dataclass, field
from typing import Optional, Self

import requests
import humanize
import sqlalchemy as db
from bs4 import BeautifulSoup
from loguru import logger
from rich import print

from advent_of_code.constants import AOC_SESSION, SQLITE_URL, TZ
from advent_of_code.enums import ResponseType
from advent_of_code.helpers import validate_year_and_day
from advent_of_code.sql_schema import answers_table
from advent_of_code.exceptions import InvalidAnswerLevel, PuzzleAnswerAlreadySubmitted, PuzzleLevelAlreadySolved, PuzzleAnswerNotFound


SQL_ENGINE = db.create_engine(SQLITE_URL)

def get_now_string():
    return dt.datetime.now(tz=TZ).strftime("%Y-%m-%dT%H:%M:%S%:z")



@dataclass
class PuzzleAnswer:
    puzzle_id: int
    year: int
    day: int
    level: int
    answer: str
    correct: Optional[bool] = field(default=None)
    timestamp: str = field(default_factory=get_now_string)
    timestamp_dt: dt.datetime = field(init=False)
    response_type: ResponseType = field(default=ResponseType.NOT_YET_SUBMITTED)
    raw_response: str = field(default_factory=str)
    id: int = field(default=0)

    def __post_init__(self):
        if not self.id:
            self.id = self.get_sql_id()
        if self.level not in [1, 2]:
            raise InvalidAnswerLevel(f"Invalid level: {self.level} (must be 1 or 2)")
        if not isinstance(self.answer, str):
            self.answer = str(self.answer)
        self.timestamp_dt = dt.datetime.fromisoformat(self.timestamp).astimezone(TZ)

    @property
    def already_submitted(self) -> bool:
        with SQL_ENGINE.connect() as conn:
            stmt = (db.select(answers_table)
                      .where(answers_table.c.puzzle_id == self.puzzle_id)
                      .where(answers_table.c.level == self.level)
                      .where(answers_table.c.answer == self.answer))
            result = conn.execute(stmt).fetchone()

            if not result:
                return False
            else:
                self.timestamp = result.timestamp
                self.timestamp_dt = dt.datetime.fromisoformat(result.timestamp).astimezone(TZ)
                self.correct = result.correct
                self.raw_response = result.raw_response
                return True

    @property
    def already_solved(self) -> bool:
        with SQL_ENGINE.connect() as conn:
            stmt = (db.select(answers_table)
                      .where(answers_table.c.puzzle_id == self.puzzle_id)
                      .where(answers_table.c.level == self.level)
                      .where(answers_table.c.correct == 1))
            result = conn.execute(stmt).fetchone()

            if not result:
                return False
            else:
                return True

    def get_correct_answer_from_db(self) -> "PuzzleAnswer | None":
        with SQL_ENGINE.connect() as conn:
            stmt = (db.select(answers_table)
                      .where(answers_table.c.puzzle_id == self.puzzle_id)
                      .where(answers_table.c.level == self.level)
                      .where(answers_table.c.correct == 1))
            result = conn.execute(stmt).fetchone()

            if not result:
                return None
            else:
                return PuzzleAnswer(**result._asdict())
        
    def submit(self) -> bool:
        if self.already_submitted:
            self.get_info_from_sql()
            e = (f"{self.year} Day {self.day} Part {self.level}: Answer \"{self.answer}\" already submitted on " + 
                 f"{self.timestamp_dt.strftime("%Y-%m-%d at %-I:%M:%S %p")} " + 
                 f"({humanize.naturaltime(dt.datetime.now(tz=TZ) - self.timestamp_dt)})")
            raise PuzzleAnswerAlreadySubmitted(e)
        
        correct_answer = self.get_correct_answer_from_db()
        if correct_answer:
            e = (f"{self.year} Day {self.day} Part {self.level} already solved on " + 
                 f"{correct_answer.timestamp_dt.strftime("%Y-%m-%d at %-I:%M:%S %p")} " + 
                 f"({humanize.naturaltime(dt.datetime.now(tz=TZ) - correct_answer.timestamp_dt)})")
            raise PuzzleLevelAlreadySolved(e)

        self.response_type, self.raw_response = self.post_to_server()
        self.correct = True if self.response_type == ResponseType.CORRECT else False

        self.write_to_sql()

        return self.correct
            
    def post_to_server(self) -> tuple[ResponseType, str]:     
        url = f"https://adventofcode.com/{self.year}/day/{self.day}/answer"
        resp = requests.post(url, 
                             headers={"Cookie": f"session={AOC_SESSION}"},
                             data={'level': self.level, 'answer': self.answer})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        message = soup.article.get_text() if soup.article else ''
        
        if "That's the right answer" in message:
            return (ResponseType.CORRECT, message)
        if "That's not the right answer" in message:
            if "answer is too high" in message:
                return (ResponseType.INCORRECT_TOO_HIGH, message)
            if "answer is too low" in message:
                return (ResponseType.INCORRECT_TOO_LOW, message)
            else:
                return (ResponseType.INCORRECT, message)
        if "You don't seem to be solving the right level" in message:
            return (ResponseType.WRONG_LEVEL, message)
        if "You gave an answer too recently" in message:
            return (ResponseType.TOO_SOON, message)
        else:
            return (ResponseType.OTHER, message)

    def write_to_sql(self) -> None:
        if self.already_submitted:
            raise PuzzleAnswerAlreadySubmitted
        
        with SQL_ENGINE.connect() as conn:
            stmt = (db.insert(answers_table)
                      .values(
                          puzzle_id=self.puzzle_id,
                          year=self.year,
                          day=self.day,
                          timestamp=self.timestamp,
                          level=self.level,
                          answer=self.answer,
                          correct=self.correct,
                          response_type=self.response_type.name,
                          raw_response=self.raw_response
                        ))
            result = conn.execute(stmt)
            conn.commit()
            
        correct_str = "correct" if self.correct else "incorrect"
        log_msg = (f"{self.year} DAY {self.day:02d} | Answer \"{self.answer}\" " + 
                    f"({correct_str}) written to DB with key {result.inserted_primary_key}.")
        logger.info(log_msg)


    def update_info_on_db(self) -> None:
        if not self.id:
            self.id = self.get_sql_id()
        
        with SQL_ENGINE.connect() as conn:
            stmt = (
                db.update(answers_table)
                .where(answers_table.c.id == self.id)
                .values(puzzle_id=self.puzzle_id,
                        year=self.year,
                        day=self.day,
                        timestamp=self.timestamp,
                        level=self.level,
                        answer=self.answer,
                        correct=self.correct,
                        response_type=self.response_type.name,
                        raw_response=self.raw_response)
            )
            conn.execute(stmt)
            conn.commit()

    def get_sql_id(self) -> int:
        with SQL_ENGINE.connect() as conn:
            stmt = (db.select(answers_table)
                      .where(answers_table.c.puzzle_id == self.puzzle_id)
                      .where(answers_table.c.level == self.level)
                      .where(answers_table.c.answer == self.answer))
            result = conn.execute(stmt).fetchone()

            if not result:
                return 0
            else:
                return result.id

    def get_info_from_sql(self) -> None:
        with SQL_ENGINE.connect() as conn:
            stmt = (db.select(answers_table)
                      .where(answers_table.c.puzzle_id == self.puzzle_id)
                      .where(answers_table.c.level == self.level)
                      .where(answers_table.c.answer == self.answer))
            result = conn.execute(stmt).fetchone()
            
            if result:
                self.timestamp = result.timestamp
                self.timestamp_dt = dt.datetime.fromisoformat(result.timestamp).astimezone(TZ)
                self.correct = result.correct
                self.raw_response = result.raw_response