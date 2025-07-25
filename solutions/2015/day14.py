import functools
import itertools
import json
import math
import os
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from pprint import pprint
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = ('Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.\n'+
           'Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.')
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

@dataclass
class Reindeer:
    name: str
    speed: int
    duration: int
    rest: int
    position: int = 0
    position_list: list[int] = field(default_factory=list)
    points: int = 0

    def __post_init__(self):
        self.cycle_time = self.duration + self.rest

    def get_position_from_race_time(self, secs: int) -> int:
        full_cycles = secs // self.cycle_time
        remainder_secs = min(self.duration, (secs % self.cycle_time))
        return (full_cycles * (self.speed * self.duration)) + (remainder_secs * self.speed)

    def fly_part_one(self, secs: int) -> int:
        self.position = self.get_position_from_race_time(secs)
        return self.position

    def fly_part_two(self, secs: int) -> None:
        get_next_position = (self.get_position_from_race_time(time) for time in range(1, secs+1))
        self.position_list = [x for x in get_next_position]

    def add_point(self) -> None:
        self.points += 1
        

@dataclass
class ReindeerSet:
    members: list[Reindeer]

    def get_reindeer_by_position_at_time(self, position: int, time: int) -> list[Reindeer]:
        return [reindeer for reindeer in self.members if reindeer.position_list[time] == position]

    def run_race_part_one(self, secs: int) -> int:
        return max(reindeer.fly_part_one(secs) for reindeer in self.members)

    def run_race_part_two(self, secs: int) -> int:
        # Make every reindeer run the full race and create position lists
        for reindeer in self.members:
            reindeer.fly_part_two(secs)

        # Then go back through everyone's lists and see who was the leader at each second
        for x in range(secs):
            leader_position = max(reindeer.position_list[x] for reindeer in self.members)
            leader_or_co_leaders = self.get_reindeer_by_position_at_time(leader_position, x)
            for reindeer in leader_or_co_leaders:
                reindeer.add_point()
        return max(reindeer.points for reindeer in self.members)
            

def parse_data(data: str):
    line_list = data.splitlines()

    output_list = []
    for line in line_list:
        parts = line.split(' ')
        name = parts[0]
        speed = int(parts[3])
        duration = int(parts[6])
        rest = int(parts[-2])
            
        output_list.append(Reindeer(name, speed, duration, rest))
                
    return ReindeerSet(output_list)
    
def part_one(data: str, secs: int):
    reindeer_set = parse_data(data)
    return reindeer_set.run_race_part_one(secs)

def part_two(data: str, secs: int):
    reindeer_set = parse_data(data)
    return reindeer_set.run_race_part_two(secs)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE, 1000)}")
    print(f"Part One (input):  {part_one(INPUT, 2503)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE, 1000)}")
    print(f"Part Two (input):  {part_two(INPUT, 2503)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()