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
from intcode import IntCode, IntCodeReturn, IntCodeReturnType, parse_intcode_program

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLES_PART_ONE = [
    '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99',
    '1102,34915192,34915192,7,4,7,99,0',
    '104,1125899906842624,99'
]
TESTS_PART_TWO = []
INPUT = aoc.get_input(YEAR, DAY)
   
def part_one(data: str):
    program = parse_intcode_program(data)
    comp = IntCode(program, input=1)
    while True:
        result = comp.execute_program()
        if result.type == IntCodeReturnType.HALT:
            return comp.output_queue

def part_two(data: str):
    program = parse_intcode_program(data)
    comp = IntCode(program, input=2)
    while True:
        result = comp.execute_program()
        if result.type == IntCodeReturnType.HALT:
            return comp.output_queue

def run_tests(tests: list[tuple[str, Any]], fn: Callable):
    for i, example in enumerate(tests, start=1):
        data, answer = example
        test_answer = fn(data)
        print(f"Test #{i}: {test_answer == answer}",
              f"({test_answer})")

def main():
    print(f"Part One (example #1):  {part_one(EXAMPLES_PART_ONE[0])}")
    print(f"Part One (example #2):  {part_one(EXAMPLES_PART_ONE[1])}")
    print(f"Part One (example #3):  {part_one(EXAMPLES_PART_ONE[2])}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()