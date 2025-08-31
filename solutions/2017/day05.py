from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

@dataclass
class Computer:
    instructions: list[int]
    ptr: int = 0

    def execute_instructions(self, part_two: bool = False) -> int:
        count = 0
        while self.ptr < len(self.instructions):
            prev_pointer = deepcopy(self.ptr)
            self.ptr += self.instructions[self.ptr]
            if part_two and self.instructions[prev_pointer] >= 3:
                self.instructions[prev_pointer] -= 1
            else:
                self.instructions[prev_pointer] += 1
            count +=1
        return count

def parse_data(data: str) -> Computer:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        if line.startswith('-'):
            output_list.append(0 - int(line[1:]))
        else:
            output_list.append(int(line))
    return Computer(output_list)
    
def part_one(data: str):
    computer = parse_data(data)
    return computer.execute_instructions()

def part_two(data: str):
    computer = parse_data(data)
    return computer.execute_instructions(part_two=True)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

       
if __name__ == '__main__':
    main()