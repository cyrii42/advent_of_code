import itertools
from pathlib import Path

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

def get_scanner_position(t: int, layer_range: int) -> int:
    cycle = ([n for n in range(layer_range-1)] + 
             [n for n in range(layer_range-1, 0, -1)])
    idx = t % len(cycle)
    return cycle[idx]

def simulate_run(layer_dict: dict[int, int], delay: int = 0) -> int:
    depth = 0
    max_depth = max(depth for depth in layer_dict.keys())

    total_severity = 0
    while depth <= max_depth:
        if depth not in layer_dict:
            depth += 1
            continue

        range_num = layer_dict[depth]
        scanner_position = get_scanner_position(depth+delay, range_num)
        if scanner_position == 0:
            # getting caught still counts for Part 2 even if the severity is zero
            if delay > 0:
                return 1
            
            total_severity += (depth * range_num)          
        depth += 1

    return total_severity

def parse_data(data: str) -> dict[int, int]:
    line_list = data.splitlines()
    output_dict = {}
    for line in line_list:
        depth, range = line.split(': ')
        output_dict[int(depth)] = int(range)
    return output_dict
    
def part_one(data: str):
    layer_dict = parse_data(data)
    return simulate_run(layer_dict)

def part_two(data: str):
    layer_dict = parse_data(data)
    for x in itertools.count(start=1):
        if simulate_run(layer_dict, delay=x) == 0:
            return x

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()