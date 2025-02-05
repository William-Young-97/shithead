from typing import List
from game.deck import Deck
from game.player import Player, HumanPlayer, AIPlayer
from game.card import Card

class Game:
    def __init__(self, num_players: int = 2):
        self.deck = Deck()
        self.discard_pile: List[Card] = []
        self.players: List[Player] = []
        self.current_player_index = 0
        self._initialize_players(num_players)
    
    def _initialize_players(self, num_players: int):
        self.players.append(HumanPlayer())
        for _ in range(num_players - 1):
            self.players.append(AIPlayer())
    
    def deal_cards(self):
        for player in self.players:
            for _ in range(3):
                player.face_down_cards.append(self.deck.cards.pop())
            for _ in range(3):
                player.face_up_cards.append(self.deck.cards.pop())
            for _ in range(3):
                player.hand.append(self.deck.cards.pop())
    
    def _check_win_condition(self) -> bool:
        for player in self.players:
            if not player.hand and not player.face_up_cards and not player.face_down_cards:
                return True
        return False
    

    # helpers
    def get_players(self):
        return self.players