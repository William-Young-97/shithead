from game.player import Player

class Game:
    def __init__(self, deck, num_players=2) -> None:
        self.deck = deck
        self.players = []
        for _ in range(num_players):
            self.players.append(Player())

    # helpers
    def get_players(self):
        return self.players