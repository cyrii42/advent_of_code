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

@dataclass
class Loop:
    tile_set: set[Point] = field(repr=False)

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

class Rectangle(NamedTuple):
    upper_left: Point
    upper_right: Point
    lower_right: Point
    lower_left: Point

    @property
    def points(self) -> list[Point]:
        return [self.upper_left, self.upper_right, self.lower_right, self.lower_left]

    @property
    def area(self) -> int:
        width = abs(self.upper_left.col - self.lower_right.col) + 1
        height = abs(self.upper_left.row - self.lower_right.row) + 1
        return width * height

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
    # return all(p in loop.tile_set for p in box_points)
    # return len([p for p in box_points if p in loop.tile_set]) >= 4


def validate_point(p: Point, loop: Loop) -> bool:
    if p in loop.tile_set:
        return True

    num_intersections = len([x for x in range(loop.max_col+1)
                             if Point(p.row, x) in loop.tile_set])
    # print(num_intersections)
    return num_intersections % 2 != 0

    # row_tiles = [t for t in loop.tile_set if t.row == p.row]
    # if not row_tiles:
    #     return False
    # return (p.col >= min(t.col for t in row_tiles)
    #         and p.col <= max(t.col for t in row_tiles))
    

def parse_data(data: str) -> list[RedTile]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        col, row = [int(x) for x in line.split(',')]
        output_list.append(RedTile(row, col))
    return output_list

def generate_rectangles(red_tile_list: list[RedTile]) -> list[Rectangle]:
    ''' Returns a list of rectangles sorted by area in descending order '''
    output_list: list[Rectangle] = []
    for p1, p2 in itertools.permutations(red_tile_list, 2):
        top_row = max(p1.row, p2.row)
        bottom_row = min(p1.row, p2.row)
        left_col = min(p1.col, p2.col)
        right_col = max(p1.col, p2.col)
        box_points = [
            Point(top_row, left_col),       # upper left
            Point(top_row, right_col),      # upper right
            Point(bottom_row, right_col),   # lower right
            Point(bottom_row, left_col)     # lower left
        ]
        output_list.append(Rectangle(*box_points))
    return sorted(output_list, key=lambda r: r.area, reverse=True)
        
def part_one(data: str):
    red_tile_list = parse_data(data)
    rectangles = generate_rectangles(red_tile_list)
    return rectangles[0].area

    max_area = 0
    for rectangle in rectangles:
        width = abs(p1.col - p2.col) + 1
        height = abs(p1.row - p2.row) + 1
        area = width * height
        max_area = max(max_area, area)
    return max_area

def part_two(data: str):
    red_tile_list = parse_data(data)
    rectangles = generate_rectangles(red_tile_list)
    loop = create_loop(red_tile_list)

    for rectangle in alive_it(rectangles):
        if all(validate_point(p, loop) for p in rectangle.points):
            print(rectangle.area)
            # return rectangle.area

    # max_area = 0
    # for rectangle in rectangles:
    #     width = abs(p1.col - p2.col) + 1
    #     height = abs(p1.row - p2.row) + 1
    #     area = width * height
    #     max_area = max(max_area, area)
    # return max_area


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()