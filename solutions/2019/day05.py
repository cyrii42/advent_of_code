import functools
import hashlib
import itertools
import json
import math
import operator
import os
import sys
import re
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, NamedTuple, Optional, Self, Any
import inspect

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_bar, alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '1002,4,3,4,33'
INPUT = aoc.get_input(YEAR, DAY)

class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1

class Parameter(NamedTuple):
    value: int
    mode: ParameterMode

def get_num_parameters(fn: Callable) -> int:
    return len([x for x in inspect.signature(fn).parameters if x != 'mode'])

def get_ones_digit(num: int) -> int:
    return (num // 10**0) % 10

def get_digit_from_right(num: int, n: int) -> int:
    return (num // 10**n) % 10

@dataclass
class Computer:
    program: list[int] = field(repr=False)
    input_num: int
    output_list: list[int] = field(default_factory=list)
    ptr: int = 0

    def execute_program(self):
        while True:
            opcode = self.program[self.ptr]
            if opcode == 99:
                break

            match get_ones_digit(opcode):
                case 1 | 2:
                    fn = self.add if opcode == 1 else self.mul
                    parameter_list = []
                    for x in range(2, 5):
                        self.ptr += 1
                        mode_num = get_digit_from_right(opcode, x)
                        mode = ParameterMode(mode_num)
                        parameter = Parameter(value=self.program[self.ptr], mode=mode)
                        # print(fn, parameter)
                        parameter_list.append(parameter)
                    a, b, c = parameter_list
                    fn(a, b, c)
                case 3:
                    self.ptr += 1
                    a = self.program[self.ptr]
                    self.program[a] = self.input_num
                case 4:
                    self.ptr += 1
                    output_num = self.program[self.ptr]

                    if output_num != 0:
                        print(f"Non-zero output at line {self.ptr}")
                    self.output_list.append(output_num)
                case _:
                    print('asodfiasdoifhasdofhsadofih')

            self.ptr += 1
       
    def add(self, a: Parameter, b: Parameter, c: Parameter) -> None:
        val_a = self.program[a.value] if a.mode == ParameterMode.POSITION else a.value
        val_b = self.program[b.value] if b.mode == ParameterMode.POSITION else b.value
        self.program[c.value] = val_a + val_b

    def mul(self, a: Parameter, b: Parameter, c: Parameter) -> None:
        val_a = self.program[a.value] if a.mode == ParameterMode.POSITION else a.value
        val_b = self.program[b.value] if b.mode == ParameterMode.POSITION else b.value
        self.program[c.value] = val_a * val_b

def parse_data(data: str) -> list[int]:
    output_list = []
    for num_str in data.split(','):
        if num_str[0] == '-':
            output_list.append(0 - int(num_str[1:]))
        else:
            output_list.append(int(num_str))
    return output_list
    
    
def part_one(data: str):
    program = parse_data(data)
    comp = Computer(program, input_num=1)
    comp.execute_program()
    print(comp)

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
       
if __name__ == '__main__':
    main()