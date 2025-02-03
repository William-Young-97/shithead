from game.player import Player, HumanPlayer, AIPlayer
from game.card import Card
from unittest.mock import patch


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
    assert player.hand[-1].rank == 7
# helpers
# def deal_cards_in_order(deck, players):
#     for player in players:
#         for _ in range(3):
#             player.face_down_cards.append(deck.cards.pop())
#         for _ in range(3):
#             player.face_up_cards.append(deck.cards.pop())
#         for _ in range(3):
#             player.hand.append(deck.cards.pop())