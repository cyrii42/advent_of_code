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

@dataclass(frozen=True)
class Port:
    comp_id: int
    type: int
    

    def __add__(self, other) -> int:
        if not isinstance(other, Port):
            raise TypeError
        return self.type + other.type

class Component(NamedTuple):
    id: int
    port1: Port
    port2: Port
    
    def __repr__(self):
        return f"{self.port1.type}/{self.port2.type}"

    @property
    def strength(self) -> int:
        return self.port1.type + self.port2.type

# def make_graph(port_list: list[Port]) -> dict[Port, list[Port]]:
#     output_dict = {}
#     for port in port_list:
#         output_dict[port] = [p for p in port_list
#                              if p.type > 0
#                              and p.type == port.type
#                              and p.comp_id != port.comp_id]
#     return output_dict

# def make_graph(component_list: list[Component]
#                ) -> dict[Component, list[Component]]:
#     output_dict = {}
#     for comp in component_list:
#         output_dict[comp] = [c for c in component_list 
#                                 if c != comp
#                                 and (
#                                     (c.port1.type > 0 and c.port1.type == comp.port1.type) 
#                                     or (c.port2.type > 0 and c.port2.type == comp.port2.type)
#                                     or (c.port1.type > 0 and c.port1.type == comp.port2.type)
#                                     or (c.port2.type > 0 and c.port2.type == comp.port1.type)
#                                 )]
#     return output_dict



def find_strongest_bridge(graph: dict[Component, list[Component]],
                          parent: Component,
                          visited: Optional[list[Component]] = None,
                          used_ports: Optional[list[Port]] = None
                          ) -> list[Component]:
    if visited is None:
        visited = [parent]
    else:
        visited.append(parent)
        
    if used_ports is None:
        used_ports = [p for p in (parent.port1, parent.port2) 
                      if p.type == 0]
        unused_ports = [p for comp in visited for p in comp if p not in used_ports]
        print(unused_ports)
    else:
        unused_ports = [p for comp in visited for p in comp if p not in used_ports]
        used_ports += [p for p in (parent.port1, parent.port2) 
                       if p.type == unused_ports[-1]]
        
    for child in graph[parent]:
        if child not in visited:
            if ((parent.port1 in unused_ports and 
                 ((child.port1 == parent.port1) or child.port2 == parent.port1))
            or (parent.port2 in unused_ports and 
                 ((child.port1 == parent.port2) or child.port2 == parent.port2))):
                find_strongest_bridge(graph, child, visited, used_ports)
            
    return visited

def parse_data(data: str) -> defaultdict[int, set[int]]:
    ''' https://www.reddit.com/r/adventofcode/comments/7lte5z/comment/droveqk/'''
    # line_list = data.splitlines()
    # output_list = []
    # for comp_id, line in enumerate(line_list):
    #     type1, type2 = [int(x) for x in line.split('/')]
    #     port1 = Port(comp_id, type1)
    #     port2 = Port(comp_id, type2)
    #     output_list.append(Component(comp_id, port1, port2))
    # return output_list
    components = defaultdict(set)
    for line in data.strip().splitlines():
        a, b = [int(x) for x in line.split('/')]
        components[a].add(b)
        components[b].add(a)
    return components

def gen_bridges(bridge, components):
    ''' https://www.reddit.com/r/adventofcode/comments/7lte5z/comment/droveqk/ '''
    bridge = bridge or [(0, 0)]
    cur = bridge[-1][1]
    for b in components[cur]:
        if not ((cur, b) in bridge or (b, cur) in bridge):
            new = bridge+[(cur, b)]
            yield new
            yield from gen_bridges(new, components)
    
def part_one(data: str):
    ''' https://www.reddit.com/r/adventofcode/comments/7lte5z/comment/droveqk/ '''
    graph = parse_data(data)
    mx = []
    for bridge in gen_bridges(None, graph):
        mx.append((len(bridge), sum(a+b for a, b in bridge)))
    return sorted(mx, key=lambda x: x[1])[-1][1]
        

def part_two(data: str):
    ''' https://www.reddit.com/r/adventofcode/comments/7lte5z/comment/droveqk/ '''
    graph = parse_data(data)
    mx = []
    for bridge in gen_bridges(None, graph):
        mx.append((len(bridge), sum(a+b for a, b in bridge)))
    return sorted(mx)[-1][1]



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