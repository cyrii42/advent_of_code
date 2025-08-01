import functools
import itertools
import math
import operator
import pathlib
from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE="1\n2\n3\n4\n5\n7\n8\n9\n10\n11"
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def find_first_group_qe(package_list: list[int], weight_per_group: int) -> int:
    min_qe = math.inf
    min_group_size = math.inf
    for x in range(len(package_list)):
        if min_group_size < math.inf:
            break
        
        search_set = (g for g in itertools.permutations(package_list, r=x) 
                      if sum(g) == weight_per_group)
        
        for group in search_set:
            qe = functools.reduce(operator.mul, group)
            if qe < min_qe:
                min_qe = qe
                min_group_size = x

    return int(min_qe) if isinstance(min_qe, int) else 0

def parse_data(data: str):
    line_list = data.splitlines()
    return sorted([int(x) for x in line_list], reverse=True)
    
def part_one(data: str):
    package_list = parse_data(data)
    weight_per_group = int(sum(package_list) / 3)
    return find_first_group_qe(package_list, weight_per_group)

def part_two(data: str):
    package_list = parse_data(data)
    weight_per_group = int(sum(package_list) / 4)
    return find_first_group_qe(package_list, weight_per_group)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()