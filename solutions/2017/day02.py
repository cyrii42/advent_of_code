import itertools
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE_PART_ONE = '5\t1\t9\t5\n7\t5\t3\n2\t4\t6\t8'
EXAMPLE_PART_TWO = '5\t9\t2\t8\n9\t4\t7\t3\n3\t8\t6\t5'
INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str):
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        split = line.split('\t') 
        output_list.append([int(x) for x in split])
    return output_list

def get_checksum(line: list[int]):
    return max(line) - min(line)

def find_divisors(line: list[int]) -> int:
    nums = sorted(line, reverse=True)
    for x, y in itertools.permutations(nums, 2):
        if x % y == 0:
            return x // y
    return 0

def part_one(data: str):
    line_list = parse_data(data)
    return sum(get_checksum(line) for line in line_list)

def part_two(data: str):
    line_list = parse_data(data)
    return sum(find_divisors(line) for line in line_list)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE_PART_ONE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()