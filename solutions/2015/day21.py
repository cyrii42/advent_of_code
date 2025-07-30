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

class InventoryFull(Exception):
    pass

class ItemNotAvailable(Exception):
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
    damage: int
    defense: int

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
    equipped_weapon: Optional[Item] = None
    equipped_armor: Optional[Item] = None
    equipped_rings: list[Item] = field(default_factory=list)

    @property
    def total_gold_spent(self) -> int:
        return sum(item.cost for item in self.inventory)

    @property
    def inventory(self) -> list[Item]:
        output = deepcopy(self.equipped_rings)
        if self.equipped_weapon:
            output.append(deepcopy(self.equipped_weapon))
        if self.equipped_armor:
            output.append(deepcopy(self.equipped_armor))
        return output

    def clear_inventory(self):
        self.equipped_weapon = None

        self.equipped_armor = None
        self.defense = 0
        self.equipped_rings = list()
        self.defense = 0
        self.damage = 0

    def remove_item(self, item_to_remove: Item):
        match item_to_remove.type:
            case ItemType.WEAPON:
                if not self.equipped_weapon:
                    print("No weapon equipped.")
                    return
                if self.equipped_weapon != item_to_remove:
                    print(f"Cannot remove weapon {item_to_remove.name}; does not match",
                          f"currently equipped weapon {self.equipped_weapon.name}")
                    return
                if self.equipped_weapon == item_to_remove:
                    print(f"Removing equipped weapon:  \"{self.equipped_weapon.name}\" (damage: {self.equipped_weapon.damage})")
                    self.equipped_weapon = None
            case ItemType.ARMOR:
                if not self.equipped_armor:
                    print("No armor equipped.")
                    return
                if self.equipped_armor != item_to_remove:
                    print(f"Cannot remove armor \"{item_to_remove.name}\"; does not match",
                          f"currently equipped armor \"{self.equipped_armor.name}\"")
                    return
                else:
                    print(f"Removing equipped armor:  \"{self.equipped_armor.name}\" (defense: {self.equipped_armor.defense})")
                    self.equipped_armor = None
            case ItemType.RING:
                if item_to_remove not in self.equipped_rings:
                    print(f"Ring \"{item_to_remove.name}\" is not in current inventory; cannot remove.")
                    return
                else:
                    idx = [i for i, ring in enumerate(self.equipped_rings) if ring == item_to_remove][0]
                    print(f"Removing equipped ring:  \"{item_to_remove.name}\"")
                    self.equipped_rings.pop(idx)
    
    def add_item(self, item: Item):
        match item.type:
            case ItemType.WEAPON:
                self.equipped_weapon = item
                self.damage += item.damage
                # print(f"New weapon equipped: \"{item.name}\" (cost: {item.cost})")
            case ItemType.ARMOR:
                self.equipped_armor = item
                self.defense = item.defense
                # print(f"New armor equipped: \"{item.name}\" (cost: {item.cost})")
            case ItemType.RING:
                if item in self.equipped_rings:
                    print(f"Ring \"{item.name}\" already in inventory.  Cannot add.")
                    return
                if len(self.equipped_rings) == 2:
                    outgoing = self.equipped_rings.pop(0)
                    self.damage -= outgoing.damage
                    self.defense -= outgoing.defense
                    print(f"Ring inventory full.  Removing first-equipped ring (\"{outgoing.name}\")",
                          f"and replacing with \"{item.name}\" (cost: {item.cost})")
                # else:
                    # print(f"New ring equipped: \"{item.name}\" (cost: {item.cost})")
                self.equipped_rings.append(item)
                self.damage += item.damage
                self.defense = item.defense

    def clear_ring_inventory(self):
        print("Clearing ring inventory.  No rings equipped.")
        self.equipped_rings = list()

    

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
    rings = [Item(*x) for x in RING_SHOP]

    boss = Boss(12, 7, 2)
    player = Player(8, 5, 5)

    simulate_game(player, boss)
    
    
def part_one(data: str):
    weapons = [Item(*x) for x in WEAPON_SHOP]
    armor = [Item(*x) for x in ARMOR_SHOP]
    rings = [Item(*x) for x in RING_SHOP]
    
    boss_hp, boss_damage, boss_defense = parse_data(data)
    boss = Boss(boss_hp, boss_damage, boss_defense)
    player = Player(100, 0, 0)
    
    simulate_game(player, boss, print_info=False)
    print('---------------------------')

    unequipped_loss_margin = boss.HP

    a = deepcopy(weapons)
    b = deepcopy(armor)
    c = deepcopy(rings)
    d = deepcopy(rings)

    loadouts = (x for x in itertools.product(a, b, c, d) if x[2] != x[3])

    win_list = []
    while True:
        try:
            player.clear_inventory()
            player.HP = 100
            boss.HP = boss_hp
            
            next_try = next(loadouts)
            for item in next_try:
                player.add_item(item)
            
            player_wins, gold_spent = simulate_game(player, boss, print_info=False)

            if player_wins:
                print(f"WIN!  {gold_spent}")
                win_list.append(gold_spent)
        except StopIteration:
            return min(win_list)
        

'''
STOPPING FOR NOW, BUT:  YOUR PROBLEM IS THAT YOU'RE ONLY ITERATING THROUGH THE SCENARIOS
WHERE EVERY INVENTORY SLOT IS FILLED.  THERE MIGHT BE WINNING SCENARIOS WHERE SOME ARE EMPTY!
'''



def part_two(data: str):
    __ = parse_data(data)



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