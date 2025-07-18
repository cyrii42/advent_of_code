'''--- Day 11: Monkey in the Middle ---'''

import math
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from operator import add, mul
from pathlib import Path
from typing import Literal, NamedTuple, Optional, Self

from alive_progress import alive_it
from rich import print

from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day11_example.txt'
INPUT = DATA_DIR / '2022_day11_input.txt'

@dataclass
class Item:
    worry_level: int

    def apply_operation(self, operation: str) -> None:
        operand_str, num_str = operation.split(' ')

        match operand_str:
            case '*':
                operand = mul
            case '+':
                operand = add
            case _:
                raise ValueError(f"Unrecognized operand string: {operand_str}")

        if num_str == 'old':
            self.worry_level = operand(self.worry_level, self.worry_level)
        else:
            self.worry_level = operand(self.worry_level, int(num_str))

    def divide_for_boredom(self):
        self.worry_level = self.worry_level // 3

    def apply_test(self, test_num: int) -> bool:
        return self.worry_level % test_num == 0

@dataclass
class Monkey:
    num: int
    item_list: list[Item]
    operation: str = field(repr=False)
    test_num: int = field(repr=False)
    next_monkey_true: int = field(repr=False)
    next_monkey_false: int = field(repr=False)
    inspection_count: int = 0

    @classmethod
    def create_monkey(cls, line_list: list[str]) -> Self:
        monkey_num = int(line_list[0][-2])

        starting_items = line_list[1].strip('Starting items: ').split(',')
        starting_items = [Item(int(item.strip(' '))) for item in starting_items]

        operation = line_list[2][21:]

        test = int(''.join(char for char in line_list[3] if char.isnumeric()))

        next_monkey_true = int(''.join(char for char in line_list[4] if char.isnumeric()))
        next_monkey_false = int(''.join(char for char in line_list[5] if char.isnumeric()))
       
        return cls(monkey_num, starting_items, operation, test, next_monkey_true, next_monkey_false)
    
    def receive_item(self, item: Item) -> None:
        self.item_list.append(item)

    def delete_item(self, item_to_drop: Item) -> None:
        self.item_list = [item for item in self.item_list if item.worry_level != item_to_drop.worry_level]


@dataclass
class Game:
    monkey_list: list[Monkey]

    @property
    def least_common_multiple(self) -> int:
        return math.lcm(*[monkey.test_num for monkey in self.monkey_list])

    def get_monkey_by_num(self, num: int) -> Monkey:
        return [monkey for monkey in self.monkey_list if monkey.num == num][0]

    def play_round(self, part_one: bool = True):
        for monkey in self.monkey_list:
            items_to_drop: list[Item] = []
            for item in monkey.item_list:
                monkey.inspection_count += 1
                item.apply_operation(monkey.operation)
                if part_one:
                    item.divide_for_boredom()
                else:
                    item.worry_level = item.worry_level % self.least_common_multiple
                
                if item.apply_test(monkey.test_num):
                    next_monkey = self.get_monkey_by_num(monkey.next_monkey_true)
                    next_monkey.receive_item(item)
                    items_to_drop.append(item)
                else:
                    next_monkey = self.get_monkey_by_num(monkey.next_monkey_false)
                    next_monkey.receive_item(item)
                    items_to_drop.append(item)
            for item in items_to_drop:
                monkey.delete_item(item)

    def get_answer(self) -> int:
        inspection_counts = [monkey.inspection_count for monkey in self.monkey_list]
        inspection_counts = sorted(inspection_counts, reverse=True)
        return inspection_counts[0] * inspection_counts[1]


def ingest_data(filename: Path):
    with open(filename) as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        line_list = [line.strip(' ') for line in line_list if len(line) > 0]
    return line_list

def create_monkeys(line_list: list[str]) -> list[Monkey]:
    output_list = []
    for x in range(6, len(line_list)+1, 6):
        output_list.append(Monkey.create_monkey(line_list[x-6:x]))
    return output_list

def part_one(filename: Path):
    line_list = ingest_data(filename)
    monkeys = create_monkeys(line_list)
    game = Game(monkeys)
    for x in range(20):
        game.play_round()
    return game.get_answer()

def part_two(filename: Path):
    line_list = ingest_data(filename)
    monkeys = create_monkeys(line_list)
    game = Game(monkeys)
    for _ in range(10_000):
        game.play_round(part_one=False)
    return game.get_answer()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 
    print(f"Part One (input):  {part_one(INPUT)}") # 
    
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # 
    print(f"Part Two (input):  {part_two(INPUT)}") # 

    random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()
