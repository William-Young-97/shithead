from game.deck import Deck
from game.card import Card

def test_deck_create():
    deck = Deck().create()

    assert len(deck.cards) == 52
    assert isinstance(deck.cards[0], Card)