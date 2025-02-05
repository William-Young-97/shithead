from game.player import Player, HumanPlayer, AIPlayer
from game.deck import Deck

class Game:
    def __init__(self, num_players=2) -> None:
        self.deck = Deck()
        self.user = HumanPlayer()
        self.players = [self.user]
        for _ in range(num_players - 1):
            self.players.append(AIPlayer())
        self.current_player = self.get_current_player()
        self.discard_pile = []
    
    def deal_cards(self):
        # Populate all players facedown, facecards, and then hand
        self.deck.shuffle()
        
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
    
    # hard coded for until turns implemented
    def get_current_player(self):
        return self.players[0]

    # helpers
    def get_players(self):
        return self.players