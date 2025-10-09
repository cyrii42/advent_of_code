from collections import deque
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from typing import NamedTuple

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)
TESTS_PART_ONE = [
    ("#######\n#.G...#\n#...EG#\n#.#.#G#\n#..G#E#\n#.....#\n#######", 47, 590, 27730),
    ("#######\n#G..#E#\n#E#E.E#\n#G.##.#\n#...#E#\n#...E.#\n#######", 37, 982, 36334),
    ("#######\n#E..EG#\n#.#G.E#\n#E.##E#\n#G..#.#\n#..E#.#\n#######\n", 46, 859, 39514),
    ("#######\n#E.G#.#\n#.#G..#\n#G.#.G#\n#G..#.#\n#...E.#\n#######\n", 35, 793, 27755), 
    ("#######\n#.E...#\n#.#..G#\n#.###.#\n#E#G#G#\n#...#G#\n#######\n", 54, 536, 28944),
    ("#########\n#G......#\n#.E.#...#\n#..##..G#\n#...##..#\n#...#...#\n#.G...G.#\n#.....G.#\n#########\n", 20, 937, 18740),   
]
TESTS_PART_TWO = [
    ("#######\n#.G...#\n#...EG#\n#.#.#G#\n#..G#E#\n#.....#\n#######", 15, 4988),
    ("#######\n#E..EG#\n#.#G.E#\n#E.##E#\n#G..#.#\n#..E#.#\n#######\n", 4, 31284),
    ("#######\n#E.G#.#\n#.#G..#\n#G.#.G#\n#G..#.#\n#...E.#\n#######\n", 15, 3478), 
    ("#######\n#.E...#\n#.#..G#\n#.###.#\n#E#G#G#\n#...#G#\n#######\n", 12, 6474),
    ("#########\n#G......#\n#.E.#...#\n#..##..G#\n#...##..#\n#...#...#\n#.G...G.#\n#.....G.#\n#########\n", 34, 1140),   
]

STARTING_HP = 200
ATTACK_POWER = 3

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

class Position(NamedTuple):
    x: int
    y: int

class NodeType(Enum):
    WALL = 0
    CAVERN = 1

@dataclass(frozen=True)
class Node:
    position: Position
    node_type: NodeType

    def __repr__(self):
        return (f"x={self.position.x}, y={self.position.y}")

class NoTargetsRemaining(Exception):
    pass

class NoPathsFound(Exception):
    pass

class UnitType(Enum):
    GOBLIN = 0
    ELF = 1

class NodePath(NamedTuple):
    nodes: list[Node]

@dataclass
class Unit:
    id: int
    node: Node
    hit_points: int = STARTING_HP
    attack_power: int = ATTACK_POWER

    @property
    def unit_type(self) -> UnitType:
        return UnitType.ELF if isinstance(self, Elf) else UnitType.GOBLIN  

    @property
    def enemy_type(self) -> UnitType:
        return UnitType.GOBLIN if isinstance(self, Elf) else UnitType.ELF   

    def execute_turn(self, unit_list: list["Unit"], 
                     graph: dict[Node, list[Node]], 
                     print_info: bool = False):
        other_units = [unit for unit in unit_list 
                       if unit.hit_points > 0 and unit.id != self.id]
        target_list = self.identify_targets(unit_list)
        if not target_list:
            raise NoTargetsRemaining
        
        adjacent_targets = [t for t in target_list if self.is_adjacent(t, graph)]
        if adjacent_targets:
            self.attack(adjacent_targets, print_info=print_info)
            
        else:
            try:
                self.move(target_list, other_units, graph, print_info=print_info)
            except NoPathsFound:
                return
            adjacent_targets = [t for t in target_list if self.is_adjacent(t, graph)]
            if adjacent_targets:
                self.attack(adjacent_targets, print_info=print_info)

    def identify_targets(self, unit_list: list["Unit"]) -> list["Unit"]:
        match self.enemy_type:
            case UnitType.GOBLIN:
                return [unit for unit in unit_list 
                        if isinstance(unit, Goblin) and unit.hit_points > 0]
            case UnitType.ELF:
                return [unit for unit in unit_list 
                        if isinstance(unit, Elf) and unit.hit_points > 0]

    def is_adjacent(self, target: "Unit", graph: dict[Node, list[Node]]) -> bool:
        return target.node in graph[self.node]

    def move(self, 
             target_list: list["Unit"], 
             other_units: list["Unit"], 
             graph: dict[Node, list[Node]],
             print_info: bool = False
             ) -> None:
        other_unit_nodes = [unit.node for unit in other_units]
        target_squares = self.identify_target_squares(target_list, other_unit_nodes, graph)
        prev_node = self.node
        next_node, target_node = self.find_next_node(target_squares, other_unit_nodes, graph)
        if print_info:
            print(f"Moving {self.unit_type.name} #{self.id} from {prev_node}",
                  f"to {next_node} (target: {target_node})")
        self.node = next_node      

    def identify_target_squares(self, target_list: list["Unit"], other_unit_nodes: list[Node],
                                graph: dict[Node, list[Node]]) -> list[Node]:
        return [node for target in target_list for node in graph[target.node]
                if node not in other_unit_nodes]

    def find_next_node(self, target_squares: list[Node], other_unit_nodes: list[Node],
                       graph: dict[Node, list[Node]]) -> tuple[Node, Node]:
        eligible_paths = [find_shortest_paths(self.node, target_square, 
                                              other_unit_nodes, graph)
                          for target_square in target_squares]
        if not eligible_paths:
            raise NoPathsFound(f"{self}")
        shortest_path_length = min(length for _, length in eligible_paths)
        shortest_path_lists = [path_list for path_list, length in eligible_paths 
                          if length == shortest_path_length]
        shortest_paths = [path for path_list in shortest_path_lists for path in path_list]

        if not shortest_paths:
            raise NoPathsFound(f"{self}")
        if len(shortest_paths) == 1:
            return (shortest_paths[0].nodes[0], shortest_paths[0].nodes[-1])
        else:          
            next_node, target_node = self.get_winning_start_and_target(shortest_paths)
            return (next_node, target_node)

    def get_winning_start_and_target(self, path_list: list[NodePath]) -> tuple[Node, Node]:
        target_to_first_dict = {}
        for path in path_list:
            first = path.nodes[0]
            target = path.nodes[-1]
            target_to_first_dict[target] = [path.nodes[0] for path in path_list
                                           if path.nodes[0] == first]
                    
        target_nodes = [path.nodes[-1] for path in path_list]
        target_nodes_sorted = sort_nodes(target_nodes)
        winning_target_node = target_nodes_sorted[0]

        first_nodes = target_to_first_dict[winning_target_node]
        first_nodes_sorted = sort_nodes(first_nodes)
        winning_first_node = first_nodes_sorted[0]
        
        return (winning_first_node, winning_target_node)

    def attack(self, adjacent_targets: list["Unit"], print_info: bool = False):
        if len(adjacent_targets) > 1:
            adjacent_targets = sort_units(adjacent_targets)
            adjacent_targets.sort(key=lambda unit: unit.hit_points)
            if print_info:
                if (len(adjacent_targets) > 2 
                    and adjacent_targets[0].hit_points == adjacent_targets[1].hit_points):
                    print(f"Adjacent Targets: {adjacent_targets}")
                    print(f"Target: {adjacent_targets[0]}")
                    print()
        target = adjacent_targets[0]
        target.hit_points = max(0, target.hit_points - self.attack_power)
        if print_info:
            print(f"{self.unit_type.name} #{self.id} ({self.node}) " + 
                  f"attacking {target.unit_type.name} #{target.id} ({target.node}) " +
                  f"(HP: {target.hit_points})")
        
class Elf(Unit):
    pass

class Goblin(Unit):
    pass

@dataclass
class Game:
    graph: dict[Node, list[Node]] = field(repr=False)
    units: list[Unit]
    rounds_completed: int = 0

    def sort_all_units(self) -> None:
        self.units = sort_units(self.units)

    def simulate_combat(self, 
                        elf_attack: int = 0,
                        print_info: bool = False):
        if elf_attack:
            for unit in self.units:
                if isinstance(unit, Elf):
                    unit.attack_power = elf_attack
        while True:
            self.sort_all_units()
            if print_info:
                print(f"Round #{self.rounds_completed+1} - BEGINNING")
                self.print_game_state()
                print()
            for unit in self.units:
                if unit.hit_points > 0:
                    try:
                        unit.execute_turn(self.units, self.graph, print_info=print_info)
                        if print_info:
                            print(f"Round #{self.rounds_completed+1} - Unit #{unit.id}")
                            self.print_game_state()
                            print()
                    except NoPathsFound as e:
                        raise NoPathsFound(e, self)
                    except NoTargetsRemaining:
                        if print_info:
                            print("GAME OVER")
                            self.print_game_state()
                            print()
                            self.sort_all_units()
                            print([unit for unit in self.units if unit.hit_points > 0])
                        raise
            self.rounds_completed += 1
            if print_info:
                print(f"Round #{self.rounds_completed} - COMPLETE")
                self.print_game_state()
                print()          
                print(self)

    def remove_dead_units(self):
        self.units = [unit for unit in self.units if unit.hit_points > 0]

    def solve_part_one(self, print_info: bool = False) -> tuple[int, int, int]: # type: ignore
        try:
            self.simulate_combat(print_info=print_info)
        except NoTargetsRemaining:
            return (self.rounds_completed,
                    sum(unit.hit_points for unit in self.units),
                    (self.rounds_completed * sum(unit.hit_points 
                                                for unit in self.units)))

    def solve_part_two(self, 
                       elf_attack: int = 0,
                       print_info: bool = False) -> tuple:   # type: ignore
        num_elves_at_start = len([unit for unit in self.units if isinstance(unit, Elf)])
        try:
            self.simulate_combat(elf_attack=elf_attack,
                                 print_info=print_info)
        except NoTargetsRemaining:
            remaining_elves = len([unit for unit in self.units 
                                   if isinstance(unit, Elf) and unit.hit_points > 0])
            no_elves_died = remaining_elves == num_elves_at_start
            return (no_elves_died,
                    elf_attack,
                    self.rounds_completed,
                    sum(unit.hit_points for unit in self.units),
                    (self.rounds_completed * sum(unit.hit_points 
                                                for unit in self.units)))

    @property
    def min_max(self) -> tuple[int, int, int, int]:
        ''' Returns: (min_x, min_y, max_x, max_y) '''
        node_list = [n for n in self.graph.keys()]
        min_x = min(node.position.x for node in node_list)
        min_y = min(node.position.y for node in node_list)
        max_x = max(node.position.x for node in node_list)
        max_y = max(node.position.y for node in node_list)

        return (min_x, min_y, max_x, max_y)

    def print_game_state(self) -> None:
        min_x, min_y, max_x, max_y = self.min_max
        unit_positions = [unit.node.position for unit in self.units
                          if unit.hit_points > 0]
        wall_positions = [n.position for n in self.graph.keys() 
                          if n.node_type == NodeType.WALL]

        for y in range(min_y, max_y+1):
            row = ''
            for x in range(min_x, max_x+1):
                pos = Position(x, y)
                if pos in unit_positions:
                    unit = next(unit for unit in self.units 
                                if unit.hit_points > 0 
                                and unit.node.position == pos)
                    match unit.unit_type:
                        case UnitType.GOBLIN:
                            row += 'G'
                        case UnitType.ELF:
                            row += 'E'
                        case _:
                            row += '?'
                elif pos in wall_positions:
                    row += '#'
                else:
                    row += '.'
            print(row)

def sort_units(unit_list: list[Unit]) -> list[Unit]:
    unit_list.sort(key=lambda unit: unit.node.position.x)
    unit_list.sort(key=lambda unit: unit.node.position.y)
    return unit_list

def sort_nodes(node_list: list[Node]) -> list[Node]:
    node_list.sort(key=lambda node: node.position.x)
    node_list.sort(key=lambda node: node.position.y)
    return node_list

def find_shortest_paths(start_node: Node, 
                        end_node: Node, 
                        other_unit_nodes: list[Node],
                        graph: dict[Node, list[Node]]
                        ) -> tuple[list[NodePath], int]:
    queue = deque([(start_node, [])])

    visited = set()
    visited.add(start_node)

    shortest_path_length = 999999999
    output_list = []
    while queue:
        node, path = queue.popleft()
        if node == end_node:
            shortest_path_length = min(len(path), shortest_path_length)
            output_list.append(path)
        else:
            neighbors = sort_nodes([node for node in graph[node] 
                                    if node.node_type != NodeType.WALL
                                    and node not in other_unit_nodes])
            for neighbor in neighbors:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
                    visited.add(neighbor)
                    
    assert len([path for path in output_list if len(path) < shortest_path_length]) == 0
    shortest_paths = [NodePath(path) for path in output_list 
                      if len(path) == shortest_path_length]
    return (shortest_paths, shortest_path_length)

def create_graph(node_list: list[Node]) -> dict[Node, list[Node]]:
    output_dict: dict[Node, list[Node]] = {}

    def get_node_neighbor_coordinates(node: Node) -> list[Position]:
        x, y = (node.position.x, node.position.y)

        output_list = []
        for dir in Direction:
            dx, dy = DIRECTION_DELTAS[dir]
            output_list.append(Position(x + dx, y + dy))
        return output_list
    
    for node in node_list:
        neighbor_list = []
        for x, y in get_node_neighbor_coordinates(node):
            try:
                neighbor_list.append(
                    next(node for node in node_list 
                        if node.position.x == x 
                        and node.position.y == y
                    ))
            except StopIteration:
                continue
        output_dict[node] = neighbor_list
        
    return output_dict

def parse_data(data: str) -> tuple[list[Node], list[Unit]]:
    line_list = data.splitlines()
    node_list, unit_list = ([], [])
    next_unit_id = 0
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            if char == ' ':
                continue
            elif char == '#':
                node_type = NodeType.WALL
            elif char == '.':
                node_type = NodeType.CAVERN
            elif char == 'G':
                node_type = NodeType.CAVERN
                unit_list.append(Goblin(next_unit_id,
                                        Node(Position(x, y), node_type)))
                next_unit_id += 1
            elif char == 'E':
                node_type = NodeType.CAVERN
                unit_list.append(Elf(next_unit_id,
                                     Node(Position(x, y), node_type)))
                next_unit_id += 1
            else:
                raise ValueError
            node_list.append(Node(Position(x, y), node_type))
    return (node_list, unit_list)

def part_one_tests(print_info: bool = False):
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        data, num_rounds, total_hp, outcome = example
        test_num_rounds, test_total_hp, test_outcome = part_one(data, print_info=print_info)
       
        print(f"Test #{i}: {test_outcome == outcome}",
              f"({test_num_rounds} rounds, {test_total_hp} total HP, {test_outcome} outcome)",
              f"(should be {num_rounds}, {total_hp}, {outcome})")

        if print_info:
            print()
            print("---------------------------------------")
            print()

def part_two_tests(print_info: bool = False):
    for i, example in enumerate(TESTS_PART_TWO, start=1):
        data, elf_attack, outcome = example
        no_elves_died, test_elf_attack, _, _, test_outcome = part_two(data, print_info=print_info)
        success = no_elves_died and test_elf_attack == elf_attack and test_outcome == outcome
        print(f"Test #{i}: {success} ({test_elf_attack}, {test_outcome}) (should be {elf_attack}, {outcome})")

        if print_info:
            print()
            print("---------------------------------------")
            print()

def part_one(data: str, print_info: bool = False):
    node_list, unit_list = parse_data(data)
    graph = create_graph(node_list)
    game = Game(graph, unit_list)
    
    return game.solve_part_one(print_info=print_info)

def part_two(data: str, print_info: bool = False, guess: int = 0):
    if guess:
        node_list, unit_list = parse_data(data)
        graph = create_graph(node_list)
        game = Game(graph, unit_list)
        return game.solve_part_two(elf_attack=guess, print_info=print_info)
    
    x = 0
    while True:
        node_list, unit_list = parse_data(data)
        graph = create_graph(node_list)
        game = Game(graph, unit_list)
        response = game.solve_part_two(elf_attack=x, print_info=print_info)
        if response[0]:
            return response
        x += 1

def main():
    part_one_tests(print_info=False)
    print(f"Part One (input):  {part_one(INPUT)}")
    part_two_tests(print_info=False)
    print(f"Part Two (input):  {part_two(INPUT, guess=19)}")

if __name__ == '__main__':
    main()