import math
from pathlib import Path
from typing import Callable

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY).replace('\n', '')
INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str) -> list[tuple[int, int]]:
    pairs = [pair.split('-') for pair in data.split(',')]
    return [(int(pair[0]), int(pair[1])) for pair in pairs]

def validate_id_part_one(id: int) -> bool:
    id_str = str(id)

    if len(id_str) % 2 != 0:
        return True

    midpoint = len(id_str) // 2
    if id_str[:midpoint] == id_str[midpoint:]:
        return False

    return True

def validate_id_part_two(id: int) -> bool:
    id_str = str(id)
    
    for i in range(1, (math.ceil(len(id_str) / 2) + 1)):
        substring = id_str[0:i]
        count = id_str.count(substring)
        if (count > 1 and count == math.ceil(len(id_str) / len(substring))):
            return False

    return True

def get_answer(data: str, validation_fn: Callable[[int], bool]):
    pairs = parse_data(data)

    invalid_id_list = []
    for pair in pairs:
        start, end = pair
        for id in range(start, end+1):
            if not validation_fn(id):
                invalid_id_list.append(id)
    return sum(invalid_id_list)

def part_one(data: str):
    return get_answer(data, validate_id_part_one)

def part_two(data: str):
    return get_answer(data, validate_id_part_two)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()