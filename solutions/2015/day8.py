import ast
import codecs
import functools
import itertools
import json
import math
import os
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from pprint import pprint
from string import ascii_letters
from typing import Callable, NamedTuple, Optional, Protocol, Self

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

def part_one_example():
    with open(aoc.DATA_DIR / '2015.08_examples.txt', 'r') as f:
        total_code_len = 0
        total_string_len = 0
        for s in f.readlines():
            s = s.strip('\n')
            code_len = len(s)
            total_code_len += code_len
            string_len = len(s
                             .removeprefix('\"')
                             .removesuffix('\"')
                             .encode('utf-8')
                             .decode('unicode_escape'))
            total_string_len += string_len
        return total_code_len - total_string_len

def part_two_example():
    total_code_len = 0
    total_escape_len = 0
    with open(aoc.DATA_DIR / '2015.08_examples.txt', 'r') as f:
        for s in f.readlines():
            s = s.strip('\n')
            code_len = len(s)
            total_code_len += code_len
            
            s1 = re.escape(s)
            s2 = re.sub(r'([\",])', r'\\\1', s1)
            escape_len = len(s2) + 2  # adding two for the outer quotation marks
            total_escape_len += escape_len
        return total_escape_len - total_code_len


def parse_data(data: str):
    line_list = [line for line in data.split('\n') if line]
    return line_list
    
def part_one():
    with open(aoc.DATA_DIR / '2015.08_input.txt', 'r') as f:
        total_code_len = 0
        total_string_len = 0
        for s in f.readlines():
            s = s.strip('\n')
            code_len = len(s)
            total_code_len += code_len
            string_len = len(s
                             .removeprefix('\"')
                             .removesuffix('\"')
                             .encode('utf-8')
                             .decode('unicode_escape'))
            total_string_len += string_len
        return total_code_len - total_string_len

def part_two():
    total_code_len = 0
    total_escape_len = 0
    with open(aoc.DATA_DIR / '2015.08_input.txt', 'r') as f:
        for s in f.readlines():
            s = s.strip('\n')
            code_len = len(s)
            total_code_len += code_len
            
            s1 = re.escape(s)
            s2 = re.sub(r'([\",])', r'\\\1', s1)
            escape_len = len(s2) + 2  # adding two for the outer quotation marks
            total_escape_len += escape_len
        return total_escape_len - total_code_len




def main():
    print(f"Part One (example): {part_one_example()}")
    print(f"Part One (input):  {part_one()}")
    print()
    print(f"Part Two (example):  {part_two_example()}")
    print(f"Part Two (input):  {part_two()}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()