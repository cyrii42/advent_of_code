'''--- Day 13: Claw Contraption ---'''

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

EXAMPLE = DATA_DIR / 'day13_example.txt'
INPUT = DATA_DIR / 'day13_input.txt'

MAX_BUTTON_PRESSES = 100

class Coordinate(NamedTuple):
    x: int
    y: int

@dataclass
class Machine():
    button_a: Coordinate
    button_b: Coordinate
    prize_location: Coordinate

    def find_prize_combo_part_one(self) -> int:
        ax = self.button_a.x
        ay = self.button_a.y
        bx = self.button_b.x
        by = self.button_b.y
        px = self.prize_location.x
        py = self.prize_location.y
        
        if (ax * MAX_BUTTON_PRESSES) + (bx * MAX_BUTTON_PRESSES) < px:
            return 0
        if (ay * MAX_BUTTON_PRESSES) + (by * MAX_BUTTON_PRESSES) < py:
            return 0

        for i in range(101):
            for j in range(101):
                if ax*i + bx*j == px and ay*i + by*j == py:
                    return i*3 + j

        return 0

    def find_prize_combo_part_two(self) -> int:
        ax = self.button_a.x
        ay = self.button_a.y
        bx = self.button_b.x
        by = self.button_b.y
        px = self.prize_location.x + 10_000_000_000_000
        py = self.prize_location.y + 10_000_000_000_000

        ...

def ingest_data(filename: Path) -> list[Machine]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        line_list = [line for line in line_list if line != '']

    data_list = []
    for x in range(0, len(line_list), 3):
        machine_data = line_list[x:x+3]
        data_list.append(machine_data)

    return [process_machine_data(data) for data in data_list]

def process_machine_data(data: list[str]) -> Machine:
    line_1 = data[0].removeprefix('Button A: ').replace(' ', '').replace('X+', '').replace('Y+', '').split(',')
    button_a = Coordinate(int(line_1[0]), int(line_1[1]))

    line_2 = data[1].removeprefix('Button B: ').replace(' ', '').replace('X+', '').replace('Y+', '').split(',')
    button_b = Coordinate(int(line_2[0]), int(line_2[1]))

    line_3 = data[2].removeprefix('Prize: ').replace(' ', '').replace('X=', '').replace('Y=', '').split(',')
    prize_location = Coordinate(int(line_3[0]), int(line_3[1]))

    return Machine(button_a, button_b, prize_location)
        

def part_one(filename: Path):
    machine_list = ingest_data(filename)
    return sum(machine.find_prize_combo_part_one() for machine in machine_list)


def part_two(filename: Path):
    machine_list = ingest_data(filename)
    return sum(machine.find_prize_combo_part_two() for machine in machine_list)


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    # random_tests()



def random_tests():
    ...


       


if __name__ == '__main__':
    main()