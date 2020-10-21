from DealerClass import Dealer
from PlayerClass import Player


if __name__ == '__main__':
    dealer = Dealer()
    print("Welcome to Black Jack!!!")
    while True:
        try:
            num_ppl = int(input("How many people are playing? "))
            break
        except ValueError:
            print("Please enter a valid number.")
    for i in range(1, num_ppl + 1):
        name = input(f"Player {i}'s name: ")
        chips = dealer.amount_of_money()
        dealer.add_player(Player(name, chips))
    while True:
        payouts = []
        for player in dealer.list_of_players:
            bet = player.initial_bet()
            if bet == "q": 
                print(f"{player.name} are payed out ${chips}. Have a great day!")
                payouts.append(player)
        for player in payouts:
            dealer.list_of_players.remove(player)
        if not dealer.list_of_players:
            break
        dealer.initial_deal()
        for player in dealer.list_of_players:
            insurance = player.turn(dealer.deck[0])
            if insurance == "y":
                dealer.insurance(player)
        dealer.turn(player)    
        dealer.reset()
