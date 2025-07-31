import json
from pathlib import Path
from typing import Callable

from rich import print
from rich.pretty import Pretty
from rich.table import Table

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

EXAMPLES_PART_ONE = {
    '[1,2,3]': 6,
    '{"a":2,"b":4}': 6,
    '[[[3]]]': 3,
    '{"a":{"b":4},"c":-1}': 3,
    '{"a":[-1,1]}': 0,
    '[-1,{"a":1}]': 0,
    '[]': 0,
    '{}': 0
}

EXAMPLES_PART_TWO = {
    '[1,2,3]': 6,
    '[1,{"c":"red","b":2},3]': 4,
    '{"d":"red","e":[1,2,3,4],"f":5}': 0,
    '[1,"red",5]': 6
}

INPUT = aoc.get_input(YEAR, DAY)
DESCRIPTION = aoc.get_description(YEAR, DAY)

def parse_data(data: str):
    return data.strip('\n')

def prettify(*args):
    arg_list = list(args)
    return [Pretty(arg) for arg in arg_list]

def test_examples(examples: dict[str, int], func: Callable) -> None:
    table = Table()
    table.add_column('Example', justify='left')
    table.add_column('Expected', justify='center')
    table.add_column('Actual', justify='center')
    table.add_column('Passed?', justify='center')
    for example, expected in examples.items():
        result = func(example)
        row_items = prettify(json.loads(example), expected, result, result == expected)
        table.add_row(*row_items)
    print(table)

def traverse_json(obj: dict | list | str | int, part_two: bool = False):
    output = 0
    if isinstance(obj, int):
        output += obj
    if isinstance(obj, list):
        output += sum(traverse_json(x, part_two=part_two) for x in obj)
    if isinstance(obj, dict):
        if part_two and 'red' in obj.values():
            output += 0
        else:
            output += sum(traverse_json(v, part_two=part_two) for v in obj.values())
    return output

def part_one(data: str):
    s = parse_data(data)
    obj = json.loads(s)
    return traverse_json(obj, part_two=False)

def part_two(data: str):
    s = parse_data(data)
    obj = json.loads(s)
    return traverse_json(obj, part_two=True)


def main():
    test_examples(EXAMPLES_PART_ONE, part_one)
    print(f"Part One (input):  {part_one(INPUT)}")
    test_examples(EXAMPLES_PART_TWO, part_two)
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()