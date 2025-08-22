'''--- Day 4: Ceres Search ---'''

import re
import pandas as pd
import numpy as np
from pathlib import Path
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2024_day4_example.txt'
INPUT = DATA_DIR / '2024_day4_input.txt'

PART_2_SQUARE_HEIGHT = 3
PART_2_SQUARE_WIDTH = 3

REGEX_PART_ONE = r'(?=(?P<forward>XMAS)|(?P<backward>SAMX))'
REGEX_PART_TWO = r'M.S.A.M.S|S.M.A.S.M|M.M.A.S.S|S.S.A.M.M'

def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        
    return line_list

def get_vertical_lines(horizontal_line_list: list[str]) -> list[str]:
    num_columns = len(horizontal_line_list[0])

    output_list = []
    for i in range(num_columns):
        output_list.append(''.join(line[i] for line in horizontal_line_list))

    return output_list

def get_diagonal_lines(horizontal_line_list: list[str], vertical_line_list: list[str]) -> list[str]:
    num_columns = len(horizontal_line_list)
    num_rows = len(vertical_line_list)

    rows = [list(x) for x in horizontal_line_list]    

    output_list = []
    
    df = pd.DataFrame(rows)
    for x in range(0-num_rows, num_columns-1):
        output_list.append(''.join(x for x in np.diag(df, k=x)))

    df2 = df.iloc[::-1].reset_index(drop=True)
    for x in range(0-num_rows, num_columns-1):
        output_list.append(''.join(x for x in np.diag(df2, k=x)))

    return output_list

def regex_part_one(input: str) -> int:
    pattern = re.compile(REGEX_PART_ONE)
    matches = pattern.finditer(input)

    total = 0
    for m in matches:
        if m.group(1) is not None or m.group(2) is not None:
            total += 1

    return total

def part_one(filename: Path) -> int:   
    horizontal_line_list = ingest_data(filename)
    horizontal_total = sum(regex_part_one(line) for line in horizontal_line_list)

    vertical_line_list = get_vertical_lines(horizontal_line_list)
    vertical_total = sum(regex_part_one(line) for line in vertical_line_list)

    diagonal_line_list = get_diagonal_lines(horizontal_line_list, vertical_line_list)
    diagonal_total = sum(regex_part_one(line) for line in diagonal_line_list)

    return horizontal_total + vertical_total + diagonal_total

def regex_part_two(input: str) -> int:
    pattern = re.compile(REGEX_PART_TWO)
    matches = pattern.findall(input)

    return 1 if matches else 0  

def get_squares(horizontal_line_list: list[str], vertical_line_list: list[str]) -> list[str]:
    num_rows = len(horizontal_line_list)
    num_columns = len(vertical_line_list)

    output_list = []
    for row_num in range(num_rows - (PART_2_SQUARE_WIDTH - 1)):
        for col_num in range(num_columns - (PART_2_SQUARE_HEIGHT -1)):
            sq1 = (horizontal_line_list[row_num])[col_num] + (horizontal_line_list[row_num])[col_num+1] + (horizontal_line_list[row_num])[col_num+2]
            sq2 = (horizontal_line_list[row_num+1])[col_num] + (horizontal_line_list[row_num+1])[col_num+1] + (horizontal_line_list[row_num+1])[col_num+2]
            sq3 = (horizontal_line_list[row_num+2])[col_num] + (horizontal_line_list[row_num+2])[col_num+1] + (horizontal_line_list[row_num+2])[col_num+2]
            output_list.append(sq1 + sq2 + sq3)
    return output_list

def part_two(filename: Path) -> int:
    horizontal_line_list = ingest_data(filename)
    vertical_line_list = get_vertical_lines(horizontal_line_list)

    square_list = get_squares(horizontal_line_list, vertical_line_list)
    answer = sum(regex_part_two(square) for square in square_list)

    return answer

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")
    
if __name__ == '__main__':
    main()