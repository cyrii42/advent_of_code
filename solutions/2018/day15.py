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
        return (f"({self.node_type.name}: " + 
                f"x={self.position.x}, y={self.position.y})")

class NoTargetsRemaining(Exception):
    pass

class UnitType(Enum):
    GOBLIN = 0
    ELF = 1

@dataclass
class Unit:
    id: int
    node: Node
    hit_points: int = STARTING_HP
    attack_power: int = ATTACK_POWER

    @property
    def enemy_type(self) -> UnitType:
        return UnitType.GOBLIN if isinstance(self, Elf) else UnitType.ELF

    def sort_units(self, unit_list: list["Unit"]) -> list["Unit"]:
        unit_list.sort(key=lambda unit: unit.node.position.x)
        unit_list.sort(key=lambda unit: unit.node.position.y)
        return unit_list

    def simulate_round(self, unit_list: list["Unit"], graph: dict[Node, list[Node]]):
        targets = self.identify_targets(unit_list)
        if not targets:
            raise NoTargetsRemaining
        
        adjacent_targets = self.sort_units([t for t in targets 
                                            if self.is_adjacent(t, graph)])
        if adjacent_targets:
            attack_target = adjacent_targets[0]
            self.attack(attack_target)
            
        else:
            self.move(graph)
            adjacent_targets = self.sort_units([t for t in targets 
                                                if self.is_adjacent(t, graph)])
            if adjacent_targets:
                attack_target = adjacent_targets[0]
                self.attack(attack_target)
            
    def identify_targets(self, 
                         unit_list: list["Unit"], 
                         ) -> list["Unit"]:
        ''' Each unit begins its turn by identifying all possible targets (enemy_type 
        units). If no targets remain, combat ends.

        Then, the unit identifies all of the open squares (.) that are in range 
        of each target; these are the squares which are adjacent (immediately up, 
        down, left, or right) to any target and which aren't already occupied by 
        a wall or another unit. Alternatively, the unit might already be in range 
        of a target. If the unit is not already in range of a target, and there are
        no open squares which are in range of a target, the unit ends its turn. '''
        match self.enemy_type:
            case UnitType.GOBLIN:
                return [unit for unit in unit_list if isinstance(unit, Goblin)]
            case UnitType.ELF:
                return [unit for unit in unit_list if isinstance(unit, Elf)]

    def identify_target_squares(self, 
                                target_list: list["Unit"],
                                graph: dict[Node, list[Node]]
                                ) -> list[Node]:
        ...

    def is_adjacent(self, target: "Unit", graph: dict[Node, list[Node]]) -> bool:
        ...

    def move(self, target_squares: list[Node], graph: dict[Node, list[Node]]):
        ''' To move, the unit first considers the squares that are in range and 
        determines which of those squares it could reach in the fewest steps. A 
        step is a single movement to any adjacent (immediately up, down, left, or 
        right) open (.) square. Units cannot move into walls or other units. The 
        unit does this while considering the current positions of units and does 
        not do any prediction about where units will be later. If the unit cannot 
        reach (find an open path to) any of the squares that are in range, it ends 
        its turn. If multiple squares are in range and tied for being reachable in 
        the fewest steps, the square which is first in reading order is chosen. 

        The unit then takes a single step toward the chosen square along the shortest 
        path to that square. If multiple steps would put the unit equally closer to 
        its destination, the unit chooses the step which is first in reading order. 
        (This requires knowing when there is more than one shortest path so that you 
        can consider the first step of each such path.) '''
        ...

    def attack(self, target: "Unit"):
        ''' After moving (or if the unit began its turn in range of a target), 
        the unit attacks.

        To attack, the unit first determines all of the targets that are in range 
        of it by being immediately adjacent to it. If there are no such targets, 
        the unit ends its turn. Otherwise, the adjacent target with the fewest hit
        points is selected; in a tie, the adjacent target with the fewest hit points 
        which is first in reading order is selected.

        The unit deals damage equal to its attack power to the selected target, reducing 
        its hit points by that amount. If this reduces its hit points to 0 or fewer, 
        the selected target dies: its square becomes . and it takes no further turns. '''
        ...
    

class Elf(Unit):
    pass

class Goblin(Unit):
    pass



@dataclass
class Game:
    graph: dict[Node, list[Node]] = field(repr=False)
    units: list[Unit]
    rounds_completed: int = 0

    def sort_nodes(self, node_list: list[Node]) -> list[Node]:
        node_list.sort(key=lambda node: node.position.x)
        node_list.sort(key=lambda node: node.position.y)
        return node_list

    def sort_units(self, unit_list: list[Unit]) -> list[Unit]:
        unit_list.sort(key=lambda unit: unit.node.position.x)
        unit_list.sort(key=lambda unit: unit.node.position.y)
        return unit_list

    def sort_all_units(self) -> None:
        self.units = self.sort_units(self.units)

    def simulate_combat(self):
        while True:
            self.sort_all_units()
            for unit in self.units:
                try:
                    unit.simulate_round(self.units, self.graph)
                except NoTargetsRemaining:
                    raise             
            self.rounds_completed += 1

    def solve_part_one(self) -> int:
        try:
            self.simulate_combat()
        except NoTargetsRemaining:
            return self.rounds_completed * sum(unit.hit_points for unit in self.units)

def find_shortest_path(start_node: Node, end_node: Node, graph: dict) -> int:
    queue = deque([(start_node, [])])

    visited = set()
    visited.add(start_node)

    while queue:
        node, path = queue.popleft()
        if node == end_node:
            return len(path)
        neighbors = graph[node]
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
                visited.add(neighbor)
    return -1

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
    ...

def part_one(data: str):
    node_list, unit_list = parse_data(data)
    graph = create_graph(node_list)
    game = Game(graph, unit_list)

    for unit in game.units:
        print(unit.enemy_type)
    
    return game.solve_part_one()

def part_two(data: str):
    ...



def main():
    # part_one_tests():
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()