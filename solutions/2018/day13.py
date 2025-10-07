from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from typing import NamedTuple
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

with open(aoc.DATA_DIR / '2018.13_example.txt', 'r') as f:
    EXAMPLE = f.read()
with open(aoc.DATA_DIR / '2018.13_example_part_two.txt', 'r') as f:
    EXAMPLE_PART_TWO = f.read()
INPUT = aoc.get_input(YEAR, DAY)

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

DIRECTION_DELTAS = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
}

class NodeType(Enum):
    VERTICAL = 0        # |
    HORIZONTAL = 1      # -
    CURVE_BACKSLASH = 2 # \
    CURVE_SLASH = 3     # /
    INTERSECTION = 4    # +
    CART_UP = 5         # ^
    CART_DOWN = 6       # v
    CART_LEFT = 7       # <
    CART_RIGHT = 8      # >

class Position(NamedTuple):
    x: int
    y: int

@dataclass(frozen=True)
class Node:
    position: Position
    char: str = field(repr=False)
    node_type: NodeType = field(repr=False)

    def __repr__(self):
        return (f"({self.node_type.name}: " + 
                f"x={self.position.x}, y={self.position.y})")

class CartTurn(IntEnum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

@dataclass
class Cart:
    id: int
    node: Node
    direction: Direction 
    num_turns: int = 0

    def turn_left(self):
        self.direction = Direction((self.direction - 1) % len(Direction))

    def turn_right(self):
        self.direction = Direction((self.direction + 1) % len(Direction))

    def turn_at_curve(self):
        match [self.direction, self.node.node_type]:
            case ([Direction.RIGHT, NodeType.CURVE_BACKSLASH]   # > \
                  | [Direction.DOWN, NodeType.CURVE_SLASH]      # /
                  | [Direction.LEFT, NodeType.CURVE_BACKSLASH]  # \ <
                  | [Direction.UP, NodeType.CURVE_SLASH]):      # /
                self.turn_right()
            case ([Direction.RIGHT, NodeType.CURVE_SLASH]       # > /
                  | [Direction.DOWN, NodeType.CURVE_BACKSLASH]  # \
                  | [Direction.LEFT, NodeType.CURVE_SLASH]      # / <
                  | [Direction.UP, NodeType.CURVE_BACKSLASH]):  # \
                self.turn_left()

    def turn_at_intersection(self) -> None:
        self.turn_type = self.num_turns % len(CartTurn)
        
        match self.turn_type:
            case CartTurn.LEFT:
                self.turn_left()
            case CartTurn.RIGHT:
                self.turn_right()
            case _:
                pass
            
        self.num_turns += 1

    def tick(self, graph: dict[Node, list[Node]]) -> None:
        x, y = (self.node.position.x, self.node.position.y)
        delta_x, delta_y = DIRECTION_DELTAS[self.direction]
        next_position = Position(x + delta_x, y + delta_y)
        try:
            next_node = next(n for n in graph[self.node] 
                             if n.position == next_position)  
        except StopIteration:
            print(f"Failed to find node at position {next_position}")
            print(graph[self.node])
            raise
        else:
            self.node = next_node
            match self.node.node_type:
                case NodeType.INTERSECTION:
                    self.turn_at_intersection()
                case NodeType.CURVE_SLASH | NodeType.CURVE_BACKSLASH:
                    self.turn_at_curve()
                case _:
                    pass

@dataclass
class CartGroup:
    carts: list[Cart]
    graph: dict[Node, list[Node]]

    def tick(self, part_two: bool = False):       
        for cart in self.carts:
            cart.tick(graph=self.graph)

            num_positions = len(set([cart.node.position for cart in self.carts]))
            if num_positions < len(self.carts):
                position_list = [cart.node.position for cart in self.carts]
                collision_points = {p for p in position_list 
                                    if position_list.count(p) > 1}

                if part_two:
                    self.carts = [c for c in self.carts 
                                  if c.node.position not in collision_points]
                else:
                    collision_point = collision_points.pop()
                    return collision_point

        if len(self.carts) == 1:
            last_cart = self.carts[0]
            return last_cart.node.position

def get_node_neighbor_coordinates(node: Node) -> list[Position]:
    x, y = (node.position.x, node.position.y)

    output_list = []
    for dir in Direction:
        delta_x, delta_y = DIRECTION_DELTAS[dir]
        output_list.append(Position(x + delta_x, y + delta_y))
    return output_list

def create_graph(node_list: list[Node]) -> dict[Node, list[Node]]:
    output_dict: dict[Node, list[Node]] = {}
    
    for node in node_list:
        neighbor_list = []
        for x, y in get_node_neighbor_coordinates(node):
            try:
                neighbor_list.append(
                    next(node for node in node_list 
                        if node.position.x == x 
                        and node.position.y == y))
            except StopIteration:
                continue
        output_dict[node] = neighbor_list
        
    return output_dict

def parse_data(data: str) -> tuple[list[Node], list[Cart]]:
    line_list = data.splitlines()
    node_list, cart_list = ([], [])
    next_cart_id = 0
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            if char == ' ':
                continue
            elif char == '|':
                node_type = NodeType.VERTICAL
            elif char == '-':
                node_type = NodeType.HORIZONTAL
            elif char == '\\':
                node_type = NodeType.CURVE_BACKSLASH
            elif char == '/':
                node_type = NodeType.CURVE_SLASH
            elif char == '+':
                node_type = NodeType.INTERSECTION
            elif char == '^':
                node_type = NodeType.VERTICAL
                cart_list.append(Cart(id=next_cart_id,
                                      node=Node(Position(x, y), char, node_type),
                                      direction=Direction.UP))
                next_cart_id += 1
            elif char == 'v':
                node_type = NodeType.VERTICAL
                cart_list.append(Cart(id=next_cart_id,
                                      node=Node(Position(x, y), char, node_type),
                                      direction=Direction.DOWN))
                next_cart_id += 1
            elif char == '<':
                node_type = NodeType.HORIZONTAL
                cart_list.append(Cart(id=next_cart_id,
                                      node=Node(Position(x, y), char, node_type),
                                      direction=Direction.LEFT))
                next_cart_id += 1
            elif char == '>':
                node_type = NodeType.HORIZONTAL
                cart_list.append(Cart(id=next_cart_id,
                                      node=Node(Position(x, y), char, node_type),
                                      direction=Direction.RIGHT))
                next_cart_id += 1
            else:
                raise ValueError
            node_list.append(Node(Position(x, y), char, node_type))
    return (node_list, cart_list)

def part_one(data: str):
    node_list, cart_list = parse_data(data)
    graph = create_graph(node_list)
    cart_group = CartGroup(cart_list, graph)

    answer = None
    while True:
        answer = cart_group.tick()
        if answer:
            return answer

def part_two(data: str):
    node_list, cart_list = parse_data(data)
    graph = create_graph(node_list)
    cart_group = CartGroup(cart_list, graph)

    answer = None
    while True:
        answer = cart_group.tick(part_two=True)
        if answer:
            return answer
        
def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()