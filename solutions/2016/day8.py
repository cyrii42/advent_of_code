import pathlib

import numpy as np
from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

np.set_printoptions(linewidth=1000)

class Grid:
    def __init__(self, rows: int, cols: int):
        self.grid = np.array([[0 for _ in range(cols)] for _ in range(rows)])

    def execute_instruction(self, inst: str) -> None:
        if inst.startswith('rect'):
            inst = inst.removeprefix('rect ')
            a, b = inst.split('x')
            self.rect(int(a), int(b))
        elif inst.startswith ('rotate row'):
            inst = inst.removeprefix('rotate row y=')
            a, b = inst.split('by')
            self.shift_right(int(a), int(b))
        else:
            inst = inst.removeprefix('rotate column x=')
            a, b = inst.split('by')
            self.shift_down(int(a), int(b))
            
    def print(self):
        print(self.grid)

    def print_lines(self):
        for i, x in enumerate(np.nditer(self.grid, order='C'), start=1):
            if x == 1:
                print('#', end=' ')
            else:
                print(' ', end=' ')
            if i % 50 == 0:
                print('\n')

    def rect(self, width: int, height: int) -> None:
        self.grid[0:height,0:width] = 1

    def shift_right(self, row_num: int, pixels: int) -> None:
        self.grid[row_num,0:] = np.roll(self.grid[row_num,0:], pixels)

    def shift_down(self, col_num: int, pixels: int) -> None:
        self.grid[0:,col_num] = np.roll(self.grid[0:,col_num], pixels)


def part_one(data: str):
    grid = Grid(6, 50)
    
    line_list = data.splitlines()
    for line in line_list:
        grid.execute_instruction(line)
        
    return grid.grid.sum()
    
def part_two(data: str):
    grid = Grid(6, 50)
    
    line_list = data.splitlines()
    for line in line_list:
        grid.execute_instruction(line)
        
    grid.print_lines()

def tests():
    grid = Grid(3, 7)
    grid.rect(3, 2)
    grid.print()

    grid.shift_down(1, 1)
    grid.print()

    grid.shift_right(0, 4)
    grid.print()

    grid.shift_down(1, 1)
    grid.print()

def main():
    print(f"Part One:  {part_one(INPUT)}")
    print("Part Two:")
    part_two(INPUT)

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()