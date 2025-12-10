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

### EIGHT DIRECTIONS
class Direction(IntEnum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7

# ROW, COL
DIRECTION_DELTAS = {
    Direction.NORTH: (-1, 0),
    Direction.NORTHEAST: (-1, 1),
    Direction.EAST: (0, 1),
    Direction.SOUTHEAST: (1, 1),
    Direction.SOUTH: (1, 0),
    Direction.SOUTHWEST: (1, -1),
    Direction.WEST: (0, -1),
    Direction.NORTHWEST: (-1, -1)
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

    def print(self) -> None:
        for row in range(max(p.row for p in self.node_dict.keys())+1):
            row_nodes = [n for n in self.node_dict.values() if n.row == row]
            print(row, ''.join(n.node_type.value for n in row_nodes))

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
    manifold = Manifold(node_dict)
    num_splits = manifold.run_simulation()
    # print(manifold.node_dict)
    # print(len([n for n in manifold.node_dict.values() if n.node_type == NodeType.BEAM]))
    return num_splits

def part_two(data: str):
    ''' find the set of unique paths to any node in the bottom row '''
    node_dict = parse_data(data)
    manifold = Manifold(node_dict)
    manifold.run_simulation()
    manifold.print()
    new_node_dict = manifold.node_dict
    adjacency_list = create_graph(new_node_dict)
    # print(adjacency_list)
    graph = nx.DiGraph()

    for parent, children in adjacency_list.items():
        if parent.node_type in [NodeType.START, NodeType.BEAM]:
            for child in children:
                if (child.node_type == NodeType.BEAM and child.row > parent.row
                    and (child.col in [parent.col-1, parent.col, parent.col+1])):
                    graph.add_edge(parent, child)

    print(graph)
    
    start = [n for n in graph.nodes if n.node_type == NodeType.START][0]
    bottom_row = [n for n in graph.nodes if n.row == 15]

    total_timelines = 0
    all_timelines = set()
    for end_point in bottom_row:
        for path in nx.all_simple_paths(graph, start, end_point):
            all_timelines.add(tuple(path))
    print(list(all_timelines)[500])
    return len(all_timelines)

def main():
    # print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()