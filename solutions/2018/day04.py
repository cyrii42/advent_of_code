import datetime as dt
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import NamedTuple
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class EventType(Enum):
    START = 0
    SLEEP = 2
    WAKE = 3

class WakefulnessState(Enum):
    ASLEEP = 0
    AWAKE = 1

class Event(NamedTuple):
    guard_id: int
    dt: dt.datetime
    event_type: EventType

    def __repr__(self) -> str:
        return (f"#{self.guard_id} ({self.dt.strftime('%Y-%m-%d %H:%M')}) " + 
                f"({self.event_type.name})")

class NoSleepiestMinute(Exception):
    pass

@dataclass
class Guard:
    id: int
    event_list: list[Event] = field(repr=False)
    minutes_asleep: int = field(init=False)
    sleep_dict: defaultdict[int, int] = field(init=False)

    def __post_init__(self):
        self.sleep_dict = defaultdict(int)
        self.minutes_asleep = self.get_total_time_asleep()
        
    def get_total_time_asleep(self) -> int:
        sleeps = [event.dt for event in self.event_list
                  if event.event_type == EventType.SLEEP]
        wakeups = [event.dt for event in self.event_list
                  if event.event_type == EventType.WAKE]

        total = 0
        for sleep, wake in zip(sleeps, wakeups):
            total += wake.minute - sleep.minute
            for min in range(sleep.minute, wake.minute):
                self.sleep_dict[min] += 1

        return total

    def get_sleepiest_minute(self) -> tuple[int, int]:
        max_frequency = max(v for v in self.sleep_dict.values())
        mins_at_max = [m for m in self.sleep_dict.keys()
                       if self.sleep_dict[m] == max_frequency]
        if len(mins_at_max) > 1:
            raise NoSleepiestMinute
        sleepiest_minute = mins_at_max[0]
        return (sleepiest_minute, max_frequency)

def make_guards(event_list: list[Event]) -> list[Guard]:
    all_guard_ids = set([event.guard_id for event in event_list])
    guard_list = []
    for guard_id in all_guard_ids:
        events = [event for event in event_list if event.guard_id == guard_id]
        guard_list.append(Guard(guard_id, events))
    return guard_list

def parse_data(data: str) -> list[Event]:
    line_list = data.splitlines()
    
    event_list_1 = []
    for line in line_list:
        parts = line.split(' ')
        date, time = parts[0:2]
        ts = dt.datetime.fromisoformat(f"{date} {time}"[1:-1])
        event_list_1.append((ts, parts[2:]))

    event_list_1 = sorted(event_list_1, key=lambda x: x[0])
    event_list_2 = []
    current_guard_id = None
    for ts, parts in event_list_1:
        match parts[0]:
            case 'Guard':
                current_guard_id = int(parts[1][1:])
                event_list_2.append(Event(current_guard_id, ts, EventType.START))
            case 'wakes':
                assert current_guard_id
                event_list_2.append(Event(current_guard_id, ts, EventType.WAKE))
            case 'falls':
                assert current_guard_id
                event_list_2.append(Event(current_guard_id, ts, EventType.SLEEP))
    return event_list_2
    
def part_one(data: str):
    event_list = parse_data(data)
    guard_list = make_guards(event_list)
    guard_list = sorted(guard_list, key=lambda g: g.minutes_asleep, reverse=True)
    sleepiest_guard = guard_list[0]
    sleepiest_minute, _ = sleepiest_guard.get_sleepiest_minute()
    return sleepiest_minute * sleepiest_guard.id

def find_sleepiest_minute_all_guards(guard_list: list[Guard]) -> int:
    winning_guard_id = -1
    winning_minute = -1
    winning_frequency = -1

    for guard in guard_list:
        if guard.minutes_asleep > 0:
            try:
                sleepiest_minute, max_frequency = guard.get_sleepiest_minute()
                if max_frequency > winning_frequency:
                    winning_guard_id = guard.id
                    winning_minute = sleepiest_minute
                    winning_frequency = max_frequency
            except NoSleepiestMinute:
                continue
    return winning_guard_id * winning_minute

def part_two(data: str):
    event_list = parse_data(data)
    guard_list = make_guards(event_list)
    return find_sleepiest_minute_all_guards(guard_list)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()