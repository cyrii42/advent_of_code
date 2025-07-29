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
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Iterator, NamedTuple, Optional, Protocol, Self

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

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def parse_data(data: str) -> int:
    return int(data)

def check_example_part_one():
    target_list = [10, 30, 40, 70, 60, 120, 80, 150, 130]


@dataclass
class House:
    id: int
    total_presents: int = 0

@dataclass
class Elf:
    id: int
    
    def __post_init__(self):
        self.delivery = map(lambda x: (x * self.id, self.id * 10), itertools.count(1))

    @property
    def next_delivery(self) -> tuple[int, int]:
        return self.delivery.__next__()

def elf_generator(elf_id: int) -> Generator[tuple[int, int]]:
    i = 1
    while True:
        i += 1
        yield (elf_id * i, elf_id * 10) 

    
def get_nth_house(n: int) -> int:
    ...
    
def part_one(data: str):
    target = parse_data(data)

    # houses = [House(x) for x in range(1, 1000)]

    # elves = [elf_generator(x) for x in range(1, 11)]
    # for x in range(10):
    #     elf = elves[x]
    #     for _ in range(10):
    #         house_id, presents = elf.__next__()
    #         house = houses[house_id]
    #         house.total_presents += presents

    # print([house for house in houses[0:10]])

    elf = Elf(3)
    for _ in range(5):
        print(elf.next_delivery)

def part_two(data: str):
    __ = parse_data(data)



def main():
    check_example_part_one()
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()