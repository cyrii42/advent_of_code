import functools
import hashlib
import itertools
import json
import math
import operator
import os
import pathlib
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
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
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = 'abc'
INPUT = aoc.get_input(YEAR, DAY)

TRIPLE_PATTERN = r'(.)\1{2,}'

def get_hash(s: str):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def generate_key(salt: str):
    idx = 0

    while True:
        h = get_hash(f"{salt}{idx}")
        m = re.search(TRIPLE_PATTERN, h)
        if m:
            char = m[0][0]
            if verify_key(idx, char, salt):
                yield idx
        idx += 1

def verify_key(idx: int, char: str, salt: str) -> bool:
    pattern = ''.join(char for _ in range(5))
    return any(pattern in get_hash(f"{salt}{x}") 
               for x in range(idx+1, idx+1001))
    
def part_one(data: str):
    salt = data
    gen = generate_key(salt)
    for _ in range(63):
        next(gen)
    return next(gen)
    

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