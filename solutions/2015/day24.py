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
from typing import Callable, Literal, NamedTuple, Optional, Protocol, Self

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

EXAMPLE="1\n2\n3\n4\n5\n7\n8\n9\n10\n11"
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

@dataclass
class PackageGroup:
    packages: list[int]
    weight: int = field(init=False)
    qe: int = field(init=False)

    def __post_init__(self):
        self.weight = sum(package for package in self.packages)
        self.qe = functools.reduce(operator.mul, self.packages)
    

def parse_data(data: str):
    line_list = data.splitlines()
    return [int(x) for x in line_list]
    
def part_one(data: str):
    package_list = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()