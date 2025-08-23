import pathlib
from dataclasses import dataclass, field
from string import ascii_lowercase
from typing import Self

from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = aoc.DATA_DIR / '2016.03_examples.txt'
INPUT = aoc.DATA_DIR / '2016.03_input.txt'

@dataclass
class RoomInfo:
    name: str
    id: int
    checksum: str
    is_real: bool = field(init=False)
    real_name: str = field(init=False)

    def __post_init__(self):
        self.is_real = self.confirm_checksum()
        self.real_name = self.decrypt_name()

    def confirm_checksum(self) -> bool:
        ''' A room is real (not a decoy) if the checksum is the five most common
        letters in the encrypted name, in order, with ties broken by alphabetization. '''

        letters = sorted({char for char in self.name if char.isalpha()})
        letters = sorted(letters, key=lambda char: self.name.count(char), reverse=True)
        checksum = ''.join(char for char in letters[0:5])
        return checksum == self.checksum

    @classmethod
    def from_str(cls, line: str) -> Self:
        checksum = line[-6:].strip(']')
        id = int(''.join(char for char in line if char.isdigit()))
        name = ''.join(char for char in line[0:-11])
        return cls(name, id, checksum)

    def decrypt_name(self) -> str:
        output_str = ''
        
        for char in self.name:
            if char == '-':
                output_str += ' '
            else:
                idx = ascii_lowercase.index(char)
                new_idx = (idx + self.id) % 26
                output_str += ascii_lowercase[new_idx]
                
        return output_str  

def parse_data(data_file: pathlib.Path) -> list[RoomInfo]:
    with open(data_file, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    return [RoomInfo.from_str(line) for line in line_list]
    
def part_one(data: pathlib.Path):
    room_list = parse_data(data)
    return sum(room.id for room in room_list if room.is_real)

def part_two(data: pathlib.Path):
    room_list = parse_data(data)
    return next(room.id for room in room_list 
                if room.real_name == 'northpole object storage')

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()