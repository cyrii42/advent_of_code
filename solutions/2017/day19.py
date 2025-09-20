import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Literal, NamedTuple, Optional, Protocol, Self

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

class TooManyNeigbors(Exception):
    pass

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

DIRECTION_DELTAS = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}

class NodeType(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    CORNER = 2
    LETTER = 3

@dataclass(frozen=True)
class Node:
    x: int
    y: int
    char: str
    node_type: NodeType = field(repr=False)

def get_node_neighbor_coordinates(node: Node) -> list[tuple[int, int]]:
    x, y = (node.x, node.y)

    output_list = []
    for dir in Direction:
        delta_x, delta_y = DIRECTION_DELTAS[dir]
        output_list.append((x + delta_x, y + delta_y))
    return output_list

def create_graph(node_list: list[Node]) -> dict[Node, list[Node]]:
    output_dict: dict[Node, list[Node]] = {}
    
    for node in node_list:
        neighbor_list = []
        for x, y in get_node_neighbor_coordinates(node):
            try:
                neighbor_list.append(
                    next(node for node in node_list 
                        if node.x == x and node.y == y))
            except StopIteration:
                continue
        output_dict[node] = neighbor_list
        
    return output_dict

def find_start(node_list: list[Node]) -> Node:
    return next(node for node in node_list if node.y == 0)

def determine_next_direction(node: Node, next_node: Node) -> Direction:
    delta_x = next_node.x - node.x
    delta_y = next_node.y - node.y
    match (delta_x, delta_y):
        case (0, -1):
            return Direction.NORTH
        case (1, 0):
            return Direction.EAST
        case (0, 1):
            return Direction.SOUTH
        case (-1, 0):
            return Direction.WEST

def walk_path(graph: dict[Node, list[Node]],
              node: Node,
              dir: Direction = Direction.SOUTH,
              visited: Optional[list[tuple[Node, Direction]]] = None
              ) -> list[str]:
    if not visited:
        visited = []

    visited.append((node, dir))

    if node.node_type == NodeType.CORNER:
        x, y = (node.x, node.y)
        valid_neighbors = [n for n in graph[node] if (n, dir) not in visited]
        if len(valid_neighbors) > 1:
            print(node, valid_neighbors)
            raise TooManyNeigbors
        try:
            next_node = next(n for n in graph[node] if (n, dir) not in visited)
            next_dir = determine_next_direction(node, next_node)
            print(f"FOUND A CORNER - next node: {next_node} - next dir: {next_dir}")
            walk_path(graph, next_node, next_dir, visited)
        except StopIteration:
            print('end')

    if node.node_type != NodeType.CORNER:
        x, y = (node.x, node.y)
        delta_x, delta_y = DIRECTION_DELTAS[dir]
        next_x = x + delta_x
        next_y = y + delta_y
        try:
            # print(f"Neighbors: {graph[node]}")
            # print(f"Next X: {next_x}, Next Y: {next_y}")
            next_node = next(n for n in graph[node] 
                             if n.x == next_x and n.y == next_y)
            # print(f"Next: {next_node}")
            walk_path(graph, next_node, dir, visited)
        except (StopIteration, RecursionError):
            print('end')
    return visited
    return [node.char for node, _ in visited if node.char.isalpha()]
    

# def walk_path(graph: dict[Node, list[Node]],
#               node: Node,
#               dir: Direction = Direction.SOUTH,
#               visited: Optional[list[tuple[Node, Direction]]] = None,
#               ) -> list[str]:
#     ''' i think we have to keep track of the direction somehow -- that 
#     will actually simplify things, perhaps -- you only change direction
#     if the only available neighbor is a corner -- plus you can't just
#     keep a list of visited nodes; you have to keep a list of TUPLES: 
#     (node, direction) '''
    
#     if not visited:
#         visited = []

#     visited.append((node, dir))
#     for neighbor in graph[node]:
#         if (neighbor, dir) not in visited:
#             if dir in [Direction.NORTH, Direction.SOUTH]:
#                 if neighbor.node_type in [NodeType.VERTICAL, NodeType.LETTER]:
#                     walk_path(graph, neighbor, dir, visited)
#                 elif neighbor.node_type == NodeType.CORNER:
#                     dir = Direction.EAST if dir == Direction.NORTH else Direction.WEST
#                     walk_path(graph, neighbor, dir, visited)
#                 elif neighbor.node_type == NodeType.HORIZONTAL:
#                     walk_path(graph, neighbor, dir, visited)

#             else:
#                 ...

            # if node.node_type == NodeType.LETTER:
            #     walk_path(graph, neighbor, dir, visited)
            # elif node.node_type == NodeType.CORNER:
            #     walk_path(graph, neighbor, dir, visited)
            # elif neighbor.node_type == node.node_type:
            #     walk_path(graph, neighbor, dir, visited)
            # elif neighbor.node_type == NodeType.LETTER:
            #     walk_path(graph, neighbor, dir, visited)
            # elif neighbor.node_type == NodeType.CORNER:
            #     walk_path(graph, neighbor, dir, visited)

    # print(visited)
    # return [node.char for node, _ in visited 
    #         if node.node_type == NodeType.LETTER]


def parse_data(data: str) -> list[Node]:
    line_list = data.splitlines()
    output_list = []
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
                if char == ' ':
                    continue
                elif char == '|':
                    node_type = NodeType.VERTICAL
                elif char == '-':
                    node_type = NodeType.HORIZONTAL
                elif char == '+':
                    node_type = NodeType.CORNER
                else:
                    node_type = NodeType.LETTER
                output_list.append(Node(x, y, char, node_type))
    return output_list
    
def part_one(data: str):
    node_list = parse_data(data)
    graph = create_graph(node_list)
    start = find_start(node_list)
    print(f"START: {start}")
    return walk_path(graph, start)
    

def part_two(data: str):
    __ = parse_data(data)



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