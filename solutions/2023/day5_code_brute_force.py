'''--- Day 5: If You Give A Seed A Fertilizer ---'''

from dataclasses import dataclass, field
from datetime import datetime
from pprint import pprint

from day5_data_ingestion import (process_maps, process_seeds,
                                 process_test_maps, process_test_seeds)


@dataclass
class MapRow():
    destination_range_start: int = field(repr=False)
    source_range_start: int = field(repr=False)
    range_length: int = field(repr=False)
    destination_range: range = field(init=False)
    source_range: range = field(init=False)
    destination_range_tuple: (int, int) = field(init=False)
    source_range_tuple: (int, int) = field(init=False)

    def __post_init__(self) -> None:
        self.destination_range = self.calculate_destination_range()
        self.source_range = self.calculate_source_range()
        self.destination_range_tuple = self.calculate_destination_range_tuple()
        self.source_range_tuple = self.calculate_source_range_tuple()
        
    def calculate_destination_range(self) -> range:
        destination_range_end = self.destination_range_start + self.range_length
        return range(self.destination_range_start, destination_range_end)

    def calculate_source_range(self) -> range:
        source_range_end = self.source_range_start - 1 + self.range_length
        return range(self.source_range_start, source_range_end)

    def calculate_destination_range_tuple(self) -> (int, int):
        destination_range_end = self.destination_range_start - 1 + self.range_length
        return (self.destination_range_start, destination_range_end)

    def calculate_source_range_tuple(self) -> (int, int):
        source_range_end = self.source_range_start - 1 + self.range_length
        return (self.source_range_start, source_range_end)

    
@dataclass
class Map():
    source_type: str
    destination_type: str
    rows: list[MapRow] = field(repr=False)
    range_dict_list: list[dict] = field(init=False, repr=False)
    source_range_list: list[range] = field(init=False, repr=False)
    destination_range_list: list[range] = field(init=False)#, repr=False)
    full_source_range: range = field(init=False, repr=False)
    full_destination_range: range = field(init=False, repr=False)

    def __post_init__(self) -> None:
        # print(f"Rows:  {self.rows}")
        self.range_dict_list = self.construct_range_dict_list()
        self.source_range_list = self.construct_sorted_source_range()
        self.destination_range_list = self.construct_sorted_destination_range()
        self.full_source_range = self.construct_full_source_range()
        self.full_destination_range = self.construct_full_destination_range()

    def construct_full_source_range(self) -> range:
        sorted_source_start_list = sorted(x.start for x in self.source_range_list)
        sorted_source_end_list = sorted(x.stop for x in self.source_range_list)
        return range(sorted_source_start_list[0], sorted_source_end_list[-1])

    def construct_full_destination_range(self) -> range:
        # print(f"Destination range List:  {self.destination_range_list}")
        sorted_destination_start_list = sorted(x.start for x in self.destination_range_list)
        sorted_destination_end_list = sorted(x.stop for x in self.destination_range_list)
        # print(f"Full range: {range(sorted_destination_start_list[0]pr, sorted_destination_end_list[-1])}")
        return range(sorted_destination_start_list[0], sorted_destination_end_list[-1])

    def construct_sorted_source_range(self) -> list[range]:
        source_range_list = [x.source_range for x in self.rows]
        source_range_list = sorted(source_range_list, key=lambda x: x.start)
        return source_range_list

    def construct_sorted_destination_range(self) -> list[range]:
        destination_range_list = [x.destination_range for x in self.rows]
        # print(f"\nDestination Range list pre-sorted:  {destination_range_list}")
        destination_range_list = sorted(destination_range_list, key=lambda x: x.start)
        # print(f"Destination Range list post-sorted:  {destination_range_list}")
        return destination_range_list
            
    def construct_range_dict_list(self) -> list[dict]:
        output_list = []
        for row in self.rows:
            output_list.append({'source_range': row.source_range_tuple, 'destination_range': row.destination_range_tuple})
        return output_list
        

@dataclass
class Seed():
    seed_num: int
    maps_list: list[Map] = field(repr=False)

    def find_location_num(self) -> int:
        num_to_test = self.seed_num
        maps_dict = {map.source_type: map for map in self.maps_list} 
        for source_type in ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity']:
            current_map = maps_dict[source_type]
            for range_dict in current_map.range_dict_list:
                if num_to_test in range(range_dict['source_range'][0], range_dict['source_range'][1]+1):
                    num_to_test = range_dict['destination_range'][0] + (num_to_test - range_dict['source_range'][0])
                    break
        return num_to_test

    # def find_location_num_part_two(self)

    #     num_to_test = self.seed_num
    #     maps_dict = {map.source_type: map for map in self.maps_list} 
    #     for source_type in ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity']:
    #         current_map = maps_dict[source_type]
    #         for i, source_range in enumerate(current_map.source_range_list):
    #             if num_to_test in source_range:
    #                 num_to_test = current_map.destination_range_list[i].start + (num_to_test - source_range.start)

            
            # for range_dict in current_map.range_dict_list:
            #     if num_to_test in range(range_dict['source_range'].start, range_dict['source_range'].stop+1):
            #         num_to_test = range_dict['destination_range'].start + (num_to_test - range_dict['source_range'].stop)
            #         break
        return num_to_test

    def range_test(self, test_range: range) -> bool:
        return self.seed_num in test_range

    
@dataclass
class SeedGroup():
    seed_range_start: int = field(repr=False)
    seed_range_length: int = field(repr=False)
    maps_list: list[Map] = field(repr=False)
    seed_range_end: int = field(init=False, repr=False)
    seed_range: range = field(init=False)
    seed_list: list[Seed] = field(init=False, repr=False)
    
    def __post_init__(self) -> None:
        self.seed_range_end = self.seed_range_start + self.seed_range_length
        self.seed_range = range(self.seed_range_start, self.seed_range_end)
        
    def create_seeds_in_seed_range(self, seed_range: range) -> None:
        return [Seed(x, self.maps_list) for x in seed_range]
    
    def create_subranges(self, num_subranges:int = 50) -> list[range]:
        # chunk_size = self.seed_range_length // 10
        # num_subranges = ((self.seed_range_length // chunk_size) + 1) if ((self.seed_range_length % chunk_size) != 0) else (self.seed_range_length // chunk_size)
        # return [range(chunk_size*n, min(self.seed_range_length, chunk_size*(n+1))) for n in range(num_subranges)]

        chunk_size = (self.seed_range_length // num_subranges) + (self.seed_range_length % num_subranges)
        return [range(chunk_size*n, min(self.seed_range_length, chunk_size*(n+1))) for n in range(num_subranges)]
        
    def find_lowest_location_num(self) -> int:
        for range in self.create_subranges():
            seeds_list = self.create_seeds_in_seed_range(range)
            print(f"Lowest Location Num in {range}:  {min([seed.find_location_num() for seed in seeds_list])}")
        
        # return self.create_subranges()


def part_two():
    # raw_seeds_list = process_test_seeds()
    # raw_maps_list = process_test_maps()
    raw_seeds_list = process_seeds()
    raw_maps_list = process_maps()
    maps_list = create_map_objects(raw_maps_list)
    seed_groups = create_seed_groups(raw_seeds_list, maps_list)

    # print_sorted_seed_groups(seed_groups)
    # print_sorted_maps(maps_list)

    # full_location_range = create_full_location_range(maps_list[-1])
    # full_seed_range = create_full_seed_range(seed_groups)
    # part_two_answer = find_seed_for_lowest_location_num(full_location_range, full_seed_range, maps_list)
    

    part_two_answer = find_answer_for_part_two_brute_force(raw_seeds_list, create_map_objects(raw_maps_list))
    
    print(f"\nPART #2 ANSWER:  {part_two_answer}")



    

def find_seed_for_lowest_location_num(full_location_range: range, full_seed_range: range, maps_list: list[Map]):
    print(f"Full seed range:  {full_seed_range}")
    print(f"Full location range:  {full_location_range}")
    reporting_chunk_size = 1
    for i, location_num in enumerate(full_location_range):
        for seed_num in full_seed_range:
            test_seed = Seed(seed_num, maps_list)
            if test_seed.find_location_num() == location_num:
                print(f"Found seed with lowest location!  Seed #{test_seed.seed_num} returns Location #{location_num} ")
                return location_num
            if (test_seed.seed_num % reporting_chunk_size == 0):
                print(f"Checked Seed #{test_seed.seed_num:,} for Location #{location_num}.  Still looking...")

def create_full_location_range(humidity_to_location_map: Map) -> list[range]:
    print(f"Humidity-to_Location Destination Range:  {humidity_to_location_map.full_destination_range}")
    return humidity_to_location_map.full_destination_range

def create_full_seed_range(seed_groups_list: list[SeedGroup]) -> None:
    seed_group_range_list = [x.seed_range for x in seed_groups_list]
    seed_group_range_list = sorted(seed_group_range_list, key=lambda x: x.start)

    return range(seed_group_range_list[0].start, seed_group_range_list[-1].stop)




def create_seed_groups(raw_seeds_list: list[int], maps_list: list[Map]) -> list[SeedGroup]:
    range_start_nums = [n for i, n in enumerate(raw_seeds_list) if (i % 2 == 0)]
    range_length_nums = [n for i, n in enumerate(raw_seeds_list) if (i % 2 != 0)]
    seed_group_list = [SeedGroup(range_start_nums[i], range_length_nums[i], maps_list) for i, x in enumerate(range_start_nums)]
    print(f"\n# of Seed Groups in Part 2:  {len(seed_group_list)}")
    return seed_group_list


def print_sorted_seed_groups(seed_groups_list: list[SeedGroup]) -> None:
    seed_group_range_list = [x.seed_range for x in seed_groups_list]
    seed_group_range_list = sorted(seed_group_range_list, key=lambda x: x.start)

    for i, seed_group_range in enumerate(seed_group_range_list):
        print(f"Seed Group #{i+1}:  {seed_group_range.start:,} to {seed_group_range.stop:,}")


def print_sorted_maps(maps_list: list[Map]) -> None:
    for map_num, map in enumerate(maps_list):
        map_range_list = [x for x in map.source_range_list]
        map_range_list = sorted(map_range_list, key=lambda x: x.start)

        for i, map_range in enumerate(map_range_list):
            print(f"Map #{map_num+1}, Range #{i+1}:  {map_range.start:,} to {map_range.stop:,}")

    












def find_answer_for_part_two_brute_force(raw_seeds_list: list[int], maps_list: list[Map]) -> int:
    range_start_nums = [n for i, n in enumerate(raw_seeds_list) if (i % 2 == 0)]
    range_length_nums = [n for i, n in enumerate(raw_seeds_list) if (i % 2 != 0)]
    seed_num_pairs = [(range_start_nums[i], range_length_nums[i]) for i, x in enumerate(range_start_nums)]
    
    # Find total number of seeds and print to console
    total_seeds_num = 0
    for i, pair in enumerate(seed_num_pairs):
        total_seeds_num += len(range(pair[0], pair[0]+pair[1]))
        print(f"Seed Group #{i+1}:  {len(range(pair[0], pair[0]+pair[1])):,}")
    print(f"Total Seeds:    {total_seeds_num:,}")

    # Compare each new seed to the lowest location number found so far, and only keep the lowest. 
    lowest_location_num = 0
    chunk_size = 1000000
    total_progress = 0
    for i, pair in enumerate(seed_num_pairs):
        for n, seed_num in enumerate(range(pair[0], pair[0]+pair[1])):
            seed = Seed(seed_num, maps_list)
            seed_location_num = seed.find_location_num()
            if i == 0 and n == 0:
                lowest_location_num = seed_location_num
            else:
                lowest_location_num = min(lowest_location_num, seed_location_num)
            if (n % chunk_size == 0):
                print(f"{datetime.now().strftime('%I:%M:%S %p')}: Processing Seed {total_progress+1:,} of {total_seeds_num:,} ({(((total_progress)/total_seeds_num)*100):.2f}%).",
                        f"Location #:  {seed_location_num}.  Current lowest location #:  {lowest_location_num}")
            total_progress += 1
    return lowest_location_num

def part_one():
    maps_list = create_map_objects(process_maps())
    seeds_list = [Seed(x, maps_list) for x in process_seeds()]
  
    lowest_location_num = min([seed.find_location_num() for seed in seeds_list])
    print(f"PART #1 ANSWER:  {lowest_location_num}")
    

def create_map_objects(map_coordinate_lists: list[list[list]]) -> list[Map]:
    output_list = []
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
    

def main():
    # part_one()
    part_two()


if __name__ == '__main__':
    main()

    