import itertools
from collections import deque
from pathlib import Path
from typing import Callable, Any
from rich import print

from intcode import IntCode, Halt, Output
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

def parse_data(data: str) -> list[int]:
    output_list = []
    for num_str in data.split(','):
        if num_str[0] == '-':
            output_list.append(0 - int(num_str[1:]))
        else:
            output_list.append(int(num_str))
    return output_list
        
def part_one(data: str):
    program = parse_data(data)
    max_signal = 0
    for seq in itertools.permutations([0, 1, 2, 3, 4]):
        output_signal = 0
        for i in range(5):
            input_signal = output_signal
            phase_setting = seq[i]
            amp = IntCode(program, deque([phase_setting, input_signal]))
            output_signal = amp.execute_program().value
        max_signal = max(output_signal, max_signal)
    return max_signal

def create_amplifiers(program: list[int], 
                      seq: tuple[int, ...]
                      ) -> list[IntCode]:
    id_list = ['A', 'B', 'C', 'D', 'E']
    amps = [IntCode(program=program.copy(), 
                    id=char, 
                    input_queue=deque([n])) 
            for char, n
            in zip(id_list, seq)]
    return amps

def part_two(data: str):
    program = parse_data(data)
    max_signal = 0
    for seq in itertools.permutations([5, 6, 7, 8, 9]):
        amp_list = create_amplifiers(program, seq)
        output_signal = 0
        i = 0
        while True:
            amp = amp_list[i]
            amp.input_queue.append(output_signal)
            result = amp.execute_program()
            if isinstance(result, Halt):
                amp_e = amp_list[-1]
                max_signal = max(amp_e.output, max_signal)
                break
            elif isinstance(result, Output):
                output_signal = result.value
            else:
                raise ValueError
            i = (i + 1) % len(amp_list)
    return max_signal
    
def run_tests(tests: list[tuple[str, Any]], fn: Callable):
    for i, example in enumerate(tests, start=1):
        data, answer = example
        test_answer = fn(data)
        print(f"Test #{i}: {test_answer == answer}",
              f"({test_answer})")

def main():
    run_tests(TESTS_PART_ONE, part_one)
    print(f"Part One (input):  {part_one(INPUT)}")
    run_tests(TESTS_PART_TWO, part_two)
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()