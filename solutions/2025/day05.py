from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str) -> tuple[list[range], list[int]]:
    line_list = data.splitlines()
    range_strings = [line for line in line_list if '-' in line]
    range_list = []
    for s in range_strings:
        start, end = [int(x) for x in s.split('-')]
        range_list.append(range(start, end+1))  # provided ranges are inclusive
    id_list = [int(line) for line in line_list if line and '-' not in line]
    return (range_list, id_list)

def is_fresh(id: int, range_list: list[range]) -> bool:
    for r in range_list:
        if id in r:
            return True
    return False
    
def part_one(data: str):
    range_list, id_list = parse_data(data)
    return len([id for id in id_list if is_fresh(id, range_list)])

def merge_ranges(r1: range, r2: range) -> range:
    if not r1.start <= r2.start:
        raise ValueError
    start = r1.start
    stop = max(r1.stop, r2.stop)
    return range(start, stop)

def overlap(r1: range, r2: range) -> bool:
    return r2.start < r1.stop

def part_two(data: str):
    range_list, _ = parse_data(data)
    range_list = sorted(range_list, key=lambda r: r.start)
    output_list: list[range] = []
    output_list.append(range_list.pop(0))
    for r2 in range_list:
        r1 = output_list.pop()
        if overlap(r1, r2):
            merged_range = merge_ranges(r1, r2)
            output_list.append(merged_range)
        else:
            output_list += [r1, r2]
    return sum((r.stop - r.start) for r in output_list)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()