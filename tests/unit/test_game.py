from game.game import Game
from game.deck import Deck
from game.player import Player, HumanPlayer, AIPlayer

# Here is a good spot for an integration test to make sure that the deck is shuffled

# set players is going to exist in a class outside of game. Some ui ish layer.

def test_init():
    deck = Deck()
    game = Game(deck)

    assert isinstance(game, Game)
    assert isinstance(game.deck, Deck)
    assert len(game.get_players()) == 2
    assert isinstance(game.get_players()[0], HumanPlayer)
    assert isinstance(game.get_players()[1], AIPlayer)

def test_deal_cards():
    deck = Deck()
    game = Game(deck)

    game.deal_cards()
    # check user has been dealt cards
    assert len(game.get_players()[0].get_face_down_cards()) == 3
    assert len(game.get_players()[0].get_face_up_cards()) == 3
    assert len(game.get_players()[0].get_hand()) == 3
    # check ai has  been dealt cards
    assert len(game.get_players()[0].get_face_down_cards()) == 3
    assert len(game.get_players()[0].get_face_up_cards()) == 3
    assert len(game.get_players()[0].get_hand()) == 3

# when i implement turns i'll extend this to make sure we circle the array of
# current players
def test_get_current_player():
    deck = Deck()
    game = Game(deck)
    c = game.get_current_player()

    assert c == game.players[0]
