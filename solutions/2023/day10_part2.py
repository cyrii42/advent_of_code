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
    north_east: Pipe = field(repr=False)
    east: Pipe = field(repr=False)
    south_east: Pipe = field(repr=False)
    south: Pipe = field(repr=False)
    south_west: Pipe = field(repr=False)
    west: Pipe = field(repr=False)
    north_west: Pipe = field(repr=False)
    connection_1: Direction | None = field(init=False)
    connection_2: Direction | None = field(init=False)
    part_of_main_loop: bool = False

    def __post_init__(self) -> None:
        self.find_connections_from_start() if self.char == Pipe.START else self.find_connections()

    def find_connections(self) -> None:
        if self.char == Pipe.VERTICAL:
            self.connection_1 = Direction('N') if self.north is not None else None
            self.connection_2 = Direction('S') if self.south is not None else None
        elif self.char == Pipe.HORIZONTAL:
            self.connection_1 = Direction('E') if self.east is not None else None
            self.connection_2 = Direction('W') if self.west is not None else None
        elif self.char == Pipe.NORTH_TO_EAST:
            self.connection_1 = Direction('N') if self.north is not None else None
            self.connection_2 = Direction('E') if self.east is not None else None
        elif self.char == Pipe.NORTH_TO_WEST:
            self.connection_1 = Direction('N') if self.north is not None else None
            self.connection_2 = Direction('W') if self.west is not None else None
        elif self.char == Pipe.SOUTH_TO_EAST:
            self.connection_1 = Direction('S') if self.south is not None else None
            self.connection_2 = Direction('E') if self.east is not None else None
        elif self.char == Pipe.SOUTH_TO_WEST:
            self.connection_1 = Direction('S') if self.south is not None else None
            self.connection_2 = Direction('W') if self.west is not None else None
        else:
            self.connection_1 = None
            self.connection_2 = None

    def find_connections_from_start(self) -> None:
        conn_list = []
        if self.north == Pipe.VERTICAL or self.north == Pipe.SOUTH_TO_EAST or self.north == Pipe.SOUTH_TO_WEST:
            conn_list.append(Direction('N')) if self.north is not None else conn_list.append(None)
        if self.east == Pipe.HORIZONTAL or self.east == Pipe.NORTH_TO_WEST or self.east == Pipe.SOUTH_TO_WEST:
            conn_list.append(Direction('E')) if self.east is not None else conn_list.append(None)
        if self.south == Pipe.VERTICAL or self.south == Pipe.NORTH_TO_EAST or self.south == Pipe.NORTH_TO_WEST:
            conn_list.append(Direction('S')) if self.south is not None else conn_list.append(None)
        if self.west == Pipe.HORIZONTAL or self.west == Pipe.NORTH_TO_EAST or self.west == Pipe.SOUTH_TO_EAST:
            conn_list.append(Direction('W')) if self.west is not None else conn_list.append(None)
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
        self.tiles_enclosed_by_loop = self.calculate_tiles_enclosed_by_loop()

    def calculate_tiles_enclosed_by_loop(self) -> int:
        total = 0
        for mapchar in self.char_list:
            if mapchar.part_of_main_loop:
                continue
            else:
                # print([dir for dir in Direction.__iter__()])
                print(f"Checking {mapchar}...")
                char_list = [self.get_mapchar_from_direction(mapchar, dir) for dir in Direction.__iter__()]
                # print(f"Checking {char_list}")
                if any([char for char in char_list if char is None or char.part_of_main_loop == False]):
                    continue
            total += 1
        return total

    def calculate_steps_to_farthest_point(self) -> int:
        current_pipe = self.starting_point
        previous_pipe = current_pipe
        current_pipe.part_of_main_loop = True
        steps = 0
        while True:
            print(f"Trying {current_pipe}...")
            if steps == 0:
                next_pipe = self.get_mapchar_from_direction(current_pipe, current_pipe.connection_1)
            elif self.get_mapchar_from_direction(current_pipe, current_pipe.connection_1) != previous_pipe:
                next_pipe = self.get_mapchar_from_direction(current_pipe, current_pipe.connection_1)
            else:
                next_pipe = self.get_mapchar_from_direction(current_pipe, current_pipe.connection_2)
            next_pipe.part_of_main_loop = True
            if steps > 0 and next_pipe.char == Pipe.START:
                print(f"Found Pipe:  {next_pipe}")
                return steps // 2 + 1
            previous_pipe = current_pipe
            current_pipe = next_pipe
            steps += 1

    def get_mapchar_from_direction(self, mapchar: MapChar, direction: Direction) -> MapChar:
        if direction == Direction.NORTH:
            return None if mapchar.row_num == 0 else next(filter(lambda x: x.row_num == mapchar.row_num-1 and x.index == mapchar.index, self.char_list))
        if direction == Direction.NORTH_EAST:
            return None if mapchar.row_num == 0 or mapchar.index == 139 else next(filter(lambda x: x.row_num == mapchar.row_num-1 and x.index == mapchar.index+1, self.char_list))
        if direction == Direction.EAST:
            return None if mapchar.index == 139 else next(filter(lambda x: x.row_num == mapchar.row_num and x.index == mapchar.index+1, self.char_list))
        if direction == Direction.SOUTH_EAST:
            return None if mapchar.row_num == 139 or mapchar.index == 139 else next(filter(lambda x: x.row_num == mapchar.row_num+1 and x.index == mapchar.index+1, self.char_list))
        if direction == Direction.SOUTH:
            return None if mapchar.row_num == 139 else next(filter(lambda x: x.row_num == mapchar.row_num+1 and x.index == mapchar.index, self.char_list))
        if direction == Direction.SOUTH_WEST:
            return None if mapchar.row_num == 139 or mapchar.index == 0 else next(filter(lambda x: x.row_num == mapchar.row_num+1 and x.index == mapchar.index-1, self.char_list))
        if direction == Direction.WEST:
            return  None if mapchar.index == 0 else next(filter(lambda x: x.row_num == mapchar.row_num and x.index == mapchar.index-1, self.char_list))
        if direction == Direction.NORTH_WEST:
            return None if mapchar.row_num == 0 or mapchar.index == 0 else next(filter(lambda x: x.row_num == mapchar.row_num-1 and x.index == mapchar.index-1, self.char_list))

    


def main():
    map = create_map()
    print(map.starting_point)
    print(f"\nPart Two Answer:  {map.tiles_enclosed_by_loop}")  # 322 is too low

    
def create_map() -> Map:
    with open('./inputs/day10.txt') as file:
        line_list = file.read().split(sep='\n')

    map_char_list = []
    for row_num, row in enumerate(line_list):
        if row_num == 0:
            map_char_list.append(
                [MapChar(row_num, i, Pipe(char), 
                        None,                                                       # north
                        None,                                                       # north_east
                        Pipe(line_list[row_num][i+1]) if i < len(row)-1 else None,    # east
                        Pipe(line_list[row_num+1][i+1]) if i< len(row)-1 else None,   # south_east
                        Pipe(line_list[row_num+1][i]),                              # south
                        Pipe(line_list[row_num+1][i-1]),                              # south_west
                        Pipe(line_list[row_num][i-1]),                              # west
                        None,                                                         # north_west
                    ) for (i, char) in enumerate(row)])
        elif row_num >= len(line_list)-1:
            map_char_list.append(
                [MapChar(row_num, i, Pipe(char), 
                        Pipe(line_list[row_num-1][i]),                              # north
                        Pipe(line_list[row_num-1][i+1])  if i < len(row)-1 else None, # north_east
                        Pipe(line_list[row_num][i+1]) if i < len(row)-1 else None,    # east
                        None,                                                       # south_east
                        None,                                                       # south
                        None,                                                         # south_west
                        Pipe(line_list[row_num][i-1]),                              # west
                        Pipe(line_list[row_num-1][i-1]),                              # north_west
                    ) for (i, char) in enumerate(row)])
        else:
            map_char_list.append(
                [MapChar(row_num, i, Pipe(char), 
                        Pipe(line_list[row_num-1][i]),                              # north
                        Pipe(line_list[row_num-1][i+1]) if i < len(row)-1 else None,  # north_east
                        Pipe(line_list[row_num][i+1]) if i < len(row)-1 else None,    # east
                        Pipe(line_list[row_num+1][i+1]) if i< len(row)-1 else None,   # south_east
                        Pipe(line_list[row_num+1][i]),                              # south
                        Pipe(line_list[row_num+1][i-1]),                              # south_west
                        Pipe(line_list[row_num][i-1]),                              # west
                        Pipe(line_list[row_num-1][i-1]),                              # north_west
                    ) for (i, char) in enumerate(row)])
            
    return Map([char for row in map_char_list for char in row])


class ConnectionNumError(Exception):
    ''' To be raised when a `MapChar` has less or more than 2 connections.'''
    pass

if __name__ == '__main__':
    main()
