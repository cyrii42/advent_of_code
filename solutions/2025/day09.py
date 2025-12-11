import functools
import hashlib
import itertools
import json
import math
import operator
import os
import sys
import re
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, NamedTuple, Optional, Self, Any

import numpy as np
import pandas as pd
import polars as pl
import networkx as nx
from alive_progress import alive_bar, alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class Point(NamedTuple):
    row: int
    col: int

class RedTile(Point):
    pass

class GreenTile(Point):
    pass

def parse_data(data: str) -> list[RedTile]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        col, row = [int(x) for x in line.split(',')]
        output_list.append(RedTile(row, col))
    return output_list
    
def part_one(data: str):
    red_tile_list = parse_data(data)

    max_area = 0
    for p1, p2 in itertools.permutations(red_tile_list, 2):
        width = abs(p1.col - p2.col) + 1
        height = abs(p1.row - p2.row) + 1
        area = width * height
        max_area = max(max_area, area)
    return max_area

def part_two(data: str):
    print("creating red tile list")
    red_tile_list = parse_data(data)
    # print(red_tile_list)
    print("creating loop")
    loop = create_loop(red_tile_list)
    # print(loop)
    # print('filling loop')
    # filled_loop = fill_loop(loop)
    # print(filled_loop)
    print('checking boxes')
    max_area = 0
    print(len(red_tile_list))
    for p1, p2 in alive_it(itertools.permutations(red_tile_list, 2)):
        # box = create_box(p1, p2)
        # if validate_box(box, loop):
        if validate_box(p1, p2, loop):
            # print('valid')
            width = abs(p1.col - p2.col) + 1
            height = abs(p1.row - p2.row) + 1
            area = width * height
            max_area = max(max_area, area)
    return max_area



class Loop:
    def __init__(self, tile_set: set[Point]):
        self.tile_set = tile_set

    @functools.cached_property
    def min_row(self) -> int:
        return min(tile.row for tile in self.tile_set)

    @functools.cached_property
    def max_row(self) -> int:
        return max(tile.row for tile in self.tile_set)

    @functools.cached_property
    def min_col(self) -> int:
        return min(tile.col for tile in self.tile_set)

    @functools.cached_property
    def max_col(self) -> int:
        return max(tile.col for tile in self.tile_set)

def validate_box(t1: RedTile, t2: RedTile, loop: Loop) -> bool:
    top_row = max(t1.row, t2.row)
    bottom_row = min(t1.row, t2.row)
    left_col = min(t1.col, t2.col)
    right_col = max(t1.col, t2.col)
    box_points = [
        Point(top_row, left_col),
        Point(top_row, right_col),
        Point(bottom_row, right_col),
        Point(bottom_row, left_col)
    ]
    return all(validate_point(p, loop) for p in box_points)

# def create_box(t1: RedTile, t2: RedTile) -> set[Point]:
#     min_row, max_row = (min(t1.row, t2.row), max(t1.row, t2.row))
#     min_col, max_col = (min(t1.col, t2.col), max(t1.col, t2.col))
    
#     return {Point(row, col) for row, col 
#            in itertools.product(range(min_row, max_row+1), range(min_col, max_col+1))}

# def validate_box(box: set[Point], loop: Loop):
#     return all(validate_point(p, loop) for p in box)

def create_loop(red_tile_list: list[RedTile]) -> Loop:
    output_set = set()
    for i in range(len(red_tile_list)):
        try:
            t1 = red_tile_list[i]
            t2 = red_tile_list[i+1]
        except IndexError:
            t1 = red_tile_list[i]
            t2 = red_tile_list[0]
        assert t1.row == t2.row or t1.col == t2.col

        output_set.add(t1)
        if t1.row == t2.row:
            start, end = (min(t1.col, t2.col), max(t1.col, t2.col))
            output_set.update({GreenTile(t1.row, x) 
                            for x in [x for x in range(start+1, end)]})
        elif t1.col == t2.col:
            start, end = (min(t1.row, t2.row), max(t1.row, t2.row))
            output_set.update({GreenTile(x, t1.col) 
                            for x in [x for x in range(start+1, end)]})
    return Loop(output_set)

def validate_point(p: Point, loop: Loop) -> bool:
    if p in loop.tile_set:
        return True

    row_tiles = [t for t in loop.tile_set if t.row == p.row]
    if not row_tiles:
        return False
    return (p.col >= min(t.col for t in row_tiles)
            and p.col <= max(t.col for t in row_tiles))
        
    return ((loop.min_row <= p.row <= loop.max_row)
            and (loop.min_col <= p.col <= loop.max_col))

# def fill_loop(loop: set[Point]) -> set[Point]:
#     rows = {tile.row for tile in loop}
#     print(len(rows))
#     for row in alive_it(rows):
#         row_cols = [tile.col for tile in loop if tile.row == row]
#         start, end = min(row_cols), max(row_cols)
#         # start = min(tile.col for tile in row_tiles)
#         # end = max(tile.col for tile in row_tiles)
#         loop.update({GreenTile(row, x) 
#                             for x in [x for x in range(start+1, end)]})
#     return loop
            
        
        # assert t1.row in t2 or t2.col in t2
        # overlap = t1.row if t1 in t2 else t1.col
        
        


def main():
    # print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()