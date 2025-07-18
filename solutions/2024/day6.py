'''--- Day 6: Guard Gallivant ---'''

import datetime as dt
from pathlib import Path
from rich import print
from copy import deepcopy
from typing import NamedTuple, Optional
from enum import Enum
from dataclasses import dataclass, field
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day6_example.txt'
INPUT = DATA_DIR / 'day6_input.txt'

class Point(NamedTuple):
    col: int
    row: int
    char: str

class Obstacle(Point):
    ...

class MapEdge(Point):
    ...

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

@dataclass
class MapRow():
    point_list: list[Point]
    row_num: int
    total_map_height: int

    @property
    def width(self):
        return len(self.point_list)

    def get_point(self, col_num: int) -> Point:
        return self.point_list[col_num]


@dataclass
class Map():
    row_list: list[MapRow]

    @property
    def height(self):
        return len(self.row_list)

    @property
    def width(self):
        return self.row_list[0].width

    def get_row(self, y: int) -> MapRow:
        return self.row_list[y]

    def get_point(self, row_num: int, col_num: int) -> Point:
        row = self.row_list[row_num]
        return row.get_point(col_num)

class InfiniteLoop(Exception):
    ...

    
@dataclass
class Guard():
    point: Point
    map: Map = field(repr=False)
    total_positions: int = field(default=1, repr=False)
    positions_visited: set[Point] = field(default_factory=set, repr=False)
    positions_directions_visited: set[tuple[Point, Direction]] = field(default_factory=set, repr=False)

    def __post_init__(self):
        self.direction = self.get_initial_direction()

    def get_initial_direction(self) -> Direction:
        match self.point.char:
            case '^':
                return Direction.UP
            case '>':
                return Direction.RIGHT
            case 'v':
                return Direction.DOWN
            case '<':
                return Direction.LEFT
            case _:
                raise ValueError

    def rotate(self) -> None:
        new_value = (self.direction.value + 1) % 4
        self.direction = Direction(new_value)

    def increment_position_counter(self, next_point: Point) -> None:
        if (next_point, self.direction) in self.positions_directions_visited:
            raise InfiniteLoop
        if not next_point in self.positions_visited:
            self.total_positions += 1
            self.positions_visited.add(next_point)
            self.positions_directions_visited.add((next_point, self.direction))      
        
    def find_next_point(self) -> Point:
        ''' Determine the next point based on current direction.  If next point is an obstacle, rotate and try again.'''
        current_row = self.point.row
        current_col = self.point.col
        
        match self.direction:
            case Direction.UP:
                next_point = self.map.get_point(current_row - 1, current_col)
            case Direction.RIGHT:
                next_point = self.map.get_point(current_row, current_col + 1)
            case Direction.DOWN:
                next_point = self.map.get_point(current_row + 1, current_col)
            case Direction.LEFT:
                next_point = self.map.get_point(current_row, current_col - 1)
                
        if isinstance(next_point, Obstacle):
            self.rotate()
            return self.find_next_point()
        else:
            self.increment_position_counter(next_point)
            return next_point
 
    def patrol(self) -> int:
        ''' If current position is an edge of the map, we're done, so return the total moves. 
        Otherwise, increment `total_positions`, move to the next position, and try again.'''
        self.positions_visited.add(self.point)
        while True:
            if isinstance(self.map.get_point(self.point.row, self.point.col), MapEdge):
                return self.total_positions  # we found an exit!
            else:
                self.point = self.find_next_point()
          

def find_guard(map: Map) -> Guard:
    for row in map.row_list:
        for point in row.point_list:
            if point.char in ['^', '>', '<', 'v']:
                return Guard(point, map)
    raise ValueError("Could not find a guard position in map.")


def create_map_row(line: str, row_num: int, total_map_height: int) -> MapRow:
    total_map_width = len(line)
    point_list = []
    
    for col_num, char in enumerate(line):
        if char == '#':
            point_list.append(Obstacle(col_num, row_num, char))
        elif row_num == 0 or row_num == (total_map_height - 1) or col_num == 0 or col_num == (total_map_width - 1):
            point_list.append(MapEdge(col_num, row_num, char))
        else:
            point_list.append(Point(col_num, row_num, char))
            
    return MapRow(point_list, row_num, total_map_height)


def create_map(filename: Path) -> Map:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    row_list = [create_map_row(line, row_num, len(line_list)) for row_num, line in enumerate(line_list)]
        
    return Map(row_list)

def find_loops(first_guard: Guard, points_to_check: list[Point]) -> int:
    total = 0
    for visited_point in alive_it(points_to_check):
        new_map = Map(deepcopy(first_guard.map.row_list))
        new_obstacle = Obstacle(visited_point.col, visited_point.row, '#')
        new_map.row_list[visited_point.row].point_list[visited_point.col] = new_obstacle
        new_guard = find_guard(new_map)
        try:
            new_guard.patrol()
        except InfiniteLoop:
            total += 1
    return total


def part_one(filename: Path) -> int:
    map = create_map(filename)
    guard = find_guard(map)
    answer = guard.patrol()
    return answer


def part_two(filename: Path) -> int:
    map = create_map(filename)
    guard = find_guard(map)
    guard.patrol()

    points_to_check = [point for point in guard.positions_visited if not isinstance(point, Obstacle) and point.char not in ['^', '>', '<', 'v']]
    answer = find_loops(guard, points_to_check)
    return answer


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # should be 41
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # should be 6
    print(f"Part Two (input):  {part_two(INPUT)}")


if __name__ == '__main__':
    main()