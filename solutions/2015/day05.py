from pathlib import Path

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE_PART_ONE = 'ugknbfddgicrmopn\njchzalrnumimnmhp\nhaegwjzuvuyypxyu\ndvszwmarrgswjxmb'
EXAMPLE_PART_TWO = 'qjhvhtzxzqqjkmpb\nxxyxx\nuurcxstgmygtbstg\nieodomkazucvgmuy'
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

VOWELS = 'aeiou'
FORBIDDEN_STRINGS = ['ab', 'cd', 'pq', 'xy']

def find_repeated_letters(string: str) -> bool:
    for i, char in enumerate(string):
        if i+1 == len(string):
            return False
        if char == string[i+1]:
            return True
        
    return False

def determine_niceness_part_1(string: str) -> bool:
    num_vowels = len([char for char in string if char in VOWELS])
    if num_vowels < 3:
        return False

    if any(x in string for x in FORBIDDEN_STRINGS):
        return False

    return find_repeated_letters(string)

def apply_part_2_rule_1(string: str) -> bool:
    ''' Determines whether the input string contains a pair of any two 
    letters that appears at least twice in the string without overlapping, 
    like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps). '''
    ...
    pair_list = []
    for i, char in enumerate(string):
        if i+1 == len(string):
            return False
        if f"{char}{string[i+1]}" in pair_list:
            if char != string[i+1]: # if the pair isn't the same letter twice, we're good
                return True
            if i+2 == len(string): # if we're at the end of the string, we're good 
                return True
            if string[i+2] != char and string[i-1] != char:
                return True
        pair_list.append(f"{char}{string[i+1]}")
    return False
    

def apply_part_2_rule_2(string: str) -> bool:
    ''' Determine whether the input string contains at least one letter that 
    repeats with exactly one letter between them, like xyx, abcdefeghi (efe), 
    or even aaa. '''
    ...
    for i, char in enumerate(string):
        if i+2 == len(string):
            return False
        if char == string[i+2]:
            return True
        
    return False

def determine_niceness_part_2(string: str) -> bool:
    if not apply_part_2_rule_1(string):
        return False

    return apply_part_2_rule_2(string)

def parse_data(data: str) -> list[str]:
    return [line for line in data.split('\n') if line]
    
def part_one(data: str):
    string_list = parse_data(data)
    return len([x for x in string_list if determine_niceness_part_1(x)])

def part_two(data: str):
    string_list = parse_data(data)
    return len([x for x in string_list if determine_niceness_part_2(x)])



def main():
    print(f"Part One (example):  {part_one(EXAMPLE_PART_ONE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    # random_tests()

def random_tests():
    for x in EXAMPLE_PART_TWO.split('\n'):
        print(f"{x}: {apply_part_2_rule_1(x)}")
    for x in EXAMPLE_PART_TWO.split('\n'):
        print(f"{x}: {apply_part_2_rule_2(x)}")

    strings_to_test = ['zurkakkkpchzxjhq', 'enamqzfzjunnnkpe']
    for string in strings_to_test:
        print(apply_part_2_rule_1(string))



       
if __name__ == '__main__':
    main()