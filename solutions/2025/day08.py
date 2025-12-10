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

import numpy as np
import pandas as pd
import polars as pl
import networkx as nx
from alive_progress import alive_bar, alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class Point(NamedTuple):
    x: int
    y: int
    z: int

def get_distance(n1: Point, n2: Point) -> float:
    ''' https://en.wikipedia.org/wiki/Euclidean_distance#Higher_dimensions '''
    return math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2 + (n1.z - n2.z)**2)

def find_closest_point(p1: Point, point_list: list[Point]) -> Point:
    distances = {get_distance(p1, p2): p2 for p2 in point_list if p2 != p1}
    return distances[min(distances.keys())]

def find_two_closest_points(point_list: list[Point]) -> tuple[Point, Point]:
    distance_dict = {get_distance(p1, p2): (p1, p2) for p1, p2 
                     in itertools.permutations(point_list, 2)}
    return distance_dict[min(distance_dict.keys())]

'''
- take closest pair of boxes
- 

'''

   
def part_one(data: str, stop: int = 1000):
    point_list = [Point(*[int(x) for x in line.split(',')]) 
                  for line in data.splitlines()]

    distance_dict = {get_distance(p1, p2): (p1, p2) for p1, p2 
                     in itertools.permutations(point_list, 2)}
    distances = sorted(distance_dict.keys())

    circuit_list: list[list[Point]] = []

    i = 0
    connections_made = 0
    for distance in distances:
        if connections_made == stop:
            print(circuit_list)
            return len(circuit_list[0]) * len(circuit_list[1]) * len(circuit_list[2]) 
        p1, p2 = distance_dict[distance]
        # print(p1, p2)
        # print()

        # Check whether p1 and p2 are already linked in a circuit; if so, do nothing
        if any(c for c in circuit_list if p1 in c and p2 in c):
            print(f"ALREADY LINKED TOGETHER:  {p1} and {p2}")

        elif any(c for c in circuit_list if p1 in c) and any(c for c in circuit_list if p2 in c):
            ...
            print(f"ALREADY IN SEPARATE CIRCUITS: {p1} and {p2}")
            c1 = next(c for c in circuit_list if p1 in c)
            c2 = next(c for c in circuit_list if p2 in c)
            c_new = list(set(c1 + c2))
            circuit_list.append(c_new)
            circuit_list.remove(c1)
            circuit_list.remove(c2)
            connections_made += 1

        # Check whether neither p1 nor p2 is already in a circuit; if so, make a new circuit for them
        elif not any(c for c in circuit_list if p1 in c) and not any(c for c in circuit_list if p2 in c):
            print(f"Adding new circuit: {p1}, {p2}")
            circuit_list.append([p1, p2])
            connections_made += 1



        # Otherwise, 
        else:
            for circuit in circuit_list:
                if p1 in circuit and p2 not in circuit:
                    print(f"Adding {p2} to {circuit}")
                    circuit.append(p2)
                    connections_made += 1
                    break
                if p2 in circuit and p1 not in circuit:
                    print(f"Adding {p1} to {circuit}")
                    circuit.append(p1)
                    connections_made += 1
                    break
        

    circuit_list = sorted(circuit_list, key=lambda c: len(c), reverse=True)
    print(circuit_list)
    return len(circuit_list[0]) * len(circuit_list[1]) * len(circuit_list[2])

    
def part_two(data: str):
    ...



def main():
    print(f"Part One (example):  {part_one(EXAMPLE, stop = 10)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
       
if __name__ == '__main__':
    main()