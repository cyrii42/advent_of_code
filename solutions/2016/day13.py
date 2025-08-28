import pathlib
from collections import deque
from dataclasses import dataclass, field
from typing import NamedTuple

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)

NUM_ROWS = 50
NUM_COLS = 50
GOAL_X = 31
GOAL_Y = 39

DIRECTIONS = {
    'N':    (1, 0),
    'E':    (0, 1),
    'S':    (-1, 0),
    'W':    (0, -1),
}

class Node(NamedTuple):
    x: int
    y: int

def location_is_open(node: Node, fav_num: int) -> bool:
    x, y = node
    step1 = (x*x + 3*x + 2*x*y + y + y*y)
    step2 = step1 + fav_num
    step3 = str(bin(step2))[2:]
    step4 = len([char for char in step3 if char == '1'])
    return True if step4 % 2 == 0 else False

@dataclass
class Maze:
    num_rows: int
    num_cols: int
    fav_num: int
    goal_x: int
    goal_y: int
    graph: dict[Node, list[Node]] = field(default_factory=dict)

    def __post_init__(self):
        self.create_graph()

    def create_graph(self) -> None:
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                node = Node(x, y)
                potential_neighbors = [Node(x+i, y+j) for i, j in DIRECTIONS.values() 
                                       if x+i >= 0 and x+i < self.num_cols
                                       and y+j >= 0 and y+j < self.num_rows]
                neighbors = [node for node in potential_neighbors 
                             if location_is_open(node, self.fav_num)]
                self.graph[node] = neighbors

    def find_shortest_path(self, part_two: bool = False) -> int:
        start = Node(1, 1)
        end = Node(self.goal_x, self.goal_y)
        queue = deque([(start, [])])

        visited = set()
        visited.add(start)

        while queue:
            node, path = queue.popleft()
            if part_two and len(path) == 50:
                return len(visited)
            if node == end:
                return len(path)
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
                    visited.add(neighbor)
        return 0                    

def parse_data(data: str) -> Maze:
    fav_num = int(data)
    if data == '10':
        num_rows = 7
        num_cols = 10
        goal_x = 7
        goal_y = 4
    else:
        num_rows = NUM_ROWS
        num_cols = NUM_COLS
        goal_x = GOAL_X
        goal_y = GOAL_Y
        
    return Maze(num_rows, num_cols, fav_num, goal_x, goal_y)
        
def part_one(data: str):
    maze = parse_data(data)
    return maze.find_shortest_path()
    
def part_two(data: str):
    maze = parse_data(data)
    return maze.find_shortest_path(part_two=True)


def main():
    print(f"Part One (example):  {part_one('10')}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()