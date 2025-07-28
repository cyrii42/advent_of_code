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

EXAMPLE_PART_ONE = aoc.get_example(YEAR, DAY)
EXAMPLE_PART_TWO = 'e => H\ne => O\nH => HO\nH => OH\nO => HH\n'
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)


class Replacement(NamedTuple):
    start: str
    end: str

def parse_data(data: str) -> tuple[list[Replacement], str]:
    line_list = data.splitlines()

    r_list = []
    molecule = ''
    for line in line_list:
        if '=>' in line:
            start, end = line.split(' => ')
            r_list.append(Replacement(start, end))
        elif line:
            molecule = line

    molecule = molecule if molecule else 'HOHOHO'       
    return r_list, molecule

def find_new_molecules(r_list: list[Replacement], starting_molecule: str) -> set[str]:
    output_set = set()
    
    for r in r_list:
        for m in re.finditer(r.start, starting_molecule):
            start, end = m.span()
            new_molecule = m.string[0:start] + r.end + m.string[end:]
            output_set.add(new_molecule)

    return output_set
    
def part_one(data: str):
    r_list, starting_molecule = parse_data(data)
    distinct_new_molecules = find_new_molecules(r_list, starting_molecule)
    return len(distinct_new_molecules)



def fabricate_target_molecule(r_list: list[Replacement], 
                              start_str: str,
                              target_str: str,
                              count: int = 0) -> int:

    if start_str == target_str:
        return count
    
    for r in r_list:
        if r.start in start_str:
            for m in re.finditer(r.start, start_str):
                start, end = m.span()
                new_start_str = m.string[0:start] + r.end + m.string[end:]
                if new_start_str == start_str:
                    continue
                if new_start_str == target_str:
                    return count
                
                return fabricate_target_molecule(r_list, new_start_str, target_str, count+1)

    return count

            
            
        
        
    

        

    

def part_two(data: str):
    r_list, target_str = parse_data(data)
    start_str = 'e'

    return fabricate_target_molecule(r_list, start_str, target_str)

    

    for r in r_list:
        ...



def main():
    # print(f"Part One (example):  {part_one(EXAMPLE_PART_ONE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # # print()
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()