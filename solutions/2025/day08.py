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

@dataclass
class Circuit:
    boxes: list[Point] = field(default_factory=list)

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
   
def part_one(data: str):
    point_list = [Point(*[int(x) for x in line.split(',')]) 
                  for line in data.splitlines()]

    distance_dict = {get_distance(p1, p2): (p1, p2) for p1, p2 
                     in itertools.permutations(point_list, 2)}
    distances = sorted(distance_dict.keys())

    circuit_list: list[Circuit] = []
    for distance in distances:
        p1, p2 = distance_dict[distance]

        if any(c for c in circuit_list if p1 in c.boxes and p2 in c.boxes):
            continue

        if any(c for c in circuit_list if p1 in c.boxes or p2 in c.boxes):
            for circuit in circuit_list:
                if p1 in circuit.boxes and p2 not in circuit.boxes:
                    circuit.boxes.append(p2)
                    break
                elif p2 in circuit.boxes and p1 not in circuit.boxes:
                    circuit.boxes.append(p1)
                    break

        else:
            circuit_list.append(Circuit(boxes=[p1, p2]))

    circuit_list = sorted(circuit_list, key=lambda c: len(c.boxes), reverse=True)
    print(circuit_list)
    return len(circuit_list[0].boxes) * len(circuit_list[1].boxes)

            
    

    # while True:
    #     p1, p2 = find_two_closest_points(point_list)
    
    
    # p1, p2 = find_two_closest_points(point_list)
    # print(p1, p2)
    
    
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