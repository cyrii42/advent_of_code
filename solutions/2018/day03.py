from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 5,5: 2x2\n'
INPUT = aoc.get_input(YEAR, DAY)

class Point(NamedTuple):
    row: int
    col: int

@dataclass
class Claim:
    id: int
    inches_from_left: int
    inches_from_top: int
    width: int
    height: int

    def get_coordinates(self) -> list[Point]:
        start = Point(row=self.inches_from_top,
                      col=self.inches_from_left)
        output_list = []
    
        for row in range(self.height):
            for col in range(self.width):
                pt_row = start.row + row
                pt_col = start.col + col
                output_list.append(Point(pt_row, pt_col))
        return output_list

def make_claim_dict(claim_list: list[Claim]
                        ) -> dict[int, list[Point]]:
    return {claim.id: claim.get_coordinates() for claim in claim_list}

def find_overlaps(claim_dict: dict[int, list[Point]]) -> set[Point]:
    points_seen = set()
    repeated_points = set()
    for point_list in claim_dict.values():
        for point in point_list:
            if point in points_seen:
                repeated_points.add(point)
            else:
                points_seen.add(point)
    return repeated_points

def parse_data(data: str) -> list[Claim]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        id, _ , inches, rect = line.split(' ')
        id = int(id.removeprefix('#'))
        inches_from_left, inches_from_top = (
            [int(x) for x in inches.removesuffix(':').split(',')])
        width, height = [int(x) for x in rect.split('x')]
        output_list.append(Claim(id, inches_from_left, 
                                     inches_from_top, width, height))
    return output_list

def part_one(data: str):
    claim_list = parse_data(data)
    claim_dict = make_claim_dict(claim_list)
    repeated_points = find_overlaps(claim_dict)
    return len(repeated_points)  

def part_two(data: str):
    claim_list = parse_data(data)
    claim_dict = make_claim_dict(claim_list)
    repeated_points = find_overlaps(claim_dict)
    for claim_id, points_list in claim_dict.items():
        if not any(p in repeated_points for p in points_list):
            return claim_id

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()