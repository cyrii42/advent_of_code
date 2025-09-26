from pathlib import Path

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)
EXAMPLE_PART_ONE = 'abcdef\nbababc\nabbcde\nabcccd\naabcdd\nabcdee\nababab'
EXAMPLE_PART_TWO = 'abcde\nfghij\nklmno\npqrst\nfguij\naxcye\nwvxyz\n'

class NoBoxesFound(Exception):
    pass

def contains_two(box: str) -> bool:
    return any(box.count(char) == 2 for char in box)

def contains_three(box: str) -> bool:
    return any(box.count(char) == 3 for char in box)
    
def part_one(data: str):
    box_list = data.splitlines()
    num_two = len([box for box in box_list if contains_two(box)])
    num_three = len([box for box in box_list if contains_three(box)])
    return num_two * num_three

def count_position_differences(box1: str, box2: str) -> int:
    count = 0
    for i in range(len(box1)):
        if box1[i] != box2[i]:
            count += 1
    return count

def find_fabric_boxes(box_list: list[str]) -> tuple[str, str]:
    for box1 in box_list:
        for box2 in box_list:
            if box1 != box2 and count_position_differences(box1, box2) == 1:
                return (box1, box2)
    raise NoBoxesFound

def find_common_letters(box1: str, box2: str) -> str:
    output = ''
    for i in range(len(box1)):
        if box1[i] == box2[i]:
            output += box1[i]
    return output

def part_two(data: str):
    box_list = data.splitlines()
    (box1, box2) = find_fabric_boxes(box_list)
    return find_common_letters(box1, box2)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE_PART_ONE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()