'''--- Day 1: Sonar Sweep ---'''

import math
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from operator import add, mul
from pathlib import Path
from typing import Literal, NamedTuple, Optional, Self

from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2021_day1_example.txt'
INPUT = DATA_DIR / '2021_day1_input.txt'


def ingest_data(filename: Path):
    with open(filename) as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    return line_list

def part_one(filename: Path):
    num_list = [int(num_char) for num_char in ingest_data(filename)]

    num_increases = 0
    for i, num in enumerate(num_list):
        if i == 0:
            continue
        if num > num_list[i-1]:
            num_increases += 1
    return num_increases

def part_two(filename: Path):
    num_list = [int(num_char) for num_char in ingest_data(filename)]

    num_increases = 0
    last_sum = math.inf
    for i, num in enumerate(num_list):
        if i < 2:
            continue
        rolling_sum = num + num_list[i-1] + num_list[i-2]
        if rolling_sum > last_sum:
            num_increases += 1
        last_sum = rolling_sum
        
    return num_increases

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 7
    print(f"Part One (input):  {part_one(INPUT)}") # 
    
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # 5
    print(f"Part Two (input):  {part_two(INPUT)}") # 

    random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()
