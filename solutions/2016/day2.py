import functools
import itertools
import json
import math
import operator
import os
import pathlib
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Literal, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = 'ULL\nRRDDD\nLURDL\nUUUUD'
INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str):
    line_list = data.splitlines()
    return line_list

def create_keypad_part_one() -> np.ndarray:
    return np.array([[y for y in range(x, x+3)] for x in [1, 4, 7]])

def execute_instruction_set_part_one(start: tuple[int, int], 
                                     instruction_set: str) -> tuple[int, int]:
    row, col = start
    for char in instruction_set:
        match char:
            case 'U':
                row = max(row-1, 0)
            case 'R':
                col = min(col+1, 2)
            case 'D':
                row = min(row+1, 2)
            case 'L':
                col = max(col-1, 0)
    return (row, col)

    
def part_one(data: str):
    keypad = create_keypad_part_one()
    instructions_list = parse_data(data)

    output_str = ''
    start = (1, 1)
    for instruction_set in instructions_list:
        position = execute_instruction_set_part_one(start, instruction_set)
        row, col = position
        num = keypad[row, col]
        output_str += str(num)
        start = position
    return output_str


def create_keypad_part_two() -> np.ndarray:
    return np.array([[None, None, '1', None, None], 
                     [None, '2', '3', '4', None], 
                     ['5', '6', '7', '8', '9'], 
                     [None, 'A', 'B', 'C', None],
                     [None, None, 'D', None, None]])


def execute_instruction_set_part_two(start: tuple[int, int], 
                                     instruction_set: str,
                                     keypad: np.ndarray) -> tuple[int, int]:
    row, col = start
    
    # print(f"START: ({row}, {col})")
    for char in instruction_set:
        match char:
            case 'U':
                new_row = max(row-1, 0)
                row = new_row if keypad[new_row, col] else row
            case 'R':
                new_col = min(col+1, 4)
                col = new_col if keypad[row, new_col] else col
            case 'D':
                new_row = min(row+1, 4)
                row = new_row if keypad[new_row, col] else row
            case 'L':
                new_col = max(col-1, 0)
                col = new_col if keypad[row, new_col] else col
        # print(f"{char}: ({row}, {col})")
    return (row, col)

def part_two(data: str):
    keypad = create_keypad_part_two()
    instructions_list = parse_data(data)

    output_str = ''
    start = (2, 0)
    for instruction_set in instructions_list:
        position = execute_instruction_set_part_two(start, instruction_set, keypad)
        row, col = position
        num = keypad[row, col]
        output_str += num
        start = position
    return output_str



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()