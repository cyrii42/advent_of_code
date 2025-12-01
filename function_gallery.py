from enum import Enum, IntEnum, StrEnum
from typing import NamedTuple, Callable, Any
from dataclasses import dataclass, field
from collections import deque

def run_tests(tests: list[tuple[str, Any]], fn: Callable):
    for i, example in enumerate(tests, start=1):
        data, answer = example
        test_answer = fn(data)
        print(f"Test #{i}: {test_answer == answer}",
              f"({test_answer})")

### FOUR DIRECTIONS
class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @property
    def left(self) -> "Direction":
        return Direction((self.value -1 ) % len(Direction))

    @property
    def right(self) -> "Direction":
        return Direction((self.value + 1) % len(Direction))

    @property
    def opposite(self) -> "Direction":
        num_dirs = len(Direction)
        return Direction((self.value + num_dirs // 2) % num_dirs)


### EIGHT DIRECTIONS
class Direction(IntEnum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7

    @property
    def left(self) -> "Direction":
        return Direction((self.value - 1) % len(Direction))

    @property
    def right(self) -> "Direction":
        return Direction((self.value + 1) % len(Direction))

    @property
    def opposite(self) -> "Direction":
        num_dirs = len(Direction)
        return Direction((self.value + num_dirs // 2) % num_dirs)


## for infinite positive grid beginning at upper left
DIRECTION_DELTAS = {      # ROW, COL
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}
DIRECTION_DELTAS = {      # X, Y
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
}

DIRECTION_DELTAS = {      # ROW, COL
    Direction.NORTH: (-1, 0),
    Direction.NORTHEAST: (-1, 1),
    Direction.EAST: (0, 1),
    Direction.SOUTHEAST: (1, 1),
    Direction.SOUTH: (1, 0),
    Direction.SOUTHWEST: (1, -1),
    Direction.WEST: (0, -1),
    Direction.NORTHWEST: (-1, -1)
}

DIRECTION_DELTAS = {      # X, Y
    Direction.NORTH: (0, -1),
    Direction.NORTHEAST: (1, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTHEAST: (1, 1),
    Direction.SOUTH: (0, 1),
    Direction.SOUTHWEST: (-1, 1),
    Direction.WEST: (-1, 0),
    Direction.NORTHWEST: (-1, 1)
}


class Point(NamedTuple):
    row: int
    col: int

def get_point_neighbors(point: Point) -> list[Point]:
    row, col = point.row, point.col

    output_list = []
    for dir in Direction:
        delta_row, delta_col = DIRECTION_DELTAS[dir]
        output_list.append((row + delta_row, col + delta_col))
    return output_list

def create_graph(node_list: list[Node]) -> dict[Node, list[Node]]:
    output_dict: dict[Node, list[Node]] = {}
    
    for node in node_list:
        neighbor_list = []
        for row, col in get_node_neighbor_coordinates(node):
            try:
                neighbor_list.append(
                    next(node for node in node_list 
                        if node.row == row and node.col == col))
            except StopIteration:
                continue
        output_dict[node] = neighbor_list
        
    return output_dict

def find_shortest_path(self, start_node: Node, end_node: Node) -> int:
    queue = deque([(start_node, [])])

    visited = set()
    visited.add(start_node)

    while queue:
        node, path = queue.popleft()
        if node == end_node:
            return len(path)
        neighbors = self.graph[node]
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
                visited.add(neighbor)
    return -1

def find_reachable_nodes(graph: dict[Point, list[Point]], 
                         parent: Point,
                         visited: Optional[set[Point]] = None) -> set[Point]:   
    if visited is None:
        visited = set()
        
    visited.add(parent)
    for child in graph[parent]:
        if child not in visited:
            find_reachable_nodes(graph, child, visited)
            
    return visited