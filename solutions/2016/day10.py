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

class BotRecipientType(Enum):
    BOT = 'bot'
    BIN = 'output'

class TooManyChips(Exception):
    pass

class BinAlreadyExists(Exception):
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
    low_recipient_type: BotRecipientType
    low_recipient_id: int
    high_recipient_type: BotRecipientType
    high_receipient_id: int

@dataclass
class OutputBin:
    id: int
    chip: Optional[int] = None

@dataclass
class Bot:
    id: int
    chip_1: Optional[int] = None
    chip_2: Optional[int] = None
    inst: Optional[BotInstruction] = None

    @property
    def ready(self) -> bool:
        return all(x for x in [self.chip_1, self.chip_2, self.inst])

@dataclass
class Factory:
    bots: list[Bot] = field(default_factory=list)
    output_bins: list[OutputBin] = field(default_factory=list)

    def make_distribution(self, dist: Distribution):
        try:
            bot = self.get_bot_by_id(dist.bot_id)
            if bot.chip_1 and bot.chip_2:
                raise TooManyChips(f"Bot #{dist.bot_id} already has two chips.")
            if bot.chip_1:
                bot.chip_2 = dist.value
            else:
                bot.chip_1 = dist.value
                
        except StopIteration:
            bot = Bot(id=dist.bot_id, chip_1=dist.value)
            self.bots.append(bot)

    def get_bot_by_id(self, bot_id: int) -> Bot:
        return next(bot for bot in self.bots if bot.id == bot_id)

    def add_instruction(self, inst: BotInstruction):
        try:
            bot = self.get_bot_by_id(inst.bot_id)
            if bot.inst:
                raise TooManyInstructions(f"Bot #{inst.bot_id} already has instructions.")
            bot.inst = inst
            
        except StopIteration:
            bot = Bot(id=inst.bot_id, inst=inst)
            self.bots.append(bot)
            
    def execute_all_instruction(self):
        for bot in self.bots:
            if not bot.inst or not bot.chip_1 or not bot.chip_2:
                raise BotNotReady(f"Bot #{bot.id} is not ready to execute instructions.")

            low_chip = bot.chip_1 if not bot.chip_2 else min(bot.chip_1, bot.chip_2)
            match bot.inst.low_recipient_type:
                case BotRecipientType.BOT:
                    output_bot = self.get_bot_by_id(bot.inst.low_recipient_id)
                    # if output_bot.chip_1 and output_bot.chip_2:
                    #     raise TooManyChips(f"Bot #{output_bot.id} already has two chips.")
                    if output_bot.chip_1:
                        output_bot.chip_2 = low_chip
                    else:
                        output_bot.chip_1 = low_chip

                    if bot.chip_1 == low_chip:
                        bot.chip_1 = None
                    else:
                        bot.chip_2 = None
                        
                case BotRecipientType.BIN:
                    if len([bin for bin in self.output_bins if bin.id == bot.inst.low_recipient_id]) > 0:
                        raise BinAlreadyExists(f"Bin #{bot.inst.low_recipient_id} already exists.")
                    output_bin = OutputBin(id=bot.inst.low_recipient_id, chip=low_chip)
                    self.output_bins.append(output_bin)

            high_chip = bot.chip_1 if not bot.chip_2 else max(bot.chip_1, bot.chip_2)
            match bot.inst.high_recipient_type:
                case BotRecipientType.BOT:
                    output_bot = self.get_bot_by_id(bot.inst.low_recipient_id)
                    # if output_bot.chip_1 and output_bot.chip_2:
                    #     raise TooManyChips(f"Bot #{output_bot.id} already has two chips.")
                    if output_bot.chip_1:
                        output_bot.chip_2 = high_chip
                    else:
                        output_bot.chip_1 = high_chip
                        
                    if bot.chip_1 == high_chip:
                        bot.chip_1 = None
                    else:
                        bot.chip_2 = None
                        
                case BotRecipientType.BIN:
                    if len([bin for bin in self.output_bins if bin.id == bot.inst.low_recipient_id]) > 0:
                        raise BinAlreadyExists(f"Bin #{bot.inst.low_recipient_id} already exists.")
                    output_bin = OutputBin(id=bot.inst.low_recipient_id, chip=high_chip)
                    self.output_bins.append(output_bin)

            print(self)
                    


    def create_bot_or_add_chip(self, bot_id: int, value: int) -> None:
        try:
            bot = self.get_bot_by_id(bot_id)
            if bot.chip_1 and bot.chip_2:
                raise TooManyChips(f"Bot #{bot_id} already has two chips.")
            if bot.chip_1:
                bot.chip_2 = value
            else:
                bot.chip_1 = value
        except StopIteration:
            bot = Bot(id=bot_id, chip_1=value)
            self.bots.append(bot)
            
    def parse_data(self, data: str) -> None:
        line_list = data.splitlines()

        for line in line_list:
            if line.startswith('value'):
                nums = [char for char in line if char.isdigit()]
                value = int(nums[0])
                bot_id= int(nums[1])
                self.create_bot_or_add_chip(bot_id, value)
            else:
                _, bot_id, _, _, _, low_type_str, low_val, _, _, _, high_type_str, high_val = line.split(' ')
                low_type = BotRecipientType(low_type_str)
                high_type = BotRecipientType(high_type_str)
                inst = BotInstruction(int(bot_id), low_type, int(low_val), high_type, int(high_val))
                self.add_instruction(inst)

            

            
        

# def parse_data(data: str):
#     line_list = data.splitlines()

#     output_list = []
#     for line in line_list:
#         if line.startswith('value'):
#             nums = [char for char in line if char.isdigit()]
#             value = int(nums[0])
#             bot_id= int(nums[1])
#             bot = Bot()
#         else:
#             _, bot_id, _, _, _, low_type_str, low_val, _, _, _, high_type_str, high_val = line.split(' ')
#             low_type = Bot if low_type_str == 'bot' else OutputBin
#             high_type = Bot if high_type_str == 'bot' else OutputBin
#             inst = BotInstruction(int(bot_id), low_type, int(low_val), high_type, int(high_val))
#             output_list.append(inst)
            
    
def part_one(data: str):
    factory = Factory()
    factory.parse_data(data)
    print(factory)
    factory.execute_all_instruction()
    print(factory)

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()