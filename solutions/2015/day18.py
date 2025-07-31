from pathlib import Path

import numpy as np
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = '.#.#.#\n...##.\n#....#\n..#...\n#.#..#\n####..'
EXAMPLE_PART_TWO = '##.#.#\n...##.\n#....#\n..#...\n#.#..#\n####.#'
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def parse_data(data: str) -> np.ndarray:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        line = line.replace('#', '1').replace('.', '0')
        output_list.append([int(char) for char in line])
    return np.array(output_list)

def get_neighbors(matrix: np.ndarray, x: int, y: int) -> np.ndarray:
    m = matrix.copy()
    x_start = max(x-1, 0)
    x_end = min(x+2, matrix.shape[1])
    
    y_start = max(y-1, 0)
    y_end = min(y+2, matrix.shape[0])
    
    return m[x_start:x_end, y_start:y_end]

def get_light_state(matrix: np.ndarray, x: int, y: int) -> int:
    m = matrix.copy()
    current_state = m[x, y]
    neighbor_matrix = get_neighbors(m, x, y)
    neighbor_sum = np.sum(neighbor_matrix) - current_state

    if current_state == 1:
        if neighbor_sum == 2 or neighbor_sum == 3:
            return 1
        else:
            return 0
    else:
        if neighbor_sum == 3:
            return 1
        else: 
            return 0

def animate_matrix(matrix: np.ndarray):
    rows, cols = matrix.shape
    m_copy = matrix.copy()
    for row in range(rows):
        for col in range(cols):
            matrix[row, col] = get_light_state(m_copy, row, col)
    return matrix
    

def part_one(data: str, steps: int):
    matrix = parse_data(data)
    for _ in range(steps):
        animate_matrix(matrix)
    return np.sum(matrix)




def get_light_state_part_two(matrix: np.ndarray, x: int, y: int) -> int:
    if ((x == 0 or x == matrix.shape[0]-1) 
        and (y == 0 or y == matrix.shape[1]-1)):
        return 1
    
    m = matrix.copy()
    current_state = m[x, y]
    neighbor_matrix = get_neighbors(m, x, y)
    neighbor_sum = np.sum(neighbor_matrix) - current_state
    
    if current_state == 1:
        if neighbor_sum == 2 or neighbor_sum == 3:
            return 1
        else:
            return 0
    else:
        if neighbor_sum == 3:
            return 1
        else: 
            return 0

def animate_matrix_part_two(matrix: np.ndarray):
    rows, cols = matrix.shape
    m_copy = matrix.copy()
    for row in range(rows):
        for col in range(cols):
            matrix[row, col] = get_light_state_part_two(m_copy, row, col)
    return matrix

def part_two(data: str, steps: int):
    matrix = parse_data(data)
    for _ in range(steps):
        animate_matrix_part_two(matrix)
    return np.sum(matrix)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE, steps=4)}")
    print(f"Part One (input):  {part_one(INPUT, steps=100)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO, steps=5)}")
    print(f"Part Two (input):  {part_two(INPUT, steps=100)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()