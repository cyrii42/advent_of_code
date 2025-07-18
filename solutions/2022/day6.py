'''--- Day 6: Tuning Trouble ---'''

from pathlib import Path
from rich import print
from copy import deepcopy
from dataclasses import dataclass
from typing import NamedTuple
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day6_example.txt'
INPUT = DATA_DIR / '2022_day6_input.txt'

def ingest_data(filename: Path) -> str:
    with open(filename, 'r') as f:
        return f.read()

def find_start_of_packet_marker(data: str) -> int:
    for i in range(len(data)):
        if i < 3:
            continue
        test_chars = data[i-3:i+1]
        if len(test_chars) == len(set(test_chars)):
            return i+1
    return 0

def find_start_of_message_marker(data: str) -> int:
    for i in range(len(data)):
        if i < 13:
            continue
        test_chars = data[i-13:i+1]
        if len(test_chars) == len(set(test_chars)):
            return i+1
    return 0

def part_one(filename: Path):
    data = ingest_data(filename)
    return find_start_of_packet_marker(data)

def part_two(filename: Path):
    data = ingest_data(filename)
    return find_start_of_message_marker(data)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 7
    print(f"Part One (input):  {part_one(INPUT)}") # 
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # 19
    print(f"Part Two (input):  {part_two(INPUT)}") # 

    # random_tests()


def random_tests():
    asdf = 'abcdefghijk'
    print(asdf[0:3])

if __name__ == '__main__':
    main()