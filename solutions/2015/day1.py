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

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

    
def part_one(data: str) -> int:
    location = 0
    for char in data:
        if char == '(':
            location += 1
        if char == ')':
            location -= 1
    return location


def part_two(data: str) -> int:
    location = 0
    for i, char in enumerate(data, start=1):
        if char == '(':
            location += 1
        if char == ')':
            location -= 1

        if location == -1:
            return i
    return -1



def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    print(part_two(')'))
    print(part_two('()())'))

       
if __name__ == '__main__':
    main()