import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
from collections import defaultdict, deque
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
class DanceGroup:
    moves_list: list[str] = field(repr=False)
    dancers: str = 'abcdefghijklmnop'

    @property
    def num_dancers(self) -> int:
        return len(self.dancers)

    def simulate_dance(self):
        for move in self.moves_list:
            match move[0]:
                case 's':
                    self.spin(int(move[1:]))
                case 'x':
                    a, b = move[1:].split('/')
                    self.exchange(int(a), int(b))
                case 'p':
                    a, b = move[1:].split('/')
                    self.partner(a, b)

    def spin(self, n: int) -> None:
        ''' Makes N programs move from the end to the front, but maintain
        their order otherwise. (For example, s3 on abcde produces cdeab). '''
        self.dancers = self.dancers[-n:] + self.dancers[:-n]

    def exchange(self, a: int, b: int) -> None:
        ''' Makes the programs at positions A and B swap places. '''
        if a == b:
            return 
        
        idx1 = min(a, b)
        idx2 = max(a, b)

        if idx1 == 0:
            self.dancers = (self.dancers[idx2] + 
                            self.dancers[idx1+1:idx2] + self.dancers[idx1] +
                            self.dancers[idx2+1:])   

        elif idx2 == self.num_dancers - 1:
            self.dancers = (self.dancers[0:idx1] + self.dancers[idx2] + 
                            self.dancers[idx1+1:idx2] + self.dancers[idx1])  

        else:
            self.dancers = (self.dancers[0:idx1] + self.dancers[idx2] + 
                            self.dancers[idx1+1:idx2] + self.dancers[idx1] +
                            self.dancers[idx2+1:])   

    def partner(self, a: str, b: str) -> None:
        ''' Makes the programs named A and B swap places. '''
        if a == b:
            return 
        
        idx_a = self.dancers.index(a)
        idx_b = self.dancers.index(b)
        self.exchange(idx_a, idx_b)
    
    @classmethod
    def from_data(cls, data: str) -> Self:
        return cls(data.split(','))

def example_part_one():
    dg = DanceGroup(moves_list=['s1','x3/4','pe/b'], dancers='abcde')
    dg.simulate_dance()
    return dg.dancers
    
def part_one(data: str):
    dg = DanceGroup.from_data(data)
    dg.simulate_dance()
    return dg.dancers

def part_two(data: str):
   ...



def main():
    print(f"Part One (example):  {example_part_one()}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()