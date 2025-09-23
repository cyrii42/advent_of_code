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
# START = np.rot90(START, k=3)

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
    potential_inputs: list[np.ndarray] = field(init=False, repr=False)

    def __post_init__(self):
        self.potential_inputs = self.create_potential_inputs_list()

    def create_potential_inputs_list(self) -> list[np.ndarray]:
        return [self.input.copy(),
                np.flip(self.input.copy()),
                np.fliplr(self.input.copy()),
                np.rot90(self.input.copy(), k=1),
                np.flip(np.rot90(self.input.copy(), k=1)),
                np.fliplr(np.rot90(self.input.copy(), k=1)),
                np.rot90(self.input.copy(), k=2),
                np.flip(np.rot90(self.input.copy(), k=2)),
                np.fliplr(np.rot90(self.input.copy(), k=2)),
                np.rot90(self.input.copy(), k=3),
                np.flip(np.rot90(self.input.copy(), k=3)),
                np.fliplr(np.rot90(self.input.copy(), k=3)),]

    def check_input(self, input_image: np.ndarray) -> bool:
        if input_image.shape[0] != self.input.shape[0]:
            return False

        return any(np.array_equal(test, self.input)
                   for test in self.potential_inputs)

    def to_dict(self) -> dict[bytes, np.ndarray]:
        return {test.tobytes(): self.output for test in self.potential_inputs}

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
        raise EnhancementFailed(subimage)

    def _merge_enhanced_subimages(self, subimage_list: list[np.ndarray]) -> np.ndarray:
        num_subimages = len(subimage_list)
        subimages_per_row = math.isqrt(num_subimages)
        num_rows = subimages_per_row

        row_list = []
        for i in range(num_rows):
            start = 0 + i*subimages_per_row
            end = subimages_per_row + i*subimages_per_row
            row_list.append(np.concatenate(*[subimage_list[start:end]], axis=1))

        return np.concatenate([row for row in row_list], axis=0)       

def parse_data(data: str, part_two: bool=False) -> list[Rule]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        line = line.replace('#', '1').replace('.', '0').replace('=>', '/')
        line = [x.strip() for x in line.split('/')]
        break_pt = len(line) // 2   # 2 of 5 OR 3 of 7
        if part_two:
            start = pl.DataFrame([[int(c) for c in num] for num in line[0:break_pt]])
            end = pl.DataFrame([[int(c) for c in num] for num in line[break_pt:]])
            output_list.append(Rule_v2(start, end))
        else:
            start = np.array([[int(c) for c in num] for num in line[0:break_pt]])
            end = np.array([[int(c) for c in num] for num in line[break_pt:]])
            output_list.append(Rule(start, end))
    return output_list

def part_one(data: str):
    art_generator = ArtGenerator(data)
    num_iterations = 2 if data == EXAMPLE else 5
    for _ in range(num_iterations):
        art_generator.enhance_image()
    return art_generator.num_pixels_on

@dataclass
class Rule_v2:
    input: pl.DataFrame
    output: pl.DataFrame
    potential_inputs: list[pl.DataFrame] = field(init=False, repr=False)

    def __post_init__(self):
        self.potential_inputs = self.create_potential_inputs_list()
        # print(self.potential_inputs)

    def create_potential_inputs_list(self) -> list[pl.DataFrame]:
        nparray = self.input.to_numpy()
        return [pl.from_numpy(nparray.copy()),
                pl.from_numpy(np.flip(nparray.copy())),
                pl.from_numpy(np.fliplr(nparray.copy())),
                pl.from_numpy(np.rot90(nparray.copy(), k=1)),
                pl.from_numpy(np.flip(np.rot90(nparray.copy(), k=1))),
                pl.from_numpy(np.fliplr(np.rot90(nparray.copy(), k=1))),
                pl.from_numpy(np.rot90(nparray.copy(), k=2)),
                pl.from_numpy(np.flip(np.rot90(nparray.copy(), k=2))),
                pl.from_numpy(np.fliplr(np.rot90(nparray.copy(), k=2))),
                pl.from_numpy(np.rot90(nparray.copy(), k=3)),
                pl.from_numpy(np.flip(np.rot90(nparray.copy(), k=3))),
                pl.from_numpy(np.fliplr(np.rot90(nparray.copy(), k=3)))]

    def check_input(self, input_image: pl.DataFrame) -> bool:
        if input_image.shape[0] != self.input.shape[0]:
            return False

        return any(self.input.equals(test)
                   for test in self.potential_inputs)

    def __repr__(self) -> str:
        return self.input.__str__() + ' => \n' + self.output.__str__()

@dataclass
class ArtGenerator_v2:
    data: str
    image: pl.DataFrame = field(init=False)
    ruleset: list[Rule_v2] = field(init=False)

    def __post_init__(self) -> None:
        self.image = pl.from_numpy(START)
        self.ruleset = parse_data(self.data, part_two=True)

    def __repr__(self) -> str:
        return self.image.__str__()

    @property
    def image_size(self) -> int:
        ''' Returns the length of the first row of the image '''
        return self.image.shape[0]

    @property
    def num_pixels_on(self) -> int:
        return self.image.sum().sum_horizontal()[0]

    def enhance_image(self) -> None:
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

    def _extract_subimages(self) -> list[pl.DataFrame]:
        subimage_size = 2 if self.image_size % 2 == 0 else 3
        
        slices = [(0+(i*subimage_size),subimage_size+(i*subimage_size))
                  for i in range(self.image_size // subimage_size)]
        
        output_list = []
        for pair in itertools.product(slices, repeat=2):
            image_copy = self.image
            s1, s2 = pair
            output_list.append(image_copy[s1[0]:s1[1], s2[0]:s2[1]])
        return output_list

    def _enhance_subimage(self, subimage: pl.DataFrame) -> pl.DataFrame:
        for rule in self.ruleset:
            if rule.check_input(subimage):
                return rule.output
        raise EnhancementFailed(subimage)

    def _merge_enhanced_subimages(self, subimage_list: list[pl.DataFrame]) -> pl.DataFrame:
        num_subimages = len(subimage_list)
        subimages_per_row = math.isqrt(num_subimages)
        num_rows = subimages_per_row

        row_list = []
        for i in range(num_rows):
            start = 0 + i*subimages_per_row
            end = subimages_per_row + i*subimages_per_row
            row_list.append(pl.concat(*[subimage_list[start:end]]))

        return pl.concat([row for row in row_list])        

def part_two(data: str):
    ''' https://www.reddit.com/r/adventofcode/comments/7l78eb/comment/drk8j2m/

    After 3 iterations a 3x3 block will have transformed into 9 more 3x3 blocks whose
    futures can all be calculated independently. Using this fact I just keep track of 
    how many of each "type" of 3x3 block I have at each stage, and can thus easily 
    calculate the number of each type of 3x3 block I'll have 3 iterations later.'''

    '''
    OTHER IDEA:
    - there are only so many rules; maybe, instead of actually reconstructing the 
    picture each time, you just have a dictionary that keeps a running tally of 
    how many of each output type there are
        - but then how do you make the NEXT image?
        - 

    '''
    art_generator = ArtGenerator_v2(data)
    num_iterations = 2 if data == EXAMPLE else 18
    for _ in range(num_iterations):
        art_generator.enhance_image()
        print(art_generator.num_pixels_on)
    return art_generator.num_pixels_on


def main():
    # print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
    # print(START)
    # b = START.tolist()
    # print(str(START))
    # print(np.frombuffer(b, dtype=int))   

    # l = {START.tobytes(): START}
    # l1 = l[START.tobytes()]
    # print(np.array(l1))

    df = pl.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    print(df.sum().sum_horizontal()[0])

            
if __name__ == '__main__':
    main()