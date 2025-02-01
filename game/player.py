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