'''--- Day 1: Calorie Counting ---'''

from pathlib import Path
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day1_example.txt'
INPUT = DATA_DIR / '2022_day1_input.txt'
                
def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    return line_list


def part_one(filename: Path) -> int:
    line_list = ingest_data(filename)
    num_list = [int(x) if x.isnumeric() else 0 for x in line_list] 
    highest_total = 0
    running_total = 0
    for num in num_list:
        if num == 0:
            running_total = 0
        else:
            running_total += num
            highest_total = running_total if running_total > highest_total else highest_total
    return highest_total
            

def part_two(filename: Path) -> int:
    line_list = ingest_data(filename)
    num_list = [int(x) if x.isnumeric() else 0 for x in line_list] 
    all_totals = []
    running_total = 0
    for num in num_list:
        if num == 0:
            all_totals.append(running_total)
            running_total = 0
        else:
            running_total += num
    all_totals.append(running_total)

    all_totals_sorted = sorted(all_totals, reverse=True)
    print(all_totals_sorted)
    answer = sum(all_totals_sorted[:3])
    return answer


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # should be 2400
    print(f"Part One (input):  {part_one(INPUT)}") # 
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # should be 45000
    print(f"Part Two (input):  {part_two(INPUT)}") # 

if __name__ == '__main__':
    main()