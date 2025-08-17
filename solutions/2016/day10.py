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
from enum import Enum, IntEnum
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

class TooManyChips(Exception):
    pass

class TooManyInstructions(Exception):
    pass

class BotNotYetCreated(Exception):
    pass

class BotNotReady(Exception):
    pass

class Distribution(NamedTuple):
    bot_id: int
    value: int

class BotInstruction(NamedTuple):
    bot_id: int
    low_type: type
    low_id: int
    high_type: type
    high_id: int

@dataclass
class OutputBin:
    id: int
    chip: Optional[int] = None

@dataclass
class Bot:
    id: int
    chip_1: Optional[int] = None
    chip_2: Optional[int] = None
    low_bot: Optional[int] = None
    high_bot: Optional[int] = None

    @property
    def ready(self) -> bool:
        return all(x for x in [self.chip_1, self.chip_2, self.low_bot, self.high_bot])

@dataclass
class Factory:
    bots: list[Bot] = field(default_factory=list)
    output_bins: list[int] = field(default_factory=list)

    def make_distribution(self, dist: Distribution):
        try:
            bot = next(bot for bot in self.bots if bot.id == dist.bot_id)
            if bot.chip_1 and bot.chip_2:
                raise TooManyChips(f"Bot #{dist.bot_id} already has two chips.")

            if bot.chip_1:
                bot.chip_2 = dist.value
            else:
                bot.chip_1 = dist.value
                
        except StopIteration:
            bot = Bot(id=dist.bot_id, chip_1=dist.value)
            self.bots.append(bot)

    def add_instructions(self, inst: BotInstruction):
        try:
            bot = next(bot for bot in self.bots if bot.id == inst.bot_id)
            if bot.low_bot or bot.high_bot:
                raise TooManyInstructions(f"Bot #{inst.bot_id} already has instructions.")
            
            bot.low_bot = inst.low_bot
            bot.high_bot = inst.high_bot
            
        except StopIteration:
            bot = Bot(id=inst.bot_id, low_bot=inst.low_bot, high_bot=inst.high_bot)
            self.bots.append(bot)

        if bot.ready:
            self.execute_instructions
            

    def execute_instructions(self, bot: Bot):
        if not bot.ready:
            raise BotNotReady(f"Bot #{bot.id} is not ready to execute instructions.")

        
        try:
            bot = next(bot for bot in self.bots if bot.id == bot_id)
        except StopIteration:
            raise BotNotYetCreated(f"Bot #{bot_id} does not exist!")

        

            

            
        

def parse_data(data: str):
    line_list = data.splitlines()

    output_list = []
    for line in line_list:
        if line.startswith('value'):
            nums = [char for char in line if char.isdigit()]
            value = int(nums[0])
            bot_id= int(nums[1])
            ...
        else:
            _, bot_id, _, _, _, low_type_str, low_val, _, _, _, high_type_str, high_val = line.split(' ')
            low_type = Bot if low_type_str == 'bot' else OutputBin
            high_type = Bot if high_type_str == 'bot' else OutputBin
            inst = BotInstruction(int(bot_id), low_type, int(low_val), high_type, int(high_val))
            
    
def part_one(data: str):
    __ = parse_data(data)

def part_two(data: str):
    __ = parse_data(data)



def main():
    # print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()