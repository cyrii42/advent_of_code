'''--- Day 2: Cube Conundrum ---'''

import day2_input

input_dict = day2_input.day2_input_dict

test_dict = {
    1: '3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    2: '1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    3: '8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    4: '1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    5: '6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
    }


class Game():
    def __init__(self, id: int, game_string: str):
        self.id = id
        self.game_string = game_string
        self.subsets_list = [subset.split(sep=', ') for subset in self.game_string.split(sep='; ')]

        self.max_colors = {'green': 0, 'red': 0, 'blue': 0}
        for subset in self.subsets_list:
            subset_dict = {color.split()[1]: int(color.split()[0]) for color in subset}
            for color, num in subset_dict.items():
                if num > self.max_colors[color]:
                    self.max_colors[color] = num

        self.power = self.max_colors['green'] * self.max_colors['red'] * self.max_colors['blue']

                        
    def check_possible_part_1(self, red_test: int, green_test: int, blue_test: int) -> bool:
        return red_test >= self.max_colors['red'] and green_test >= self.max_colors['green'] and blue_test >= self.max_colors['blue']


def main():
    games_list = []
    for id, game_string in input_dict.items():
        games_list.append(Game(id, game_string))

    part_1_sum = 0
    for game in games_list:
        if game.check_possible_part_1(red_test=12, green_test=13, blue_test=14):
            part_1_sum = part_1_sum + game.id
    print(f"Answer for Day 2, part 1:  {part_1_sum}")

    part_2_sum = 0
    for game in games_list:
        part_2_sum = part_2_sum + game.power
    print(f"Answer for Day 2, part 2:  {part_2_sum}")
        
        


if __name__ == '__main__':
    main()