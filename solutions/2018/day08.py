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
INPUT = aoc.get_input(YEAR, DAY)

''' Specifically, a node consists of:

    - A header, which is always exactly two numbers:
        - The quantity of child nodes.
        - The quantity of metadata entries.
    - Zero or more child nodes (as specified in the header).
    - One or more metadata entries (as specified in the header). '''

@dataclass(frozen=True)
class Node:
    c: int
    m: int
    metadata: list[int] = field(default_factory=list)


def create_tree(data: deque[int], level: int = 0) -> list[Node]:
    output_list = []
    print(f'creating tree at level {level}')

    while data:
        print(data)
        num_children = data.popleft()
        num_metadata = data.popleft()

        while data and num_children > 0:
            output_list += create_tree(data, level+1)
            num_children -= 1

        metadata_list = []
        while data and num_metadata > 0:
            metadata_list.append(data.popleft())
            num_metadata -= 1
  
        output_list.append(Node(num_children, num_metadata, metadata_list))

    print(f"Returning from level {level}: {output_list}")
    return output_list
        
        
        
    
    
def part_one(data: str):
    node_data = deque([int(x) for x in data.split(' ')])
    # print(node_data)
    node_list = create_tree(node_data)
    print(node_list )




def part_two(data: str):
    ...



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