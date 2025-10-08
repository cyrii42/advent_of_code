import hashlib
import pathlib
from collections import deque
from dataclasses import dataclass, field
from enum import Enum

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE_TESTS_PART_ONE = [
    ('ihgpwlah', 'DDRRRD'),
    ('kglvqrro', 'DDUDRLRRUDRD'),
    ('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR')
]
EXAMPLE_TESTS_PART_TWO = [
    ('ihgpwlah', 370),
    ('kglvqrro', 492),
    ('ulqzkmiv', 830)
]
INPUT = aoc.get_input(YEAR, DAY)

START = (0, 0)
END = (3, 3)

MAX_X = 3
MAX_Y = 3

class Direction(Enum):
    U = 0
    D = 1
    L = 2
    R = 3

DIRECTION_DELTAS = {
    Direction.U: (0, -1),
    Direction.D: (0, 1),
    Direction.L: (-1, 0),
    Direction.R: (1, 0),
}

def get_hash(s: str):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

@dataclass
class Room():
    x: int
    y: int
    path: str
    passcode: str
    door_codes: str = field(init=False)
    door_status: dict[Direction, bool] = field(init=False)

    @property
    def num_open_doors(self) -> int:
        return len([x for x in self.door_status.values() if x])

    def __post_init__(self):
        self.door_codes = get_hash(f"{self.passcode}{self.path}")
        self.door_status = {d: self.is_open(d) for d in Direction}

    @property
    def hash(self) -> str:
        return f"{self.x}_{self.y}_{self.door_codes}"

    def get_valid_neighbors(self) -> list["Room"]:
        output_list = []
        for dir, delta in DIRECTION_DELTAS.items():
            if self.is_open(dir):
                dx, dy = delta
                output_list.append(Room(self.x + dx, 
                                        self.y + dy,
                                        path=self.path + dir.name,
                                        passcode=self.passcode))
        return output_list

    def is_open(self, dir: Direction) -> bool:
        if self.door_codes[dir.value] not in ['b', 'c', 'd', 'e', 'f']:
            return False

        match dir:
            case Direction.U:
                return self.y > 0
            case Direction.D:
                return self.y < MAX_Y
            case Direction.L:
                return self.x > 0
            case Direction.R:
                return self.x < MAX_X
    
@dataclass
class Maze:
    passcode: str
    path: str = field(default_factory=str)
    
    def get_room(self, x: int, y: int) -> Room:
        return Room(x=x, y=y, path=self.path, passcode=self.passcode)

    def find_path(self, part_two: bool = False):
        start = self.get_room(*START)
        end = END
        queue = deque([(start, [start])])

        visited = set()
        visited.add(start.hash)

        longest = 0
        while queue:
            room, path = queue.popleft()
            if (room.x, room.y) == end:
                if not part_two:
                    return room.path
                else:
                    longest = max(len(path)-1, longest)
            else:
                for neighbor in room.get_valid_neighbors():
                    if neighbor.hash not in visited:
                        new_path = path + [neighbor]
                        queue.append((neighbor, new_path))
                        visited.add(neighbor.hash)
        return longest

def part_one_tests():
    for i, example in enumerate(EXAMPLE_TESTS_PART_ONE, start=1):
        passcode, answer = example
        print(f"Test #{i} ({passcode}): {part_one(passcode) == answer} ({part_one(passcode)})")

def part_two_tests():
    for i, example in enumerate(EXAMPLE_TESTS_PART_TWO, start=1):
        passcode, answer = example
        print(f"Test #{i} ({passcode}): {part_two(passcode) == answer} ({part_two(passcode)})")
        
def part_one(data: str):
    maze = Maze(passcode=data)
    return maze.find_path()
    
def part_two(data: str):
    maze = Maze(passcode=data)
    return maze.find_path(part_two=True)

def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    part_two_tests()
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()