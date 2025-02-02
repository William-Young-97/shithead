from game.player import Player, HumanPlayer, AIPlayer

class Game:
    def __init__(self, deck, num_players=2) -> None:
        self.deck = deck
        self.user = HumanPlayer()
        self.players = [self.user]
        for _ in range(num_players - 1):
            self.players.append(AIPlayer())
        self.current_player = self.get_current_player()
    
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
    
    # hard coded for until turns implemented
    def get_current_player(self):
        return 0

    # helpers
    def get_players(self):
        return self.players