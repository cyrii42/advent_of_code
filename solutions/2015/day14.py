from dataclasses import dataclass, field
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLE = ('Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.\n'+
           'Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.')
INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

@dataclass
class Reindeer:
    name: str
    speed: int
    duration: int
    rest: int
    position: int = 0
    position_list: list[int] = field(default_factory=list)
    points: int = 0

    def __post_init__(self):
        self.cycle_time = self.duration + self.rest

    def get_position_from_race_time(self, secs: int) -> int:
        full_cycles = secs // self.cycle_time
        remainder_secs = min(self.duration, (secs % self.cycle_time))
        return (full_cycles * (self.speed * self.duration)) + (remainder_secs * self.speed)

    def fly_part_one(self, secs: int) -> int:
        self.position = self.get_position_from_race_time(secs)
        return self.position

    def fly_part_two(self, secs: int) -> None:
        self.position_list = [self.get_position_from_race_time(time) for time in range(1, secs+1)]

    def add_point(self) -> None:
        self.points += 1
        

@dataclass
class ReindeerSet:
    members: list[Reindeer]

    def get_reindeer_by_position_at_time(self, position: int, time: int) -> list[Reindeer]:
        return [reindeer for reindeer in self.members if reindeer.position_list[time] == position]

    def run_race_part_one(self, secs: int) -> int:
        return max(reindeer.fly_part_one(secs) for reindeer in self.members)

    def run_race_part_two(self, secs: int) -> int:
        # Make every reindeer run the full race and create position lists
        for reindeer in self.members:
            reindeer.fly_part_two(secs)

        # Then go back through everyone's lists and see who was the leader at each second
        for x in range(secs):
            leader_position = max(reindeer.position_list[x] for reindeer in self.members)
            leader_or_co_leaders = self.get_reindeer_by_position_at_time(leader_position, x)
            for reindeer in leader_or_co_leaders:
                reindeer.add_point()
        return max(reindeer.points for reindeer in self.members)
            

def parse_data(data: str):
    line_list = data.splitlines()

    output_list = []
    for line in line_list:
        parts = line.split(' ')
        name = parts[0]
        speed = int(parts[3])
        duration = int(parts[6])
        rest = int(parts[-2])
            
        output_list.append(Reindeer(name, speed, duration, rest))
                
    return ReindeerSet(output_list)
    
def part_one(data: str, secs: int):
    reindeer_set = parse_data(data)
    return reindeer_set.run_race_part_one(secs)

def part_two(data: str, secs: int):
    reindeer_set = parse_data(data)
    return reindeer_set.run_race_part_two(secs)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE, 1000)}")
    print(f"Part One (input):  {part_one(INPUT, 2503)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE, 1000)}")
    print(f"Part Two (input):  {part_two(INPUT, 2503)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()