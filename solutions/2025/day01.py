import operator
from enum import Enum
from pathlib import Path
from typing import NamedTuple
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class Direction(Enum):
    LEFT = 0
    RIGHT = 1

class Rotation(NamedTuple):
    direction: Direction
    num_clicks: int

def parse_data(data: str) -> list[Rotation]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        direction = Direction.LEFT if line[0] == 'L' else Direction.RIGHT
        num_clicks = int(line[1:])
        output_list.append(Rotation(direction, num_clicks))
    return output_list
    
def part_one(data: str):
    rotation_list = parse_data(data)
    dial = 50
    zero_counter = 0

    for rotation in rotation_list:
        fn = operator.add if rotation.direction == Direction.RIGHT else operator.sub
        dial = (fn(dial, rotation.num_clicks)) % 100
        if dial == 0:
            zero_counter += 1

    return zero_counter

def part_two(data: str):
    rotation_list = parse_data(data)
    dial = 50
    zero_counter = 0

    for rotation in rotation_list:
        fn = operator.add if rotation.direction == Direction.RIGHT else operator.sub
        count = 0

        while count < rotation.num_clicks:
            dial = (fn(dial, 1)) % 100
            if dial == 0:
                zero_counter += 1
            count += 1

    return zero_counter

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()