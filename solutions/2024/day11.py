'''--- Day 11: Plutonian Pebbles ---'''

from pathlib import Path
from rich import print
from pprint import pprint
from copy import deepcopy
from typing import NamedTuple, Protocol, Optional
from enum import Enum
from dataclasses import dataclass, field
from string import ascii_letters
import itertools
import functools
import pandas as pd
import numpy as np
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2024_day11_example.txt'
INPUT = DATA_DIR / '2024_day11_input.txt'

def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        return f.read().split()

class Stone():
    def __init__(self, num: str | int):
        if isinstance(num, str):
            self.num_str = num
            self.num_int = int(num)
        elif isinstance(num, int):
            self.num_str = str(num)
            self.num_int = num

    def __repr__(self):
        return f"{self.num_str}"

@dataclass
class StoneLine():
    stones: list[Stone]
    stone_dict: dict[int, int] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        self.create_stone_dict()

    def create_stone_dict(self):
        for stone in self.stones:
            if stone.num_int in self.stone_dict.keys():
                self.stone_dict[stone.num_int] += 1
            else:
                self.stone_dict[stone.num_int] = 1

    def blink(self) -> None:
        new_dict: dict[int, int] = {}
        for num_int, num_occurrences in self.stone_dict.items():
            new_stones = transform_stone(Stone(num_int))
            for new_stone in new_stones:
                if new_stone.num_int in new_dict.keys():
                    new_dict[new_stone.num_int] += num_occurrences
                else:
                    new_dict[new_stone.num_int] = num_occurrences
        self.stone_dict = new_dict


    def __repr__(self):
        return f"{self.stones}"


def transform_stone(stone: Stone) -> list[Stone]:   
    if stone.num_int == 0:
        return [Stone(1)]

    if len(stone.num_str) % 2 == 0:
        middle_idx = len(stone.num_str) // 2
        int1 = int(stone.num_str[0:middle_idx])
        int2 = int(stone.num_str[middle_idx:])
        return [Stone(int1), Stone(int2)]

    else:
        new_int = stone.num_int * 2024
        return [Stone(new_int)]



def part_one(filename: Path):
    str_list = ingest_data(filename)
    stone_list = [Stone(stone_str) for stone_str in str_list]
    stone_line = StoneLine(stone_list)
    for _ in alive_it(range(25)):
        stone_line.blink()
    return sum(stone_line.stone_dict.values())


def part_two(filename: Path):
    str_list = ingest_data(filename)
    stone_list = [Stone(stone_str) for stone_str in str_list]
    stone_line = StoneLine(stone_list)
    for _ in alive_it(range(75)):
        stone_line.blink()
    return sum(stone_line.stone_dict.values())


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")




       


if __name__ == '__main__':
    main()