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

### FOUR DIRECTIONS
class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

# ROW, COL
DIRECTION_DELTAS = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}

class NodeType(Enum):
    EMPTY = '.'
    START = 'S'
    BEAM = '|'
    SPLITTER = '^'

class Point(NamedTuple):
    row: int
    col: int

class Node(NamedTuple):
    row: int
    col: int
    node_type: NodeType

    @property
    def point(self) -> Point:
        return Point(self.row, self.col) 

type NodeGraph = dict[Node, list[Node]]
def create_graph(node_dict: dict[Point, Node]) -> NodeGraph:
    output_dict = {}
    
    for node in node_dict.values():
        neighbor_list = []
        for direction in Direction:
            delta_row, delta_col = DIRECTION_DELTAS[direction]
            try:
                neighbor_point = Point(node.row + delta_row,
                                       node.col + delta_col)
                neighbor = node_dict[neighbor_point]
                neighbor_list.append(neighbor)
            except KeyError:
                continue
        output_dict[node] = neighbor_list
        
    return output_dict

class EndOfManifold(Exception):
    pass

class NodePath(NamedTuple):
    nodes: list[Node]

def sort_nodes(node_list: list[Node]) -> list[Node]:
    node_list.sort(key=lambda node: node.row)
    node_list.sort(key=lambda node: node.col)
    return node_list

@dataclass
class Manifold:
    node_dict: dict[Point, Node]
    graph: NodeGraph
    max_row: int = field(init=False)

    def __post_init__(self):
        self.max_row = max(p.row for p in self.node_dict.keys())

    def run_simulation(self):
        start = [n for n in self.node_dict.values() 
                 if n.node_type == NodeType.START][0]
        self.fire_beam_down(start)

        total_splits = 0
        for current_row in range(self.max_row+1):
            beams_in_row = [n for n in self.node_dict.values()
                            if n.row == current_row and 
                            n.node_type == NodeType.BEAM]
            for beam in beams_in_row:
                total_splits += self.fire_beam_down(beam)
                
        return total_splits
            
    def fire_beam_down(self, node: Node) -> int:
        num_splits = 0
        row, col, _ = node
        try:
            node_below = self.node_dict[Point(row+1, col)]
            row_below, col_below, _ = node_below
        except KeyError:
            return num_splits

        match node_below.node_type:
            case NodeType.EMPTY:
                point_below = Point(row_below, col_below)
                self.node_dict[point_below] = Node(*point_below, NodeType.BEAM)
            case NodeType.SPLITTER:
                point_left = Point(row_below, col_below-1)
                point_right = Point(row_below, col_below+1)
                self.node_dict[point_left] = Node(*point_left, NodeType.BEAM)
                self.node_dict[point_right] = Node(*point_right, NodeType.BEAM)
                num_splits += 1

        return num_splits

    @property
    def part_two_answer(self) -> int:
        num_beams = len([n for n in self.node_dict.values() if n.node_type == NodeType.BEAM])
        return num_beams // 2

def parse_data(data: str) -> dict[Point, Node]:
    line_list = data.splitlines()

    output_dict = {}
    for row, line in enumerate(line_list):
        for col, char in enumerate(line):
            node = Node(row, col, NodeType(char))
            output_dict[node.point] = node
    return output_dict
    
def part_one(data: str):
    node_dict = parse_data(data)
    graph = create_graph(node_dict)
    manifold = Manifold(node_dict, graph)
    num_splits = manifold.run_simulation()
    # print(manifold.node_dict)
    # print(len([n for n in manifold.node_dict.values() if n.node_type == NodeType.BEAM]))
    return num_splits

def part_two(data: str):
    ''' find the set of unique paths to any node in the bottom row '''

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