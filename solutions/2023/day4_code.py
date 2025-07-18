'''--- Day 4: Scratchcards ---'''

from dataclasses import dataclass, field
import time

class Card():
    def __init__(self, card_num: str, winning_nums: list, held_nums: list):
        self.card_num = int(card_num)
        self.winning_nums = winning_nums
        self.held_nums = held_nums
        self.num_of_winning_numbers = len([x for x in self.held_nums if x in self.winning_nums])
        self.total_points = self.find_total_points() if self.num_of_winning_numbers > 0 else 0
        self.reward_card_nums = self.find_reward_card_nums()

    def find_total_points(self) -> int:
        total = 0
        for x in range(self.num_of_winning_numbers):
            if x == 0:
                total = 1
            else: 
                total = total * 2
        return total

    def find_reward_card_nums(self) -> list[int]:
        card_num_list = [x for x in range(self.card_num+1, (self.card_num + 1 + self.num_of_winning_numbers))]
        print(f"Card #{self.card_num} gets {self.num_of_winning_numbers} reward cards:  {card_num_list}")
        return card_num_list
  
@dataclass
class CardPile():
    card_list: list[Card]
    rewards_card_list: list[Card] = field(init=False)

    def __post_init__(self):
        self.rewards_card_list = self.card_list + self.pull_all_reward_cards(self.card_list)

    def pull_card(self, card_num_to_pull: int) -> Card:
        for card in self.card_list:
            if card.card_num == card_num_to_pull:
                return card
        print(f"ERROR:  Could not find Card #{card_num_to_pull}")

    def pull_reward_cards_for_card(self, card: Card) -> list[Card]:
        output_list = []
        for reward_card_num in card.reward_card_nums:
            output_list.append(self.pull_card(reward_card_num))
        return output_list

    def pull_all_reward_cards(self, list_of_cards: list[Card]) -> list[Card]:
        output_list = []
        for card in list_of_cards:
            print(f"Processing Card #{card.card_num} ({card.num_of_winning_numbers} reward cards)...")
            reward_cards = self.pull_reward_cards_for_card(card)
            if len(reward_cards) > 0:
                print(f"Card #{card.card_num}:  Pulling {card.num_of_winning_numbers} Reward Card(s) {[x.card_num for x in reward_cards]}")
                output_list += reward_cards    
                output_list += self.pull_all_reward_cards(reward_cards)

        return output_list

def main():
    start_time = time.time()
    card_pile = ingest_input_string()

    part_one_answer = find_part_one_answer(card_pile.card_list)
    print(f"PART ONE:  {part_one_answer} points")
    
    part_two_answer = len(card_pile.rewards_card_list)
    print(f"PART TWO:  {part_two_answer} total reward cards ({time.time() - start_time:.2f} sec)") 


def find_part_one_answer(card_list: list[Card]) -> int:
    grand_total = 0
    for card in card_list:
        print(f"# of winning nums:  {card.num_of_winning_numbers}")
        print(f"Points:  {card.total_points}")
        grand_total += card.total_points

    return grand_total

def ingest_input_string() -> CardPile:
    with open('./inputs/day4.txt') as file:
        input_string = file.read()

    card_string_list = [x.lstrip('Card').strip() for x in input_string.split(sep="\n")]
    card_num_list = [(x.split(sep=":"))[0] for x in card_string_list]
    nums_list = [(x.split(sep=":"))[1].strip() for x in card_string_list]
    winning_nums_list = [(((x.split(sep="|"))[0]).strip()).split(sep=' ') for x in nums_list]
    held_nums_list = [(((x.split(sep="|"))[1]).strip()).split(sep=' ') for x in nums_list]

    card_list = []
    for x in range(len(card_num_list)):
        card = Card(card_num_list[x], 
                    [int(num) for num in winning_nums_list[x] if num != ''], 
                    [int(num) for num in held_nums_list[x] if num != ''])
        card_list.append(card)
    return CardPile(card_list)


test_list = CardPile([
    Card(1, [41, 48, 83, 86, 17], [83, 86,  6, 31, 17,  9, 48, 53,]),
    Card(2, [13, 32, 20, 16, 61], [61, 30, 68, 82, 17, 32, 24, 19,]),
    Card(3, [ 1, 21, 53, 59, 44], [69, 82, 63, 72, 16, 21, 14,  1,]),
    Card(4, [41, 92, 73, 84, 69], [59, 84, 76, 51, 58,  5, 54, 83,]),
    Card(5, [87, 83, 26, 28, 32], [88, 30, 70, 12, 93, 22, 82, 36,]),
    Card(6, [31, 18, 13, 56, 72], [74, 77, 10, 23, 35, 67, 36, 11,])
])


if __name__ == '__main__':
    main()