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

EXAMPLE = '../.# => ##./#../...\n.#./..#/### => #..#/..../..../#..#'
INPUT = aoc.get_input(YEAR, DAY)

START = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, 1, 1]])

# START = np.array([[1, 1, 0, 1, 1, 0],
#                   [1, 0, 0, 1, 0, 0], 
#                   [0, 0, 0, 0, 0 ,0],
#                   [1, 1, 0, 1, 1, 0],
#                   [1, 0, 0, 1, 0, 0],
#                   [0, 0, 0, 0, 0, 0]]) 
                  

class EnhancementFailed(Exception):
    pass

@dataclass
class Rule:
    input: np.ndarray
    output: np.ndarray

    def check_input(self, input_image: np.ndarray) -> bool:
        if input_image.shape[0] != self.input.shape[0]:
            return False

        return (np.array_equal(input_image, self.input) 
                or np.array_equal(np.flipud(input_image), self.input)
                or np.array_equal(np.fliplr(input_image), self.input)
                or np.array_equal(np.rot90(input_image, k=1), self.input)
                or np.array_equal(np.rot90(input_image, k=2), self.input)
                or np.array_equal(np.rot90(input_image, k=3), self.input))

    def __repr__(self) -> str:
        return self.input.__str__() + ' => \n' + self.output.__str__()

@dataclass
class ArtGenerator:
    data: str
    image: np.ndarray = field(init=False)
    ruleset: list[Rule] = field(init=False)

    def __post_init__(self) -> None:
        self.image = START
        self.ruleset = parse_data(self.data)

    def __repr__(self) -> str:
        return self.image.__str__()

    @property
    def image_size(self) -> int:
        ''' Returns the length of the first row of the image '''
        return self.image.shape[0]

    @property
    def num_pixels_on(self) -> int:
        return self.image.sum()

    def enhance_image(self) -> None:
        ''' If the size is evenly divisible by 2, break the pixels up 
            into 2x2 squares, and convert each 2x2 square into a 3x3 square 
            by following the corresponding enhancement rule. 

            Otherwise, the size is evenly divisible by 3; break the 
            pixels up into 3x3 squares, and convert each 3x3 square into 
            a 4x4 square by following the corresponding enhancement rule.

            Finally, join the squares into a new grid.'''

        # if image size = 3, we only have one sub-image, so enhance it and return
        if self.image_size == 3:
            self.image = self._enhance_subimage(self.image)
            return

        # otherwise, break the pixels up into 2x2 or 3x3 squares
        subimage_list = self._extract_subimages()

        # then enhance each sub-image
        enhanced_subimages = [self._enhance_subimage(si) for si in subimage_list]

        # then stitch the sub-images back together
        self.image = self._merge_enhanced_subimages(enhanced_subimages)

    def _extract_subimages(self) -> list[np.ndarray]:
        subimage_size = 2 if self.image_size % 2 == 0 else 3
        
        slices = [(0+(i*subimage_size),subimage_size+(i*subimage_size))
                  for i in range(self.image_size // subimage_size)]
        
        output_list = []
        for pair in itertools.product(slices, repeat=2):
            image_copy = self.image.copy()
            s1, s2 = pair
            output_list.append(image_copy[s1[0]:s1[1], s2[0]:s2[1]])
        return output_list

    def _enhance_subimage(self, subimage: np.ndarray) -> np.ndarray:
        for rule in self.ruleset:
            if rule.check_input(subimage):
                return rule.output
        raise EnhancementFailed

    def _merge_enhanced_subimages(self, subimage_list: list[np.ndarray]) -> np.ndarray:
        ...

    

def parse_data(data: str) -> list[Rule]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        line = line.replace('#', '1').replace('.', '0').replace('=>', '/')
        line = [x.strip() for x in line.split('/')]
        break_pt = len(line) // 2   # 2 of 5 OR 3 of 7
        start = np.array([[int(c) for c in num] for num in line[0:break_pt]])
        end = np.array([[int(c) for c in num] for num in line[break_pt:]])
        output_list.append(Rule(start, end))
    return output_list

def part_one(data: str):
    art_generator = ArtGenerator(data)
    num_iterations = 2 if data == EXAMPLE else 5
    # for rule in art_generator.ruleset:
    #     print(f"{rule}\n")
    for _ in range(num_iterations):
        art_generator.enhance_image()
    # print(art_generator.image)
    # return art_generator.num_pixels_on

def part_two(data: str):
    art_generator = ArtGenerator(data)
    

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