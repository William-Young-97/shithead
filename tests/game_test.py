from game.game import Game
from game.deck import Deck

def test_init():
    game = Game()
    assert isinstance(game, Game)
    assert isinstance(game.deck, Deck)
