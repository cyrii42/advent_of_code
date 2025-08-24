import functools
import hashlib
import itertools
import json
import math
import operator
import os
import pathlib
import re
from collections import deque
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

INPUT = aoc.get_input(YEAR, DAY)

def run_white_elephant_part_one(num_elves: int, print_info: bool = False) -> int:
    d = {n: 1 for n in range(num_elves)}
    elf = -1
    while True:
        elf = ((elf + 1) % num_elves)
        while not d[elf]:
            if print_info:
                print(f"Elf #{elf+1} has no presents and is skipped.")
            elf = ((elf + 1) % num_elves)
        
        next_elf = ((elf + 1) % num_elves)
        while not d[next_elf]:
            next_elf = ((next_elf + 1) % num_elves)
            
        d[elf] += d[next_elf]
        if print_info:
            print(f"Elf #{elf+1} takes Elf #{next_elf+1}'s {d[next_elf]} present(s)",
                  f"(Elf #{elf+1} now has {d[elf]})")
        d[next_elf] = 0

        if d[elf] >= num_elves:
            return elf+1

def test_part_one():
    print(f"TEST (5): {part_one('5') == 3} ({part_one('5', print_info=True)})")

def part_one(data: str, print_info: bool = False):
    num_elves = int(data)
    return run_white_elephant_part_one(num_elves, print_info=print_info)
    

def part_two(data: str):
    ...



def main():
    test_part_one()
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()