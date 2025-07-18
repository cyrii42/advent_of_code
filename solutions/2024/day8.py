'''--- Day 8: Resonant Collinearity ---'''

from pathlib import Path
from rich import print
from pprint import pprint
from copy import deepcopy
from typing import NamedTuple, Protocol
from enum import Enum
from dataclasses import dataclass
from string import ascii_letters
import itertools
import pandas as pd
import numpy as np
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day8_example.txt'
INPUT = DATA_DIR / 'day8_input.txt'

@dataclass(frozen=True)
class Antenna():
    char: str
    row_num: int
    col_num: int

    @property
    def vector(self) -> np.ndarray:
        return np.array([self.row_num, self.col_num])
        

@dataclass(frozen=True)
class Antinode():
    char: str
    row_num: int
    col_num: int

    def validate(self, map_height: int) -> bool:
        return self.row_num >= 0 and self.row_num < map_height and self.col_num >= 0 and self.col_num < map_height

    def __eq__(self, other) -> bool:
        return self.row_num == other.row_num and self.col_num == other.col_num

    def __hash__(self):
        return hash((self.row_num, self.col_num))

@dataclass
class Map():
    row_list: list[str]

    @property
    def height(self) -> int:
        return len(self.row_list)

    @property
    def width(self) -> int:
        return len(self.row_list)

    @property
    def string(self) -> str:
        return ''.join(row for row in self.row_list)

    @property
    def antenna_types(self) -> set[str]:
        return set([char for char in self.string if char.isalnum()])

    @property
    def antenna_list(self) -> list[Antenna]:
        output_list = []
        for row_num, row in enumerate(self.row_list):
            for col_num, char in enumerate(row):
                if char.isalnum():
                    output_list.append(Antenna(char, row_num, col_num))
        return output_list

    def print(self):
        for row in self.row_list:
            print(row)

    def find_antinodes(self) -> set[Antinode]:
        output_list: list[Antinode] = []
        for char in self.antenna_types:
            antennas = [x for x in self.antenna_list if x.char == char]
            combos = itertools.combinations(antennas, 2)
            for combo in combos:
                antenna_1 = combo[0]
                antenna_2 = combo[1]
                # print(f"{antenna_1} - {antenna_2}")
                output_list += self.calculate_antinodes(antenna_1, antenna_2)
        return set([antinode for antinode in output_list if antinode.validate(map_height=self.height)])

    def calculate_antinodes(self, antenna_1: Antenna, antenna_2: Antenna) -> tuple[Antinode, Antinode]:                
        row_diff = antenna_1.row_num - antenna_2.row_num
        col_diff = antenna_1.col_num - antenna_2.col_num
        
        antinode_1 = Antinode(char=antenna_1.char,
                              row_num=antenna_1.row_num - row_diff,
                              col_num=antenna_1.col_num - col_diff)

        antinode_2 = Antinode(char=antenna_2.char,
                              row_num=antenna_2.row_num + row_diff,
                              col_num=antenna_2.col_num + col_diff)

        return (antinode_1, antinode_2)
            

def create_map(filename: Path) -> Map:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        
    return Map(line_list)

def part_one(filename: Path):
    map = create_map(filename)
    # map.print()
    # print()
    # print(map.antenna_list)
    # print(map.antenna_types)
    antinodes = map.find_antinodes()
    # print(map.height)
    # print(asdf)
    return len(antinodes)

def part_two(filename: Path):
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    # aaa = Antinode('C', 1, 1)
    # bbb = Antinode('D', 1, 1)
    # print(aaa == bbb)
    # c = [aaa, bbb]
    # print(c)
    # print(set(c))

    # f = [1, 2, 3]
    # print(list(itertools.combinations(f, 2)))

    # a = np.array([2, 4])
    # b = np.array([5, 8])
    # c = a + b
    # d = a - b
    # print(type(c))
    # print(c)
    # print(d)
    


if __name__ == '__main__':
    main()