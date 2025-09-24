import pathlib
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Callable, Optional

from alive_progress import alive_bar
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

    def __repr__(self) -> str:
        return f"{self.name} {self.v1} {self.v2}"

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

    def solve_part_two(self) -> int:
        ''' Whoever wrote this program obviously didn't choose a very efficient 
        implementation. You'll need to optimize the program if it has any hope 
        of completing before Santa needs that printer working.

        After setting register a to 1, if the program were to run to completion, 
        what value would be left in register h?


        NOTES:
        - to end the program, G has to be 0
        - which means G has to be 122700 (the seemingly constant value of C)
        - 
        - so, what happens to G during the program?
            - lines:
                00 set b 57          set B to 57
                01 set c b           set C to 57
                02 jnz a 2           jump 2 lines if A != 0
                03 jnz 1 5           SKIPPED
                04 mul b 100         multiply B by 100 (to 5700?)
                05 sub b -100000     add 100_000 to B
                06 set c b           set C to the value of B (always 105700?)
                07 sub c -17000      add 17_000 to C 
                08 set f 1           set F to 1
                09 set d 2           set D to 2
                10 set e 2           set E to 2
                11 set g d           set G to the value of D (slowly increasing by 1)
                12 mul g e           multiply G is multiplied by the value of E (fluctuating, not sure how)
                13 sub g b           subtract the value of B (always 105700) from G
                14 jnz g 2           jump forward 2 if G != 0
                15 set f 0           SKIPPED, except when we're escaping the 11-19 loop
                16 sub e -1          add 1 to E
                17 set g e           set G to the value of E (fluctuating, not sure how)
                18 sub g b           subtract the value of B (always 105700) from G
                19 jnz g -8          jump back 8 lines if G != 0 (back to #11, "set g d")
                20 sub d -1          add 1 to D
                21 set g d           set G to the value of D (slowly increasing by 1)
                22 sub g b           subtract the value of B (always 105700) from G
                23 jnz g -13         jump back 13 lines if G != 0 (to #10, "set e 2")
                24 jnz f 2           jump forward 2 if f != 0 (to #26, "set g b")
                25 sub h -1          ***** add 1 to H ******
                26 set g b           set G to the value of B (always 105700)
                27 sub g c           subtract the value of C (always 122700) from G
                28 jnz g 2           jump forward 2 lines if G != 0 (to #30, "sub b -17")
                29 jnz 1 3           ***** jump 3 lines if 1 != 0 **** ****END PROGRAM*****
                30 sub b -17         add 17 to B
                31 jnz 1 -23         jump back 23 lines if 1 != 0 (to "#08, set f 1")

        looks like it's looping #11 through #19:
                11 set g d           set G to the value of D (slowly increasing by 1)
                12 mul g e           multiply G is multiplied by the value of E (increasing by 1 every loop)
                13 sub g b           subtract the value of B (always 105700) from G
                14 jnz g 2           jump forward 2 if G != 0
                SKIPPED
                16 sub e -1          add 1 to E
                17 set g e           set G to the value of E (increasing by 1 every loop)
                18 sub g b           subtract the value of B (always 105700) from G
                19 jnz g -8          jump back 8 lines if G != 0 (back to "set g d")
        - eventually, after 845,594 instructions (105,700 loops?), G = 0
        - so we go on to #20 (sub d -1), which adds 1 to D
        - then #21 (set g d), which sets G to this newly incremented value of D
        - then #22 (sub g b), which subtracts B (105,700) from G
        - then #23 (jnz g -13), which jumps back to #10 (set e 2), and we start another 11-19 loop again
        - SO:  in order for G to still be 0 at #23, D has to be 105,700 (the value of B)
        - at that point, f != 0 (because we just escaped a 11-19 loop), which means we add 1 to H
        - 
        


        '''
        
        # while self.ptr < len(self.program):
        for i in range(105700*8+100):
            if i % 10000 == 0 or i > 800_000:
                self.execute_next_instruction(print_info=True)
            else:
                self.execute_next_instruction(print_info=False)
            if self.register_dict['g'] == 0:
                print(f"Execution #{i+1}")
            # if i % 100_000 == 0:
            # print(self.register_dict)
        return self.register_dict['h']

    def execute_next_instruction(self, print_info: bool = False) -> None:
        if self.awaiting_input and not self.input_queue:
            raise AwaitingInput
        
        inst = self.program[self.ptr]
        func = self.get_instruction_func(inst.name)
        pre_inst_ptr = self.ptr
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
        if print_info:
            print(f"Ptr @ {pre_inst_ptr} - {inst} - {self.register_dict}")
            
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
    # print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
        
       
if __name__ == '__main__':
    main()