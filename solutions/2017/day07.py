import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Literal, NamedTuple, Optional, Protocol, Self

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
class Program:
    name: str
    weight: int
    children_names: list[str] = field(default_factory=list, repr=False)
    children: list["Program"] = field(default_factory=list, repr=False)
    parent: "Program" = field(init=False, repr=False)

    @property
    def total_weight(self) -> int:       
        return self.weight + sum(c.weight for c in self.children)

@dataclass
class Tower:
    programs: list[Program]

    def __post_init__(self):
        self.populate_children()

    def get_program_by_name(self, name: str) -> Program | None:
        try:
            return next(p for p in self.programs if p.name == name)
        except StopIteration:
            print(f"Can't find program w/ name {name} among {len(self.programs)} programs:",
                  f"{[program.name for program in self.programs]}")
            return None

    def populate_children(self) -> None:
        for program in self.programs:
            if not program.children_names:
                continue
            for name in program.children_names:
                prog_to_append = self.get_program_by_name(name)
                if prog_to_append:
                    program.children.append(prog_to_append)

    def get_all_children_names(self) -> set[str]:
        output_set = set()
        for program in self.programs:
            if not program.children_names:
                continue
            for child in program.children_names:
                output_set.add(child)
        return output_set

    def get_top_parent(self) -> Program:
        return next(p for p in self.programs 
                    if p.name not in self.get_all_children_names())

    def get_stack_weights(self) -> list[int]:
        top_parent = self.get_top_parent()
        return [child.total_weight for child in top_parent.children]

    def get_sub_towers(self) -> list["Tower"]:
        top_parent = self.get_top_parent()
        return [Tower(child.children) for child in top_parent.children if child.children]

    def make_parent_to_children_dict(self) -> dict[str, list[str]]:
        return {p.name: p.children_names for p in self.programs}

    def make_child_to_immediate_parent_dict(self) -> dict[str, str]:
        output_dict: dict[str, str] = {}

        parent_to_children_dict = self.make_parent_to_children_dict()
        all_children = set()
        for child_list in parent_to_children_dict.values():
            for child in child_list:
                all_children.add(child)
                
        for child in all_children:
            parents = [parent for parent in parent_to_children_dict.keys()
                          if child in parent_to_children_dict[parent]]
            if len(parents) > 1:
                raise IndexError(f"Found {len(parents)} for program {child}")
            if len(parents) == 1:
                output_dict[child] = parents[0]
        return output_dict

    def print_hierarchy(self):
        parents = [self.get_top_parent()]

        level = 0
        while True:
            print(f"Level {level}: ")
            
            

def parse_data(data: str) -> Tower:
    line_list = data.splitlines()
    
    program_list = []
    for line in line_list:
        match line.split(' '):
            case [name, weight, '->', *children_names]:
                children_names = [child.replace(',', '') 
                            for child in children_names]
                program = Program(name=name,
                                  weight=int(''.join(
                                      c for c in weight if c.isdigit())),
                                  children_names=children_names)
                program_list.append(program)
            case [name, weight]:
                program = Program(name=name,
                                  weight=int(''.join(
                                      c for c in weight if c.isdigit())))
                program_list.append(program)
    return Tower(program_list)
    
def part_one(data: str):
    tower = parse_data(data)
    return tower.get_top_parent().name

def part_two(data: str):
    tower = parse_data(data)
    print(tower.make_parent_to_children_dict())
    print(tower.make_child_to_immediate_parent_dict())


    ''' Can we make a dictionary for looking up a program's parents? '''
    
    # sub_towers = tower.get_sub_towers()
    # print(sub_towers)
    

    ''' I guess maybe we need to go down and create sub-stacks '''



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()