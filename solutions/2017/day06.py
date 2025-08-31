from copy import deepcopy
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '0\t2\t7\t0'
INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str):
    return [int(x) for x in data.split('\t')]

def reallocate_memory(blocks: list[int]) -> list[int]:
    max_blocks = max(blocks)
    idx = blocks.index(max_blocks)
    blocks[idx] = 0

    i = (idx + 1) % len(blocks)
    while max_blocks > 0:       
        blocks[i] += 1
        max_blocks -= 1
        i = (i + 1) % len(blocks)

    return blocks
    
def part_one(data: str):
    blocks = parse_data(data)
    
    count = 0
    seen = []
    seen.append(deepcopy(blocks))
    while True:
        count +=1
        blocks = reallocate_memory(blocks)
        if blocks in seen:
            return count
        seen.append(deepcopy(blocks))

def part_two(data: str):
    blocks = parse_data(data)
    
    seen_count = 0
    seen = []
    seen.append(deepcopy(blocks))
    state = None
    while True:
        blocks = reallocate_memory(blocks)
        if blocks == state:
            return seen_count
        if blocks in seen and not seen_count:
            state = deepcopy(blocks)
            seen_count += 1
            continue
        seen.append(deepcopy(blocks))
        if seen_count:
            seen_count += 1

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
       
if __name__ == '__main__':
    main()