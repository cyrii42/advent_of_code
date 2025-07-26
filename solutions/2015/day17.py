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
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = '20\n15\n10\n5\n5'
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def parse_data(data: str) -> list[int]:
    line_list = data.splitlines()
    return sorted([int(x) for x in line_list], reverse=False)
    
def part_one(data: str, target: int):
    container_sizes = parse_data(data)
    all_iterables = [itertools.combinations(container_sizes, i) 
                     for i in range(2, len(container_sizes)+1)]
    all_combos = itertools.chain(*all_iterables)
    all_matching_combos = (x for x in all_combos if sum(x) == target)

    return sum(1 for _ in all_matching_combos)


def part_two(data: str, target: int):
    container_sizes = parse_data(data)
    all_iterables = [itertools.combinations(container_sizes, i) 
                     for i in range(2, len(container_sizes)+1)]
    all_combos, all_combos_2 = itertools.tee(itertools.chain(*all_iterables), 2)
    all_matching_combos = (x for x in all_combos if sum(x) == target)

    min_containers = min(len(x) for x in all_combos_2 if sum(x) == target)
    all_matching_min_combos = (x for x in all_matching_combos 
                               if len(x) == min_containers)

    return sum(1 for _ in all_matching_min_combos)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE, target=25)}")
    print(f"Part One (input):  {part_one(INPUT, target=150)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE, target=25)}")
    print(f"Part Two (input):  {part_two(INPUT, target=150)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()