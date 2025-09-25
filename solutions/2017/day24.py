import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
import sys
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, NamedTuple, Optional, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_bar, alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

@dataclass
class Component:
    port1: int
    port2: int

    @property
    def port_type_sum(self) -> int:
        return self.port1 + self.port2

def validate_connection(comp1: Component, comp2: Component):
    comp2_ports = (comp2.port1, comp2.port2)
    return (comp1.port1 in comp2_ports or comp1.port2 in comp2_ports)

@dataclass
class Bridge:
    component_list: list[Component]

    def is_valid(self) -> bool:
        if self.component_list[0].port1 != 0:
            return False

        i = 0
        while i < len(self.component_list) - 1:
            if not validate_connection(self.component_list[i], self.component_list[i+1]):
                return False
            i += 1

        return True
            
        # return (
        #     len(list(set(self.port_type_list))) <= len(self.component_list) + 1
        #     and self.component_list[0].port1 == 0
        # )

    @property
    def port_type_list(self) -> list[int]:
        output_list = []
        for comp in self.component_list:
            output_list.append(comp.port1)
            output_list.append(comp.port2)
        return output_list
    
    @property
    def strength(self) -> int:
        return sum(comp.port_type_sum for comp in self.component_list)

def parse_data(data: str) -> list[Component]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        num1, num2 = line.split('/')
        output_list.append(Component(int(num1), int(num2)))
    return output_list
    
def part_one(data: str):
    component_list = parse_data(data)
    combos = (itertools.combinations(component_list, x) for x in range(2, len(component_list)+1))
    combinations = itertools.chain(*combos)
    winner = None
    for combo in combinations:
        print(combo)
        bridge = Bridge(list(combo))
        if bridge.is_valid() and winner is None or bridge.strength > winner.strength:
            winner = bridge
    return winner
        

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()