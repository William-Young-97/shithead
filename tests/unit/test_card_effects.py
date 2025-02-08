from game.card import Card
from game.game import Game
from tests.helpers import fake_input_sequence


def test_ten_clears_discard_pile():
    game = Game(input_fn=fake_input_sequence(["Bob", "0"]))
    game.discard_pile = [Card("Jack", "Clubs", 11)]
    player = game.players[0]
    player.hand = [Card("10", "Clubs", 10)]
    player.select_action(game)
    assert len(game.discard_pile) == 0

def test_seven_reverses_order_of_play():
    game = Game(input_fn=fake_input_sequence(["Bob", "0"]))
    game.discard_pile = [Card("5", "Clubs", 5)]
    player = game.players[0]
    player.hand = [Card("10", "Clubs", 10)]
    player.select_action(game)