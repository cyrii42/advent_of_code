'''--- Day 6: Wait For It ---'''
from dataclasses import dataclass, field


TEST_RACES_PART_ONE = [(7, 9), (15, 40), (30, 200)]
INPUT_RACES_PART_ONE = [(40, 233), (82, 1011), (84, 1110), (92, 1487)]
TEST_RACE_PART_TWO = (71530, 940200)
INPUT_RACE_PART_TWO = (40828492, 233101111101487)

@dataclass
class Race():
    total_time: int
    distance_to_beat: int
    ways_to_win: int = field(init=False)

    def __post_init__(self) -> None:
        self.ways_to_win = self.calculate_ways_to_win()

    def calculate_ways_to_win(self) -> int:
        output = 0
        for i in range(self.total_time):
            speed = i
            remaining_time = self.total_time - i
            distance_traveled = remaining_time * speed
            if distance_traveled > self.distance_to_beat:
                output += 1
        return output


def main():
    print(f"Part #1 Answer:  {find_part_one_answer()}")
    print(f"Part #2 Answer:  {find_part_two_answer()}")
    

def find_part_one_answer():
    race_list = [Race(x[0], x[1]) for x in INPUT_RACES_PART_ONE]
    ways_to_win_list = [race.ways_to_win for race in race_list]

    output = 0
    for i in range(len(ways_to_win_list)):
        if i == 0:
            output = ways_to_win_list[0]
        else:
            output = output * ways_to_win_list[i]
    return output

def find_part_two_answer():
    race = Race(INPUT_RACE_PART_TWO[0], INPUT_RACE_PART_TWO[1])
    return race.ways_to_win
        



if __name__ == '__main__':
    main()