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
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '3'
INPUT = aoc.get_input(YEAR, DAY)

NUM_REPEATS = 2017

@dataclass
class Spinlock:
    num_steps: int
    ptr: int = 0
    buffer: list[int] = field(init=False)
    counter: itertools.count = field(init=False)

    def __post_init__(self):
        self.buffer = [0]
        self.counter = itertools.count(start=1)

    @property
    def buffer_size(self) -> int:
        return len(self.buffer)

    def run_simulation(self):
        print(f"{self.buffer} (Position: {self.ptr}) (buffer size {self.buffer_size})")
        for _ in range(10):
            self.ptr = self.ptr + self.num_steps % self.buffer_size
            self.buffer.insert(self.ptr+1, next(self.counter))
            print(f"{self.buffer} (Position: {self.ptr}) (buffer size {self.buffer_size})")
        # self.buffer[self.ptr + 1] = 2017

    def solve_part_one(self) -> int:
        self.run_simulation()
        idx_2017 = self.buffer.index(2017)
        print(self.buffer[idx_2017-5:idx_2017+6])
        return self.buffer[idx_2017+1]
    
    
    
    
def part_one(data: str):
    num_steps = int(data)
    spinlock = Spinlock(num_steps=num_steps)
    spinlock.run_simulation()
    # return spinlock.solve_part_one()

def part_two(data: str):
    num_steps = int(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    for n in range(5):
        print(f"{n}: {(n+3) % (n+1)}")
    asdf = [1, 2, 3, 4, 5]
    asdf.insert(3, 9)
    print(asdf)
    print((0 + 3) % 1)

       
if __name__ == '__main__':
    main()