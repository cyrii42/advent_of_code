import functools
import itertools
import json
import math
import os
import re
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

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

'''
In this game, the player (you) and the enemy (the boss) 
take turns attacking. The player always goes first. Each 
attack reduces the opponent's hit points by at least 1. 
The first character at or below 0 hit points loses.

Damage dealt by an attacker each turn is equal to the 
attacker's damage score minus the defender's armor score. 
An attacker always does at least 1 damage. So, if the
attacker has a damage score of 8, and the defender has 
an armor score of 3, the defender loses 5 hit points. 
If the defender had an armor score of 300, the defender 
would still lose 1 hit point.

Your damage score and armor score both start at zero. 
They can be increased by buying items in exchange for gold. 
You start with no items and have as much gold as you need. 
Your total damage or armor is equal to the sum of those 
stats from all of your items. You have 100 hit points.

Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3

You must buy exactly one weapon; no dual-wielding. 
Armor is optional, but you can't use more than one. 
You can buy 0-2 rings (at most one for each hand). 
You must use any items you buy. The shop only has 
one of each item, so you can't buy, for example, 
two rings of Damage +3.
'''

class ItemType(Enum):
    WEAPON = 1
    ARMOR = 2
    RING = 3

WEAPON_SHOP = [
    ('Dagger', ItemType.WEAPON, 8, 4, 0),
    ('Shortsword', ItemType.WEAPON, 10, 5, 0),
    ('Warhammer', ItemType.WEAPON, 25, 6, 0),
    ('Longsword', ItemType.WEAPON, 40, 7, 0),
    ('Greataxe', ItemType.WEAPON, 74, 8, 0),
]

ARMOR_SHOP = [
    ('Leather', ItemType.ARMOR, 13, 0, 1),
    ('Chainmail', ItemType.ARMOR, 31, 0, 2),
    ('Splintmail', ItemType.ARMOR, 53, 0, 3),
    ('Bandedmail', ItemType.ARMOR, 75, 0, 4),
    ('Platemail', ItemType.ARMOR, 102, 0, 5),
]

RING_SHOP = [
    ('Damage +1', ItemType.RING, 25, 1, 0),
    ('Damage +2', ItemType.RING, 50, 2, 0),
    ('Damage +3', ItemType.RING, 100, 3, 0),
    ('Defense +1', ItemType.RING, 20, 0, 1),
    ('Defense +2', ItemType.RING, 40, 0, 2),
    ('Defense +3', ItemType.RING, 80, 0, 3),
]

class InventoryException(Exception):
    pass

class InventoryFull(InventoryException):
    pass

class ItemMax(InventoryException):
    pass

class ItemNotAvailable(InventoryException):
    pass

@dataclass
class Item:
    name: str
    type: ItemType
    cost: int
    damage: int
    defense: int

@dataclass
class Character:
    HP: int
    _damage: int = field(default=0, repr=False)
    _defense: int = field(default=0, repr=False)

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value: int):
        self._damage = value

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value: int):
        self._defense = value

    def take_damage(self, opponent: "Character"):
        damage_inflicted = max(1, opponent.damage-self.defense)
        self.HP = max(0, self.HP-damage_inflicted)

    def attack(self, opponent: "Character"):
        damage_inflicted = max(1, self.damage-opponent.defense)
        opponent.HP = max(0, opponent.HP-damage_inflicted)
    

@dataclass
class Boss(Character):
    pass
    

@dataclass
class Player(Character):
    inventory: list[Item] = field(default_factory=list)

    @property
    def damage(self):
        return sum(item.damage for item in self.inventory)

    @damage.setter
    def damage(self, value: int):
        self._damage = value

    @property
    def defense(self):
        return sum(item.defense for item in self.inventory)

    @defense.setter
    def defense(self, value: int):
        self._defense = value

    @property
    def total_gold_spent(self) -> int:
        return sum(item.cost for item in self.inventory)

    def clear_inventory(self):
        self.inventory = list()

    def add_item(self, item_to_add: Item):
        try:
            self._add_item(item_to_add)
        except InventoryException as e:
            print(f"ERROR: {e}")
            return

    def _add_item(self, item_to_add: Item):
        if len(self.inventory) >= 4:
            raise InventoryFull(f"Inventory already contains {len(self.inventory)} items.  Cannot add more.")

        max_items = 2 if item_to_add.type == ItemType.RING else 1
        if len([item for item in self.inventory if item.type == item_to_add.type]) >= max_items:
            raise ItemMax(f"Inventory already contains maximum ({max_items}) of type \"{item_to_add.type.name}\"")

        if item_to_add in self.inventory:
            raise ItemNotAvailable(f"Item {item_to_add.name} is already in inventory.")

        self.inventory.append(item_to_add)

    def remove_item(self, item_to_remove: Item):
        if item_to_remove not in self.inventory:
            print(f"Item \"{item_to_remove.name}\" is not in current inventory; cannot remove.")
            return

        else:
            idx = [i for i, item in enumerate(self.inventory) if item == item_to_remove][0]
            print(f"Removing equipped item:  \"{item_to_remove.name}\"")
            self.inventory.pop(idx)

    

def parse_data(data: str):   
    line_list = data.splitlines()
    boss_hp = int(line_list[0].split(' ')[-1])
    boss_damage = int(line_list[1].split(' ')[-1])
    boss_defense = int(line_list[2].split(' ')[-1])
    return (boss_hp, boss_damage, boss_defense)


def simulate_game(player: Player, boss: Boss, print_info: bool = True) -> tuple[bool, int]:
    ''' Returns a tuple: true/false for player win, and total gold spent by the player '''
    n = 0
    while player.HP > 0 and boss.HP > 0:
        if n % 2 == 0:
            player.attack(boss)
            # print(f"Player attacks!  Boss HP:  {boss.HP}")
        else:
            boss.attack(player)
            # print(f"Boss attacks!  Player HP:  {player.HP}")
        n += 1
    
        # print('-----------------------')
    if print_info:
        if player.HP > boss.HP:
            print(f"Player wins! ({n+1} rounds)")        
        else:
            print(f"Boss wins! ({n+1} rounds)")

        print("\nRemaining HP:")
        print(f"Player:\t{player.HP}")
        print(f"Boss:\t{boss.HP}")
        print(f"\nGold:\t{player.total_gold_spent}")
    # print('-----------------------')

    player_wins = player.HP > boss.HP
    return (player_wins, player.total_gold_spent)


    
def example_part_one():
    weapons = [Item(*x) for x in WEAPON_SHOP]
    armor = [Item(*x) for x in ARMOR_SHOP]

    boss = Boss(12, 7, 2)
    
    player = Player(8)
    player.add_item(weapons[1])
    player.add_item(armor[4])

    simulate_game(player, boss)
    
    
def part_one(data: str):
    weapons = [Item(*x) for x in WEAPON_SHOP]
    armor = [Item(*x) for x in ARMOR_SHOP]
    rings = [Item(*x) for x in RING_SHOP]
    
    boss_hp, boss_damage, boss_defense = parse_data(data)
    boss = Boss(boss_hp, boss_damage, boss_defense)

    loadouts = (x for x in itertools.product([None, 0, 1, 2, 3, 4, 5], repeat=4) 
                if x[0] != 5
                and x[1] != 5
                and not (x[2] and x[3] and x[2] == x[3]))

    win_list = []
    while True:
        try:
            weapon_idx, armor_idx, ring1_idx, ring2_idx = next(loadouts)
            boss = Boss(109, 8, 2)
            player = Player(100)
            if weapon_idx is not None:
                player.add_item(weapons[weapon_idx])
            if armor_idx is not None:
                player.add_item(armor[armor_idx])
            if ring1_idx is not None:
                player.add_item(rings[ring1_idx])
            if ring2_idx is not None:
                player.add_item(rings[ring2_idx])
            player_wins, gold_spent = simulate_game(player, boss, print_info=False)
            if player_wins:
                win_list.append(gold_spent)
        except StopIteration:
            return min(win_list)

def part_two(data: str):
    ...




def main():
    # print(f"Part One (example):  {example_part_one()}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
        
       
if __name__ == '__main__':
    main()