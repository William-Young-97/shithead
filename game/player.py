class Player:
    def __init__(self) -> None:
        self.face_down_cards = []
        self.face_up_cards = []
        self.hand = []

    
    def get_face_down_cards(self):
        return self.face_down_cards
    
    def get_face_up_cards(self):
        return self.face_up_cards
    
    def get_hand(self):
        return self.hand
    
    def play_card(self, discard_pile):
        if not self.hand:
            raise ValueError("No cards in hand to play")
        
        selected_card = self._select_card()
        if self._is_valid_move(selected_card, discard_pile):
            discard_pile.append(selected_card)
            self.hand.remove(selected_card)
        else:
            raise ValueError("Invalid move: Card cannot be played")
        
    def _select_card(self):
        raise NotImplementedError("Subclasses must implement _select_card")

    # will have to edit this logic for special cards later
    def _is_valid_move(self, card, discard_pile):
        if not discard_pile:
            return True
        top_card = discard_pile[-1]
        return card.value >= top_card.value
    
    def draw(self, deck):
        self.hand.append(deck.pop())

class HumanPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
    
    def get_visible_state(self) -> dict:
        return {
            "hand": [str(card) for card in self.hand],
            "face_up": [str(card) for card in self.face_up_cards],
            "face_down": ["?" * 3 for _ in self.face_down_cards]
        }
    
    def _select_card(self):
        """Get input from the user."""
        print("Your hand:", [str(card) for card in self.hand])
        choice = int(input("Select a card (0 to 3): "))
        return self.hand[choice]

class AIPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
    
    def _select_card(self):
        """AI logic to choose a card."""
        # Example: Play the first valid card
        for card in self.hand:
            return card