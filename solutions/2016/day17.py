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

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE_TESTS = [
    ('ihgpwlah', 'DDRRRD'),
    ('kglvqrro', 'DDUDRLRRUDRD'),
    ('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR')
]
INPUT = aoc.get_input(YEAR, DAY)

GOAL = (3, 3)

MAX_X = 3
MAX_Y = 3

class OutOfMaze(Exception):
    ...

# class Direction(Enum):
#     UP =    'U'
#     DOWN =  'D'
#     LEFT =  'L'
#     RIGHT = 'R'

class Direction(IntEnum):
    U = 0
    D = 1
    L = 2
    R = 3

def get_hash(s: str):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

@dataclass
class Room():
    x: int
    y: int
    door_codes: str
    door_status: dict[Direction, bool] = field(init=False)
    valid_neighbors: list[tuple[int, int]] = field(init=False)

    def __post_init__(self):
        self.door_status = {d: self.is_open(d) for d in Direction}
        self.valid_neighbors = self.get_valid_neighbors()

    def get_valid_neighbors(self) -> list[tuple[int, int]]:
        

    def is_open(self, dir: Direction) -> bool:
        if self.door_codes[dir.value] not in ['b', 'c', 'd', 'e', 'f']:
            return False
        
        x, y = (self.x, self.y)
        match dir:
            case Direction.U:
                return y > 0
            case Direction.D:
                return y < MAX_Y
            case Direction.L:
                return x > 0
            case Direction.R:
                return x < MAX_X
    
@dataclass
class Maze:
    passcode: str
    current_location: tuple[int, int] = (0, 0)
    current_room: Room = field(init=False)
    path: str = field(default_factory=str)

    def __post_init__(self):
        self.current_room = self.get_current_room()
    
    def get_current_room(self) -> Room:
        x, y = self.current_location
        return Room(x=x, 
                    y=y,
                    door_codes=get_hash(
                        f"{self.passcode}{self.path}"))

    def get_location_from_path(self) -> tuple[int, int]:
        x, y = (0, 0)
        for char in self.path:
            match Direction[char]:
                case Direction.U:
                    if y == 0:
                        raise OutOfMaze
                    else:
                        y -= 1
                case Direction.D:
                    if y == MAX_Y:
                        raise OutOfMaze
                    else:
                        y += 1
                case Direction.L:
                    if x == 0:
                        raise OutOfMaze
                    else:
                        x -= 1
                case Direction.R:
                    if x == MAX_X:
                        raise OutOfMaze
                    else:
                       x += 1
        return (x, y)

def part_one_tests():
    for i, example in enumerate(EXAMPLE_TESTS, start=1):
        passcode, answer = example
        print(f"Test #{i} ({passcode}): {part_one(passcode) == answer}")
    
def part_one(data: str):
    maze = Maze(passcode=data)
    print(maze.get_room_status())
    

def part_two(data: str):
    ...


def main():
    # part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()