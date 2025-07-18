'''--- Day 2: Dive! ---'''

import math
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from operator import add, mul
from pathlib import Path
from typing import Literal, NamedTuple, Optional, Self

from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2021_day2_example.txt'
INPUT = DATA_DIR / '2021_day2_input.txt'

@dataclass
class Submarine:
    position: int = 0
    depth: int = 0
    aim: int = 0

    def move_part_one(self, move_str: str) -> None:
        direction, num_str = move_str.split(' ')
        num = int(num_str)
        match direction:
            case 'up':
                self.depth -= num
            case 'down':
                self.depth += num
            case 'forward':
                self.position += num

    def move_part_two(self, move_str: str) -> None:
        direction, num_str = move_str.split(' ')
        num = int(num_str)
        match direction:
            case 'up':
                self.aim -= num
            case 'down':
                self.aim += num
            case 'forward':
                self.position += num
                self.depth += (self.aim * num)

    def get_answer(self):
        return self.position * self.depth

def ingest_data(filename: Path):
    with open(filename) as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    return line_list

def part_one(filename: Path):
    line_list = ingest_data(filename)
    sub = Submarine()
    for line in line_list:
        sub.move_part_one(line)
    return sub.get_answer()

def part_two(filename: Path):
    line_list = ingest_data(filename)
    sub = Submarine()
    for line in line_list:
        sub.move_part_two(line)
    return sub.get_answer()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 150
    print(f"Part One (input):  {part_one(INPUT)}") # 
    
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # 900
    print(f"Part Two (input):  {part_two(INPUT)}") # 

    random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()