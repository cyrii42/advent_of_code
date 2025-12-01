from pathlib import Path
from typing import Callable, NamedTuple, Any

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

TESTS_PART_ONE = [
    ('R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83', 159),
    ('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7', 135)
]
TESTS_PART_TWO = [
    ('R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83', 610),
    ('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7', 410)
]
INPUT = aoc.get_input(YEAR, DAY)

DIRECTION_DELTAS = {
    'U': (0, -1),
    'R': (1, 0),
    'D': (0, 1),
    'L': (-1, 0),
}

class WireTurn(NamedTuple):
    direction: str
    distance: int

class Point(NamedTuple):
    x: int
    y: int

    @property
    def distance_from_origin(self) -> int:
        return abs(self.x) + abs(self.y)

def parse_path(path: str) -> list[WireTurn]:
    return [WireTurn(turn[0], int(turn[1:])) for turn in path.split(',')]

def get_full_path(path: list[WireTurn]) -> list[Point]:
    current_pos = Point(0, 0)
    output_list = []
   
    for turn in path:
        dx, dy = DIRECTION_DELTAS[turn.direction]
        for _ in range(turn.distance):
            new_pos = Point(current_pos.x + dx, current_pos.y + dy)
            output_list.append(new_pos)
            current_pos = new_pos

    return output_list

def part_one(data: str):
    path1, path2 = (parse_path(path) for path in data.splitlines())
    full_path1 = get_full_path(path1)
    full_path2 = get_full_path(path2)

    overlapping_points = set(full_path1) & set(full_path2)
    overlapping_points_sorted = sorted(overlapping_points, 
                                       key=lambda p: p.distance_from_origin)

    return overlapping_points_sorted[0].distance_from_origin

def part_two(data: str):
    path1, path2 = (parse_path(path) for path in data.splitlines())
    full_path1 = get_full_path(path1)
    full_path2 = get_full_path(path2)

    overlapping_points = set(full_path1) & set(full_path2)
    signal_delay_list = [full_path1.index(p) + 1    # adding one for origin
                         + full_path2.index(p) + 1  # adding one for origin
                         for p in overlapping_points]
    return min(signal_delay_list)

def run_tests(tests: list[tuple[str, Any]], fn: Callable):
    for i, example in enumerate(tests, start=1):
        data, answer = example
        test_answer = fn(data)
        print(f"Test #{i}: {test_answer == answer}",
              f"({test_answer})")

def main():
    run_tests(TESTS_PART_ONE, part_one)
    print(f"Part One (input):  {part_one(INPUT)}")
    run_tests(TESTS_PART_TWO, part_two)
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()