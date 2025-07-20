'''--- Day 10: Pipe Maze ---'''

from dataclasses import dataclass, field
from enum import Enum


class Pipe(Enum):
    START = 'S'
    VERTICAL = '|'
    HORIZONTAL = '-'
    NORTH_TO_EAST = 'L'
    NORTH_TO_WEST = 'J'
    SOUTH_TO_EAST = 'F'
    SOUTH_TO_WEST = '7'
    GROUND = '.'

class Direction(Enum):
    NORTH = 'N'
    NORTH_EAST = 'NE'
    EAST = 'E'
    SOUTH_EAST = 'SE'
    SOUTH = 'S'
    SOUTH_WEST = 'SW'
    WEST = 'W'
    NORTH_WEST = 'NW'

@dataclass
class MapChar():
    row_num: int
    index: int
    char: Pipe #= field(repr=False)
    north: Pipe = field(repr=False)
    east: Pipe = field(repr=False)
    south: Pipe = field(repr=False)
    west: Pipe = field(repr=False)
    connection_1: Direction | None = field(init=False)
    connection_2: Direction | None = field(init=False)

    def __post_init__(self) -> None:
        self.find_connections_from_start() if self.char == Pipe.START else self.find_connections()

    def find_connections(self) -> None:
        if self.char == Pipe.VERTICAL:
            self.connection_1 = Direction('N') if self.north else None
            self.connection_2 = Direction('S') if self.south else None
        elif self.char == Pipe.HORIZONTAL:
            self.connection_1 = Direction('E') if self.east else None
            self.connection_2 = Direction('W') if self.west else None
        elif self.char == Pipe.NORTH_TO_EAST:
            self.connection_1 = Direction('N') if self.north else None
            self.connection_2 = Direction('E') if self.east else None
        elif self.char == Pipe.NORTH_TO_WEST:
            self.connection_1 = Direction('N') if self.north else None
            self.connection_2 = Direction('W') if self.west else None
        elif self.char == Pipe.SOUTH_TO_EAST:
            self.connection_1 = Direction('S') if self.south else None
            self.connection_2 = Direction('E') if self.east else None
        elif self.char == Pipe.SOUTH_TO_WEST:
            self.connection_1 = Direction('S') if self.south else None
            self.connection_2 = Direction('W') if self.west else None
        else:
            self.connection_1 = None
            self.connection_2 = None

    def find_connections_from_start(self) -> None:
        conn_list = []
        if self.north == Pipe.VERTICAL or self.north == Pipe.SOUTH_TO_EAST or self.north == Pipe.SOUTH_TO_WEST:
            conn_list.append(Direction('N')) if self.north else conn_list.append(None)
        if self.east == Pipe.HORIZONTAL or self.east == Pipe.NORTH_TO_WEST or self.east == Pipe.SOUTH_TO_WEST:
            conn_list.append(Direction('E')) if self.east else conn_list.append(None)
        if self.south == Pipe.VERTICAL or self.south == Pipe.NORTH_TO_EAST or self.south == Pipe.NORTH_TO_WEST:
            conn_list.append(Direction('S')) if self.south else conn_list.append(None)
        if self.west == Pipe.HORIZONTAL or self.west == Pipe.NORTH_TO_EAST or self.west == Pipe.SOUTH_TO_EAST:
            conn_list.append(Direction('W')) if self.west else conn_list.append(None)
        if len(conn_list) != 2:
            raise ConnectionNumError(f"Starting MapChar must have exactly 2 connections; this one has {len(conn_list)}")
        else:
            self.connection_1 = conn_list[0]
            self.connection_2 = conn_list[1]

@dataclass
class Map():
    char_list: list[MapChar] = field(repr=False)
    starting_point: MapChar = field(init=False)
    steps_to_farthest_point: int = field(init=False)

    def __post_init__(self) -> None:
        self.starting_point = next(filter(lambda x: x.char == Pipe.START, self.char_list))
        self.steps_to_farthest_point = self.calculate_steps_to_farthest_point()

    def calculate_steps_to_farthest_point(self) -> int:
        current_pipe = self.starting_point
        previous_pipe = current_pipe
        steps = 0
        while True:
            print(f"Trying {current_pipe}...")
            if steps == 0:
                next_pipe = self.get_mapchar_from_direction(current_pipe, current_pipe.connection_1)
            elif self.get_mapchar_from_direction(current_pipe, current_pipe.connection_1) != previous_pipe:
                next_pipe = self.get_mapchar_from_direction(current_pipe, current_pipe.connection_1)
            else:
                next_pipe = self.get_mapchar_from_direction(current_pipe, current_pipe.connection_2)
            if steps > 0 and next_pipe.char == Pipe.START:
                print(f"Found Pipe:  {next_pipe}")
                return steps // 2 + 1
            previous_pipe = current_pipe
            current_pipe = next_pipe
            steps += 1

    def get_mapchar_from_direction(self, mapchar: MapChar, direction: Direction) -> MapChar:
        if direction == Direction.NORTH:
            return next(filter(lambda x: x.row_num == mapchar.row_num-1 and x.index == mapchar.index, self.char_list))
        if direction == Direction.EAST:
            return next(filter(lambda x: x.row_num == mapchar.row_num and x.index == mapchar.index+1, self.char_list))
        if direction == Direction.SOUTH:
            return next(filter(lambda x: x.row_num == mapchar.row_num+1 and x.index == mapchar.index, self.char_list))
        if direction == Direction.WEST:
            return next(filter(lambda x: x.row_num == mapchar.row_num and x.index == mapchar.index-1, self.char_list))

    


def main():
    map = create_map()
    print(map.starting_point)
    print(f"\nPart One Answer:  {map.steps_to_farthest_point}")  # 13957 is too high; 6978 is too low

    
def create_map() -> Map:
    with open('./inputs/day10.txt') as file:
        line_list = file.read().split(sep='\n')

    map_char_list = []
    for row_num, row in enumerate(line_list):
        if row_num == 0:
            map_char_list.append(
                [MapChar(row_num, i, Pipe(char), 
                        None,                                                       # north
                        Pipe(line_list[row_num][i+1]) if i < len(row)-1 else None,    # east
                        Pipe(line_list[row_num+1][i]),                              # south
                        Pipe(line_list[row_num][i-1]),                              # west
                    ) for (i, char) in enumerate(row)])
        elif row_num >= len(line_list)-1:
            map_char_list.append(
                [MapChar(row_num, i, Pipe(char), 
                        Pipe(line_list[row_num-1][i]),                              # north
                        Pipe(line_list[row_num][i+1]) if i < len(row)-1 else None,    # east
                        None,                                                       # south
                        Pipe(line_list[row_num][i-1]),                              # west
                    ) for (i, char) in enumerate(row)])
        else:
            map_char_list.append(
                [MapChar(row_num, i, Pipe(char), 
                        Pipe(line_list[row_num-1][i]),                              # north
                        Pipe(line_list[row_num][i+1]) if i < len(row)-1 else None,    # east
                        Pipe(line_list[row_num+1][i]),                              # south
                        Pipe(line_list[row_num][i-1]),                              # west
                    ) for (i, char) in enumerate(row)])
            
    return Map([char for row in map_char_list for char in row])


class ConnectionNumError(Exception):
    ''' To be raised when a `MapChar` has less or more than 2 connections.'''
    pass

if __name__ == '__main__':
    main()
