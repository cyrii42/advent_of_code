import pathlib
from copy import deepcopy

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '10000'
INPUT = aoc.get_input(YEAR, DAY)

def flip(char: str):
    return '0' if char == '1' else '1'

def apply_dragon_curve(data: str) -> str:
    a = data
    b = deepcopy(a)
    b = ''.join(flip(char) for char in reversed(b))
    return a + '0' + b

def generate_checksum(data: str) -> str:
    output_str = ''
    i = 0
    while i < (len(data) - 1):
        if data[i] + data[i+1] in ['00', '11']:
            output_str += '1'
        else:
            output_str += '0'
        i += 2
    if len(output_str) % 2 != 0:
        return output_str
    else:
        return generate_checksum(output_str)
    
def part_one(data: str):
    initial_state = data
    disk_length = 20 if data == EXAMPLE else 272

    state = initial_state
    while len(state) < disk_length:
        state = apply_dragon_curve(state)

    state = state[0:disk_length+1]
    return generate_checksum(state)
    
def part_two(data: str):
    initial_state = data
    disk_length = 35651584

    state = initial_state
    while len(state) < disk_length:
        state = apply_dragon_curve(state)

    state = state[0:disk_length+1]
    return generate_checksum(state)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()