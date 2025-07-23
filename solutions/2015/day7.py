import functools
import itertools
import json
import math
import operator
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

class WireNotFound(Exception):
    pass

GATES: dict[str, Callable] = {
    'AND': operator.and_,
    'OR': operator.or_,
    'LSHIFT': operator.lshift,
    'RSHIFT': operator.rshift
}

@dataclass
class WireSet:
    wires: dict[str, np.uint16] = field(default_factory=dict)

    @property
    def complete(self) -> bool:
        return self.wires.get('a') is not None

    def provide_signal(self, parts: list[str]) -> np.uint16 | None:
        item1, _, _ = parts
        if item1.isdigit():
            return np.uint16(item1)
        else:
            input_id = item1
            return self.wires.get(input_id)

    def apply_not(self, parts: list[str]) -> np.uint16 | None:
        _, item1, _, _ = parts
             
        if item1.isdigit():
            input_signal = np.uint16(item1)
        else:
            input_id = item1
            input_signal = self.wires.get(input_id)

        return ~input_signal if input_signal is not None else None

    def apply_other(self, parts: list[str]) -> np.uint16 | None:
        item1, func_name, item2, _, _ = parts
        func = GATES[func_name]

        if item1.isdigit():
            input_signal_1 = np.uint16(item1)
        else:
            input_id_1 = item1
            input_signal_1 = self.wires.get(input_id_1)

        if item2.isdigit():
            input_signal_2 = np.uint16(item2)
        else:
            input_id_2 = item2
            input_signal_2 = self.wires.get(input_id_2)

        if input_signal_1 is not None and input_signal_2 is not None:
            return func(input_signal_1, input_signal_2)
        else:
            return None




    def execute_instruction(self, instruction: str) -> None:
        parts = instruction.split(' ')
        output_id = parts[-1]

        if output_id in self.wires.keys():
            return

        if len(parts) == 3:
            output_signal = self.provide_signal(parts)

        elif parts[0] == 'NOT':
            output_signal = self.apply_not(parts)

        elif parts[1] in ['LSHIFT', 'RSHIFT', 'AND', 'OR']:
            output_signal = self.apply_other(parts)

        else:
            raise WireNotFound(parts, len(parts))

        if output_signal is not None:
            self.wires[output_id] = output_signal
        else:
            return




def parse_data(data: str) -> list[str]:
    line_list = [line for line in data.split('\n') if line]
    return line_list

def part_one_example(data: str):
    wire_set = WireSet()
    instruction_list = parse_data(data)

    for instruction in instruction_list:
        wire_set.execute_instruction(instruction)

    print(wire_set)    
    
def part_one(data: str):
    wire_set = WireSet()
    instruction_list = parse_data(data)

    while not wire_set.complete:
        for instruction in instruction_list:
            wire_set.execute_instruction(instruction)

    return wire_set.wires['a']
        
def part_two(data: str, part_one_signal: np.uint16):
    wire_set = WireSet()
    instruction_list = parse_data(data)

    wire_set.wires['b'] = part_one_signal

    while not wire_set.complete:
        for instruction in instruction_list:
            wire_set.execute_instruction(instruction)

    return wire_set.wires.get('a')



def main():
    part_one_example(EXAMPLE)
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT, part_one(INPUT))}")

    random_tests()

def random_tests():
    ...
       
if __name__ == '__main__':
    main()