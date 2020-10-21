"""
Deck of Cards & Universal Rules of BlackJack
"""

import random

class BlackJack:
    CARD_VALUE = {
        "A": [1, 11],
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10
    }
    MIN_BET = 2

    def __init__(self):
        self.deck_of_cards = {
            "A": 4,
            "1": 4,
            "2": 4,
            "3": 4,
            "4": 4,
            "5": 4,
            "6": 4,
            "7": 4,
            "8": 4,
            "9": 4,
            "10": 4,
            "J": 4,
            "Q": 4,
            "K": 4
        }


    def random_card(self) -> str:
        """
        pick random cards
        """
        check = set(list(self.deck_of_cards.values()))
        if len(check) == 1 and 0 in check: self.reset_cards()
        while True:
            card = random.choice(list(self.deck_of_cards))
            if self.deck_of_cards[card] >= 1:
                self.deck_of_cards[card] -= 1
                return card

    def reset_cards(self) -> None:
        """
        reset cards 
        """
        for card in self.deck_of_cards:
            self.deck_of_cards[card] = 4

    @staticmethod
    def total(my_deck : [str]) -> int:
        """
        showing your total and the dealer's total
        """
        if "A" not in my_deck:
            return sum([BlackJack.CARD_VALUE[card] for card in my_deck])
        else:
            res = 0
            for i in range(len(my_deck)):
                if my_deck[i] == "A":
                    if BlackJack.under_twenty_one(res + BlackJack.CARD_VALUE[my_deck[i]][1] + BlackJack.total(my_deck[i+1:])):
                        res += BlackJack.CARD_VALUE[my_deck[i]][1]
                    else:
                        res += BlackJack.CARD_VALUE[my_deck[i]][0]
                else:
                    res += BlackJack.CARD_VALUE[my_deck[i]]
            return res

    @staticmethod
    def twenty_one(res : int) -> bool:
        """
        Checking if card(s) equals to 21 or more, auto win at 21
        """
        if res == 21: 
            print("You got 21!")
            return True
   
    @staticmethod
    def under_twenty_one(res : int) -> bool:
        """
        Checking if card(s) is still under 21
        """ 
        if res < 21:
            return True
        return False

