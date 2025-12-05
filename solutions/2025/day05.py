import functools
import hashlib
import itertools
import json
import math
import operator
import os
import sys
import re
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, NamedTuple, Optional, Self, Any

import numpy as np
import pandas as pd
import polars as pl
import networkx as nx
from alive_progress import alive_bar, alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

def is_fresh(id: int, range_list: list[range]) -> bool:
    for r in range_list:
        if id in r:
            return True
    return False

def parse_data(data: str) -> tuple[list[range], list[int]]:
    line_list = data.splitlines()

    range_strings = [line for line in line_list if '-' in line]
    range_list = []
    for s in range_strings:
        start, end = [int(x) for x in s.split('-')]
        range_list.append(range(start, end+1))  # ranges should be inclusive

    id_list = [int(line) for line in line_list if line and '-' not in line]

    return (range_list, id_list)
    
def part_one(data: str):
    range_list, id_list = parse_data(data)
    return len([id for id in id_list if is_fresh(id, range_list)])

def part_two(data: str):
    __ = parse_data(data)



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