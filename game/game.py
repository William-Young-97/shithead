from game.player import Player, HumanPlayer, AIPlayer

class Game:
    def __init__(self, deck, num_players=2) -> None:
        self.deck = deck
        self.user = HumanPlayer()
        self.players = [self.user]
        for _ in range(num_players - 1):
            self.players.append(AIPlayer())

    # helpers
    def get_players(self):
        return self.players