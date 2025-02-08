from game.card import Card
from game.game import Game
from tests.helpers import fake_input_sequence, fake_output

def test_invalid_play_prompts_for_valid_move_or_pickup():
    game = Game(input_fn=fake_input_sequence(["Alice", "0"]), output_fn=fake_output)
    player = game.players[0]
    player.hand = [Card("6", "Hearts", 6), Card("6", "Spades", 6), Card("6", "Clubs", 6)]
    game.discard_pile = [Card("8", "Spades", 8)]

    try:
        game._play_turn()
    except ValueError as e:
        assert "Invalid move" in str(e)
        assert "higher than the" in str(e)
        assert "or pickup the pile" in str(e)

    assert len(player.hand) == 3
    assert len(game.discard_pile) == 1
    assert game.discard_pile[0].rank == "8"
    assert game.current_player_index == 0 
