from enum import Enum
from pathlib import Path
from typing import NamedTuple, Optional
from day10 import part_two as create_knot_hash
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = 'flqrgnkx'
INPUT = aoc.get_input(YEAR, DAY)

TOTAL_ROWS = 128
TOTAL_COLS = 128

class Point(NamedTuple):
    row: int
    col: int
    used: bool = False

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

DIRECTION_DELTAS = {
    Direction.NORTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, -1),
    Direction.WEST: (-1, 0),
}

def convert_hash_to_bits(hash_output: str) -> str:
    return ''.join(f"{bin(int(char, base=16)).removeprefix('0b'):0>4}"
                   for char in hash_output)

def create_grid(data: str) -> list[str]:
    hash_inputs = [f"{data}-{row_num}" for row_num in range(TOTAL_ROWS)]
    hash_outputs = [create_knot_hash(x) for x in hash_inputs]
    return [convert_hash_to_bits(h) for h in hash_outputs]
   
def part_one(data: str):
    grid = create_grid(data)
    return sum(len([char for char in row if char == '1']) for row in grid)

def create_point_list(grid: list[str]) -> list[Point]:
    output_list = []
    for row_num, row in enumerate(grid):
        for col_num, char in enumerate(row):
            if char == '1':
                output_list.append(Point(row_num, col_num, True))
    return output_list

def validate_coordinates(row: int, col: int) -> bool:
    return row >= 0 and row < TOTAL_ROWS and col >= 0 and col < TOTAL_COLS

def get_point_neighbor_coordinates(point: Point) -> list[tuple[int, int]]:
    row, col, _ = point

    output_list = []
    for dir in Direction:
        delta_row, delta_col = DIRECTION_DELTAS[dir]
        new_row = row + delta_row
        new_col = col + delta_col
        if validate_coordinates(new_row, new_col):
            output_list.append((new_row, new_col))
    return output_list

def create_graph(point_list: list[Point]) -> dict[Point, list[Point]]:
    output_dict: dict[Point, list[Point]] = {}
    
    for point in point_list:
        neighbor_list = []
        for row, col in get_point_neighbor_coordinates(point):
            try:
                neighbor_list.append(
                    next(p for p in point_list 
                        if p.row == row and p.col == col and p.used))
            except StopIteration:
                continue
        output_dict[point] = neighbor_list
        
    return output_dict

def find_reachable_nodes(graph: dict[Point, list[Point]], 
                         parent: Point,
                         visited: Optional[set[Point]] = None) -> set[Point]:   
    if visited is None:
        visited = set()
        
    visited.add(parent)
    for child in graph[parent]:
        if child not in visited:
            find_reachable_nodes(graph, child, visited)
            
    return visited

def count_groups(graph: dict[Point, list[Point]]) -> int:
    visited = set()
    num_groups = 0
    for node in graph.keys():
        if node not in visited:
            reachable_nodes = find_reachable_nodes(graph, node)
            visited.update(reachable_nodes)
            num_groups += 1
    return num_groups

def part_two(data: str):
    grid = create_grid(data)
    point_list = create_point_list(grid)
    graph = create_graph(point_list)
    return count_groups(graph)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()