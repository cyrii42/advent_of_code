import functools
import hashlib
import itertools
import json
import math
import operator
import os
import pathlib
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Literal, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

'''
CHIPS:
    - if a microchip is ever left in the same area as another generator, and it's 
    not connected to its own generator, the microchip will be fried.

    - keep microchips connected to their corresponding generator when they're 
    in the same room, and away from other generators otherwise.

ELEVATOR:
    - can carry at most yourself and two generators or microchips in any combination

    - will only function if it contains at least one generator or microchip

    - always stops on each floor to recharge, and this takes long enough that 
    the items within it and the items on that floor can irradiate each other. 
    (You can prevent this if a microchip and its generator end up on the same 
    floor in this way, as they can be connected while the elevator is recharging.)
      
'''

BOTTOM_FLOOR = 1
TOP_FLOOR = 4

class GameException(Exception):
    pass

class RadiationWarning(GameException):
    pass

class ElevatorFull(GameException):
    pass

class ElevatorEmpty(GameException):
    pass

class FloorEmpty(GameException):
    pass

class ElevatorCannotMove(GameException):
    pass

class ItemNotFound(GameException):
    pass

class DuplicateObject(GameException):
    pass

class TooManyObjects(GameException):
    pass

class Direction(Enum):
    UP = 0
    DOWN = 1

class ObjectType(Enum):
    GENERATOR = 'generator'
    MICROCHIP = 'microchip'

class Object(NamedTuple):
    name: str
    type: ObjectType

    def __str__(self):
        return f"{self.name} {self.type.value}"

    def __repr__(self):
        return f"{self.name} {self.type.value}"

@dataclass
class Elevator:
    floor_num: Literal[1, 2, 3, 4]
    objects: list[Object] = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return not self.objects

    @property
    def full(self) -> bool:
        return len(self.objects) > 2

    def add_object(self, obj: Object) -> None:
        if self.full:
            raise ElevatorFull(f"Elevator is full! Cannot add {obj}")
        if obj in self.objects:
            raise DuplicateObject(f"{obj} already exists!")
        self.objects.append(obj)

    def remove_object(self, obj: Object) -> None:
        if self.empty:
            raise ElevatorEmpty(f"Elevator is empty!  Cannot remove {obj}")
        if obj not in self.objects:
            raise ItemNotFound(f"Elevator does not contain {obj}; cannot remove.")
        self.objects = [x for x in self.objects if x != obj]

@dataclass
class Floor:
    num: int
    objects: list[Object] = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return not self.objects

    def add_object(self, obj: Object) -> None:
        if obj in self.objects:
            raise DuplicateObject(f"{obj} already exists!")
        self.objects.append(obj)

    def remove_object(self, obj: Object) -> None:
        if self.empty:
            raise FloorEmpty(f"Floor is empty!  Cannot remove {obj}")
        if obj not in self.objects:
            raise ItemNotFound(f"Floor does not contain {obj}; cannot remove.")
        self.objects = [x for x in self.objects if x != obj]

@dataclass
class Building:
    floors: list[Floor]
    elevator: Elevator

    # def __repr__(self) -> str:
    #     return 'aposdhfasodpihf'

    @property
    def all_objects(self) -> list[Object]:
        ...

    @property
    def irradiated(self) -> bool:
        for floor in self.floors:
            if self.elevator.floor_num == floor.num:
                objects = floor.objects + self.elevator.objects
            else:
                objects = floor.objects
                
            microchips = [x for x in objects if x.type == ObjectType.MICROCHIP]
            generators = [x for x in objects if x.type == ObjectType.GENERATOR]
            for chip in microchips:
                if (any(x for x in generators if x.name != chip.name)
                    and not any(x for x in generators if x.name == chip.name)):
                    return True
                
        return False

    def add_object_to_elevator(self, obj: Object) -> None:
        try:
            self.elevator.add_object(obj)
        except GameException:
            raise

    def remove_object_from_elevator(self, obj: Object) -> None:
        try:
            self.elevator.remove_object(obj)
        except GameException:
            raise

    def add_object_to_floor(self, obj: Object, floor: Floor) -> None:
        floor.add_object(obj)

    def remove_object_from_floor(self, obj: Object, floor: Floor) -> None:
        try:
            floor.remove_object(obj)
        except GameException:
            raise

    def move_elevator(self, direction: Direction):
        match direction:
            case Direction.UP:
                if self.elevator.floor_num == TOP_FLOOR:
                    raise ElevatorCannotMove("Elevator is already at top floor!")
                self.elevator.floor_num = self.elevator.floor_num + 1
                
            case Direction.DOWN:
                if self.elevator.floor_num == BOTTOM_FLOOR:
                    raise ElevatorCannotMove("Elevator is already at bottom floor!")
                self.elevator.floor_num = self.elevator.floor_num - 1

    def move_objects(self, object_list: list[Object], direction: Direction):
        if len(object_list) > 2:
            raise TooManyObjects

        for obj in object_list:
            try:
                current_floor = next(f for f in self.floors if obj in f.objects)
                self.remove_object_from_floor(obj, current_floor)
                self.add_object_to_elevator(obj)
            except GameException:
                raise
            try:
                self.move_elevator(direction)
                new_floor = next(f for f in self.floors if f.num == self.elevator.floor_num)
                self.remove_object_from_elevator(obj)
                self.add_object_to_floor(obj, new_floor)
            except GameException:
                raise

        if self.irradiated:
            raise RadiationWarning



def parse_data(data: str) -> Building:
    IGNORED_WORDS = ['The', 'floor', 'contains', 'a', 'and',
                     'first', 'second', 'third', 'fourth',
                     'nothing', 'relevant']
    line_list = data.splitlines()

    floor_list = []
    for i, line in enumerate(line_list, start=1):
        line = line.removesuffix('.').replace(',', '').replace('-compatible', '')
        words = [word for word in line.split(' ') if word not in IGNORED_WORDS]

        j = 0
        object_list = []
        while j < len(words):
            object_list.append(Object(name=words[j], type=ObjectType(words[j+1])))
            j += 2
        floor_list.append(Floor(i, object_list))

    return Building(floor_list, Elevator(1))
            
        
    
def part_one(data: str):
    building = parse_data(data)
    print(building)
    print(building.all_objects)

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    asdf = [1]
    asdf = [x for x in asdf if x != 1]
    print(asdf)
       
if __name__ == '__main__':
    main()