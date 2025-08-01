import pathlib
from typing import Generator

import numpy as np
from rich import print
import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)

FIRST_CODE = 20151125   
STEP_TWO = 252533
STEP_THREE = 33554393

def parse_data(data: str) -> tuple[int, int]:
    words = data.split(' ')
    row = int(words[-3].strip(','))
    col = int(words[-1].strip('.'))
    return (row, col)

def code_generator() -> Generator[int]:
    code = FIRST_CODE
    while True:
        yield code
        code = (code * STEP_TWO) % STEP_THREE

def get_box_from_row_and_col(row: int, col: int) -> int:
    return sum(range(row + col - 1)) + col

def get_code_from_row_and_col(row: int, col: int) -> int:
    box_num = get_box_from_row_and_col(row, col)
    cg = code_generator()
    for _ in range(box_num - 1):
        next(cg)
    return next(cg)

def check_example_part_one():
    m = np.zeros((6, 6), dtype=np.int64)
    for x in range(6):
        for y in range(6):
            m[x,y] = get_code_from_row_and_col(x+1, y+1)
    print(m)
    
def part_one(data: str):
    row, col = parse_data(data)
    return get_code_from_row_and_col(row, col)

def part_two(data: str):
    __ = parse_data(data)



def main():
    check_example_part_one()
    print(f"Part One (input):  {part_one(INPUT)}")

    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
       
if __name__ == '__main__':
    main()