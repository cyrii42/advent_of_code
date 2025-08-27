import itertools
import math
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

with open(aoc.DATA_DIR / '2016.22_example.txt') as f:
    EXAMPLE = f.read()
INPUT = aoc.get_input(YEAR, DAY)

class InsufficientDiskSpace(Exception):
    pass

class NodesNotAdjcacent(Exception):
    pass

class NoEmptyNodes(Exception):
    pass

class NodeNotEmpty(Exception):
    pass

DIRECTIONS = {
    'UP':    (1, 0),
    'RIGHT': (0, 1),
    'DOWN':  (-1, 0),
    'LEFT':  (0, -1),
}

@dataclass
class Node:
    x: int
    y: int
    size: int = field(repr=True)
    used: int = field(repr=True)
    avail: int = field(repr=True)
    used_pct: int = field(repr=True)
    has_goal_data: bool = False

    @property
    def coord(self) -> tuple[int, int]:
        return (self.x, self.y)

    def add_data(self, data: int) -> None:
        if self.used + data > self.size:
            raise InsufficientDiskSpace
        self.used += data
        self.avail -= data
        self.used_pct = math.ceil(self.used / self.size * 100)

    def extract_data(self) -> int:
        output = deepcopy(self.used)
        self.used = 0
        self.avail = self.size
        self.used_pct = 0
        return output
        
@dataclass
class Grid:
    nodes: list[Node]
    graph: dict[tuple[int, int], list[tuple[int, int]]] = field(init=False, repr=False)

    def __post_init__(self):
        self.graph = self.create_graph()
        self.get_node_by_location((self.max_x, 0)).has_goal_data = True

    @property
    def max_x(self) -> int:
        return max(node.x for node in self.nodes)

    @property
    def max_y(self) -> int:
        return max(node.y for node in self.nodes)

    @property
    def goal_node(self) -> Node:
        return next(node for node in self.nodes if node.has_goal_data)

    @property
    def left_of_goal_node(self) -> Node:
        return next(node for node in self.nodes 
                    if node.x == self.goal_node.x - 1
                    and node.y == self.goal_node.y)

    @property
    def empty_node(self) -> Node:
        return [node for node in self.nodes if node.used == 0][0]

    @property
    def size_of_empty_node(self) -> int:
        return self.empty_node.size

    def create_graph(self) -> dict[tuple[int, int], list[tuple[int, int]]]:
        output = {}
        for x in range(self.max_x+1):
            for y in range(self.max_y+1):
                node = (x, y)
                neighbors = [(x+i, y+j) for i, j in DIRECTIONS.values() 
                              if x+i >= 0 and x+i <= self.max_x
                              and y+j >= 0 and y+j <= self.max_y]
                output[node] = neighbors
        return output

    def get_node_by_location(self, loc: tuple[int, int]) -> Node:
        x, y = loc
        return next(n for n in self.nodes if n.x == x and n.y == y)

    def check_adjacency(self, node1: Node, node2: Node) -> bool:
        return (node2.x, node2.y) in self.graph[(node1.x, node1.y)]

    def get_adjacent_nodes(self, node: Node) -> list[Node]:
        return [self.get_node_by_location(loc)
                for loc in self.graph[node.coord]]

    def move_data(self, node1: Node, node2: Node) -> None:
        if not self.check_adjacency(node1, node2):
            raise NodesNotAdjcacent
        if node1.used > node2.avail:
            raise InsufficientDiskSpace
        data = node1.extract_data()
        node2.add_data(data)
        if node1.has_goal_data:
            node1.has_goal_data = False
            node2.has_goal_data = True

    def move_free_space_along_path(self, path: list[Node]) -> int:
        ''' Returns the number of moves '''
        if path[0].used != 0:
            raise NodeNotEmpty

        moves = 0
        for i in range(len(path)):
            if i == len(path) - 1:
                break
            self.move_data(path[i+1], path[i])
            moves += 1
        assert path[-1].used == 0
        return moves
        
    def find_shortest_path_between_nodes(self, 
                                         start: Node, 
                                         end: Node) -> list[Node]:
        queue = deque([(start, [start])])

        visited = set()
        visited.add(start.coord)

        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            potential_neighbors = self.get_adjacent_nodes(node)
            neighbors = [n for n in potential_neighbors 
                         if n.used < self.size_of_empty_node
                         and not n.has_goal_data]
            for neighbor in neighbors:
                if neighbor.coord not in visited:
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
                    visited.add(neighbor.coord)
        return []

    def solve_part_one(self) -> int:
        total = 0
        for a, b in itertools.permutations(self.nodes, 2):
            if a.used > 0 and a.used <= b.avail:
                total += 1
        return total

    def solve_part_two(self, print_info: bool = False) -> int:
        ''' Your goal is to gain access to the data that begins in 
        the node with y=0 and the highest x (that is, the node in 
        the top-right corner).'''

        total_moves = 0
        
        # repeat until goal data is in (1, 0)
        while self.goal_node.coord != (1, 0):
            # move the empty node to the left of the goal data
            if print_info:
                print("Before moving empty node:")
                print(f"Empty node: {self.empty_node}")
                print(f"Goal node: {self.goal_node}")
                print(f"Left of goal node: {self.left_of_goal_node}")
                print()
            
            path = self.find_shortest_path_between_nodes(self.empty_node, 
                                                         self.left_of_goal_node)
            total_moves += self.move_free_space_along_path(path)

            if print_info:
                print("After moving empty node:")
                print(f"Empty node: {self.empty_node}")
                print(f"Goal node: {self.goal_node}")
                print(f"Left of goal node: {self.left_of_goal_node}")
                print()
            
            # move the goal data to the empty node
            self.move_data(self.goal_node, self.empty_node)
            total_moves += 1
            if print_info:
                print("After moving data:")
                print(f"Empty node: {self.empty_node}")
                print(f"Goal node: {self.goal_node}")
                print(f"Left of goal node: {self.left_of_goal_node}")
                print()
            
        # move the empty node to (0, 0) and move the goal data there
        zero_one = self.get_node_by_location((0, 0))
        path = self.find_shortest_path_between_nodes(self.empty_node, 
                                                     zero_one)
        total_moves += self.move_free_space_along_path(path)
        
        # move the goal data to the empty node
        self.move_data(self.goal_node, self.empty_node)
        total_moves += 1

        return total_moves

def parse_data(data: str) -> Grid:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        if not line.startswith('/dev/grid/node-'):
            continue
        name, size, used, avail, used_pct = [x for x in line.split(' ') if x]
        x, y = name.removeprefix('/dev/grid/node-').split('-')
        output_list.append(Node(x=int(x.removeprefix('x')), 
                                y=int(y.removeprefix('y')), 
                                size=int(size.removesuffix('T')), 
                                used=int(used.removesuffix('T')), 
                                avail=int(avail.removesuffix('T')), 
                                used_pct=int(used_pct.removesuffix('%'))))
    return Grid(output_list)
    
def part_one(data: str):
    grid = parse_data(data)
    return grid.solve_part_one()

def part_two(data: str):
    grid = parse_data(data)
    return grid.solve_part_two()

def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()