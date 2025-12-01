from pathlib import Path
from rich import print
from typing import Callable, Any

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

TESTS_PART_ONE = [
    ('12', 2),
    ('14', 2),
    ('1969', 654),
    ('100756', 33583)
]

TESTS_PART_TWO = [
    ('14', 2),
    ('1969', 966),
    ('100756', 50346)
]

INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str):
    return [int(x) for x in data.splitlines()]
    
def part_one(data: str):
    mass_list = parse_data(data)
    return sum(((mass // 3) - 2) for mass in mass_list)

def calculate_fuel_part_two(mass: int) -> int:
    total_fuel = 0
    
    while True:
        fuel = ((mass // 3) - 2) 
        if fuel < 0:
            break
        total_fuel += fuel
        mass = fuel

    return total_fuel

def part_two(data: str):
    mass_list = parse_data(data)
    return sum(calculate_fuel_part_two(mass) for mass in mass_list)

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