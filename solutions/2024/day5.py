'''--- Day 5: Print Queue ---'''

from pathlib import Path
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2024_day5_example.txt'
INPUT = DATA_DIR / '2024_day5_input.txt'
                
def get_ordering_rules(filename: Path) -> list[tuple[int, int]]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        ordering_rules = [line for line in line_list if '|' in line]
        ordering_rules = [line.split('|') for line in ordering_rules]
        ordering_rules = [(int(x), int(y)) for x, y in ordering_rules]      
        
    return ordering_rules      


def get_page_updates(filename: Path) -> list[list[int]]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        page_updates = [line for line in line_list if '|' not in line and line != '']
        page_updates = [line.split(',') for line in page_updates]
        page_updates = [list(map(int, num_strings)) for num_strings in page_updates]
        
    return page_updates


def validate_update(ordering_rules: list[tuple[int, int]], update: list[int]) -> bool:      
    applicable_rules = [rule for rule in ordering_rules if rule[0] in update and rule[1] in update]

    for i, page in enumerate(update):
        before_failures = [rule[1] for rule in applicable_rules if rule[0] == page and rule[1] in update[:i]] 
        after_failures = [rule[0] for rule in applicable_rules if rule[1] == page and rule[0] in update[i:]]

        if before_failures or after_failures:
            return False

    return True


def fix_invalid_update(ordering_rules: list[tuple[int, int]], update: list[int]) -> list[int]:
    applicable_rules = [rule for rule in ordering_rules if rule[0] in update and rule[1] in update]

    for rule in applicable_rules:
        first_page = rule[0]
        first_page_idx = update.index(first_page)
        second_page = rule[1]
        second_page_idx = update.index(second_page)

        if second_page_idx < first_page_idx:
            update.remove(second_page)
            update.insert(len(update), second_page)

    if validate_update(ordering_rules, update):
        return update

    else:  
        return fix_invalid_update(ordering_rules, update)


def find_middle_page_num(update: list[int]) -> int:
    middle_idx = len(update) // 2  # we're not adding one here because of zero-indexing!!!
    return update[middle_idx]


def part_one(filename: Path) -> int:
    ordering_rules = get_ordering_rules(filename)
    page_updates = get_page_updates(filename)
    valid_updates = [update for update in page_updates if validate_update(ordering_rules, update)]
    answer = sum(find_middle_page_num(update) for update in valid_updates)
    
    return answer


def part_two(filename: Path) -> int:
    ordering_rules = get_ordering_rules(filename)
    page_updates = get_page_updates(filename)
    invalid_updates = [update for update in page_updates if not validate_update(ordering_rules, update)]
    fixed_updates = [fix_invalid_update(ordering_rules, update) for update in invalid_updates]
    answer = sum(find_middle_page_num(update) for update in fixed_updates)
    
    return answer


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # should be 143
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # should be 123
    print(f"Part Two (input):  {part_two(INPUT)}")


if __name__ == '__main__':
    main()