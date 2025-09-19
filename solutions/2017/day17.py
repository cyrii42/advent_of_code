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
        ''' It starts with a circular buffer containing only the value 0, 
        which it marks as the current position. It then steps forward through 
        the circular buffer some number of steps (your puzzle input) before
        inserting the first new value, 1, after the value it stopped on. The 
        inserted value becomes the current position. Then, it steps forward 
        from there the same number of steps, and wherever it stops, inserts 
        after it the second new value, 2, and uses that as the new current 
        position again.'''

        num_insertions = 2017

        for _ in range(num_insertions):
            self.ptr = (self.ptr + self.num_steps) % self.buffer_size
            self.insert_new_number(next(self.counter))
            self.ptr = self.ptr + 1

    def insert_new_number(self, num: int) -> None:
        idx = self.ptr
        if idx >= self.buffer_size - 1:
            self.buffer.append(num)
        else:
            self.buffer.insert(idx+1, num)

    def solve_part_one(self) -> int:
        self.run_simulation()
        idx_2017 = self.buffer.index(2017)
        return self.buffer[idx_2017+1]

    def solve_part_two(self) -> int:
        ...

def modulo_tests():
    n = 0
    mod = 2
    for x in range(1, 4):
        print(f"{n} + {x} mod {mod} = {(n+x)%mod}")
    
def part_one(data: str):
    num_steps = int(data)
    spinlock = Spinlock(num_steps=num_steps)
    return spinlock.solve_part_one()

def part_two(data: str):
    num_steps = int(data)
    spinlock = Spinlock(num_steps=num_steps)
    return spinlock.solve_part_two()


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    # random_tests()

def random_tests():
    modulo_tests()

       
if __name__ == '__main__':
    main()