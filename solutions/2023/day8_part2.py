'''--- Day 8: Haunted Wasteland ---'''

from pprint import pprint
from datetime import datetime
from dataclasses import dataclass, field
import math

@dataclass
class Ghost():
    start: str
    maps_dict: dict
    instructions_str: str

    def __post_init__():
        pass

    
with open('./inputs/day8.txt') as file:
    line_list = file.read().split(sep='\n')
instructions_str = line_list.pop(0)
maps_dict = {row[0:3]: (row[7:10], row[12:15]) for row in line_list[1:]}




def find_node_ending_in_Z(starting_point: str) -> tuple:
    total = 0
    next_location = starting_point
    while True:
        for dir in instructions_str:
            total += 1
            current_location = maps_dict[next_location]
            if dir == 'L':
                next_location = current_location[0]
            else:
                next_location = current_location[1]
                
            if next_location[2] == 'Z':
                print(f"\nPart Two:  Went from {starting_point} to {next_location} in {total} steps!")
                return (starting_point, next_location, total)




def part_two():
    list_a = [x for x in maps_dict.keys() if x[2] == 'A']

    a_to_z_list = []
    for starting_point in list_a:
        a_to_z_list.append(find_node_ending_in_Z(starting_point))
    print(f"\nTuple List:  {a_to_z_list}")
  
    print(f"\nLeast Common Multiple (i.e., Part Two Answer):  {math.lcm(*[x[2] for x in a_to_z_list])}")  # correct answer is 22103062509257


def show_info():
    list_a = [x for x in maps_dict.keys() if x[2] == 'A']

    line_list_sorted = sorted(line_list[1:], key=lambda x: x[2])
    final_letter_set = sorted(list(set([x[2] for x in line_list[1:]])))  # 20: ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Z']

    group_list = []
    for letter in final_letter_set:
        # group_list.append(sorted([x for x in line_list[1:] if x[2] == letter], key=lambda x: (x[2], x[0], x[1])))
        group_list.append([x for x in line_list[1:] if x[2] == letter])

    part_two_maps_dict = {x[0][2]: x for x in group_list}
    for (key, value) in part_two_maps_dict.items():
        print(f"{key}:  {len(value)}")
    pprint(part_two_maps_dict)
    

def main():
    part_one()
    part_two()













def part_one() -> int:
    with open('./inputs/day8.txt') as file:
        line_list = file.read().split(sep='\n')
    instructions_str = line_list.pop(0)
    maps_dict = {row[0:3]: (row[7:10], row[12:15]) for row in line_list[1:]}
    
    total = 0
    next_location = 'AAA'
    while True:
        for dir in instructions_str:
            total += 1
            current_location = maps_dict[next_location]
            if dir == 'L':
                next_location = current_location[0]
            else:
                next_location = current_location[1]
                
            if next_location == 'ZZZ':
                print(f"\nPart One:  Found ZZZ in {total} steps!")
                return total






if __name__ == '__main__':
    main()







    # list_a = [x for x in maps_dict.keys() if x[2] == 'A']

    # line_list_sorted = sorted(line_list[1:], key=lambda x: x[2])
    # final_letter_set = sorted(list(set([x[2] for x in line_list[1:]])))  # 20: ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Z']

    # group_list = []
    # for letter in final_letter_set:
    #     # group_list.append(sorted([x for x in line_list[1:] if x[2] == letter], key=lambda x: (x[2], x[0], x[1])))
    #     group_list.append([x for x in line_list[1:] if x[2] == letter])

    # part_two_maps_dict = {x[0][2]: x for x in group_list}
    # for (key, value) in part_two_maps_dict.items():
    #     print(f"{key}:  {len(value)}")
    # pprint(part_two_maps_dict)













# def part_two() -> int:
#     list_a = [x for x in maps_dict.keys() if x[2] == 'A']
#     list_z = [x for x in maps_dict.keys() if x[2] == 'Z']
#     # GROUP_SIZE = len(list_a)

#     total = 0
#     starting_point_list = [starting_point for (starting_point, options) in maps_dict.items() if starting_point[2] == 'A']
#     options_list = [options for (starting_point, options) in maps_dict.items() if starting_point[2] == 'A']
#     REPORTING_CHUNK_SIZE = 1_000_000
#     while True:
#         for dir in instructions_str:
#             total += 1
#             if total == 1 or total % REPORTING_CHUNK_SIZE == 0:
#                 print(f"{datetime.now().strftime('%-I:%M:%S %p')}:  Trying {starting_point_list} at Step #{total:,}...")
#             new_starting_point_list = []
#             for starting_point in starting_point_list:
#                 options = maps_dict[starting_point]
#                 if dir == 'L':
#                     starting_point = options[0]
#                 else:
#                     starting_point = options[1]
#                 new_starting_point_list.append(starting_point)
#             last_letter_set = set([x[2] for x in new_starting_point_list])
#             if len(last_letter_set) == 1 and 'Z' in last_letter_set:
#                 print(f"\nPart Two:  Found ZZZ in {total} steps!")
#                 return total
#         starting_point_list = new_starting_point_list



        # line_list_sorted = sorted(line_list[1:], key=lambda x: x[2])
    # final_letter_set = sorted(list(set([x[2] for x in line_list[1:]])))  # 20: ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Z']

    # group_list = []
    # for letter in final_letter_set:
    #     # group_list.append(sorted([x for x in line_list[1:] if x[2] == letter], key=lambda x: (x[2], x[0], x[1])))
    #     group_list.append([x for x in line_list[1:] if x[2] == letter])

    # part_two_maps_dict = {x[0][2]: x for x in group_list}
    # for (key, value) in part_two_maps_dict.items():
    #     print(f"{key}:  {len(value)}")
    # pprint(part_two_maps_dict)