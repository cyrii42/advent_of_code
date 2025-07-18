from advent_of_code.models import Puzzle
from advent_of_code.exceptions import PuzzleNotFound
from advent_of_code.helpers import validate_year_and_day

def get_example(year: int, day: int) -> str:
    validate_year_and_day(year, day)
    try:
        puzzle = Puzzle.from_database(year, day)
    except PuzzleNotFound:
        puzzle = Puzzle.from_server(year, day)
    
    return puzzle.example_text

def get_input(year: int, day: int) -> str:
    validate_year_and_day(year, day)
    try:
        puzzle = Puzzle.from_database(year, day)
    except PuzzleNotFound:
        puzzle = Puzzle.from_server(year, day)
        
    return puzzle.input_text

def print_description(year: int, day: int) -> None:
    validate_year_and_day(year, day)
    try:
        puzzle = Puzzle.from_database(year, day)
    except PuzzleNotFound:
        puzzle = Puzzle.from_server(year, day)

    print(puzzle.title + '\n')
    print(puzzle.part_1_description)
    if puzzle.part_2_description:
        print('--- Part Two ---\n')
        print(puzzle.part_2_description)

def get_description(year: int, day: int) -> str:
    validate_year_and_day(year, day)
    try:
        puzzle = Puzzle.from_database(year, day)
    except PuzzleNotFound:
        puzzle = Puzzle.from_server(year, day)

    output = puzzle.title
    output += '\n'
    output += puzzle.part_1_description
    if puzzle.part_2_description:
        output += '--- Part Two ---\n'
        output += puzzle.part_2_description

    return output
    