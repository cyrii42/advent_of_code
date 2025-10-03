from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

def create_order_graph(pair_list: list[tuple[str, str]]
                       ) -> dict[str, set[str]]:
    output_dict = defaultdict(set)
    for parent, child in pair_list:
        output_dict[parent].add(child)
    return output_dict

def create_prereq_graph(pair_list: list[tuple[str, str]]
                               ) -> dict[str, set[str]]:
    output_dict = defaultdict(set)
    for parent, child in pair_list:
        output_dict[child].add(parent)
    return output_dict

def find_correct_order(order_graph: dict[str, set[str]], 
                       prereq_graph: dict[str, set[str]]
                       ) -> str:
    start = sorted(p for p in order_graph.keys() 
                   if p not in prereq_graph.keys())[0]
    all_nodes = {n for n in order_graph.keys()} | {n for n in prereq_graph.keys()}
    visited = [start]

    while True:
        next_node_list = sorted([node for node in all_nodes 
                                 if node not in visited 
                                 and all(n in visited for n in prereq_graph[node])], 
                                reverse=True)
        next_node = next_node_list.pop()
        visited.append(next_node)
        if len(visited) == len(all_nodes):
            return ''.join(node for node in visited)

def parse_data(data: str) -> list[tuple[str, str]]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        _, step1, _, _, _, _, _, step2, _, _ = line.split()
        output_list.append((step1, step2))
    return output_list

def part_one(data: str):
    pair_list = parse_data(data)
    order_graph = create_order_graph(pair_list)
    prereq_graph = create_prereq_graph(pair_list)
    return find_correct_order(order_graph, prereq_graph)

@dataclass
class Elf:
    id: int
    step: str
    example: bool = field(default=False, repr=False) 
    t: int = field(init=False)

    def __post_init__(self):
        assert 1 <= self.id <= 5
        assert len(self.step) == 1 
        assert self.step.isupper()
        constant = 0 if self.example else 60
        self.t = constant + (ord(self.step) - 64)

    @property
    def finished(self) -> bool:
        return self.t <= 0

    def increment(self) -> None:
        self.t -= 1

class ElfSlotsFull(Exception):
    pass

@dataclass
class ElfGroup:
    elf_list: list[Elf] = field(default_factory=list)
    example: bool = field(default=False, repr=False) 
    time_elapsed: int = 0

    @property
    def full(self) -> bool:
        limit = 2 if self.example else 5
        return len(self.elf_list) >= limit

    @property
    def steps_processing(self) -> list[str]:
        return [elf.step for elf in self.elf_list]

    def add_elf(self, step: str) -> None:
        if self.full:
            raise ElfSlotsFull

        next_elf_id = len(self.elf_list) + 1
        self.elf_list.append(Elf(next_elf_id, step, self.example))

    def delete_elf(self, elf: Elf) -> None:
        self.elf_list.remove(elf)

    def list_elves(self) -> None:
        print(self.elf_list)

    def get_finished_steps(self) -> list[str]:
        output_list = []
        elves_to_delete = []
        
        for elf in self.elf_list:
            elf.increment()
            if elf.finished:
                output_list.append(elf.step)
                elves_to_delete.append(elf)

        for elf in elves_to_delete:
            self.delete_elf(elf)

        self.time_elapsed += 1
        return output_list
        
def count_required_steps(order_graph: dict[str, set[str]], 
                         prereq_graph: dict[str, set[str]],
                         example: bool = False
                         ) -> int:
    ''' If multiple steps are available, workers should still begin them in 
    alphabetical order. Each step takes 60 seconds plus an amount corresponding
    to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, 
    while step Z takes 60+26=86 seconds. No time is required between steps. '''

    all_nodes = {n for n in order_graph.keys()} | {n for n in prereq_graph.keys()}
    visited = []

    elf_group = ElfGroup(example=example)

    while True:
        next_node_list = sorted([node for node in all_nodes 
                                  if node not in visited 
                                  and all(n in visited for n in prereq_graph[node])
                                  and node not in elf_group.steps_processing], 
                                reverse=True)

        while next_node_list and not elf_group.full:
            next_node = next_node_list.pop()
            elf_group.add_elf(next_node)

        finished = elf_group.get_finished_steps()
        for node in sorted(finished):
            visited.append(node)

        if len(visited) == len(all_nodes):
            return elf_group.time_elapsed

def part_two(data: str):
    pair_list = parse_data(data)
    order_graph = create_order_graph(pair_list)
    prereq_graph = create_prereq_graph(pair_list)
    example = True if data == EXAMPLE else False
    return count_required_steps(order_graph, prereq_graph, example)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()