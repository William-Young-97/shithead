from game.card_effects import Card_effects
from game.card import Card
from game.player import HumanPlayer

def test_ten_clears_discard_pile():
    discard_pile = [Card("5", "Clubs", 5)]
    player = HumanPlayer(input_fn=fake_input_sequence(["Bob", 0]))
    player.hand = [Card("10", "Clubs", 10)]
    player.play_card()
    assert len(discard_pile) == 0
    
def fake_input_sequence(responses):
    responses_iter = iter(responses)
    def inner(prompt):
        return next(responses_iter)
    return inner