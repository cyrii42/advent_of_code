from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
from collections import deque
from rich import print

import advent_of_code as aoc
from intcode import IntCode, Output, Halt

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '1002,4,3,4,33'
INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str) -> list[int]:
    output_list = []
    for num_str in data.split(','):
        if num_str[0] == '-':
            output_list.append(0 - int(num_str[1:]))
        else:
            output_list.append(int(num_str))
    return output_list
    
def part_one(data: str):
    program = parse_data(data)
    comp = IntCode(program, input_queue=deque([1]))
    while True:
        result = comp.execute_program()
        if isinstance(result, Halt):
            return result.value
    

def part_two(data: str):
    program = parse_data(data)
    comp = IntCode(program, input_queue=deque([5]))
    while True:
        result = comp.execute_program()
        if isinstance(result, Halt):
            return result.value

def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()