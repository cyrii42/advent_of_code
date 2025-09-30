from enum import IntEnum
from pathlib import Path
from typing import NamedTuple
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class NoCoordinateFound(Exception):
    pass

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

DIRECTION_DELTAS = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}

class Point(NamedTuple):
    row: int
    col: int

class Coordinate(Point):
    pass

def get_grid_dimensions(coordinate_list: list[Coordinate]) -> tuple[int, int]:
    max_row = max(coordinate.row for coordinate in coordinate_list)
    max_col = max(coordinate.col for coordinate in coordinate_list)

    higher_num = max(max_row, max_col)
    return (higher_num, higher_num)

def get_manhattan_distance(p1: Point, p2: Point) -> int:
    return abs(p1.row - p2.row) + abs(p1.col - p2.col)

def create_coordinate_distance_dict(coordinate_list: list[Coordinate]
                                    ) -> dict[Coordinate, dict[Point, int]]:
    max_row, max_col = get_grid_dimensions(coordinate_list)

    output_dict = {}
    for c in coordinate_list:
        sub_dict = {}
        for row in range(max_row+1):
            for col in range(max_col+1):
                point = Point(row, col)
                if point in coordinate_list:
                    sub_dict[Coordinate(row, col)] = get_manhattan_distance(point, c)
                else:
                    sub_dict[point] = get_manhattan_distance(point, c)
        output_dict[c] = sub_dict
    return output_dict

def find_closest_coordinate(point: Point, 
                            coordinate_distance_dict: dict[Coordinate, dict[Point, int]]
                            ) -> Coordinate | None:
    distance_dict = {c: coordinate_distance_dict[c][point] 
                     for c in coordinate_distance_dict.keys()}
    closest_distance = min(v for v in distance_dict.values())
    if len([v for v in distance_dict.values() if v == closest_distance]) > 1:
        return None
    else:
        closest_point = sorted([(k, v) for k, v in distance_dict.items()], 
                               key=lambda x: x[1])[0][0]
        return closest_point

def create_closest_coordinate_dict(c_distance_dict: dict[Coordinate, dict[Point, int]]
                                  ) -> dict[Point, Coordinate|None]:
    coordinate_list = [c for c in c_distance_dict.keys()]
    max_row, max_col = get_grid_dimensions(coordinate_list)

    output_dict = {}
    for row in range(max_row+1):
        for col in range(max_col+1):
            point = Point(row, col)
            if point in coordinate_list:
                coordinate = Coordinate(*point)
                output_dict[coordinate] = find_closest_coordinate(point, 
                                                                  c_distance_dict)
            else:
                output_dict[point] = find_closest_coordinate(point, 
                                                             c_distance_dict)
    return output_dict

def create_coordinate_area_dict(closest_coordinate_dict: dict[Point, Coordinate|None]
                                ) -> dict[Coordinate, list[Point]]:
    coordinate_set = {c for c in closest_coordinate_dict.values() if c}

    output_dict = {}
    for coordinate in coordinate_set:
        output_dict[coordinate] = [p for p, c in closest_coordinate_dict.items() 
                                   if p and c == coordinate]
    return output_dict

def find_largest_finite_area(coordinate_area_dict: dict[Coordinate, list[Point]],
                             max_row: int,
                             max_col: int
                             ) -> int:
    filtered_list = [area_list for area_list in coordinate_area_dict.values()
                     if not any(point.row == 0 for point in area_list)
                     and not any(point.row == max_row for point in area_list)
                     and not any(point.col == 0 for point in area_list)
                     and not any(point.col == max_col for point in area_list)]
    return max(len(area_list) for area_list in filtered_list)

def parse_data(data: str) -> list[Coordinate]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        col, row = [int(x) for x in line.split(',')]
        output_list.append(Coordinate(row, col))
    return output_list
    
def part_one(data: str):
    coordinate_list = parse_data(data)
    coordinate_distance_dict = create_coordinate_distance_dict(coordinate_list)
    closest_coordinate_dict = create_closest_coordinate_dict(coordinate_distance_dict)
    coordinate_area_dict = create_coordinate_area_dict(closest_coordinate_dict)
    max_row, max_col = get_grid_dimensions(coordinate_list)
    return find_largest_finite_area(coordinate_area_dict, max_row, max_col)

def get_size_of_central_region(coordinate_list: list[Coordinate]) -> int:
    max_row, max_col = get_grid_dimensions(coordinate_list)
    answer = 0
    for row in range(max_row+1):
        for col in range(max_col+1):
            point = Point(row, col)
            total_distance = sum(get_manhattan_distance(point, c) for c in coordinate_list)
            if total_distance < 10_000:
                answer += 1
    return answer         

def part_two(data: str):
    coordinate_list = parse_data(data)
    return get_size_of_central_region(coordinate_list)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()