'''--- Day 10: Cathode-Ray Tube ---'''


import math
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Literal, NamedTuple, Optional, Self

from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day10_example.txt'
INPUT = DATA_DIR / '2022_day10_input.txt'    

PART_ONE_CYCLES = [20, 60, 100, 140, 180, 220]

TOTAL_PIXELS = 240
CRT_WIDTH = 40
CRT_HEIGHT = 6

PIXEL_ON = '#'
PIXEL_OFF = '.'

@dataclass
class CPU:
    instruction_set: list[str]
    value: int = 1
    cycle_count: int = 1
    value_list: list[int] = field(default_factory=list)
    pixel_str: str = field(default_factory=str)

    @property
    def pixel_position(self) -> int:
        return (self.cycle_count - 1) % CRT_WIDTH
    
    @property
    def sprite(self) -> tuple[int, int, int]:
        return (self.value-1, self.value, self.value+1)

    @property
    def next_pixel(self) -> str:
        return PIXEL_ON if self.pixel_position in self.sprite else PIXEL_OFF
    
    def set_register_value(self, instruction: str) -> None:
        if instruction == 'noop':
            if self.cycle_count in PART_ONE_CYCLES:
                self.value_list.append(self.value * self.cycle_count)
            self.cycle_count += 1
        else:
            for _ in range(2):
                if self.cycle_count in PART_ONE_CYCLES:
                    self.value_list.append(self.value * self.cycle_count)
                self.cycle_count += 1
            self.value += int(instruction.split()[1])

    def get_part_one_answer(self) -> int:
        for instruction in self.instruction_set:
            self.set_register_value(instruction)
        return sum(value for value in self.value_list)
            
    def render_crt_image(self):
        for instruction in self.instruction_set:
            if instruction == 'noop':
                self.pixel_str += self.next_pixel
                self.cycle_count += 1
            else:
                for _ in range(2):
                    self.pixel_str += self.next_pixel
                    self.cycle_count += 1
                self.value += int(instruction.split()[1])
                
        print()
        for x in range(CRT_WIDTH, TOTAL_PIXELS+1, CRT_WIDTH):
            print(self.pixel_str[x-40:x])
        print()
                


def ingest_data(filename: Path):
    with open(filename) as f:
        line_list = [line.strip('\n')for line in f.readlines()]
    return line_list

def part_one(filename: Path):
    instruction_set = ingest_data(filename)
    cpu = CPU(instruction_set)
    return cpu.get_part_one_answer()

def part_two(filename: Path):
    instruction_set = ingest_data(filename)
    cpu = CPU(instruction_set)
    cpu.render_crt_image()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 
    print(f"Part One (input):  {part_one(INPUT)}") # 
    
    print(f"Part Two (example):  {part_two(EXAMPLE)}") #
    print(f"Part Two (input):  {part_two(INPUT)}") #

    random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()
