import functools
import hashlib
import itertools
import json
import math
import operator
import os
import pathlib
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Literal, NamedTuple, Optional, Protocol, Self, Sequence

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

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

'''
CHIPS:
    - if a microchip is ever left in the same area as another generator, and it's 
    not connected to its own generator, the microchip will be fried.

    - keep microchips connected to their corresponding generator when they're 
    in the same room, and away from other generators otherwise.

ELEVATOR:
    - can carry at most yourself and two generators or microchips in any combination

    - will only function if it contains at least one generator or microchip

    - always stops on each floor to recharge, and this takes long enough that 
    the items within it and the items on that floor can irradiate each other. 
    (You can prevent this if a microchip and its generator end up on the same 
    floor in this way, as they can be connected while the elevator is recharging.)
      
'''

BOTTOM_FLOOR = 1
TOP_FLOOR = 4

class ItemType(Enum):
    GENERATOR = 'generator'
    MICROCHIP = 'microchip'

@dataclass
class Item:
    element: str
    type: ItemType
    floor: int

    def __repr__(self) -> str:
        return f"{self.element} {self.type.value} (Floor #{self.floor})"

@dataclass
class State:
    items: list[Item]
    # valid_next_states: list["State"] = field(init=False)

    def get_potential_items_to_move(self) -> Sequence[tuple[Item, Optional[Item]]]:
        combo_list = [(item, None) for item in self.items]
        for floor in range(1, TOP_FLOOR + 1):
            items_on_floor = (item for item in self.items if item.floor == floor)
            for combo in itertools.permutations(items_on_floor, 2):
                combo_list.append(combo) # type: ignore
        return combo_list

    @property
    def is_valid(self) -> bool:
        for floor in range(1, TOP_FLOOR + 1):
            items_on_floor = [item for item in self.items if item.floor == floor]
            microchips = [item for item in items_on_floor 
                          if item.type == ItemType.MICROCHIP]
            generators = [item for item in items_on_floor 
                          if item.type == ItemType.GENERATOR]
            for chip in microchips:
                if (any(gen for gen in generators if gen.element != chip.element)
                    and not any(gen for gen in generators if gen.element == chip.element)):
                    return False
        return True

def parse_data(data: str) -> State:
    IGNORED_WORDS = ['The', 'floor', 'contains', 'a', 'and',
                    'first', 'second', 'third', 'fourth',
                    'nothing', 'relevant']
    line_list = data.splitlines()
    item_list = []
    for i, line in enumerate(line_list, start=1):
        line = line.removesuffix('.').replace(',', '').replace('-compatible', '')
        words = [word for word in line.split(' ') if word not in IGNORED_WORDS]
        print(words)
        
        j = 0
        while j < len(words):
            item = Item(element=words[j], 
                                type=ItemType(words[j+1]),
                                floor=i)
            print(item)
            item_list.append(item)
            j += 2
    return State(item_list)


    
def part_one(data: str):
    initial_state = parse_data(data)
    print(list(initial_state.get_potential_items_to_move()))
    


def part_two(data: str):
    ...



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