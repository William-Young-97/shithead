from game.player import Player
from game.card import Card

def test_init():
    player = Player()
    assert isinstance(player, Player)
    assert player.get_face_down_cards() == []
    assert player.get_face_up_cards() == []
    assert player.get_hand() == []


def test_visible_state_representation():
    # Setup player with cards
    player = Player()
    player.hand = [Card("A", "Spades", 14), Card("2", "Hearts", 2),  Card("3", "Hearts", 3)]
    player.face_up_cards = [Card("10", "Diamonds", 10), Card("10", "Clubs", 10), Card("10", "Spades", 10)]
    player.face_down_cards = [Card("5", "Clubs", 5), Card("5", "Diamonds", 5), Card("5", "Hearts", 5)]

    # Get formatted output
    visible = player.get_visible_state()
    
    # Verify visible cards
    assert visible["hand"] == ["A♠", "2♥", "3♥"]
    assert visible["face_up"] == ["10♦", "10♣", "10♠"]
    assert visible["face_down"] == ["???", "???", "???"]