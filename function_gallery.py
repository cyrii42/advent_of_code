from enum import Enum, IntEnum, StrEnum
from typing import NamedTuple
from dataclasses import dataclass, field
from collections import deque

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @property
    def left(self) -> "Direction":
        return Direction((self.value -1 ) % 4)

    @property
    def right(self) -> "Direction":
        return Direction((self.value + 1) % 4)

    @property
    def opposite(self) -> "Direction":
        return Direction((self.value + 2) % 4)

## for infinite positive grid beginning at upper left
DIRECTION_DELTAS = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
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