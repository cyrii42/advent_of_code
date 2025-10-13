from dataclasses import dataclass
from enum import Enum, IntEnum
from pathlib import Path
from typing import NamedTuple

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '''.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.'''
INPUT = aoc.get_input(YEAR, DAY)

class Direction(IntEnum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7

    @property
    def left(self) -> "Direction":
        return Direction((self.value - 1) % len(Direction))

    @property
    def right(self) -> "Direction":
        return Direction((self.value + 1) % len(Direction))

    @property
    def opposite(self) -> "Direction":
        num_dirs = len(Direction)
        return Direction((self.value + num_dirs // 2) % num_dirs)
    
DIRECTION_DELTAS = {
    Direction.NORTH: (0, -1),
    Direction.NORTHEAST: (1, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTHEAST: (1, 1),
    Direction.SOUTH: (0, 1),
    Direction.SOUTHWEST: (-1, 1),
    Direction.WEST: (-1, 0),
    Direction.NORTHWEST: (-1, -1)
}

class Point(NamedTuple):
    x: int
    y: int

class NodeType(Enum):
    OPEN = 0
    TREES = 1
    LUMBERYARD = 2

class AcreType(Enum):
    OPEN = 0
    TREES = 1
    LUMBERYARD = 2

@dataclass
class Node:
    position: Point
    node_type: NodeType

    def __repr__(self):
        return (f"{self.node_type.name} (x={self.position.x}, " +
                f"y={self.position.y})")

@dataclass
class CollectionArea:
    acre_dict: dict[Point, AcreType]

    @property
    def max_x(self) -> int:
        return max(pos.x for pos in self.acre_dict.keys())

    @property
    def max_y(self) -> int:
        return max(pos.y for pos in self.acre_dict.keys())

    @property
    def num_trees(self) -> int:
        return len([acre for acre, acre_type in self.acre_dict.items()
                    if acre_type == AcreType.TREES])

    @property
    def num_lumberyards(self) -> int:
        return len([acre for acre, acre_type in self.acre_dict.items()
                    if acre_type == AcreType.LUMBERYARD])

    def get_type(self, pos: Point) -> AcreType | None:
        return self.acre_dict.get(pos)

    def set_type(self, pos: Point, acre_type: AcreType) -> None:
        self.acre_dict[pos] = acre_type

    @staticmethod
    def get_position(pos: Point, direction: Direction):
        dx, dy = DIRECTION_DELTAS[direction]
        return Point(pos.x+dx, pos.y+dy)

    def tick(self):
        next_minute_dict = {}
        for pos in self.acre_dict:
            surrounding_types = self.get_surrounding_types(pos)
            num_trees = len([t for t in surrounding_types 
                            if t == AcreType.TREES])
            num_lumberyards = len([t for t in surrounding_types 
                                   if t == AcreType.LUMBERYARD])
            match self.acre_dict[pos]:
                case AcreType.OPEN:
                    if num_trees >= 3:
                        next_minute_dict[pos] = AcreType.TREES
                    else:
                        next_minute_dict[pos] = AcreType.OPEN
                case AcreType.TREES:
                    if num_lumberyards >= 3:
                        next_minute_dict[pos] = AcreType.LUMBERYARD
                    else:
                        next_minute_dict[pos] = AcreType.TREES
                case AcreType.LUMBERYARD:
                    if num_lumberyards >= 1 and num_trees >= 1:
                        next_minute_dict[pos] = AcreType.LUMBERYARD
                    else:
                        next_minute_dict[pos] = AcreType.OPEN
        self.acre_dict = next_minute_dict

    def run_simulation(self, num_minutes: int = 10):
        for _ in range(num_minutes):
            self.tick()
        return self.num_lumberyards * self.num_trees

    def get_surrounding_types(self, pos: Point) -> list[AcreType]:
        output_list = []
        for direction in Direction:
            acre_pos = self.get_position(pos, direction)
            acre_type = self.get_type(acre_pos)
            if acre_type:
                output_list.append(acre_type)
        return output_list

    def print_diagram(self):
        for y in range(0, self.max_y+1):
            row = ''
            for x in range(0, self.max_x+1):
                pos = Point(x, y)
                match self.acre_dict[pos]:
                    case AcreType.OPEN:
                        row += '.'
                    case AcreType.LUMBERYARD:
                        row += '#'
                    case AcreType.TREES:
                        row += '|'
                    case _:
                        row += "?"
            print(row)

def parse_data(data: str) -> dict[Point, AcreType]:
    line_list = data.splitlines()
    output_dict = {}
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            pos = Point(x, y)
            if char == ' ':
                continue
            elif char == '#':
                output_dict[pos] = AcreType.LUMBERYARD
            elif char == '.':
                output_dict[pos] = AcreType.OPEN
            elif char == '|':
                output_dict[pos] = AcreType.TREES
            else:
                raise ValueError
    return output_dict
    
def part_one(data: str):
    acre_dict = parse_data(data)
    collection_area = CollectionArea(acre_dict)
    return collection_area.run_simulation()

def part_two(data: str):
    acre_dict = parse_data(data)
    collection_area = CollectionArea(acre_dict)

    answers = set()
    cycle_steps = []
    for i in range(0, 10_000):
        collection_area.tick()
        answer = collection_area.num_lumberyards * collection_area.num_trees
        if answer in answers:
            if i >= 525 and i < 580:
                cycle_steps.append(answer)
            if i > 580:
                break
            # if i > 1000:
            #     print(answer)
            #     print(cycle_steps[(i - 515) % 27])
            #     print()
            # if i > 1020:
            #     break
        answers.add(answer)

    return cycle_steps[(1_000_000_000 - 515) % 27]

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()