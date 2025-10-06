import itertools
from pathlib import Path

from alive_progress import alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)
TESTS_PART_ONE = [
    ('18', (33, 45), 29),
    ('42', (21, 61), 30)
]
TESTS_PART_TWO = [
    ('18', (90, 269, 16), 113),
    ('42', (232, 251, 12), 119)
]

MIN_X = 1
MAX_X = 300
MIN_Y = 1
MAX_Y = 300

def get_power_level(x: int, y: int, serial_number: int):  
    rack_ID = x + 10
    power_level = ((rack_ID * y) + serial_number) * rack_ID
    power_level = power_level // 100 % 10   # get hundreds digit
    power_level = power_level - 5
    return power_level

def create_grid(serial_number: int):
    output_dict = {}
    for x in range(MIN_X, MAX_X+1):
        for y in range(MIN_Y, MAX_Y+1):
            output_dict[(x, y)] = get_power_level(x, y, serial_number)
    return output_dict

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        serial_number, top_left_corner, total_power = example
        print(f"Test #{i}: {part_one(serial_number) == top_left_corner}",
              f"({part_one(serial_number)})")
    
def part_one(data: str):
    serial_number = int(data)
    grid = create_grid(serial_number)

    start_x = 1
    start_y = 1
    highest_power_so_far = -999999
    answer = None
    for start_x in range(MIN_X, MAX_X-2):
        for start_y in range(MIN_Y, MAX_Y-2):
            sub_grid = [(start_x+delta_x, start_y+delta_y) 
                        for delta_x, delta_y 
                        in itertools.product(range(0, 3), repeat=2)]

            total_power = 0
            for x, y in sub_grid:
                total_power += grid[(x, y)]

            if total_power > highest_power_so_far:
                highest_power_so_far = total_power
                answer = (start_x, start_y)
    return answer
    
def part_two_tests():
    for i, example in enumerate(TESTS_PART_TWO, start=1):
        serial_number, top_left_corner, total_power = example
        test_answer = part_two(serial_number)
        print(f"Test #{i}: {test_answer == top_left_corner} ({test_answer})")

def part_two(data: str, print_info: bool = False):
    serial_number = int(data)
    grid = create_grid(serial_number)

    start_x = 1
    start_y = 1
    highest_power_so_far = -999999
    answer = None
    for size in alive_it(range(1, 21)):
        for start_x in range(MIN_X, MAX_X-2):
            for start_y in range(MIN_Y, MAX_Y-2):
                sub_grid = ((start_x+delta_x, start_y+delta_y) 
                            for delta_x, delta_y 
                            in itertools.product(range(0, size), repeat=2)
                            if start_x+delta_x <= MAX_X
                            and start_y+delta_y <= MAX_Y)

                total_power = 0
                for x, y in sub_grid:
                    total_power += grid[(x, y)]

                if total_power > highest_power_so_far:
                    if print_info:
                        print(f"New highest power:  {total_power} {(start_x, start_y, size)}")
                    highest_power_so_far = total_power
                    answer = (start_x, start_y, size)
    return answer



def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    part_two_tests()
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()