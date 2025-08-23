import hashlib
import pathlib

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = 'abc'
INPUT = aoc.get_input(YEAR, DAY)

def get_hash(s: str):
    return hashlib.md5(s.encode('utf-8')).hexdigest()
    
def part_one(door_id: str):
    output_str = ''
    i = 0
    while len(output_str) < 8:
        hash = get_hash(f"{door_id}{i}")
        if hash[0:5] == '00000':
            output_str += hash[5]
        i += 1
    return output_str

def validate_hash(hash: str) -> bool:
    return hash[0:5] == '00000' and hash[5].isdigit() and int(hash[5]) < 8

def part_two(door_id: str):
    d: dict[int, str] = {}
    i = 0
    while len(d) < 8:
        hash = get_hash(f"{door_id}{i}")
        if validate_hash(hash) and int(hash[5]) not in d.keys():
            key = int(hash[5])
            d[key] = hash[6]
        i += 1
    return ''.join(d[key] for key in sorted(d.keys()))

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()