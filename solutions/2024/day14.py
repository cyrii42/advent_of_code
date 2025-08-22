'''--- Day 14: Restroom Redoubt ---'''

import math
from pathlib import Path
from rich import print
from pprint import pprint
from copy import deepcopy
from typing import NamedTuple, Protocol, Optional
from enum import Enum, IntEnum
from dataclasses import dataclass, field
from string import ascii_letters
import itertools
import functools
import pandas as pd
import numpy as np
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2024_day14_example.txt'
INPUT = DATA_DIR / '2024_day14_input.txt'

SPACE_WIDTH = 101
SPACE_HEIGHT = 103

@dataclass
class Robot():
    px: int
    py: int
    vx: int
    vy: int

    @property
    def quadrant(self) -> int:
        midpoint_x = SPACE_WIDTH // 2
        midpoint_y = SPACE_HEIGHT // 2
        if self.px < midpoint_x and self.py < midpoint_y:
            return 1
        if self.px > midpoint_x and self.py < midpoint_y:
            return 2
        if self.px < midpoint_x and self.py > midpoint_y:
            return 3
        if self.px > midpoint_x and self.py > midpoint_y:
            return 4
        return 0

    def move(self, moves: int) -> None:
        for _ in range(moves):
            self.px = (self.px + self.vx) % SPACE_WIDTH
            self.py = (self.py + self.vy) % SPACE_HEIGHT
        

def ingest_data(filename: Path) -> list[Robot]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    return [process_robot_data(data) for data in line_list]

def process_robot_data(data: str) -> Robot:
    position_str = data.split(' ')[0].removeprefix('p=')
    position_ints = [int(x) for x in position_str.split(',')]
        
    velocity_str = data.split(' ')[1].removeprefix('v=')
    velocity_ints = [int(x) for x in velocity_str.split(',')]

    return Robot(position_ints[0], position_ints[1], velocity_ints[0], velocity_ints[1])

def determine_safety_factor(robot_list: list[Robot]) -> int:
    quadrant_1 = len([robot for robot in robot_list if robot.quadrant == 1])
    quadrant_2 = len([robot for robot in robot_list if robot.quadrant == 2])
    quadrant_3 = len([robot for robot in robot_list if robot.quadrant == 3])
    quadrant_4 = len([robot for robot in robot_list if robot.quadrant == 4])

    return quadrant_1 * quadrant_2 * quadrant_3 * quadrant_4

def find_christmas_tree(robot_list: list[Robot]) -> int:
    ...
        

def part_one(filename: Path):
    robot_list = ingest_data(filename)
    for robot in robot_list:
        robot.move(100)
    return determine_safety_factor(robot_list)
    


def part_two(filename: Path):
    ...


def main():
    # print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    # random_tests()



def random_tests():
    print(101 // 2)


       


if __name__ == '__main__':
    main()