import pytest
from game.card import Card
from game.player import HumanPlayer
from game.game import Game

# A helper that returns predetermined inputs.
def fake_input_sequence(responses):
    responses_iter = iter(responses)
    def inner(prompt):
        return str(next(responses_iter))
    return inner

# A fake output function that collects messages.
def fake_output(message):
    fake_output.captured.append(message)
# Initialize a list to hold captured messages.
fake_output.captured = []

def test_invalid_play_returns_to_loop_and_picks_up_discard():
    # Create a game with fake input/output.
    game = Game(input_fn=fake_input_sequence(["Alice", "0"]), output_fn=fake_output)
    
    # Set up the game's discard pile with a card of value 8.
    game.discard_pile = [Card("8", "Spades", 8)]
    
    # Get the human player.
    player = game.players[0]
    
    # Set up the player's hand with a card of value 7 (which is too low).
    player.hand = [Card("7", "Hearts", 7)]
    
    # Expect the play to raise a ValueError.
    with pytest.raises(ValueError) as excinfo:
        player.play_card(game)
    
    # Verify the error message is as expected.
    assert "Invalid move: card value too low" in str(excinfo.value)
    
    # Now simulate the game handling the invalid move.
    # (In your game loop, this would be done in the exception handler.)
    game._handle_no_valid_moves(player)
    
    # After handling, the discard pile should be picked up by the player and be empty.
    assert len(game.discard_pile) == 0
    # In this example, the player's hand should now contain the original card plus the discarded card.
    # (Initially hand had 1 card and discard pile had 1 card, so hand should now have 2.)
    assert len(player.hand) == 2
    
    # Also, verify that an appropriate error message was printed to output.
    # For example, the output might contain "Invalid move:" or similar.
    assert any("Invalid move:" in msg for msg in fake_output.captured)
