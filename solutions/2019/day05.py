from pathlib import Path
from rich import print

import advent_of_code as aoc
from intcode import IntCode, IntCodeReturnType, parse_intcode_program

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '1002,4,3,4,33'
INPUT = aoc.get_input(YEAR, DAY)
   
def part_one(data: str):
    program = parse_intcode_program(data)
    comp = IntCode(program, input=1)
    while True:
        result = comp.execute_program()
        if result.type == IntCodeReturnType.HALT:
            return result.value
    
def part_two(data: str):
    program = parse_intcode_program(data)
    comp = IntCode(program, input=5)
    while True:
        result = comp.execute_program()
        if result.type == IntCodeReturnType.HALT:
            return result.value

def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()