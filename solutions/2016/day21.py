import itertools
from enum import Enum
from pathlib import Path

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

PART_ONE_TESTS = [('swap position 4 with position 0', 'ebcda'),
                  ('swap letter d with letter b', 'edcba'),
                  ('reverse positions 0 through 4', 'abcde'),
                  ('rotate left 1 step', 'bcdea'),
                  ('move position 1 to position 4', 'bdeac'),
                  ('move position 3 to position 0', 'abdec'),
                  ('rotate based on position of letter b', 'ecabd'),
                  ('rotate based on position of letter d', 'decab')]
INPUT = aoc.get_input(YEAR, DAY)

START = 'abcdefgh'

class Direction(Enum):
    LEFT = 'left'
    RIGHT = 'right'

def swap_position(password: str, x: int, y: int) -> str:
    first_idx = min(x, y)
    second_idx = max(x, y)
    return (f"{password[0:first_idx]}{password[second_idx]}" +
            f"{password[first_idx+1:second_idx]}{password[first_idx]}" +
            f"{password[second_idx+1:]}")

def swap_letter(password: str, x: str, y: str) -> str:
    output_str = ''
    for char in password:
        if char == x:
            output_str += y
        elif char == y:
            output_str += x
        else:
            output_str += char
    return output_str

def rotate_string(password: str, dir: Direction, steps: int) -> str:
    match dir:
        case Direction.LEFT:
            for _ in range(steps):
                password = f"{password[1:]}{password[0]}"
        case Direction.RIGHT:
            for _ in range(steps):
                password = f"{password[-1]}{password[0:-1]}"
    return password

def rotate_right(password: str, ltr: str) -> str:
    idx = password.index(ltr)
    steps = 1 + idx
    if idx >= 4:
        steps += 1
    for _ in range(steps):
        password = f"{password[-1]}{password[0:-1]}"
    return password

def reverse_positions(password: str, x: int, y: int) -> str:
    return f"{password[0:x]}{''.join(char for char in reversed(password[x:y+1]))}{password[y+1:]}"

def move_position(password: str, x: int, y: int) -> str:
    ltr = password[x]
    if x < y:
        return f"{password[0:x]}{password[x+1:y]}{password[y]}{ltr}{password[y+1:]}"
    else:
        return f"{password[0:y]}{ltr}{password[y:x]}{password[x+1:]}"

def execute_instruction(password: str, inst: str):
    match inst.split(' '):
        case ('swap', 'position', x, _, _, y):
            password = swap_position(password, int(x), int(y))
        case ('swap', 'letter', x, _, _, y):
            password = swap_letter(password, x, y)
        case ('rotate', 'based', _, _, _, _, x):
            password = rotate_right(password, x)
        case ('rotate', dir, x, _):
            password = rotate_string(password, Direction(dir), int(x))
        case ('reverse', _, x, _, y):
            password = reverse_positions(password, int(x), int(y))
        case ('move', _, x, _, _, y):
            password = move_position(password, int(x), int(y))
    return password

def scramble_password(password: str, instructions: list[str]) -> str:
    for inst in instructions:
        password = execute_instruction(password, inst)
    return password

def part_one_tests():
    password = 'abcde'
    i = 1
    for inst, answer in PART_ONE_TESTS:
        password = execute_instruction(password, inst)
        print(f"Step {i} ({inst}):  {password} {password == answer}")
        i += 1
    
def part_one(data: str):
    instructions = data.splitlines()
    password = START
    return scramble_password(password, instructions)
    
def part_two(data: str):
    instructions = data.splitlines()
    scrambled = 'fbgdceah'
    for x in itertools.permutations(scrambled):
        s = ''.join(char for char in x)
        if scramble_password(s, instructions) == scrambled:
            return s

def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()