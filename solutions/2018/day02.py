import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
import sys
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, NamedTuple, Optional, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_bar, alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)
EXAMPLE = 'abcdef\nbababc\nabbcde\nabcccd\naabcdd\nabcdee\nababab'

def contains_two(box: str) -> bool:
    return any(box.count(char) == 2 for char in box)

def contains_three(box: str) -> bool:
    return any(box.count(char) == 3 for char in box)
    
def part_one(data: str):
    box_list = data.splitlines()
    num_two = len([box for box in box_list if contains_two(box)])
    num_three = len([box for box in box_list if contains_three(box)])
    return num_two * num_three

def find_fabric_boxes(box_list: list[str]) -> tuple[str, str]:
    ...

def part_two(data: str):
    ...



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()