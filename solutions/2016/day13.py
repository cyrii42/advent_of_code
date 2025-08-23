import functools
import hashlib
import itertools
import json
import math
import operator
import os
import pathlib
import re
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Literal, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)

NUM_ROWS = 50
NUM_COLS = 50
GOAL_ROW = 39
GOAL_COL = 31

# class Direction(IntEnum):
#     N  = 0
#     NE = 1
#     E  = 2
#     SE = 3
#     S  = 4
#     SW = 5
#     W  = 6
#     NW = 7

DIRECTIONS = {
    'N':    (1, 0),
    'NE':   (1, 1),
    'E':    (0, 1),
    'SE':   (-1, 1),
    'S':    (-1, 0),
    'SW':   (-1, -1),
    'W':    (0, -1),
    'NW':   (1, -1)
}

@dataclass
class Maze:
    num_rows: int
    num_cols: int
    fav_num: int
    goal_row: int
    goal_col: int
    maze: np.ndarray = field(init=False)
    d: dict[tuple[int, int], list[tuple[int, int]]] = field(init=False)

    def __post_init__(self):
        self.maze = np.array([[0 for _ in range(self.num_cols)] 
                              for _ in range(self.num_rows)])
        coordinates = [x for x in 
                       itertools.product(range(self.num_cols), 
                                         range(self.num_rows))]     
        for pair in coordinates:
            col, row = pair
            self.maze[row, col] = self.characterize_location(col, row)
        self.d = self.create_dict(coordinates)
        
    # Define the BFS function
    def bfs(self):
        print(f"Goal row: {self.goal_row}")
        print(f"Goal col: {self.goal_col}")
        count = 0
        visited = []
        queue = deque([(0, 0)])  # Initialize the queue with the starting node

        while queue:
            node = queue.popleft()

            print(node)
            row, col = node
            if row == self.goal_row and col == self.goal_col:
                return count

            if node not in visited:
                visited.append(node)
                count += 1

                # Enqueue all unvisited neighbors (children) of the current node
                for neighbor in self.d[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        # print(visited)
        # return count

    def create_dict(self, coordinates: list[tuple[int, int]]) -> dict:
        output_dict = {}
        for pair in coordinates:
            col, row = pair
            output_dict[(row, col)] = self.get_valid_neighbors(row, col)
        return output_dict

    def print(self):
        print(self.maze)

    def characterize_location(self, col: int, row: int) -> int:
        step1 = (col*col + 3*col + 2*col*row + row + row*row)
        step2 = step1 + self.fav_num
        step3 = str(bin(step2))[2:]
        step4 = len([char for char in step3 if char == '1'])
        return 0 if step4 % 2 == 0 else 1

    def get_neighbors(self, row: int, col: int) -> np.ndarray:
        row_start = max(row-1, 0)
        row_end = row+1
        col_start = max(col-1, 0)
        col_end = col+1
        return self.maze[row_start:row_end+1, col_start:col_end+1]

    def get_valid_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        output_list = []
        for loc in DIRECTIONS.values():
            new_row = row + loc[0]
            new_col = col + loc[1]
            if self.validate_pair((new_row, new_col)):
                output_list.append((new_row, new_col))
        return output_list

    # def get_valid_directions(self, 
    #                          row: int,
    #                          col: int
    #                          ) -> list[tuple[int, int]]:
    #     output_list = []
    #     for loc in DIRECTIONS.values():
    #         new_row = row + loc[0]
    #         new_col = col + loc[1]
    #         if self.validate_pair((new_row, new_col)):
    #             output_list.append(loc)
    #     return output_list

    def validate_pair(self, pair: tuple[int, int]) -> bool:
        row, col = pair
        if row < 0 or row >= self.num_rows:
            return False
        if col < 0 or col >= self.num_cols:
            return False
        if self.maze[row, col] == 0:
            return False
        return True
        
    
    def traverse(self, 
                 row: int = 0, 
                 col: int = 0,
                 count: int = 0,
                 points_visited: set[tuple[int, int]] = set()):
        
        if row == self.goal_row and col == self.goal_col:
            return count

        points_visited.add((row, col))
        count += 1

        neighbors = self.get_neighbors(row, col)

        ### maybe run all of the valid directions at once, find the minimum, 
        ### increment count by that number

        ### figure out a way to get a list of the VALID directions for a 
        ### given point

        # count += min((self.traverse(new_row, new_col, count, points_visited)
        #             for new_row, new_col in self.get_valid_directions(row, col)
        #              if (new_row, new_col) not in points_visited))

        counts = []
        for loc in self.get_valid_directions(row, col):
            # try:
            if not neighbors[loc]:
                continue
            new_row = row + loc[0]
            new_col = col + loc[1]
            if (new_row, new_col) not in points_visited:
                counts.append(self.traverse(new_row, new_col, count, points_visited))
        return counts
            # except IndexError:
            #     print(f"Index error on {row}, {col} with loc {loc}")
            #     continue
            

        return count

                

def parse_data(data: str) -> Maze:
    fav_num = int(data)
    if data == '10':
        num_rows = 7
        num_cols = 10
        goal_row = 4
        goal_col = 7
    else:
        num_rows = NUM_ROWS
        num_cols = NUM_COLS
        goal_row = GOAL_ROW
        goal_col = GOAL_COL
        
    return Maze(num_rows, num_cols, fav_num, goal_row, goal_col)
        
def part_one(data: str):
    maze = parse_data(data)
    # maze.print()
    print(maze.bfs())
    # print(maze.traverse())
    # print(maze.get_neighbors(1, 1))
    

def part_two(data: str):
    ...


def main():
    # print(f"Part One (example):  {part_one('10')}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    x = '01'
    print(int(x))

       
if __name__ == '__main__':
    main()