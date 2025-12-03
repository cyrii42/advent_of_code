from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

def find_max_joltage_part_one(battery_bank: list[int]) -> int:
    tens_digit = max(n for n in battery_bank[0:-1])  # excluding final battery
    tens_digit_idx = battery_bank.index(tens_digit)
    ones_digit = max(n for n in battery_bank[tens_digit_idx+1:])
    return (tens_digit * 10) + ones_digit

def find_max_joltage(battery_bank: list[int], num_digits: int) -> int:
    '''
- Determine how many digits you must drop: drops = n - k (where n is the input length). 
  If k >= n, just return the input as-is (concatenate digits).
- Build the result with a stack-like structure while scanning the input left-to-right:
    - For each digit, while the stack is non-empty, drops > 0, and the top of the stack 
      is smaller than the incoming digit, pop the stack and decrement drops. This removes 
      smaller earlier digits that would reduce the final number.
    - Push the incoming digit onto the stack.
- After processing all digits, if you still have drops > 0, remove that many digits from 
  the end of the stack (they are the least useful).
- The desired k digits are the first k elements of the stack. Concatenate them (preserving 
  order) to form the final integer.
'''
    digits_to_drop = len(battery_bank) - num_digits
    stack = []
    
    for next_digit in battery_bank:
        while stack and digits_to_drop > 0 and stack[-1] < next_digit:
            stack.pop()
            digits_to_drop -= 1
        stack.append(next_digit)
        
    while len(stack) > num_digits:
        stack.pop()

    return int(''.join(map(str, stack)))

def parse_data(data: str) -> list[list[int]]:
    line_list = data.splitlines()
    return [[int(x) for x in line] for line in line_list]
    
def part_one(data: str):
    battery_banks = parse_data(data)
    return sum(find_max_joltage(bank, num_digits=2) for bank in battery_banks)
    
def part_two(data: str):
    battery_banks = parse_data(data)
    return sum(find_max_joltage(bank, num_digits=12) for bank in battery_banks)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()