from game.card import Card

def test_init_normal_card():
    card = Card("Ace", "Spades", 14)
    assert card.rank == "Ace"
    assert card.suit == "Spades"
    assert card.value == 14

def test_init_special_card():
    card = Card("Ten", "Spades", 10, True)
    assert card.special == True