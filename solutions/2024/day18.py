'''--- Day 18: RAM Run ---'''

import functools
import itertools
import math
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from pprint import pprint
from string import ascii_letters
from typing import Callable, NamedTuple, Optional, Protocol

import numpy as np
import pandas as pd
from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day18_example.txt'
INPUT = DATA_DIR / 'day18_input.txt'

class Point(NamedTuple):
    x: int
    y: int

class OutsideGrid(Exception):
    pass

class Death(Exception):
    pass

class Success(Exception):
    pass

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

@dataclass
class Grid:
    byte_list: list[Point] = field(repr=False)
    max_num: int = field(repr=False)
    end: Point = field(init=False, repr=False)
    corrupted_points: list[Point] = field(default_factory=list, repr=False)
    current_point: Point = field(default=Point(0, 0))

    def __post_init__(self):
        self.end = Point(x=self.max_num, y=self.max_num)
        self.simulate_bytes()

    def simulate_bytes(self):
        for byte in self.byte_list:
            self.corrupted_points.append(Point(byte.x, byte.y))

    def find_next_position(self, direction: Direction) -> Point | None:
        ''' Determine the next Point based on input direction.'''
        current_x = self.current_point.x
        current_y = self.current_point.y
        
        match direction:
            case Direction.UP:
                return Point(current_x, current_y+1)
            case Direction.RIGHT:
                return Point(current_x+1, current_y)
            case Direction.DOWN:
                return Point(current_x, current_y-1)
            case Direction.LEFT:
                return Point(current_x-1, current_y)

    def test_move(self, next_point: Point) -> bool:
        
        if next_point in self.corrupted_points:
            raise Death(f"You moved onto a corrupted next_point ({next_point.x}, {next_point.y})!")
        if (next_point.x < 0 
                or next_point.x > self.max_num 
                or next_point.y < 0 
                or next_point.y > self.max_num):
            raise OutsideGrid(f"You tried to move outside the grid ({next_point.x}, {next_point.y})!")
        if next_point == self.end:
            raise Success("you win!")
        else:
            return True

    

def read_input(filename: Path) -> list[Point]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    output_list = []
    for line in line_list:
        x, y = line.split(',')
        output_list.append(Point(x=int(x), y=int(y)))
    return output_list

def part_one(filename: Path):
    byte_list = read_input(filename)
    max_x = max(byte.x for byte in byte_list)
    max_y = max(byte.y for byte in byte_list)
    max_num = max(max_x, max_y)
    grid = Grid(byte_list, max_num)
    print(grid)
    grid.move(Point(65, 6))

def part_two(filename: Path):
    ...


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two_example()}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    # random_tests()


def random_tests():
    ...

       
if __name__ == '__main__':
    main()