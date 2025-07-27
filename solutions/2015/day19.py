import functools
import itertools
import json
import math
import os
import re
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


class Replacement(NamedTuple):
    start: str
    end: str

def parse_data(data: str) -> tuple[list[Replacement], str]:
    line_list = data.splitlines()

    replacement_list = []
    molecule = ''
    for line in line_list:
        if '=>' in line:
            parts = line.split(' => ')
            replacement_list.append(Replacement(parts[0], parts[1]))
        elif line:
            molecule = line

    molecule = molecule if molecule else 'HOHOHO'       
    return replacement_list, molecule

def make_replacement_dict(r_list: list[Replacement]) -> dict[str, list[str]]:
    unique_starts = {r.start for r in r_list}
    return {key: [r.end for r in r_list if r.start == key] for key in unique_starts}
            
    
def part_one(data: str):
    r_list, molecule = parse_data(data)
    # r_dict = make_replacement_dict(r_list)

    counter
    def 

    total_distinct_molecules = set()
    for r in r_list:
        for match in re.finditer(r.start, molecule):
            print(match.endpos) 
        
    

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()