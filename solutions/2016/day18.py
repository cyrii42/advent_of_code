import pathlib
from enum import StrEnum

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)

class Tile(StrEnum):
    TRAP = '^'
    SAFE = '.'

def characterize_tile(left: str, right: str) -> str:
    if right == Tile.TRAP and left == Tile.SAFE:
        return Tile.TRAP
    if left == Tile.TRAP and right == Tile.SAFE:
        return Tile.TRAP
    return Tile.SAFE

def get_next_row(prev_row: str) -> str:
    output_str = ''
    for i in range(len(prev_row)):
        left = Tile.SAFE.value if i == 0 else prev_row[i-1]
        right = Tile.SAFE.value if i == len(prev_row)-1 else prev_row[i+1]
        output_str += characterize_tile(left, right)
    return output_str
    
def part_one(data: str):
    row = data
    n = len([x for x in row if x == '.'])
    for _ in range(39):
        row = get_next_row(row)
        n += len([x for x in row if x == '.'])
    return n

def part_two(data: str):
    row = data
    n = len([x for x in row if x == '.'])
    for _ in range(399_999):
        row = get_next_row(row)
        n += len([x for x in row if x == '.'])
    return n

def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
       
if __name__ == '__main__':
    main()