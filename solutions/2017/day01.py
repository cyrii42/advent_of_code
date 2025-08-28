from pathlib import Path

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

TESTS_PART_ONE = [
    ('1122', 3),
    ('1111', 4),
    ('1234', 0),
    ('91212129', 9)
]
TESTS_PART_TWO = [
    ('1212', 6),
    ('1221', 0),
    ('123425', 4),
    ('123123', 12),
    ('12131415', 4)
]
INPUT = aoc.get_input(YEAR, DAY)

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        data, answer = example
        print(f"Test #{i} ({data}): {part_one(data) == answer}",
              f"({part_one(data)})")

def part_two_tests():
    for i, example in enumerate(TESTS_PART_TWO, start=1):
        data, answer = example
        print(f"Test #{i} ({data}): {part_two(data) == answer}",
              f"({part_two(data)})")
    
def part_one(data: str):
    total = 0
    for i, num_char in enumerate(data):
        if i == len(data)-1:
            next_char = data[0]
        else:
            next_char = data[i+1]
            
        if num_char == next_char:
            total += int(num_char)
    return total

def part_two(data: str):
    total = 0
    for i, num_char in enumerate(data):
        halfway_around = (i + (len(data) // 2)) % len(data)
        next_char = data[halfway_around]
        
        if num_char == next_char:
            total += int(num_char)
    return total

def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    part_two_tests()
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()