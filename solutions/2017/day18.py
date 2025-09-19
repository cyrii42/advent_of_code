import pathlib
from dataclasses import dataclass, field
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

def dummy_func():
    raise NoValidFunction

@dataclass
class Instruction:
    name: str
    v1: str|int
    v2: Optional[str|int] = None

    # @property
    # def is_valid(self) -> bool:
    #     if self.name in ['inc', 'dec'] and self.v2:
    #         return False
    #     if self.name == 'cpy' and (not self.v2 or isinstance(self.v2, int)):
    #         return False
    #     return True

@dataclass
class Computer:
    program: list[Instruction]
    ptr: int = 0
    register_dict: dict[str, int] = field(default_factory=dict)
    instructions_dict: dict[str, Callable] = field(
        default_factory=dict, repr=False)
    sounds_played: list[int] = field(default_factory=list)
    sound_recovered: bool = False

    @property
    def last_sound_played(self) -> int:
        return self.sounds_played[-1]

    def __post_init__(self):
        self.instructions_dict: dict[str, Callable] = {
            'snd': self.snd,
            'set': self.set,
            'add': self.add,
            'mul': self.mul,
            'mod': self.mod,
            'rcv': self.rcv,
            'jgz': self.jgz
        }

    def solve_part_one(self) -> int:
        ''' The program exits when it tries to run an instruction 
        beyond the ones defined. '''
        while self.ptr < len(self.program):
            inst = self.program[self.ptr]
            func = self.get_instruction_func(inst.name)
            try:
                if inst.v1 is not None and inst.v2 is not None:
                    func(inst.v1, inst.v2)
                else:
                    func(inst.v1)
            except TypeError:
                print(f"Trying to execute {inst} at line {self.ptr}")
                raise
            if self.sound_recovered:
                return self.last_sound_played
        return -9999999

    def solve_part_two(self) -> int:
        ...
            
    def get_register_value(self, r: str) -> int:
        return self.register_dict.get(r, 0)

    def set_register_value(self, r: str, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        self.register_dict[r] = value

    def get_instruction_func(self, inst_name: str) -> Callable:
        try:
            return self.instructions_dict[inst_name]
        except KeyError:
            raise NoValidFunction(f"Could not find instruction {inst_name}")

    def snd(self, x: int) -> None:
        ''' plays a sound with a frequency equal to the value of X '''
        x_value = x if isinstance(x, int) else self.get_register_value(x)
        self.sounds_played.append(x_value)
        self.ptr += 1

    def set(self, x: str, y: int) -> None:
        ''' sets register X to the value of Y '''
        y_value = y if isinstance(y, int) else self.get_register_value(y)
        self.set_register_value(x, y_value)
        self.ptr += 1

    def add(self, x: str, y: str|int) -> None:
        ''' increases register X by the value of Y '''
        x_value = self.get_register_value(x)
        y_value = y if isinstance(y, int) else self.get_register_value(y)
        new_value = x_value + y_value
        self.set_register_value(x, new_value)
        self.ptr += 1
        
    def mul(self, x: str, y: str|int) -> None:
        ''' sets register X to the result of multiplying the value 
        contained in register X by the value of Y '''
        x_value = self.get_register_value(x)
        y_value = y if isinstance(y, int) else self.get_register_value(y)
        new_value = x_value * y_value
        self.set_register_value(x, new_value)
        self.ptr += 1

    def mod(self, x: str, y: str|int) -> None:
        ''' sets register X to the remainder of dividing the 
        value contained in register X by the value of Y (that is, 
        it sets X to the result of X modulo Y) '''
        x_value = self.get_register_value(x)
        y_value = y if isinstance(y, int) else self.get_register_value(y)
        new_value = x_value % y_value
        self.set_register_value(x, new_value)
        self.ptr += 1
        
    def rcv(self, x: str|int) -> int | None:
        ''' recovers the frequency of the last sound played, but only 
        when the value of X is not zero. (If it is zero, the command 
        does nothing) '''
        x_value = x if isinstance(x, int) else self.get_register_value(x)
        if x_value != 0:
            self.sound_recovered = True
        self.ptr += 1
        
    def jgz(self, x: str|int, y: str|int):
        ''' jumps with an offset of the value of Y, but only if the 
        value of X is greater than zero. (An offset of 2 skips the 
        next instruction, an offset of -1 jumps to the previous 
        instruction, and so on) '''
        x_value = x if isinstance(x, int) else self.get_register_value(x)
        y_value = y if isinstance(y, int) else self.get_register_value(y)
        if x_value > 0:
            self.ptr += y_value
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
    return computer.solve_part_one()

def part_two(data: str):
    computer = parse_data(data)
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