from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def calculate_surface_area(l: int, h: int, w: int) -> int:
    s1 = l*w
    s2 = w*h
    s3 = h*l
    smallest_side = min(s1, s2, s3)
    return (2*s1) + (2*s2) + (2*s3) + smallest_side

def get_smallest_perimeter(l: int, h: int, w: int) -> int:
    sorted_sides = sorted([l, h, w])
    s1 = sorted_sides[0]
    s2 = sorted_sides[1]
    return (2*s1) + (2*s2)

def calculate_volume(l: int, h: int, w: int) -> int:
    return l*h*w

def calculate_total_ribbon(l: int, h: int, w: int) -> int:
    return get_smallest_perimeter(l, h, w) + calculate_volume(l, h, w)

def read_data(data: str) -> list[tuple[int, int, int]]:
    line_list = [line for line in data.split('\n') if line]
    split_list = [line.split('x') for line in line_list]
    return [(int(x[0]), int(x[1]), int(x[2])) for x in split_list]
    
    
def part_one(data: str):
    boxes = read_data(data)
    return sum(calculate_surface_area(*box) for box in boxes)

def part_two(data: str):
    boxes = read_data(data)
    return sum(calculate_total_ribbon(*box) for box in boxes)



def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (input):  {part_two(INPUT)}")

    # random_tests()

def random_tests():
    print(get_smallest_perimeter(2, 3, 4) + calculate_volume(2, 3, 4))
    print(get_smallest_perimeter(1, 1, 10) + calculate_volume(1, 1, 10))

       
if __name__ == '__main__':
    main()