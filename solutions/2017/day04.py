from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

def validate_passphrase_part_one(passphrase: str) -> bool:
    words = passphrase.split(' ')
    return len(words) == len(set(words))
    
def part_one(data: str):
    line_list = data.splitlines()
    return sum(validate_passphrase_part_one(line) for line in line_list)

def validate_passphrase_part_two(passphrase: str) -> bool:
    words = [''.join(sorted(word)) for word in passphrase.split(' ')]
    return len(words) == len(set(words))

def part_two(data: str):
    line_list = data.splitlines()
    return sum(validate_passphrase_part_two(line) for line in line_list)

def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

       
if __name__ == '__main__':
    main()