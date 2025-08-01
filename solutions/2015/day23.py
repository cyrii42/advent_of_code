import functools
import itertools
import json
import math
import os
import pathlib
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Literal, NamedTuple, Optional, Protocol, Self

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
DESCRIPTION = aoc.get_description(YEAR, DAY)

class NoValidFunction(Exception):
    pass

def dummy_func():
    raise NoValidFunction

class Instruction(NamedTuple):
    name: str
    reg: Optional[str] = ''
    offset: Optional[int] = 0

@dataclass
class Computer:
    program: list[Instruction]
    a: int = 0
    b: int = 0
    ptr: int = 0

    def __post_init__(self):
        self.instructions_dict: dict[str, Callable] = {
            'hlf': self.hlf,
            'tpl': self.tpl,
            'inc': self.inc,
            'jmp': self.jmp,
            'jie': self.jie,
            'jio': self.jio,
        }

    def execute_program(self) -> None:
        ''' The program exits when it tries to run an instruction beyond the ones defined. '''
        while True:
            if self.ptr >= len(self.program):
                break
            inst = self.program[self.ptr]
            func = self.get_instruction_func(inst.name)
            if inst.reg and inst.offset:
                func(inst.reg, inst.offset)
            elif inst.offset:
                func(inst.offset)
            else:
                func(inst.reg)
            
    def get_register_value(self, r: str):
        match r:
            case 'a':
                return self.a
            case 'b': 
                return self.b
            case _:
                raise ValueError

    def set_register_value(self, r: str, value: int):
         match r:
            case 'a':
                self.a = value
            case 'b': 
                self.b = value
            case _:
                raise ValueError

    def get_instruction_func(self, inst_name: str) -> Callable:
        return self.instructions_dict.get(inst_name, dummy_func)
            
    def hlf(self, r: str):
        ''' sets register `r` to half its current value, then continues 
        with the next instruction '''
        current_reg_val = self.get_register_value(r)
        new_reg_val = current_reg_val // 2
        self.set_register_value(r, new_reg_val)
        self.ptr += 1

    def tpl(self, r: str):
        ''' sets register `r` to triple its current value, then continues 
        with the next instruction '''
        current_reg_val = self.get_register_value(r)
        new_reg_val = current_reg_val * 3
        self.set_register_value(r, new_reg_val)
        self.ptr += 1

    def inc(self, r: str):
        ''' increments register `r`, adding `1` to it, then continues with the 
        next instruction '''
        current_reg_val = self.get_register_value(r)
        new_reg_val = current_reg_val + 1
        self.set_register_value(r, new_reg_val)
        self.ptr += 1

    def jmp(self, offset: int):
        ''' is a jump; it continues with the instruction, `offset` away relative 
        to itself '''
        self.ptr += offset
        
    def jie(self, r: str, offset: int):
        ''' is like jmp, but only jumps if register `r` is even ("jump if even") '''
        reg_val = self.get_register_value(r)
        
        if reg_val % 2 == 0:
            self.ptr += offset
        else:
            self.ptr += 1

    def jio(self, r: str, offset: int):
        ''' is like jmp, but only jumps if register `r` is `1` ("jump if one", not odd) '''
        reg_val = self.get_register_value(r)
        
        if reg_val == 1:
            self.ptr += offset
        else:
            self.ptr += 1

def get_offset_int(offset_str: str) -> int:
    offset_sign = offset_str[0]
    if offset_sign == '+':
        return int(offset_str[1:])
    else:
        return 0 - int(offset_str[1:])

def parse_data(data: str) -> list[Instruction]:
    line_list = data.splitlines()

    output_list = []
    for line in line_list:
        if ',' in line:
            name, reg, offset_str = line.split(' ')
            reg = reg.removesuffix(',')
            offset_int = get_offset_int(offset_str)
            output_list.append(Instruction(name, reg, offset_int))
        elif line[-1].isdigit():
            name, offset_str = line.split(' ')
            offset_int = get_offset_int(offset_str)
            output_list.append(Instruction(name, None, offset_int))
        else:
            name, reg = line.split(' ')
            output_list.append(Instruction(name, reg))
    return output_list

def example_part_one(data: str):
    program = parse_data(data)
    computer = Computer(program)
    computer.execute_program()
    return computer.a
    
def part_one(data: str):
    program = parse_data(data)
    computer = Computer(program)
    computer.execute_program()
    return computer.b

def part_two(data: str):
    program = parse_data(data)
    computer = Computer(program)
    computer.a = 1
    computer.execute_program()
    return computer.b


def main():
    print(f"Part One (example):  {example_part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
       
if __name__ == '__main__':
    main()