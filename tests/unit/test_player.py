from game.player import Player, HumanPlayer
from game.card import Card
from game.deck import Deck
from game.game import Game
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

def test_user_play_card():
    deck = Deck()
    game = Game(deck)
    
    card = Card("8", "Diamonds", 8)

    game.current_player.hand = [card]
    print(game.players[0].get_visible_state())
    with patch("builtins.input", return_value="0"):
        game.current_player.play_card(game.discard_pile)

    assert len(game.current_player.hand) == 0
    assert game.pile[-1] == card



# helpers
# def deal_cards_in_order(deck, players):
#     for player in players:
#         for _ in range(3):
#             player.face_down_cards.append(deck.cards.pop())
#         for _ in range(3):
#             player.face_up_cards.append(deck.cards.pop())
#         for _ in range(3):
#             player.hand.append(deck.cards.pop())