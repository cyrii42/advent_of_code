import operator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, NamedTuple
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class Instruction(NamedTuple):
    reg_name: str
    func: Callable[[int, int], int]
    amt: int
    test_reg_name: str
    test_condition: Callable[[int, int], bool]
    test_amt: int

@dataclass
class Computer:
    instruction_list: list[Instruction]
    reg_dict: dict[str, int] = field(default_factory=dict)

    def get_registry_value(self, reg_name: str) -> int:
        if reg_name not in self.reg_dict:
            self.reg_dict[reg_name] = 0
        return self.reg_dict[reg_name]

    def set_registry_value(self, reg_name: str, value: int) -> None:
        self.reg_dict[reg_name] = value

    def apply_test(self, inst: Instruction) -> bool:
        test_reg_value = self.get_registry_value(inst.test_reg_name)
        return inst.test_condition(test_reg_value, inst.test_amt)

    def execute_instructions(self) -> int:
        highest_so_far = -99999999
        for inst in self.instruction_list:           
            if self.apply_test(inst):
                current_value = self.get_registry_value(inst.reg_name)
                new_value = inst.func(current_value, inst.amt)
                self.set_registry_value(inst.reg_name, new_value)
                highest_so_far = max(highest_so_far, current_value)
        return highest_so_far
                
    def solve_part_one(self) -> int:
        self.execute_instructions()
        return max(self.reg_dict.values())

    def solve_part_two(self) -> int:
        return self.execute_instructions()

def get_test_func(test_condition: str) -> Callable[[int, int], bool]:
    match test_condition:
        case '>':
            return operator.gt
        case '<':
            return operator.lt
        case '>=':
            return operator.ge
        case '<=':
            return operator.le
        case '!=':
            return operator.ne
        case '==':
            return operator.eq
        case _:
            raise ValueError

def parse_data(data: str) -> list[Instruction]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        reg_name, func, amt, _, test_reg_name, test_condition, test_amt = line.split(' ')
        output_list.append(Instruction(
                           reg_name=reg_name,
                           func=operator.add if func == 'inc' else operator.sub,
                           amt=int(amt),
                           test_reg_name=test_reg_name,
                           test_condition=get_test_func(test_condition),
                           test_amt=int(test_amt)))  
    return output_list
    
def part_one(data: str):
    instruction_list = parse_data(data)
    computer = Computer(instruction_list)
    return computer.solve_part_one()

def part_two(data: str):
    instruction_list = parse_data(data)
    computer = Computer(instruction_list)
    return computer.solve_part_two()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()