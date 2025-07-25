import functools
import itertools
import json
import math
import os
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from pprint import pprint
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

class InvalidPair(Exception):
    pass

class Pair(NamedTuple):
    guest: str
    neighbor: str
    value: int

@dataclass
class PairSet:
    pairs: list[Pair]

    def __post_init__(self):
        self.all_guests = {f.guest for f in self.pairs} | {f.neighbor for f in self.pairs}

    @property
    def num_seats(self) -> int:
        return len(self.all_guests)

    def add_me(self) -> None:
        for guest in self.all_guests:
            self.pairs.append(Pair('ME', guest, 0))
            self.pairs.append(Pair(guest, 'ME', 0))
        self.all_guests = {f.guest for f in self.pairs} | {f.neighbor for f in self.pairs}

    def get_pair(self, guest: str, neighbor: str) -> Pair:
        if guest not in self.all_guests or neighbor not in self.all_guests:
            raise InvalidPair(f"Invalid pair: {guest} and {neighbor}")
        else:
            return [p for p in self.pairs 
                    if p.guest == guest and p.neighbor == neighbor][0]

    def get_result(self, name1: str, name2: str) -> int:
        try:
            pair1 = self.get_pair(name1, name2)
            pair2 = self.get_pair(name2, name1) 
        except InvalidPair:
            raise
        
        return pair1.value + pair2.value

    def get_result_from_permutation(self, perm: tuple)-> int:
        output = 0
        for i, name in enumerate(perm):
            try:
                output += self.get_result(name, perm[i+1])
            except IndexError:
                output += self.get_result(name, perm[0])
        return output

def parse_data(data: str) -> PairSet:
    line_list = data.splitlines()

    output_list = []
    for line in line_list:
        parts = line.split(' ')
        guest = parts[0]
        verb = parts[2]
        value = int(parts[3])
        neighbor = parts[-1].strip('.')

        if verb == 'lose':
            value = 0 - value
            
        output_list.append(Pair(guest, neighbor, value))
                
    return PairSet(output_list)


def part_one(data: str):
    pair_set = parse_data(data)
    perms = itertools.permutations(pair_set.all_guests, pair_set.num_seats)
    return max(pair_set.get_result_from_permutation(perm) for perm in perms)
        
def part_two(data: str):
    pair_set = parse_data(data)
    pair_set.add_me()
    perms = itertools.permutations(pair_set.all_guests, pair_set.num_seats)
    return max(pair_set.get_result_from_permutation(perm) for perm in perms)


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()