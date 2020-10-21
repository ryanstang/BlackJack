"""
Dealer's Attributes & Actions
"""

from PlayerClass import Player
from RulesClass import BlackJack
import time

class Dealer(Player):
    NUM_OF_PLAYERS = 0

    def __init__(self):
        super().__init__()
        self.list_of_players = []
        self.deck  = []
    
    def add_player(self, player : Player) -> None:
        """
        Check if player name is taken, if not, add to list of players
        """
        current_player = [player.name for player in self.list_of_players]
        while True:
            if player.name.isalpha() and player.name not in current_player:
                self.list_of_players.append(player)
                Dealer.NUM_OF_PLAYERS += 1
                break
            elif not player.name.isalpha():
                new_name = input(f"{player.name} is not a valid entry. Please enter a name: ")
                player.name = new_name.capitalize()
            else:
                new_name = input(f"{player.name} is already chosen. Please enter a different name: ")
                player.name = new_name.capitalize()
    
    def amount_of_money(self) -> int:
        """
        Asking user how many chips they want to get each chip is worth a dollar
        """
        print("$1 = 1 chip")
        while True:
            try:
                chips = int(input(f"How many chips does {self.name} want to buy?(Minimum: ${self.MIN_BET}) $"))
                if chips >= self.MIN_BET:
                    return chips
                print(f"Please enter an amount more than {self.MIN_BET}.")
            except ValueError:
                print("Please try again and enter a valid number.")
    
    def option(self) -> [str]:
        """
        Dealer's Play
        turn the face-down card up
        if total is 17 or more, it must stand
        if total is 16 or under, they must take a card
        if dealer has ace, and counting it as 11 would bring the totoal
        to 17 or more, dealer must stand with those cards
        """
        print("\nDealer's cards are", end= " ")
        print(*self.deck, sep = ", ", end = " ") 
        print(f"for a total of {BlackJack.total(self.deck)}.")
        while BlackJack.under_twenty_one(BlackJack.total(self.deck)):
            tot = BlackJack.total(self.deck)
            if tot >= 17:
                break
            else:
                self.deck.append(self.random_card())
                print(f"Dealer drew a {self.deck[len(self.deck) - 1]}. Dealer's total is now {BlackJack.total(self.deck)}.")
                time.sleep(1)
        return self.deck
    
    def initial_deal(self) -> ([int], [int]):
        """
        The Deal
        give player two cards face up,
        dealer gets one card face up, other faced down
        """
        for _ in range(2):
            for player in self.list_of_players:
                card = self.random_card()
                player.deck.append(card) 
            self.deck.append(card)
    
    def insurance(self, player : Player) -> None:
        """
        if the first card of the dealer is "A", dealer can ask each player
        if they want to place up to half theeir bets to guess if the the second
        card is a 10
        if correct, they win the bet they win 2-1 bet they placed
        """
        while True:
            try:
                ans = int(input(f"{player.name} can bet from {self.MIN_BET} to {player.bet//2} chips for insurance. How many chips would you like to bet? "))
                if self.MIN_BET <= ans <= player.bet //2:
                    break
            except:
                print("Please enter a valid answer.")
        if BlackJack.twenty_one(BlackJack.total(self.deck)):
            print("Dealer's cards are", end= " ")
            print(*self.deck, sep = ", ", end = " ") 
            print(f"for a total of 21. You win {ans * 2} chips!")
            player.chips += ans * 2
        else:
            print(f"Dealer's total did not equal to 21. You lost {ans} chips!")
            player.chips -= ans
    
    def settlement(self, player : Player) -> int: 
        """
        Who Won
        if player bust, dealer auto wins
        if dealer over 21, dealer pays player the bet
        if dealer 21<, dealer pays bet if lost to play
        else standoff(no chips are collected)
        """
        user_tot, dealer_tot = BlackJack.total(player.deck), BlackJack.total(self.deck)
        if dealer_tot > 21:
            print(f"\n{player.name} wins {player.bet} chips!")
            player.chips += player.bet 
        elif user_tot > 21:
            print(f"\n{player.name} loses {player.bet} chips!")
            player.chips -= player.bet
        elif  user_tot > dealer_tot:
            print(f"\n{player.name} wins {player.bet} chips!")
            player.chips += player.bet 
        elif  user_tot < dealer_tot:
            print(f"\n{player.name} loses {player.bet} chips!")
            player.chips -= player.bet 
        else:
            print("It is a standoff!")
    
    def turn(self, player : Player) -> None:
        """
        run a dealer turn
        """
        
        if BlackJack.under_twenty_one(min([BlackJack.total(p.deck) for p in self.list_of_players])):
            self.deck = self.option()
        for player in self.list_of_players:
            if not player.insure:
                self.settlement(player)
            player.reset()