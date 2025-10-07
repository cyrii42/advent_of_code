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

with open(aoc.DATA_DIR / '2018.13_example.txt', 'r') as f:
    EXAMPLE = f.read()
INPUT = aoc.get_input(YEAR, DAY)

sys.setrecursionlimit(10**6)

class TooManyNeigbors(Exception):
    pass

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
    VERTICAL = 0        # |
    HORIZONTAL = 1      # -
    CURVE_LEFT = 2      # \
    CURVE_RIGHT = 3     # /
    CURVE = 9           # \ or /
    INTERSECTION = 4    # +
    CART_UP = 5         # ^
    CART_DOWN = 6       # v
    CART_LEFT = 7       # <
    CART_RIGHT = 8      # >

class Position(NamedTuple):
    x: int
    y: int

@dataclass(frozen=True)
class Node:
    position: Position
    char: str = field(repr=False)
    node_type: NodeType = field(repr=False)

    def __repr__(self):
        return (f"({self.node_type.name}: " + 
                f"x={self.position.x}, y={self.position.y})")

class CartTurn(IntEnum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

class NotAnIntersection(Exception):
    pass

@dataclass
class Cart:
    id: int
    node: Node
    direction: Direction 
    intersection_dict: dict[Node, int] = field(init=False)

    def __post_init__(self):
        self.intersection_dict = defaultdict(int)

    def turn_left(self):
        self.direction = Direction((self.direction - 1) % len(Direction))

    def turn_right(self):
        self.direction = Direction((self.direction + 1) % len(Direction))

    def turn_at_curve(self):
        match [self.direction, self.node.node_type,]:
            case [Direction.NodeType.C]

    def turn_at_intersection(self) -> None:
        if self.node.node_type != NodeType.INTERSECTION:
            raise NotAnIntersection
     
        self.turn_type = self.intersection_dict[self.node] % len(CartTurn)
        match self.turn_type:
            case CartTurn.LEFT:
                self.turn_left()
            case CartTurn.RIGHT:
                self.turn_right()
            case _:
                pass
        self.intersection_dict[self.node] += 1

    def tick(self, graph: dict[Node, list[Node]]) -> None:
        x, y = (self.node.position.x, self.node.position.y)
        delta_x, delta_y = DIRECTION_DELTAS[self.direction]
        next_position = Position(x + delta_x, y + delta_y)
        try:
            next_node = next(n for n in graph[self.node] if n.position == next_position)  
        except StopIteration:
            print(f"Failed to find node at position {next_position}")
            print(graph[self.node])
            raise
        else:
            self.node = next_node
            if self.node.node_type == NodeType.INTERSECTION:
                self.turn_at_intersection()
            elif self.node.node_type == NodeType.CURVE_LEFT or NodeType.CURVE_RIGHT:
                self.turn_at_curve()

@dataclass
class CartGroup:
    carts: list[Cart]
    graph: dict[Node, list[Node]]

    def tick(self):
        for cart in self.carts:
            cart.tick(graph=self.graph)

        if len([cart.node for cart in self.carts]) < len(self.carts):
            print("COLLISION!!!!!!!!")
        

def get_node_neighbor_coordinates(node: Node) -> list[Position]:
    x, y = (node.position.x, node.position.y)

    output_list = []
    for dir in Direction:
        delta_x, delta_y = DIRECTION_DELTAS[dir]
        output_list.append(Position(x + delta_x, y + delta_y))
    return output_list

def create_graph(node_list: list[Node]) -> dict[Node, list[Node]]:
    output_dict: dict[Node, list[Node]] = {}
    
    for node in node_list:
        neighbor_list = []
        for x, y in get_node_neighbor_coordinates(node):
            try:
                neighbor_list.append(
                    next(node for node in node_list 
                        if node.position.x == x 
                        and node.position.y == y))
            except StopIteration:
                continue
        output_dict[node] = neighbor_list
        
    return output_dict

def find_start(node_list: list[Node]) -> Node:
    return next(node for node in node_list if node.position.y == 0)

def determine_next_direction(node: Node, next_node: Node) -> Direction:
    delta_x = next_node.position.x - node.position.x
    delta_y = next_node.position.y - node.position.y
    match (delta_x, delta_y):
        case (0, -1):
            return Direction.UP
        case (1, 0):
            return Direction.RIGHT
        case (0, 1):
            return Direction.DOWN
        case (-1, 0):
            return Direction.LEFT
        case _:
            raise ValueError

def walk_path(graph: dict[Node, list[Node]],
              node: Node,
              dir: Direction = Direction.DOWN,
              visited: Optional[list[tuple[Node, Direction]]] = None
              ) -> tuple[str, int]:
    if not visited:
        visited = []

    visited.append((node, dir))

    if node.node_type == NodeType.INTERSECTION:
        next_node = next(n for n in graph[node] if (n, dir) not in visited)
        next_dir = determine_next_direction(node, next_node)
        walk_path(graph, next_node, next_dir, visited)

    else:
        x, y = (node.position.x, node.position.y)
        delta_x, delta_y = DIRECTION_DELTAS[dir]
        next_x = x + delta_x
        next_y = y + delta_y
        try:
            next_node = next(n for n in graph[node] 
                             if n.position.x == next_x 
                             and n.position.y == next_y)    
            walk_path(graph, next_node, dir, visited) 
        except StopIteration:
            pass

    return (''.join(node.char for node, _ in visited if node.char.isalpha()),
            len(visited))

def parse_data(data: str) -> tuple[list[Node], list[Cart]]:
    line_list = data.splitlines()
    node_list, cart_list = ([], [])
    next_cart_id = 0
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            if char == ' ':
                continue
            elif char == '|':
                node_type = NodeType.VERTICAL
            elif char == '-':
                node_type = NodeType.HORIZONTAL

            #### CURVE CAN BE LEFT OR RIGHT DEPENDING ON THE DIRECTION YOU'RE COMING FROM ####  
            elif char in ['\\', '/']:
                node_type = NodeType.CURVE  
            # elif char == '\\':
            #     node_type = NodeType.CURVE_LEFT
            # elif char == '/':
            #     node_type = NodeType.CURVE_RIGHT


            elif char == '+':
                node_type = NodeType.INTERSECTION
            elif char == '^':
                node_type = NodeType.VERTICAL
                cart_list.append(Cart(id=next_cart_id,
                                      node=Node(Position(x, y), char, node_type),
                                      direction=Direction.UP))
                next_cart_id += 1
            elif char == 'v':
                node_type = NodeType.VERTICAL
                cart_list.append(Cart(id=next_cart_id,
                                      node=Node(Position(x, y), char, node_type),
                                      direction=Direction.DOWN))
                next_cart_id += 1
            elif char == '<':
                node_type = NodeType.HORIZONTAL
                cart_list.append(Cart(id=next_cart_id,
                                      node=Node(Position(x, y), char, node_type),
                                      direction=Direction.LEFT))
                next_cart_id += 1
            elif char == '>':
                node_type = NodeType.HORIZONTAL
                cart_list.append(Cart(id=next_cart_id,
                                      node=Node(Position(x, y), char, node_type),
                                      direction=Direction.RIGHT))
                next_cart_id += 1
            else:
                raise ValueError
            node_list.append(Node(Position(x, y), char, node_type))
    return (node_list, cart_list)
    
def part_one(data: str):
    node_list, cart_list = parse_data(data)
    graph = create_graph(node_list)
    cart_group = CartGroup(cart_list, graph)

    for _ in range(20):
        cart_group.tick()
    
    # start = find_start(node_list)
    # p1_answer, p2_answer = walk_path(graph, start)
    # print(f"Part One:  {p1_answer}")
    # print(f"Part Two:  {p2_answer}")

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    direction = Direction.UP
    print(Direction((direction + 1) % len(Direction)).name)

       
if __name__ == '__main__':
    main()