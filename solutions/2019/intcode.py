from dataclasses import dataclass, field
from collections import deque, defaultdict
from enum import Enum
from typing import Callable, NamedTuple

class AwaitingInput(Exception):
    pass

class IntCodeReturnType(Enum):
    HALT = 0
    OUTPUT = 1
    AWAITING_INPUT = 2

class IntCodeReturn(NamedTuple):
    type: IntCodeReturnType
    value: int

def parse_intcode_program(data: str) -> defaultdict[int, int]:
    output_dict = defaultdict(int)
    for i, num_str in enumerate(data.split(',')):
        if num_str[0] == '-':
            output_dict[i] = 0 - int(num_str[1:])
        else:
            output_dict[i] = int(num_str)
    return output_dict

@dataclass
class IntCode:
    program: defaultdict[int, int] = field(repr=False)
    input: int
    input_queue: deque[int] = field(init=False)
    output_queue: deque[int] = field(default_factory=deque)
    ptr: int = 0
    relative_base: int = 0

    def __post_init__(self):
        self.input_queue = deque([self.input])
        self.opcode_dict: dict[int, Callable] = {
            1: self.add,
            2: self.mul,
            3: self.input_fn,
            4: self.output_fn,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            9: self.adjust_relative_base,
            99: self.end_program,
        }

    def add_input(self, new_input: int) -> None:
        self.input_queue.append(new_input)

    def get_input(self) -> int:
        try:
            return self.input_queue.popleft()
        except IndexError:
            return 0

    @property
    def output(self) -> int:
        return self.output_queue[-1]

    def access_memory_address(self, address: int) -> int:
        try:
            return self.program[address]
        except IndexError:
            return 0

    def parse_instruction(self, instruction: int) -> tuple[Callable, int, int, int]:
        instruction_str = f"{instruction:05d}"
        opcode = int(instruction_str[3:])
        fn = self.opcode_dict[opcode]
        mode_c, mode_b, mode_a = [int(x) for x in list(instruction_str[0:3])]
        return (fn, mode_a, mode_b, mode_c)    

    def get_value(self, num: int, mode: int) -> int:
        match mode:
            case 0:  # position mode
                return self.program[num]
            case 1:  # immediate mode
                return num
            case 2:  # relative mode
                position = self.relative_base + num
                return self.program[position]
            case _:
                raise ValueError(f"Unrecognized mode designation: {mode}")

    def execute_program(self) -> IntCodeReturn:
        while True:
            inst = self.program[self.ptr]
            fn, mode_a, mode_b, mode_c = self.parse_instruction(inst)

            if fn == self.end_program:
                return IntCodeReturn(IntCodeReturnType.HALT, self.output)
            elif fn in [self.add, self.mul, self.less_than, self.equals]:
                a, b, c = [self.program[self.ptr + x] for x in range(1, 4)]
                val_a = self.get_value(a, mode_a)
                val_b = self.get_value(b, mode_b)
                val_c = self.relative_base + c if mode_c == 2 else c
                fn(val_a, val_b, val_c)
                self.ptr += 4
            elif fn in [self.jump_if_true, self.jump_if_false]:
                a, b = [self.program[self.ptr + x] for x in range(1, 3)]
                val_a = self.get_value(a, mode_a)
                val_b = self.get_value(b, mode_b)
                fn(val_a, val_b)
            elif fn == self.adjust_relative_base:
                a = self.program[self.ptr + 1]
                val_a = self.get_value(a, mode_a)
                fn(val_a)
                self.ptr += 2
            elif fn == self.input_fn:
                try:
                    a = self.program[self.ptr + 1]
                    val_a = self.relative_base + a if mode_a == 2 else a
                    fn(val_a)
                    self.ptr += 2
                except AwaitingInput:
                    self.ptr += 2
                    return IntCodeReturn(IntCodeReturnType.AWAITING_INPUT, 0)
            elif fn == self.output_fn:
                a = self.program[self.ptr + 1]
                val_a = self.get_value(a, mode_a)
                fn(val_a)
                self.ptr += 2
                return IntCodeReturn(IntCodeReturnType.OUTPUT, self.output)

    def add(self, a: int, b: int, c: int) -> None:
        ''' Adds together numbers read from two positions and stores
        the result in a third position'''
        
        self.program[c] = a + b

    def mul(self, a: int, b: int, c: int) -> None:
        ''' Multiplies numbers read from two positions and stores
        the result in a third position'''
        
        self.program[c] = a * b

    def input_fn(self, a: int) -> None:
        ''' Takes a single integer as input and saves it to the position 
        given by its only parameter. For example, the instruction 3,50 would 
        take an input value and store it at address 50.'''
        
        try:
            self.program[a] = self.input_queue.popleft()
        except IndexError:
            raise AwaitingInput

    def output_fn(self, a: int) -> None:
        ''' Outputs the value of its only parameter. For example, the 
        instruction 4,50 would output the value at address 50. '''

        self.output_queue.append(a)

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
        ''' If the first parameter is less than the second parameter, stores 1 
        in the position given by the third parameter. Otherwise, stores 0. '''
        
        if a < b:
            self.program[c] = 1
        else:
            self.program[c] = 0

    def equals(self, a: int, b: int, c: int) -> None:
        ''' If the first parameter is equal to the second parameter, stores 1 
        in the position given by the third parameter. Otherwise, stores 0. '''
        
        if a == b:
            self.program[c] = 1
        else:
            self.program[c] = 0

    def adjust_relative_base(self, a: int) -> None:
        ''' Adjusts the relative base by the value of the parameter. '''
        
        self.relative_base += a

    def end_program(self) -> int:
        return self.output_queue.pop()
