'''--- Day 9: Rope Bridge ---'''

import math
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Literal, NamedTuple, Optional, Self

from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day9_example.txt'
INPUT = DATA_DIR / '2022_day9_input.txt'    

class Direction(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'

@dataclass
class Move:
    direction: Direction

@dataclass(frozen=True)
class Position:
    row: int
    col: int

@dataclass
class Head:
    row: int = 0
    col: int = 0

    def move(self, move: Move) -> None:
        match move.direction:
            case Direction.LEFT:
                self.col -= 1
            case Direction.RIGHT:
                self.col += 1
            case Direction.UP:
                self.row -= 1
            case Direction.DOWN:
                self.row += 1

@dataclass
class Tail:
    row: int = 0
    col: int = 0
    head: Head = field(default_factory=Head, repr=False)
    positions: set[Position] = field(default_factory=set, repr=False)

    @property
    def position(self) -> Position:
        return Position(self.row, self.col)

    def move_head(self, move: Move) -> None:
        self.head.move(move)

        # If the head is ever two steps directly up, down, left, or right from the tail, 
        #   the tail must also move one step in that direction so it remains close enough.
        # Otherwise, if the head and tail aren't touching and aren't in the same row or column, 
        #   the tail always moves one step diagonally to keep up.
        if self.head.row == self.row:
            if self.head.col == self.col-2:
                self.col = self.col-1
            elif self.head.col == self.col+2:
                self.col = self.col+1
        elif self.head.col == self.col:
            if self.head.row == self.row-2:
                self.row = self.row-1
            elif self.head.row == self.row+2:
                self.row = self.row+1
                
        elif self.head.row == self.row+2 and self.head.col == self.col+1:  # upper right
            ...
        elif self.head.row == self.row-1 and self.head.col == x:
            ...
            

        '''Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail always moves one step diagonally to keep up:

        .....    .....    .....
        .....    ..H..    ..H..
        ..H.. -> ..... -> ..T..
        .T...    .T...    .....
        .....    .....    .....

        .....    .....    .....
        .....    .....    .....
        ..H.. -> ...H. -> ..TH.
        .T...    .T...    .....
        .....    .....    .....
        '''
       
            

        self.positions.add(self.position)

        # print(self)
        # print(self.head)
        # print()

    def get_part_one_answer(self) -> int:
        return len(self.positions)
        


def ingest_data(filename: Path):
    with open(filename) as f:
        line_list = [line.strip('\n')for line in f.readlines()]
        line_list_split = [line.split() for line in line_list]
        instruction_list = [(Direction(line[0]), int(line[1])) for line in line_list_split]
    return instruction_list

def get_move_list(instruction_list: list[tuple[Direction, int]]) -> list[Move]:
    output_list = []
    for instruction in instruction_list:
        for _ in range(instruction[1]):
            output_list.append(Move(instruction[0]))
    return output_list

def part_one(filename: Path):
    instruction_list = ingest_data(filename)
    move_list = get_move_list(instruction_list)
    
    tail = Tail()
    for move in move_list:
        tail.move_head(move)

    return tail.get_part_one_answer()

def part_two(filename: Path):
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") #
    # print(f"Part One (input):  {part_one(INPUT)}") #
    
    # print(f"Part Two (example):  {part_two(EXAMPLE)}") #
    # print(f"Part Two (input):  {part_two(INPUT)}") #

    # random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()
