from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '1002,4,3,4,33'
INPUT = aoc.get_input(YEAR, DAY)

@dataclass
class Computer:
    program: list[int] = field(repr=False)
    input_num: int
    output_list: list[int] = field(default_factory=list)
    ptr: int = 0

    def __post_init__(self):
        self.opcode_dict: dict[int, Callable] = {
            1: self.add,
            2: self.mul,
            3: self.input,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            99: self.end_program,
        }

    def parse_instruction(self, instruction: int) -> tuple[Callable, int, int, int]:
        instruction_str = f"{instruction:05d}"
        opcode = int(instruction_str[3:])
        fn = self.opcode_dict[opcode]
        mode_c, mode_b, mode_a = [int(x) for x in list(instruction_str[0:3])]
        return (fn, mode_a, mode_b, mode_c)    

    def get_value(self, num: int, mode: int) -> int:
        return num if mode == 1 else self.program[num]   

    def execute_program(self):
        while True:
            inst = self.program[self.ptr]
            fn, mode_a, mode_b, _ = self.parse_instruction(inst)

            if fn == self.end_program:
                break
            elif fn in [self.add, self.mul, self.less_than, self.equals]:
                a, b, c = [self.program[self.ptr + x] for x in range(1, 4)]
                val_a = self.get_value(a, mode_a)
                val_b = self.get_value(b, mode_b)
                val_c = c  # Write parameters will never be in immediate mode
                fn(val_a, val_b, val_c)
                self.ptr += 4
            elif fn in [self.jump_if_true, self.jump_if_false]:
                a, b = [self.program[self.ptr + x] for x in range(1, 3)]
                val_a = self.get_value(a, mode_a)
                val_b = self.get_value(b, mode_b)
                fn(val_a, val_b)
            elif fn == self.input:
                a = self.program[self.ptr + 1]
                val_a = a
                fn(val_a)
                self.ptr += 2 
            elif fn == self.output:
                a = self.program[self.ptr + 1]
                val_a = self.get_value(a, mode_a)
                fn(val_a)
                self.ptr += 2    

    def add(self, a: int, b: int, c: int) -> None:
        ''' Adds together numbers read from two positions and stores
        the result in a third position'''
        
        self.program[c] = a + b

    def mul(self, a: int, b: int, c: int) -> None:
        ''' Multiplies numbers read from two positions and stores
        the result in a third position'''
        
        self.program[c] = a * b

    def input(self, a: int) -> None:
        ''' Takes a single integer as input and saves it to the position 
        given by its only parameter. For example, the instruction 3,50 would 
        take an input value and store it at address 50.'''
        
        self.program[a] = self.input_num

    def output(self, a: int) -> None:
        ''' Outputs the value of its only parameter. For example, the 
        instruction 4,50 would output the value at address 50. '''
        
        self.output_list.append(a)

    def jump_if_true(self, a: int, b: int) -> None:
        ''' If the first parameter is non-zero, sets the instruction pointer 
        to the value from the second parameter. Otherwise, does nothing. '''
        
        if a != 0:
            self.ptr = b
        else:
            self.ptr += 3

    def jump_if_false(self, a: int, b: int) -> None:
        ''' If the first parameter is zero, sets the instruction pointer 
        to the value from the second parameter. Otherwise, does nothing. '''
        
        if a == 0:
            self.ptr = b
        else:
            self.ptr += 3

    def less_than(self, a: int, b: int, c: int) -> None:
        ''' if the first parameter is less than the second parameter, stores 1 
        in the position given by the third parameter. Otherwise, stores 0. '''
        
        if a < b:
            self.program[c] = 1
        else:
            self.program[c] = 0

    def equals(self, a: int, b: int, c: int) -> None:
        ''' if the first parameter is equal to the second parameter, stores 1 
        in the position given by the third parameter. Otherwise, stores 0. '''
        
        if a == b:
            self.program[c] = 1
        else:
            self.program[c] = 0

    def end_program(self) -> None:
        pass

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
    comp = Computer(program, 1)
    comp.execute_program()
    return comp.output_list[-1]

def part_two(data: str):
    program = parse_data(data)
    comp = Computer(program, 5)
    comp.execute_program()
    return comp.output_list[-1]

def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()