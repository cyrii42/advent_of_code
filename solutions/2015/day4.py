import functools
import hashlib
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

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLES = ['abcdef', 'pqrstuv']

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def get_hash(s: str):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def parse_data(data: str) -> str:
    return data.strip('\n')

def part_one(data: str) -> int:
    secret_key = parse_data(data)
    test_num = 0
    while True:
        if get_hash(f"{secret_key}{test_num}")[0:5] == '00000':
            return test_num
        else:
            test_num += 1
            
def part_two(data: str):
    secret_key = parse_data(data)
    test_num = 0
    while True:
        if get_hash(f"{secret_key}{test_num}")[0:6] == '000000':
            return test_num
        else:
            test_num += 1



def main():
    for example in EXAMPLES:
        print(f"Part One Example {example}: {part_one(example)}")
    print()
    print(f"Part One Input:  {part_one(INPUT)}")
    for example in EXAMPLES:
        print(f"Part Two Example {example}: {part_two(example)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()


def random_tests():
    ...
    

       
if __name__ == '__main__':
    main()