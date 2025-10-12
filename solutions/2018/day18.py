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

EXAMPLE = '''.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.'''
INPUT = aoc.get_input(YEAR, DAY)

class Direction(IntEnum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7

    @property
    def left(self) -> "Direction":
        return Direction((self.value - 1) % len(Direction))

    @property
    def right(self) -> "Direction":
        return Direction((self.value + 1) % len(Direction))

    @property
    def opposite(self) -> "Direction":
        num_dirs = len(Direction)
        return Direction((self.value + num_dirs // 2) % num_dirs)
    
DIRECTION_DELTAS = {
    Direction.NORTH: (0, -1),
    Direction.NORTHEAST: (1, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTHEAST: (1, 1),
    Direction.SOUTH: (0, 1),
    Direction.SOUTHWEST: (-1, 1),
    Direction.WEST: (-1, 0),
    Direction.NORTHWEST: (-1, -1)
}

class Point(NamedTuple):
    x: int
    y: int

class NodeType(Enum):
    OPEN = 0
    TREES = 1
    LUMBERYARD = 2

class AcreType(Enum):
    OPEN = 0
    TREES = 1
    LUMBERYARD = 2

@dataclass
class Node:
    position: Point
    node_type: NodeType

    def __repr__(self):
        return (f"{self.node_type.name} (x={self.position.x}, " +
                f"y={self.position.y})")

@dataclass
class CollectionArea:
    acre_dict: dict[Point, AcreType]

    @property
    def max_x(self) -> int:
        return max(pos.x for pos in self.acre_dict.keys())

    @property
    def max_y(self) -> int:
        return max(pos.y for pos in self.acre_dict.keys())

    @property
    def num_trees(self) -> int:
        return len([acre for acre, acre_type in self.acre_dict.items()
                    if acre_type == AcreType.TREES])

    @property
    def num_lumberyards(self) -> int:
        return len([acre for acre, acre_type in self.acre_dict.items()
                    if acre_type == AcreType.LUMBERYARD])

    def get_type(self, pos: Point) -> AcreType | None:
        return self.acre_dict.get(pos)

    def set_type(self, pos: Point, acre_type: AcreType) -> None:
        self.acre_dict[pos] = acre_type

    # def validate_position(self, pos: Point) -> bool:
    #     return (pos.x >= 0 and pos.x <= self.max_x 
    #             and pos.y >= 0 and pos.y <= self.max_y)

    @staticmethod
    def get_position(pos: Point, direction: Direction):
        dx, dy = DIRECTION_DELTAS[direction]
        return Point(pos.x+dx, pos.y+dy)

    def tick(self):
        last_minute_dict = deepcopy(self.acre_dict)
        for pos in last_minute_dict:
            surrounding_types = self.get_surrounding_types(pos)
            print(f"{pos} ({last_minute_dict[pos]})")
            print(surrounding_types)
            num_trees = len([t for t in surrounding_types 
                            if t == AcreType.TREES])
            num_lumberyards = len([t for t in surrounding_types 
                                   if t == AcreType.LUMBERYARD])
            match last_minute_dict[pos]:
                case AcreType.OPEN:
                    if num_trees >= 3:
                        self.set_type(pos, AcreType.TREES)
                case AcreType.TREES:
                    if num_lumberyards >= 3:
                        self.set_type(pos, AcreType.LUMBERYARD)
                case AcreType.LUMBERYARD:
                    if num_lumberyards == 0 and num_trees == 0:
                        self.set_type(pos, AcreType.OPEN)

    def get_surrounding_types(self, pos: Point) -> list[AcreType]:
        output_list = []
        for direction in Direction:
            acre_pos = self.get_position(pos, direction)
            acre_type = self.get_type(acre_pos)
            if acre_type:
                output_list.append(acre_type)
        return output_list

    def print_diagram(self):
        for y in range(0, self.max_y+1):
            row = ''
            for x in range(0, self.max_x+1):
                pos = Point(x, y)
                match self.acre_dict[pos]:
                    case AcreType.OPEN:
                        row += '.'
                    case AcreType.LUMBERYARD:
                        row += '#'
                    case AcreType.TREES:
                        row += '|'
                    case _:
                        row += "?"
            print(row)
            

def create_graph(node_list: list[Node]) -> dict[Point, list[Node]]:
    output_dict: dict[Point, list[Node]] = {}

    def get_node_neighbor_coordinates(node: Node) -> list[Point]:
        x, y = node.position

        output_list = []
        for dir in Direction:
            dx, dy = DIRECTION_DELTAS[dir]
            output_list.append(Point(x + dx, y + dy))
        return output_list
    
    for node in node_list:
        neighbor_list = []
        for x, y in get_node_neighbor_coordinates(node):
            try:
                neighbor_list.append(
                    next(node for node in node_list 
                        if node.position.x == x 
                        and node.position.y == y))
            except StopIteration:
                continue
        output_dict[node.position] = neighbor_list
        
    return output_dict

def parse_data(data: str) -> dict[Point, AcreType]:
    line_list = data.splitlines()
    output_dict = {}
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            pos = Point(x, y)
            if char == ' ':
                continue
            elif char == '#':
                output_dict[pos] = AcreType.LUMBERYARD
            elif char == '.':
                output_dict[pos] = AcreType.OPEN
            elif char == '|':
                output_dict[pos] = AcreType.TREES
            else:
                raise ValueError
    return output_dict
    
def part_one(data: str):
    acre_dict = parse_data(data)
    collection_area = CollectionArea(acre_dict)

    collection_area.print_diagram()

    collection_area.tick()
    
    # print()
    # for _ in range(2):
    #     collection_area.tick()
    #     collection_area.print_diagram()
    #     print()

    
    return collection_area.num_lumberyards * collection_area.num_trees
    print(graph)

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()