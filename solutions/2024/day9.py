'''--- Day 9: Disk Fragmenter ---'''

from pathlib import Path
from rich import print
from pprint import pprint
from copy import deepcopy
from typing import NamedTuple, Protocol, Optional
from enum import Enum
from dataclasses import dataclass, field
from string import ascii_letters
import itertools
import pandas as pd
import numpy as np
from alive_progress import alive_it
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day9_example.txt'
INPUT = DATA_DIR / 'day9_input.txt'


def ingest_data(filename: Path) -> str:
    with open(filename, 'r') as f:
        return f.read()


@dataclass
class File():
    length: int
    id: Optional[int] = None

@dataclass
class Block():
    index: int
    id: Optional[int] = None

@dataclass
class Filesystem():
    files: list[File]
    blocks: list[Block] = field(default_factory=list)

    def populate_block_list(self):
        id_list = [file.id for file in self.files for _ in range(file.length)]
        self.blocks += [Block(i, file_id) for i, file_id in enumerate(id_list)]
            
    def compress_part_one(self):
        self.populate_block_list()
        free_blocks = [block for block in self.blocks if block.id is None]       
        for free_block in alive_it(free_blocks):
            non_free_blocks = [block for block in self.blocks if block.id is not None]
            if non_free_blocks[-1].index > free_block.index:
                self.blocks[free_block.index] = Block(free_block.index, non_free_blocks[-1].id)
                self.blocks[non_free_blocks[-1].index] = Block(non_free_blocks[-1].index, None)

    def compress_part_two(self):
        non_empty_files = [file for file in self.files if file.id is not None]
        for file in reversed(non_empty_files):
            for i, test_file in enumerate(self.files):
                if test_file.id is None and test_file.length >= file.length:
                    self.files[i] = File(length=file.length,
                                         id=file.id)
                    if test_file.length > file.length:
                        self.files.insert(i+1, File(length=test_file.length - file.length,
                                                    id=None))
                    break
        self.clean_up()
        self.populate_block_list()
            
    def clean_up(self):
        running_set: set[int] = set()
        for i, file in enumerate(self.files):
            if file.id is None:
                continue
            elif file.id in running_set:
                self.files[i] = File(length=file.length, id=None)
            else:
                running_set.add(file.id)
            
    def calculate_checksum(self) -> int:
        total = 0
        for i, block in enumerate(self.blocks):
            total += 0 if block.id is None else i * block.id
        return total

def create_filesystem(input: str) -> Filesystem:
    file_list = []
    next_id = 0
    for i, char in enumerate(input):
        if i % 2 == 0:
            file_list.append(File(length=int(char), 
                                  id=next_id))
            next_id += 1
        else:
            file_list.append(File(length=int(char), 
                                  id=None))
        
    return Filesystem(file_list)
        
        

def part_one(filename: Path):
    input = ingest_data(filename)
    filesystem = create_filesystem(input)
    filesystem.compress_part_one()

    return filesystem.calculate_checksum()


def part_two(filename: Path):
    input = ingest_data(filename)
    filesystem = create_filesystem(input)
    filesystem.compress_part_two()

    return filesystem.calculate_checksum()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")



    


if __name__ == '__main__':
    main()