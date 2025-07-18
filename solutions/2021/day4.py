'''--- Day 4: Giant Squid ---'''

import math
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from operator import add, mul
from pathlib import Path
from typing import Literal, NamedTuple, Optional, Self

from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2021_day4_example.txt'
INPUT = DATA_DIR / '2021_day4_input.txt'



@dataclass
class Board:
    row_list: list[list[int]]

    @classmethod
    def create(cls, line_list: list[str]) -> Self:
        line_list = [line.replace('  ', ' ') for line in line_list]
        temp_row_list = [line.split(' ') for line in line_list]
        row_list = []
        for row in temp_row_list:
            row = [int(x) for x in row]
            row_list.append(row)
        print(row_list)

def ingest_data(filename: Path):
    with open(filename) as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    return line_list

def part_one(filename: Path):
    line_list = ingest_data(filename)
    line_list = [line.strip(' ') for line in line_list]
    line_list = [line for line in line_list if len(line) > 0]
    number_list = [int(num_str) for num_str in line_list.pop(0).split(',')]

    board_list = []
    for x in range(5, len(line_list)+1, 5):
        board_list.append(Board.create(line_list[x-5:x]))

def part_two(filename: Path):
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 
    # print(f"Part One (input):  {part_one(INPUT)}") # 
    
    # print(f"Part Two (example):  {part_two(EXAMPLE)}") # 
    # print(f"Part Two (input):  {part_two(INPUT)}") # 

    random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()