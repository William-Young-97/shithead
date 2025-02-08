from game.card import Card
from game.game import Game

def test_ten_clears_discard_pile():
    game = Game(input_fn=fake_input_sequence(["Bob", "0"]))
    game.discard_pile = [Card("5", "Clubs", 5)]
    player = game.players[0]
    player.hand = [Card("10", "Clubs", 10)]
    player.select_action(game)
    assert len(game.discard_pile) == 0

def fake_input_sequence(responses):
    responses_iter = iter(responses)
    def inner(prompt):
        return next(responses_iter)
    return inner