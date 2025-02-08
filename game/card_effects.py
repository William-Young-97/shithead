from abc import ABC, abstractmethod

class CardEffects(ABC):
    @abstractmethod
    def apply(self, game):
        pass

class TenEffect(CardEffects):
    def apply(self, game):
        game.discard_pile.clear()