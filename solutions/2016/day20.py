import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
from collections import deque
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
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

MAX_VALUE = 4_294_967_295

def parse_data(data: str):
    line_list = data.splitlines()
    num_list = []
    output_list = []
    for line in line_list:
        num1, num2 = line.split('-')
        num_list.append((int(num1), int(num2)))
    num_list = list(sorted(num_list))
    for pair in num_list:
        num1, num2 = pair
        output_list.append(range(int(num1), int(num2)+1))
    return output_list

def test(n: int, l: list[range]):
    return any(n in r for r in l)
    
def part_one(data: str):
    list_of_ranges = parse_data(data)

    n = 0
    with alive_bar() as bar:
        while True:
            if not test(n, list_of_ranges):
                return n
            n += 1
            bar()

def part_two(data: str):
    ''' How many IPs are allowed by the blacklist? '''
    r_list = parse_data(data)
    
    potentials: list[range] = []
    for i in range(len(r_list)):
        r1_end = r_list[i][-1] + 1
        if i == len(r_list)-1:
            potentials.append(range(r1_end+1, MAX_VALUE))
            break
        
        r2_start = r_list[i+1][0]
        if r2_start > r1_end:
            potentials.append(range(r1_end+1, r2_start))

    total = 0
    num_potentials = sum(len(r) for r in potentials)
    print(f"Total # of potentials: {num_potentials:,}")
    with alive_bar(num_potentials) as bar:
        for r in potentials:
            for n in r:
                if not test(n, r_list):
                    total += 1
                bar()

    return total
        

        
        

    # total = 0
    # n = 0
    # with alive_bar() as bar:
    #     while n <= MAX_VALUE:
    #         if not test(n, list_of_ranges):
    #             total += 1
    #         n += 1
    #         bar()

    # return len([x for x in range(0, 4294967295+1) if not test(x, list_of_ranges)])



def main():
    # print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()