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
    
# ROW, COL
DIRECTION_DELTAS = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}

# X, Y
DIRECTION_DELTAS = {      
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
}

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

# ROW, COL
DIRECTION_DELTAS = {
    Direction.NORTH: (-1, 0),
    Direction.NORTHEAST: (-1, 1),
    Direction.EAST: (0, 1),
    Direction.SOUTHEAST: (1, 1),
    Direction.SOUTH: (1, 0),
    Direction.SOUTHWEST: (1, -1),
    Direction.WEST: (0, -1),
    Direction.NORTHWEST: (-1, -1)
}

# X, Y
DIRECTION_DELTAS = {
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

class NodeType(Enum):
    EMPTY = 0
    FILLED = 1

class Node(NamedTuple):
    x: int
    y: int
    node_type: NodeType

type NodeDict = dict[tuple[int, int], Node]
def create_node_dict(data: str) -> NodeDict:
    line_list = data.splitlines()
    node_list: list[Node] = []
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            node_type = NodeType.FILLED if char == '#' else NodeType.EMPTY
            node_list.append(Node(x, y, node_type))
    node_dict = {(node.x, node.y): node for node in node_list}
    return node_dict

def get_point_neighbors(point: Point) -> list[Point]:
    row, col = point

    output_list = []
    for dir in Direction:
        delta_row, delta_col = DIRECTION_DELTAS[dir]
        output_list.append((row + delta_row, col + delta_col))
    return output_list


type NodeGraph = dict[Node, list[Node]]
def create_graph(node_dict: dict[tuple[int, int], Node]) -> NodeGraph:
    output_dict = {}
    
    for node in node_dict.values():
        neighbor_list = []
        for direction in Direction:
            dx, dy = DIRECTION_DELTAS[direction]
            try:
                neighbor = node_dict[(node.x + dx, node.y + dy)]
                neighbor_list.append(neighbor)
            except KeyError:
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