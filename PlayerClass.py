"""
Player's Attributes & Actions
"""
from RulesClass import BlackJack

class Player(BlackJack):
    
    def __init__(self, name : str = "", chips: int = 0):
        super().__init__()
        self.name = name.capitalize()
        self.deck = []
        self.chips = chips
        self.bet = 0
        self.insure = False
    
    def initial_bet(self) -> int:
        """
        Betting 
            Min limit: 2 chips 
            Max limit: ALL IN
        """ 
        print(f"\nMinimum Bet: {self.MIN_BET} chips\nMaximum Bet: {self.chips} chips")
        while True:
            try:
                bet = input(f"How many chips would {self.name} like to bet?(Enter 'q' to get payout) ")
                if bet.lower() == "q":
                    return "q"
                if self.MIN_BET <= int(bet) <= self.chips:
                    self.bet = int(bet)
                    return
                print(f"Amount betted is not between {self.MIN_BET} chips and {self.chips} chips")
            except ValueError:
                print("Please try again and enter a valid number or quit.")

    def user_option(self) -> [str]: 
        """
        The Play
            stand: not ask for another card
            hit: ask for another card(total < 21)
        """
        while BlackJack.under_twenty_one(BlackJack.total(self.deck)):
            option = input("What would you like to do?\n\
                1. Stand\n\
                2. Hit\n")
            if option.lower() == "stand":
                break
            elif option.lower() == "hit":
                self.deck.append(self.random_card())
                print(f"{self.name} drew a {self.deck[len(self.deck) - 1]}. Your total is now {BlackJack.total(self.deck)}.")
            else:
                print("Enter a valid option.")
    
    def special_pair(self) -> str:
        """
        Check what user wants to do if split of double down
        """
        while True:
            try:
                if self.deck[0] == self.deck[1] and 9 <= BlackJack.total(self.deck) <= 11:
                    ans = input(f"{self.name} can either split the pair or double down. Split or Double or Skip? ")
                    if ans.lower() in ["split", "double", "skip"]:
                        return ans.lower()
                elif self.deck[0] == self.deck[1]:
                    ans = input(f"{self.name} can split the pair. Split or Skip? ")
                    if ans.lower() in ["split", "skip"]:
                        return ans.lower()
                elif 9 <= BlackJack.total(self.deck) <= 11:
                    ans = input(f"{self.name} can double down. Double or Skip? ")
                    if ans.lower() in ["double", "skip"]:
                        return ans.lower()
                else:
                    return "skip"
            except:
                print("Please enter a valid answer.")

    def split_pairs(self) -> int:
        """
        Splitting Pairs(two same cards)
        split the two cards and treat them as sperate bets 
        pairs of aces: player is given one card for each ace and cannot draw again
        """
        pair = [[card] for card in self.deck]
        for deck in pair:
            deck.append(self.random_card())
            print(f"{self.name}'s cards are", end= " ")
            print(*deck, sep = ", ", end = " ") 
            print(f"for a total of {BlackJack.total(deck)}.")
            if "A" not in self.deck:
                self.user_option()
    
    def double_down(self) -> int:
        """
        Doubling Down
        when two og cards equal to 9,10, 11, the dealer only gives one card
        do not show the total until dealer finishes
        """
        self.deck.append(self.random_card())
        print(f"{self.name}'s cards are", end= " ")
        print(*self.deck, sep = ", ", end = " ") 
        print(f"for a total of {BlackJack.total(self.deck)}.")

    def turn(self, first_card : str) -> None or str:
        """
        run a player turn
        """
        self.dealer_card = first_card
        print(f"\n{self.name}'s cards are", end= " ")
        print(*self.deck, sep = ", ", end = " ") 
        print(f"for a total of {BlackJack.total(self.deck)}.")
        print(f"Dealer's first card is {self.dealer_card}.")
        if self.dealer_card[0] == "A":
            #fix 
            ask = input("Do you want to place an insurance?(yes/no) ")
            if ask.lower()[0] == "y":
                self.insure = True
                return "y"
        special = self.special_pair()
        if special == "split":
            self.split_pairs()
        elif special == "double":
            self.double_down()
        else:
            self.user_option()
    
    def reset(self) -> None:
        self.bet = 0
        self.deck = []
        self.insure = False