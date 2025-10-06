import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
import sys
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, NamedTuple, Optional, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_bar, alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

@dataclass
class Position:
    ''' x is horizontal; y is vertical '''
    x: int
    y: int
    vx: int
    vy: int

    def increment(self) -> None:
        self.x += self.vx
        self.y += self.vy

@dataclass
class LightGroup:
    lights: list[Position]

    @property
    def min_max(self) -> tuple[int, int, int, int]:
        ''' Returns: (min_x, min_y, max_x, max_y) '''
        min_x = min(light.x for light in self.lights)
        min_y = min(light.y for light in self.lights)
        max_x = max(light.x for light in self.lights)
        max_y = max(light.y for light in self.lights)

        return (min_x, min_y, max_x, max_y)

    def print_grid(self) -> None:
        ...

def parse_data(data: str):
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        line = line.replace('position=', '').replace('velocity=', '')
        line = line.replace('<', '').replace('>', '').replace(',', '')
        x, y, vx, vy = [int(num) for num in line.split(' ') if num]
        output_list.append(Position(x, y, vx, vy))
    return LightGroup(output_list)
    
def part_one(data: str):
    light_group = parse_data(data)
    print(light_group.min_max)
    

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()