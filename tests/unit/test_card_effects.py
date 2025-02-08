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
    player.hand = [Card("7", "Clubs", 7)]
    player.select_action(game)
    ai = game.players[1]
    ai.hand = [Card("8", "Clubs", 8)]
    ai.select_action(game)
    assert len(ai.hand) == 3

def test_invalid_move_after_seven():
    game = Game(input_fn=fake_input_sequence(["Bob", "0"]))
    game.discard_pile = [Card("5", "Clubs", 5)]
    player = game.players[0]
    player.hand = [Card("7", "Clubs", 7)]
    player.select_action(game)
    ai = game.players[1]
    ai.hand = [Card("9", "Clubs", 9)]
    try:
        ai.select_action(game)
    except ValueError as e:
        assert "Invalid move" in str(e), "The error message should indicate an invalid move."
        assert "lower than the 7" in str(e), "The error message should mention the value constraint."

def test_three_is_invisible():
    game = Game(input_fn=fake_input_sequence(["Bob", "0"]))
    game.discard_pile = [Card("5", "Clubs", 5)]
    player = game.players[0]
    player.hand = [Card("3", "Clubs", 3)]
    player.select_action(game)
    assert game.discard_pile[-1].rank == "3"
    assert game.get_effective_top_card().rank == "5"
