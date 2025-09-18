from pathlib import Path
from typing import Generator

from alive_progress import alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = 'Generator A starts with 65\nGenerator B starts with 8921'
INPUT = aoc.get_input(YEAR, DAY)

FACTOR_A = 16807
FACTOR_B = 48271
MODULO_DIV = 2147483647

def convert_to_binary(value: int, num_bits: int = 32) -> str:
    return f"{bin(value).removeprefix('0b'):0>{num_bits}}"

def pair_generator(a_start: int, 
                   b_start: int
                   ) -> Generator[tuple[str, str]]:
    value_a = a_start
    value_b = b_start

    while True:
        value_a = (value_a * FACTOR_A) % MODULO_DIV
        bin_a = convert_to_binary(value_a)
        value_b = (value_b * FACTOR_B) % MODULO_DIV
        bin_b = convert_to_binary(value_b)
        yield (bin_a, bin_b)

def generator_part_two(start: int, 
                       factor: int,
                       multiple: int
                       ) -> Generator[str]:
    value = start

    while True:
        value = (value * factor) % MODULO_DIV
        if value % multiple == 0:
            yield convert_to_binary(value)
        
def parse_data(data: str) -> tuple[int, int]:
    line_list = data.splitlines()
    a_start = int(line_list[0].split(' ')[-1])
    b_start = int(line_list[1].split(' ')[-1])
    return (a_start, b_start)
    
def part_one(data: str, sample_size: int = 40_000_000):
    a_start, b_start = parse_data(data)
    pair_gen = pair_generator(a_start, b_start)

    num_matches = 0
    for _ in alive_it(range(sample_size)):
        bin_a, bin_b = next(pair_gen)
        if bin_a[16:] == bin_b[16:]:
            num_matches += 1
    return num_matches
    
def part_two(data: str, sample_size: int = 5_000_000):
    a_start, b_start = parse_data(data)
    gen_a = generator_part_two(a_start, FACTOR_A, 4)
    gen_b = generator_part_two(b_start, FACTOR_B, 8)

    num_matches = 0
    for _ in alive_it(range(sample_size)):
        bin_a = next(gen_a)
        bin_b = next(gen_b)
        if bin_a[16:] == bin_b[16:]:
            num_matches += 1
    return num_matches
    
def main():
    print(f"Part One (example):  {part_one(EXAMPLE, sample_size=5)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()