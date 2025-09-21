import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

sys.setrecursionlimit(10**6)

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
        case _:
            raise ValueError

def walk_path(graph: dict[Node, list[Node]],
              node: Node,
              dir: Direction = Direction.SOUTH,
              visited: Optional[list[tuple[Node, Direction]]] = None
              ) -> tuple[str, int]:
    if not visited:
        visited = []

    visited.append((node, dir))

    if node.node_type == NodeType.CORNER:
        next_node = next(n for n in graph[node] if (n, dir) not in visited)
        next_dir = determine_next_direction(node, next_node)
        walk_path(graph, next_node, next_dir, visited)

    else:
        x, y = (node.x, node.y)
        delta_x, delta_y = DIRECTION_DELTAS[dir]
        next_x = x + delta_x
        next_y = y + delta_y
        try:
            next_node = next(n for n in graph[node] 
                             if n.x == next_x and n.y == next_y)    
            walk_path(graph, next_node, dir, visited) 
        except StopIteration:
            pass

    return (''.join(node.char for node, _ in visited if node.char.isalpha()),
            len(visited))

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
    
def solve(data: str):
    node_list = parse_data(data)
    graph = create_graph(node_list)
    start = find_start(node_list)
    p1_answer, p2_answer = walk_path(graph, start)
    print(f"Part One:  {p1_answer}")
    print(f"Part Two:  {p2_answer}")

def main():
    print("EXAMPLE:")
    solve(EXAMPLE)
    
    print("\nINPUT:")
    solve(INPUT)

if __name__ == '__main__':
    main()