from abc import ABC, abstractmethod

class CardEffects(ABC):
    @abstractmethod
    def apply(self, game):
        pass

    @abstractmethod
    def __str__(self):
        pass

class TenEffect(CardEffects):
    def apply(self, game):
        game._clear_discard_pile()
    
    def __str__(self):
        return "The ten burned the discard pile."
    
class SevenEffect(CardEffects):
    def apply(self, game):
        game.is_reversed = not game.is_reversed

    def __str__(self):
        return "The seven reversed the order of play!"
    
class ThreeEffect(CardEffects):
    def apply(self, game):
        pass
    
    def as_string(self, game):
        effective_top = game.get_effective_top_card()
        if effective_top:
            return f"The three takes on the rank of: {effective_top.rank}"
        else:
            return "The three has no card beneath to copy."
    
    def __str__(self):
        
        return "ThreeEffect (dynamic representation requires game context)"