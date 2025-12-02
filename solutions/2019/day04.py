from pathlib import Path
from typing import Callable, Any
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

TESTS_PART_ONE = [
    ('111111', True),
    ('223450', False),
    ('123789', False)
]
TESTS_PART_TWO = [
    ('112233', True),
    ('123444', False),
    ('111122', True)
]
INPUT = aoc.get_input(YEAR, DAY)

def test_password_part_one(password: str) -> bool:
    return (len(password) == 6 and test_adjacency(password) 
            and test_non_decreasing(password))

def test_password_part_two(password: str) -> bool:
    return (len(password) == 6 and test_adjacency(password, part_two=True) 
            and test_non_decreasing(password))

def test_adjacency(password: str, part_two: bool = False) -> bool:
    i = 0
    if part_two:
        doubled_digits = {char for char in password if password.count(char) == 2}
        if not doubled_digits:
            return False
        for digit in doubled_digits:
            i = password.index(digit)
            try:
                if password[i+1] == digit:
                    return True
            except IndexError:
                continue
        return False
        
    else:
        while i < len(password)-1:
            if password[i] == password[i+1]:
                return True
            i += 1
        return False

def test_non_decreasing(password: str) -> bool:
    i = 0
    while i < len(password)-1:
        if int(password[i]) > int(password[i+1]):
            return False
        i += 1
    return True
   
def part_one(data: str):
    start, end = [int(x) for x in data.split('-')]
    
    num_valid_passwords = 0
    for x in range(start, end+1):
        if test_password_part_one(str(x)):
            num_valid_passwords += 1
    return num_valid_passwords

def part_two(data: str):
    start, end = [int(x) for x in data.split('-')]
    
    num_valid_passwords = 0
    for x in range(start, end+1):
        if test_password_part_two(str(x)):
            num_valid_passwords += 1
    return num_valid_passwords

def run_tests(tests: list[tuple[str, Any]], fn: Callable):
    for i, example in enumerate(tests, start=1):
        data, answer = example
        test_answer = fn(data)
        print(f"Test #{i}: {test_answer == answer}",
              f"(result was {test_answer})")

def main():
    run_tests(TESTS_PART_ONE, test_password_part_one)
    print(f"Part One (input):  {part_one(INPUT)}")
    run_tests(TESTS_PART_TWO, test_password_part_two)
    print(f"Part Two (input):  {part_two(INPUT)}")
      
if __name__ == '__main__':
    main()