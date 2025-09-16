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

TESTS_PART_ONE = [
    ('ne,ne,ne', 3),
    ('ne,ne,sw,sw', 0),
    ('ne,ne,s,s', 2),
    ('se,sw,se,sw,sw', 3),
]

class HexDirection(Enum):
    NORTH = 'N'
    NORTHEAST = 'NE'
    SOUTHEAST = 'SE'
    SOUTH = 'S'
    SOUTHWEST = 'SW'
    NORTHWEST = 'NW'

class HexCoordinate(NamedTuple):
    q: int
    r: int
    s: int

def execute_instruction(current_position: HexCoordinate,
                        direction: HexDirection,
                        num_steps: int = 1
                        ) -> HexCoordinate:
    ''' https://www.redblobgames.com/grids/hexagons/#neighbors-cube '''
    
    q, r, s = current_position
    match direction:
        case HexDirection.NORTH:
            return HexCoordinate(q, r-num_steps, s+num_steps)
        case HexDirection.NORTHEAST:
            return HexCoordinate(q+num_steps, r-num_steps, s)
        case HexDirection.SOUTHEAST:
            return HexCoordinate(q+num_steps, r, s-num_steps)
        case HexDirection.SOUTH:
            return HexCoordinate(q, r+num_steps, s-num_steps)
        case HexDirection.SOUTHWEST:
            return HexCoordinate(q-num_steps, r+num_steps, s)
        case HexDirection.NORTHWEST:
            return HexCoordinate(q-num_steps, r, s+num_steps)
  
def model_path(start: HexCoordinate, 
               directions: list[HexDirection], 
               part_two: bool = False
               ) -> int:
    distance = 0
    furthest_distance = 0
    current_position = start

    for dir in directions:
        current_position = execute_instruction(current_position, dir)
        distance = max(point for point in current_position)
        furthest_distance = max(distance, furthest_distance)

    if part_two:
        return furthest_distance
    else:
        return distance

def parse_data(data: str) -> list[HexDirection]:
    return [HexDirection(s.upper()) for s in data.split(',')]

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        data, answer = example
        test_answer = part_one(data)
        print(f"Test #{i} ({data}) ({test_answer}): {test_answer == answer}")

def part_one(data: str):
    directions = parse_data(data)
    start = HexCoordinate(0, 0, 0)
    return model_path(start, directions)

def part_two(data: str):
    directions = parse_data(data)
    start = HexCoordinate(0, 0, 0)
    return model_path(start, directions, part_two=True)

def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()