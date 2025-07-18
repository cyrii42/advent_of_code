'''--- Day 12: Hill Climbing Algorithm ---'''

import math
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from operator import add, mul
from pathlib import Path
from typing import Literal, NamedTuple, Optional, Self

from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day12_example.txt'
INPUT = DATA_DIR / '2022_day12_input.txt'

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class ImpossibleMove(Exception):
    pass

@dataclass
class Position:
    row: int
    col: int
    char: str

    @property
    def start(self) -> bool:
        return self.char == 'S'

    @property
    def end(self) -> bool:
        return self.char == 'E'

    @property
    def elevation(self) -> int:
        return 999 if self.start or self.end else ord(self.char)
            
    def check_step(self, next_position: "Position") -> bool:
        return next_position.elevation <= (self.elevation + 1)


@dataclass(frozen=True)
class Map:
    position_list: list[Position]

    @property
    def start(self) -> Position:
        return [position for position in self.position_list if position.start][0]

    @property
    def end(self) -> Position:
        return [position for position in self.position_list if position.end][0]

    @classmethod
    def create(cls, line_list: list[str]) -> Self:
        position_list = []
        for i, line in enumerate(line_list):
            char_list = [char for char in line]
            position_sublist = [Position(row=i, col=j, char=char) for j, char in enumerate(char_list)]
            position_list += position_sublist
        return cls(position_list)

    def get_position(self, row_num: int, col_num: int) -> Position | None:
        # print(f"Checking {row_num}, {col_num}")
        try:
            return [position for position in self.position_list 
                    if position.row == row_num and position.col == col_num][0]
        except IndexError:
            return None


@dataclass
class Hiker:
    map: Map = field(repr=False)
    position: Position

    @classmethod
    def create(cls, map: Map) -> Self:
        return cls(map, map.start)

    def check_step(self, next_position: Position) -> bool:
        return next_position.elevation <= (self.position.elevation + 1)

    def find_next_position(self, direction: Direction) -> Position | None:
        current_row = self.position.row
        current_col = self.position.col
        
        match direction:
            case Direction.UP:
                return self.map.get_position(current_row - 1, current_col)
            case Direction.RIGHT:
                return self.map.get_position(current_row, current_col + 1)
            case Direction.DOWN:
                return self.map.get_position(current_row + 1, current_col)
            case Direction.LEFT:
                return self.map.get_position(current_row, current_col - 1)

    def take_step(self, next_position: Position) -> None:
        if not self.check_step(next_position):
            raise ImpossibleMove
        else:
            self.position = next_position
            print(f"Moved to {next_position}")

    def find_best_path(self):
        for direction in Direction:
            next_position = self.find_next_position(direction)
            if not next_position:
                print('Next position is None')
                continue
            if next_position.end:
                print("FOUND EXIT!")
                return
            try:
                self.take_step(next_position)
                self.find_best_path()
            except ImpossibleMove:
                print('Next position is too high')
                continue
        print('Loop ended')
                

        


def ingest_data(filename: Path):
    with open(filename) as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    return line_list

def part_one(filename: Path):
    line_list = ingest_data(filename)
    map = Map.create(line_list)
    print(map)
    hiker = Hiker.create(map)
    hiker.find_best_path()

def part_two(filename: Path):
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") #
    # print(f"Part One (input):  {part_one(INPUT)}") # 
    
    # print(f"Part Two (example):  {part_two(EXAMPLE)}") # 
    # print(f"Part Two (input):  {part_two(INPUT)}") # 

    random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()
