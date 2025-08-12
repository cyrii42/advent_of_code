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

EXAMPLE = '5 10 25'
INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str) -> list[list[int]]:
    line_list = data.splitlines()
    return [[int(x) for x in line.strip().split()] for line in line_list]

def check_valid_triangle(nums: list[int]) -> bool:
    ''' In a valid triangle, the sum of any two sides must be larger than the remaining side. '''
    a, b, c = sorted(nums)
    return a + b > c
    
def part_one(data: str):
    nums_list = parse_data(data)
    return len([nums for nums in nums_list if check_valid_triangle(nums)])

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()