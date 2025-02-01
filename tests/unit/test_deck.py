from game.deck import Deck
from game.card import Card

def test_create():
    deck = Deck()
    deck.create()
    print(deck.cards)

    assert len(deck.cards) == 52
    assert isinstance(deck.cards[0], Card)

def test_shuffle():
    deck = Deck()
    deck.create()
    original_order = deck.cards.copy()
    
    deck.shuffle()
    shuffled_order = deck.cards.copy()

    assert original_order != shuffled_order, "Shuffle should change the deck order"