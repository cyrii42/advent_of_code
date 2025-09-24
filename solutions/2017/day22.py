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

@dataclass
class Node:
    row: int
    col: int
    infected: bool = False

    @property
    def char(self) -> str:
        return '#' if self.infected else '.'

    def __iter__(self):
        for f in (self.row, self.col, self.infected):
            yield f

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

@dataclass
class Cluster:
    node_list: list[Node]
    carrier_node: Node = field(init=False)
    carrier_dir: Direction = Direction.UP
    num_infection_bursts: int = 0

    def print_cluster(self):
        min_row = min(n.row for n in self.node_list)
        max_row = max(n.row for n in self.node_list)

        for row in range(min_row, max_row+1):
            print(''.join(n.char for n in 
                          (node for node in self.node_list if node.row == row)))
        print(f"Carrier: {self.carrier_node.row}, {self.carrier_node.col} "
              f"({self.carrier_node.infected}) ({self.carrier_dir.name})")
        print()

    def __post_init__(self) -> None:
        self.carrier_node = self.get_node((0, 0))

    def get_node(self, coordinates: tuple[int, int]) -> Node:
        row, col = coordinates
        try:
            return next(n for n in self.node_list if n.row == row and n.col == col)
        except StopIteration:
            self.node_list.append((Node(row, col)))
            return next(n for n in self.node_list if n.row == row and n.col == col)

    def execute_burst(self) -> None:
        ''' 
        1. If the current node is infected, it turns to its right. Otherwise, 
        it turns to its left. (Turning is done in-place; the current node does 
        not change.)

        2. If the current node is clean, it becomes infected. Otherwise, 
        it becomes cleaned. (This is done after the node is considered 
        for the purposes of changing direction.)

        3. The virus carrier moves forward one node in the direction it is facing.
    '''
        if self.carrier_node.infected:
            self.carrier_dir = Direction((self.carrier_dir + 1) % 4)  # turn right
            self.carrier_node.infected = False
        else:
            self.carrier_dir = Direction((self.carrier_dir - 1) % 4)  # turn left
            self.carrier_node.infected = True
            self.num_infection_bursts += 1

        row, col, _ = self.carrier_node
        delta_row, delta_col = DIRECTION_DELTAS[self.carrier_dir]
        new_coordinates = (row+delta_row, col+delta_col)
        self.carrier_node = self.get_node(new_coordinates)
    
    @classmethod
    def from_data(cls, data: str) -> Self:
        line_list = data.splitlines()
        num_rows = len(line_list)
        num_cols = len(line_list[0])
        center_row, center_col = (math.floor(num_rows/2), math.floor(num_cols/2))

        node_list = []
        for i, row in enumerate(line_list):
            row_num = i - center_row
            for j, node_char in enumerate(row):
                col_num = j - center_col
                infected = True if node_char == '#' else False
                node_list.append(Node(row_num, col_num, infected))
        return cls(node_list)          
    
def part_one(data: str):
    cluster = Cluster.from_data(data)
    num_bursts = 70 if data == EXAMPLE else 10_000
    for _ in range(num_bursts):
        cluster.execute_burst()
    return cluster.num_infection_bursts

def part_two(data: str):
    cluster = Cluster.from_data(data)



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