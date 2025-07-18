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
from typing import Callable, NamedTuple, Optional, Protocol

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR, TZ

CURRENT_FILE = Path(__file__)
YEAR = CURRENT_FILE.parts[-2]
DAY = CURRENT_FILE.stem.removeprefix('day')

EXAMPLE_FILE = DATA_DIR / str(YEAR) / str(DAY) / 'example.txt'
INPUT_FILE = DATA_DIR / str(YEAR) / str(DAY) / 'input.txt' 

def calculate_fuel_required(mass: int) -> int:
    return math.floor(mass / 3) - 2

def read_data(filename: Path) -> list[int]:
    if not filename.exists():
        return None
    
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        return [int(line) for line in line_list]
    
def part_one(filename: Path):
    data = read_data(filename)
    return sum(calculate_fuel_required(x) for x in data)

def part_two(filename: Path):
    data = read_data(filename)


def main():
    print(f"Part One (input):  {part_one(INPUT_FILE)}")
    print()
    print(f"Part Two (input):  {part_two(INPUT_FILE)}")

    random_tests()


def random_tests():
    ...

       
if __name__ == '__main__':
    main()