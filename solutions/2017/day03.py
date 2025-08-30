import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
from collections import deque
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

TESTS_PART_ONE = [
    ('1', 0),
    ('12', 3),
    ('23', 2),
    ('1024', 31)
]
INPUT = aoc.get_input(YEAR, DAY)

class Direction(Enum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7

DIRECTION_DELTAS = {
    Direction.NORTH: (0, 1),
    Direction.NORTHEAST: (1, 1),
    Direction.EAST: (1, 0),
    Direction.SOUTHEAST: (1, -1),
    Direction.SOUTH: (0, -1),
    Direction.SOUTHWEST: (-1, -1),
    Direction.WEST: (-1, 0),
    Direction.NORTHWEST: (-1, 1)
}

'''     17  16  15  14  13
        18   5   4   3  12
        19   6   1   2  11
        20   7   8   9  10
        21  22  23---> ...  

    Layer #1
    x = layer_num * 2
    up x-1
    left 2
    down x
    right x '''

@dataclass
class DataPoint:
    num: int
    x: int
    y: int

def get_next_datapoint() -> Generator[DataPoint]:
    num = 1
    x, y = (0, 0)

    yield DataPoint(num, x, y)

    dir_gen = get_next_direction()
    while True:
        num += 1
        dir = next(dir_gen)
        delta = DIRECTION_DELTAS[dir]
        x += delta[0]
        y += delta[1]
        
        yield DataPoint(num, x, y)

def get_next_direction() -> Generator[Direction]:
    layer_num = 0
    dir_sequence = deque([Direction.EAST])

    while True:
        if not dir_sequence:
            layer_num += 1
            dir_sequence = get_direction_sequence_by_layer(layer_num)
            
        yield dir_sequence.popleft()
        
def get_direction_sequence_by_layer(layer_num: int) -> deque[Direction]:
    output = deque()
    x = layer_num * 2
    for _ in range(x-1):
        output.append(Direction.NORTH)
    for _ in range(x):
        output.append(Direction.WEST)
    for _ in range(x):
        output.append(Direction.SOUTH)
    for _ in range(x+1):
        output.append(Direction.EAST)
    return output

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        data, answer = example
        print(f"Test #{i} ({data}): {part_one(data) == answer}",
              f"({part_one(data)})")

def part_one(data: str):
    square = int(data)
    datapoint_gen = get_next_datapoint()
    for _ in range(square-1):
        next(datapoint_gen)
    dp = next(datapoint_gen)
    return abs(dp.x) + abs(dp.y)

def get_neighbor_locations(x: int, y: int) -> list[tuple[int, int]]:
    output_list = []
    for dir in Direction:
        delta = DIRECTION_DELTAS[dir]
        output_list.append((x+delta[0],
                            y+delta[1]))
    return output_list

def get_next_datapoint_part_two() -> Generator[DataPoint]:
    start_num = 1
    x, y = (0, 0)
    datapoint_dict: dict[tuple[int, int], int] = {(x, y): start_num}
    
    yield DataPoint(start_num, x, y)
    
    dir_gen = get_next_direction()
    while True:
        start_num += 1
        dir = next(dir_gen)
        delta = DIRECTION_DELTAS[dir]
        x += delta[0]
        y += delta[1]

        neighbors = get_neighbor_locations(x, y)
        num = sum(datapoint_dict.get(n, 0) for n in neighbors)
        datapoint_dict[(x, y)] = num
        
        yield DataPoint(num, x, y)
        

def part_two(data: str):
    puzzle_input = int(data)
    datapoint_gen = get_next_datapoint_part_two()

    n = 1
    while True:
        next_dp = next(datapoint_gen)
        if next_dp.num > puzzle_input:
            return next_dp.num
        n += 1
    



def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...



# def get_layer_start_coordinates(layer_num: int) -> tuple[int, int]:
#     '''
#     (0, 0)    (layer_num, (0 - (layer_num-1))
#     (1, 0)
#     (2, -1)
#     (3, -2)
#     (4, -3) '''
#     return (layer_num, (0 - (layer_num - 1)))

# def get_layer_num(num: int) -> int:
#     if num < 1:
#         return -1
#     gen = get_next_layer_range()
#     layer = 0
#     while True:
#         next_range = next(gen)
#         if num in next_range:
#             return layer
#         layer += 1

# def get_nums_in_next_layer() -> Generator[int]:
#     x = 0
#     while True:
#         yield 1 + sum(8*(i+1) for i in range(x))
#         x += 1

# def get_next_layer_range() -> Generator[range]:
#     yield range(1, 2)
    
#     x = 2 
#     i = 1
#     while True:
#         next = x + (8 * i) - 1
#         yield range(x, next+1)
        
#         x = next + 1
#         i += 1

# def get_layer_start_num(layer_num: int) -> int:
#     gen = get_next_layer_range()
#     r = next(gen)
#     for _ in range(layer_num):
#         r = next(gen)
#     return r[0]
       
if __name__ == '__main__':
    main()