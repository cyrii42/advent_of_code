import pathlib

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str):
    line_list = data.splitlines()
    return line_list

def decode_messages(msgs: list[str], reverse: bool = True) -> str:
    output_str = ''
    for i in range(len(msgs[0])):
        col_i = ''.join(msg[i] for msg in msgs)
        ltrs = sorted(col_i, key=lambda x: col_i.count(x), 
                      reverse=reverse)
        output_str += ltrs[0]
    return output_str
    
def part_one(data: str):
    msgs = parse_data(data)
    return decode_messages(msgs)
        
def part_two(data: str):
    msgs = parse_data(data)
    return decode_messages(msgs, reverse=False)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()