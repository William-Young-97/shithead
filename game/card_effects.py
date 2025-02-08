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