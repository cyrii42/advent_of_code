import pathlib
from dataclasses import dataclass
from typing import Self

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

@dataclass
class Disc:
    num_positions: int
    start: int

    def open_slot(self, time: int) -> bool:
        position = (self.start + time) % self.num_positions
        return position == 0

@dataclass
class Sculpture:
    discs: list[Disc]

    def add_disc(self, disc: Disc) -> None:
        self.discs.append(disc)

    def press_button(self, start_time: int) -> bool:
        t = start_time
        for disc in self.discs:
            t += 1
            if not disc.open_slot(t):
                return False
        return True

    def find_start_time(self) -> int:
        t = 0
        while True:
            if self.press_button(t):
                return t
            t += 1

    @classmethod
    def from_input(cls, data: str) -> Self:
        line_list = data.splitlines()
        discs = []
        for line in line_list:
            parts = line.split(' ')
            num_positions = int(parts[3])
            start = int(parts[-1].removesuffix('.'))
            discs.append(Disc(num_positions, start))
        return cls(discs)
    
def part_one(data: str):
    sculpture = Sculpture.from_input(data)
    return sculpture.find_start_time()

def part_two(data: str):
    sculpture = Sculpture.from_input(data)
    sculpture.add_disc(Disc(11, 0))
    return sculpture.find_start_time()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()