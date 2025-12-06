import functools
import math
from pathlib import Path
from typing import Callable, NamedTuple
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

TESTS_PART_ONE = [
    (aoc.DATA_DIR / '2019.10_example1.txt', 33),
    (aoc.DATA_DIR / '2019.10_example2.txt', 35),
    (aoc.DATA_DIR / '2019.10_example3.txt', 41),
    (aoc.DATA_DIR / '2019.10_example4.txt', 210),
]
TESTS_PART_TWO = [(aoc.DATA_DIR / '2019.10_example4.txt', 802)]

type NodeDict = dict[tuple[int, int], Node]
type NodeGraph = dict[Node, list[Node]]

class Node(NamedTuple):
    x: int
    y: int

class Asteroid(Node):
    pass

def create_node_dict(data: str) -> NodeDict:
    line_list = data.splitlines()
    node_list: list[Node] = []
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            if char == '#':
                node_list.append(Asteroid(x, y))
            else:
                node_list.append(Node(x, y))
    node_dict = {(node.x, node.y): node for node in node_list}
    return node_dict

def get_slope(node1: Node, node2: Node) -> float:
    x1, y1 = node1
    x2, y2 = node2
    rise = y2 - y1
    run = x2 - x1
    try:
        return rise / run
    except ZeroDivisionError:
        return float('nan')

def get_atan2(node1: Node, node2: Node) -> float:
    x1, y1 = node1
    x2, y2 = node2
    rise = y2 - y1
    run = x2 - x1
    return math.atan2(rise, run)

def test_slope_and_atan2(asteroids: list[Node]):
    test = asteroids[5]
    print(test)
    for a in asteroids:
        if a == test:
            continue
        print(f"Asteroid {a.x},{a.y}: {get_atan2(test, a)} {get_slope(test, a)}")

def get_angles(a1: Node, a_list: list[Asteroid]) -> set[float]:
    return {get_atan2(a1, a2) for a2 in a_list if a1 != a2}

def get_angles_dict(a1: Node, a_list: list[Asteroid]
                    ) -> dict[float, list[Asteroid]]:
    angles = get_angles(a1, a_list)
    return {angle: [a2 for a2 in a_list if get_atan2(a1, a2) == angle]
            for angle in angles}

def find_monitoring_station(a_list: list[Asteroid]) -> tuple[Node, int]:
    a_dict = {a1: len(get_angles(a1, a_list)) for a1 in a_list}
    num = max(a_dict.values())
    station = [a for a, n in a_dict.items() if n == num][0]
    return (station, num)

def part_one(data: str):
    node_dict = create_node_dict(data)
    a_list = [n for n in node_dict.values() if isinstance(n, Asteroid)]
    _, num = find_monitoring_station(a_list)
    return num

def manhattan_distance(n1: Node, n2: Node) -> int:
    return abs(n1.x - n2.x) + abs(n1.y - n2.y)

def part_two(data: str):
    UP = 0 - (math.pi / 2)
    node_dict = create_node_dict(data)
    a_list = [n for n in node_dict.values() if isinstance(n, Asteroid)]
    station, _ = find_monitoring_station(a_list)
    angles_dict = get_angles_dict(station, a_list)
    angles = sorted([angle for angle in angles_dict.keys()])
    assert UP in angles
    i = angles.index(UP)

    distance_from_station = functools.partial(manhattan_distance, station)

    count = 0
    while True:
        angle = angles[i]
        asteroids = angles_dict[angle]
        if len(asteroids) > 1:
            asteroids = sorted(asteroids, key=lambda n: distance_from_station(n))
        if len(asteroids) > 0:
            asteroid_to_vaporize = asteroids[0]
            angles_dict[angle].remove(asteroid_to_vaporize)
            count += 1
            if count == 200:
                return (asteroid_to_vaporize.x * 100) + asteroid_to_vaporize.y
        i = (i + 1) % len(angles)

def run_tests(tests: list[tuple[Path, int]], fn: Callable):
    for i, example in enumerate(tests, start=1):
        filepath, answer = example
        with open(filepath, 'r') as f:
            data = f.read()
        test_answer = fn(data)
        print(f"Test #{i}: {test_answer == answer}",
              f"({test_answer})")

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    run_tests(TESTS_PART_ONE, part_one)
    print(f"Part One (input):  {part_one(INPUT)}")
    run_tests(TESTS_PART_TWO, part_two)
    print(f"Part Two (input):  {part_two(INPUT)}")
   
if __name__ == '__main__':
    main()