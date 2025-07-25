import functools
import itertools
import json
import math
import os
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from pprint import pprint
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.pretty import Pretty
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def parse_data(data: str):
    return data.strip('\n')

def prettify(*args):
    arg_list = list(args)
    return [Pretty(arg) for arg in arg_list]

def test_examples() -> None:
    examples = {
        '[1,2,3]': 6,
        '{"a":2,"b":4}': 6,
        '[[[3]]]': 3,
        '{"a":{"b":4},"c":-1}': 3,
        '{"a":[-1,1]}': 0,
        '[-1,{"a":1}]': 0,
        '[]': 0,
        '{}': 0
    }

    table = Table()
    table.add_column('Example', justify='left')
    table.add_column('Expected', justify='center')
    table.add_column('Actual', justify='center')
    table.add_column('Passed?', justify='center')
    for example, expected in examples.items():
        print(f"Testing {example} ({type(example)})...")
        result = part_one(example)
        row_items = prettify(json.loads(example), expected, result, result == expected)
        table.add_row(*row_items)
    print(table)
    
def part_one(data: str):
    s = parse_data(data)
    obj = json.loads(s)
    return traverse_json(obj)

def traverse_json(obj: dict | list | str | int):
    output = 0
    if isinstance(obj, int):
        output += obj
    if isinstance(obj, list):
        output += sum(traverse_json(x) for x in obj)
    if isinstance(obj, dict):
        output += sum(traverse_json(v) for v in obj.values())
    return output
        

def part_two(data: str):
    __ = parse_data(data)



def main():
    test_examples()
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()