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
                                 and all(n in visited for n in prereq_graph[node])], reverse=True)
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