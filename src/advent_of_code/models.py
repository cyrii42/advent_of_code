import re
import time
import random
import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Self, Literal

import requests
import sqlalchemy as db
from bs4 import BeautifulSoup
from loguru import logger
from rich import print

from advent_of_code.constants import (AOC_SESSION, SQLITE_URL, TZ, DATA_DIR)
from advent_of_code.sql_schema import PuzzleSQL, AnswerSQL, puzzles_table, answers_table
from advent_of_code.exceptions import (ElementNotFound, AOCLoginException, 
                                       InvalidAnswerLevel, PuzzleAnswerAlreadySubmitted)
from advent_of_code.sql_functions import get_puzzle_from_db_by_year_and_day
from advent_of_code.helpers import validate_year_and_day
from advent_of_code.local import write_code_template
from advent_of_code.server import get_input_from_server
from advent_of_code.html_parsing import (get_solved_statuses_from_soup, 
                                         get_puzzle_description_from_soup,
                                         get_example_from_soup)

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

    def submit(self) -> bool:
        if self.already_submitted:
            raise PuzzleAnswerAlreadySubmitted
        
        self.correct, self.raw_response = self.post_to_server()
        self.write_to_sql()

        return self.correct
            
    def post_to_server(self) -> tuple[bool, str]:
        return (True, 'Random choice') if random.randint(1, 2) == 1 else (False, 'Random choice')
      
    #     url = f"https://adventofcode.com/{self.year}/day/{self.day}/answer"
    #     resp = requests.post(url, 
    #                          headers={"Cookie": f"session={AOC_SESSION}"},
    #                          data={'level': level, 'answer': answer})
    #     resp.raise_for_status()
    #     soup = BeautifulSoup(resp.text, 'html.parser')

    #     message = soup.article.get_text() if soup.article else ''
    #     if "That's the right answer" in message:
    #         print(f"Right answer!  {answer}")
    #         return (True, message)
    #     elif "That's not the right answer" in message:
    #         print(f"Wrong answer:  {answer}")
    #         return (False, message)
    #     elif "You don't seem to be solving the right level" in message:
    #         return (False, message)
    #     elif "You gave an answer too recently" in message:
    #         wait_pattern = r"You have (?:(\d+)m )?(\d+)s left to wait"
    #         try:
    #             [(minutes, seconds)] = re.findall(wait_pattern, message)
    #         except ValueError:
    #             return (False, message)
    #         else:
    #             wait_time = int(seconds)
    #             if minutes:
    #                 wait_time += 60 * int(minutes)
    #             print(f"Waiting {wait_time} seconds to autoretry...")
    #             time.sleep(wait_time)
    #             return self.post_answer_to_server(level=level, answer=answer)
    #     else:
    #         return (False, message)

    @property
    def already_submitted(self) -> bool:
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
                return True
            else:
                return False

    @property
    def already_solved(self) -> bool:
        puzzle = get_puzzle_from_db_by_year_and_day(self.year, self.day)
        if self.level == 1 and puzzle.part_1_solved:
            return True
        if self.level == 2 and puzzle.part_2_solved:
            return True
        
        with SQL_ENGINE.connect() as conn:
            stmt = (db.select(answers_table)
                      .where(answers_table.c.puzzle_id == self.puzzle_id)
                      .where(answers_table.c.level == self.level))
            result = conn.execute(stmt).fetchall()

            if not result:
                return False
            if any(row.correct for row in result):
                return True
            else:
                return False

    def update_info_on_db(self) -> None:
        if not self.id:
            self.id = self.get_sql_id()

        values_dict = {key: value for key, value in self.__dict__.items() if key != 'timestamp_dt'}
        
        with SQL_ENGINE.connect() as conn:
            stmt = (
                db.update(answers_table)
                .where(answers_table.c.id == self.id)
                .values(**values_dict)
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
            if result:
                return result.id
            else:
                return 0

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
            else:
                return None

    def get_sql_object(self) -> AnswerSQL:
        return AnswerSQL(puzzle_id=self.puzzle_id,
                         year=self.year,
                         day=self.day,
                         timestamp=self.timestamp,
                         level=self.level,
                         answer=self.answer,
                         correct=self.correct,
                         raw_response=self.raw_response)

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
                          raw_response=self.raw_response
                        ))
            result = conn.execute(stmt)
            conn.commit()
            correct_str = "correct" if self.correct else "incorrect"
            logger.info(f"{self.year} DAY {self.day:02d} | Answer {self.answer} ({correct_str}) written to DB with key {result.inserted_primary_key}.")
            

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
        if not self.id:
            self.id = self.get_sql_id()
        if not self.url:
            self.url = f"https://adventofcode.com/{self.year}/day/{self.day}"
            
        self.answers = self.pull_all_answers_from_db()
        self.check_answers_in_list()
                
        # self.data_dir = DATA_DIR / str(self.year) / str(self.day)

        # self.part_1_description_on_disk = (self.data_dir / 'description_part1.txt').exists()
        # self.part_2_description_on_disk = (self.data_dir / 'description_part2.txt').exists()
        # self.example_on_disk = (self.data_dir / 'example.txt').exists()
        # self.input_on_disk = (self.data_dir / 'input.txt').exists()
        # self.all_data_on_disk = all([self.part_1_description_on_disk, self.part_2_description_on_disk,
        #                              self.example_on_disk, self.input_on_disk])
        # if self.all_data_on_disk:
        #     self.pull_data_from_disk()
        # else:
        #     self.pull_data_from_server()

    def update_answers_in_db_answer_table(self) -> None:
        if not self.part_1_answer and not self.part_2_answer:
            logger.debug(f"{self.year} DAY {self.day:02d} | No correct answers found.")
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
                logger.debug(f"{self.year} DAY {self.day:02d} | All correct answers already found on DB.")


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
                logger.info(f"{self.year} DAY {self.day:02d} | Adding new Part One answer: {answer_text}")
                self.part_1_answer = answer_text
                self.part_1_solved = True
                update_db = True
            if i == 2 and (answer_text != self.part_2_answer):
                logger.info(f"{self.year} DAY {self.day:02d} | Adding new Part Two answer: {answer_text}")
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
                return [PuzzleAnswer(**row._asdict()) for row in result]

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
                return 0

    def get_sql_object(self) -> PuzzleSQL:
        return PuzzleSQL(year=self.year,
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
                         url=self.url,
                         )

    def pull_data_from_disk(self):
        data_dir = DATA_DIR / str(self.year) / str(self.day)
        logger.debug(f"Pulled data from disk ({self.year} day #{self.day})")
        with open(data_dir / 'description_part1.txt') as f:
            self.part_1_description = f.read().removesuffix('\n')

        with open(data_dir / 'description_part2.txt') as f:
            self.part_2_description = f.read().removesuffix('\n')

        with open(data_dir / 'example.txt', 'w') as f:
            self.example_text = f.read().removesuffix('\n')

        with open(data_dir / 'input.txt', 'w') as f:
            self.input_text = f.read().removesuffix('\n')

    

    def pull_data_from_server(self, get_input: bool = True):
        logger.info(f"Pulled data from server ({self.year} day #{self.day})")
        resp = requests.get(self.url, headers={"Cookie": f"session={AOC_SESSION}"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        self.part_1_solved, self.part_2_solved = get_solved_statuses_from_soup(soup)
        self.part_1_description, self.part_2_description = get_puzzle_description_from_soup(soup)
        
        try:
            self.example_text = get_example_from_soup(soup)
        except ElementNotFound as e:
            logger.debug(f"{self.year} DAY {self.day:02d} | {e}")
            self.example_text = ''

        if get_input:
            try:
                self.input_text = get_input_from_server(self.year, self.day)
            except AOCLoginException as e:
                logger.debug(f"{self.year} DAY {self.day:02d} | {e}")
                self.input_text = ''
        else:
            self.input_text = ''

    def write_code_template(self, overwrite: bool = False) -> None:
        write_code_template(self.year, self.day, overwrite)

    def download_html_file(self) -> None:
        url = f"https://adventofcode.com/{self.year}/day/{self.day}"
        resp = requests.get(url, headers={"Cookie": f"session={AOC_SESSION}"})
        resp.raise_for_status()

        html = resp.text

        filename = f"aoc_{self.year}_day_{self.day}.html"
        filepath = DATA_DIR / str(self.year) / str(self.day) / filename

        if isinstance(html, str):
            with open(filepath, 'w') as f:
                f.write(html)
            logger.info(f"{self.year} DAY {self.day:02d} | Writing new file: {filepath}")

    def write_data_files(self) -> None:
        data_dir = Path(DATA_DIR / str(self.year) / str(self.day))
        if not data_dir.exists():
            data_dir.mkdir()

        if self.part_1_description:
            filename = 'description_part1.txt'
            with open(data_dir / filename, 'w') as f:
                f.write(f"{self.title}\n\n")
                f.write(self.part_1_description.removesuffix('\n'))
            logger.debug(f"{self.year} DAY {self.day:02d} | Writing description part 1 to {data_dir / filename}")
                
        if self.part_2_description:
            filename = 'description_part2.txt'
            with open(data_dir / 'description_part2.txt', 'w') as f:
                f.write(f"{self.title}\n")
                f.write("    --- (PART TWO) ---\n\n")
                f.write(self.part_2_description.removesuffix('\n'))
            logger.debug(f"{self.year} DAY {self.day:02d} | Writing description part 2 to {data_dir / filename}")
                
        if self.example_text:
            filename = 'example.txt'
            with open(data_dir / filename, 'w') as f:
                f.write(self.example_text.removesuffix('\n'))
            logger.debug(f"{self.year} DAY {self.day:02d} | Writing example text to {data_dir / filename}")

        if self.input_text:
            filename = 'input.txt'
            with open(data_dir / filename, 'w') as f:
                f.write(self.input_text.removesuffix('\n'))
            logger.debug(f"{self.year} DAY {self.day:02d} | Writing input text to {data_dir / filename}")

        self.download_html_file()

    def submit_answer(self, answer: str|int, level: Optional[Literal[1, 2]] = None) -> PuzzleAnswer:
        if not isinstance(answer, str):
            answer = str(answer)
        if not level:
            level = 2 if self.part_1_solved else 1

        answer_obj = PuzzleAnswer(puzzle_id=self.id, 
                                  year=self.year,
                                  day=self.day,
                                  level=level, 
                                  answer=answer)
        if answer_obj.already_submitted:
            print(f"Answer {answer} already submitted on",
              f"{answer_obj.timestamp_dt.strftime("%Y-%m-%d @ %-I:%M:%S %p")}",
              f"({((dt.datetime.now(tz=TZ) - answer_obj.timestamp_dt).seconds) // 60} minutes ago)")
            return answer_obj
        # if answer_obj.already_solved:
        #     print("Puzzle already solved.")
        #     return answer_obj
        
        answer_obj.submit()
        self.answers.append(answer_obj)
        return answer_obj






        




if __name__ == "__main__":
    pass




# @dataclass
# class PuzzleData:
#     year: int
#     day: int
#     part_1_description: str = field(default_factory=str)
#     part_2_description: str = field(default_factory=str)
#     example_text: str = field(default_factory=str, repr=False)
#     input_text: str = field(default_factory=str, repr=False)

#     def __post_init__(self):
#         self.url = f"https://adventofcode.com/{self.year}/day/{self.day}"
#         self.data_dir = DATA_DIR / str(self.year) / str(self.day)
        
#     @classmethod
#     def pull_data_from_disk(cls, year: int, day: int) -> Self:
#         dir = DATA_DIR / str(year) / str(day)
        
#         with open(dir / 'description_part1.txt') as f:
#             part_1_description = f.read().removesuffix('\n')

#         with open(dir / 'description_part2.txt') as f:
#             part_2_description = f.read().removesuffix('\n')

#         with open(dir / 'example.txt', 'w') as f:
#             example_text = f.read().removesuffix('\n')

#         with open(dir / 'input.txt', 'w') as f:
#             input_text = f.read().removesuffix('\n')

#         return cls(year=year, 
#                    day=day, 
#                    part_1_description=part_1_description,
#                    part_2_description=part_2_description,
#                    example_text=example_text,
#                    input_text=input_text)

#     @classmethod
#     def pull_data_from_server(cls, year: int, day: int, get_input: bool = True) -> Self:
#         url = f"https://adventofcode.com/{year}/day/{day}"
#         resp = requests.get(url, headers={"Cookie": f"session={AOC_SESSION}"})
#         resp.raise_for_status()
        
#         soup = BeautifulSoup(resp.text, 'html.parser')

#         part_1_description, part_2_description = get_puzzle_description_from_soup(soup)
        
#         try:
#             example_text = get_example_from_soup(soup)
#         except ElementNotFound as e:
#             logger.debug(f"{year} DAY {day:02d} | {e}")
#             example_text = ''

#         if get_input:
#             try:
#                 input_text = get_input_from_server(year, day)
#             except AOCLoginException as e:
#                 logger.debug(f"{year} DAY {day:02d} | {e}")
#                 input_text = ''
#         else:
#             input_text = ''

#         return cls(year=year, 
#                    day=day, 
#                    part_1_description=part_1_description,
#                    part_2_description=part_2_description,
#                    example_text=example_text,
#                    input_text=input_text)
