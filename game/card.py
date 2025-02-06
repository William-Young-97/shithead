class Card:
    def __init__(self, rank, suit, value, special=False):
        self.rank = rank
        self.suit = suit
        self.value = value
        self.special = special
    
    def __str__(self):
        suit_symbols = {"Spades": "♠", "Hearts": "♥", "Diamonds": "♦", "Clubs": "♣"}
        return f"{self.rank}{suit_symbols[self.suit]}" 