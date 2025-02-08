from game.card_effects import TenEffect

def get_card_effect(rank: str):
    mapping = {
        "10": TenEffect
    }
    effect_class = mapping.get(rank)
    return effect_class() if effect_class is not None else None