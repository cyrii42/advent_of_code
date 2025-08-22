'''--- Day 7: Bridge Repair ---'''

from pathlib import Path
from rich import print
from copy import deepcopy
import itertools
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2024_day7_example.txt'
INPUT = DATA_DIR / '2024_day7_input.txt'

OPERATORS_PART_ONE = ['+', '*']
OPERATORS_PART_TWO = ['+', '*', '||']

def ingest_data(filename: Path) -> list[tuple[int, list[int]]]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n').split(':') for line in f.readlines()]
        output_list = [(int(test_value), [int(x) for x in numbers.split()]) for test_value, numbers in line_list]
        
    return output_list

def find_operator_combos(number_list: list[int], potential_operators: list[str]) -> list[list[str]]:
    num_gaps = len(number_list) - 1
    operator_combos = itertools.product(potential_operators, repeat=num_gaps)
    operator_combo_list = [list(x) for x in list(operator_combos)]
    return operator_combo_list

def validate_equation(test_value: int, number_list: list[int], operator_combo_list: list[list[str]]) -> bool:
    for operator_list in operator_combo_list:
        result = parse_operator_list(deepcopy(number_list), deepcopy(operator_list))
        if result == test_value:
            return True

    return False
        
def parse_operator_list(number_list: list[int], operator_list: list[str]) -> int:
    if len(number_list) == 1:
        return number_list[0]

    num_1 = number_list.pop(0)
    num_2 = number_list.pop(0)
    operator = operator_list.pop(0)
    result = perform_calculation(num_1, num_2, operator)
    number_list.insert(0, result)
    return parse_operator_list(number_list, operator_list)

def perform_calculation(num_1: int, num_2: int, operator: str) -> int:
    match operator:
        case '+': return num_1 + num_2
        case '*': return num_1 * num_2
        case '||': return int(f"{num_1}{num_2}")
        case _: raise ValueError
    
def find_calibration_result(filename: Path, operator_list: list[str]) -> int:
    input_data = ingest_data(filename)

    valid_equations = list()
    for equation_input in alive_it(input_data):
        test_value, number_list = equation_input
        operator_combos = find_operator_combos(number_list, operator_list)
        if validate_equation(test_value, number_list, operator_combos):
            valid_equations.append(test_value)
        
    return sum(valid_equations)

def part_one(filename: Path) -> int:
    return find_calibration_result(filename, OPERATORS_PART_ONE)

def part_two(filename: Path) -> int:
    return find_calibration_result(filename, OPERATORS_PART_TWO)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()