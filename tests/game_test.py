from game.game import Game
from game.deck import Deck
# Here is a good spot for an integration test to make sure that the deck is shuffled
# after being init
def test_init():
    deck = Deck()
    game = Game(deck)
    assert isinstance(game, Game)
    assert isinstance(game.deck, Deck)
    assert get_players() == []