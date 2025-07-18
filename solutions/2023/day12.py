'''--- Day 12: Hot Springs ---'''

import re
from pathlib import Path

DATA_DIR = Path("/home/zvaughan/python/advent_of_code_2023/inputs")
EXAMPLE = DATA_DIR / 'day12_example.txt'
INPUT = DATA_DIR / 'day12_input.txt'

OPERATIONAL_PATTERN = r"\.+"
DAMAGED_PATTERN = r"\#+"
UNKNOWN_PATTERN = r"\?+"
REGEX_PART_ONE = OPERATIONAL_PATTERN + '|' + DAMAGED_PATTERN + '|' + UNKNOWN_PATTERN

def ingest_data(filename: Path) -> list[tuple[str, str]]:
    with open(filename, 'r') as f:
        pair_list = [(pair[0], pair[1]) for pair in [x.split() for x in f.readlines()]]
    return pair_list

def count_possibilities(pair: tuple[str, str]) -> int:  
    criteria = [int(x) for x in pair[1].split(',')]
    num_groups = len(criteria)

    springs = pair[0]
    pattern = re.compile(REGEX_PART_ONE)
    spring_groups = pattern.finditer(springs)

    total = 0
    for group in spring_groups:
        text = group.group(0)

        match text:
            case ".":
                print(f'operational: {len(text)}')
            case "#":
                print(f'damaged: {len(text)}')
            case _:
                print(f'unknown: {len(text)}')

    return total
    
    

def part_one(filename: Path) -> int:
    pair_list = ingest_data(filename)

    print(pair_list[0])
    count_possibilities(pair_list[0])
    
    # answer = sum(count_possibilities(pair) for pair in pair_list)
    # return answer

def part_two(filename: Path) -> int:
    ...


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")


if __name__ == '__main__':
    main()