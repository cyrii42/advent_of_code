import functools
import itertools
import json
import math
import operator
import os
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from pprint import pprint
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Iterator, NamedTuple, Optional, Protocol, Self

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

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def parse_data(data: str) -> int:
    return int(data)

def check_example_part_one():
    target_list = [10, 30, 40, 70, 60, 120, 80, 150, 130]


@dataclass
class House:
    id: int
    total_presents: int = 0

@dataclass
class Elf:
    id: int
    
    def __post_init__(self):
        self.delivery = map(lambda x: (x * self.id, self.id * 10), itertools.count(1))

    @property
    def next_delivery(self) -> tuple[int, int]:
        return self.delivery.__next__()



def determine_house_presents(house_num: int) -> int:
    '''The first house gets 10 presents: it is visited only by Elf 1, 
    which delivers 1 * 10 = 10 presents. The fourth house gets 70 presents, 
    because it is visited by Elves 1, 2, and 4, for a total of 10 + 20 + 40 = 70 presents.

    So:  For a given house n, the house is visited by Elf #n, plus all other Elves 
    between 1 and n whose numbers are divisible by n
    '''
    return sum(x*10 for x in range(1, house_num+1) if house_num % x == 0)

def factors(n):
    return set(functools.reduce(
        list.__add__,
        ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

    
def part_one(data: str):
    target = parse_data(data)

    factor_dict = {i: sum(factors(i)) for i in range(1, 101)}

    print(sorted(factor_dict.items(), key=lambda x: x[1], reverse=True))

    # for i in range(1, 101):
    #     print(f"{i}: {sum(factors((i))):,}")

    # print()
    # print(sum([x*10 for x in factors(300000000)]))
    # print(sum(determine_house_presents(300000000)))
    

    # n = 1
    # while True:
    #     if sum(factors((n))) >= target:
    #         return n
    #     else:
    #         n += 1


    
    # print({i: [x for x in range(1, 11) if x % i == 0] for i in range(1, 11)})

    # n = 1
    # while True:
    #     if get_result_for_house_n(n) >= target:
    #         return n
    #     else:
    #         n += 1

    # houses = [House(x) for x in range(1, 1000)]

    # elves = [elf_generator(x) for x in range(1, 11)]
    # for x in range(10):
    #     elf = elves[x]
    #     for _ in range(10):
    #         house_id, presents = elf.__next__()
    #         house = houses[house_id]
    #         house.total_presents += presents

    # print([house for house in houses[0:10]])

    # elf = Elf(3)
    # for _ in range(5):
    #     print(elf.next_delivery)

def part_two(data: str):
    __ = parse_data(data)


def get_cum_sum_for_house_n(n):
    elves_dict = {i: [x for x in range(1, n+1) if x % i == 0] for i in range(1, 11)}

    elves_per_house = [[key for key, val in elves_dict.items() if y in val] for y in range(1, n+1)]

    output = 0
    for house in range(n):
        print(f"House {house}: {elves_per_house[house]} ({sum(elf*10 for elf in elves_per_house[house])})")
        output += sum(elf*10 for elf in elves_per_house[house])
    return output
        



def main():
    # print(get_result_for_house_n(4))
    # check_example_part_one()
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
    # get_sum_for_house_num(7)
    # for i in range (1, 11):
    #     print(f"Elf #{i}: {[x for x in range(1, 11) if x % i == 0]}")

    # elves_dict = {i: [x for x in range(1, 11) if x % i == 0] for i in range(1, 11)}

    # for y in range(1, 11):
    #     elves = [key for key, val in elves_dict.items() if y in val]
    #     print(f"House #{y}: {sum(elf*10 for elf in elves)} (present in {elves})")
    
    # print(sum(x*10 for x in range(1, 8) if x % 7 == 0))
    # print()
    # output = 0
    # for i in range(1, 11):
    #     output += sum(x*10 for x in range(1, i+i) if i % x == 0)
    #     print(output)

       
if __name__ == '__main__':
    main()