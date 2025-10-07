from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

@dataclass
class PlantGroup:
    pot_dict: dict[int, bool]
    note_dict: dict[tuple[bool, ...], bool]

    def simulate_growth(self, num_generations: int = 20):
        for _ in range(num_generations):
            new_dict = defaultdict(bool)
            min_pot_num = min(k for k in self.pot_dict.keys())
            max_pot_num = max(k for k in self.pot_dict.keys())
            for pot_num in range(min_pot_num-2, max_pot_num+3):
                group = tuple(self.pot_dict[x] for x in range(pot_num-2, pot_num+3))
                if group in self.note_dict:
                    new_dict[pot_num] = self.note_dict[group]
                else:
                    new_dict[pot_num] = False
            self.pot_dict = new_dict
           
        pots_with_plants = (k for k, v in self.pot_dict.items() if v)
        
        return sum(pots_with_plants)

    def print_pots(self):
        output = ''
        for value in self.pot_dict.values():
            output += '#' if value else '.'
        print(output)
                

def process_initial_state(initial_state_line: str):
    output_dict = defaultdict(bool)
    for i, char in enumerate(initial_state_line):
        output_dict[i] = True if char == '#' else False
    return output_dict

def process_note_list(line_list: list[str]) -> dict[tuple[bool, ...], bool]:
    output_dict = {}
    for line in line_list:
        state_list, _, outcome = line.split(' ')
        state_tuple = tuple(True if char == '#' else False for char in state_list)
        output_dict[state_tuple] = True if outcome == '#' else False
    return output_dict

def parse_data(data: str) -> PlantGroup:
    line_list = data.splitlines()
    initial_state_line = line_list[0].removeprefix('initial state: ')
    initial_state = process_initial_state(initial_state_line)
    note_list = process_note_list(line_list[2:])
    return PlantGroup(initial_state, note_list)
    
def part_one(data: str):
    plants = parse_data(data)
    answer = plants.simulate_growth()
    return answer

def part_two_exploration(data: str):
    for x in range(2, 201):
        plants1 = parse_data(data)
        plants2 = parse_data(data)
        answer1 = plants1.simulate_growth(num_generations=x-1)
        answer2 = plants2.simulate_growth(num_generations=x)
        print(f"{x}:  {answer2} - {answer2 - answer1}")

    return 4107 + ((50_000_000_000 - 163) * 23)

def part_two(data: str):
    return 4107 + ((50_000_000_000 - 163) * 23)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()