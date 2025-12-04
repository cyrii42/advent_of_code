import itertools
from dataclasses import dataclass, field
from collections import deque
from pathlib import Path
from typing import Callable, Any
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

TESTS_PART_ONE = [
    ('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', 43210),  # 4,3,2,1,0
    ('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0', 54321), # 0,1,2,3,4
    ('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0', 65210) # 1,0,4,3,2
]
TESTS_PART_TWO = [
    ('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', 139629729), # 9,8,7,6,5
    ('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10', 18216) # 9,7,8,5,6
]
INPUT = aoc.get_input(YEAR, DAY)

class AwaitingInput(Exception):
    pass

class NewOutput(Exception):
    pass

class EndProgram(Exception):
    pass

@dataclass
class Amplifier:
    program: list[int] = field(repr=False)
    input_queue: deque[int] = field(default_factory=deque)
    output_queue: deque[int] = field(default_factory=deque)
    id: str = ''
    ptr: int = 0
    part_two: bool = False
    awaiting_input: bool = False

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

    def execute_next_instruction(self) -> None:
        if self.awaiting_input and not self.input_queue:
            raise AwaitingInput
        
        inst = self.program[self.ptr]
        fn, mode_a, mode_b, _ = self.parse_instruction(inst)
    
        if fn == self.end_program:
            raise EndProgram
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
            try:
                a = self.program[self.ptr + 1]
                val_a = a
                fn(val_a)
                self.ptr += 2
            except AwaitingInput:
                raise
        elif fn == self.output:
            try:
                a = self.program[self.ptr + 1]
                val_a = self.get_value(a, mode_a)
                fn(val_a)
            except NewOutput:
                raise
            finally:
                self.ptr += 2

    def execute_program(self):
        while True:
            try:
                self.execute_next_instruction()
            except EndProgram:
                break

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

        if not self.part_two:
            self.program[a] = self.input_queue.popleft()
        else:
            try:
                self.program[a] = self.input_queue.popleft()
            except IndexError:
                raise AwaitingInput

    def output(self, a: int) -> None:
        ''' Outputs the value of its only parameter. For example, the 
        instruction 4,50 would output the value at address 50. '''
        
        self.output_queue.append(a)
        if self.part_two:
            raise NewOutput

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

def try_phase_sequence(program: list[int], seq: tuple[int, ...]) -> int:
    if len(seq) != 5:
        raise ValueError("Sequence must contain exactly 5 numbers")
    output_signal = 0
    for i in range(5):
        input_signal = output_signal
        phase_setting = seq[i]
        comp = Amplifier(program, deque([phase_setting, input_signal]))
        comp.execute_program()
        output_signal = comp.output_queue.pop()
    return output_signal
        
def part_one(data: str):
    program = parse_data(data)
    max_signal = 0
    for seq in itertools.permutations([0, 1, 2, 3, 4]):
        signal = try_phase_sequence(program, seq)
        max_signal = max(signal, max_signal)
    return max_signal

def create_amplifiers(program: list[int]) -> list[Amplifier]:
    return [Amplifier(program, id=char, part_two=True) 
            for char in ['A', 'B', 'C', 'D', 'E']]

@dataclass
class AmplifierSeries:
    program: list[int]
    amplifiers: list[Amplifier]

    def get_highest_thruster_signal(self) -> int:
        max_signal = 0
        for seq in itertools.permutations([5, 6, 7, 8, 9]):
            signal = self.try_phase_sequence(seq)
            max_signal = max(signal, max_signal)
        return max_signal

    def try_phase_sequence(self, seq: tuple[int, ...]) -> int:
        phase_sequence = deque(seq)

        self.amplifiers[0].input_queue.append(0)
       
        while True:
            next_input = deque(seq)
            for amp in self.amplifiers:
                print(amp)
                try:
                    amp.execute_program()
                except NewOutput:
                    next_input.append(amp.output_queue.pop())
                    amp.ptr += 2
                except AwaitingInput:
                    if next_input:
                        amp.input(next_input.popleft())
                        amp.ptr += 2
                    else:
                        continue
                except EndProgram:
                    return self.amplifiers[-1].output_queue.pop()
        

def part_two(data: str):
    ...
    ### I feel like there's been another problem that involved
    ### passing data among objects... try looking at:
    #   - 2016 day 10
    #   - 2017 day 18
    program = parse_data(data)
    amp_list = [Amplifier(program.copy(), id=char, part_two=True) 
                for char in ['A', 'B', 'C', 'D', 'E']]
    amp_series = AmplifierSeries(program, amp_list)

    return amp_series.get_highest_thruster_signal()

    # phase_sequence = (x for x in )

    # while True:
    #     for amp in amps:
    #         try:
    #             amp.execute_program()
    #         except 

    # while True:
    #     try:
    #         comp0.execute_next_instruction()
    #     except AwaitingInput:
    #         pass
    #     except NewOutput:
    #         value = comp0.output_queue.pop()
    #         comp1.input_queue.append(value)
            
    #     try:
    #         comp1.execute_next_instruction()
    #     except AwaitingInput:
    #         pass
    #     except NewOutput:
    #         value = comp1.output_queue.pop()
    #         comp0.input_queue.append(value)

    #     if comp0.awaiting_input and comp1.awaiting_input:
    #         return comp1.values_sent
    
def run_tests(tests: list[tuple[str, Any]], fn: Callable):
    for i, example in enumerate(tests, start=1):
        data, answer = example
        test_answer = fn(data)
        print(f"Test #{i}: {test_answer == answer}",
              f"({test_answer})")

def main():
    # run_tests(TESTS_PART_ONE, part_one)
    # print(f"Part One (input):  {part_one(INPUT)}")
    run_tests(TESTS_PART_TWO, part_two)
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    asdf = itertools.permutations([0, 1, 2, 3, 4])
    x = deque(next(asdf))
    print(x)
    print(x.popleft())
    print(x)
       
if __name__ == '__main__':
    main()