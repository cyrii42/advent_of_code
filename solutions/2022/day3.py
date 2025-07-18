'''--- Day 3: Rucksack Reorganization ---'''

from pathlib import Path
from rich import print
import string
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day3_example.txt'
INPUT = DATA_DIR / '2022_day3_input.txt'

def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    return line_list

def split_rucksacks(line_list: list[str]) -> list[tuple[str, str]]:
    output_list = []
    for line in line_list:
        halfway_point = len(line) // 2
        pair = (line[0:(halfway_point)], line[(halfway_point):])
        output_list.append(pair)
        
    return output_list

def find_mistake(rucksack: tuple[str, str]) -> str:
    compartment1, compartment2 = rucksack
    intersection = set(compartment1) & set(compartment2)
    if len(intersection) > 1:
        raise ValueError
    
    return list(intersection)[0]


def group_rucksacks(line_list: list[str]) -> list[list[str]]:
    output_list = []
    while len(line_list) > 0:
        inner_list = []
        for _ in range(3):
            inner_list.append(line_list.pop(0))
        output_list.append(inner_list)
    return output_list

def find_badge(rucksack_list: list[str]) -> str:
    rucksack_set_list = [set(x) for x in rucksack_list]
    intersection = set.intersection(*rucksack_set_list)

    if len(intersection) != 1:
        raise ValueError(f"Intersection contains {len(intersection)} elements!")
    
    return list(intersection)[0]
    
      
def part_one(filename: Path) -> int:
    line_list = ingest_data(filename)
    rucksacks = split_rucksacks(line_list)
    mistakes = [find_mistake(x) for x in rucksacks]
    answer = sum((string.ascii_letters.find(mistake) + 1) for mistake in mistakes)
    return answer

def part_two(filename: Path) -> int:
    line_list = ingest_data(filename)
    groups = group_rucksacks(line_list)
    badges = [find_badge(group) for group in groups]
    answer = sum((string.ascii_letters.find(badge) + 1) for badge in badges)
    return answer
    

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # should be 157
    print(f"Part One (input):  {part_one(INPUT)}") # 
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # should be 70
    print(f"Part Two (input):  {part_two(INPUT)}") # 

if __name__ == '__main__':
    main()