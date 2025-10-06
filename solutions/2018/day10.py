from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class Position(NamedTuple):
    x: int
    y: int

class Velocity(Position):
    pass

@dataclass
class Light:
    position: Position
    velocity: Velocity

    def increment(self) -> None:
        x, y = self.position
        vx, vy = self.velocity
        self.position = Position(x + vx, y + vy)

@dataclass
class LightGroup:
    lights: list[Light]

    @property
    def lit_points(self) -> list[Position]:
        return [light.position for light in self.lights]

    @property
    def num_unique_columns(self) -> int:
        return len(set([light.position.y for light in self.lights]))

    @property
    def min_max(self) -> tuple[int, int, int, int]:
        ''' Returns: (min_x, min_y, max_x, max_y) '''
        min_x = min(light.position.x for light in self.lights)
        min_y = min(light.position.y for light in self.lights)
        max_x = max(light.position.x for light in self.lights)
        max_y = max(light.position.y for light in self.lights)

        return (min_x, min_y, max_x, max_y)

    def print_grid(self) -> None:
        min_x, min_y, max_x, max_y = self.min_max

        for y in range(min_y, max_y+1):
            row = ''
            for x in range(min_x, max_x+1):
                pos = Position(x, y)
                row += '#' if pos in self.lit_points else '.'
            print(row)

    def increment(self) -> None:
        for light in self.lights:
            light.increment()
            
def parse_data(data: str):
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        line = line.replace('position=', '').replace('velocity=', '')
        line = line.replace('<', '').replace('>', '').replace(',', '')
        x, y, vx, vy = [int(num) for num in line.split(' ') if num]
        output_list.append(Light(Position(x, y), Velocity(vx, vy)))
    return LightGroup(output_list)

def run_example():
    data = EXAMPLE
    lights = parse_data(data)
    for _ in range(3):
        lights.increment()
    lights.print_grid()
    print()
    
def part_one_and_part_two(data: str):
    lights = parse_data(data)
    starting_unique_cols = lights.num_unique_columns
    
    total_time = 0
    while lights.num_unique_columns >= starting_unique_cols - 80:
        total_time += 1
        lights.increment()
        
    lights.print_grid()
    return total_time
        
def main():
    run_example()
    print(f"Part Two Answer:  {part_one_and_part_two(INPUT)}")
       
if __name__ == '__main__':
    main()