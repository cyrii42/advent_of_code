from pathlib import Path
from typing import Optional

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str) -> dict[int, list[int]]:
    line_list = data.splitlines()
    graph = {}
    for line in line_list:
        parts = line.replace(',', '').split(' ')
        id = int(parts[0])
        neighbors = [int(neighbor) for neighbor in parts[1:] if neighbor.isdigit()]
        graph[id] = neighbors
    return graph

def find_reachable_nodes(graph: dict[int, list[int]], 
                         parent: int = 0,
                         visited: Optional[set[int]] = None) -> set[int]:   
    if visited is None:
        visited = set()
        
    visited.add(parent)
    for child in graph[parent]:
        if child not in visited:
            find_reachable_nodes(graph, child, visited)
            
    return visited

def count_groups(graph: dict[int, list[int]]) -> int:
    visited = set()
    num_groups = 0
    for node in graph.keys():
        if node not in visited:
            reachable_nodes = find_reachable_nodes(graph, node)
            visited.update(reachable_nodes)
            num_groups += 1
    return num_groups
    
def part_one(data: str):
    graph = parse_data(data)
    return len(find_reachable_nodes(graph))

def part_two(data: str):
    graph = parse_data(data)
    return count_groups(graph)
    
def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()