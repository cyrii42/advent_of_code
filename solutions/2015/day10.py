from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = '1'
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def parse_data(data: str) -> str:
    return data.strip('\n')

def get_next_sequence(input: str) -> str:
    output_str = ''

    counter = 1
    for i, char in enumerate(input):
        if i == len(input) - 1:
            output_str += f"{counter}{char}"
            break
        
        if input[i+1] != char:
            output_str += f"{counter}{char}"
            counter = 1
        else:
            counter += 1
    return output_str

def part_one(data: str):
    s = parse_data(data)
    num = 40 if data == INPUT else 5

    output = s
    for _ in range(num):
        output = get_next_sequence(output)

    return len(output)
   
def part_two(data: str):
    s = parse_data(data)
    num = 50

    output = s
    for _ in range(num):
        output = get_next_sequence(output)

    return len(output)


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()