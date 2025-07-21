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
from string import ascii_letters
from typing import Callable, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

'''
https://wiki.python.org/moin/BitwiseOperators

x << y
    Returns x with the bits shifted to the left by y places (and new bits on the 
    right-hand-side are zeros). This is the same as multiplying x by 2**y.
x >> y
    Returns x with the bits shifted to the right by y places. This is the same as 
    floor division of x by 2**y.
x & y
    Does a "bitwise and". Each bit of the output is 1 if the corresponding bit of 
    x AND of y is 1, otherwise it's 0.
x | y
    Does a "bitwise or". Each bit of the output is 0 if the corresponding bit of 
    x AND of y is 0, otherwise it's 1.
~ x
    Returns the complement of x - the number you get by switching each 1 for a 0 
    and each 0 for a 1. This is the same as -x - 1.
x ^ y
    Does a "bitwise exclusive or". Each bit of the output is the same as the 
    corresponding bit in x if that bit in y is 0, and it's the complement of 
    the bit in x if that bit in y is 1.
'''

def parse_data(data: str):
    line_list = [line for line in data.split('\n') if line]
    print(line_list)
    
def part_one(data: str):
    __ = parse_data(data)

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
    x = 5
    print(x)
    print(x << 2)

       
if __name__ == '__main__':
    main()