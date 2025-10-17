#texas holdem 
import random
from phevaluator.evaluator import evaluate_cards

#define classes
class Player():
    """initalize a baseline for both human and computer players"""
    def __init__(self, given_name, given_chips):
        """initalize initial attributes"""
        
        self.name=given_name
        self.initial_chips=given_chips
        self.chips=given_chips
        self.is_dealer=False
        self.is_playing=False
        self.hand=[]
        self.has_bet=False
        self.amount_contributed=0
        self.final_score=0
        self.has_bust=False
        
    def choose_move(self, is_betting, current_hand):
        
        print(f"\n{self.name}'s Current Hand: {self.hand} Total Chips: {self.chips}")
        choice=input(f"Would you like to bet, call, or fold {self.name}? ").lower()
        
        if choice=="bet":
            pass
        
        elif choice=="call":
            self.call_bet()
        
        elif choice=="fold":
            self.fold()
        
        return choice
        
        
    def bet(self):
        
        while True:
            bet_amount=int(input("How much would you like to bet? "))
            if bet_amount>self.chips:
                print("You do not have sufficent chips, try again.")
            else:
                self.amount_contributed+=bet_amount
                self.chips-=bet_amount
                self.has_bet=True
                
                print(f"\n{self.name} has bet {bet_amount} chips.")
                
                return bet_amount
                break
        
    def call_bet(self):
        print(f"\n{self.name} has called.")
    
    
    def raise_bet(self, amount):
        raise_amount=int(input("How much would you like to raise by? "))
        
        total_amount=raise_amount+amount
        self.amount_contributed+=total_amount
        self.chips-=total_amount
        
        print(f"\n{self.name} has raised the bet to {total_amount}.")
        
        return total_amount
    
    
    def fold(self):
        self.is_playing=False
        print(f"\n{self.name} has folded.")
    
    
    def player_evaluate(self, current_hand):
        if len(current_hand) == 3: 
            score=evaluate_cards(self.hand[0], self.hand[1], current_hand[0],current_hand[1], current_hand[2])
        elif len(current_hand) == 4: 
            score=evaluate_cards(self.hand[0], self.hand[1], current_hand[0],current_hand[1], current_hand[2], current_hand[3])
        elif len(current_hand)==5:
            score=evaluate_cards(self.hand[0], self.hand[1], current_hand[0],current_hand[1], current_hand[2], current_hand[3], current_hand[4])
        
        return score

class Human_Player(Player):
    """create a class for the human player"""
    def __init__(self, given_name, given_chips):
        super().__init__(given_name, given_chips)
        
        self.is_human=True
    def display_info(self):
        print(f"\nPlayer: {self.name}")
        print(f"Current Chips: {self.chips}")
        
        overall_chips=self.chips-self.initial_chips
        if overall_chips<0:
            print(f"Loss: {overall_chips} chips")
        else:
            print(f"Profit: {overall_chips} chips")
    
    
    def display_hand(self):
        print(f"Your Hand: {self.hand}")
        
        
    def display_chips(self):
        print(f"You have {self.chips} chips.")
    

class Computer_Player(Player):
    """create a class for the computer players"""
    def __init__(self, given_name, given_chips):
        super().__init__(given_name, given_chips)
        
        self.is_human=False
    
    def bet(self, amount):
        
        self.current_bet=amount
        
        while True:
            if amount>self.chips:
                self.fold()
            else:
                self.amount_contributed+=amount
                self.chips-=amount
                self.has_bet=True
                
                print(f"\n{self.name} has bet {amount} chips.")
                
                break
    
    def choose_move(self, is_betting, current_hand):
        score=self.player_evaluate(current_hand)
        
        if score>7000:
            if is_betting==True:
                choice="fold"
                self.fold()
            else:
                choice="call"
                self.call_bet()
        
        elif score>5000:
            #small bet
            if is_betting==True:
                choice="fold"
                self.fold()
            else:
                choice="bet"
                self.bet(random.randint(1,3))
        
        elif score>3000:
            #medium bet
            if is_betting==True:
                choice="call"
                self.call_bet()
            else:
                choice="bet"
                self.bet(random.randint(5,20))
        
        elif score>1000:
            #large bet
            if is_betting==True:
                choice="call"
                self.call_bet()
            else:
                choice="bet"
                self.bet(random.randint(25,50))
        
        else:
            if is_betting==True:
                choice="call"
                self.call_bet()
            else:
                choice="bet"
                self.bet(self.chips)
        
        return choice
        
class Game():
    """create a class to handle the poker game"""
    def __init__(self, given_players):
        
        self.players=given_players
        self.currently_playing=given_players
        self.cards_in_play=[]
        self.active_players=len(self.players)
        
    def initialize_deck(self):
        
        suits=["C", "D", "S", "H"]
        ranks=["2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K", "A"]
        self.hand=[]
        
        for suit in suits:
            for rank in ranks:
                card=rank+suit
                self.hand.append(card)
        
        random.shuffle(self.hand)
    
    def betting_pot(self):
        self.pot_amount=0
        
        #collect 5 tokens from each player each round for ante
        for player in self.players:
            player.chips-=5
            if player.chips<0:
                print(f"{player.name} you are out of chips, you can no longer play.")
                player.chips=0
                player.is_playing=False
                player.has_bust=True
                self.active_players-=1
            else:
                player.is_playing=True
                self.pot_amount+=5
    
    
    def initialize_hands(self):
        for player in self.players:
            card_1=self.hand.pop(0)
            card_2=self.hand.pop(0)
            
            player.hand.append(card_1)
            player.hand.append(card_2)
        
    
    
    def place_bets(self):
        
        is_betting=True
        is_a_bet=False
        bet_amount=0
        turn_count=0
        
        for player in players:
            player.amount_contributed=0
            
        while is_betting:
            for player in self.players:
                if player.is_playing==True:
            
                    if turn_count==self.active_players:
                        is_betting=False
                        break
                        
                    chosen_move=player.choose_move(is_a_bet, self.cards_in_play)
                    
                    if chosen_move=="bet":
                        
                        if is_a_bet==True:
                            bet_amount=player.raise_bet(bet_amount)
                            self.pot_amount+=bet_amount
                            player.has_bet=True
                         
                        else:
                            if player.is_human==True:
                                bet_amount=player.bet()
                            else:
                                bet_amount=player.current_bet
                            
                            is_a_bet=True
                            self.pot_amount+=bet_amount
                            
                        turn_count=1
                    
                    elif chosen_move=="call":
                        if player.has_bet==True:
                            chips_called=bet_amount-player.amount_contributed
                            player.chips-=chips_called
                            self.pot_amount+=chips_called
                        else:
                            player.chips-=bet_amount
                            self.pot_amount+=bet_amount
                            player.has_bet=True
                            player.amount_contributed+=bet_amount
                        turn_count+=1
                    else:
                        self.active_players-=1
                        self.currently_playing.pop(self.players.index(player))
                else:
                    pass
        
    def show_flop(self):
        card_1=self.hand.pop(0)
        self.cards_in_play.append(card_1)
        card_2=self.hand.pop(0)
        self.cards_in_play.append(card_2)
        card_3=self.hand.pop(0)
        self.cards_in_play.append(card_3)
        
        print("\n-------------------THE FLOP-------------------")
        print(f"\t      {self.cards_in_play}")
    
        self.place_bets()
          
        print(f"\n{self.pot_amount} chips in the pot")
        
        input("Press Enter to Continue:")
        
    def show_turn(self):
        card_1=self.hand.pop(0)
        self.cards_in_play.append(card_1)
        
        print("\n-------------------THE TURN-------------------")
        print(f"\t  {self.cards_in_play}")
        
        self.place_bets()
        
        print(f"\n{self.pot_amount} chips in the pot")

        input("Press Enter to Continue:")

    def show_river(self):
        card_1=self.hand.pop(0)
        self.cards_in_play.append(card_1)
        
        print("\n------------------THE RIVER-------------------")
        print(f"\t{self.cards_in_play}")
        
        self.place_bets()
        
        print(f"\n{self.pot_amount} chips in the pot")
        
        input("Press Enter to Continue:")
        
    def determine_winner(self):
        scores=[]
        for player in self.currently_playing:
            player.final_score=player.player_evaluate(self.cards_in_play)
            scores.append(player.final_score)
            
        winning_score=min(scores)
        index=scores.index(winning_score)
        
        print(f"\n{self.currently_playing[index].name} had the winning hand!")
        self.currently_playing[index].chips+=self.pot_amount

#main code

#my_game=Game(players)

#my_game.initialize_deck()
#my_game.initialize_hands()
#my_game.betting_pot()
#my_game.show_flop()
#my_game.show_turn()
#my_game.show_river()
#my_game.determine_winner()

players=[]
cpu_names=["Michael", "Dan", "Ethan", "James", "Noah", "Bob", "Joe", "Olivia", "Alan", "Emily", "Ava"]
print("Welcome to the Texas Hold'Em Simulator!")

name=input("\nWhat is your name? ").title()
chips=int(input("How many chips would you like to play with? "))

player_1=Human_Player(name, chips)
players.append(player_1)

num_players=int(input("How many players would you like to play with? "))

for i in range(num_players):
    name=random.choice(cpu_names)
    cpu_names.remove(name)
    cpu_player=Computer_Player(name, random.randint(500,1500))
    players.append(cpu_player)

is_playing=True
while is_playing:
    my_game=Game(players)
    
    my_game.initialize_deck()
    my_game.initialize_hands()
    my_game.betting_pot()
    my_game.show_flop()
    my_game.show_turn()
    my_game.show_river()
    my_game.determine_winner()
    
    keep_playing=input("\nWould you like to play another round? ")
    if keep_playing.startswith('n'):
        is_playing=False

print("\nThank you for playing!")
