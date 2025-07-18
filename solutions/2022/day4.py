'''--- Day 4: Camp Cleanup ---'''

from pathlib import Path
from rich import print
from copy import deepcopy
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day4_example.txt'
INPUT = DATA_DIR / '2022_day4_input.txt'

def ingest_data(filename: Path) -> list[tuple[range, range]]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        range_pair_list = [x for x in [line.split(',') for line in line_list]]
        
    output_list = []
    for range_pair in range_pair_list:
        inner_list = []
        for range_str in range_pair:
            range_int_list = list(map(int, range_str.split('-')))
            range_obj = range(range_int_list[0], range_int_list[1]+1)
            inner_list.append(range_obj)
        output_list.append(inner_list)
    return output_list

def find_overlap(range_pair: tuple[range, range]) -> bool:
    range_1, range_2 = range_pair
    set1 = set(range_1)
    set2 = set(range_2)
    result = len(set1-set2) == 0 or len(set2-set1) == 0
    return result

def find_intersection(range_pair: tuple[range, range]) -> bool:
    range_1, range_2 = range_pair
    set1 = set(range_1)
    set2 = set(range_2)
    result = len(set1.intersection(set2)) > 0 or len(set2.intersection(set1)) > 0
    return result

def part_one(filename: Path) -> int:
    range_pair_list = ingest_data(filename)
    answer = len([x for x in range_pair_list if find_overlap(x)])
    return answer

def part_two(filename: Path) -> int:
    range_pair_list = ingest_data(filename)
    answer = len([x for x in range_pair_list if find_intersection(x)])
    return answer

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 2
    print(f"Part One (input):  {part_one(INPUT)}") # 
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # 4
    print(f"Part Two (input):  {part_two(INPUT)}") # 

if __name__ == '__main__':
    main()