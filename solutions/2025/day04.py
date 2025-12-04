from enum import Enum, IntEnum
from pathlib import Path
from typing import NamedTuple
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class Direction(IntEnum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7

# ROW, COL
DIRECTION_DELTAS = {
    Direction.NORTH: (-1, 0),
    Direction.NORTHEAST: (-1, 1),
    Direction.EAST: (0, 1),
    Direction.SOUTHEAST: (1, 1),
    Direction.SOUTH: (1, 0),
    Direction.SOUTHWEST: (1, -1),
    Direction.WEST: (0, -1),
    Direction.NORTHWEST: (-1, -1)
}

class NodeType(Enum):
    OPEN = 0
    PAPER = 1

class Node(NamedTuple):
    row: int
    col: int
    node_type: NodeType

def parse_data(data: str) -> dict[tuple[int, int], Node]:
    line_list = data.splitlines()
    node_list: list[Node] = []
    for row, line in enumerate(line_list):
        for col, char in enumerate(line):
            node_type = NodeType.PAPER if char == '@' else NodeType.OPEN
            node_list.append(Node(row, col, node_type))
    node_dict = {(node.row, node.col): node for node in node_list}
    return node_dict
        
def get_node_neighbor_coordinates(node: Node) -> list[tuple[int, int]]:
    row, col = (node.row, node.col)

    output_list = []
    for dir in Direction:
        delta_row, delta_col = DIRECTION_DELTAS[dir]
        output_list.append((row + delta_row, col + delta_col))
    return output_list

def create_graph(node_dict: dict[tuple[int, int], Node]) -> dict[Node, list[Node]]:
    output_dict: dict[Node, list[Node]] = {}
    
    for node in node_dict.values():
        neighbor_list = []
        for neighbor_coords in get_node_neighbor_coordinates(node):
            try:
                neighbor_list.append(node_dict[neighbor_coords])
            except KeyError:
                continue
        output_dict[node] = neighbor_list
        
    return output_dict

def find_accessible_paper_rolls(node_dict: dict[tuple[int, int], Node]) -> list[Node]:
    graph = create_graph(node_dict)
    return [node for node in graph if node.node_type == NodeType.PAPER
            and len([n for n in graph[node] if n.node_type == NodeType.PAPER]) < 4]

def part_one(data: str):
    node_dict = parse_data(data)
    accessible_paper_rolls = find_accessible_paper_rolls(node_dict)
    return len(accessible_paper_rolls)

def part_two(data: str):
    node_dict = parse_data(data)

    rolls_removed = 0
    while True:
        accessible_paper_rolls = find_accessible_paper_rolls(node_dict)
        if len(accessible_paper_rolls) == 0:
            return rolls_removed

        new_empty_nodes = [Node(node.row, node.col, NodeType.OPEN) 
                           for node in accessible_paper_rolls]
        for node in new_empty_nodes:
            node_dict[(node.row, node.col)] = node
            rolls_removed += 1

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()