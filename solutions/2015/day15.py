import functools
import itertools
import operator
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

class CookieMismatch(Exception):
    pass

class Characteristic(Enum):
    CAPACITY = 0
    DURABILITY = 1
    FLAVOR = 2
    TEXTURE = 3
    CALORIES = 4

@dataclass
class Ingredient():
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    def get_score(self, characteristic: Characteristic, tsp: int) -> int:
        match characteristic:
            case Characteristic.CAPACITY:
                return tsp * self.capacity
            case Characteristic.DURABILITY:
                return tsp * self.durability
            case Characteristic.FLAVOR:
                return tsp * self.flavor
            case Characteristic.TEXTURE:
                return tsp * self.texture
            case Characteristic.CALORIES:
                return tsp * self.calories

@dataclass
class Cookie:
    ingredients: list[Ingredient]
    amounts: tuple[int, ...]
    total_score: int = 0
    total_capacity: int = 0
    total_durability: int = 0
    total_flavor: int = 0
    total_texture: int = 0
    total_calories: int = 0

    def __post_init__(self):
        if len(self.amounts) != len(self.ingredients):
            raise CookieMismatch(f"Invalid combo length: {len(self.amounts)}")
        
        for i, ingredient in enumerate(self.ingredients):
            tsp = self.amounts[i]
            self.total_capacity += ingredient.get_score(Characteristic.CAPACITY, tsp)
            self.total_durability += ingredient.get_score(Characteristic.DURABILITY, tsp)
            self.total_flavor += ingredient.get_score(Characteristic.FLAVOR, tsp)
            self.total_texture += ingredient.get_score(Characteristic.TEXTURE, tsp)
            self.total_calories += ingredient.get_score(Characteristic.CALORIES, tsp)
            
        self.total_score = self.get_total_score()

    def get_total_score(self) -> int:
        raw_nums = [self.total_capacity, self.total_durability, self.total_flavor, self.total_texture]
        nums_to_multiply = [max(num, 0) for num in raw_nums]

        return functools.reduce(operator.mul, nums_to_multiply, 1)

def parse_data(data: str):
    line_list = data.splitlines()

    output_list = []
    for line in line_list:
        parts = line.split(' ')
        name = parts[0].strip(':')
        capacity = int(parts[2].strip(','))
        durability = int(parts[4].strip(','))
        flavor = int(parts[6].strip(','))
        texture = int(parts[8].strip(','))
        calories = int(parts[-1])
            
        output_list.append(Ingredient(name, capacity, durability, flavor, texture, calories))
                
    return output_list
    
def part_one(data: str):
    ingredient_list = parse_data(data)
    combos = (x for x in itertools.product(range(101), repeat=len(ingredient_list)) if sum(x) == 100)
    cookies = (Cookie(ingredient_list, combo) for combo in combos)
    
    return max(cookie.total_score for cookie in cookies)
        
def part_two(data: str):
    ingredient_list = parse_data(data)
    combos = (x for x in itertools.product(range(101), repeat=len(ingredient_list)) if sum(x) == 100)
    cookies = (Cookie(ingredient_list, combo) for combo in combos)

    return max(cookie.total_score for cookie in cookies if cookie.total_calories == 500)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()