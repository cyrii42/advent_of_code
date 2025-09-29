import sys
from pathlib import Path

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = 'dabAcCaCBAcCcaDA'
INPUT = aoc.get_input(YEAR, DAY)

sys.setrecursionlimit(10**6)

def find_reacting_units(unit1: str, unit2: str) -> bool:
    if unit1 == unit2:
        return False
    if unit1.lower() != unit2.lower():
        return False
    return True

def simulate_reactions(polymer: str) -> str:
    i = 0
    output = ''
    while i < len(polymer):
        if i == len(polymer) - 1:
            output += polymer[i]
            break
        unit1, unit2 = polymer[i], polymer[i+1]
        if find_reacting_units(unit1, unit2):
            i += 2
            continue
        else:
            output += unit1
            i += 1

    if output == polymer:
        return output
    else:
        return simulate_reactions(output)
    
def part_one(data: str):
    polymer = data
    polymer = simulate_reactions(polymer)
    return len(polymer)

def part_two(data: str):
    polymer = data
    letters = set(polymer.upper())

    result_dict = {}
    for letter in letters:
        test_polymer = ''.join(char for char in polymer if char.upper() != letter)
        result = simulate_reactions(test_polymer)
        print(len(result))
        result_dict[letter] = len(result)
    return min(result for result in result_dict.values())

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()