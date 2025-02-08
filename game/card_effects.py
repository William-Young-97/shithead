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
        game.discard_pile.clear()
    
    def __str__(self):
        return "The ten burned the discard pile."