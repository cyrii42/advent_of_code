from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Self

from alive_progress import alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class NodeState(IntEnum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3

def clean_default():
    return NodeState.CLEAN

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

DIRECTION_DELTAS = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}

@dataclass
class Cluster:
    node_dict: defaultdict[tuple[int, int], NodeState] 
    part_two: bool = False
    carrier_pos: tuple[int, int] = (0, 0)
    carrier_dir: Direction = Direction.UP
    num_infection_bursts: int = 0

    def print_cluster(self):
        min_row = min(n[0] for n in self.node_dict.keys())
        max_row = max(n[0] for n in self.node_dict.keys())
        min_col = min(n[1] for n in self.node_dict.keys())
        max_col = max(n[1] for n in self.node_dict.keys())

        def get_rowcol_state(row, col):
            state = self.node_dict.get((row, col), NodeState.CLEAN)
            return '#' if state == NodeState.INFECTED else '.'

        for row in range(min_row, max_row+1):
            print(''.join(get_rowcol_state(row, col) 
                          for col in range(min_col, max_col+1)))

    def execute_burst(self) -> None:
        current_state = self.node_dict[self.carrier_pos]
        match current_state:
            case NodeState.INFECTED:
                self.carrier_dir = Direction((self.carrier_dir + 1) % 4)  # turn right
                if not self.part_two:
                    self.node_dict[self.carrier_pos] = NodeState.CLEAN
            case NodeState.CLEAN:
                self.carrier_dir = Direction((self.carrier_dir - 1) % 4)  # turn left
                if not self.part_two:
                    self.node_dict[self.carrier_pos] = NodeState.INFECTED
            case NodeState.WEAKENED:
                pass                                                      # do not turn
            case NodeState.FLAGGED:
                self.carrier_dir = Direction((self.carrier_dir + 2) % 4)  # turn around

        if self.part_two:
            self.node_dict[self.carrier_pos] = NodeState((current_state + 1) % 4)
            
        if self.node_dict[self.carrier_pos] == NodeState.INFECTED:
            self.num_infection_bursts += 1

        row, col = self.carrier_pos
        delta_row, delta_col = DIRECTION_DELTAS[self.carrier_dir]
        self.carrier_pos = (row+delta_row, col+delta_col)
    
    @classmethod
    def from_data(cls, data: str, part_two: bool = False) -> Self:
        line_list = data.splitlines()
        num_rows = len(line_list)
        num_cols = len(line_list[0])
        center_row, center_col = (num_rows//2, num_cols//2)

        node_dict = defaultdict(clean_default)
        for i, row in enumerate(line_list):
            row_num = i - center_row
            for j, node_char in enumerate(row):
                col_num = j - center_col
                state = NodeState.INFECTED if node_char == '#' else NodeState.CLEAN
                node_dict[(row_num, col_num)] = state
        return cls(node_dict, part_two)          

def part_one(data: str):
    cluster = Cluster.from_data(data)
    num_bursts = 70 if data == EXAMPLE else 10_000
    for _ in range(num_bursts):
        cluster.execute_burst()
    return cluster.num_infection_bursts

def part_two(data: str):
    cluster = Cluster.from_data(data, part_two=True)
    num_bursts = 100 if data == EXAMPLE else 10_000_000
    for _ in alive_it(range(num_bursts)):
        cluster.execute_burst()
    return cluster.num_infection_bursts

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()