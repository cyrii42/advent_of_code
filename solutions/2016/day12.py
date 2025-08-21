import pathlib
from dataclasses import dataclass
from typing import Callable, NamedTuple, Optional

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

class NoValidFunction(Exception):
    pass

def dummy_func():
    raise NoValidFunction

class Instruction(NamedTuple):
    name: str
    v1: str|int
    v2: Optional[str|int] = None

@dataclass
class Computer:
    program: list[Instruction]
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    ptr: int = 0

    def __post_init__(self):
        self.instructions_dict: dict[str, Callable] = {
            'cpy': self.cpy,
            'inc': self.inc,
            'dec': self.dec,
            'jnz': self.jnz,
        }

    def execute_program(self) -> None:
        ''' The program exits when it tries to run an instruction 
        beyond the ones defined. '''
        while True:
            if self.ptr >= len(self.program):
                break
            inst = self.program[self.ptr]
            func = self.get_instruction_func(inst.name)
            if inst.v1 and inst.v2:
                func(inst.v1, inst.v2)
            else:
                func(inst.v1)
            
    def get_register_value(self, r: str):
        match r:
            case 'a':
                return self.a
            case 'b': 
                return self.b
            case 'c': 
                return self.c
            case 'd': 
                return self.d
            case _:
                raise ValueError

    def set_register_value(self, r: str, value: int):
         match r:
            case 'a':
                self.a = value
            case 'b': 
                self.b = value
            case 'c': 
                self.c = value
            case 'd': 
                self.d = value
            case _:
                raise ValueError

    def get_instruction_func(self, inst_name: str) -> Callable:
        return self.instructions_dict.get(inst_name, dummy_func)
            
    def cpy(self, v: int|str, r: str):
        ''' copies v (either an integer or the value of 
        a register) into register r '''
        value = v if isinstance(v, int) else self.get_register_value(v)
        self.set_register_value(r, value)
        self.ptr +=1

    def inc(self, r: str):
        ''' increases the value of register r by one '''
        value = self.get_register_value(r)
        self.set_register_value(r, value+1)
        self.ptr +=1

    def dec(self, r: str):
        ''' decreases the value of register r by one '''
        value = self.get_register_value(r)
        self.set_register_value(r, value-1)
        self.ptr +=1

    def jnz(self, v: int|str, n: int):
        ''' jumps to an instruction n away (positive means
        forward; negative means backward), but only if 
        v (either an integer or the value of a register) 
        is not zero. '''
        value = v if isinstance(v, int) else self.get_register_value(v)
        if value != 0:
            self.ptr += n
        else:
            self.ptr += 1
            
def parse_data(data: str) -> Computer:
    line_list = data.splitlines()

    output_list = []
    for line in line_list:
        parts = line.split(' ')
        name = parts[0]
        v1 = parts[1]
        if v1.isdigit():
            v1 = int(v1)
        elif v1[0] == '-':
            v1 = 0 - int(v1[1:])
            
        if len(parts) == 3:
            v2 = parts[2]
            if v2.isdigit():
                v2 = int(v2)
            elif v2[0] == '-':
                v2 = 0 - int(v2[1:])
            output_list.append(Instruction(name, v1, v2))
        else:
            output_list.append(Instruction(name, v1))
    return Computer(output_list)
    
def part_one(data: str):
    computer = parse_data(data)
    computer.execute_program()
    return computer.a

def part_two(data: str):
    computer = parse_data(data)
    computer.c = 1
    computer.execute_program()
    return computer.a

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
       
if __name__ == '__main__':
    main()