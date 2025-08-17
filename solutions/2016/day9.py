import pathlib
import re

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)

PART_ONE_TESTS = [
    ('ADVENT', 'ADVENT'),
    ('A(1x5)BC', 'ABBBBBC'),
    ('(3x3)XYZ', 'XYZXYZXYZ'),
    ('A(2x2)BCD(2x2)EFG', 'ABCBCDEFEFG'),
    ('(6x1)(1x3)A', '(1x3)A'),
    ('X(8x2)(3x3)ABCY', 'X(3x3)ABC(3x3)ABCY')
]

MARKER_PATTERN = r'\(\d+x\d+\)'

def parse_marker(marker: str) -> tuple[int, int]:
    num_chars, num_repeats = marker.removeprefix('(').removesuffix(')').split('x')
    return (int(num_chars), int(num_repeats))
    
def decompress_v1(seq: str) -> str:
    pattern = re.compile(MARKER_PATTERN)
    output_str = ''
    i = 0
    while i < len(seq):
        m = pattern.match(seq[i:])
        if m:
            marker = m.group(0)
            num_chars, num_repeats = parse_marker(marker)
            
            start = i + m.end(0)
            end = start + num_chars
            chars_to_append = seq[start:end]

            for _ in range(num_repeats):
                output_str += chars_to_append
            i = end
        else:
            output_str += seq[i]
            i += 1
    return output_str

def part_one(data: str):
    decompressed_data = decompress_v1(data)
    return len(decompressed_data)

def decompress_v2(seq: str) -> int:
    pattern = re.compile(MARKER_PATTERN)
    count = 0
    i = 0
    while i < len(seq):
        m = pattern.match(seq[i:])
        if m:
            marker = m.group(0)
            num_chars, num_repeats = parse_marker(marker)
            
            start = i + m.end(0)
            end = start + num_chars
            chars_to_append = seq[start:end]

            if pattern.search(chars_to_append):
                count += decompress_v2(chars_to_append) * num_repeats
            else:
                count += num_chars * num_repeats
            i = end
        else:
            count += 1
            i += 1 
    return count

def part_two(data: str):
    decompressed_len = decompress_v2(data)
    return decompressed_len

def part_one_tests():
    for i, test in enumerate(PART_ONE_TESTS, start=1):
        test_start, test_answer = test
        answer = decompress_v1(test_start)
        print(f"Test #{i}: {answer == test_answer and len(answer) == len(test_answer)}")
        print(f"INPUT:     {test_start}")
        print(f"EXPECTED:  {test_answer} ({len(test_answer)} chars)")
        print(f"RESULT:    {answer} ({len(answer)} chars)\n")

def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...
    

       
if __name__ == '__main__':
    main()