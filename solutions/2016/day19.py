import bisect
import pathlib

from alive_progress import alive_bar
from rich import print

import advent_of_code as aoc

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)

def run_white_elephant_part_one(num_elves: int, print_info: bool = False) -> int:
    d = {n: 1 for n in range(num_elves)}
    elf = -1
    while True:
        elf = ((elf + 1) % num_elves)
        while not d[elf]:
            if print_info:
                print(f"Elf #{elf+1} has no presents and is skipped.")
            elf = ((elf + 1) % num_elves)
        
        next_elf = ((elf + 1) % num_elves)
        while not d[next_elf]:
            next_elf = ((next_elf + 1) % num_elves)
            
        d[elf] += d[next_elf]
        if print_info:
            print(f"Elf #{elf+1} takes Elf #{next_elf+1}'s {d[next_elf]} present(s)",
                  f"(Elf #{elf+1} now has {d[elf]})")
        d[next_elf] = 0

        
        if d[elf] >= num_elves:
            return elf+1

def get_elf_across_circle(elf: int, d: dict[int, int]) -> int:
    '''
    only two elves:  the other one
    odd-sided polygon:   floor and ceiling of n / 2
    even-sided polygon:  n / 2
    '''
    eligible_elves = sorted(d.keys())
    num_eligible_elves = len(eligible_elves)
    idx = bisect.bisect_left(eligible_elves, elf)
    opposite_idx = (idx + (num_eligible_elves // 2)) % num_eligible_elves
    return eligible_elves[opposite_idx]     

def run_white_elephant_part_two(num_elves: int, print_info: bool = False) -> int:
    ''' Realizing the folly of their present-exchange rules, the Elves agree to 
    instead steal presents from the Elf directly across the circle. If two Elves 
    are across the circle, the one on the left (from the perspective of the stealer)
    is stolen from. The other rules remain unchanged: Elves with no presents are 
    removed from the circle entirely, and the other elves move in slightly to keep 
    the circle evenly spaced. '''

    d = {n: 1 for n in range(num_elves)}
    elf = -1

    with alive_bar() as bar:
        while True:
            elf = ((elf + 1) % num_elves)
            while not d.get(elf):
                elf = ((elf + 1) % num_elves)
            
            opposite_elf = get_elf_across_circle(elf, d)
                
            d[elf] += d[opposite_elf]
            if print_info:
                print(f"Elf #{elf+1} takes Elf #{opposite_elf+1}'s {d[opposite_elf]} present(s)",
                    f"(Elf #{elf+1} now has {d[elf]})")
            del d[opposite_elf]

            if d[elf] >= num_elves:
                return elf+1
            
            bar()
    

def test_part_one():
    print(f"TEST (5): {part_one('5') == 3} ({part_one('5', print_info=True)})")

def part_one(data: str, print_info: bool = False):
    num_elves = int(data)
    return run_white_elephant_part_one(num_elves, print_info=print_info)
    
def test_part_two():
    print(f"TEST (5): {part_two('5') == 2} ({part_two('5', print_info=True)})")

def part_two(data: str, print_info: bool = False):
    num_elves = int(data)
    return run_white_elephant_part_two(num_elves, print_info=print_info)



def main():
    # test_part_one()
    # print(f"Part One (input):  {part_one(INPUT, print_info=False)}")
    # test_part_two()
    print(f"Part Two (input):  {part_two(INPUT, print_info=False)}")

    random_tests()

def random_tests():
    asdf = [x for x in range(50)]
    print(bisect.bisect_left(asdf, 20))
    print(asdf.index(20))

       
if __name__ == '__main__':
    main()