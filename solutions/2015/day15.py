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

class Ingredient(NamedTuple):
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


@dataclass
class Cookie:
    ingredients: list[Ingredient]

    def __post_init__(self):
        self.num_ingredients = len(self.ingredients)
        self.combos = (x for x in 
                       itertools.permutations([x for x in range(101)], self.num_ingredients) 
                       if sum(x) == 100)

    def test_combo(self):
        ...

def parse_data(data: str):
    line_list = data.splitlines()

    output_list = []
    for line in line_list:
        parts = line.split(' ')
        name = parts[0]
        capacity = int(parts[2].strip(','))
        durability = int(parts[4].strip(','))
        flavor = int(parts[6].strip(','))
        texture = int(parts[8].strip(','))
        calories = int(parts[-1])
            
        output_list.append(Ingredient(name, capacity, durability, flavor, texture, calories))
                
    return Cookie(output_list)
    
def part_one(data: str):
    cookie = parse_data(data)
    print(cookie)

def part_two(data: str):
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