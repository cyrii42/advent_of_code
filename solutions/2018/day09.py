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

INPUT = aoc.get_input(YEAR, DAY)
TESTS_PART_ONE = [
    ('9 players; last marble is worth 25 points', 32),
    # ('10 players; last marble is worth 1618 points', 8317),
    # ('13 players; last marble is worth 7999 points', 146373),
    # ('17 players; last marble is worth 1104 points', 2764),
    # ('21 players; last marble is worth 6111 points', 54718),
    # ('30 players; last marble is worth 5807 points', 37305),
]

@dataclass
class MarbleGame:
    num_players: int
    last_marble: int
    player = 0
    ptr: int = 1
    score_dict: dict[int, int] = field(init=False)
    marble_list: deque[int] = field(init=False)
    marble_bag: itertools.count = field(init=False)
    
    def __post_init__(self):
        self.marble_list = deque([0])
        self.marble_bag = itertools.count(1)
        self.score_dict = defaultdict(int)

    @property
    def size(self) -> int:
        return len(self.marble_list)

    def print(self) -> None:
        output = ''
        for i, num in enumerate(self.marble_list):
            if i == self.ptr:
                output += f"({num})"
            else:
                output += ' ' + str(num) + ' '
        print(output)

    def simulate_game(self):
        while True:
            next_marble = next(self.marble_bag)
            if next_marble == self.last_marble:
                # print(self.score_dict)
                return max(v for v in self.score_dict.values())

            if next_marble % 23 == 0:
                # print(self.marble_list)
                self.marble_list.rotate(7)
                self.ptr = (self.ptr - 7) % self.size
                # print(self.marble_list)
                self.score_dict[self.player] = self.marble_list.popleft()
            else:
                self.marble_list.popleft()
                self.marble_list.rotate(1 - self.ptr)
                step_3_rotations = -1 if (self.ptr == 
                                          (self.size - 1)) else -2
                self.marble_list.rotate(step_3_rotations) 
                self.marble_list.appendleft(next_marble)
                self.marble_list.rotate(self.ptr + 1)
                self.marble_list.appendleft(0)
                self.ptr = (self.ptr + 2) % self.size
                self.print()

            self.player = (self.player + 1) % self.num_players
            
            
    

def parse_data(data: str) -> MarbleGame:
    parts = data.split(' ')
    num_players = int(parts[0])
    last_marble = int(parts[6])
    return MarbleGame(num_players, last_marble)

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        data, answer = example
        print(f"Test #{i}: {part_one(data) == answer}",
              f"({part_one(data)})")
    
def part_one(data: str):
    game = parse_data(data)
    return game.simulate_game()

def part_two(data: str):
    __ = parse_data(data)



def main():
    part_one_tests()
    # print(f"Part One (input):  {part_one(INPUT)}")
    # part_two_tests()
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

'''
[6]  0  4  2  5  1 (6) 3 
[7]  0  4  2  5  1  6  3 (7)
[8]  0 (8) 4  2  5  1  6  3  7 
[9]  0  8  4 (9) 2  5  1  6  3  7 
[1]  0  8  4  9  2(10) 5  1  6  3  7 
[2]  0  8  4  9  2 10  5(11) 1  6  3  7 
[3]  0  8  4  9  2 10  5 11  1(12) 6  3  7 
'''

def random_tests():
    ...
    # ptr = 7
    # # asdf = deque([0, 4, 2, 5, 1, 3])
    # # asdf = deque([0, 2, 1, 3
    # # asdf = deque([0, 4, 2, 5, 1, 6, 3, 7])
    # next_num = 12
    # asdf = deque([0, 8, 4, 9, 2, 10, 5, 11, 1, 6, 3, 7 ])
    # print(asdf)

    
    # asdf.popleft()  # remove leading zero
    # asdf.rotate(1 - ptr)  # put the current pointer at the beginning
    # step_3_rotations = -1 if ptr == (len(asdf) - 1) else -2
    # asdf.rotate(step_3_rotations)  # rotate CW one or two more times
    # asdf.appendleft(next_num)   # insert the next number at the beginning
    # asdf.rotate(ptr + 1)  # rotate back
    # asdf.appendleft(0)  # replace leading zero
    # print(asdf)

    
    # c = itertools.count(1)
    # asdf = deque([0])
    # ptr = 1
    # for _ in range(5):
    #     offset = (ptr * 2) % len(asdf)
    #     asdf.popleft()
    #     asdf.rotate(1-offset)
    #     asdf.appendleft(next(c))
    #     asdf.rotate(offset)
    #     asdf.appendleft(0)
    #     print(asdf)
    #     ptr += 1

       
if __name__ == '__main__':
    main()