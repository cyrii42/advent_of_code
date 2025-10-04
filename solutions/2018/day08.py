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

EXAMPLE = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
# EXAMPLE = '3 4 0 3 1 2 5 2 2 1 1 0 2 3 3 1 0 3 1 2 4 1 2 1 2 0 1 2 1 2 1 1 2 3'

'''
3 4 0 3 1 2 5 2 2 1 1 0 2 3 3 1 0 3 1 2 4 1 2 1 2 0 1 2 1 2 1 1 2 3
A------------------------------------------------------------------
    B-------- C------------------------------ G-------------
                  D------------ F--------         H----
                      E------
'''


INPUT = aoc.get_input(YEAR, DAY)

sys.setrecursionlimit(10**6)

''' Specifically, a node consists of:

    - A header, which is always exactly two numbers:
        - The quantity of child nodes.
        - The quantity of metadata entries.
    - Zero or more child nodes (as specified in the header).
    - One or more metadata entries (as specified in the header). 

    So maybe:
    - capture (popleft) the two header numbers at the beginning of the list
    - capture (popright) the correct number of metadata entries at the end of the list
    - recurse on the remaining numbers

    '''

@dataclass(frozen=True)
class Node:
    c: int
    m: int
    level: int = 0
    metadata: list[int] = field(default_factory=list)

    @property
    def metadata_sum(self) -> int:
        return sum(m for m in self.metadata)


def create_tree(data: deque[int], level: int = 0) -> list[Node]:
    ''' STILL NEED TO DO THE PARENT/CHILD RELATIONSHIPS; THIS IS
    JUST A FLAT LIST RIGHT NOW'''
    output_list = []

    while data:
        num_children = data.popleft()
        try:
            num_metadata = data.popleft()
        except IndexError:
            break
        # print(num_children, num_metadata)

        # if num_children > 0:
        #     output_list += create_tree(data, level+1)
        #     metadata_list = [data.popleft() for _ in range(num_metadata)]
        # else:
        #     metadata_list = [data.pop() for _ in range(num_metadata)]

        # try:
        #     metadata_list = []
        #     for _ in range(num_metadata):
        #         metadata_list.append(data.popleft())
        #     # metadata_list = [data.popleft() for _ in range(num_metadata)]
        # except IndexError:
        #     print(num_children, num_metadata, metadata_list, level)
        #     raise

        if num_children == 0:
            metadata_list = [data.popleft() for _ in range(num_metadata)]
            
        else:
            metadata_list = [data.pop() for _ in range(num_metadata)]
            output_list += create_tree(data, level+1)

        node = Node(num_children, num_metadata, level, metadata_list)
        print(node)
        output_list.append(node)

        # if num_children > 0:
        #     output_list += create_tree(data, level+1)

  
    return output_list
        

def get_metadata_total(data: list[int]):
    ''' https://dev.to/steadbytes/aoc-2018-day-8-memory-maneuver-34jf '''
    n_children, n_metadata = data[0:2]
    remaining = data[2:]

    total = 0
    
    # if there aren't any children, this loop doesn't happen
    for _ in range(n_children):
        child_total, remaining = get_metadata_total(remaining)
        total += child_total

    current_node_metadata = remaining[0:n_metadata]
    current_node_total = sum(current_node_metadata)

    total += current_node_total

    return total, remaining[n_metadata:]


    
    
def part_one(data: str):
    node_data = [int(x) for x in data.split(' ')]
    # return solve_part_one(node_data)  
    # node_data = deque([int(x) for x in data.split(' ')])
    # print(node_data)
    # node_list = create_tree(node_data)
    # print(node_list)
    # return sum(node.metadata_sum for node in node_list)
    meta_total, _ = get_metadata_total(node_data)
    return meta_total




def part_two(data: str):
    ...



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