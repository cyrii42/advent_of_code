import pathlib

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE_PART_ONE = '5 10 25'
EXAMPLE_PART_TWO = '101 301 501\n102 302 502\n103 303 503\n201 401 601\n202 402 602\n203 403 603'
INPUT = aoc.get_input(YEAR, DAY)

def parse_data_part_one(data: str) -> list[list[int]]:
    line_list = data.splitlines()
    return [[int(x) for x in line.strip().split()] for line in line_list]

def check_valid_triangle(nums: list[int]) -> bool:
    ''' In a valid triangle, the sum of any two sides must be larger than the remaining side. '''
    a, b, c = sorted(nums)
    return a + b > c
    
def part_one(data: str):
    nums_list = parse_data_part_one(data)
    return len([nums for nums in nums_list if check_valid_triangle(nums)])

def parse_data_part_two(data: str) -> list[list[int]]:
    line_list = data.splitlines()
    line_list = [[int(x) for x in line.strip().split()] for line in line_list]

    output_list = []
    for i in range(0, len(line_list), 3):
        output_list.append([line_list[i][0], line_list[i+1][0], line_list[i+2][0]])
        output_list.append([line_list[i][1], line_list[i+1][1], line_list[i+2][1]])
        output_list.append([line_list[i][2], line_list[i+1][2], line_list[i+2][2]])
        
    return output_list

def part_two(data: str):
    nums_list = parse_data_part_two(data)
    return len([nums for nums in nums_list if check_valid_triangle(nums)])

def main():
    print(f"Part One (example):  {part_one(EXAMPLE_PART_ONE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (input):  {part_two(EXAMPLE_PART_TWO)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()