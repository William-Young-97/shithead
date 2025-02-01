class Player:
    def __init__(self) -> None:
        self.face_down_cards = []
        self.face_up_cards = []
        self.hand = []

    # Helper methods
    def get_face_down_cards(self):
        return self.face_down_cards
    
    def get_face_up_cards(self):
        return self.face_up_cards
    
    def get_hand(self):
        return self.hand
    
class HumanPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
    
    def get_visible_state(self) -> dict:
        return {
            "hand": [str(card) for card in self.hand],
            "face_up": [str(card) for card in self.face_up_cards],
            "face_down": ["?" * 3 for _ in self.face_down_cards]
        }

class AIPlayer(Player):
    def __init__(self) -> None:
        super().__init__()