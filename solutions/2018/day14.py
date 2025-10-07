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
    ('9', '5158916779'),
    ('5', '0124515891'),
    ('18', '9251071085'),
    ('2018', '5941429882'),
]

START = (3, 7)

'''
To create new recipes, the two Elves combine their current recipes. This creates new recipes
from the digits of the sum of the current recipes' scores. With the current recipes' scores 
of 3 and 7, their sum is 10, and so two new recipes would be created: the first with score 1
and the second with score 0. If the current recipes' scores were 2 and 3, the sum, 5, would 
only create one recipe (with a score of 5) with its single digit.

The new recipes are added to the end of the scoreboard in the order they are created. So, 
after the first round, the scoreboard is 3, 7, 1, 0.

After all new recipes are added to the scoreboard, each Elf picks a new current recipe. 
To do this, the Elf steps forward through the scoreboard a number of recipes equal to 1 
plus the score of their current recipe. So, after the first round, the first Elf moves 
forward 1 + 3 = 4 times, while the second Elf moves forward 1 + 7 = 8 times. If they run 
out of recipes, they loop back around to the beginning. After the first round, both Elves
happen to loop around until they land on the same recipe that they had in the beginning; 
in general, they will move to different recipes.
'''

@dataclass
class ElfPair:
    num_recipes: int
    elf_recipes: tuple[int, int] = field(init=False)
    scoreboard: deque[int] = field(init=False)

    def __post_init__(self):
        elf1, elf2 = START
        self.elf_recipes = (elf1, elf2)
        self.scoreboard = deque([*START])      

    def create_new_recipes(self) -> None:
        ...

    def add_new_recipes_to_scoreboard(self, new_scores: list[int]) -> None:
        assert 0 < len(new_scores) < 3
         
    def choose_new_recipes(self) -> None:
        for i, elf_recipe in enumerate(self.elf_recipes):
            ...
            
            

    def execute_next_round(self) -> None:
        self.create_new_recipes()
        self.choose_new_recipes()

    def solve_part_one(self) -> str:
        while len(self.scoreboard) < self.num_recipes + 10:
            self.execute_next_round()

        # find the scores of the ten recipes after the first *num_recipes*
        self.scoreboard.rotate(0 - self.num_recipes)
        return ''.join(str(self.scoreboard.popleft()) for _ in range(10))

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        num_recipes, answer = example
        test_answer = part_one(num_recipes)
        print(f"Test #{i}: {test_answer == answer}",
              f"({test_answer})")

def execute_next_round(recipe_scores: deque[int]) -> deque[int]:
    return deque([x for x in range(10)]*3)
    
def part_one(data: str):
    elf_pair = ElfPair(int(data))
    return elf_pair.solve_part_one()

def part_two(data: str):
    ...



def main():
    part_one_tests()
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()