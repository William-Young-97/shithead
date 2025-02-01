from game.card import Card
import random

class Deck:
    def __init__(self) -> None:
        self.cards = self.create()

    def create(self):
        deck = []
        suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
        ranks = ["2", "3", "4", "5", "6", "7", 
                 "8", "9", "10", "Jack", "Queen", "King", 
                 "Ace"]
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        
        for suit in suits:
            for idx, _ in enumerate(ranks):
                deck.append(Card(ranks[idx], suit, values[idx]))
        return deck

    def shuffle(self):
         random.shuffle(self.cards)
    
    # Helper methods
    def get_card_list(self) -> list[tuple]:
        return [(card.rank, card.suit) for card in self.cards]