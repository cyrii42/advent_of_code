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
from typing import Callable, Iterable, NamedTuple, Optional, Protocol, Self

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

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

class InsufficientMana(Exception):
    pass

class OutOfMana(Exception):
    pass

class NoActiveSpell(Exception):
    pass

class EffectAlreadyActive(Exception):
    pass

class Spell(Enum):
    MAGIC_MISSILE = 0
    DRAIN = 1
    SHIELD = 2
    POISON = 3
    RECHARGE = 4

SPELL_PRICES = {
    Spell.MAGIC_MISSILE: 53,
    Spell.DRAIN: 73,
    Spell.SHIELD: 113,
    Spell.POISON: 173,
    Spell.RECHARGE: 229
}

@dataclass
class Boss:
    HP: int
    damage: int = 0
    defense: int = 0
    
    def attack(self, player: "Player"):
        damage_inflicted = max(1, self.damage - player.defense)
        player.HP -= damage_inflicted
    

@dataclass
class Player:
    HP: int = 50
    mana: int = 500
    damage: int = 0
    defense: int = 0
    shield_active: bool = False
    shield_timer: int = 0
    poison_active: bool = False
    poison_timer: int = 0
    recharge_active: bool = False
    recharge_timer: int = 0
    total_mana_spent: int = 0

    def apply_current_effects(self, boss: Boss, print_info: bool = True):
        if not any([self.shield_active, self.poison_active, self.recharge_active]):
            return

        if self.shield_active:
            self.defense = 7  # prompt says "increased by 7" but it's otherwise always zero
            self.shield_timer -= 1
            if print_info:
                print(f"Player's SHIELD spell is active ({self.shield_timer} turns left)!")
            if self.shield_timer <= 0:
                self.shield_active = False
                self.defense = 0  # resetting SHIELD (or just keeping it at zero)
        if self.poison_active:
            boss.HP -= 3
            self.poison_timer -= 1
            if print_info:
                print(f"Player's POISON spell is active ({self.poison_timer} turns left)!",
                  f"Boss HP: {boss.HP}")
            if self.poison_timer <= 0:
                self.poison_active = False
        if self.recharge_active:
            self.mana += 101
            self.recharge_timer -= 1
            if print_info:
                print(f"Player's RECHARGE spell is active ({self.recharge_timer} turns left)!",
                  f"Player mana: {self.mana}")
            if self.recharge_timer <= 0:
                self.recharge_active = False

    def spend_mana(self, spell: Spell):
        cost = SPELL_PRICES[spell]
        if self.mana < min(v for v in SPELL_PRICES.values()):
            raise OutOfMana("Player does not have enough mana to cast any spell.")
        if self.mana < cost:
            raise InsufficientMana(f"Player has insufficent mana ({self.mana}) to cast {spell.name} (cost: {cost})!")
        self.mana -= cost
        self.total_mana_spent += cost

    def cast_spell(self, spell: Spell, boss: Boss, print_info: bool = True):                  
        match spell:
            case Spell.MAGIC_MISSILE:
                self.spend_mana(spell)
                boss.HP -= 4
            case Spell.DRAIN:
                self.spend_mana(spell)
                boss.HP -= 2
                self.HP += 2
            case Spell.SHIELD:
                if self.shield_active:
                    raise EffectAlreadyActive("SHIELD is already active.")
                self.spend_mana(spell)
                self.defense = 7  # prompt says "increased by 7" but it's otherwise always zero
                self.shield_active = True
                self.shield_timer = 6
            case Spell.POISON:
                if self.poison_active:
                    raise EffectAlreadyActive("POISON is already active.")
                self.spend_mana(spell)
                self.poison_active = True
                self.poison_timer = 6
            case Spell.RECHARGE:
                if self.recharge_active:
                    raise EffectAlreadyActive("RECHARGE is already active.")
                self.spend_mana(spell)
                self.recharge_active = True
                self.recharge_timer = 5

                
def get_spell_from_user() -> Spell:
    msg = "Which spell?  Magic Missile (53) | Drain (73) | Shield (113) | Poison (173) | Recharge (229)?  "
    choice = input(msg).upper()
    if choice not in ['MM', 'MAGIC MISSILE', 'D', 'DRAIN', 'S', 'SHIELD', 'P', 'POISON', 'R', 'RECHARGE']:
        print("INVALID INPUT")
        return get_spell_from_user()

    match choice:
        case 'MM' | 'MAGIC MISSILE':
            return Spell.MAGIC_MISSILE
        case 'D' | 'DRAIN':
            return Spell.DRAIN
        case 'S' | 'SHIELD':
            return Spell.SHIELD
        case 'P' | 'POISON':
            return Spell.POISON
        case 'R' | 'RECHARGE':
            return Spell.RECHARGE
        case _:
            raise ValueError
            

def play_game(player: Player, boss: Boss, hard_mode: bool = False) -> tuple[bool, int]:
    ''' Returns a tuple: true/false for player win, and total gold spent by the player '''
    n = 0
    spells_cast = []
    while player.HP > 0 and boss.HP > 0:
        print(f"\n------ ROUND {n+1} -------")
        print(f"Player: {player.HP} HP, {player.mana} mana, {player.defense} defense | Boss HP: {boss.HP}")
        if n % 2 == 0:
            if hard_mode:
                player.HP -= 1
                if player.HP <= 0:
                    break
            spell = get_spell_from_user()
            player.apply_current_effects(boss)
            if boss.HP <= 0:
                break

            try:
                player.cast_spell(spell, boss)
            except EffectAlreadyActive as e:
                print(e)
                while True:
                    try:
                        spell = get_spell_from_user()
                        player.cast_spell(spell, boss)
                        break
                    except EffectAlreadyActive as e:
                        print(e)
                        continue
            except InsufficientMana as e:
                print(e)
                while True:
                    try:
                        spell = get_spell_from_user()
                        player.cast_spell(spell, boss)
                        break
                    except InsufficientMana as e:
                        print(e)
                        continue
                    except EffectAlreadyActive as e:
                        print(e)
                        while True:
                            try:
                                spell = get_spell_from_user()
                                player.cast_spell(spell, boss)
                                break
                            except EffectAlreadyActive as e:
                                print(e)
                                continue
            except OutOfMana as e:
                print(e)
                n += 1
                continue
            else:
                spells_cast.append(spell)
                print(f"Player casts {spell.name}!")
        else:
            player.apply_current_effects(boss)
            if boss.HP <= 0:
                break
            boss.attack(player)
            print("Boss attacks!")
        n += 1

    print_game_info(player, boss, n)
        
    player_wins = player.mana > 0 and player.HP > boss.HP
    if player_wins:
        print(spells_cast)
    return (player_wins, player.total_mana_spent)



def simulate_game(player: Player, 
                  boss: Boss, 
                  spell_list: tuple[Spell, ...], 
                  print_info: bool = True,
                  hard_mode: bool = False) -> tuple[bool, int]:
    ''' Returns a tuple: true/false for player win, and total gold spent by the player '''
    n = 0
    spell_num = 0
    if print_info:
        print(f"\n\nMATCHUP:  Player HP: {player.HP} Player mana: {player.mana} | Boss HP: {boss.HP}")
    while player.HP > 0 and boss.HP > 0:
        if print_info:
            print(f"------ ROUND {n+1} -------")
        if n % 2 == 0:
            if hard_mode:
                player.HP -= 1
                if player.HP <= 0:
                    break
            player.apply_current_effects(boss, print_info=print_info)
            if boss.HP <= 0:
                break
            
            try:
                spell = spell_list[spell_num]
            except IndexError:
                if print_info:
                    print(f"No spells remaining! Player HP: {player.HP} Player mana: {player.mana} | Boss HP: {boss.HP}")
                return (False, 999999999)

            try:
                player.cast_spell(spell, boss, print_info=print_info)
                spell_num += 1
                if print_info:
                    print(f"Player casts {spell.name}! Player HP: {player.HP} Player mana: {player.mana} | Boss HP: {boss.HP}")
            except (OutOfMana, InsufficientMana):
                if print_info:
                    print(f"Player is out of mana! Player HP: {player.HP} Player mana: {player.mana} | Boss HP: {boss.HP}")
                return (False, player.total_mana_spent)
        else:
            player.apply_current_effects(boss, print_info=print_info)
            if boss.HP <= 0:
                break
            boss.attack(player)
            if print_info:
                print(f"Boss attacks! Player HP: {player.HP} Player mana: {player.mana} | Boss HP: {boss.HP}")
        n += 1

    if print_info:
        print_game_info(player, boss, n)
        
    player_wins = player.HP > boss.HP
    return (player_wins, player.total_mana_spent)

def print_game_info(player: Player, boss: Boss, n: int):
    print("\n-------------------------------")
    if player.HP > boss.HP:
        print(f"Player wins! ({n+1} rounds)")        
    else:
        print(f"Boss wins! ({n+1} rounds)")

    print(f"Player:\t{player.HP} HP | {player.mana} mana")
    print(f"Boss:\t{boss.HP} HP")
    
    print(f"Mana Spent: {player.total_mana_spent}")

    


    
def example_one():
    player = Player(HP=10, mana=250)
    boss = Boss(HP=13, damage=8)

    spell_list = (
        Spell.POISON,
        Spell.MAGIC_MISSILE,
    )
    simulate_game(player, boss, spell_list, print_info=True)

def example_two():
    player = Player(HP=10, mana=250)
    boss = Boss(HP=14, damage=8)

    spell_list = (
        Spell.RECHARGE,
        Spell.SHIELD,
        Spell.DRAIN,
        Spell.POISON,
        Spell.MAGIC_MISSILE,
    )
    simulate_game(player, boss, spell_list, print_info=True)
            
def parse_data(data: str):   
    line_list = data.splitlines()
    boss_hp = int(line_list[0].split(' ')[-1])
    boss_damage = int(line_list[1].split(' ')[-1])
    return (boss_hp, boss_damage)


def get_mana_spent_from_spell_list(spell_list: list[Spell]):
    return sum(SPELL_PRICES[spell] for spell in spell_list)
    
def part_one(data: str, hard_mode: bool=False, num_outer_loops: int = 10):
    lowest_mana_spent = 99999999999
    for x in range(num_outer_loops):
        for spell_list in alive_it(itertools.product([spell for spell in Spell], repeat=x), total=5**x):  # type: ignore
            if sum(SPELL_PRICES[spell] for spell in spell_list) >= lowest_mana_spent:
                continue
            
            player = Player(HP=50, mana=500)
            boss_hp, boss_damage = parse_data(data)
            boss = Boss(HP=boss_hp, damage=boss_damage)
            try:
                player_wins, mana_spent = simulate_game(player, boss, spell_list, print_info=False, hard_mode=hard_mode)
            except EffectAlreadyActive:
                continue
            if player_wins:
                if mana_spent < lowest_mana_spent:
                    lowest_mana_spent = mana_spent
                print(f"WIN! (mana: {mana_spent:,}) (lowest so far: {lowest_mana_spent:,})")
    return lowest_mana_spent

def part_two(data: str):
    return part_one(data, hard_mode=True)




def main():
    example_one()
    example_two()
    print()
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
       
if __name__ == '__main__':
    main()