'''--- Day 3: Mull It Over ---'''

import re
from pathlib import Path
from advent_of_code.constants import DATA_DIR

EXAMPLE_PART_ONE = DATA_DIR / '2024_day3_example.txt'
EXAMPLE_PART_TWO = DATA_DIR / '2024_day3_part2_example.txt'
INPUT = DATA_DIR / '2024_day3_input.txt'

REGEX_PART_ONE = r"mul\([0-9]{1,3}\,[0-9]{1,3}\)"

MUL_PATTERN = r"(?P<muls>mul\([0-9]{1,3}\,[0-9]{1,3}\))"
DO_PATTERN = r"(?P<do>do\(\))"
DONT_PATTERN = r"(?P<dont>don't\(\))"
REGEX_PART_TWO = MUL_PATTERN + '|' + DO_PATTERN + '|' + DONT_PATTERN

def ingest_data(filename: Path) -> str:
    with open(filename, 'r') as f:
        text = f.read()
    return text

def parse_mul(text: str) -> int:
    num1, num2 = text.removeprefix('mul(').removesuffix(')').split(',')
    return int(num1) * int(num2)

def part_one(filename: Path) -> int:
    text = ingest_data(filename)
    pattern = re.compile(REGEX_PART_ONE)
    muls = pattern.findall(text)
    return sum([parse_mul(mul) for mul in muls])

def part_two(filename: Path) -> int:
    text = ingest_data(filename)
    pattern = re.compile(REGEX_PART_TWO)
    matches = pattern.finditer(text)

    total = 0
    enabled = True
    for m in matches:
        text = m.group(0)

        match text:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _ if enabled:
                total += parse_mul(text)

    return total


def main():
    print(f"Part One (example):  {part_one(EXAMPLE_PART_ONE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO)}")
    print(f"Part Two (input):  {part_two(INPUT)}")


if __name__ == '__main__':
    main()