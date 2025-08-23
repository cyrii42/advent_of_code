import hashlib
import pathlib
import re

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = 'abc'
INPUT = aoc.get_input(YEAR, DAY)

TRIPLE_PATTERN = r'(.)\1{2,}'

HASH_DICT = {}
STRETCHED_HASH_DICT = {}

def get_hash(s: str):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def get_stretched_hash(s: str):
    h = hashlib.md5(s.encode('utf-8')).hexdigest()
    for _ in range(2016):
        h = hashlib.md5(h.encode('utf-8')).hexdigest()
    return h

def generate_key(salt: str, part_two: bool = False):
    idx = 0
    func = get_stretched_hash if part_two else get_hash
    while True:
        h = func(f"{salt}{idx}")
        m = re.search(TRIPLE_PATTERN, h)
        if m:
            char = m[0][0]
            if verify_key(idx, char, salt, part_two=part_two):
                yield idx
        idx += 1

def verify_key(idx: int, char: str, salt: str, 
               part_two: bool = False) -> bool:
    pattern = ''.join(char for _ in range(5))
    func = get_stretched_hash if part_two else get_hash
    d = STRETCHED_HASH_DICT if part_two else HASH_DICT
    
    for x in range(idx+1, idx+1001):
        s = f"{salt}{x}"
        if s in d.keys():
            h = d[s]
        else:
            h = func(s)
            d[s] = h
            
        if pattern in h:
            return True

    return False
    
def part_one(data: str):
    salt = data
    gen = generate_key(salt)
    for _ in range(63):
        next(gen)
    return next(gen)
    
def part_two(data: str):
    salt = data
    gen = generate_key(salt, part_two=True)
    for _ in range(63):
        next(gen)
    return next(gen)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()