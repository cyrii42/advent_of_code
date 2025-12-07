import functools
import hashlib
import itertools
import json
import math
import operator
import os
import sys
import re
import time
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
from intcode import IntCode, IntCodeReturnType, parse_intcode_program

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @property
    def left(self) -> "Direction":
        return Direction((self.value -1 ) % len(Direction))

    @property
    def right(self) -> "Direction":
        return Direction((self.value + 1) % len(Direction))

# X, Y (normal Cartesian plane)
DIRECTION_DELTAS = {      
    Direction.UP: (0, 1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, -1),
    Direction.LEFT: (-1, 0),
}

class Point(NamedTuple):
    x: int
    y: int

@dataclass
class Robot:
    comp: IntCode = field(repr=False)
    position: Point = Point(0, 0)
    direction: Direction = Direction.UP
    panel_dict: defaultdict[Point, int] = field(init=False, repr=False)
    next_panel: int | None = None
    next_turn: int | None = None
    
    def __post_init__(self):
        self.panel_dict = defaultdict(int)

    def execute(self) -> int:
        while True:
            result = self.comp.execute_program()
            if result.type == IntCodeReturnType.OUTPUT:
                if not self.next_panel:
                    self.next_panel = result.value
                    self.paint()
                elif not self.next_turn:
                    self.next_turn = result.value
                    pos = self.position
                    self.turn_and_move()
                    assert self.position != pos
                    new_input = self.panel_dict[self.position]
                    assert new_input in [0, 1]
                    self.comp.add_input(new_input)
                else:
                    raise ValueError
            if result.type == IntCodeReturnType.HALT:
                print(self.panel_dict)
                return len(self.panel_dict)

    def paint(self) -> None:
        assert self.next_panel
        self.panel_dict[self.position] = self.next_panel

    def turn_and_move(self) -> None:
        assert self.next_turn in [0, 1]
        if self.next_turn == 0:
            self.direction = self.direction.left
        else:
            self.direction = self.direction.right

        x, y = self.position
        dx, dy = DIRECTION_DELTAS[self.direction]
        self.position = Point(x+dx, y+dy)

        self.next_panel = None
        self.next_turn = None

def part_one(data: str):
    program = parse_intcode_program(data)
    comp = IntCode(program, input=0)
    robot = Robot(comp)
    return robot.execute()

def part_two(data: str):
    ...



def main():
    # print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()