import functools
import itertools
import json
import math
import os
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from pprint import pprint
from string import ascii_letters
from typing import Callable, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def get_next_password(password: str) -> str:
    ...        

def check_test_zero(password: str) -> bool:
    return len(password) == 8 and all(char.islower() for char in password)

def check_test_one(password: str) -> bool:
    ...

def check_test_two(password: str) -> bool:
    return not any(char in password for char in ['i', 'o', 'l'])

def check_test_three(password: str) -> bool:
    ...



def parse_data(data: str) -> str:
    return data.strip('\n')

def run_example_tests() -> None:
    print(check_test_zero('hijklmmn'))
    print(check_test_two('hijklmmn'))
    
def part_one(data: str):
    password = parse_data(data)

def part_two(data: str):
    __ = parse_data(data)



def main():
    run_example_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()