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

class Component(NamedTuple):
    port1: int
    port2: int
    
    def __repr__(self):
        return f"{self.port1}/{self.port2}"

def get_strength(comp: Component) -> int:
        return comp.port1 + comp.port2

@dataclass
class Bridge:
    component_list: list[Component]

    @property
    def strength(self) -> int:
        return sum(get_strength(comp) for comp in self.component_list)

def make_graph(component_list: list[Component]) -> dict[Component, list[Component]]:
    output_dict = {}
    for comp in component_list:
        output_dict[comp] = [c for c in component_list 
                                if c != comp
                                and (
                                    (c.port1 > 0 and c.port1 == comp.port1) 
                                    or (c.port2 > 0 and c.port2 == comp.port2)
                                    or (c.port1 > 0 and c.port1 == comp.port2)
                                    or (c.port2 > 0 and c.port2 == comp.port1)
                                )]
    return output_dict

def parse_data(data: str) -> list[Component]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        port1, port2 = [int(x) for x in line.split('/')]
        output_list.append(Component(port1, port2))
    return output_list

def make_component_dict(component_list: list[Component]) -> dict[Component, tuple[bool, bool]]:
    return {comp: (False, False) for comp in component_list}

def find_strongest_bridge(graph: dict[Component, list[Component]],
                          parent: Component,
                          visited: Optional[list[Component]] = None) -> list[Component]:
    if visited is None:
        visited = []
        
    visited.append(parent)
    # print(f"{parent}: {graph[parent]}")
    for child in graph[parent]:
        if child not in visited:
            find_strongest_bridge(graph, child, visited)
            
    return visited
    
def part_one(data: str):
    component_list = parse_data(data)
    graph = make_graph(component_list)
    potential_starts = [comp for comp in component_list if comp.port1 == 0 or comp.port2 == 0]

    print(find_strongest_bridge(graph, potential_starts[0]))

    # valid_bridges = find_valid_bridges(graph)
    # return max(bridge.strength for bridge in valid_bridges)
        

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