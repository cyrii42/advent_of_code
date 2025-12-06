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

TESTS_PART_ONE = [
    (aoc.DATA_DIR / '2019.10_example1.txt', 33),
    (aoc.DATA_DIR / '2019.10_example2.txt', 35),
    (aoc.DATA_DIR / '2019.10_example3.txt', 41),
    (aoc.DATA_DIR / '2019.10_example4.txt', 210),
]
TESTS_PART_TWO = [(aoc.DATA_DIR / '2019.10_example4.txt', 802)]

type NodeDict = dict[tuple[int, int], Node]
type NodeGraph = dict[Node, list[Node]]

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

# X, Y (starting at upper left and going down; positive is)
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

class NodeType(Enum):
    EMPTY = 0
    ASTEROID = 1

class Point(NamedTuple):
    x: int
    y: int

class Node(NamedTuple):
    x: int
    y: int
    node_type: NodeType

def create_node_dict(data: str) -> NodeDict:
    line_list = data.splitlines()
    node_list: list[Node] = []
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            node_type = NodeType.ASTEROID if char == '#' else NodeType.EMPTY
            node_list.append(Node(x, y, node_type))
    node_dict = {(node.x, node.y): node for node in node_list}
    return node_dict
        
def create_graph(node_dict: NodeDict) -> NodeGraph:
    graph = {}
    
    for node in node_dict.values():
        neighbor_list = []
        for direction in Direction:
            dx, dy = DIRECTION_DELTAS[direction]
            try:
                neighbor = node_dict[(node.x + dx, node.y + dy)]
                neighbor_list.append(neighbor)
            except KeyError:
                continue
        graph[node] = neighbor_list
        
    return graph

def get_slope(node1: Node, node2: Node) -> float:
    x1, y1, _ = node1
    x2, y2, _ = node2
    rise = y2 - y1
    run = x2 - x1
    try:
        return rise / run
    except ZeroDivisionError:
        return float('nan')

def get_atan2(node1: Node, node2: Node) -> float:
    x1, y1, _ = node1
    x2, y2, _ = node2
    rise = y2 - y1
    run = x2 - x1
    return math.atan2(rise, run)

def test_slope_and_atan2(asteroids: list[Node]):
    test = asteroids[5]
    print(test)
    for a in asteroids:
        if a == test:
            continue
        print(f"Asteroid {a.x},{a.y}: {get_atan2(test, a)} {get_slope(test, a)}")

def part_one(data: str):
    node_dict = create_node_dict(data)
    a_list = [n for n in node_dict.values() if n.node_type == NodeType.ASTEROID]

    a_dict = {a1: len({get_atan2(a1, a2) for a2 in a_list if a1 != a2}) for a1 in a_list}
    return max(a_dict.values())

def part_two(data: str):
    ...

def run_tests(tests: list[tuple[Path, int]], fn: Callable):
    for i, example in enumerate(tests, start=1):
        filepath, answer = example
        with open(filepath, 'r') as f:
            data = f.read()
        test_answer = fn(data)
        print(f"Test #{i}: {test_answer == answer}",
              f"({test_answer})")

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    run_tests(TESTS_PART_ONE, part_one)
    print(f"Part One (input):  {part_one(INPUT)}")
    run_tests(TESTS_PART_TWO, part_two)
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
           
if __name__ == '__main__':
    main()