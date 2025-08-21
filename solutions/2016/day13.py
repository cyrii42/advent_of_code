import functools
import hashlib
import itertools
import json
import math
import operator
import os
import pathlib
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Literal, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)

WIDTH = 7
HEIGHT = 10

class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    
def characterize_location(x: int, y: int, fav_num: int) -> int:
    step1 = (x*x + 3*x + 2*x*y + y + y*y)
    step2 = step1 + fav_num
    step3 = str(bin(step2))[2:]
    step4 = len([char for char in step3 if char == '1'])
    return 0 if step4 % 2 == 0 else 1
        
def part_one(data: str):
    fav_num = int(data)
    if data == '10':
        goal_row = 4
        goal_col = 7
    else:
        goal_row = 39
        goal_col = 31
    maze = Maze(fav_num, goal_row, goal_col)

@dataclass
class Maze:
    fav_num: int
    goal_row: int
    goal_col: int
    maze: np.ndarray = field(init=False)

    def __post_init__(self):
        coordinates = [x for x in itertools.product(range(HEIGHT), range(WIDTH))]
        self.maze = np.array([[0 for _ in range(HEIGHT)] for _ in range(WIDTH)])
        for pair in coordinates:
            x, y = pair
            self.maze[y, x] = characterize_location(x, y, self.fav_num)



    
    def traverse(self, 
                 row: int = 0, 
                 col: int = 0,
                 count: int = 0):
        if row == self.goal_row and col == self.goal_col:
            return count
        
        for dir in Direction:
            ...
        
    

def part_two(data: str):
    ...


def main():
    print(f"Part One (example):  {part_one('10')}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()