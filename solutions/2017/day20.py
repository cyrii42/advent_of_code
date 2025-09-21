import functools
import itertools
import operator
import hashlib
import json
import math
import os
import re
from pathlib import Path
from collections import deque, defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, NamedTuple, Optional, Protocol, Self, Literal, Generator

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it, alive_bar
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class Point(NamedTuple):
    x: int
    y: int
    z: int

@dataclass
class Particle:
    position: Point
    velocity: Point
    acceleration: Point

    @property
    def distance_from_origin(self) -> int:
        ''' the sum of the absolute values of a particle's X, Y, and Z position '''
        x, y, z = self.position
        return sum([abs(x), abs(y), abs(z)])

    def get_position(self, t: int) -> Point:
        ...

    def get_velocity(self, t: int) -> Point:
        ...
    

def parse_data(data: str):
    line_list = data.splitlines()
    
def part_one(data: str):
    __ = parse_data(data)

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()