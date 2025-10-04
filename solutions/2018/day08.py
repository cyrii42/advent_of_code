import sys
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
INPUT = aoc.get_input(YEAR, DAY)

sys.setrecursionlimit(10**6)

def get_metadata_total(data: list[int]):
    ''' https://dev.to/steadbytes/aoc-2018-day-8-memory-maneuver-34jf '''
    n_children, n_metadata = data[0:2]
    remaining = data[2:]

    total = 0
    
    # if there aren't any children, this loop doesn't happen
    for _ in range(n_children):
        child_total, remaining = get_metadata_total(remaining)
        total += child_total

    current_node_metadata = remaining[0:n_metadata]
    current_node_total = sum(current_node_metadata)

    total += current_node_total

    return total, remaining[n_metadata:]  

def solve_part_two(data: list[int]):
    n_children, n_metadata = data[0:2]
    remaining = data[2:]

    total = 0

    if n_children == 0:
        current_node_metadata = remaining[0:n_metadata]
        current_node_total = sum(current_node_metadata)
        total += current_node_total
    else:
        children = []
        for _ in range(n_children):
            value, remaining = solve_part_two(remaining)
            children.append(value)
        current_node_metadata = remaining[0:n_metadata]
        for i in current_node_metadata:
            try:
                total += children[i-1]  # metadata isn't zero-indexed
            except IndexError:
                continue

    return total, remaining[n_metadata:]  
    
def part_one(data: str):
    node_data = [int(x) for x in data.split(' ')]
    total, _ = get_metadata_total(node_data)
    return total

def part_two(data: str):
    node_data = [int(x) for x in data.split(' ')]
    total, _ = solve_part_two(node_data)
    return total

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()