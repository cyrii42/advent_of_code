import pathlib
from dataclasses import dataclass, field
from enum import Enum
import operator
from typing import NamedTuple, Optional, Callable

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class BotRecipientType(Enum):
    BOT = 'bot'
    BIN = 'output'

class ChipsAreEqual(Exception):
    pass

class TooManyChips(Exception):
    pass

class TooManyInstructions(Exception):
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
    high_recipient_id: int

class Comparison(NamedTuple):
    bot_id: int
    low_chip_value: int
    high_chip_value: int

@dataclass
class OutputBin:
    id: int
    chip: int

    def add_chip(self, chip_value: int) -> None:
        if self.chip:
            raise TooManyChips(f"Output Bin #{self.id} is already full.")
        self.chip = chip_value 

@dataclass
class Bot:
    id: int
    chip_1: Optional[int] = None
    chip_2: Optional[int] = None
    inst: Optional[BotInstruction] = None

    @property
    def ready(self) -> bool:
        return all(x for x in [self.chip_1, self.chip_2, self.inst])

    def add_chip(self, chip_value: int) -> None:
        if self.chip_1 and self.chip_2:
            raise TooManyChips(f"Bot #{self.id} already has two chips.") 
        if self.chip_1:
            self.chip_2 = chip_value
        else:
            self.chip_1 = chip_value

    def extract_high_chip(self) -> int:
        return self.extract_chip(func=operator.gt)

    def extract_low_chip(self) -> int:
        return self.extract_chip(func=operator.lt)

    def extract_chip(self, func: Callable) -> int:
        if not self.chip_1 and not self.chip_2:
            raise BotNotReady(f"Bot #{self.id} has no chips.")

        if self.chip_1 and self.chip_2:
            if self.chip_1 == self.chip_2:
                raise ChipsAreEqual(f"Bot #{self.id} has two chips of equal value.")
            if func(self.chip_1, self.chip_2):
                output = self.chip_1
                self.chip_1 = None
                return output
            else:
                output = self.chip_2
                self.chip_2 = None
                return output
        
        if self.chip_2 and not self.chip_1:
            output = self.chip_2
            self.chip_2 = None
            return output
        
        if self.chip_1 and not self.chip_2:
            output = self.chip_1
            self.chip_1 = None
            return output
        
        return -1

@dataclass
class Factory:
    bots: list[Bot] = field(default_factory=list)
    output_bins: list[OutputBin] = field(default_factory=list)
    comparisons: list[Comparison] = field(default_factory=list)

    def make_distribution(self, dist: Distribution):
        try:
            bot = self.get_bot_by_id(dist.bot_id)
            bot.add_chip(dist.value)
                
        except StopIteration:
            bot = Bot(id=dist.bot_id, chip_1=dist.value)
            self.bots.append(bot)

    def get_bot_by_id(self, bot_id: int) -> Bot:
        return next(bot for bot in self.bots if bot.id == bot_id)

    def get_bin_by_id(self, bin_id: int) -> OutputBin:
        return next(bin for bin in self.output_bins if bin.id == bin_id)

    def add_instruction(self, inst: BotInstruction):
        try:
            bot = self.get_bot_by_id(inst.bot_id)
            if bot.inst:
                raise TooManyInstructions(f"Bot #{inst.bot_id} already has instructions.")
            bot.inst = inst
            
        except StopIteration:
            bot = Bot(id=inst.bot_id, inst=inst)
            self.bots.append(bot)

    def execute_all_instructions(self):
        for bot in self.bots:
            self.execute_bot_instruction(bot)
            
    def execute_bot_instruction(self, bot: Bot):
        if not bot.chip_1 or not bot.chip_2 or not bot.inst:
            return 
        
        low_chip_value = bot.extract_low_chip()
        match bot.inst.low_recipient_type:
            case BotRecipientType.BOT:
                new_bot = self.create_bot_or_add_chip(bot.inst.low_recipient_id, 
                                                  low_chip_value)
                if new_bot.ready:
                    self.execute_bot_instruction(new_bot)
                
            case BotRecipientType.BIN:
                self.output_bins.append(OutputBin(bot.inst.low_recipient_id, 
                                                    low_chip_value))
        
        high_chip_value = bot.extract_high_chip()
        match bot.inst.high_recipient_type:
            case BotRecipientType.BOT:
                new_bot = self.create_bot_or_add_chip(bot.inst.high_recipient_id, 
                                                      high_chip_value)
                if new_bot.ready:
                    self.execute_bot_instruction(new_bot)
                
            case BotRecipientType.BIN:
                self.output_bins.append(OutputBin(bot.inst.high_recipient_id, 
                                                    high_chip_value))
                
        self.comparisons.append(Comparison(bot.id, low_chip_value, high_chip_value))

    def create_bot_or_add_chip(self, bot_id: int, value: int) -> Bot:
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
        return bot
            
    def parse_data(self, data: str) -> None:
        line_list = data.splitlines()

        for line in line_list:
            if line.startswith('value'):
                _, value, _, _, _, bot_id = line.split(' ')
                self.create_bot_or_add_chip(int(bot_id), int(value))
            else:
                _, bot_id, _, _, _, low_type_str, low_val, _, _, _, high_type_str, high_val = line.split(' ')
                low_type = BotRecipientType(low_type_str)
                high_type = BotRecipientType(high_type_str)
                inst = BotInstruction(int(bot_id), low_type, int(low_val), high_type, int(high_val))
                self.add_instruction(inst)

    def get_part_one_answer(self, high_val: int, low_val: int) -> int:
        comp = next(comp for comp in self.comparisons
                    if comp.high_chip_value == high_val
                    and comp.low_chip_value == low_val)
        return comp.bot_id

    def get_part_two_answer(self) -> int:
        bin_0 = self.get_bin_by_id(0)
        bin_1 = self.get_bin_by_id(1)
        bin_2 = self.get_bin_by_id(2)
        return bin_0.chip * bin_1.chip * bin_2.chip

def part_one(data: str):
    factory = Factory()
    factory.parse_data(data)
    factory.execute_all_instructions()
    if data == EXAMPLE:
        return factory.get_part_one_answer(5, 2)
    else:
        return factory.get_part_one_answer(61, 17)

def part_two(data: str):
    factory = Factory()
    factory.parse_data(data)
    factory.execute_all_instructions()
    return factory.get_part_two_answer()



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()