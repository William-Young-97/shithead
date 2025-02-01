from game.card import card

def test_card_creation():
    card = Card("Ace", "Spades", 14)
    assert card.rank == "Ace"
    assert card.suit == "Spades"
    assert card.calue == 14