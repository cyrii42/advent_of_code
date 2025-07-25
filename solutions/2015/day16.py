import functools
import itertools
import json
import math
import os
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
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

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

TICKER_TAPE = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1   
}   

class ItemType(Enum):
    CHILDREN = 'children'
    CATS = 'cats'
    SAMOYEDS = 'samoyeds'
    POMERANIANS = 'pomeranians'
    AKITAS = 'akitas'
    VIZSLAS = 'vizslas'
    GOLDFISH = 'goldfish'
    TREES = 'trees'
    CARS = 'cars'
    PERFUMES = 'perfumes'

class Item(NamedTuple):
    type: ItemType
    num: int

@dataclass
class Sue:
    id: int
    items: list[Item] = field(default_factory=list)

    def check_ticker_tape_part_one(self) -> bool:
        ticker_tape_items = [Item(ItemType(key), value) 
                             for key, value in TICKER_TAPE.items()]
        
        return all(item in ticker_tape_items for item in self.items)

    def check_ticker_tape_part_two(self) -> bool:
        ticker_tape_items = [Item(ItemType(key), value) 
                             for key, value in TICKER_TAPE.items()]

        answer_list: list[bool] = []
        for item in self.items:
            if item.type in [ItemType.CATS, ItemType.TREES]:
                if item.type not in [ItemType(key) for key in TICKER_TAPE.keys()]:
                    return False
                ticker_tape_item = Item(item.type, TICKER_TAPE[item.type.value])
                answer_list.append(item.num > ticker_tape_item.num)
            elif item.type in [ItemType.POMERANIANS, ItemType.GOLDFISH]:
                if item.type not in [ItemType(key) for key in TICKER_TAPE.keys()]:
                    return False
                ticker_tape_item = Item(item.type, TICKER_TAPE[item.type.value])
                answer_list.append(item.num < ticker_tape_item.num)
            else:
                answer_list.append(item in ticker_tape_items)

        return all(answer_list)
                

def parse_data(data: str) -> list[Sue]:
    line_list = data.splitlines()

    output_list = []
    for line in line_list:
        parts = line.split(' ')
        id = int(parts[1].strip(':'))
        item1_name = parts[2].strip(':')
        item1_num = int(parts[3].strip(','))
        item2_name = parts[4].strip(':')
        item2_num = int(parts[5].strip(','))
        item3_name = parts[6].strip(':')
        item3_num = int(parts[7].strip(','))

        item_list = [Item(ItemType(item1_name), item1_num),
                     Item(ItemType(item2_name), item2_num),
                     Item(ItemType(item3_name), item3_num)]
        output_list.append(Sue(id, item_list))
                
    return output_list

def part_one(data: str):
    sue_list = parse_data(data)

    matching_sues = [sue for sue in sue_list if sue.check_ticker_tape_part_one()]
    if len(matching_sues) == 1:
        return matching_sues[0].id
    else:
        print(matching_sues)

def part_two(data: str):
    sue_list = parse_data(data)

    matching_sues = [sue for sue in sue_list if sue.check_ticker_tape_part_two()]
    if len(matching_sues) == 1:
        return matching_sues[0].id
    else:
        print(matching_sues)



def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()