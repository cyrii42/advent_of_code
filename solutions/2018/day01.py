from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)
TESTS_PART_ONE = [
    ('+1\n-2\n+3\n+1', 3),
    ('+1\n+1\n+1', 3),
    ('+1\n+1\n-2', 0),
    ('-1\n-2\n-3', -6)]

def parse_data(data: str):
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        sign = line[0]
        num = line[1:]
        if sign == '-':
            output_list.append(0 - int(num))
        else:
            output_list.append(int(num))
    return output_list

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        data, answer = example
        print(f"Test #{i}: {part_one(data) == answer}",
              f"({part_one(data)})")
    
def part_one(data: str):
    shift_list = parse_data(data)
    num = 0
    for shift in shift_list:
        num += shift
    return num

def part_two(data: str):
    shift_list = parse_data(data)
    results_seen = set()
    num = 0
    while True:
        for shift in shift_list:
            num += shift
            if num in results_seen:
                return num
            results_seen.add(num)

def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()