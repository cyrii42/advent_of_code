import pathlib

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.DATA_DIR / '2016.07_examples.txt'
EXAMPLE_PART_TWO = aoc.DATA_DIR / '2016.07_examples_part_two.txt'
INPUT = aoc.DATA_DIR / '2016.07_input.txt'

def parse_data(data_file: pathlib.Path):
    with open(data_file, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    return line_list

def is_abba(seq: str) -> bool:
    return (all(char.isalpha() for char in seq) 
            and seq[0] == seq[3] 
            and seq[1] == seq[2]
            and seq[0] != seq[1])

def supports_tls(ip: str) -> bool:
    hypernet = False
    abba_found = False

    for i in range(len(ip) - 3):
        if ip[i] == '[':
            hypernet = True
            continue
        if ip[i] == ']':
            hypernet = False
            continue

        if hypernet and is_abba(ip[i:i+4]):
            return False

        if not hypernet and is_abba(ip[i:i+4]):
            abba_found = True
            
    return abba_found
    
def part_one(data_file: pathlib.Path):
    ip_list = parse_data(data_file)
    return len([ip for ip in ip_list if supports_tls(ip)])

def is_aba(seq: str) -> bool:
    return (all(char.isalpha() for char in seq) 
            and seq[0] == seq[2] 
            and seq[0] != seq[1])

def is_bab(seq: str, aba: str) -> bool:
    return is_aba(seq) and seq[0] == aba[1] and seq[1] == aba[0]

def supports_ssl(ip: str) -> bool:
    hypernet = False
    aba_list = []

    for i in range(len(ip) - 2):
        if ip[i] == '[':
            hypernet = True
            continue
        if ip[i] == ']':
            hypernet = False
            continue

        if not hypernet and is_aba(ip[i:i+3]):
            aba_list.append(ip[i:i+3])

    if len(aba_list) == 0:
        return False

    for i in range(len(ip) - 2):
        if ip[i] == '[':
            hypernet = True
            continue
        if ip[i] == ']':
            hypernet = False
            continue
        
        if hypernet and any(is_bab(ip[i:i+3], aba) for aba in aba_list):
            return True
            
    return False

def part_two(data_file: pathlib.Path):
    ip_list = parse_data(data_file)
    return len([ip for ip in ip_list if supports_ssl(ip)])

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()