import datetime as dt
import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
import sys
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, NamedTuple, Optional, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_bar, alive_it
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
    ts: dt.datetime
    event_type: EventType

@dataclass
class Guard:
    id: int
    event_dict: dict[dt.datetime, EventType] = field(repr=False)
    minutes_asleep: int = field(init=False)
    tick_tock_dict: dict[dt.datetime, WakefulnessState] = field(init=False, repr=False)
    sleepiest_minute: int = field(init=False)

    def __post_init__(self):
        self.minutes_asleep = self.get_total_time_asleep()
        self.tick_tock_dict = self.make_tick_tock_dict()
        if self.minutes_asleep > 0:
            self.sleepiest_minute = self.get_sleepiest_minute()
        
    def get_total_time_asleep(self) -> int:
        sleeps = [ts for ts, event_type in self.event_dict.items()
                  if event_type == EventType.SLEEP]
        wakeups = [ts for ts, event_type in self.event_dict.items()
                   if event_type == EventType.WAKE]

        total = 0
        for sleep, wake in zip(sleeps, wakeups):
            total += wake.minute - sleep.minute
        return total

    def make_tick_tock_dict(self) -> dict[dt.datetime, WakefulnessState]:
        output_dict = {}
        current_state = WakefulnessState.AWAKE
        sorted_event_dict = sorted(self.event_dict)
        for i, ts in enumerate(sorted_event_dict):
            if i >= len(self.event_dict) - 1:
                break
            match self.event_dict[ts]:
                case EventType.START | EventType.WAKE:
                    current_state = WakefulnessState.AWAKE
                case EventType.SLEEP:
                    current_state = WakefulnessState.ASLEEP
            min_range = sorted_event_dict[i+1].minute - ts.minute
            for x in range(min_range+1):
                output_dict[ts + dt.timedelta(minutes=x)] = current_state
        return output_dict

    def get_sleepiest_minute(self) -> int:
        output_dict = defaultdict(int)
        for ts, state in self.tick_tock_dict.items():
            if state == WakefulnessState.ASLEEP:
                output_dict[ts.minute] += 1
        sorted_list = sorted(output_dict.items(), key=lambda x: x[1], reverse=True)
        return sorted_list[0][0]

def make_guards(event_list: list[Event]) -> list[Guard]:
    all_guard_ids = set([event.guard_id for event in event_list])
    guard_list = []
    for guard_id in all_guard_ids:
        events = [event for event in event_list if event.guard_id == guard_id]
        event_dict = {event.ts: event.event_type for event in events}
        guard_list.append(Guard(guard_id, event_dict))
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
    print(guard_list)
    guard_list = sorted(guard_list, key=lambda g: g.minutes_asleep, reverse=True)
    sleepiest_guard = guard_list[0]
    # print(sleepiest_guard.tick_tock_dict)
    # print(sleepiest_guard.get_sleepiest_minute())
    return sleepiest_guard.sleepiest_minute * sleepiest_guard.id

def part_two(data: str):
    __ = parse_data(data)



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()