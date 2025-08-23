'''--- Day 7: No Space Left On Device ---'''

from pathlib import Path
from rich import print
from copy import deepcopy
from dataclasses import dataclass, field
from typing import NamedTuple, Optional
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day7_example.txt'
INPUT = DATA_DIR / '2022_day7_input.txt'

@dataclass
class File():
    name: str
    size: int

@dataclass
class Directory():
    name: str
    level: int
    parent: Optional['Directory'] = field(default=None, repr=False)
    files: list[File] = field(default_factory=list)
    children: list['Directory'] = field(default_factory=list)

    def __eq__(self, other):
        return self.name == other.name

    @property
    def children_names(self) -> list[str]:
        return [dir.name for dir in self.children if dir.name != self.name]

    @property
    def total_size(self) -> int:
        if len(self.children) == 0:
            return sum(file.size for file in self.files)
        else:
            return sum(file.size for file in self.files) + sum(dir.total_size for dir in self.children)

@dataclass
class Filesystem():
    terminal_output: list[str]
    dir_list: list[Directory]

    def find_dir(self, dir: Directory) -> Directory:
        try:
            return next(dir for dir in self.dir_list if dir == dir)
        except StopIteration:
            raise FileNotFoundError(f"Directory \"{dir.name}\" not found in filesystem.")

    def find_dir_by_name(self, name: str) -> Directory:
        try:
            return next(dir for dir in self.dir_list if dir.name == name)
        except StopIteration:
            raise FileNotFoundError(f"Directory \"{name}\" not found in filesystem.")

    @property
    def dir_names(self) -> list[str]:
        return [dir.name for dir in self.dir_list]

    def populate_children(self):
        for dir in self.dir_list:
            if dir.parent is not None:
                dir.parent.children.append(dir)

    def populate_files(self):
        current_dir = self.dir_list[0]
        dir_level = 0
        for line in self.terminal_output:
            if line == '$ cd /':
                current_dir = self.dir_list[0]
                dir_level = 0
                continue
            if line == '$ cd ..':
                dir_level =- 1 if dir_level > 0 else 0
                if current_dir.parent is None:
                    current_dir = self.dir_list[0]
                else:
                    current_dir = current_dir.parent
                continue
            elif line.startswith('$ cd'):
                dir_level += 1
                dir_name = line.removeprefix('$ cd ')
                current_dir = self.find_dir_by_name(dir_name)
            elif line[0].isdigit():
                file_size, file_name = line.split(' ')
                file = File(file_name, int(file_size))
                current_dir.files.append(file)
            elif line.startswith('dir'):
                child_dir_name = line.removeprefix('dir ')
                child_dir = Directory(name=child_dir_name, level=dir_level+1)
                if child_dir in current_dir.children:
                    continue
                else:
                    print(f"Couldn't find child directory {child_dir.name} in directory {current_dir.name}'s list of children ({current_dir.children_names})!!")
                    # print(f"But it does exist:  {self.find_dir_by_name(child_dir_name)}")
                    current_dir.children.append(child_dir)
            else:
                continue

    def get_part_one_answer(self) -> int:
        # for dir in self.dir_list:
        #     print(f"Directory {dir.name} has total size:  {dir.total_size}")
        return sum(dir.total_size for dir in self.dir_list if dir.total_size <= 100_000)
                

def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        
    return line_list

def create_filesystem(terminal_output: list[str]) -> Filesystem:  
    dir_list = [Directory(name='/', level=0)]
    current_dir = dir_list[0]
    dir_level = 0
    for line in terminal_output:
        if line == '$ cd /':
            dir_level = 0
            current_dir = dir_list[0]
            continue
        if line == '$ cd ..':
            dir_level =- 1 if dir_level > 0 else 0
            if current_dir.parent is None:
                current_dir = dir_list[0]
            else:
                current_dir = current_dir.parent
            continue
        if line == '$ ls':
            continue
        if line.startswith('$ cd'):
            dir_name = line.removeprefix('$ cd ')
            parent = dir_list[-1] if dir_level > 0 else dir_list[0]
            dir_level += 1   
            dir_list.append(Directory(name=dir_name,
                                      level=dir_level,
                                      parent=parent))
            continue
    for line in terminal_output:
        if line.startswith('dir'):
            child_dir_name = line.removeprefix('dir ')
            child_dir = Directory(name=child_dir_name, level=dir_level+1, parent=current_dir)
            if Directory(child_dir.name, dir_level+1) not in dir_list:
                dir_list.append(child_dir)
            
    return Filesystem(terminal_output, dir_list)


        
# def find_directory_sizes(terminal_output: list[str]) -> list[File]:
#     output_list = []
#     current_dir_name = '/'
#     for line in terminal_output:
#         if 

def part_one(filename: Path):
    terminal_output = ingest_data(filename)
    filesystem = create_filesystem(terminal_output)
    filesystem.populate_children()
    filesystem.populate_files()
    # print(filesystem)
    return filesystem.get_part_one_answer()

def part_two(filename: Path):
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 95437
    print(f"Part One (input):  {part_one(INPUT)}") # 
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}") #
    # print(f"Part Two (input):  {part_two(INPUT)}") # 

    # random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()