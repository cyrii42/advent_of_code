from pathlib import Path

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

MAX_VALUE = 4_294_967_295

def parse_data(data: str):
    line_list = data.splitlines()
    pair_list = []
    for line in line_list:
        num1, num2 = line.split('-')
        pair_list.append((int(num1), int(num2)))
    pair_list = list(sorted(pair_list))
    return pair_list

def part_one(data: str):
    pair_list = parse_data(data)
    
    test_ip, idx = (0, 0)
    while True:
        lower, upper = pair_list[idx]
        if test_ip >= lower:
            if test_ip <= upper:
                test_ip = upper + 1
                continue
            else:
                idx += 1
        else:
            return test_ip
            
def part_two(data: str):
    ''' How many IPs are allowed by the blacklist? '''
    pair_list = parse_data(data)

    total, test_ip, idx = (0, 0, 0)
    while test_ip <= MAX_VALUE:
        lower, upper = pair_list[idx]
        if test_ip >= lower:
            if test_ip <= upper:
                test_ip = upper + 1
                continue
            else:
                idx += 1
        else:
            total += 1
            test_ip += 1
    return total


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
       
if __name__ == '__main__':
    main()