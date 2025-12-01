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

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

def execute_program(program: list[int]) -> list[int]:
    ptr = 0
    while True:
        opcode = program[ptr]
        if opcode == 99:
            return program
        func = operator.add if opcode == 1 else operator.mul
        loc1 = program[ptr+1]
        val1 = program[loc1]
        loc2 = program[ptr+2]
        val2 = program[loc2]
        loc = program[ptr+3]
        program[loc] = func(val1, val2)
        ptr += 4

def parse_data(data: str):
    return [int(x) for x in data.split(',')]
    
def part_one(data: str):
    program = parse_data(data)
   
    if data == INPUT:
        program[1] = 12
        program[2] = 2

    program = execute_program(program)
    return program[0]

def part_two(data: str):
    program = parse_data(data)

    for noun, verb in itertools.product(range(100), repeat=2):
        program = parse_data(data)
        program[1] = noun
        program[2] = verb
        program = execute_program(program)
        if program[0] == 19690720:
            return f"{noun}{verb}"



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()