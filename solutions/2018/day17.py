import functools
import hashlib
import heapq
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
from enum import Enum, Flag, IntEnum, StrEnum, auto
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

    @property
    def left(self) -> "Direction":
        return Direction((self.value -1 ) % 4)

    @property
    def right(self) -> "Direction":
        return Direction((self.value + 1) % 4)

    @property
    def opposite(self) -> "Direction":
        return Direction((self.value + 2) % 4)
        
DIRECTION_DELTAS = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
}

class NodeType(Flag):
    SOURCE = auto()
    SAND = auto()
    CLAY = auto()
    WATER_FLOWING = auto()
    WATER_SETTLED = auto()
    WATER = WATER_FLOWING | WATER_SETTLED

class Position(NamedTuple):
    x: int
    y: int

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

WATER_SPRING = Position(x=500, y=0)

@dataclass(frozen=True)
class Node:
    position: Position
    node_type: NodeType

    def __repr__(self):
        return (f"{self.node_type.name} (x={self.position.x}, " +
                f"y={self.position.y})")

@dataclass
class GroundwaterModel:
    position_dict: defaultdict[Position, NodeType]
    sources: list[Position] = field(default_factory=list)
    min_y: int = field(init=False)
    max_y: int = field(init=False)
    min_x: int = field(init=False)
    max_x: int = field(init=False)

    def __post_init__(self):
        self.min_y = min(pos.y for pos, node_type in self.position_dict.items()
                         if node_type == NodeType.CLAY)
        self.max_y = max(pos.y for pos, node_type in self.position_dict.items()
                         if node_type == NodeType.CLAY)
        self.min_x = min(pos.x for pos, node_type in self.position_dict.items()
                         if node_type == NodeType.CLAY)
        self.max_x = max(pos.x for pos, node_type in self.position_dict.items()
                         if node_type == NodeType.CLAY)

    @property
    def num_water_nodes(self) -> int:
        return len([pos for pos, node_type in self.position_dict.items()
                    if pos.y >= self.min_y
                    and pos.y <= self.max_y
                    and node_type in [NodeType.WATER_FLOWING, 
                                      NodeType.WATER_SETTLED]])

    def get_type(self, pos: Position) -> NodeType:
        return self.position_dict[pos]

    def set_type(self, pos: Position, node_type: NodeType) -> None:
        self.position_dict[pos] = node_type
    
    @staticmethod
    def get_position(pos: Position, direction: Direction):
        dx, dy = DIRECTION_DELTAS[direction]
        return Position(pos.x+dx, pos.y+dy)

    def model_water_flow(self):
        ''' https://gist.github.com/CameronAavik/f052fdca87715429e28b3fdfce243298 '''

        self.sources.append(WATER_SPRING)

        while self.sources:
            # get the latest water source and ensure that it hasn't been replaced
            # with still water
            pos = self.sources.pop()
            if self.get_type(pos) == NodeType.WATER_SETTLED:
                continue

            # follow the stream down by incrementing the y variable. Once we hit a
            # wall we then fill it up a level at a time by searching for a wall or
            # an overflow both left and right. If there were no overflows, fill
            # with still water, else fill with moving water
            pos = self.get_position(pos, Direction.DOWN)
            while pos.y <= self.max_y:
                match self.get_type(pos):
                    case NodeType.SAND:
                        self.set_type(pos, NodeType.WATER_FLOWING)
                        pos = self.get_position(pos, Direction.DOWN)
                    case NodeType.CLAY | NodeType.WATER_SETTLED:
                        pos = self.get_position(pos, Direction.UP)
                        left_pos, left_overflow = self.search(pos, Direction.LEFT)
                        right_pos, right_overflow = self.search(pos, Direction.RIGHT)
                        for x in range(left_pos.x, right_pos.x + 1):
                            if left_overflow or right_overflow:
                                water_type = NodeType.WATER_FLOWING
                            else:
                                water_type = NodeType.WATER_SETTLED
                            self.set_type(Position(x, pos.y), water_type)
                    case NodeType.WATER_FLOWING:
                        break

    def search(self, pos: Position, 
               direction: Direction
               ) -> tuple[Position, bool]:
        while True:
            pos_below = self.get_position(pos, Direction.DOWN)
            # if we hit a wall, go back 1 and return no overflow
            if self.get_type(pos) == NodeType.CLAY:
                return (self.get_position(pos, direction.opposite), False)
            
            # if the tile below is empty, then we have overflowed; 
            # create a new water source
            if self.get_type(pos_below) == NodeType.SAND:
                self.sources.append(pos)
                return (pos, True)
            
            # if the current tile and the tile below are both streams, then we 
            # have overflowed into an existing stream; no need to add a new source
            if (self.get_type(pos) == NodeType.WATER_FLOWING
                and self.get_type(pos_below) == NodeType.WATER_FLOWING):
                return (pos, True)
            
            pos = self.get_position(pos, direction)


    def print_diagram(self):
        for y in range(self.min_y-1, self.max_y+1):
            row = ''
            for x in range(self.min_x, self.max_x+2):
                pos = Position(x, y)
                if pos == WATER_SPRING:
                    row += '+'
                else:
                    match self.position_dict[pos]:
                        case NodeType.SAND:
                            row += '.'
                        case NodeType.CLAY:
                            row += '#'
                        case NodeType.WATER_FLOWING:
                            row += '|'
                        case NodeType.WATER_SETTLED:
                            row += '~'
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
            
def parse_data(data: str) -> defaultdict[Position, NodeType]:
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
    model = GroundwaterModel(position_dict)
    if data == EXAMPLE:
        model.print_diagram()
    model.model_water_flow()
    if data == EXAMPLE:
        print()
        model.print_diagram()
    return model.num_water_nodes
 
def part_two(data: str):
    ...



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    d = Direction.RIGHT
    print(d.left.name)

       
if __name__ == '__main__':
    main()