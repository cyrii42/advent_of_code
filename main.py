import sqlalchemy as db
from loguru import logger
from rich import print

from advent_of_code.constants import SQLITE_URL
from advent_of_code.local import get_puzzle_from_local
from advent_of_code.logging_config import setup_logging
from advent_of_code.models import Puzzle, PuzzleAnswer
from advent_of_code.server import get_puzzle_from_server
from advent_of_code.sql_functions import get_puzzle_from_db_by_year_and_day
from advent_of_code.sql_schema import answers_table, puzzles_table

setup_logging()



def main():
    puzzle = Puzzle.from_database(2023, 7)
    print(puzzle)
    
    ...
    # update_answers_table_with_response_types()
    
    # puzzle = get_puzzle_from_db_by_year_and_day(2020, 6)
    # print(puzzle)
    # puzzle.submit_answer(123412333343333333222223333334444444333342134)



    
    # fix_manual_raw_responses()
    # delete_blank_answers_on_db()
    
    # find_answer_test()
    # find_answers_in_html_text_on_db()
    
    # delete_and_replace_all_puzzles_on_db()
    # answer_list = find_answers_in_html_text_on_db()
    
    # puzzle = get_puzzle_from_local(2019, 1)
    # print_stuff(**puzzle.__dict__)
    # puzzle_dict = {key: value for key, value in puzzle.__dict__.items() if key != 'answers'}
    # print(puzzle_dict)
    # print([key for key in puzzle.__dict__.keys()])
    # puzzle.update_info_on_db()
    # puzzle.id = 101
    # puzzle.answers = puzzle.find_answers_in_db()
    # print(puzzle)
    
    # delete_and_replace_all_puzzles_on_db()
    
    
    
    # puzzle = get_puzzle_from_server(2019, 1)
    # puzzle.write_data_files()
    
    # answer = answer_tests()
    # print(answer)
    # print(answer.already_submitted)
    # answer.write_to_sql()

    # create_answers_table()

    # answer_obj = PuzzleAnswer(
    #     puzzle_id=101,
    #     year=2019,
    #     day=1,
    #     level=1,
    #     answer='3342351',
    #     correct=True,
    #     timestamp='2025-07-17T23:11:20-04:00',
    #     raw_response="That's the right answer!  You are one gold star closer to rescuing Santa. [Continue to Part Two]",
    #     id=2
    # )
    # print(answer_obj.already_submitted)
    # print(answer_obj.already_solved)
    # # answer_obj.write_to_sql()

    # answers = get_answers_by_year_and_day(2019, 1)
    # print(answers)
    # if answers:
    #     print(answers[0].timestamp)
    #     print(answers[0].already_submitted)
    #     print(answers[0].already_solved)

    # drop_answers_table()
    

    # sql_tests()
    # answer_tests()
    
    # assess_examples()
    # pull_all_html_files()
    
    # download_html_file(2022, 6)
    
    # puzzle = get_puzzle_from_local(2017, 6)
    # print(puzzle)
    # print(puzzle.id)
    # print(lookup_puzzle_db_id(puzzle))

    # get_puzzle_by_db_id(205)
    
    # puzzle = Puzzle(year=2024, day=5)

    # puzzle = get_puzzle(year=2024, day=5, get_input=False)
    # puzzle.write_data_files()
    # print(puzzle)

    # asdf()
    
    # print(puzzle)
    # puzzle.pull_data_from_server()
    # print(puzzle.input)
    # logger.info("pulled a pulzzle!")
    # puzzle.pull_data()
    # print(puzzle)
    # logging.warning('asodifasdfp9h88932gf923gf9awg3f9aw3gfhasodifhasodifh')
    # puzzle = get_puzzle(2024, 14)
    # puzzle.submit_answer(2, 'asdoifh')
    
    # make_solution_dirs()
    # for year in range(2015, 2026):
    #     for day in range(1, 26):
    #         write_code_template_v2(year=year, day=day, overwrite=True)

    # puzzle = get_puzzle(2024, 5)
    # print(puzzle)

    # url = f"https://adventofcode.com/2024/day/5/input"
    # resp = requests.get(url, headers={"Cookie": f"session={AOC_SESSION}"})
    # print(resp.text)

    # for x in range(2015, 2026):
    #     new_dir = SOLUTIONS_DIR / f"{x}"
    #     if not new_dir.exists():
    #         new_dir.mkdir()

    # year = 2024
    # day = 17
    # dir = Path(DATA_DIR / str(year) / str(day))
    # print(dir)
    # print(dir.exists())

if __name__ == "__main__":
    main()
