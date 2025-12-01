import itertools
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)
    
def part_one(data: str):
    entry_list = [int(x) for x in data.splitlines()]
    for x, y in itertools.product(entry_list, repeat=2):
        if x + y == 2020:
            return x * y

def part_two(data: str):
    entry_list = [int(x) for x in data.splitlines()]
    for x, y, z in itertools.product(entry_list, repeat=3):
        if x + y + z == 2020:
            return x * y * z

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()