from pathlib import Path
from alive_progress import alive_bar
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def parse_data(data: str) -> int:
    return int(data)

def determine_house_presents(house_num: int) -> int:
    return sum(x*10 for x in range(1, house_num+1) if house_num % x == 0)

def part_one(data: str):
    target = parse_data(data)
    print(f"TARGET: {target}")

    n = 1
    with alive_bar() as bar:
        while True:
            if determine_house_presents(n) >= target:
                return n

            if n % 50_000 == 0:
                print(f"{n}: {determine_house_presents(n)}")
            bar()
            n += 1

            
def determine_house_presents_part_two(house_num: int) -> int:
    return 11 * sum([house_num // n for n in range(1, 51) if house_num % n == 0])

def part_two(data: str):   
    target = parse_data(data)
    print(f"TARGET: {target}")
    
    n = 1
    with alive_bar() as bar:
        while True:
            if determine_house_presents_part_two(n) >= target:
                return n
            else:
                n += 1
                bar()



def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()