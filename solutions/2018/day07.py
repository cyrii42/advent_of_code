import functools
import hashlib
import heapq
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
from queue import PriorityQueue
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

def create_order_graph(pair_list: list[tuple[str, str]]
                       ) -> dict[str, set[str]]:
    output_dict = defaultdict(set)
    for parent, child in pair_list:
        output_dict[parent].add(child)
    return output_dict

def create_prereq_graph(pair_list: list[tuple[str, str]]
                               ) -> dict[str, set[str]]:
    output_dict = defaultdict(set)
    for parent, child in pair_list:
        output_dict[child].add(parent)
    return output_dict

def find_correct_order(order_graph: dict[str, set[str]], 
                       prereq_graph: dict[str, set[str]]
                       ) -> str:
    start = sorted(p for p in order_graph.keys() 
                   if p not in prereq_graph.keys())[0]
    all_nodes = {n for n in order_graph.keys()} | {n for n in prereq_graph.keys()}
    visited = [start]

    while True:
        next_node_list = sorted([node for node in all_nodes 
                                 if node not in visited 
                                 and all(n in visited for n in prereq_graph[node])], 
                                reverse=True)
        next_node = next_node_list.pop()
        visited.append(next_node)
        if len(visited) == len(all_nodes):
            return ''.join(node for node in visited)

def parse_data(data: str) -> list[tuple[str, str]]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        _, step1, _, _, _, _, _, step2, _, _ = line.split()
        output_list.append((step1, step2))
    return output_list

def part_one(data: str):
    pair_list = parse_data(data)
    order_graph = create_order_graph(pair_list)
    prereq_graph = create_prereq_graph(pair_list)
    return find_correct_order(order_graph, prereq_graph)



@dataclass
class Elf:
    id: int
    step: str
    time_remaining: int = field(init=False)

    def __post_init__(self):
        assert 1 <= self.id <= 5
        assert len(self.step) == 1 
        assert self.step.isupper()
        self.time_remaining = 60 + (ord(self.step) - 64)    ## add 60 for input

    @property
    def finished(self) -> bool:
        return self.time_remaining <= 0

    def increment(self) -> None:
        self.time_remaining -= 1

class ElfSlotsFull(Exception):
    pass

@dataclass
class ElfGroup:
    elf_list: list[Elf] = field(default_factory=list)

    @property
    def full(self) -> bool:
        return len(self.elf_list) >= 5   ## 2 for example, 5 for input

    @property
    def steps_processing(self) -> list[str]:
        return [elf.step for elf in self.elf_list]

    def add_elf(self, step: str) -> None:
        if len(self.elf_list) >= 5:
            raise ElfSlotsFull

        next_elf_id = len(self.elf_list) + 1
        self.elf_list.append(Elf(next_elf_id, step))

    def delete_elf(self, elf: Elf) -> None:
        self.elf_list.remove(elf)

    def list_elves(self) -> None:
        print(self.elf_list)

    def get_finished_steps(self) -> list[str]:
        output_list = []
        
        for elf in self.elf_list:
            elf.increment()
            if elf.finished:
                output_list.append(elf.step)
                self.delete_elf(elf)
            
        return output_list
        

    

def find_correct_order_part_two(order_graph: dict[str, set[str]], 
                                prereq_graph: dict[str, set[str]]
                                ) -> str:
    ''' If multiple steps are available, workers should still begin them in 
    alphabetical order. Each step takes 60 seconds plus an amount corresponding
    to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, 
    while step Z takes 60+26=86 seconds. No time is required between steps. '''

    start = sorted(p for p in order_graph.keys() 
                   if p not in prereq_graph.keys())[0]
    all_nodes = {n for n in order_graph.keys()} | {n for n in prereq_graph.keys()}
    visited = []

    elf_group = ElfGroup()

    while True:
        next_node_list = sorted([node for node in all_nodes 
                                 if node not in visited 
                                 and all(n in visited for n in prereq_graph[node])
                                 and node not in elf_group.steps_processing], 
                                reverse=True)

        if next_node_list and not elf_group.full:
            next_node = next_node_list.pop()
            elf_group.add_elf(next_node)

        visited += elf_group.get_finished_steps()
        elf_group.list_elves()
        
        if len(visited) == len(all_nodes):
            return ''.join(node for node in visited)
    

def part_two(data: str):
    pair_list = parse_data(data)
    order_graph = create_order_graph(pair_list)
    prereq_graph = create_prereq_graph(pair_list)
    return find_correct_order_part_two(order_graph, prereq_graph)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()



def random_tests():
    ...

       
if __name__ == '__main__':
    main()