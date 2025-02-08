from game.card_effects import TenEffect, SevenEffect, ThreeEffect

def get_card_effect(rank: str):
    mapping = {
        "10": TenEffect,
        "7": SevenEffect,
        "3": ThreeEffect,
    }
    effect_class = mapping.get(rank)
    return effect_class() if effect_class is not None else None