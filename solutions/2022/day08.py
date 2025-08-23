'''--- Day 8: Treetop Tree House ---'''

import math
from copy import deepcopy
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, NamedTuple, Optional, Self

from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day8_example.txt'
INPUT = DATA_DIR / '2022_day8_input.txt'
       

def ingest_data(filename: Path):
    with open(filename) as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    return line_list

def make_column_lists(row_list: list[str]) -> list[str]:
    output_list = []
    for x in range(len(row_list)):
        output_list.append(''.join(row[x] for row in row_list))
        
    return output_list

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

@dataclass
class Tree():
    row: int
    col: int
    num: int

@dataclass
class Map():
    tree_list: list[Tree]

    @property
    def height(self) -> int:
        return max(tree.row for tree in self.tree_list)

    @classmethod
    def create_map(cls, line_list: list[str]) -> Self:
        tree_list = []
        for i, line in enumerate(line_list):
            for j, char in enumerate(line):
                tree_list.append(Tree(row=i, col=j, num=int(char)))
        
        return cls(tree_list)

    def get_adjacent_trees(self, tree: Tree, direction: Direction) -> list[Tree]:
        match direction:
            case Direction.LEFT:
                return sorted([test_tree for test_tree in self.tree_list 
                               if test_tree.row == tree.row and test_tree.col < tree.col],
                              key=lambda tree: tree.col, reverse=True)
            case Direction.RIGHT:
                return sorted([test_tree for test_tree in self.tree_list 
                               if test_tree.row == tree.row and test_tree.col > tree.col],
                              key=lambda tree: tree.col, reverse=False)
            case Direction.UP: 
                return sorted([test_tree for test_tree in self.tree_list 
                               if test_tree.col == tree.col and test_tree.row < tree.row],
                              key=lambda tree: tree.row, reverse=True)
            case Direction.DOWN:
                return sorted([test_tree for test_tree in self.tree_list 
                               if test_tree.col == tree.col and test_tree.row > tree.row],
                              key=lambda tree: tree.row, reverse=False)

    def check_tree(self, tree: Tree) -> bool:
        if tree.row == 0 or tree.row == self.height or tree.col == 0 or tree.col == self.height:
            return True
        if all(test_tree.num < tree.num for test_tree in self.get_adjacent_trees(tree, Direction.LEFT)):
            return True
        if all(test_tree.num < tree.num for test_tree in self.get_adjacent_trees(tree, Direction.RIGHT)):
            return True
        if all(test_tree.num < tree.num for test_tree in self.get_adjacent_trees(tree, Direction.UP)):
            return True
        return all(test_tree.num < tree.num for test_tree in self.get_adjacent_trees(tree, Direction.DOWN))

    def get_scenic_score(self, tree: Tree) -> int:
        if tree.row == 0 or tree.col == 0:
            return 0
        
        score_list = []
        for direction in Direction:
            score = 0
            for adjacent_tree in self.get_adjacent_trees(tree, direction):
                score += 1
                if adjacent_tree.num >= tree.num:
                    break
            score_list.append(score)
            
        return math.prod(score_list)
        
    def get_part_one_answer(self) -> int:
        tree_checks = [self.check_tree(tree) for tree in self.tree_list]
        return len([x for x in tree_checks if x])

    def get_part_two_answer(self) -> int:
        return max(self.get_scenic_score(tree) for tree in self.tree_list)

def part_one(filename: Path):
    line_list = ingest_data(filename)
    map = Map.create_map(line_list)
    return map.get_part_one_answer()

def part_two(filename: Path):
    line_list = ingest_data(filename)
    map = Map.create_map(line_list)
    return map.get_part_two_answer()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 
    print(f"Part One (input):  {part_one(INPUT)}") # 
    
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # 
    print(f"Part Two (input):  {part_two(INPUT)}") # 

    # random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()





