from dataclasses import dataclass, field
from typing import Optional, Literal, Self

import sqlalchemy as db
from sqlalchemy.exc import IntegrityError
from bs4 import BeautifulSoup
from loguru import logger

from advent_of_code.constants import SQLITE_URL
from advent_of_code.sql_schema import puzzles_table, answers_table
from advent_of_code.exceptions import (ElementNotFound, AOCLoginException, PuzzleNotFound, 
                                       PuzzleAnswerAlreadySubmitted, PuzzleLevelAlreadySolved)
from advent_of_code.helpers import validate_year_and_day
from advent_of_code.server import get_raw_html_from_server, get_input_from_server
from advent_of_code.html_parsing import (get_puzzle_title_and_descriptions_from_soup,
                                         get_solved_statuses_from_soup, 
                                         get_example_from_soup,
                                         get_answers_from_soup)

from .puzzle_answer import PuzzleAnswer

SQL_ENGINE = db.create_engine(SQLITE_URL)        

@dataclass
class Puzzle:
    year: int
    day: int
    title: str = field(default_factory=str)
    part_1_description: str = field(default_factory=str)
    part_1_solved: bool = field(default=False)
    part_1_answer: str = field(default_factory=str)
    part_2_description: str = field(default_factory=str)
    part_2_solved: bool = field(default=False)
    part_2_answer: str = field(default_factory=str)
    example_text: str = field(default_factory=str, repr=False)
    input_text: str = field(default_factory=str, repr=False)
    raw_html: str = field(default_factory=str, repr=False)
    url: str = field(default_factory=str)
    id: int = field(default=0)
    answers: list[PuzzleAnswer] = field(default_factory=list)

    def __post_init__(self):
        if not self.url:
            self.url = f"https://adventofcode.com/{self.year}/day/{self.day}"
        if not self.id:
            self.id = self.get_sql_id()
        self.answers = self.pull_all_answers_from_db()
        self.check_answers_in_list()

    def update_answers_in_db_answer_table(self) -> None:
        if not self.part_1_answer and not self.part_2_answer:
            logger.debug(f"{self.year} DAY {self.day:02d} (ID: {self.id}) | No correct answers found.")
            return None

        for level in [1, 2]:
            if not [x for x in self.answers if x.correct and x.level == level]:
                answer_to_write = self.part_1_answer if level == 1 else self.part_2_answer 
                if not answer_to_write:
                    continue
                raw_response = "Found in HTML response from AOC server."
                answer_obj = PuzzleAnswer(puzzle_id=self.id, 
                                          year=self.year,
                                          day=self.day,
                                          level=level,
                                          answer=answer_to_write,
                                          correct=True,
                                          raw_response=raw_response)
                answer_obj.write_to_sql()
            else:
                logger.debug(f"{self.year} DAY {self.day:02d} (ID: {self.id}) | All correct answers already found in database.")

    def find_answers_in_raw_html(self) -> None:
        if not self.raw_html:
            return None
        
        soup = BeautifulSoup(self.raw_html, 'html.parser')
        answer_p_tags = [p for p in soup.find_all('p') 
                         if 'Your puzzle answer was' in p.get_text()]

        update_db = False
        for i, tag in enumerate(answer_p_tags, start=1):
            answer_text = tag.find('code').get_text() # type: ignore

            if i == 1 and (answer_text != self.part_1_answer):
                logger.info(f"{self.year} DAY {self.day:02d} (ID: {self.id}) | Adding new Part One answer: {answer_text}")
                self.part_1_answer = answer_text
                self.part_1_solved = True
                update_db = True
            if i == 2 and (answer_text != self.part_2_answer):
                logger.info(f"{self.year} DAY {self.day:02d} (ID: {self.id}) | Adding new Part Two answer: {answer_text}")
                self.part_2_answer = answer_text
                self.part_2_solved = True
                update_db = True

        if update_db:
            self.update_info_on_db()    
            self.update_answers_in_db_answer_table()    
                
    def update_info_on_db(self) -> None:
        if not self.id:
            self.id = self.get_sql_id()

        values_dict = {key: value for key, value in self.__dict__.items() if key != 'answers'}
        logger.debug(f"{self.year} DAY {self.day:02d} (ID: {self.id}) | Updating info on DB: {values_dict}")
        
        with SQL_ENGINE.connect() as conn:
            stmt = (
                db.update(puzzles_table)
                .where(puzzles_table.c.id == self.id)
                .values(**values_dict)
            )
            conn.execute(stmt)
            conn.commit()

    def pull_all_answers_from_db(self) -> list[PuzzleAnswer]:
        with SQL_ENGINE.connect() as conn:
            stmt = (db.select(answers_table)
                      .where(answers_table.c.puzzle_id == self.id))
            result = conn.execute(stmt).fetchall()

            if not result:
                return list()
            else:
                answers = sorted([PuzzleAnswer(**row._asdict()) for row in result],
                              key=lambda a: a.timestamp_dt)
                logger.debug(f"{self.year} DAY {self.day:02d} (ID: {self.id}) | Pulled answers from DB: {answers}")
                return answers

    def check_answers_in_list(self) -> None:
        if not self.answers:
            return None

        correct_answers_part_1 = [x for x in self.answers if x.correct and x.level == 1]
        correct_answers_part_2 = [x for x in self.answers if x.correct and x.level == 2]

        if correct_answers_part_1:
            self.part_1_solved = True
            self.part_1_answer = correct_answers_part_1[0].answer
        if correct_answers_part_2:
            self.part_2_solved = True
            self.part_2_answer = correct_answers_part_2[0].answer

    def submit_answer(self, 
                      answer: str|int, 
                      level: Optional[Literal[1, 2]] = None,
                      force: bool = False
                      ) -> PuzzleAnswer:
        if not isinstance(answer, str):
            answer = str(answer)
        if not level:
            level = 2 if self.part_1_solved else 1

        answer_obj = PuzzleAnswer(puzzle_id=self.id, 
                                  year=self.year,
                                  day=self.day,
                                  level=level, 
                                  answer=answer)

        try:
            answer_obj.submit(force=force)
        except (PuzzleAnswerAlreadySubmitted, PuzzleLevelAlreadySolved) as e:
            logger.debug(e)
            raise
        else:
            self.answers.append(answer_obj)
            self.refresh_data_from_server()
            return answer_obj

    def get_sql_id(self) -> int:
        with SQL_ENGINE.connect() as conn:
            stmt = (db
                    .select(puzzles_table)
                    .where(puzzles_table.c.year == self.year)
                    .where(puzzles_table.c.day == self.day))
            result = conn.execute(stmt).fetchone()
            if result:
                return result.id 
            else:
                return self.write_to_db()  # returns the new primary key

    def write_to_db(self) -> int:
        try:
            with SQL_ENGINE.connect() as conn:
                stmt = (db.insert(puzzles_table)
                          .values(
                              year=self.year,
                              day=self.day,
                              title=self.title,
                              part_1_description=self.part_1_description,
                              part_1_solved=self.part_1_solved,
                              part_1_answer=self.part_1_answer,
                              part_2_description=self.part_2_description,
                              part_2_solved=self.part_2_solved,
                              part_2_answer=self.part_2_answer,
                              example_text=self.example_text,
                              input_text=self.input_text,
                              raw_html=self.raw_html,
                              url=self.url))
                result = conn.execute(stmt)
                logger.debug(f"{self.year} DAY {self.day:02d}) | New SQL Result: {result}")
                assert result.inserted_primary_key
                primary_key = result.inserted_primary_key.tuple()[0]
                conn.commit()
                logger.debug(f"{self.year} DAY {self.day:02d}) | Wrote puzzle to DB (new puzzle ID: {primary_key})")
                return primary_key
        except IntegrityError as e:
            logger.error(f"{self.year} DAY {self.day:02d}) | SQLAlchemy Integrity Error: {e}")
            return -1

    @classmethod
    def from_database(cls, year: int, day: int) -> Self:
        validate_year_and_day(year, day)
        with SQL_ENGINE.connect() as conn:
            stmt = (db.select(puzzles_table)
                    .where(puzzles_table.c.year == year)
                    .where(puzzles_table.c.day == day))
            row = conn.execute(stmt).fetchone()
            if not row:
                raise PuzzleNotFound(f"No puzzle found in database for {year} DAY {day:02f}")
            return cls(**row._asdict())

    def refresh_data_from_server(self):
        self.raw_html = get_raw_html_from_server(self.year, self.day)
        soup = BeautifulSoup(self.raw_html, 'html.parser')

        self.part_1_solved, self.part_2_solved = get_solved_statuses_from_soup(soup)
        self.title, self.part_1_description, self.part_2_description = get_puzzle_title_and_descriptions_from_soup(soup)
        self.part_1_answer, self.part_2_answer = get_answers_from_soup(soup)

    @classmethod
    def from_server(cls, year: int, day: int) -> Self:
        raw_html = get_raw_html_from_server(year, day)
        soup = BeautifulSoup(raw_html, 'html.parser')

        part_1_solved, part_2_solved = get_solved_statuses_from_soup(soup)
        title, part_1_description, part_2_description = get_puzzle_title_and_descriptions_from_soup(soup)
        part_1_answer, part_2_answer = get_answers_from_soup(soup)

        try:
            example_text = get_example_from_soup(soup)
        except ElementNotFound as e:
            logger.debug(f"{year} DAY {day:02d} | {e}")
            example_text = ''

        try:
            input_text = get_input_from_server(year, day)
        except AOCLoginException as e:
            logger.debug(f"{year} DAY {day:02d} | {e}")
            input_text = ''

        return cls(year=year,
                   day=day, 
                   title=title,
                   part_1_description=part_1_description,
                   part_1_solved=part_1_solved,
                   part_1_answer=part_1_answer,
                   part_2_description=part_2_description,
                   part_2_solved=part_2_solved,
                   part_2_answer=part_2_answer,
                   example_text=example_text,
                   input_text=input_text,
                   raw_html=raw_html)
        




if __name__ == "__main__":
    pass