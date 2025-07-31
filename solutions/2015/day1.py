from pathlib import Path

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

    
def part_one(data: str) -> int:
    location = 0
    for char in data:
        if char == '(':
            location += 1
        if char == ')':
            location -= 1
    return location


def part_two(data: str) -> int:
    location = 0
    for i, char in enumerate(data, start=1):
        if char == '(':
            location += 1
        if char == ')':
            location -= 1

        if location == -1:
            return i
    return -1



def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()