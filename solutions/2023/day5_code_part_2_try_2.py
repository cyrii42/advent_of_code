'''--- Day 5: If You Give A Seed A Fertilizer ---'''
import itertools
from dataclasses import dataclass, field
from pprint import pprint

from day5_data_ingestion import (process_maps, process_seeds,
                                 process_test_maps, process_test_seeds)


@dataclass
class MapRow():
    destination_range_start: int = field(repr=False)
    source_range_start: int = field(repr=False)
    range_length: int = field(repr=False)
    source_range: range = field(init=False)
    destination_range: range = field(init=False)
    range_tuple: tuple[range, range] = field(init=False)

    def __post_init__(self) -> None:
        self.destination_range = self.calculate_destination_range()
        self.source_range = self.calculate_source_range()
        self.range_tuple = (self.source_range, self.destination_range)
        
    def calculate_source_range(self) -> range:
        source_range_end = self.source_range_start + self.range_length
        return range(self.source_range_start, source_range_end)

    def calculate_destination_range(self) -> range:
        destination_range_end = self.destination_range_start + self.range_length
        return range(self.destination_range_start, destination_range_end)
    
@dataclass
class Map():
    source_type: str
    destination_type: str
    rows: list[MapRow] = field(repr=False)
    rows_sorted: list[MapRow] = field(init=False, repr=False)
    source_range_list: list[range] = field(init=False, repr=False)
    source_to_range_length_dict: dict = field(init=False)

    def __post_init__(self) -> None:
        self.rows_sorted = sorted([row for row in self.rows], key=lambda x: x.source_range_start)
        self.source_range_list = [row.source_range for row in self.rows_sorted]
        self.source_to_range_length_dict = {row.source_range_start: row.range_length for row in self.rows_sorted}


@dataclass
class Seed():
    seed_num: int


@dataclass
class SeedGroup():
    seed_range_start: int = field(repr=False)
    seed_range_length: int = field(repr=False)
    seed_range_end: int = field(init=False, repr=False)
    seed_range: range = field(init=False)
    
    def __post_init__(self) -> None:
        self.seed_range_end = self.seed_range_start + self.seed_range_length
        self.seed_range = range(self.seed_range_start, (self.seed_range_end))


def main():
    # raw_seeds_list = process_test_seeds()
    # raw_maps_list = process_test_maps()
    raw_seeds_list = process_seeds()
    raw_maps_list = process_maps()
    
    maps_list = create_map_objects(raw_maps_list)
    seed_group_list = create_seed_groups(raw_seeds_list)

    for map in maps_list:
        print(f"\n{map.source_type} to {map.destination_type}:  {map.source_to_range_length_dict}")
        
    # print(f"\n# of Seed Groups:  {len(seed_group_list)}")
    # for n, seed_group in enumerate(seed_group_list):
    #     print(f"Seed Group #{n+1}:  {seed_group.seed_range} ({len(seed_group.seed_range):,} seeds)")      

   

    # for each seed group, determine the seed-to-soil source range in which the starting and ending seed falls
    seed_to_soil_map = maps_list[0]
    for seed_group_num, seed_group in enumerate(seed_group_list):
        seed_group_start = seed_group.seed_range_start
        seed_group_start_range_num = 0
        seed_group_end = seed_group.seed_range_end
        seed_group_end_range_num = 0

        for i, source_range in enumerate(seed_to_soil_map.source_range_list):
            if seed_group_start in source_range:
                seed_group_start_range_num = i
                break

        for i, source_range in enumerate(seed_to_soil_map.source_range_list):
            if seed_group_end in source_range:
                seed_group_end_range_num = i
                break

        print(f"Seed Group #{seed_group_num+1}:  Starts in Seed-to-Soil Range #{seed_group_start_range_num}, ends in Seed-to-Soil Range #{seed_group_end_range_num} (spanning {seed_group_end_range_num - seed_group_start_range_num} ranges)")

    # NEXT STEPS:  
    #   - for each seed group, set an instance variable containing the # of seed-to-soil ranges spanned
    #   - for seed groups that span 2 or more ranges, figure out how to determine the points where the range changes happen
    #   - then, for each seed, you can just take the seed-to-soil range in which the seed falls and add the range length



    part_two_answer = None
    print(f"\nPART #2 ANSWER:  {part_two_answer}")  # correct answer is 41222968

    
    

def create_seed_groups(raw_seeds_list: list[int]) -> list[SeedGroup]:
    range_start_nums = [n for i, n in enumerate(raw_seeds_list) if (i % 2 == 0)]
    range_length_nums = [n for i, n in enumerate(raw_seeds_list) if (i % 2 != 0)]
    seed_group_list = [SeedGroup(range_start_nums[i], range_length_nums[i]) for i, x in enumerate(range_start_nums)]
    return sorted(seed_group_list, key=lambda x: x.seed_range_start)



def create_map_objects(map_coordinate_lists: list[list[str|int]]) -> list[Map]:
    output_list: list[Map] = []
    for map in map_coordinate_lists:
        output_list.append(Map(map[0], map[1], [MapRow(x[0], x[1], x[2]) for x in map[2]]))

    seed_to_soil = [x for x in output_list if x.source_type == 'seed']
    soil_to_fertilizer = [x for x in output_list if x.source_type == 'soil']
    fertilizer_to_water = [x for x in output_list if x.source_type == 'fertilizer']
    water_to_light = [x for x in output_list if x.source_type == 'water']
    light_to_temperature = [x for x in output_list if x.source_type == 'light']
    temperature_to_humidity = [x for x in output_list if x.source_type == 'temperature']
    humidity_to_location = [x for x in output_list if x.source_type == 'humidity']

    return [seed_to_soil + soil_to_fertilizer + fertilizer_to_water + water_to_light
            + light_to_temperature + temperature_to_humidity + humidity_to_location][0]
    




if __name__ == '__main__':
    main()

    