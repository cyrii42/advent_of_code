from pathlib import Path

import networkx as nx
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE_PART_ONE = 'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L'
EXAMPLE_PART_TWO = 'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN'
INPUT = aoc.get_input(YEAR, DAY)

def create_directed_graph(map: list[tuple[str, str]]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for parent, child in map:
        graph.add_edge(parent, child)
    return graph

def create_undirected_graph(map: list[tuple[str, str]]) -> nx.Graph:
    graph = nx.Graph()
    for parent, child in map:
        graph.add_edge(parent, child)
    return graph

def parse_data(data: str) -> list[tuple[str, str]]:
    line_list = [pair.split(')') for pair in data.splitlines()]
    return [(pair[0], pair[1]) for pair in line_list]
    
def part_one(data: str):
    map = parse_data(data)
    graph = create_directed_graph(map)
    return sum(len(nx.descendants(graph, n)) for n in graph)

def part_two(data: str):
    map = parse_data(data)
    graph = create_undirected_graph(map)
    return nx.shortest_path_length(graph, 'YOU', 'SAN') - 2

def main():
    print(f"Part One (example):  {part_one(EXAMPLE_PART_ONE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()