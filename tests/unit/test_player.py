from game.player import Player, HumanPlayer, AIPlayer
from game.card import Card
from unittest.mock import patch
import pytest


def test_init():
    player = Player()
    assert isinstance(player, Player)
    assert player.get_face_down_cards() == []
    assert player.get_face_up_cards() == []
    assert player.get_hand() == []


def test_visible_state_representation():
    # Setup player with cards
    player = HumanPlayer()
    player.hand = [Card("A", "Spades", 14), Card("2", "Hearts", 2),  Card("3", "Hearts", 3)]
    player.face_up_cards = [Card("10", "Diamonds", 10), Card("10", "Clubs", 10), Card("10", "Spades", 10)]
    player.face_down_cards = [Card("5", "Clubs", 5), Card("5", "Diamonds", 5), Card("5", "Hearts", 5)]

    # Get formatted output
    visible = player.get_visible_state()
    
    # Verify visible cards
    assert visible["hand"] == ["A♠", "2♥", "3♥"]
    assert visible["face_up"] == ["10♦", "10♣", "10♠"]
    assert visible["face_down"] == ["???", "???", "???"]

def test_human_player_play_card():
    player = HumanPlayer()
    player.hand = [Card("8", "Diamonds", 8), Card("2", "Spades", 2)]
    discard_pile = [Card("7", "Hearts", 7)]
    
    with patch("builtins.input", return_value="0"):  # Mock input
        player.play_card(discard_pile)
    
    assert len(player.hand) == 1
    assert discard_pile[-1].rank == "8"

def test_ai_player_play_card():
    player = AIPlayer()
    player.hand = [Card("8", "Diamonds", 8), Card("2", "Spades", 2)]
    discard_pile = [Card("7", "Hearts", 7)]
    
    player.play_card(discard_pile)
    
    assert len(player.hand) == 1
    assert discard_pile[-1].rank == "8"

def test_player_draw_card():
    player = Player()
    player.hand = [Card("8", "Diamonds", 8), Card("2", "Spades", 2)]
    deck = [Card("7", "Hearts", 7)]

    player.draw(deck)

    assert len(player.hand) == 3
    assert player.hand[-1].rank == "7"

def test_pickup_discard_pile():
    player = Player()
    player.hand = [Card("8", "Diamonds", 8), Card("4", "Spades", 4)]
    discard_pile = [Card("9", "Hearts", 9)]
    player.pickup_discard_pile(discard_pile)

    assert len(player.hand) == 3
    assert player.hand[-1].rank == "9"

def test_source_transitions():
    player = Player()
    
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

def test_play_from_different_sources():
    player = HumanPlayer()
    discard = []
    
    # Test hand play
    player.hand = [Card("5", "Spades", 5)]
    with patch("builtins.input", return_value="0"):
        player.play_card(discard)
    assert len(player.hand) == 0
    assert discard[-1].rank == "5"
    
    # Test face-up play
    player.face_up_cards = [Card("6", "Hearts", 6)]
    with patch("builtins.input", return_value="0"):
        player.play_card(discard)
    assert len(player.face_up_cards) == 0
    assert discard[-1].rank == "6"
    
    # Test face-down play
    player.face_down_cards = [Card("7", "Diamonds", 7)]
    with patch("builtins.input", return_value="0"):
        player.play_card(discard)
    assert len(player.face_down_cards) == 0
    assert discard[-1].rank == "7"

def test_invalid_play_handling():
    player = AIPlayer()
    discard = [Card("8", "Spades", 8)]
    
    # Test invalid move with proper validation
    player.hand = [Card("7", "Hearts", 7)]
    with pytest.raises(ValueError):
        player.play_card(discard)

def test_current_source_edge_cases():
    player = Player()
    
    # Empty state
    assert player.current_source is None
    
    # Only face-down remaining
    player.face_down_cards = [Card("5", "Clubs", 5)]
    assert player.current_source == player.face_down_cards

def test_face_down_revelation(capsys):
    player = HumanPlayer()
    player.face_down_cards = [Card("J", "Spades", 11)]
    discard = []
    
    with patch("builtins.input", return_value="0"):
        # Bypass validation and force valid move
        player._is_valid_move = lambda *args: True
        player.play_card(discard)
    
    captured = capsys.readouterr()
    # Check both messages in output
    assert "Select from face-down cards: ['???']" in captured.out
    assert "Revealed face-down card: J♠" in captured.out