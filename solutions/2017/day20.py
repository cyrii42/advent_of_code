from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE_PART_ONE = 'p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>\np=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>'
EXAMPLE_PART_TWO = ('p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>\np=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>'+
                    '\np=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>\np=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>')

INPUT = aoc.get_input(YEAR, DAY)

class Point(NamedTuple):
    x: int
    y: int
    z: int

@dataclass()
class Particle:
    id: int
    p: Point
    v: Point
    a: Point

    @property
    def distance(self) -> int:
        x, y, z = self.p
        return sum([abs(x), abs(y), abs(z)])

    def update_position(self) -> None:
        self.v = add_points(self.v, self.a)
        self.p = add_points(self.p, self.v)

    def __eq__(self, other):
        return self.p == other.p

def add_points(p1: Point, p2: Point) -> Point:
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return Point(x1+x2, y1+y2, z1+z2)

def parse_data(data: str) -> list[Particle]:
    line_list = data.splitlines()
    output_list = []
    for i, line in enumerate(line_list):
        line = (line.replace(' ', '').replace('<','').replace('>','')
                .replace('p=', '').replace('v=','').replace('a=',''))
        line = [int(x) for x in line.split(',')]
        px, py, pz, vx, vy, vz, ax, ay, az = line
        particle = Particle(
                    id=i,
                    p=Point(px, py, pz),
                    v=Point(vx, vy, vz),
                    a=Point(ax, ay, az))
        output_list.append(particle)
    return output_list
    
def part_one(data: str):
    particle_list = parse_data(data)
    for _ in range(10_000):
        for particle in particle_list:  
            particle.update_position()
    closest = next(particle for particle in
                   sorted(particle_list, key=lambda x: x.distance))
    return closest.id

def eliminate_matches(particle_list: list[Particle]) -> list[Particle]:
    for particle in particle_list:
        if particle_list.count(particle) > 1:
            particle_list = [p for p in particle_list if p != particle]
    return particle_list
            
def part_two(data: str):
    particle_list = parse_data(data)
    for _ in range(1000):
        for particle in particle_list:
            particle.update_position()
        if any(particle_list.count(p) > 1 for p in particle_list):
            particle_list = eliminate_matches(particle_list)
    return len(particle_list)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE_PART_ONE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()