'''--- Day 1: Historian Hysteria ---'''

from pathlib import Path
from advent_of_code.constants import DATA_DIR

def ingest_data(filename: Path) -> list[tuple[int, int]]:
    with open(filename, 'r') as f:
        lines = [line.strip('\n').split() for line in f.readlines()]
        pairs = [(int(line[0]), int(line[1])) for line in lines]
    return pairs

def sort_pairs(pairs: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
    left_nums  = sorted([pair[0] for pair in pairs])
    right_nums = sorted([pair[1] for pair in pairs])

    return (left_nums, right_nums)

def pair_sorted_lists(sorted_num_lists: tuple[list[int], list[int]]) -> list[tuple[int, int]]:
    left_nums = sorted_num_lists[0]
    right_nums = sorted_num_lists[1]
    
    return [(left_num, right_num) for left_num, right_num in zip(left_nums, right_nums)]

def calculate_differences(new_pairs: list[tuple[int, int]]) -> int:
    pair_differences = [abs(pair[0] - pair[1]) for pair in new_pairs]
    return sum(pair_differences)

def part_one():
    pairs = ingest_data(DATA_DIR.joinpath('day1_input.txt'))
    sorted_num_lists = sort_pairs(pairs)
    new_pairs = pair_sorted_lists(sorted_num_lists)
    answer = calculate_differences(new_pairs)
    print(answer)  # 2430334


def calculate_similarity_score(sorted_num_lists: tuple[list[int], list[int]]) -> int:
    left_nums  = sorted_num_lists[0]
    right_nums = sorted_num_lists[1]

    total = 0
    for num in left_nums:
        total += (num * right_nums.count(num))

    return total

    
    

def part_two():
    pairs = ingest_data(DATA_DIR.joinpath('2024_day1_input.txt'))
    sorted_num_lists = sort_pairs(pairs)
    answer = calculate_similarity_score(sorted_num_lists)
    print(answer)

def main():
    part_two()

    

    

if __name__ == '__main__':
    main()