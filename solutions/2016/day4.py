import functools
import itertools
import json
import math
import operator
import os
import pathlib
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Literal, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.DATA_DIR / '2016.03_examples.txt'
INPUT = aoc.DATA_DIR / '2016.03_input.txt'

@dataclass
class RoomInfo:
    name: str
    id: int
    checksum: str
    is_real: bool = field(init=False)

    def __post_init__(self):
        self.is_real = self.confirm_checksum()

    def confirm_checksum(self) -> bool:
        ''' A room is real (not a decoy) if the checksum is the five most common
        letters in the encrypted name, in order, with ties broken by alphabetization. '''

        letters = sorted({char for char in self.name})
        letters = sorted(letters, key=lambda char: self.name.count(char), reverse=True)
        checksum = ''.join(char for char in letters[0:5])
        return checksum == self.checksum

    @classmethod
    def from_str(cls, line: str) -> Self:
        checksum = line[-6:].strip(']')
        id = int(''.join(char for char in line if char.isdigit()))
        name = ''.join(char for char in line[0:-7] if char.isalpha())
        return cls(name, id, checksum)

def parse_data(data_file: pathlib.Path) -> list[RoomInfo]:
    with open(data_file, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    return [RoomInfo.from_str(line) for line in line_list]
    
def part_one(data: pathlib.Path):
    room_list = parse_data(data)
    return sum(room.id for room in room_list if room.is_real)

def part_two(data: pathlib.Path):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()