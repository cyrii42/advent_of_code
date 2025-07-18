'''--- Day 17: Chronospatial Computer ---'''

import functools
import itertools
import math
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from pprint import pprint
from string import ascii_letters
from typing import Callable, NamedTuple, Optional, Protocol

import numpy as np
import pandas as pd
from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day17_example.txt'
INPUT = DATA_DIR / 'day17_input.txt'

class NoValidFunction(Exception):
    pass

def dummy_func():
    raise NoValidFunction

@dataclass
class Computer:
    program: list[int] = field(repr=False)
    reg_a: int
    reg_b: int
    reg_c: int
    pointer: int = field(repr=False, default=0)
    output: list[int] = field(default_factory=list)

    def __post_init__(self):
        self.original_registers = (self.reg_a, self.reg_b, self.reg_c)
        self.instructions_dict: dict[int, Callable] = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }

    def reset(self):
        self.reg_a, self.reg_b, self.reg_c = self.original_registers
        self.output = list()

    def check_new_reg_a_value(self, value: int) -> bool:
        self.reset()
        self.reg_a = value
        self.execute_program()
        return self.output == self.program

    def get_output_str(self) -> str:
        output_str = ''
        for x in self.output:
            output_str = output_str + str(x) + ','
        return output_str.removesuffix(',')

    '''
0: divide reg_a by (2**combo_op), store in reg_a
1: calculate reg_B XOR literal_op, store in reg_b
2: calculate combo_op MOD 8, store in reg_b
3: halt if reg_a is 0, else set pointer to literal_op
4: calculate reg_b XOR reg_c, store in reg_b
5: OUTPUT combo_op MOD 8
6: divide reg_a by (2**combo_op), store in reg_b
7: divide reg_a by (2**combo_op), store in reg_c

Register A: 46323429
Register B: 0
Register C: 0

Program: 2,4,  Reg B = Reg A MOD 8
         1,1,  Reg B = Reg B XOR 1
         7,5,  Reg C = Reg A / (2**Reg B)
         1,5,  Reg B = Reg B XOR 5
         4,3,  Reg B = Reg B XOR Reg C
         0,3,  Reg A = Reg A / (2**3)
         5,5,  OUTPUT Reg B MOD 8
         3,0   halt or go back to start


outputs Reg B mod 8


'''

    def execute_program(self) -> None:
        ''' A number called the instruction pointer identifies the position in the program 
        from which the next opcode will be read; it starts at 0, pointing at the first 3-bit 
        number in the program. Except for jump instructions, the instruction pointer increases 
        by 2 after each instruction is processed (to move past the instruction's opcode and 
        its operand). If the computer tries to read an opcode past the end of the program, it 
        instead halts. '''
        
        if self.pointer >= len(self.program):
            return

        opcode  = self.program[self.pointer]
        operand = self.program[self.pointer + 1]

        func = self.get_instruction_func(opcode)
        func(operand)
        
        print(self) ##############

        # if opcode in [0, 3, 5]:
        #     print(f"Executing opcode {opcode} with operand {operand} (Reg A: {self.reg_a}) (output: {self.output})")

        if opcode == 3:
            if self.reg_a == 0:
                return
            else:
                self.pointer = func(operand)
        else:
            self.pointer = self.pointer + 2

        if self.pointer < len(self.program):
            self.execute_program()

    def get_instruction_func(self, opcode: int) -> Callable:
        return self.instructions_dict.get(opcode, dummy_func)
            
    def decode_combo_operand(self, num: int) -> int:
        ''' 
        - Combo operands 0 through 3 represent literal values 0 through 3.
        - Combo operand 4 represents the value of register A.
        - Combo operand 5 represents the value of register B.
        - Combo operand 6 represents the value of register C.
        - Combo operand 7 is reserved and will not appear in valid programs.'''
        
        if num in [0, 1, 2, 3]:
            return num
        if num == 4:
            return self.reg_a
        if num == 5:
            return self.reg_b
        if num == 6:
            return self.reg_c
        else:
            raise ValueError(f"Invalid combo operator: {num}")

    def adv(self, combo_operand: int) -> None:
        ''' The adv instruction (opcode 0) performs division. The numerator is the value in the 
        A register. The denominator is found by raising 2 to the power of the instruction's combo
        operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A 
        by 2^B.) The result of the division operation is truncated to an integer and then written 
        to the A register. '''

        op = self.decode_combo_operand(combo_operand)
        numerator = self.reg_a
        denominator = 2**op
        result = math.floor(numerator/denominator)
        self.reg_a = result

    def bxl(self, literal_operand: int) -> None:
        ''' The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the 
        instruction's literal operand, then stores the result in register B. '''
        
        self.reg_b = self.reg_b ^ literal_operand

    def bst(self, combo_operand: int) -> None:
        ''' The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 
        (thereby keeping only its lowest 3 bits), then writes that value to the B register. '''

        op = self.decode_combo_operand(combo_operand)
        result = op % 8
        self.reg_b = result
        
    def jnz(self, literal_operand: int) -> int:
        ''' The jnz instruction (opcode 3) does nothing if the A register is 0. However, if 
        the A register is not zero, it jumps by setting the instruction pointer to the value of 
        its literal operand; if this instruction jumps, the instruction pointer is not increased 
        by 2 after this instruction. '''

        return literal_operand

    def bxc(self, operand: int) -> None:
        ''' The bxc instruction (opcode 4) calculates the bitwise XOR of register B and 
        register C, then stores the result in register B. (For legacy reasons, this instruction 
        reads an operand but ignores it.) '''

        self.reg_b = self.reg_b ^ self.reg_c

    def out(self, combo_operand: int) -> None:
        ''' The out instruction (opcode 5) calculates the value of its combo operand modulo 8, 
        then outputs that value. (If a program outputs multiple values, they are separated 
        by commas.) '''

        op = self.decode_combo_operand(combo_operand)
        result = op % 8
        self.output.append(result)

    def bdv(self, combo_operand: int) -> None:
        ''' The bdv instruction (opcode 6) works exactly like the adv instruction except that 
        the result is stored in the B register. (The numerator is still read from the A register.) '''

        op = self.decode_combo_operand(combo_operand)
        numerator = self.reg_a
        denominator = 2**op
        result = math.floor(numerator/denominator)
        self.reg_b = result

    def cdv(self, combo_operand: int) -> None:
        ''' The cdv instruction (opcode 7) works exactly like the adv instruction except that
        the result is stored in the C register. (The numerator is still read from the A register.) '''

        op = self.decode_combo_operand(combo_operand)
        numerator = self.reg_a
        denominator = 2**op
        result = math.floor(numerator/denominator)
        self.reg_c = result

def read_data(filename: Path) -> Computer:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        reg_a = int(''.join(char for char in line_list[0] if char.isdigit()))
        reg_b = int(''.join(char for char in line_list[1] if char.isdigit()))
        reg_c = int(''.join(char for char in line_list[2] if char.isdigit()))
        program_str = line_list[4].removeprefix('Program: ')
        program = []
        for char in program_str:
            if char.isdigit():
                program.append(int(char))
        return Computer(program, reg_a, reg_b, reg_c)




def part_one(filename: Path):
    comp = read_data(filename)
    comp.execute_program()
    return comp.get_output_str()

def part_two_example():
    comp = Computer([0,3,5,4,3,0], 2024, 0, 0)
    print(comp)
    num = get_int_from_list(comp.program)
    result = comp.check_new_reg_a_value(num)
    if result:
        return num
    else:
        print(f"Didn't work: {num}")
        value = num
        while True:
            result = comp.check_new_reg_a_value(value)
            print(f"Checking: {value} - {result}")
            if result:
                return value
            else:
                value += 8

    # print(comp.check_new_reg_a_value(117423440))
    # print(comp.check_new_reg_a_value(423))
    # print(comp.check_new_reg_a_value(117440))
    # print(comp.check_new_reg_a_value(34344444))

    # value = get_int_from_list(comp.program)
    # value = 0
    # while True:
    #     result = comp.check_new_reg_a_value(value)
    #     print(f"Checking: {value} - {result}")
    #     if result:
    #         return value
    #     else:
    #         value += 8
    
# 
def part_two(filename: Path):
    comp = read_data(filename)
    input_prog = deepcopy(comp.program)
    test_num = get_int_from_list(input_prog)
    print(f"Program: {input_prog} (length {len(input_prog)}) ({get_int_from_list(input_prog):,})")
    
    test = Computer(input_prog, test_num, 0, 0)
    test.execute_program()
    output = test.output
    print(f"Output:  {output} (length {len(output)}) ({get_int_from_list(output):,})")
    
    # comp = read_data(filename)
    # num = get_int_from_list(comp.program)
    # result = comp.check_new_reg_a_value(num)
    # if result:
    #     return num
    # else:
    #     print(f"Didn't work: {num}")
    #     value = num
    #     while True:
    #         result = comp.check_new_reg_a_value(value)
    #         # print(f"Checking: {value} - {result}")
    #         if result:
    #             return value
    #         else:
    #             value += 8


def main():
    # print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two_example()}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def get_int_from_list(int_list: list[int]) -> int:
    copied_list = deepcopy(int_list)
    final_zero = copied_list.pop(-1)
    rev_list = list(reversed(copied_list))
    new_list = rev_list + [final_zero]
    num_str = ''.join(str(x) for x in new_list)
    return int(num_str, base=8)
    # int_list = int_list[:-1]
    # i = len(int_list)

    # output = 0
    # for x in reversed(int_list):
    #     output += (x * (i * 8))
    #     i -= 1
    # return output
        


def random_tests():
    # comp = Computer([0,3,5,4,3,0], 2024, 0, 0)
    # print(comp.program)
    # print(comp.program_int)
    # print(comp.program_bin_num)
    # comp.execute_program()
    # print(comp.output)
    # print()
    # for x in range(46323429, 46323500, 1):
    #     comp = Computer([2,4,1,1,7,5,1,5,4,3,0,3,5,5,3,0], x, 0, 0)
    #     comp.execute_program()
    #     print(f"{x}: {comp.get_output_str()}")

    # prog = [2,4,1,1,7,5,1,5,4,3,0,3,5,5,3,0]
    # comp = Computer(prog, 46323429, 0, 0)
    # print(comp)
    # comp.execute_program()
    # print(comp)

    # print()
    # math.fmod
    # print(math.floor(5790428-1 / 256))

    for x in range(8):
        print(f"{x}: {x^1}")
    print()
    for x in range(8):
        print(f"{x}: {x^5}")

    # print(get_int_from_list([6, 0]))
    # print(get_int_from_list([7, 0]))
    # print(get_int_from_list([0, 1, 0]))
    # print(get_int_from_list([1, 1, 0]))
    # print(get_int_from_list([3, 2, 0]))
    # print(get_int_from_list([4, 2, 0]))
    # print(get_int_from_list([0,3,5,4,3,0]))

    # print()
    # print(int('175', base=8))

    # print(oct(117440))
    # print(get_int_from_list([2, 5, 0]))

    # asdf = ['0o445311', '0o545311', '0o645311', '0o355311', '0o365311', '0o375311']
    # for x in asdf:
    #     print(f"{x}: {int(x, 8)} ({int(int(x, 8) / 8)})")
        
    # print()
    # print(oct(150217))
    # print()
    # print(22873 - 18777)
    # print()
    # print(get_int_from_list([4, 4, 5, 3, 1, 1, 0]))

    # '''
    # 48: 6,0
    #     (6 * 8) + (0 * 0)
    # 56: 7,0
    #     (7 * 8) + (0 * 0)
    # 64: 0,1,0
    #     (0 * 16) + (8 * 8) + (0 * 0)
    # 72: 1,1,0
    # '''

       
if __name__ == '__main__':
    main()