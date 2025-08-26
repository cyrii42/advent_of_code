import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
from collections import deque
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

with open(aoc.DATA_DIR / '2016.22_example.txt') as f:
    EXAMPLE = f.read()
INPUT = aoc.get_input(YEAR, DAY)

class InsufficientDiskSpace(Exception):
    pass

class NodesNotAdjcacent(Exception):
    pass

class NoFreeNeighbors(Exception):
    pass

DIRECTIONS = {
    'UP':    (1, 0),
    'RIGHT': (0, 1),
    'DOWN':  (-1, 0),
    'LEFT':  (0, -1),
}

@dataclass
class Node:
    x: int
    y: int
    size: int = field(repr=True)
    used: int = field(repr=True)
    avail: int = field(repr=True)
    used_pct: int = field(repr=True)

    @property
    def coord(self) -> tuple[int, int]:
        return (self.x, self.y)

    def add_data(self, data: int) -> None:
        if self.used + data > self.size:
            raise InsufficientDiskSpace
        self.used += data
        self.avail -= data
        self.used_pct = math.ceil(self.used / self.size * 100)

    def extract_data(self) -> int:
        output = deepcopy(self.used)
        self.used = 0
        self.avail = self.size
        self.used_pct = 0
        return output
        
        
@dataclass
class Grid:
    nodes: list[Node]
    graph: dict[tuple[int, int], list[tuple[int, int]]] = field(init=False, repr=False)

    def __post_init__(self):
        self.graph = self.create_graph()

    @property
    def max_x(self) -> int:
        return max(node.x for node in self.nodes)

    @property
    def max_y(self) -> int:
        return max(node.y for node in self.nodes)

    @property
    def empty_nodes(self) -> list[Node]:
        return [node for node in self.nodes if node.used == 0]

    def create_graph(self) -> dict[tuple[int, int], list[tuple[int, int]]]:
        output = {}
        for x in range(self.max_x+1):
            for y in range(self.max_y+1):
                node = (x, y)
                neighbors = [(x+i, y+j) for i, j in DIRECTIONS.values() 
                              if x+i >= 0 and x+i <= self.max_x
                              and y+j >= 0 and y+j <= self.max_y]
                output[node] = neighbors
        return output

    def get_node_by_location(self, loc: tuple[int, int]) -> Node:
        x, y = loc
        return next(n for n in self.nodes if n.x == x and n.y == y)

    def check_adjacency(self, node1: Node, node2: Node) -> bool:
        return (node2.x, node2.y) in self.graph[(node1.x, node1.y)]

    def get_adjacent_nodes(self, node: Node) -> list[Node]:
        return [self.get_node_by_location(loc)
                for loc in self.graph[node.coord]]

    def get_adj_nodes_with_free_space(self, 
                                      start_node: Node) -> list[Node]:
        potential_nodes = self.get_adjacent_nodes(start_node)
        return [node for node in potential_nodes 
                if node.avail >= start_node.used]

    def move_data(self, node1: Node, node2: Node) -> None:
        if not self.check_adjacency(node1, node2):
            raise NodesNotAdjcacent
        if node1.used > node2.avail:
            raise InsufficientDiskSpace
        data = node1.extract_data()
        node2.add_data(data)
 
    def move_data_from_node(self, node: Node) -> Node:
        avail_neighbors = self.get_adj_nodes_with_free_space(node)
        if not avail_neighbors:
            raise NoFreeNeighbors
        else:
            self.move_data(node, avail_neighbors[0])
            return node

    def find_closest_empty_node_to_node(self, node: Node) -> Node:
        ...

    def allocate_free_space_adj_to_node(self, node: Node) -> None:
        if self.get_adj_nodes_with_free_space(node):
            return

        ...

        

    def solve_part_one(self) -> int:
        total = 0
        for a, b in itertools.permutations(self.nodes, 2):
            if a.used > 0 and a.used <= b.avail:
                total += 1
        return total

    def solve_part_two(self) -> int:
        ''' Your goal is to gain access to the data that begins in 
        the node with y=0 and the highest x (that is, the node in 
        the top-right corner).'''

        goal_node = self.get_node_by_location((self.max_x, 0))
        start = goal_node
        end = self.get_node_by_location((0, 0))
        queue = deque([(start, [start])])

        visited = set()
        visited.add(start.coord)

        while queue:
            node, path = queue.popleft()
            if node == end:
                return len(path) - 1
            avail_neighbors = self.get_adj_nodes_with_free_space(node)
            if not avail_neighbors:
                print(f"dead end at {node}")
                print(self.get_adjacent_nodes(node))
                try:
                    node = self.move_data_from_node(node)
                except NoFreeNeighbors:
                    raise
            else:
                for neighbor in avail_neighbors:
                    if neighbor.coord not in visited:
                        new_path = path + [neighbor]
                        queue.append((neighbor, new_path))
                        visited.add(neighbor.coord)
        return -1

def parse_data(data: str) -> Grid:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        if not line.startswith('/dev/grid/node-'):
            continue
        name, size, used, avail, used_pct = [x for x in line.split(' ') if x]
        x, y = name.removeprefix('/dev/grid/node-').split('-')
        output_list.append(Node(x=int(x.removeprefix('x')), 
                                y=int(y.removeprefix('y')), 
                                size=int(size.removesuffix('T')), 
                                used=int(used.removesuffix('T')), 
                                avail=int(avail.removesuffix('T')), 
                                used_pct=int(used_pct.removesuffix('%'))))
    return Grid(output_list)
    
def part_one(data: str):
    grid = parse_data(data)
    return grid.solve_part_one()

def part_two(data: str):
    grid = parse_data(data)
    print(grid.get_adjacent_nodes(grid.nodes[1]))
    return grid.solve_part_two()



def main():
    # print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()