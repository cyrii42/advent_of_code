'''--- Day 2: Red-Nosed Reports ---'''

from pathlib import Path
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day2_example.txt'
INPUT = DATA_DIR / 'day2_input.txt'

def ingest_data(filename: Path) -> list[list[int]]:
    with open(filename, 'r') as f:
        lines = [line.strip('\n').split() for line in f.readlines()]
        
    output_list = []
    for line in lines:
        new_list = [int(num_str) for num_str in line]
        output_list.append(new_list)
    return output_list

def determine_safety_part_one(levels: list[int]) -> int:
    if len(levels) != len(set(levels)):
        return 0
    if (levels[0] < levels[1]) and (sorted(levels) != levels):
        return 0
    if (levels[0] > levels[1]) and (sorted(levels, reverse=True) != levels):
        return 0
    
    for i, x in enumerate(levels):
        if (i + 1) == len(levels):
            return 1
        if not 0 < abs(x - levels[i+1]) <= 3:
            return 0

    return 1

def determine_safety_part_two(levels: list[int]) -> int:
    if determine_safety_part_one(levels) == 1:
        return 1

    for i in range(len(levels)):
        new_levels = levels.copy()
        new_levels.pop(i)
        if determine_safety_part_one(new_levels) == 1:
            return 1

    return 0

   

def part_one():
    lines = ingest_data(INPUT)
    safety_checks = [determine_safety_part_one(line) for line in lines]
    answer = sum(safety_checks)
    return answer

def part_two():
    lines = ingest_data(INPUT)
    safety_checks = [determine_safety_part_two(line) for line in lines]
    answer = sum(safety_checks)
    return answer

def main():
    print(f"Part One:  {part_one()}")
    print(f"Part Two:  {part_two()}")

   

if __name__ == '__main__':
    main()