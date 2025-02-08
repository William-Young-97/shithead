from game.player import Player, HumanPlayer, AIPlayer
from game.card import Card
from game.game import Game
from unittest.mock import patch
import pytest
from tests.helpers import fake_input_sequence, fake_output

# Finish reimplementing game across play_hand()

def test_init():
    player = Player(output_fn=fake_output)
    assert isinstance(player, Player)
    assert player.get_face_down_cards() == []
    assert player.get_face_up_cards() == []
    assert player.get_hand() == []

def test_visible_state_representation():
    # Setup player with cards
    player = HumanPlayer(input_fn=fake_input_sequence(["Bob"]), output_fn=fake_output)
    player.hand = [Card("A", "Spades", 14), Card("2", "Hearts", 2), Card("3", "Hearts", 3)]
    player.face_up_cards = [Card("10", "Diamonds", 10), Card("10", "Clubs", 10), Card("10", "Spades", 10)]
    player.face_down_cards = [Card("5", "Clubs", 5), Card("5", "Diamonds", 5), Card("5", "Hearts", 5)]
    
    # Get the multiline string output
    visible = player.get_visible_state()
    
    # Define the expected multiline string (note: leading/trailing whitespace is stripped)
    expected = (
        "Hand: ['A♠', '2♥', '3♥']\n\n"
        "Face Up: ['10♦', '10♣', '10♠']\n\n"
        "Face Down: ['???', '???', '???']"
    )
    
    assert visible.strip() == expected.strip()

def test_human_player_select_action_play_card():
    game = Game(input_fn=fake_input_sequence(["Alice", "0"]))
    player = game.players[0]
    player.hand = [Card("8", "Diamonds", 8), Card("2", "Spades", 2)]
    game.discard_pile = [Card("7", "Hearts", 7)]
    player.select_action(game) 
    assert len(player.hand) == 3
    assert game.discard_pile[-1].rank == "8"

def test_ai_player_select_action_play_card():
    game = Game(input_fn=fake_input_sequence(["Alice", "0"]))
    player = game.players[1]
    player.hand = [Card("8", "Diamonds", 8), Card("2", "Spades", 2)]
    game.discard_pile = [Card("7", "Hearts", 7)]

    player.select_action(game)
    
    assert len(player.hand) == 3
    assert game.discard_pile[-1].rank == "8"

def test_player_draw_card():
    player = Player(output_fn=fake_output)
    player.hand = [Card("8", "Diamonds", 8), Card("2", "Spades", 2)]
    deck = [Card("7", "Hearts", 7)]

    player.draw(deck)

    assert len(player.hand) == 3
    assert player.hand[-1].rank == "7"

def test_pickup_discard_pile():
    game = Game(input_fn=fake_input_sequence(["Alice"]))
    player = game.players[0]
    player.hand = [Card("8", "Diamonds", 8), Card("4", "Spades", 4)]
    game.discard_pile = [Card("9", "Hearts", 9)]
    player.pickup_discard_pile(game)

    assert len(player.hand) == 3
    assert player.hand[-1].rank == "9"

def test_source_transitions():
    player = Player(output_fn=fake_output)
    
    # Initial state - no cards
    assert player.current_source is None
    
    # Add face-down cards
    player.face_down_cards = [Card("2", "Hearts", 2)]
    assert player.current_source == player.face_down_cards
    
    # Add face-up cards
    player.face_up_cards = [Card("3", "Diamonds", 3)]
    assert player.current_source == player.face_up_cards
    
    # Add hand cards
    player.hand = [Card("4", "Clubs", 4)]
    assert player.current_source == player.hand

def test_select_action_from_different_sources():
    game = Game(input_fn=fake_input_sequence(["Alice", "0", "0", "0"]))
    game.deck = []
    game.discard_pile = []
    player = game.players[0]

    # Test hand play
    player.hand = [Card("5", "Spades", 5)]
    player.select_action(game)
    assert len(player.hand) == 0
    assert game.discard_pile[-1].rank == "5"
    
    # Test face-up play
    player.face_up_cards = [Card("6", "Hearts", 6)]
    player.select_action(game)
    assert len(player.face_up_cards) == 0
    assert game.discard_pile[-1].rank == "6"
    
    # Test face-down play
    player.face_down_cards = [Card("7", "Diamonds", 7)]
    player.select_action(game)
    assert len(player.face_down_cards) == 0
    assert game.discard_pile[-1].rank == "7"

def test_invalid_play_handling():
    game = Game(input_fn=fake_input_sequence(["Alice", "0"]))
    game.deck = [Card("8", "Spades", 8), Card("8", "Spades", 8)]
    game.discard_pile = [Card("8", "Spades", 8)]
    player = game.players[0]

    # Test invalid move with proper validation
    player.hand = [Card("6", "Hearts", 6)]
    with pytest.raises(ValueError):
        player.select_action(game)

def test_current_source_edge_cases():
    player = Player(output_fn=fake_output)
    
    # Empty state
    assert player.current_source is None
    
    # Only face-down remaining
    player.face_down_cards = [Card("5", "Clubs", 5)]
    assert player.current_source == player.face_down_cards

def test_face_down_revelation():
    captured_messages = []

    def fake_output(message):
        captured_messages.append(message)

    
    game = Game(input_fn=fake_input_sequence(["Alice", "0"]), output_fn=fake_output)
    game.discard_pile = []
    game.deck = []
    player = game.players[0]
    player.face_down_cards = [Card("J", "Spades", 11)]

    player._move = lambda *args: True
    player.select_action(game)

    # Now assert on the messages collected.
    assert any("Select from face-down cards: ['???']" in msg for msg in captured_messages)
    assert any("Revealed face-down card: J♠" in msg for msg in captured_messages)


def test_human_player_get_name():
    player = HumanPlayer(input_fn=fake_input_sequence(["Bob"]), output_fn=fake_output)

    assert player.get_name() == "Bob"
    assert player.name == "Bob"

def test_ai_player_get_name():
    player = AIPlayer(output_fn=fake_output)
    
    with patch("random.choice", return_value="Bob"):
        assert player.get_name() == "Bob"
        assert player.name == "Bob" 