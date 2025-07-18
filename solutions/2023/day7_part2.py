'''--- Day 7: Camel Cards ---'''

from dataclasses import dataclass, field
from enum import IntEnum

CARD_LIST = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

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
    jokers_in_hand: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.cards_sorted_by_prevalence = ''.join(sorted(self.card_str, key=lambda x: self.card_str.count(x), reverse=True))
        self.cards_sorted_by_prevalence_minus_jokers = ''.join(sorted(self.card_str.replace('J', ''), 
                                                                      key=lambda x: self.card_str.count(x), reverse=True))
        self.cards_set = set(self.card_str)
        self.cards_set_minus_jokers = set(self.cards_sorted_by_prevalence_minus_jokers)
        self.jokers_in_hand = self.card_str.count('J')
        self.hand_type = self.determine_hand_type_with_jokers() if self.jokers_in_hand > 0 else self.determine_hand_type_no_jokers()

    def determine_hand_type_no_jokers(self) -> HandType:
        most_prevelant_card = self.cards_sorted_by_prevalence[0]
        if len(self.cards_set) == 1:
            return HandType.FIVE_OF_A_KIND
        elif len(self.cards_set) == 2:
            if self.card_str.count(most_prevelant_card) == 4:
                return HandType.FOUR_OF_A_KIND
            else:
                return HandType.FULL_HOUSE
        elif len(self.cards_set) == 3:
            if self.card_str.count(most_prevelant_card) == 3:
                return HandType.THREE_OF_A_KIND
            else:
                return HandType.TWO_PAIR
        elif len(self.cards_set) == 4:
            return HandType.ONE_PAIR 
        else:
            return HandType.HIGH_CARD

    def determine_hand_type_with_jokers(self) -> HandType:
        most_prevelant_non_joker_card = None if self.jokers_in_hand == 5 else self.cards_sorted_by_prevalence_minus_jokers[0]
        if self.jokers_in_hand >= 4:
            return HandType.FIVE_OF_A_KIND
        elif self.jokers_in_hand == 3:
            if self.card_str.count(most_prevelant_non_joker_card) == 2:
                return HandType.FIVE_OF_A_KIND
            else:
                return HandType.FOUR_OF_A_KIND
        elif self.jokers_in_hand == 2:
            if self.card_str.count(most_prevelant_non_joker_card) == 3:
                return HandType.FIVE_OF_A_KIND
            elif self.card_str.count(most_prevelant_non_joker_card) == 2:
                return HandType.FOUR_OF_A_KIND
            else:
                return HandType.THREE_OF_A_KIND
        elif self.jokers_in_hand == 1:
            if self.card_str.count(most_prevelant_non_joker_card) == 4:
                return HandType.FIVE_OF_A_KIND
            elif self.card_str.count(most_prevelant_non_joker_card) == 3:
                return HandType.FOUR_OF_A_KIND
            elif self.card_str.count(most_prevelant_non_joker_card) == 2:
                if len(self.cards_set_minus_jokers) == 2:
                    return HandType.FULL_HOUSE
                else:
                    return HandType.THREE_OF_A_KIND
            else:
                return HandType.ONE_PAIR
            
        
@dataclass
class HandGroup():
    hand_list: list[Hand]
    hand_list_sorted: list[Hand] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.total_winnings = sum([(hand.bid * rank) for rank, hand in enumerate(self.sort_hands_by_strength(reverse=False), start=1)])
        
    def sort_hands_by_strength(self, reverse: bool = True) -> list[Hand]:
        return sorted(self.hand_list, key=lambda hand: (hand.hand_type,
                                                        CARD_LIST.index(hand.card_str[0]),  
                                                        CARD_LIST.index(hand.card_str[1]), 
                                                        CARD_LIST.index(hand.card_str[2]), 
                                                        CARD_LIST.index(hand.card_str[3]), 
                                                        CARD_LIST.index(hand.card_str[4])), reverse=reverse)         
    

def main():
    hand_group = create_hand_group()
    print(f"Total Winnings:  {hand_group.total_winnings}")


def create_hand_group() -> HandGroup:
    with open('./inputs/day7.txt') as file:
        line_list = file.read().split(sep='\n')

    line_list_split = [x.split(sep=' ') for x in line_list]
    return HandGroup([Hand(line[0], int(line[1])) for line in line_list_split])


if __name__ == '__main__':
    main()