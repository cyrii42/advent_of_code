from pathlib import Path
from typing import Optional

from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '3,4,1,5'
INPUT = aoc.get_input(YEAR, DAY)

STANDARD_LENGTH = 256
SUFFIX_VALUES = [17, 31, 73, 47, 23]

PART_TWO_TESTS = [
    ('', 'a2582a3a0e66e6e86e3812dcb672a272'),
    ('AoC 2017', '33efeb34ea91902bb2f59c9920caa6cd'),
    ('1,2,3', '3efbe78a8d82f29979031a4aa0b16a9d'),
    ('1,2,4', '63960835bcdc130f0b66d7ff4f6a5a8e'),
]

def create_knot_hash(input_lengths: list[int], 
                     start_list: Optional[list[int]] = None,
                     current_position: int = 0,
                     skip_size: int = 0):
    if not start_list:
        start_list = [x for x in range(STANDARD_LENGTH)]
        
    list_length = len(start_list)
    output_list = start_list
    for length in input_lengths:
        if length > 1:   # if the length is 0 or 1, no need to reverse anything
            range_start = current_position
            range_end = (current_position + length) % list_length
            
            if range_end <= range_start:   # if we've wrapped around the list
                nums = list(reversed(output_list[range_start:] + output_list[:range_end]))
                output_list[range_start:] = nums[0:(list_length - range_start)]
                output_list[:range_end] = nums[(list_length - range_start):]
            else:
                nums = reversed(output_list[range_start:range_end])
                output_list[range_start:range_end] = nums
        
        current_position = (current_position + length + skip_size) % list_length
        skip_size += 1
        
    return (output_list, current_position, skip_size)

def create_sparse_hash(input_lengths: list[int]):
    current_position = 0
    skip_size = 0
    num_list = [x for x in range(STANDARD_LENGTH)]
    for _ in range(64):
        num_list, current_position, skip_size = create_knot_hash(input_lengths=input_lengths, 
                                                                 start_list=num_list,
                                                                 current_position=current_position, 
                                                                 skip_size=skip_size)
    return num_list

def create_dense_hash(sparse_hash: list[int]) -> list[int]:
    HASH_LENGTH = 16
    num_elements = len(sparse_hash) // HASH_LENGTH
    output_list = []
    for i in range(num_elements):
        start = num_elements * i
        stop = start + HASH_LENGTH
        hash_num = sparse_hash[start]
        for num in sparse_hash[start+1:stop]:
            hash_num = hash_num ^ num
        output_list.append(hash_num)
    return output_list 

def create_hex_output(dense_hash: list[int]):
    return ''.join(f"{hex(x).removeprefix('0x'):0>2}" for x in dense_hash)

def part_one_test():
    input_lengths = [int(x) for x in EXAMPLE.split(',')]
    knot_hash, _, _ = create_knot_hash(input_lengths, start_list=[x for x in range(5)])
    print(f"Part One (example): {knot_hash[0] * knot_hash[1]}")

def part_two_tests():
    for i, example in enumerate(PART_TWO_TESTS, start=1):
        data, answer = example
        test_answer = part_two(data)
        print(f"Test #{i} ({data}) ({test_answer}):",
              f"{test_answer == answer} (should be {answer})")
    
def part_one(data: str):
    input_lengths = [int(x) for x in data.split(',')]
    knot_hash, _, _ = create_knot_hash(input_lengths)
    return knot_hash[0] * knot_hash[1]

def part_two(data: str):
    input_lengths = [ord(char) for char in data.strip()] + SUFFIX_VALUES
    sparse_hash = create_sparse_hash(input_lengths)
    dense_hash = create_dense_hash(sparse_hash)
    return create_hex_output(dense_hash)

def main():
    part_one_test()
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    part_two_tests()
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()