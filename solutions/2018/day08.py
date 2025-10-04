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

EXAMPLE = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
INPUT = aoc.get_input(YEAR, DAY)

sys.setrecursionlimit(10**6)

def get_metadata_total(data: list[int]):
    ''' https://dev.to/steadbytes/aoc-2018-day-8-memory-maneuver-34jf '''
    n_children, n_metadata = data[0:2]
    remaining = data[2:]

    total = 0
    
    # if there aren't any children, this loop doesn't happen
    for _ in range(n_children):
        child_total, remaining = get_metadata_total(remaining)
        total += child_total

    current_node_metadata = remaining[0:n_metadata]
    current_node_total = sum(current_node_metadata)

    total += current_node_total

    return total, remaining[n_metadata:]  
    
def part_one(data: str):
    node_data = [int(x) for x in data.split(' ')]
    total, _ = get_metadata_total(node_data)
    return total

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