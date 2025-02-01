from game.game import Game
from game.deck import Deck
from game.player import Player

# Here is a good spot for an integration test to make sure that the deck is shuffled


def test_init():
    deck = Deck()
    game = Game(deck)
    p1 = Player()
    p2 = Player()
    assert isinstance(game, Game)
    assert isinstance(game.deck, Deck)
    assert game.get_players() == [p1, p2]

def test_set_players():
    deck = Deck()
    game = Game(deck)