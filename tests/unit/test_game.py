from game.game import Game
from game.deck import Deck
from game.player import HumanPlayer, AIPlayer
from unittest.mock import patch

# Here is a good spot for an integration test to make sure that the deck is shuffled

# set players is going to exist in a class outside of game. Some ui ish layer.
@patch("builtins.input", return_value="Alice") 
def test_init(mock_input):
    game = Game()

    assert isinstance(game, Game)
    assert isinstance(game.deck, Deck)
    assert len(game.get_players()) == 2
    assert isinstance(game.get_players()[0], HumanPlayer)
    assert isinstance(game.get_players()[1], AIPlayer)

@patch("builtins.input", return_value="Alice") 
def test_deal_cards(mock_input):
    game = Game(num_players=2)
    game._deal_cards()
    for player in game.players:
        assert len(player.hand) == 3
        assert len(player.face_up_cards) == 3
        assert len(player.face_down_cards) == 3

@patch("builtins.input", return_value="Alice") 
def test_win_condition(mock_input):
    game = Game(num_players=2)
    game.players[0].hand = []
    game.players[0].face_up_cards = []
    game.players[0].face_down_cards = []
    
    assert game._check_win_condition() is True
