'''--- Day 2: Rock Paper Scissors ---'''

from pathlib import Path
from enum import IntEnum
from advent_of_code.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day2_example.txt'
INPUT = DATA_DIR / '2022_day2_input.txt'

def ingest_data(filename: Path) -> list[list[str]]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n').split() for line in f.readlines()]
    return line_list
                
class Hand(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class Result(IntEnum):
    WIN = 6
    DRAW = 3
    LOSS = 0

def process_game_part_one(game: tuple[Hand, Hand]) -> int:
    opponent_hand, player_hand = game
    if player_hand == opponent_hand:
        return player_hand + Result.DRAW
    elif player_hand == Hand.ROCK and opponent_hand == Hand.SCISSORS:
        return player_hand + Result.WIN
    elif player_hand == Hand.ROCK and opponent_hand == Hand.PAPER:
        return player_hand + Result.LOSS
    elif player_hand == Hand.SCISSORS and opponent_hand == Hand.PAPER:
        return player_hand + Result.WIN
    elif player_hand == Hand.SCISSORS and opponent_hand == Hand.ROCK:
        return player_hand + Result.LOSS
    elif player_hand == Hand.PAPER and opponent_hand == Hand.ROCK:
        return player_hand + Result.WIN
    elif player_hand == Hand.PAPER and opponent_hand == Hand.SCISSORS:
        return player_hand + Result.LOSS
    else:
        raise ValueError

def process_data_part_one(line_list: list[list[str]]) -> list[tuple[Hand, Hand]]:
    return [(translate_hand_part_one(line[0]), translate_hand_part_one(line[1])) 
            for line in line_list]

def translate_hand_part_one(hand_str: str) -> Hand:
    match hand_str:
        case 'A'|'X':
            return Hand.ROCK
        case 'B'|'Y':
            return Hand.PAPER
        case 'C'|'Z':
            return Hand.SCISSORS
        case _:
            raise ValueError    

def process_data_part_two(line_list: list[list[str]]) -> list[tuple]:
    return [(translate_game_str_part_two(line[0]), translate_game_str_part_two(line[1])) 
            for line in line_list]

def translate_game_str_part_two(game_str: str) -> Hand | Result:
    match game_str:
        case 'A':
            return Hand.ROCK
        case 'B':
            return Hand.PAPER
        case 'C':
            return Hand.SCISSORS
        case 'X':
            return Result.LOSS
        case 'Y':
            return Result.DRAW
        case 'Z':
            return Result.WIN
        case _:
            raise ValueError  

def process_game_part_two(game: tuple[Hand, Result]) -> int:
    opponent_hand, result = game
    if result == Result.DRAW:
        return opponent_hand + result
    if result == Result.WIN and opponent_hand == Hand.ROCK:
        return Hand.PAPER + result
    if result == Result.WIN and opponent_hand == Hand.PAPER:
        return Hand.SCISSORS + result
    if result == Result.WIN and opponent_hand == Hand.SCISSORS:
        return Hand.ROCK + result
    if result == Result.LOSS and opponent_hand == Hand.ROCK:
        return Hand.SCISSORS + result
    if result == Result.LOSS and opponent_hand == Hand.PAPER:
        return Hand.ROCK + result
    if result == Result.LOSS and opponent_hand == Hand.SCISSORS:
        return Hand.PAPER + result
    else:
        raise ValueError


def part_one(filename: Path) -> int:
    line_list = ingest_data(filename)
    game_list = process_data_part_one(line_list)
    answer = sum(process_game_part_one(game) for game in game_list)
    return answer
            
def part_two(filename: Path) -> int:
    line_list = ingest_data(filename)
    game_list = process_data_part_two(line_list)
    answer = sum(process_game_part_two(game) for game in game_list)
    return answer

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # should be 15
    print(f"Part One (input):  {part_one(INPUT)}") # 
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # should be 12
    print(f"Part Two (input):  {part_two(INPUT)}") # 

if __name__ == '__main__':
    main()