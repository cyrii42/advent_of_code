from dataclasses import dataclass, field
from pathlib import Path
from alive_progress import alive_bar
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)
TESTS_PART_ONE = [
    ('9', '5158916779'),
    ('5', '0124515891'),
    ('18', '9251071085'),
    ('2018', '5941429882'),
]
TESTS_PART_TWO = [
    ('51589', 9),
    ('01245', 5),
    ('92510', 18),
    ('59414', 2018),
]

START = (3, 7)

@dataclass
class Elf:
    index: int
    score: int

@dataclass
class ElfPair:
    num_recipes: int
    elves: tuple[Elf, Elf] = field(init=False)
    scoreboard: list[int] = field(init=False)

    def __post_init__(self):
        score_0, score_1 = START
        self.elves = (Elf(0, score_0), Elf(1, score_1))
        self.scoreboard = [*START]

    def create_new_recipes(self) -> None:
        total_score = sum(elf.score for elf in self.elves)
        new_scores = str(total_score)
        assert 0 < len(new_scores) < 3
        for digit in new_scores:
            self.scoreboard.append(int(digit))        
         
    def choose_new_recipes(self) -> None:
        for elf in self.elves:
            num_steps = elf.score + 1
            next_index = (elf.index + num_steps) % len(self.scoreboard)
            next_score = self.scoreboard[next_index]
            elf.index = next_index
            elf.score = next_score

    def execute_next_round(self) -> None:
        self.create_new_recipes()
        self.choose_new_recipes()

    def solve_part_one(self) -> str:
        while len(self.scoreboard) < self.num_recipes + 10:
            self.execute_next_round()

        return ''.join(str(num) for num 
                       in self.scoreboard[self.num_recipes:self.num_recipes+10])

    def solve_part_two(self, input_str: str, check: int = 10_000) -> int:
        with alive_bar() as bar:
            i = 0
            while True:
                self.execute_next_round()
                if i % check == 0:
                    sb_str = ''.join(str(num) for num in self.scoreboard[-check:])
                    if input_str in sb_str:
                        full_sb_str = ''.join(str(num) for num in self.scoreboard)
                        return full_sb_str.index(input_str)
                i += 1
                bar()

def part_one_tests():
    for i, example in enumerate(TESTS_PART_ONE, start=1):
        num_recipes, answer = example
        test_answer = part_one(num_recipes)
        print(f"Test #{i}: {test_answer == answer}",
              f"({test_answer})")

def part_two_tests():
    for i, example in enumerate(TESTS_PART_TWO, start=1):
        num_recipes, answer = example
        test_answer = part_two(num_recipes)
        print(f"Test #{i}: {test_answer == answer}",
              f"({test_answer})")
   
def part_one(data: str):
    elf_pair = ElfPair(int(data))
    return elf_pair.solve_part_one()

def part_two(data: str):
    elf_pair = ElfPair(int(data))
    check = 10_000 if data == INPUT else 1_000
    return elf_pair.solve_part_two(input_str=data, check=check)

def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    part_two_tests()
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()