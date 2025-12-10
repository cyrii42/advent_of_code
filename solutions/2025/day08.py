import itertools
import math
from pathlib import Path
from typing import NamedTuple
import networkx as nx
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class Point(NamedTuple):
    x: int
    y: int
    z: int

def get_distance(n1: Point, n2: Point) -> float:
    ''' https://en.wikipedia.org/wiki/Euclidean_distance#Higher_dimensions '''
    return math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2 + (n1.z - n2.z)**2)

def part_one(data: str, stop: int = 1000):
    point_list = [Point(*[int(x) for x in line.split(',')]) 
                  for line in data.splitlines()]
    distance_dict = {get_distance(p1, p2): (p1, p2) for p1, p2 
                     in itertools.permutations(point_list, 2)}
    distances = sorted(distance_dict.keys())
  
    graph = nx.Graph()
    for distance in distances[0:stop]:
        p1, p2 = distance_dict[distance]
        graph.add_weighted_edges_from([(p1, p2, distance)])

    components = sorted(list(nx.connected_components(graph)), key=len, reverse=True)
    return len(components[0]) * len(components[1]) * len(components[2])

def part_two(data: str, stop: int = 1000):
    point_list = [Point(*[int(x) for x in line.split(',')]) 
                  for line in data.splitlines()]
    distance_dict = {get_distance(p1, p2): (p1, p2) for p1, p2 
                     in itertools.permutations(point_list, 2)}
    distances = sorted(distance_dict.keys())
  
    graph = nx.Graph()
    for distance in distances:
        p1, p2 = distance_dict[distance]
        graph.add_weighted_edges_from([(p1, p2, distance)])
        if nx.is_connected(graph) and len(graph.nodes) == len(point_list):
            return p1.x * p2.x

def main():
    print(f"Part One (example):  {part_one(EXAMPLE, stop = 10)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE, stop = 10)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()