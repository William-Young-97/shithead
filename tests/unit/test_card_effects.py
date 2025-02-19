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
    assert game.get_actual_top_card().rank == "3"
    assert game.get_effective_top_card().rank == "5"

def test_two_resets_and_skips():
    game = Game(input_fn=fake_input_sequence(["Bob", "0", "0"]))
    game.discard_pile = [Card("Ace", "Clubs", 14)]
    player = game.players[0]
    player.hand = [Card("2", "Clubs", 2), Card("4", "Clubs", 4)]
    player.select_action(game)
    
    assert game.get_actual_top_card().rank == "4"
    assert len(player.hand) == 0

def test_two_resets_and_skips():
    game = Game(input_fn=fake_input_sequence(["Bob", "0", "0", "0", "0", "0"]))
    game.discard_pile = [Card("Ace", "Clubs", 14)]
    player = game.players[0]
    player.hand = [Card("2", "Clubs", 2), Card("2", "Clubs", 2), Card("2", "Clubs", 2), Card("2", "Clubs", 2)]
    player.face_up_cards = [Card("Ace", "Clubs", 14)]
    player.select_action(game)

    assert len(player.hand) == 0
    assert len(player.face_up_cards) == 0
    assert game.get_actual_top_card().rank == "Ace"

def test_win_on_two_last_card():
    game = Game(input_fn=fake_input_sequence(["Alice", "0"]))
    player = game.players[0]
    player.hand = []
    player.face_up_cards = []
    player.face_down_cards = [Card("2", "Spades", 2)]
    ai = game.players[1]
    ai.hand = [Card("Ace", "Clubs", 14)]
    game._start_game_loop()
    assert player == game._check_win_condition()

def test_two_resets_and_skips():
    # cards should be drawn imidiately after being played
    game = Game(input_fn=fake_input_sequence(["Bob", "0", "0", "0", "0"]))
    game.discard_pile = []
    game.deck.cards = [Card("Ace", "Spades", 14)]
    player = game.players[0]
    player.hand = [Card("2", "Clubs", 2), Card("2", "Clubs", 2), Card("2", "Clubs", 2)]
    player.select_action(game)
    assert game.get_actual_top_card().rank == "Ace"