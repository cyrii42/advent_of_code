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

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

DIRECTION_DELTAS = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
}

class NodeType(Enum):
    SAND = 0
    CLAY = 1
    WATER_FLOWING = 3
    WATER_SETTLED = 4

class Position(NamedTuple):
    x: int
    y: int

WATER_SPRING = Position(x=500, y=0)

@dataclass(frozen=True)
class Node:
    position: Position
    node_type: NodeType

    def __repr__(self):
        return (f"{self.node_type.name} (x={self.position.x}, " +
                f"y={self.position.y})")

# @dataclass
# class Water:
#     position: Position
#     settled: bool = False

#     def settle(self) -> None:
#         self.settled = True

@dataclass
class GroundwaterModel:
    position_dict: defaultdict[Position, NodeType]
    # graph: dict[Node, list[Node]]
    # water_list: list[Water] = field(default_factory=list)

    @property
    def min_y(self):
        return min(pos.y for pos, node_type in self.position_dict.items()
                   if node_type == NodeType.CLAY)

    @property
    def max_y(self):
        return max(pos.y for pos, node_type in self.position_dict.items()
                   if node_type == NodeType.CLAY)

    @property
    def min_x(self):
        return min(pos.x for pos, node_type in self.position_dict.items()
                   if node_type == NodeType.CLAY)

    @property
    def max_x(self):
        return max(pos.x for pos, node_type in self.position_dict.items()
                   if node_type == NodeType.CLAY)


    def model_water_flow(self):
        '''
        https://en.wikipedia.org/wiki/Flood_fill
        Flood-fill (node):
        1. Set Q to the empty queue or stack.
        2. Add node to the end of Q.
        3. While Q is not empty:
        4.   Set n equal to the first element of Q.
        5.   Remove first element from Q.
        6.   If n is Inside:
                Set the n
                Add the node to the west of n to the end of Q.
                Add the node to the east of n to the end of Q.
                Add the node to the north of n to the end of Q.  DON'T GO UP!!!
                Add the node to the south of n to the end of Q.
        7. Continue looping until Q is exhausted.
        8. Return.
        '''
        ...
        spring_x, spring_y = WATER_SPRING
        start_pos = Position(spring_x, max(spring_y, self.min_y))
        start_type = self.position_dict[start_pos]
        start_node = Node(start_pos, start_type)
        queue = deque([start_node])

        while queue:
            node = queue.popleft()
            match node.node_type:
                case NodeType.CLAY:
                    continue
                case NodeType.SAND:
                    ...
                case NodeType.WATER_FLOWING:
                    ...
                case NodeType.WATER_SETTLED:
                    ...

        return len([pos for pos, node_type in self.position_dict.items()
                    if self.min_y <= pos.y <= self.max_y
                    and node_type == NodeType.WATER_SETTLED])


    def print_diagram(self):
        water_positions = [w.position for w in self.water_list]
        clay_positions = [n.position for n in self.graph.keys() 
                          if n.node_type == NodeType.CLAY]

        for y in range(self.min_y-1, self.max_y+1):
            row = ''
            for x in range(self.min_x, self.max_x+2):
                pos = Position(x, y)
                if pos == WATER_SPRING:
                    row += '+'
                elif pos in water_positions:
                    water = next(w for w in self.water_list if w.position == pos)
                    row += '~' if water.settled else '|'
                elif pos in clay_positions:
                    row += '#'
                else:
                    row += '.'
            print(row)
   
def create_graph(pos_dict: dict[Position, NodeType]) -> dict[Node, list[Node]]:
    clay_positions = [p for p in pos_dict.keys()]
    min_y = min(pos.y for pos in clay_positions)
    max_y = max(pos.y for pos in clay_positions)
    output_dict = {}

    def get_pos_neighbor_coordinates(pos: Position) -> list[Node]:
        x, y = pos
        output_list = []
        for dir in Direction:
            dx, dy = DIRECTION_DELTAS[dir]
            neighbor_pos = Position(x + dx, y + dy)
            neighbor_type = pos_dict[neighbor_pos]
            output_list.append(Node(neighbor_pos, neighbor_type))
        return output_list
    
    for pos in clay_positions:
        node_type = pos_dict[pos]
        node = Node(pos, node_type)
        neighbor_list = []
        for neighbor in get_pos_neighbor_coordinates(pos):
            if min_y <= neighbor.position.y <= max_y:
                neighbor_list.append(neighbor)
        output_dict[node] = neighbor_list
        
    return output_dict

def create_node_list(clay_positions: list[Position]) -> list[Node]:
    min_x = min(position.x for position in clay_positions)
    min_y = min(position.y for position in clay_positions)
    max_x = max(position.x for position in clay_positions)
    max_y = max(position.y for position in clay_positions)

    output_list = []
    for y in range(min_y, max_y):
        for x in range(min_x-1, max_x+1):
            position = Position(x, y)
            node_type = (NodeType.CLAY if position in clay_positions
                         else NodeType.SAND)
            output_list.append(Node(position, node_type))
    return output_list
            
def parse_data(data: str) -> dict[Position, NodeType]:
    line_list = data.splitlines()
    clay_position_list = []
    output_dict = defaultdict(lambda: NodeType.SAND)
    for line in line_list:
        num_str, num_range_str = [s.replace('=', '') for s in line.split(', ')]
        num_axis = num_str[0]
        num = int(num_str[1:])
        start, end = [int(x) for x in num_range_str[1:].split('..')]
        num_range = range(start, end+1)
        if num_axis == 'x':
            for y in num_range:
                position = Position(x=num, y=y)
                if position not in clay_position_list:
                    clay_position_list.append(position)
        else:
            for x in num_range:
                position = Position(x=x, y=num)
                if position not in clay_position_list:
                    clay_position_list.append(position)
    output_dict.update({pos: NodeType.CLAY for pos in clay_position_list})
    return output_dict

def part_one(data: str):
    position_dict = parse_data(data)
    graph = create_graph(position_dict)
    model = GroundwaterModel(graph)
    print(model.min_x, model.min_y)
    print(model.max_x, model.max_y)
    if data == EXAMPLE:
        model.print_diagram()

def part_two(data: str):
    ...



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