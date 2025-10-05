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

INPUT = aoc.get_input(YEAR, DAY)
TESTS_PART_ONE = [
    ('9 players; last marble is worth 25 points', 32),
    ('10 players; last marble is worth 1618 points', 8317),
    ('13 players; last marble is worth 7999 points', 146373),
    ('17 players; last marble is worth 1104 points', 2764),
    ('21 players; last marble is worth 6111 points', 54718),
    ('30 players; last marble is worth 5807 points', 37305),
]

@dataclass
class MarbleGame:
    num_players: int
    last_marble: int
    marble_list: list[int] = field(init=False)
    marble_bag: itertools.count = field(init=False)
    ptr: int = 0

    def __post_init__(self):
        self.marble_list = [0]
        self.marble_bag = itertools.count()

    @property
    def size(self) -> int:
        return len(self.marble_list)

    def simulate_game(self):
        while True:
            next_marble = next(self.marble_bag)

            if next_marble % 23 == 0:
                ...

            
            
    

def parse_data(data: str):
    line_list = data.splitlines()

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        data, answer = example
        print(f"Test #{i}: {part_one(data) == answer}",
              f"({part_one(data)})")
    
def part_one(data: str):
    __ = parse_data(data)

def part_two(data: str):
    __ = parse_data(data)



def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    # part_two_tests()
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    c = itertools.count(1)
    asdf = deque([0])
    ptr = 1
    for _ in range(5):
        offset = (ptr * 2) % len(asdf)
        asdf.popleft()
        asdf.rotate(1-offset)
        asdf.appendleft(next(c))
        asdf.rotate(offset)
        asdf.appendleft(0)
        print(asdf)
        ptr += 1

       
if __name__ == '__main__':
    main()