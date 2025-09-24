import pathlib
from collections import defaultdict, deque
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

class AwaitingInput(Exception):
    pass

class NewOutput(Exception):
    pass

@dataclass
class Instruction:
    name: str
    v1: str|int
    v2: Optional[str|int] = None

@dataclass
class Computer:
    program: list[Instruction]
    debug_mode: bool = False
    register_dict: defaultdict[str, int] = field(init=False)
    ptr: int = 0
    instructions_dict: dict[str, Callable] = field(
        default_factory=dict, repr=False)
    sounds_played: list[int] = field(default_factory=list)
    sound_recovered: bool = False
    output_queue: deque[int] = field(init=False)
    input_queue: deque[int] = field(default_factory=deque)
    values_sent: int = 0
    part_two: bool = False
    awaiting_input: bool = False
    num_mul_invocations: int = 0

    @property
    def last_sound_played(self) -> int:
        return self.sounds_played[-1]

    def __post_init__(self):
        self.register_dict = defaultdict(int)
        self.instructions_dict: dict[str, Callable] = {
            'snd': self.snd,
            'set': self.set,
            'add': self.add,
            'sub': self.sub,
            'mul': self.mul,
            'mod': self.mod,
            'rcv': self.rcv,
            'jnz': self.jnz,
            'jgz': self.jgz
        }
        if self.debug_mode:
            self.register_dict['a'] = 1

    def solve_part_one(self) -> int:
        while self.ptr < len(self.program):
            self.execute_next_instruction()
        return self.num_mul_invocations

    def execute_next_instruction(self) -> None:
        if self.awaiting_input and not self.input_queue:
            raise AwaitingInput
        
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
        if func == self.mul:
            self.num_mul_invocations += 1
            
    def get_register_value(self, r: str) -> int:
        return self.register_dict.get(r, 0)

    def set_register_value(self, r: str, value: int) -> None:
        self.register_dict[r] = value

    def get_instruction_func(self, inst_name: str) -> Callable:
        return self.instructions_dict.get(inst_name, dummy_func)

    def snd(self, x: int) -> None:
        ''' PART ONE: plays a sound with a frequency equal to the value of X

        PART TWO: sends the value of X to the other program '''
        x_value = x if isinstance(x, int) else self.get_register_value(x)
        if self.part_two:
            self.output_queue.append(x_value)
            self.ptr += 1
            self.values_sent += 1
            raise NewOutput
        else:
            self.sounds_played.append(x_value)
        self.ptr += 1

    def rcv(self, x: str|int) -> int | None:
        ''' PART ONE: recovers the frequency of the last sound played, but only 
        when the value of X is not zero. (If it is zero, the command 
        does nothing)

        PART TWO: receives the next value and stores it in register X '''
        if self.part_two:
            try:
                assert isinstance(x, str)
                value = self.input_queue.popleft()
                self.set_register_value(x, value)
                self.ptr += 1
            except IndexError:
                self.awaiting_input = True
                return
        else:
            x_value = x if isinstance(x, int) else self.get_register_value(x)
            if x_value != 0:
                self.sound_recovered = True
            self.ptr += 1

    def set(self, x: str, y: int) -> None:
        ''' sets register X to the value of Y '''
        y_value = y if isinstance(y, int) else self.get_register_value(y)
        self.set_register_value(x, y_value)
        self.ptr += 1

    def sub(self, x: str, y: int) -> None:
        ''' decreases register X by the value of Y '''
        x_value = self.get_register_value(x)
        y_value = y if isinstance(y, int) else self.get_register_value(y)
        new_value = x_value - y_value
        self.set_register_value(x, new_value)
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

    def jnz(self, x: str|int, y: str|int):
        ''' jumps with an offset of the value of Y, but only if the 
        value of X is not zero. (An offset of 2 skips the next instruction, 
        an offset of -1 jumps to the previous instruction, and so on.) '''
        x_value = x if isinstance(x, int) else self.get_register_value(x)
        y_value = y if isinstance(y, int) else self.get_register_value(y)
        if x_value != 0:
            self.ptr += y_value
        else:
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
        
def parse_data(data: str) -> list[Instruction]:
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
    return output_list
    
def part_one(data: str):
    instruction_list = parse_data(data)
    computer = Computer(instruction_list)
    return computer.solve_part_one()

def part_two(data: str):
    instruction_list = parse_data(data)
    computer = Computer(instruction_list, debug_mode=True)
    return computer.solve_part_two()
        
def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
        
       
if __name__ == '__main__':
    main()