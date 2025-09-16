from pathlib import Path

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

TESTS_PART_ONE = [
    (r'{}', 1),
    (r'{{{}}}', 6),
    (r'{{},{}}', 5),
    (r'{{{},{},{{}}}}', 16),
    (r'{<a>,<a>,<a>,<a>}', 1),
    (r'{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
    (r'{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
    (r'{{<a!>},{<a!>},{<a!>},{<ab>}}', 3),
]
INPUT = aoc.get_input(YEAR, DAY)

def get_input_score(s: str, part_two: bool = False) -> int:
    i = 0
    total_score = 0
    num_open_groups = 0
    garbage_char_count = 0
    in_garbage = False
    
    while i < len(s):
        char = s[i]
        
        if char == '!':
            i += 2
            continue
        
        if in_garbage:
            if char == '>':
                in_garbage = False
            else:
                garbage_char_count += 1
            i += 1
            continue

        if char == '<':
            in_garbage = True

        if char == '{':
            num_open_groups += 1

        if char == '}':
            total_score += num_open_groups
            num_open_groups = max(num_open_groups-1, 0)

        i += 1

    if part_two:
        return garbage_char_count
    else:
        return total_score

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        data, answer = example
        print(f"Test #{i} ({data}) ({get_input_score(data)}):",
              f"{get_input_score(data) == answer}")

def part_one(data: str):
    line_list = data.splitlines()
    return sum(get_input_score(line) for line in line_list)

def part_two(data: str):
    line_list = data.splitlines()
    return sum(get_input_score(line, part_two=True) for line in line_list)

def main():
    part_one_tests()
    print()
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()