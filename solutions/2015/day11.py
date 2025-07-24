import functools
import itertools
import json
import math
import os
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from pprint import pprint
from string import ascii_letters, ascii_lowercase
from typing import Callable, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def next_letter(char: str) -> str:
    if len(char) > 1 or char not in ascii_lowercase:
        raise ValueError

    if char == 'z':
        return 'a'

    n = ascii_lowercase.find(char)
    return ascii_lowercase[n+1]

def increment_password(password: str) -> str:
    ''' Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on. 
    Increase the rightmost letter one step; if it was z, it wraps around to a, and 
    repeat with the next letter to the left until one doesn't wrap around.  '''

    if any(char not in ascii_lowercase for char in password):
        raise ValueError         

    if len(password) == 1:
        return next_letter(password[0])

    if password[-1] != 'z':
        return password[:-1] + next_letter(password[-1])
    else:
        return increment_password(password[:-1]) + 'a'

def check_test_zero(password: str) -> bool:
    return len(password) == 8 and all(char.islower() for char in password)

def check_test_one(password: str) -> bool:
    ''' Passwords must include one increasing straight of at least three letters, 
    like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.  '''
    for i, char in enumerate(password):
        if i >= len(password) - 3:
            return False

        if char in ['y', 'z']:  # can't qualify because at least one 'z' will flip to 'a'
            continue

        if next_letter(char) == password[i+1] and next_letter(next_letter(char)) == password[i+2]:
            return True

    return False
    ...

def check_test_two(password: str) -> bool:
    ''' Passwords may not contain the letters i, o, or l, as these letters can be 
    mistaken for other characters and are therefore confusing. '''

    return not any(char in password for char in ['i', 'o', 'l'])

def check_test_three(password: str) -> bool:
    ''' Passwords must contain at least two different, non-overlapping pairs of letters,
    like aa, bb, or zz. '''

    pairs = [f"{x}{x}" for x in ascii_lowercase]
    pairs_found: list[str] = []
    for i, char in enumerate(password):
        if i >= len(password) - 1:
            break

        if f"{char}{password[i+1]}" in pairs and f"{char}{password[i+1]}" not in pairs_found:
            pairs_found.append(f"{char}{password[i+1]}")

    return len(pairs_found) >= 2
    ...

def check_all_tests(password: str) -> bool:
    if not check_test_zero(password):
        return False
    if not check_test_one(password):
        return False
    if not check_test_two(password):
        return False
    if not check_test_three(password):
        return False
    return True

def get_next_valid_password(password: str) -> str:
    current_try = increment_password(password)
    while True:
        if check_all_tests(current_try):
            return current_try
        else:
            current_try = increment_password(current_try)
        
def run_example_tests() -> None:
    test1 = 'hijklmmn'
    print(f"{test1} meets test #1: {check_test_one(test1)}")
    print(f"{test1} fails test #2: {not check_test_two(test1)}\n")
    
    test2 = 'abbceffg'
    print(f"{test2} fails test #1: {not check_test_one(test2)}")
    print(f"{test2} meets test #3: {check_test_three(test2)}\n")
    
    test3 = 'abbcegjk'
    print(f"{test3} fails test #3: {not check_test_three(test3)}\n")
    
    test4 = 'abcdefgh'
    test4_answer = 'abcdffaa'
    test_passed = get_next_valid_password(test4) == test4_answer
    response = f"The next password after \"{test4}\" is \"{test4_answer}\": {test_passed}"
    if not test_passed:
        response += f" (program returns \"{get_next_valid_password(test4)}\")"
    print(response + '\n')
    
    test5 = 'ghijklmn'
    test5_answer = 'ghjaabcc'
    test_passed = get_next_valid_password(test5) == test5_answer
    response = f"The next password after \"{test5}\" is \"{test5_answer}\": {test_passed}"
    if not test_passed:
        response += f" (it's \"{get_next_valid_password(test5)}\")"
    print(response + '\n')

def parse_data(data: str) -> str:
    return data.strip('\n')

def part_one(data: str):
    password = parse_data(data)
    return get_next_valid_password(password)

def part_two(data: str):
    password = parse_data(data)
    new_password = get_next_valid_password(password)
    return get_next_valid_password(new_password)



def main():
    run_example_tests()
    print(f"Part One (input): {part_one(INPUT)}")
    print(f"Part Two (input): {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()