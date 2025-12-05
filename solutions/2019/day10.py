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



    


def count_asteroids_along_vector(node: Node, direction: Direction, node_dict: NodeDict) -> int:
    x, y, _ = node
    dx, dy = DIRECTION_DELTAS[direction]

    total_asteroids = 0
    print(f"{node.x},{node.y} - {direction.name}")
    while True:
        x, y = (x + dx, y + dy)
        try:
            node_at_point = node_dict[(x, y)]
            if node_at_point.node_type == NodeType.ASTEROID:
                print(f"\t - {node_at_point.node_type}")
        except KeyError:
            return total_asteroids
        else:
            if node_at_point.node_type == NodeType.ASTEROID:
                total_asteroids += 1    

def count_detectable_asteroids(node: Node, node_dict: NodeDict) -> int:
    # for each of the eight directions, count the total number of asteroids along
    # that vector -- for each vector, any asteroids after the first one are blocked

    total_asteroids = len([node for node in node_dict.values() if node.node_type == NodeType.ASTEROID])
    total_blocked_asteroids = 0
    print(f"\n----- {node.x},{node.y} ({total_asteroids} total asteroids) -----")
    for direction in Direction:
        total_asteroids_on_vector = count_asteroids_along_vector(node, direction, node_dict)
        total_blocked_asteroids += max(0, total_asteroids_on_vector - 1)
    total_detectable_asteroids = total_asteroids - total_blocked_asteroids - 1
    print(f"{node.x},{node.y}: {total_blocked_asteroids} blocked asteroids")
    print(f"{node.x},{node.y}: {total_detectable_asteroids} detectable asteroids")
    return total_detectable_asteroids
                
    
def part_one(data: str):
    # print(data)
    # node_dict = create_node_dict(data)
    # count_asteroids_along_lines_of_sight([n for n in node_dict.values() if n.node_type == NodeType.ASTEROID][0], node_dict)

    # all_asteroid_nodes = [node for node in node_dict.values() if node.node_type == NodeType.ASTEROID]
    # highest_total = 0
    # for node in all_asteroid_nodes:
    #     detectable_asteroids = count_detectable_asteroids(node, node_dict)
    #     # print(node, detectable_asteroids)
    #     highest_total = max(highest_total, detectable_asteroids)
    # return highest_total

    node_dict = create_node_dict(data)
    asteroids = [n for n in node_dict.values() if n.node_type == NodeType.ASTEROID]
    num_asteroids = len(asteroids)
    print(num_asteroids)
    blocked_dict = {asteroid: (num_asteroids - count_asteroids_along_lines_of_sight(asteroid, node_dict) - 1) for asteroid in asteroids}
    print(blocked_dict)
        

def count_asteroids_along_lines_of_sight(node1: Node, node_dict: NodeDict) -> int:
    print(node1)
    other_asteroids = [n for n in node_dict.values() if n != node1 and n.node_type == NodeType.ASTEROID]

    angle_set = set()
    blocked_asteroids = 0
    for node2 in other_asteroids:
        angle = abs(math.atan2(node2.y, node2.x) - math.atan2(node1.y, node1.x))
        print(angle)
        if angle in angle_set and node2.node_type == NodeType.ASTEROID:
            blocked_asteroids += 1
            print(f"blocked asteroid: {node2}")
        angle_set.add(angle)
    return blocked_asteroids


def part_two(data: str):
    ...

def find_integer_points_along_line(rise: int, run: int):
    slope = rise / run
    

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    # random_tests()

def random_tests():
    x1, y1 = (3, 4)
    x2, y2 = (1, 0)
    # x1, y1 = (3, 10)
    # x2, y2 = (8.3, 16.5)
    rise = y2 - y1
    run = x2 - x1
    slope = rise / run
    numerator, denominator = slope.as_integer_ratio()

    # print(math.gcd(-2, -4) + 1)
    # print()
    # print(math.tan(slope))
    print(slope)
    print(math.atan2(rise, run))
           
if __name__ == '__main__':
    main()