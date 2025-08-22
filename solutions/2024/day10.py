'''--- Day 10: Hoof It ---'''

from pathlib import Path
from rich import print
from pprint import pprint
from copy import deepcopy
from typing import NamedTuple, Protocol, Optional
from enum import Enum
from dataclasses import dataclass, field
from string import ascii_letters
import itertools
import pandas as pd
import numpy as np
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2024_day10_example.txt'
INPUT = DATA_DIR / '2024_day10_input.txt'
FULL_TRAIL_SET = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
@dataclass(frozen=True)
class Position():
    row_num: int
    col_num: int
    height: int

    def __post_init__(self):
        if self.height < 0 or self.height > 9:
            raise ValueError

@dataclass(frozen=True)
class Trailhead(Position):
    ...       

@dataclass
class MapRow():
    row_num: int
    position_list: list[Position]
    total_map_height: int = field(repr=False)

    @property
    def width(self):
        return len(self.position_list)

    def get_position(self, col_num: int) -> Position | None:
        if col_num >= self.total_map_height:
            return None
        else:
            return self.position_list[col_num]

@dataclass
class Map():
    row_list: list[MapRow]

    @property
    def height(self):
        return len(self.row_list)

    @property
    def width(self):
        return self.row_list[0].width

    @property
    def positions(self):
        return [position for row in self.row_list for position in row.position_list]

    @property
    def trailheads(self):
        return [position for position in self.positions if isinstance(position, Trailhead)]

    def get_row(self, row_num: int) -> MapRow:
        return self.row_list[row_num]

    def get_position(self, row_num: int, col_num: int) -> Position | None:
        if row_num < 0 or col_num < 0:
            return None
        if row_num >= self.width or col_num >= self.height:
            return None
        else:
            row = self.row_list[row_num]
            return row.get_position(col_num)

    def find_hiking_trails(self) -> int:
        total = 0
        for trailhead in self.trailheads:
            total += self.score_trailhead(trailhead)
        return total

    def find_hiking_trails_part_two(self) -> int:
        total = 0
        for trailhead in self.trailheads:
            total += self.score_trailhead_part_two(trailhead)
        return total

    def score_trailhead(self, trailhead: Trailhead) -> int:
        hiker = Hiker(trailhead, self)
        hiker.find_trails()
        trailhead_score = len(hiker.summits_found)
        # print(f"Trailhead ({trailhead}) score: {trailhead_score}")
        return trailhead_score

    def score_trailhead_part_two(self, trailhead: Trailhead) -> int:
        hiker = Hiker(trailhead, self)
        hiker.find_trails_part_two()
        trailhead_score = len(hiker.summits_found_part_two)
        # print(f"Trailhead ({trailhead}) score: {trailhead_score}")
        return trailhead_score

@dataclass
class Hiker():
    position: Position
    map: Map = field(repr=False)
    summits_found: set[Position] = field(default_factory=set, repr=False)
    summits_found_part_two: list[Position] = field(default_factory=list, repr=False)

    def __post_init__(self):
        self.starting_position = self.position
        
    def find_next_position(self, direction: Direction) -> Position | None:
        ''' Determine the next position based on input direction.'''
        current_row = self.position.row_num
        current_col = self.position.col_num
        
        match direction:
            case Direction.UP:
                next_position = self.map.get_position(current_row - 1, current_col)
            case Direction.RIGHT:
                next_position = self.map.get_position(current_row, current_col + 1)
            case Direction.DOWN:
                next_position = self.map.get_position(current_row + 1, current_col)
            case Direction.LEFT:
                next_position = self.map.get_position(current_row, current_col - 1)

        if next_position is None:
            return None
        elif self.position.height + 1 == next_position.height:
            return next_position
        else:
            return None
 
    def find_trails(self) -> None:
        next_positions = [self.find_next_position(direction) for direction in Direction]
        for position in next_positions:
            if not position:
                continue
            if position.height == 9 and position not in self.summits_found:
                # print(f"Found a new summit ({position}) from trailhead:  {self.starting_position}")
                self.summits_found.add(position)
            self.position = position
            self.find_trails()
        return None

    def find_trails_part_two(self) -> None:
        next_positions = [self.find_next_position(direction) for direction in Direction]
        for position in next_positions:
            if not position:
                continue
            if position.height == 9:
                # print(f"Found a new PART TWO summit ({position}) from trailhead:  {self.starting_position}")
                self.summits_found_part_two.append(position)
            self.position = position
            self.find_trails_part_two()
        return None

def create_map_row(line: str, row_num: int, total_map_height: int) -> MapRow:
    position_list = []
    for col_num, char in enumerate(line):
        if char == '0':
            position_list.append(Trailhead(row_num, col_num, int(char)))
        else:
            position_list.append(Position(row_num, col_num, int(char)))
    return MapRow(row_num, position_list, total_map_height)


def create_map(filename: Path) -> Map:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    row_list = [create_map_row(line, row_num, len(line_list)) for row_num, line in enumerate(line_list)]
    return Map(row_list)

def part_one(filename: Path):
    map = create_map(filename)
    return map.find_hiking_trails()


def part_two(filename: Path):
    map = create_map(filename)
    return map.find_hiking_trails_part_two()


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
   


if __name__ == '__main__':
    main()