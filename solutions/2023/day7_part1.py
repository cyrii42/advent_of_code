'''--- Day 7: Camel Cards ---'''

from dataclasses import dataclass, field
from enum import IntEnum

CARD_LIST = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

class HandType(IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0

@dataclass
class Hand():
    card_str: str
    bid: int
    hand_type: HandType = field(init=False)
    cards_sorted_by_prevalence: str = field(init=False, repr=False)
    cards_set: set = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.cards_sorted_by_prevalence = ''.join(sorted(self.card_str, key=lambda x: self.card_str.count(x), reverse=True))
        self.cards_set = set(self.card_str)
        self.hand_type = self.determine_hand_type()

    def determine_hand_type(self) -> HandType:
        if len(self.cards_set) == 1:
            return HandType.FIVE_OF_A_KIND
        elif len(self.cards_set) == 2:
            if self.cards_sorted_by_prevalence.count(self.cards_sorted_by_prevalence[0]) == 4:
                return HandType.FOUR_OF_A_KIND
            else:
                return HandType.FULL_HOUSE
        elif len(self.cards_set) == 3:
            if self.cards_sorted_by_prevalence.count(self.cards_sorted_by_prevalence[0]) == 3:
                return HandType.THREE_OF_A_KIND
            else:
                return HandType.TWO_PAIR
        elif len(self.cards_set) == 4:
            return HandType.ONE_PAIR 
        else:
            return HandType.HIGH_CARD
        
            

@dataclass
class HandGroup():
    hand_list: list[Hand]
    hand_list_sorted: list[Hand] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.hand_list_sorted = self.sort_hands_by_strength()
        self.total_winnings = sum([(hand.bid * rank) for rank, hand in enumerate(self.hand_list_sorted, start=1)])
        
    def sort_hands_by_strength(self) -> list[Hand]:
        return sorted(self.hand_list, key=lambda hand: (hand.hand_type,    # tuple with condition & tiebreakers
                                                        CARD_LIST.index(hand.card_str[0]),  
                                                        CARD_LIST.index(hand.card_str[1]), 
                                                        CARD_LIST.index(hand.card_str[2]), 
                                                        CARD_LIST.index(hand.card_str[3]), 
                                                        CARD_LIST.index(hand.card_str[4])), reverse=False)         

    


def main():
    hand_group = HandGroup(create_hand_list())
    print(f"Total Winnings:  {hand_group.total_winnings}")


def create_hand_list() -> list[Hand]:
    with open('./inputs/day7.txt') as file:
        line_list = file.read().split(sep='\n')

    line_list_split = [x.split(sep=' ') for x in line_list]
    return [Hand(line[0], int(line[1])) for line in line_list_split]


if __name__ == '__main__':
    main()