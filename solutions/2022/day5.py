'''--- Day 5: Supply Stacks ---'''

from pathlib import Path
from rich import print
from copy import deepcopy
from dataclasses import dataclass
from typing import NamedTuple
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day5_example.txt'
INPUT = DATA_DIR / '2022_day5_input.txt'

def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        
    return line_list

def process_drawing(line_list: list[str]) -> list[list[str]]:
    labels = [int(x) for x in line_list[-1].split()]
    num_stacks = len(labels)
    stack_row_list = line_list[:-1]

    stack_list_by_row = []
    for row in stack_row_list:
        inner_list = []
        for x in range(0, num_stacks):
            inner_list.append(row[1 + x*4])
        stack_list_by_row.append(inner_list)

    output_list = []
    for x in range(num_stacks):
        output_list.append([row[x] for row in stack_list_by_row if row[x] != ' '])
    
    return output_list

@dataclass
class Stack():
    num: int
    contents: list[str]

    @property
    def top_crate(self) -> str:
        return self.contents[0]

    def pop(self) -> str:
        return self.contents.pop(0)

    def push(self, item: str) -> None:
        self.contents.insert(0, item)

def create_stacks(stack_list_raw: list[list[str]]) -> list[Stack]:
    output_list = []
    for i, raw_stack in enumerate(stack_list_raw, start=1):
        output_list.append(Stack(i, raw_stack))
    return output_list

def get_stack(stack_list: list[Stack], num: int) -> Stack:
    return [stack for stack in stack_list if stack.num == num][0]

class Procedure(NamedTuple):
    origin: int
    destination: int
    quantity: int

def parse_procedure_list(procedure_str_list: list[str]) -> list[Procedure]:
    output_list = []
    for procedure_str in procedure_str_list:
        procedure_str_split = procedure_str.split()
        output_list.append(Procedure(origin=int(procedure_str_split[3]),
                                     destination=int(procedure_str_split[5]),
                                     quantity=int(procedure_str_split[1])
                                    ))
    return output_list

def execute_procedure_list(procedure_list: list[Procedure], stack_list: list[Stack]) -> list[Stack]:
    for procedure in procedure_list:
        origin_stack = get_stack(stack_list, procedure.origin)
        destination_stack = get_stack(stack_list, procedure.destination)
        for _ in range(procedure.quantity):
            destination_stack.push(origin_stack.pop())
    return stack_list

def execute_procedure_list_part_two(procedure_list: list[Procedure], stack_list: list[Stack]) -> list[Stack]:
    for procedure in procedure_list:
        origin_stack = get_stack(stack_list, procedure.origin)
        destination_stack = get_stack(stack_list, procedure.destination)
        crates = origin_stack.contents[0:procedure.quantity]
        for _ in range(procedure.quantity):
            origin_stack.pop()
        crates += (destination_stack.contents)
        destination_stack.contents = crates
    return stack_list

def part_one(filename: Path) -> str:
    line_list = ingest_data(filename)
    procedure_str_list = [line for line in line_list if 'move' in line]
    stack_list_raw = process_drawing([line for line in line_list if 'move' not in line and line != ''])
    stack_list = create_stacks(stack_list_raw)
    procedure_list = parse_procedure_list(procedure_str_list)
    new_stack_list = execute_procedure_list(procedure_list, stack_list)
    return(''.join(stack.top_crate for stack in new_stack_list))

def part_two(filename: Path) -> str:
    line_list = ingest_data(filename)
    procedure_str_list = [line for line in line_list if 'move' in line]
    stack_list_raw = process_drawing([line for line in line_list if 'move' not in line and line != ''])
    stack_list = create_stacks(stack_list_raw)
    procedure_list = parse_procedure_list(procedure_str_list)
    new_stack_list = execute_procedure_list_part_two(procedure_list, stack_list)
    return(''.join(stack.top_crate for stack in new_stack_list))

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # CMZ
    print(f"Part One (input):  {part_one(INPUT)}") # 
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # MCD
    print(f"Part Two (input):  {part_two(INPUT)}") # 

if __name__ == '__main__':
    main()