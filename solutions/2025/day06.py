import math
from collections import defaultdict
from pathlib import Path
from typing import Callable, Any

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

TESTS_PART_ONE = [(EXAMPLE, 4277556)]
TESTS_PART_TWO = [(EXAMPLE, 3263827)]

def parse_data_part_one(data: str) -> dict[int, list[str]]:
    output_dict = defaultdict(list)
    line_list = data.splitlines()
    for line in line_list:
        nums = [num for num in line.split(' ') if num]
        for j, num in enumerate(nums):
            if num:
                output_dict[j].append(num)
    return output_dict

def solve_part_one(problem: list[str]) -> int:
    nums = [int(s) for s in problem if s.isdigit()]
    if problem[-1] == '+':
        return sum(nums)
    if problem[-1] == '*':
        return math.prod(nums)
    else:
        raise ValueError(problem)

def parse_data_part_two(data: str) -> dict[int, list[str]]:
    output_dict = defaultdict(list)
    line_list = data.splitlines()

    op_line = line_list[-1]
    op_char_list = [i for i, char in enumerate(op_line) if char in ['+', '*']]
    comma_chars = [i-1 for i in op_char_list[1:]]

    new_line_list: list[str] = []
    for line in line_list:
        line_as_list = list(line)
        for i in comma_chars:
            line_as_list[i] = ','
        new_line_list.append(''.join(char for char in line_as_list))

    for line in new_line_list:
        nums = [num for num in line.split(',') if num]
        for i, num in enumerate(nums):
            if num:
                output_dict[i].append(num)
    return output_dict

def solve_part_two(problem: list[str]) -> int:
    op = problem.pop().strip()
    fn = sum if op == '+' else math.prod
    
    assert len({len(s) for s in problem}) == 1
    num_strs = [''.join(s[i] for s in problem) for i in range(len(problem[0]))]
    nums = [int(x) for x in num_strs]
    return fn(nums)
    
def part_one(data: str):
    problem_dict = parse_data_part_one(data)
    return sum(solve_part_one(p) for p in problem_dict.values())

def part_two(data: str):
    problem_dict = parse_data_part_two(data)
    return sum(solve_part_two(p) for p in problem_dict.values())

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