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

INPUT = aoc.get_input(YEAR, DAY)
TESTS_PART_ONE = [
    ("#######\n#.G...#\n#...EG#\n#.#.#G#\n#..G#E#\n#.....#\n#######", 47, 590, 27730),
    ("#######\n#G..#E#\n#E#E.E#\n#G.##.#\n#...#E#\n#...E.#\n#######", 37, 982, 36334),
    ("#######\n#E..EG#\n#.#G.E#\n#E.##E#\n#G..#.#\n#..E#.#\n#######\n", 46, 859, 39514),
    ("#######\n#E.G#.#\n#.#G..#\n#G.#.G#\n#G..#.#\n#...E.#\n#######\n", 35, 793, 27755), 
    ("#######\n#.E...#\n#.#..G#\n#.###.#\n#E#G#G#\n#...#G#\n#######\n", 54, 536, 28944),
    ("#########\n#G......#\n#.E.#...#\n#..##..G#\n#...##..#\n#...#...#\n#.G...G.#\n#.....G.#\n#########\n", 20, 937, 18740),
]

STARTING_HP = 200
ATTACK_POWER = 3

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

class Position(NamedTuple):
    x: int
    y: int

class NodeType(Enum):
    WALL = 0
    CAVERN = 1

@dataclass(frozen=True)
class Node:
    position: Position
    node_type: NodeType

    def __repr__(self):
        return (f"x={self.position.x}, y={self.position.y}")

class NoTargetsRemaining(Exception):
    pass

class UnitType(Enum):
    GOBLIN = 0
    ELF = 1

class NodePath(NamedTuple):
    nodes: list[Node]

@dataclass
class Unit:
    id: int
    node: Node
    hit_points: int = STARTING_HP
    attack_power: int = ATTACK_POWER

    @property
    def unit_type(self) -> UnitType:
        return UnitType.ELF if isinstance(self, Elf) else UnitType.GOBLIN  

    @property
    def enemy_type(self) -> UnitType:
        return UnitType.GOBLIN if isinstance(self, Elf) else UnitType.ELF   

    def simulate_round(self, unit_list: list["Unit"], graph: dict[Node, list[Node]]):
        target_list = self.identify_targets(unit_list)
        if not target_list:
            raise NoTargetsRemaining
        
        adjacent_targets = sort_units([t for t in target_list 
                                       if self.is_adjacent(t, graph)])
        if adjacent_targets:
            self.attack(adjacent_targets[0])
            
        else:
            self.move(target_list, graph)
            adjacent_targets = sort_units([t for t in target_list 
                                           if self.is_adjacent(t, graph)])
            if adjacent_targets:
                self.attack(adjacent_targets[0])

    def identify_targets(self, unit_list: list["Unit"]) -> list["Unit"]:
        match self.enemy_type:
            case UnitType.GOBLIN:
                return [unit for unit in unit_list 
                        if isinstance(unit, Goblin) and unit.hit_points > 0]
            case UnitType.ELF:
                return [unit for unit in unit_list 
                        if isinstance(unit, Elf) and unit.hit_points > 0]

    def is_adjacent(self, target: "Unit", graph: dict[Node, list[Node]]) -> bool:
        return target.node in graph[self.node]

    def move(self, target_list: list["Unit"], graph: dict[Node, list[Node]]):
        target_squares = self.identify_target_squares(target_list, graph)
        next_node = self.find_next_node(target_squares, graph)
        # print(f"Moving {self.unit_type.name} #{self.id} to {next_node}")
        self.node = next_node      

    def identify_target_squares(self, target_list: list["Unit"], 
                                graph: dict[Node, list[Node]]) -> list[Node]:
        return [node for target in target_list for node in graph[target.node]]

    def find_next_node(self, target_squares: list[Node], 
                       graph: dict[Node, list[Node]]) -> Node:
        eligible_paths = [find_shortest_paths(self.node, target_square, graph) 
                          for target_square in target_squares]
        shortest_path_length = min(length for _, length in eligible_paths)
        shortest_path_lists = [path_list for path_list, length in eligible_paths 
                          if length == shortest_path_length]
        shortest_paths = [path for path_list in shortest_path_lists for path in path_list]
        if len(shortest_paths) == 1:
            return shortest_paths[0].nodes[0]
        else:
            first_nodes = [path.nodes[0] for path in shortest_paths]
            first_nodes_sorted = sort_nodes(first_nodes)
            return first_nodes_sorted[0]

    def attack(self, target: "Unit"):
        # print(f"{self.unit_type.name} #{self.id} ({self.node}) " + 
            #   f"attacking {target.unit_type.name} #{target.id} ({target.node})")
        target.hit_points -= self.attack_power
    

class Elf(Unit):
    pass

class Goblin(Unit):
    pass



@dataclass
class Game:
    graph: dict[Node, list[Node]] = field(repr=False)
    units: list[Unit]
    rounds_completed: int = 0

    def sort_all_units(self) -> None:
        self.units = sort_units(self.units)

    def simulate_combat(self):
        while True:
            self.sort_all_units()
            unit_list = deepcopy(self.units)
            for unit in self.units:
                try:
                    unit.simulate_round(self.units, self.graph)
                except NoTargetsRemaining:
                    raise             
            self.rounds_completed += 1

    def solve_part_one(self) -> tuple[int, int, int]:
        try:
            self.simulate_combat()
        except NoTargetsRemaining:
            return (self.rounds_completed,
                    sum(unit.hit_points for unit in self.units),
                    (self.rounds_completed * sum(unit.hit_points 
                                                for unit in self.units)))



def sort_units(unit_list: list[Unit]) -> list[Unit]:
    unit_list.sort(key=lambda unit: unit.node.position.x)
    unit_list.sort(key=lambda unit: unit.node.position.y)
    return unit_list

def sort_nodes(node_list: list[Node]) -> list[Node]:
    node_list.sort(key=lambda node: node.position.x)
    node_list.sort(key=lambda node: node.position.y)
    return node_list



def find_shortest_paths(start_node: Node, 
                        end_node: Node, 
                        graph: dict[Node, list[Node]]
                        ) -> tuple[list[NodePath], int]:
    queue = deque([(start_node, [])])

    visited = set()
    visited.add(start_node)

    shortest_path_length = 999999999
    output_list = []
    while queue:
        node, path = queue.popleft()
        if node == end_node:
            if len(path) < shortest_path_length:
                shortest_path_length = len(path)
                output_list = [NodePath(path)]
            elif len(path) == shortest_path_length:
                output_list.append(NodePath(path))
            else:
                return (output_list, shortest_path_length)
        neighbors = graph[node]  # NEED TO EXCLUDE NODES THAT HAVE ANOTHER UNIT ON THEM
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
                visited.add(neighbor)
    return (output_list, shortest_path_length)

def create_graph(node_list: list[Node]) -> dict[Node, list[Node]]:
    output_dict: dict[Node, list[Node]] = {}

    def get_node_neighbor_coordinates(node: Node) -> list[Position]:
        x, y = (node.position.x, node.position.y)

        output_list = []
        for dir in Direction:
            delta_x, delta_y = DIRECTION_DELTAS[dir]
            output_list.append(Position(x + delta_x, y + delta_y))
        return output_list
    
    for node in node_list:
        if node.node_type == NodeType.WALL:
            continue
        neighbor_list = []
        for x, y in get_node_neighbor_coordinates(node):
            try:
                neighbor_list.append(
                    next(node for node in node_list 
                        if node.position.x == x 
                        and node.position.y == y
                        and node.node_type != NodeType.WALL))
            except StopIteration:
                continue
        output_dict[node] = neighbor_list
        
    return output_dict

def parse_data(data: str) -> tuple[list[Node], list[Unit]]:
    line_list = data.splitlines()
    node_list, unit_list = ([], [])
    next_unit_id = 0
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            if char == ' ':
                continue
            elif char == '#':
                node_type = NodeType.WALL
            elif char == '.':
                node_type = NodeType.CAVERN
            elif char == 'G':
                node_type = NodeType.CAVERN
                unit_list.append(Goblin(next_unit_id,
                                        Node(Position(x, y), node_type)))
                next_unit_id += 1
            elif char == 'E':
                node_type = NodeType.CAVERN
                unit_list.append(Elf(next_unit_id,
                                     Node(Position(x, y), node_type)))
                next_unit_id += 1
            else:
                raise ValueError
            node_list.append(Node(Position(x, y), node_type))
    return (node_list, unit_list)

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        data, num_rounds, total_hp, outcome = example
        test_num_rounds, test_total_hp, test_outcome = part_one(data)
        print(f"Test #{i}: {test_outcome == outcome}",
              f"({test_num_rounds} rounds, {test_total_hp} total HP, {test_outcome} outcome)")

def part_one(data: str):
    node_list, unit_list = parse_data(data)
    graph = create_graph(node_list)
    game = Game(graph, unit_list)

    # for unit in game.units:
    #     print(unit.enemy_type)
    
    return game.solve_part_one()

def part_two(data: str):
    ...



def main():
    part_one_tests()
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()