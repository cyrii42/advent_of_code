'''--- Day 15: Warehouse Woes ---'''

import math
from pathlib import Path
from rich import print
from pprint import pprint
from copy import deepcopy
from typing import NamedTuple, Protocol, Optional
from enum import Enum, IntEnum
from dataclasses import dataclass, field
from string import ascii_letters
import itertools
import functools
import pandas as pd
import numpy as np
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day15_example.txt'
INPUT = DATA_DIR / 'day15_input.txt'

class Point(NamedTuple):
    row: int
    col: int
    char: str

class Box(Point):
    ...

class Wall(Point):
    ...

class Direction(Enum):
    UP = '^'
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'

@dataclass
class MapRow():
    point_list: list[Point]
    row_num: int
    total_map_height: int

    @property
    def width(self):
        return len(self.point_list)

    def get_point(self, col_num: int) -> Point:
        return self.point_list[col_num]


@dataclass
class Map():
    row_list: list[MapRow]

    @property
    def height(self):
        return len(self.row_list)

    @property
    def width(self):
        return self.row_list[0].width

    def print(self) -> None:
        for row in self.row_list:
            print(''.join(point.char for point in row.point_list))

    def get_row(self, y: int) -> MapRow:
        return self.row_list[y]

    def get_point(self, row_num: int, col_num: int) -> Point:
        row = self.row_list[row_num]
        return row.get_point(col_num)

    def replace_point(self, old_point: Point, new_point: Point) -> None:
        row_num = old_point.row
        col_num = old_point.col
        self.row_list[row_num].point_list[col_num] = new_point

@dataclass
class Robot():
    point: Point
    map: Map = field(repr=False)
    moves_str: str = field(repr=False)
    moves_count: int = 0

    def make_next_move(self) -> None:
        if self.moves_count == len(self.moves_str):
            print('Done!')
            return None
        
        current_row = self.point.row
        current_col = self.point.col
        next_move_str = self.moves_str[self.moves_count]
        next_direction = Direction(next_move_str)

        print()
        self.map.print()
        
        match next_direction:
            case Direction.UP:
                next_point = self.map.get_point(current_row - 1, current_col)
            case Direction.RIGHT:
                next_point = self.map.get_point(current_row, current_col + 1)
            case Direction.DOWN:
                next_point = self.map.get_point(current_row + 1, current_col)
            case Direction.LEFT:
                next_point = self.map.get_point(current_row, current_col - 1)

        if isinstance(next_point, Wall):
            self.moves_count += 1
            self.make_next_move()
        elif isinstance(next_point, Box):
            print('found a box')
            match next_direction:
                case Direction.UP:
                    next_next_point = self.map.get_point(next_point.row - 1, next_point.col)
                case Direction.RIGHT:
                    next_next_point = self.map.get_point(next_point.row, next_point.col + 1)
                case Direction.DOWN:
                    next_next_point = self.map.get_point(next_point.row + 1, next_point.col)
                case Direction.LEFT:
                    next_next_point = self.map.get_point(next_point.row, next_point.col - 1)
            if isinstance(next_next_point, Wall):
                self.moves_count += 1
                self.make_next_move()
            else:
                self.map.replace_point(self.point, Point(self.point.row, self.point.col, '.'))
                self.map.replace_point(next_point, Point(next_point.row, next_point.col, '@'))
                self.map.replace_point(next_next_point, Box(next_next_point.row, next_next_point.col, 'O'))
                self.moves_count += 1
                self.point = next_point
                self.make_next_move()
        else:
            self.moves_count += 1
            self.point = next_point
            self.make_next_move()


def ingest_data(filename: Path) -> tuple[Map, str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    map_lines = [line for line in line_list if line.startswith('#')]
    move_lines = [line for line in line_list if line != '' and not line.startswith('#')]
    moves_str = ''.join(line for line in move_lines)

    return (create_map(map_lines), moves_str)

def create_map_row(line: str, row_num: int, total_map_height: int) -> MapRow:
    point_list = []
    
    for col_num, char in enumerate(line):
        if char == '#':
            point_list.append(Wall(col_num, row_num, char))
        elif char == 'O':
            point_list.append(Box(col_num, row_num, char))
        else:
            point_list.append(Point(col_num, row_num, char))
            
    return MapRow(point_list, row_num, total_map_height)

def create_map(line_list: list[str]) -> Map:
    row_list = [create_map_row(line, row_num, len(line_list)) for row_num, line in enumerate(line_list)]
        
    return Map(row_list)

def find_robot(map: Map, moves_str: str) -> Robot:
    for row in map.row_list:
        for point in row.point_list:
            if point.char == '@':
                return Robot(point, map, moves_str)
    raise ValueError("Could not find a robot position in map.")


def part_one(filename: Path):
    map, moves_str = ingest_data(filename)
    # map.print()
    robot = find_robot(map, moves_str)
    robot.make_next_move()
    # robot.map.print()


def part_two(filename: Path):
    ...


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    # random_tests()



def random_tests():
    print(Direction('v'))


       


if __name__ == '__main__':
    main()