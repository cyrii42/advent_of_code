import itertools
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

NUM_REGISTERS = 6

class NoValidFunction(Exception):
    pass

def dummy_func():
    raise NoValidFunction

class Instruction(NamedTuple):
    opcode: str
    input_a: int
    input_b: int
    output: int
    
@dataclass
class Computer:
    ptr_register: int
    instructions: list[Instruction] = field(repr=True)
    ptr: int = 0
    register_dict: dict[int, int] = field(init=False)
    opcode_list: list[Callable] = field(repr=False, 
                                             default_factory=list)
    opcode_dict: dict[str, Callable] = field(repr=False, 
                                             default_factory=dict)
    part_two: bool = False

    def __post_init__(self):
        self.register_dict = {num: 0 for num in range(6)}
        if self.part_two:
            self.register_dict[0] = 1
        self.opcode_list = [
            self.addr, self.addi, self.mulr, self.muli, self.banr, self.bani, 
            self.borr, self.bori, self.setr, self.seti, self.gtir, self.gtri, 
            self.gtrr, self.eqir, self.eqri, self.eqrr
        ]
        self.opcode_dict = {func.__name__: func for func in self.opcode_list}

    def get_opcode_func(self, opcode: str) -> Callable:
        return self.opcode_dict.get(opcode, dummy_func)

    def execute_instructions(self):
        while self.ptr < len(self.instructions):
            inst = self.instructions[self.ptr]
            opcode, a, b, c = inst
            func = self.get_opcode_func(opcode)
    
            self.set_ptr_register(self.ptr)         
            func(a, b, c)
            self.ptr = self.get_ptr_register()
            self.ptr += 1
            
        return self.get_register_value(0)

    def get_register_value(self, reg_num: int) -> int:
        assert len(self.register_dict) == NUM_REGISTERS
        assert isinstance(reg_num, int)
        assert 0 <= reg_num < NUM_REGISTERS
        
        return self.register_dict[reg_num]

    def set_ptr_register(self, value: int) -> None:
        self.set_register_value(self.ptr_register, value)

    def get_ptr_register(self) -> int:
        return self.get_register_value(self.ptr_register)

    def set_register_value(self, reg_num: int, value: int) -> None:
        assert len(self.register_dict) == NUM_REGISTERS
        assert isinstance(reg_num, int)
        assert 0 <= reg_num < NUM_REGISTERS
        assert isinstance(value, int)
        
        self.register_dict[reg_num] = value

    def get_all_registers(self) -> list[int]:
        assert len(self.register_dict) == NUM_REGISTERS

        return [v for v in self.register_dict.values()]
        
    def set_all_registers(self, reg_values: list[int]) -> None:
        assert len(self.register_dict) == NUM_REGISTERS
        assert len(reg_values) == NUM_REGISTERS
        assert all(isinstance(x, int) for x in reg_values)

        for reg_num, value in enumerate(reg_values):
            self.set_register_value(reg_num, value)

    '''
    In the opcode descriptions below, if something says "value A", it means 
    to take the number given as A literally. (This is also called an "immediate" 
    value.) If something says "register A", it means to use the number given as A 
    to read from (or write to) the register with that number.
    '''
    
    ### ADDITION ###
    def addr(self, a: int, b: int, c: int) -> None:
        ''' addr (add register) stores into register C the result 
        of adding register A and register B. '''
        reg_a = self.get_register_value(a)
        reg_b = self.get_register_value(b)
        output_value = reg_a + reg_b
        self.set_register_value(c, output_value)
        
    def addi(self, a: int, b: int, c: int) -> None:
        ''' addi (add immediate) stores into register C the result
        of adding register A and value B. '''
        reg_a = self.get_register_value(a)
        output_value = reg_a + b
        self.set_register_value(c, output_value)

    ### MULTIPLICATION ###
    def mulr(self, a: int, b: int, c: int) -> None:
        ''' mulr (multiply register) stores into register C the result 
        of multiplying register A and register B. '''
        reg_a = self.get_register_value(a)
        reg_b = self.get_register_value(b)
        output_value = reg_a * reg_b
        self.set_register_value(c, output_value)
        
    def muli(self, a: int, b: int, c: int) -> None:
        ''' muli (multiply immediate) stores into register C the result 
        of multiplying register A and value B. '''
        reg_a = self.get_register_value(a)
        output_value = reg_a * b
        self.set_register_value(c, output_value)

    ### BITWISE AND ###
    def banr(self, a: int, b: int, c: int) -> None:
        ''' banr (bitwise AND register) stores into register C the result 
        of the bitwise AND of register A and register B. '''
        reg_a = self.get_register_value(a)
        reg_b = self.get_register_value(b)
        output_value = reg_a & reg_b
        self.set_register_value(c, output_value)
        
    def bani(self, a: int, b: int, c: int) -> None:
        ''' bani (bitwise AND immediate) stores into register C the result 
        of the bitwise AND of register A and value B. '''
        reg_a = self.get_register_value(a)
        output_value = reg_a & b
        self.set_register_value(c, output_value)

    ### BITWISE OR ###
    def borr(self, a: int, b: int, c: int) -> None:
        ''' borr (bitwise OR register) stores into register C the result 
        of the bitwise OR of register A and register B. '''
        reg_a = self.get_register_value(a)
        reg_b = self.get_register_value(b)
        output_value = reg_a | reg_b
        self.set_register_value(c, output_value)
        
    def bori(self, a: int, b: int, c: int) -> None:
        ''' bori (bitwise OR immediate) stores into register C the result 
        of the bitwise OR of register A and value B. '''
        reg_a = self.get_register_value(a)
        output_value = reg_a | b
        self.set_register_value(c, output_value)

    ### ASSIGNMENT ###
    def setr(self, a: int, b: int, c: int) -> None:
        ''' setr (set register) copies the contents of register A into 
        register C. (Input B is ignored.) '''
        reg_a = self.get_register_value(a)
        output_value = reg_a
        self.set_register_value(c, output_value)
        
    def seti(self, a: int, b: int, c: int) -> None:
        ''' seti (set immediate) stores value A into register C. 
        (Input B is ignored.) '''
        output_value = a
        self.set_register_value(c, output_value)

    ### GREATER-THAN TESTING ###
    def gtir(self, a: int, b: int, c: int) -> None:
        ''' gtir (greater-than immediate/register) sets register C to 1 if value A 
        is greater than register B. Otherwise, register C is set to 0. '''
        reg_b = self.get_register_value(b)
        output_value = 1 if a > reg_b else 0
        self.set_register_value(c, output_value)
        
    def gtri(self, a: int, b: int, c: int) -> None:
        ''' gtri (greater-than register/immediate) sets register C to 1 if register A 
        is greater than value B. Otherwise, register C is set to 0. '''
        reg_a = self.get_register_value(a)
        output_value = 1 if reg_a > b else 0
        self.set_register_value(c, output_value)
        
    def gtrr(self, a: int, b: int, c: int) -> None:
        ''' gtrr (greater-than register/register) sets register C to 1 if register A 
        is greater than register B. Otherwise, register C is set to 0. '''
        reg_a = self.get_register_value(a)
        reg_b = self.get_register_value(b)
        output_value = 1 if reg_a > reg_b else 0
        self.set_register_value(c, output_value)

    ### EQUALITY TESTING ###
    def eqir(self, a: int, b: int, c: int) -> None:
        ''' eqir (equal immediate/register) sets register C to 1 if value A is equal 
        to register B. Otherwise, register C is set to 0. '''
        reg_b = self.get_register_value(b)
        output_value = 1 if a == reg_b else 0
        self.set_register_value(c, output_value)
        
    def eqri(self, a: int, b: int, c: int) -> None:
        ''' eqri (equal register/immediate) sets register C to 1 if register A is equal 
        to value B. Otherwise, register C is set to 0. '''
        reg_a = self.get_register_value(a)
        output_value = 1 if reg_a == b else 0
        self.set_register_value(c, output_value)
        
    def eqrr(self, a: int, b: int, c: int) -> None:
        ''' eqrr (equal register/register) sets register C to 1 if register A is equal 
        to register B. Otherwise, register C is set to 0. '''
        reg_a = self.get_register_value(a)
        reg_b = self.get_register_value(b)
        output_value = 1 if reg_a == reg_b else 0
        self.set_register_value(c, output_value)



def parse_test(test_str: str) -> Instruction:
    parts = test_str.split(' ')
    opcode = parts[0]
    a, b, c = [int(x) for x in parts[1:]]
    return Instruction(opcode, a, b, c)

def parse_data(data: str) -> tuple[int, list[Instruction]]:
    line_list = data.splitlines()

    ptr_register = int(line_list[0].split(' ')[1])
    
    instructions = [parse_test(line) for line in line_list[1:] if line]
    return (ptr_register, instructions)

def part_one(data: str):
    ptr_register, instructions = parse_data(data)
    comp = Computer(ptr_register, instructions)
    comp.execute_instructions()
    return comp.register_dict[0]

'''
# ip 2              # reg_2 = pointer register

0  addi 2 16 2      # reg_2 = reg_2 + 16 (JUMP to 17)

MAIN
1  seti 1 1 1       # reg_1 = 1    
2  seti 1 4 3       # reg_3 = 1
3  mulr 1 3 5       # reg_5 = reg_1 * reg_3
4  eqrr 5 4 5       # reg_5 = 1 if reg_5 == reg_4 else 0
5  addr 5 2 2       # reg_2 = reg_5 + reg_2
6  addi 2 1 2       # reg_2 += 1
7  addr 1 0 0       # reg_0 = reg_1 + reg_0
8  addi 3 1 3       # reg_3 += 1
9  gtrr 3 4 5       # reg_5 = 1 if reg_3 > reg_4 else 0
10 addr 2 5 2       # reg_2 = reg_2 + reg_5
11 seti 2 4 2       # reg_2 = 2
12 addi 1 1 1       # reg_1 += 1
13 gtrr 1 4 5       # reg_5 = 1 if reg_1 > reg_4 else 0
14 addr 5 2 2       # reg_2 = reg_5 + reg_2
15 seti 1 0 2       # reg_2 = 1
16 mulr 2 2 2       # reg_2 = reg_2 * reg_2     # HALT???

SETUP
17 addi 4 2 4       # reg_4 += 2                # reg_4 = 2
18 mulr 4 4 4       # reg_4 = reg_4 * reg_4     # reg_4 = 4
19 mulr 2 4 4       # reg_4 = reg_4 * reg_2     # reg_4 * reg_2 = 4 * 19 = 76
20 muli 4 11 4      # reg_4 = reg_4 * 11        # reg_4 = 836
21 addi 5 1 5       # reg_5 += 1                # reg_5 = 1
22 mulr 5 2 5       # reg_5 = reg_5 * reg_2     # reg_5 = 22
23 addi 5 17 5      # reg_5 += 17               # reg_5 = 39
24 addr 4 5 4       # reg_4 += reg_5            # reg_4 + reg_5 = 836 + 39 = 875
25 addr 2 0 2       # reg_2 += reg_0  (if reg_0 == 0, go to main; else go to PART 2)
26 seti 0 9 2       # reg_2 = 0  (sets pointer to 0, which goes to 1)

PART 2
27 setr 2 3 5       # reg_5 = reg_2             # reg_5 = 27
28 mulr 5 2 5       # reg_5 = reg_5 * reg_2     # 27 * 28 = 756
29 addr 2 5 5       # reg_5 += reg_2            # 756 + 29 = 785
30 mulr 2 5 5       # reg_5 = reg_2 * reg_5     # 785 * 30 = 23550
31 muli 5 14 5      # reg_5 = reg_5 * 14        # 23550 * 14 = 329700
32 mulr 5 2 5       # reg_5 = reg_5 * reg_2     # 329700 * 32 = 10550400
33 addr 4 5 4       # reg_4 += reg_5            # 875 + 10550400 = 10551275
34 seti 0 9 0       # reg_0 = 0
35 seti 0 6 2       # reg_2 = 0  (GO TO)
 '''

def part_two(data: str):
    ''' https://nbviewer.org/github/mjpieters/adventofcode/blob/master/2018/D ay%2019.ipynb '''
    def sum_factors(n: int) -> int:
        return sum(
            set(
                itertools.chain.from_iterable(
                    (i, n // i) for i in range(1, int(n**0.5) + 1) if not n % i
                )
            )
        )

    return sum_factors(10551275)

def main():
    print(f"Part One (input):  {part_one(EXAMPLE)}")   
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()