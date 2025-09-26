from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

DIRECTION_DICT = {'left': -1, 'right': 1}

class State(NamedTuple):
    id: str
    value_0: int
    direction_0: str
    next_state_0: str
    value_1: int
    direction_1: str
    next_state_1: str

@dataclass
class TuringMachine:
    current_state_id: str
    checksum_steps: int
    state_list: list[State]
    state_dict: dict[str, State] = field(init=False)
    tape: defaultdict = field(init=False)
    cursor: int = 0
    steps_executed: int = 0

    def __post_init__(self):
        self.tape = defaultdict(int)
        self.state_dict = {state.id: state for state in self.state_list}

    def execute_next_step(self):
        state = self.state_dict[self.current_state_id]
        match self.tape[self.cursor]:
            case 0:
                self.tape[self.cursor] = state.value_0
                self.cursor += DIRECTION_DICT[state.direction_0]
                self.current_state_id = state.next_state_0
            case 1:
                self.tape[self.cursor] = state.value_1
                self.cursor += DIRECTION_DICT[state.direction_1]
                self.current_state_id = state.next_state_1
        self.steps_executed += 1

    def solve_part_one(self):
        while self.steps_executed < self.checksum_steps:
            self.execute_next_step()
        return sum(self.tape.values()) 

def parse_data(data: str) -> TuringMachine:
    line_list = [line for line in data.splitlines() if line]    
    initial_state = line_list.pop(0).removesuffix('.')[-1]
    checksum_steps = int(''.join(char for char in line_list.pop(0)
                                         if char.isdigit()))
    state_list = []

    assert len(line_list) % 9 == 0
    num_states = len(line_list) // 9
    for i in range(num_states):
        start = 0 + i * 9
        end = 9 + i * 9
        state_lines = line_list[start:end]
        id = state_lines[0].removesuffix(':')[-1]
        value_0 = int(''.join(char for char in state_lines[2]
                              if char.isdigit()))
        direction_0 = state_lines[3].removesuffix('.').split(' ')[-1]
        next_state_0 = state_lines[4].removesuffix('.')[-1]
        value_1 = int(''.join(char for char in state_lines[6]
                              if char.isdigit()))
        direction_1 = state_lines[7].removesuffix('.').split(' ')[-1]
        next_state_1 = state_lines[8].removesuffix('.')[-1]
        state_list.append(
            State(
                id=id,
                value_0=value_0,
                direction_0=direction_0,
                next_state_0=next_state_0,
                value_1=value_1,
                direction_1=direction_1,
                next_state_1=next_state_1))
    return TuringMachine(initial_state, checksum_steps, state_list)
        
def part_one(data: str):
    turing_machine = parse_data(data)
    return turing_machine.solve_part_one()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")

if __name__ == '__main__':
    main()