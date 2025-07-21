import functools
import itertools
import json
import math
import os
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

EXAMPLE = ('turn on 0,0 through 999,999\ntoggle 0,0 through 999,0\n,'
           'turn off 499,499 through 500,500\n')
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

class Action(Enum):
    TURN_ON = 1
    TURN_OFF = 2
    TOGGLE = 3

class Point(NamedTuple):
    x: int
    y: int

@dataclass
class Instruction:
    start: Point
    end: Point
    action: Action

    def execute_part_one(self, grid: np.ndarray) -> np.ndarray:
        match self.action:
            case Action.TURN_ON:
                grid[self.start.x:self.end.x+1, 
                     self.start.y:self.end.y+1] = 1
                return grid
            case Action.TURN_OFF:
                grid[self.start.x:self.end.x+1, 
                     self.start.y:self.end.y+1] = 0
                return grid
            case Action.TOGGLE:
                grid[self.start.x:self.end.x+1, 
                     self.start.y:self.end.y+1] = 1 - grid[self.start.x:self.end.x+1, 
                                                           self.start.y:self.end.y+1]
                return grid

    def execute_part_two(self, grid: np.ndarray) -> np.ndarray:
        match self.action:
            case Action.TURN_ON:
                grid[self.start.x:self.end.x+1, 
                     self.start.y:self.end.y+1] += 1
                return grid
            case Action.TURN_OFF:
                grid[self.start.x:self.end.x+1, 
                     self.start.y:self.end.y+1] -= 1
                grid[grid < 0] = 0
                return grid
            case Action.TOGGLE:
                grid[self.start.x:self.end.x+1, 
                     self.start.y:self.end.y+1] += 2
                return grid
    
    @classmethod
    def create(cls, line: str) -> Self:
        parts = line.split(' ')

        start_x, start_y = (int(x) for x in parts[-3].split(','))
        end_x, end_y = (int(x) for x in parts[-1].split(','))

        start = Point(start_x, start_y)
        end = Point(end_x, end_y)
        
        if parts[0] == 'toggle':
            action = Action.TOGGLE
        elif parts[1] == 'on':
            action = Action.TURN_ON
        else:
            action = Action.TURN_OFF

        return cls(start, end, action)

def create_grid() -> np.ndarray:
    return np.array([[0 for _ in range(1_000)] for _ in range(1_000)])
    
def parse_data(data: str) -> list[Instruction]:
    line_list = [line for line in data.split('\n') if line]
    return [Instruction.create(line) for line in line_list]
    
def part_one(data: str):
    grid = create_grid()
    instructions = parse_data(data)

    for instruction in instructions:
        grid = instruction.execute_part_one(grid)
    
    return grid.sum()


def part_two(data: str):
    grid = create_grid()
    instructions = parse_data(data)

    for instruction in instructions:
        grid = instruction.execute_part_two(grid)
    
    return grid.sum()



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    # random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()