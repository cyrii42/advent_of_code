import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
import sys
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, NamedTuple, Optional, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_bar, alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class NoCoordinateFound(Exception):
    pass

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

DIRECTION_DELTAS = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}

class Point(NamedTuple):
    row: int
    col: int

class Coordinate(Point):
    pass

def validate_point(point: Point, max_row: int, max_col: int) -> bool:
    return point.row >= 0 and point.row <= max_row and point.col >= 0 and point.col <= max_col

def get_point_neighbors(point: Point, 
                        coordinate_list: list[Coordinate],
                        max_row: int,
                        max_col: int) -> list[Point]:
    row, col = point.row, point.col

    output_list = []
    for dir in Direction:
        delta_row, delta_col = DIRECTION_DELTAS[dir]
        point = Point(row + delta_row, col + delta_col)

        if not validate_point(point, max_row, max_col):
            continue
        
        if point in coordinate_list:
            output_list.append(Coordinate(row + delta_row, col + delta_col))
        else:
            output_list.append(point)
    return output_list

def create_graph(max_row: int, 
                 max_col: int, 
                 coordinate_list: list[Coordinate]
                 ) -> dict[Point, list[Point]]:
    output_dict = {}
    for row in range(max_row+1):
        for col in range(max_col+1):
            point = Point(row, col)
            if point in coordinate_list:
                output_dict[Coordinate(row, col)] = get_point_neighbors(point, coordinate_list, max_row, max_col)
            else:
                output_dict[point] = get_point_neighbors(point, coordinate_list, max_row, max_col)
    return output_dict

def create_closest_coordinate_dict(graph: dict[Point, list[Point]]) -> dict[Point, Coordinate|None]:
    return {point: find_closest_coordinate(point, graph) for point in graph.keys()}

def create_coordinate_area_dict(closest_coordinate_dict: dict[Point, Coordinate|None]) -> dict[Coordinate, list[Point]]:
    coordinate_set = {c for c in closest_coordinate_dict.values() if c}

    output_dict = {}
    for coordinate in coordinate_set:
        output_dict[coordinate] = [p for p, c in closest_coordinate_dict.items() if p and c == coordinate]
    return output_dict

def get_grid_dimensions(coordinate_list: list[Coordinate]) -> tuple[int, int]:
    max_row = max(coordinate.row for coordinate in coordinate_list)
    max_col = max(coordinate.col for coordinate in coordinate_list)

    higher_num = max(max_row, max_col)# + 1
    return (higher_num, higher_num)

def get_manhattan_distance(p1: Point, p2: Point) -> int:
    return abs(p1.row - p2.row) + abs(p1.col - p2.col)

def find_closest_coordinate(starting_point: Point, graph: dict[Point, list[Point]]) -> Coordinate | None:
    assert starting_point in graph.keys()
    queue = deque([(starting_point, [])])

    visited = set()
    visited.add(starting_point)

    closest_so_far = (None, 0)
    while queue:
        point, path = queue.popleft()
        if isinstance(point, Coordinate):
            prev_winner, prev_path_length = closest_so_far
            if prev_winner:
                if prev_path_length == len(path):
                    return None
                else:
                    print(f"Starting Point: {starting_point} Winner: {prev_winner}")
                    return prev_winner
            else:
                closest_so_far = (point, len(path))
        neighbors = graph[point]
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
                visited.add(neighbor)
    raise NoCoordinateFound

def find_largest_finite_area(coordinate_area_dict: dict[Coordinate, list[Point]],
                             max_row: int,
                             max_col: int
                             ) -> int:
    filtered_area_list_list = [area_list for area_list in coordinate_area_dict.values()
                               if not any(point.row == 0 for point in area_list)
                               and not any(point.row == max_row for point in area_list)
                               and not any(point.col == 0 for point in area_list)
                               and not any(point.col == max_col for point in area_list)]
    return max(len(area_list) for area_list in filtered_area_list_list)

def parse_data(data: str) -> list[Coordinate]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        col, row = [int(x) for x in line.split(',')]
        output_list.append(Coordinate(row, col))
    return output_list
    
def part_one(data: str):
    coordinate_list = parse_data(data)
    max_row, max_col = get_grid_dimensions(coordinate_list)
    graph = create_graph(max_row, max_col, coordinate_list)

    closest_coordinate_dict = create_closest_coordinate_dict(graph)
    coordinate_area_dict = create_coordinate_area_dict(closest_coordinate_dict)
    return find_largest_finite_area(coordinate_area_dict, max_row, max_col)
    

def part_two(data: str):
    ...



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()