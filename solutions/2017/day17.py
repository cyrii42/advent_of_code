import itertools
from dataclasses import dataclass, field
from pathlib import Path

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '3'
INPUT = aoc.get_input(YEAR, DAY)

NUM_REPEATS = 2017

@dataclass
class Spinlock:
    num_steps: int
    ptr: int = 0
    buffer: list[int] = field(init=False)
    counter: itertools.count = field(init=False)

    def __post_init__(self):
        self.buffer = [0]
        self.counter = itertools.count(start=1)

    @property
    def buffer_size(self) -> int:
        return len(self.buffer)

    def run_simulation(self, num_insertions: int = 2017) -> None:
        for _ in range(num_insertions):
            self.ptr = (self.ptr + self.num_steps) % self.buffer_size
            self.insert_new_number(next(self.counter))
            self.ptr = self.ptr + 1

    def insert_new_number(self, num: int) -> None:
        idx = self.ptr
        if idx >= self.buffer_size - 1:
            self.buffer.append(num)
        else:
            self.buffer.insert(idx+1, num)

    def solve_part_one(self) -> int:
        self.run_simulation()
        idx_2017 = self.buffer.index(2017)
        return self.buffer[idx_2017+1]

    def solve_part_two(self) -> int:
        pretend_buffer_size = 1
        ans = 0
        for _ in range(50_000_000):
            self.ptr = (self.ptr + self.num_steps) % pretend_buffer_size
            c = next(self.counter)
            if self.ptr == 0:
                ans = c
            pretend_buffer_size += 1
            self.ptr = self.ptr + 1
        return ans
    
def part_one(data: str):
    num_steps = int(data)
    spinlock = Spinlock(num_steps=num_steps)
    return spinlock.solve_part_one()

def part_two(data: str):
    num_steps = int(data)
    spinlock = Spinlock(num_steps=num_steps)
    return spinlock.solve_part_two()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()