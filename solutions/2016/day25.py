import pathlib
from dataclasses import dataclass
from typing import Callable, Optional

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

class InvalidClockSignal(Exception):
    pass

def dummy_func():
    raise NoValidFunction

@dataclass
class Instruction:
    name: str
    v1: str|int
    v2: Optional[str|int] = None

    @property
    def is_valid(self) -> bool:
        if self.name in ['inc', 'dec'] and self.v2:
            return False
        if self.name == 'cpy' and (not self.v2 or isinstance(self.v2, int)):
            return False
        return True

@dataclass
class Computer:
    program: list[Instruction]
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    ptr: int = 0
    clock_signal: str = ''

    def __post_init__(self):
        self.instructions_dict: dict[str, Callable] = {
            'cpy': self.cpy,
            'inc': self.inc,
            'dec': self.dec,
            'jnz': self.jnz,
            'tgl': self.tgl,
            'out': self.out,
        }

    def execute_program(self) -> None:
        ''' The program exits when it tries to run an instruction 
        beyond the ones defined. '''
        while True:
            if self.ptr >= len(self.program):
                break
            if len(self.clock_signal) > 50:
                break
            inst = self.program[self.ptr]
            if not inst.is_valid:
                self.ptr += 1
                continue
            func = self.get_instruction_func(inst.name)
            try:
                if inst.v1 is not None and inst.v2 is not None:
                    func(inst.v1, inst.v2)
                else:
                    func(inst.v1)
            except TypeError:
                print(f"Trying to execute {inst} at line {self.ptr}")
                raise
            
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

    def cpy(self, v: int|str, r: str):
        ''' copies v (either an integer or the value of a register) into register r '''
        value = v if isinstance(v, int) else self.get_register_value(v)
        self.set_register_value(r, value)
        self.ptr +=1

    def jnz(self, v: int|str, n: int|str):
        ''' jumps to an instruction n away (positive means forward; negative means backward), 
        but only if v (either an integer or the value of a register) is not zero. '''
        value = v if isinstance(v, int) else self.get_register_value(v)
        n = n if isinstance(n, int) else self.get_register_value(n)
        if value != 0:
            self.ptr += n
        else:
            self.ptr += 1

    def tgl(self, r: str):
        ''' tgl x toggles the instruction x away (pointing at instructions like jnz does: 
        positive means forward; negative means backward):
        - For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
        - For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
        - The arguments of a toggled instruction are not affected.
        - If an attempt is made to toggle an instruction outside the program, nothing happens.
        - If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later
        made to execute that instruction, skip it instead.
        - If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), 
        the resulting instruction is not executed until the next time it is reached. '''

        value = self.get_register_value(r)
        idx = self.ptr + value
        if idx < 0 or idx > (len(self.program) - 1):
            self.ptr += 1
            return
        
        inst_to_change = self.program[idx]
        match inst_to_change.name:
            case 'dec' | 'tgl':
                inst_to_change.name = 'inc'
            case 'inc':
                inst_to_change.name = 'dec'
            case 'cpy':
                inst_to_change.name = 'jnz'
            case 'jnz':
                inst_to_change.name = 'cpy'
        self.ptr += 1
        
    def out(self, v: int|str):
        ''' transmits v (either an integer or the value of a register) as the 
        next value for the clock signal. '''
        value = v if isinstance(v, int) else self.get_register_value(v)

        if value not in [0, 1] or self.clock_signal.endswith(str(value)):
            raise InvalidClockSignal

        self.clock_signal += str(value)
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

    n = 0
    while True:
        computer = parse_data(data)
        computer.a = n
        try:
            computer.execute_program()
        except InvalidClockSignal:
            n += 1
            continue
        else:
            print(computer.clock_signal)
            return n
        
def main():
    print(f"Part One (input):  {part_one(INPUT)}")

    random_tests()

def random_tests():
    ...
       
if __name__ == '__main__':
    main()