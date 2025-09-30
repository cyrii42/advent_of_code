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

def create_graph(pair_list: list[tuple[str, str]]) -> dict[str, set[str]]:
    output_dict = defaultdict(set)
    for parent, child in pair_list:
        output_dict[parent].add(child)
    return output_dict

# def find_correct_order(graph: dict[str, list[str]], 
#                        parent: Optional[str] = None,
#                        visited: Optional[list[str]] = None) -> str:  
#     if not parent:
#         parent = next(p for p in graph.keys() if p not in graph.values())
#     if not visited:
#         visited = []
        
#     visited.append(parent)
#     for child in sorted(graph[parent]):
#         if child not in visited:
#             find_correct_order(graph, child, visited)
            
#     return ''.join(node for node in visited)

# def find_correct_order(graph: dict[str, set[str]]) -> str:
#     start = next(p for p in graph.keys() if p not in graph.values())
#     print(f"Start: {start}")
    
#     queue = deque([(start, [])])

#     visited = []
#     visited.append(start)

#     while queue:
#         node, path = queue.popleft()
#         neighbors = graph[node]
#         for neighbor in sorted(neighbors):
#             if neighbor not in visited:
#                 new_path = path + [neighbor]
#                 queue.append((neighbor, new_path))
#                 visited.append(neighbor)

#     return ''.join(node for node in visited)

def parse_data(data: str) -> list[tuple[str, str]]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        _, step1, _, _, _, _, _, step2, _, _ = line.split()
        output_list.append((step1, step2))
    return output_list

def part_one(data: str):
    pair_list = parse_data(data)
    graph = create_graph(pair_list)
    return find_correct_order(graph)

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