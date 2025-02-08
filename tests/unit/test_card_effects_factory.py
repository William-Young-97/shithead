from game.card_effects import TenEffect
from game.card_effect_factory import get_card_effect

def test_get_card_effect_returns_ten_effect_for_10():
    effect = get_card_effect("10")
    assert effect is not None, "Expected an effect instance for rank '10'"
    assert isinstance(effect, TenEffect), "Expected an instance of TenEffect for rank '10'"

def test_get_card_effect_returns_none_for_non_special():
    effect = get_card_effect("6")
    assert effect is None, "Expected None for a non-special rank like '6'"