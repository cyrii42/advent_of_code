'''--- Day 3: Binary Diagnostic ---'''

import math
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from operator import add, mul
from pathlib import Path
from typing import Literal, NamedTuple, Optional, Self

from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2021_day3_example.txt'
INPUT = DATA_DIR / '2021_day3_input.txt'

def find_most_common_bit(nums: list[str]) -> str:
    num_zeroes = len([num for num in nums if num == '0'])
    num_ones = len([num for num in nums if num == '1'])
    if num_zeroes > num_ones:
        return '0'
    else:
        return '1'

def find_least_common_bit(nums: list[str]) -> str:
    num_zeroes = len([num for num in nums if num == '0'])
    num_ones = len([num for num in nums if num == '1'])
    if num_zeroes <= num_ones:
        return '0'
    else:
        return '1'

def calculate_gamma_rate(line_list: list[str]) -> int:
    num_bits = len(line_list[0])

    output_str = ''
    for i in range(num_bits):
        nums = [line[i] for line in line_list]
        output_str = output_str + find_most_common_bit(nums)
    return int(output_str, 2)

def calculate_epsilon_rate(line_list: list[str]) -> int:
    num_bits = len(line_list[0])

    output_str = ''
    for i in range(num_bits):
        nums = [line[i] for line in line_list]
        output_str = output_str + find_least_common_bit(nums)
    return int(output_str, 2)

def calculate_oxygen_rating(line_list: list[str]) -> int:
    num_bits = len(line_list[0])

    for i in range(num_bits):
        if len(line_list) == 1:
            break
        nums = [line[i] for line in line_list]
        most_common = find_most_common_bit(nums)
        line_list = [line for line in line_list if line[i] == most_common]
    
    return int(line_list[0], 2)
    
def calcluate_CO2_rating(line_list: list[str]) -> int:
    num_bits = len(line_list[0])

    for i in range(num_bits):
        if len(line_list) == 1:
            break
        nums = [line[i] for line in line_list]
        least_common = find_least_common_bit(nums)
        line_list = [line for line in line_list if line[i] == least_common]
    
    return int(line_list[0], 2)

def ingest_data(filename: Path):
    with open(filename) as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    return line_list

def part_one(filename: Path):
    line_list = ingest_data(filename)
    gamma_rate = calculate_gamma_rate(line_list)
    epsilon_rate = calculate_epsilon_rate(line_list)
    return gamma_rate * epsilon_rate

def part_two(filename: Path):
    line_list = ingest_data(filename)
    oxygen_rating = calculate_oxygen_rating(line_list)
    CO2_rating = calcluate_CO2_rating(line_list)
    return oxygen_rating * CO2_rating

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 198
    print(f"Part One (input):  {part_one(INPUT)}") # 
    
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # 230
    print(f"Part Two (input):  {part_two(INPUT)}") # 

    random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()