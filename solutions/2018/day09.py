import itertools
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)
TESTS_PART_ONE = [
    ('9 players; last marble is worth 25 points', 32),
    ('10 players; last marble is worth 1618 points', 8317),
    ('13 players; last marble is worth 7999 points', 146373),
    ('17 players; last marble is worth 1104 points', 2764),
    ('21 players; last marble is worth 6111 points', 54718),
    ('30 players; last marble is worth 5807 points', 37305),
]

@dataclass
class MarbleGame:
    num_players: int
    last_marble: int
    player = 0
    score_dict: dict[int, int] = field(init=False)
    marble_list: deque[int] = field(init=False)
    marble_bag: itertools.count = field(init=False)
    
    def __post_init__(self):
        self.marble_list = deque([0])
        self.marble_bag = itertools.count(1)
        self.score_dict = defaultdict(int)

    @property
    def size(self) -> int:
        return len(self.marble_list)

    def print(self) -> None:
        output = ''
        for num in self.marble_list:
            output += ' ' + str(num) + ' '
        print(output)

    def simulate_game(self):
        while True:
            next_marble = next(self.marble_bag)

            if next_marble > self.last_marble:
                return max(v for v in self.score_dict.values())

            if next_marble % 23 == 0:
                self.marble_list.rotate(7)
                removed_marble = self.marble_list.popleft()
                self.score_dict[self.player] += next_marble
                self.score_dict[self.player] += removed_marble               

            else:
                self.marble_list.rotate(-2)
                self.marble_list.appendleft(next_marble)

            self.player = (self.player + 1) % self.num_players
            
def parse_data(data: str) -> MarbleGame:
    parts = data.split(' ')
    num_players = int(parts[0])
    last_marble = int(parts[6])
    return MarbleGame(num_players, last_marble)

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        data, answer = example
        print(f"Test #{i}: {part_one(data) == answer}",
              f"({part_one(data)})")

def part_one(data: str):
    game = parse_data(data)
    return game.simulate_game()

def part_two(data: str):
    game = parse_data(data)
    game.last_marble *= 100
    return game.simulate_game()

def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()