from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

class Direction(Enum):
    NORTH = '^'
    SOUTH = 'v'
    EAST = '>'
    WEST = '<'

@dataclass
class Santa:
    x: int = 0
    y: int = 0
    visited_points: set[tuple[int, int]] = field(default_factory=set)

    def __post_init__(self):
        self.visited_points.add((self.x, self.y))

    def move(self, direction: Direction):
        match direction:
            case Direction.NORTH:
                self.y += 1
            case Direction.SOUTH:
                self.y -= 1
            case Direction.EAST:
                self.x += 1
            case Direction.WEST:
                self.x -= 1
        self.visited_points.add((self.x, self.y))

def read_data(data: str) -> list[str]:
    line_list = [line.strip('\n') for line in data]
    return line_list
    
def part_one(data: str):
    direction_list = read_data(data)

    santa = Santa()

    for char in direction_list:
        santa.move(Direction(char))

    return len(santa.visited_points)

def part_two(data: str):
    direction_list = read_data(data)

    santa = Santa()
    robo_santa = Santa()

    for i, char in enumerate(direction_list):
        if i % 2 == 0:
            santa.move(Direction(char))
        else:
            robo_santa.move(Direction(char))

    all_visited_points = santa.visited_points | robo_santa.visited_points
    return len(all_visited_points)


def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (input):  {part_two(INPUT)}")

    # random_tests()

def random_tests():
    print(part_two('^v^v^v^v^v'))

       
if __name__ == '__main__':
    main()