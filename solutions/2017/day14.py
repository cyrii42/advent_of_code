import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Literal, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_bar, alive_it
from day10 import part_two as create_knot_hash
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = 'flqrgnkx'
INPUT = aoc.get_input(YEAR, DAY)

TOTAL_ROWS = 128
TOTAL_COLS = 128

def convert_hash_to_bits(hash_output: str) -> str:
    return ''.join(f"{bin(int(char, base=16)).removeprefix('0b'):0>4}"
                   for char in hash_output)
   
def part_one(data: str):
    hash_inputs = [f"{data}-{row_num}" for row_num in range(TOTAL_ROWS)]
    hash_outputs = [create_knot_hash(x) for x in hash_inputs]
    hash_bits = [convert_hash_to_bits(h) for h in hash_outputs]
    return sum(len([char for char in bits if char == '1']) for bits in hash_bits)

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