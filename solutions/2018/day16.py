from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, NamedTuple, Optional
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
EXAMPLE_OPCODES = 3
INPUT = aoc.get_input(YEAR, DAY)

class NoValidFunction(Exception):
    pass

def dummy_func():
    raise NoValidFunction

class Instruction(NamedTuple):
    opcode: int
    input_a: int
    input_b: int
    output: int

class Sample(NamedTuple):
    instruction: Instruction
    before: list[int]
    after: list[int]
    
@dataclass
class Computer:
    instructions: Optional[list[Instruction]] = field(repr=False, 
                                              default=None)
    register_dict: dict[int, int] = field(init=False)
    opcode_list: list[Callable] = field(default_factory=list)
    opcode_dict: dict[int, Callable] = field(repr=False, 
                                             default_factory=dict)

    def __post_init__(self):
        self.register_dict = {num: 0 for num in range(4)}
        self.opcode_list = [
            self.addr, self.addi, self.mulr, self.muli, self.banr, self.bani, 
            self.borr, self.bori, self.setr, self.seti, self.gtir, self.gtri, 
            self.gtrr, self.eqir, self.eqri, self.eqrr
        ]

    def get_opcode_func(self, opcode: int) -> Callable:
        return self.opcode_dict.get(opcode, dummy_func)

    def test_sample(self, sample: Sample) -> list[Callable]:
        instruction, before, after = sample
        _, a, b, c = instruction

        output_list = []
        for func in self.opcode_list:
            self.set_all_registers(before)
            func(a, b, c)
            if self.get_all_registers() == after:
                output_list.append(func)
        return output_list

    def execute_instructions(self):
        if not self.instructions:
            return
        for inst in self.instructions:
            opcode, a, b, c = inst
            func = self.get_opcode_func(opcode)
            func(a, b, c)
        return self.get_register_value(0)

    def get_register_value(self, reg_num: int) -> int:
        assert len(self.register_dict) == 4
        assert isinstance(reg_num, int)
        assert 0 <= reg_num <= 3
        
        return self.register_dict[reg_num]

    def set_register_value(self, reg_num: int, value: int) -> None:
        assert len(self.register_dict) == 4
        assert isinstance(reg_num, int)
        assert 0 <= reg_num <= 3
        assert isinstance(value, int)
        
        self.register_dict[reg_num] = value

    def get_all_registers(self) -> list[int]:
        assert len(self.register_dict) == 4

        return [v for v in self.register_dict.values()]
        
    def set_all_registers(self, reg_values: list[int]) -> None:
        assert len(self.register_dict) == 4
        assert len(reg_values) == 4
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

def parse_sample(inst_str: list[str]) -> Sample:
    before_line, instruction_str, after_line = inst_str
    before = [int(x) for x 
              in before_line.removeprefix('Before: [').strip(']').split(',')]
    after = [int(x) for x 
              in after_line.removeprefix('After:  [').strip(']').split(',')]
    instruction_ints = [int(x) for x in instruction_str.split(' ')]
    instruction = Instruction(*instruction_ints)
    return Sample(instruction, before, after)

def parse_test(test_str: str) -> Instruction:
    opcode, a, b, c = [int(x) for x in test_str.split(' ')]
    return Instruction(opcode, a, b, c)

def parse_data(data: str) -> tuple[list[Sample], list[Instruction]]:
    line_list = data.splitlines()
    sample_str_list = []
    
    i = 0
    while True:
        if line_list[i] == '' and line_list[i+1] == '':
            break
        sample_str_list.append(line_list[i:i+3])
        i += 4
        
    samples = [parse_sample(sample_str) for sample_str in sample_str_list]
    tests = [parse_test(line) for line in line_list[i:] if line]
    return (samples, tests)

def part_one_test():
    sample = parse_sample(EXAMPLE.splitlines())
    comp = Computer()
    return len(comp.test_sample(sample))
    
def part_one(data: str):
    samples, _ = parse_data(data)
    comp = Computer()

    answer = 0
    for sample in samples:
        result = comp.test_sample(sample)
        if len(result) >= 3:
            answer += 1
    return answer

def create_opcode_dict(comp: Computer, 
                       samples: list[Sample]
                       ) -> dict[int, Callable]:
    opcode_dict: dict[int, set[Callable]] = defaultdict(set)
    for sample in samples:
        result = comp.test_sample(sample)
        if len(result) > 0:
            opcode = sample.instruction.opcode
            opcode_dict[opcode].update({func for func in result})

    func_dict: dict[Callable, set[int]] = defaultdict(set)
    for opcode, func_set in opcode_dict.items():
        for func in func_set:
            func_dict[func].add(opcode)

    final_dict = {}
    while len(final_dict) < 16:
        for func, opcodes in func_dict.items():
            if len(opcodes) == 1:
                opcode = opcodes.pop()
                final_dict[opcode] = func
                for func in func_dict.keys():
                    func_dict[func].discard(opcode)
    return final_dict

def part_two(data: str):
    samples, test_program = parse_data(data)
    comp = Computer(instructions=test_program)
    comp.opcode_dict = create_opcode_dict(comp, samples)
    return comp.execute_instructions()

def main():
    print(f"Part One (example):  {part_one_test()}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()