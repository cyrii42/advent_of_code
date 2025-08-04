import functools
import itertools
import json
import math
import operator
import os
import pathlib
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
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

EXAMPLES = [('R2, L3', 5), ('R2, R2, R2', 2), ('R5, L5, R5, R3', 12)]
INPUT = aoc.get_input(YEAR, DAY)

class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def execute_instruction(current_position: tuple[int, int],
                        direction: Direction,
                        num_steps: int) -> tuple[int, int]:
    x = current_position[0]
    y = current_position[1]
    
    match direction:
        case Direction.NORTH:
            return (x, y+num_steps)
        case Direction.EAST:
            return (x+num_steps, y)
        case Direction.SOUTH:
            return (x, y-num_steps)
        case Direction.WEST:
            return (x-num_steps, y)

def parse_data(data: str):
    return [instruction.strip() for instruction in data.split(',')]

def check_examples_part_one():
    for i, example in (enumerate(EXAMPLES, start=1)):
        prompt, answer = example
        print(f"Example #{i}: {part_one(prompt) == answer}")
    
def part_one(data: str):
    instruction_list = parse_data(data)

    location = (0, 0)
    direction = Direction.NORTH
    for instruction in instruction_list:
        turn = instruction[0]
        num_steps = int(instruction[1:])
        if turn == 'L':
            direction = Direction((direction - 1) % 4)
        if turn == 'R':
            direction = Direction((direction + 1) % 4)
        location = execute_instruction(location, direction, num_steps)
    print(location)
    return(abs(location[0]) + abs(location[1]))

def part_two(data: str):
    instruction_list = parse_data(data)



def main():
    check_examples_part_one()
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()