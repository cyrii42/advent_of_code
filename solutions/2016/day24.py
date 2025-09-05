import functools
import itertools
import math
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import NamedTuple

from alive_progress import alive_bar
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

DIRECTIONS = {
    'UP':    (1, 0),
    'RIGHT': (0, 1),
    'DOWN':  (-1, 0),
    'LEFT':  (0, -1),
}

class PointType(Enum):
    WALL = 0
    OPEN = 1
    START = 2
    LOCATION = 3

class Node(NamedTuple):
    x: int
    y: int
    type: PointType

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

@dataclass
class Grid:
    nodes: list[Node]
    graph: dict[Node, list[Node]] = field(init=False, repr=False)

    def __post_init__(self):
        self.graph = self.create_graph()

    @property
    def max_x(self) -> int:
        return max(node.x for node in self.nodes)

    @property
    def max_y(self) -> int:
        return max(node.y for node in self.nodes)

    @property
    def start(self) -> Node:
        return next(n for n in self.nodes if n.type == PointType.START)

    @property
    def locations(self) -> list[Node]:
        return [n for n in self.nodes if n.type == PointType.LOCATION]
    
    @property
    def closest_locations(self) -> list[Node]:
        return sorted(self.locations,
                      key=lambda n: self.get_distance_from_start(n))

    def create_graph(self) -> dict[Node, list[Node]]:
        output = {}
        for x in range(self.max_x+1):
            for y in range(self.max_y+1):
                node = self.get_node(x, y)
                potential_neighbors = [self.get_node(x+i, y+j) 
                                       for i, j in DIRECTIONS.values() 
                                       if x+i >= 0 and x+i <= self.max_x
                                       and y+j >= 0 and y+j <= self.max_y]
                neighbors = [n for n in potential_neighbors
                             if n.type != PointType.WALL]
                output[node] = neighbors
        return output

    def get_node(self, x: int, y: int) -> Node:
        return next(n for n in self.nodes if n.x == x and n.y == y)

    def get_distance_from_start(self, node: Node) -> int:
        return abs(node.x - self.start.x) + abs(node.y - self.start.y)

    def find_shortest_path(self, start_node: Node, end_node: Node) -> int:
        queue = deque([(start_node, [])])

        visited = set()
        visited.add(start_node)

        while queue:
            node, path = queue.popleft()
            if node == end_node:
                return len(path)
            neighbors = self.graph[node]
            for neighbor in neighbors:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
                    visited.add(neighbor)
        return -1

    def solve_part_one(self):
        path_lengths: list[int] = []
        with alive_bar(total=math.factorial(len(self.locations))) as bar:
            for combo in itertools.permutations(self.locations, len(self.locations)):
                locations = [self.start] + list(combo)

                path_length = 0
                for i in range(len(locations) - 1):
                    path_length += self.find_shortest_path(locations[i], locations[i+1])
                path_lengths.append(path_length)
                bar()
        return min(path_lengths)

    def solve_part_two(self):
        path_lengths: list[int] = []
        with alive_bar(total=math.factorial(len(self.locations))) as bar:
            for combo in itertools.permutations(self.locations, len(self.locations)):
                locations = [self.start] + list(combo) + [self.start]

                path_length = 0
                for i in range(len(locations) - 1):
                    path_length += self.find_shortest_path(locations[i], locations[i+1])
                path_lengths.append(path_length)
                bar()
        return min(path_lengths)

@functools.cache
def parse_data(data: str):
    line_list = data.splitlines()
    node_list = []
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            match char:
                case '#':
                    node_list.append(Node(x, y, PointType.WALL))
                case '.':
                    node_list.append(Node(x, y, PointType.OPEN))
                case '0':
                    node_list.append(Node(x, y, PointType.START))
                case _:
                    node_list.append(Node(x, y, PointType.LOCATION))
    return Grid(node_list)
    
def part_one(data: str):
    grid = parse_data(data)
    return grid.solve_part_one()

def part_two(data: str):
    grid = parse_data(data)
    return grid.solve_part_two()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()