import pathlib
import functools
import itertools
import operator
import hashlib
import json
import math
import os
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, NamedTuple, Optional, Protocol, Self, Literal, Generator

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich.table import Table
from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

@dataclass
class Bot:
    id: int
    chip_1: int
    chip_2: int

def parse_data(data: str):
    line_list = data.splitlines()

    for line in line_list:
        if line.startswith('value'):
            nums = [char for char in line if char.isdigit()]
            value = int(nums[0])
            bot_num = int(nums[1])
        else:
            nums = [char for char in line if char.isdigit()]
            giver_bot = int(nums[0])
            low_bot = int(nums[1])
            high_bot = int(nums[2])
    
def part_one(data: str):
    __ = parse_data(data)

def part_two(data: str):
    __ = parse_data(data)



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