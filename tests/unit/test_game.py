from game.game import Game
from game.deck import Deck
from game.card import Card
from game.player import HumanPlayer, AIPlayer
from unittest.mock import patch
from tests.helpers import fake_input_sequence, fake_output



def test_init():
    game = Game(input_fn=fake_input_sequence(["Bob"]), output_fn=fake_output)

    assert isinstance(game, Game)
    assert isinstance(game.deck, Deck)
    assert len(game.get_players()) == 2
    assert isinstance(game.get_players()[0], HumanPlayer)
    assert isinstance(game.get_players()[1], AIPlayer)

def test_deal_cards():
    game = Game(input_fn=fake_input_sequence(["Bob"]), output_fn=fake_output)
    game._deal_cards()
    for player in game.players:
        assert len(player.hand) == 3
        assert len(player.face_up_cards) == 3
        assert len(player.face_down_cards) == 3

def test_win_condition():
    game = Game(input_fn=fake_input_sequence(["Bob"]), output_fn=fake_output)
    game.players[0].hand = []
    game.players[0].face_up_cards = []
    game.players[0].face_down_cards = []
    
    winner = game._check_win_condition()
    assert winner is game.players[0]

def test_effective_top_card():
    # test that 3 is ignored
    game = Game(input_fn=fake_input_sequence(["Bob"]), output_fn=fake_output)
    game.discard_pile = [
        Card("9", "Hearts", 9),
        Card("3", "Clubs", 3)
    ]
    effective_tc = game.get_effective_top_card()
    assert effective_tc is not None
    assert effective_tc.rank == "9"
    # test it returns top card
    game.discard_pile = [
        Card("9", "Hearts", 9)
    ]
    top_card = game.get_effective_top_card()
    assert top_card.rank == "9"