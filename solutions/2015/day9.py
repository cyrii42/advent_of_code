import itertools
from dataclasses import dataclass
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

@dataclass
class Flight:
    start: str
    end: str
    distance: int

@dataclass
class FlightSet:
    flights: list[Flight]

    def __post_init__(self):
        self.all_cities = ({f.start for f in self.flights} 
                           | {f.end for f in self.flights})

    def get_distance(self, start: str, end: str) -> int:
        flight = [f for f in self.flights if 
                  (f.start == start and f.end == end)
                  or (f.start == end and f.end == start)][0]
        return flight.distance

    def get_route(self, distance: int) -> Flight:
        return [f for f in self.flights if f.distance == distance][0]

def parse_data(data: str) -> FlightSet:
    line_list = [line for line in data.split('\n') if line]
    output_list = []
    for line in line_list:
        parts = line.split(' ')
        output_list.append(Flight(parts[0], parts[2], int(parts[4])))
    return FlightSet(output_list)

def get_route_distances(flight_set: FlightSet) -> list[int]:
    perms = itertools.permutations(flight_set.all_cities, 
                                   len(flight_set.all_cities))

    route_distances = []
    for route in perms:
        route_distance = 0
        for i, city in enumerate(route):
            if i == len(route) - 1:
                break
            route_distance += flight_set.get_distance(city, route[i+1])
        route_distances.append(route_distance)
    return route_distances

    
def part_one(data: str):
    flight_set = parse_data(data)
    route_distances = get_route_distances(flight_set)
    return min(route_distances)       
    

def part_two(data: str):
    flight_set = parse_data(data)
    route_distances = get_route_distances(flight_set)
    return max(route_distances)



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