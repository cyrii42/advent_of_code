from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

@dataclass
class Program:
    name: str
    weight: int
    level: Optional[int] = field(default=None)
    parent_name: Optional[str] = field(default=None, repr=True)
    parent: "Program" = field(init=False, repr=False)
    children_names: list[str] = field(default_factory=list, repr=False)
    children: list["Program"] = field(default_factory=list, repr=False)

    @property
    def total_weight(self) -> int:       
        return self.weight + sum(c.weight for c in self.children)

@dataclass
class Tower:
    programs: list[Program]
    parent_to_children_dict: dict[str, list[str]] = field(init=False, repr=False)
    child_to_parent_dict: dict[str, str] = field(init=False, repr=False)

    def __post_init__(self):
        self.parent_to_children_dict = self.make_parent_to_children_dict()
        self.child_to_parent_dict = self.make_child_to_immediate_parent_dict()
        self.populate_parents()
        self.create_tree()

    @property
    def num_levels(self) -> int:
        return max(program.level for program in self.programs) # type: ignore

    def get_program_by_name(self, name: str) -> Program:
        try:
            return next(p for p in self.programs if p.name == name)
        except StopIteration:
            print(f"Can't find program w/ name {name} among {len(self.programs)} programs:",
                  f"{[program.name for program in self.programs]}")
            raise

    def get_program_weight_by_name(self, name: str) -> int:
        try:
            return self.get_program_by_name(name).weight
        except StopIteration:
            raise

    def get_all_children_names(self) -> set[str]:
        output_set = set()
        for program in self.programs:
            if not program.children_names:
                continue
            for child in program.children_names:
                output_set.add(child)
        return output_set

    def get_top_parent(self) -> Program:
        return next(p for p in self.programs 
                    if p.name not in self.get_all_children_names())

    def make_parent_to_children_dict(self) -> dict[str, list[str]]:
        return {p.name: p.children_names for p in self.programs}

    def populate_parents(self) -> None:
        for child_name, parent_name in self.child_to_parent_dict.items():
            child_program = self.get_program_by_name(child_name)
            if child_program:
                child_program.parent_name = parent_name
        
    def make_child_to_immediate_parent_dict(self) -> dict[str, str]:
        output_dict: dict[str, str] = {}

        parent_to_children_dict = self.make_parent_to_children_dict()
        all_children = set()
        for child_list in parent_to_children_dict.values():
            for child in child_list:
                all_children.add(child)
                
        for child in self.programs:
            parents = [parent for parent in parent_to_children_dict.keys()
                          if child.name in parent_to_children_dict[parent]]
            if len(parents) > 1:
                raise IndexError(f"Found {len(parents)} for program {child.name}")
            if len(parents) == 1:
                output_dict[child.name] = parents[0]
            elif len(parents) == 0:
                output_dict[child.name] = ''
        return output_dict

    def get_substack_weight(self, program_name: str) -> int:
        prog = self.get_program_by_name(program_name)
        if not prog.children_names:
            return prog.weight
        else:
            return prog.weight + sum(self.get_substack_weight(p) for p in prog.children_names)

    def create_tree(self, 
                    parent_name: Optional[str] = None, 
                    level: int = 1, 
                    print_info: bool = False):
        if not parent_name:
            top_parent = self.get_top_parent()
            top_parent.level = 0
            parent_name = top_parent.name
            
        children = self.parent_to_children_dict[parent_name]
        tabs = ''.join('\t' for _ in range(level))

        if children:
            if print_info:
             print(f"{tabs}Parent (level #{level}): {parent_name} | ",
                   f"Weight: {self.get_program_weight_by_name(parent_name)} | ",
                   f"Stack Weight: {self.get_substack_weight(parent_name)}")
            for child_name in children:
                child_prog = self.get_program_by_name(child_name)
                child_prog.level = level
                self.create_tree(child_name, level=level+1, print_info=print_info)
                
    def check_weights(self):
        for level in range(self.num_levels):
            for prog in [p for p in self.programs if p.level == level]:
                children = [self.get_program_by_name(child)
                            for child in prog.children_names]
                if not children:
                    continue
                
                if len(set([self.get_substack_weight(c.name) for c in children])) != 1:
                    print(f"{prog.name} (level #{level}) ({prog.weight}): ")
                    for c in children:
                        print(f"{c.name} ({c.weight}): {self.get_substack_weight(c.name)}")
                    print()

def parse_data(data: str) -> Tower:
    line_list = data.splitlines()
    
    program_list = []
    for line in line_list:
        match line.split(' '):
            case [name, weight, '->', *children_names]:
                children_names = [child.replace(',', '') 
                            for child in children_names]
                program = Program(name=name,
                                  weight=int(''.join(
                                      c for c in weight if c.isdigit())),
                                  children_names=children_names)
                program_list.append(program)
            case [name, weight]:
                program = Program(name=name,
                                  weight=int(''.join(
                                      c for c in weight if c.isdigit())))
                program_list.append(program)
    return Tower(program_list)
    
def part_one(data: str):
    tower = parse_data(data)
    return tower.get_top_parent().name

def part_two(data: str):
    tower = parse_data(data)
    tower.check_weights()




def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()