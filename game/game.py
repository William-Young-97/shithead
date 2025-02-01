class Game:
    def __init__(self, deck) -> None:
        self.deck = deck
        self.players = []

    # helpers
    def get_players(self):
        return self.players