from pathlib import Path
from rich import print

import advent_of_code as aoc
from intcode import IntCode, IntCodeReturnType, parse_intcode_program

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLES_PART_ONE = [
    '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99',
    '1102,34915192,34915192,7,4,7,99,0',
    '104,1125899906842624,99'
]
INPUT = aoc.get_input(YEAR, DAY)
   
def part_one(data: str):
    program = parse_intcode_program(data)
    comp = IntCode(program, input=1)
    while True:
        result = comp.execute_program()
        if result.type == IntCodeReturnType.HALT:
            return comp.output_queue

def part_two(data: str):
    program = parse_intcode_program(data)
    comp = IntCode(program, input=2)
    while True:
        result = comp.execute_program()
        if result.type == IntCodeReturnType.HALT:
            return comp.output_queue

def main():
    print(f"Part One (example #1):  {part_one(EXAMPLES_PART_ONE[0])}")
    print(f"Part One (example #2):  {part_one(EXAMPLES_PART_ONE[1])}")
    print(f"Part One (example #3):  {part_one(EXAMPLES_PART_ONE[2])}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()