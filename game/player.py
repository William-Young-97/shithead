import random
from game.card_effect_factory import get_card_effect
from game.card import Card

class Player:
    def __init__(self, output_fn=print) -> None:
        self.face_down_cards = []
        self.face_up_cards = []
        self.hand = []
        self.name = None
        self.output_fn = output_fn  # Injected output function

    @property
    def current_source(self):
        """Dynamically determines the active card source based on game rules"""
        if self.hand:
            return self.hand
        if self.face_up_cards:
            return self.face_up_cards
        if self.face_down_cards:
            return self.face_down_cards
        return None

    def get_visible_state(self):
        state = (
            f"Hand: {[str(c) for c in self.hand]}\n\n"
            f"Face Up: {[str(c) for c in self.face_up_cards]}\n\n"
            f"Face Down: {['???' for _ in self.face_down_cards]}"
        )
        return state

    def play_card(self, game):
        current_source = self.current_source
        if not current_source:
            raise ValueError("No cards available to play")
        
        selected_index = self._select_card()
        candidate = current_source[selected_index]  # peek without removal

        # If playing from face-down, reveal the card using the injected output function.
        if current_source is self.face_down_cards:
            self.output_fn(f"Revealed face-down card: {candidate}")

        # Validate move before removing the card.

        if game.discard_pile and candidate.value < game.discard_pile[-1].value:
            error_msg= (f"Invalid move: Please play a special card, a number equal or higher than the {game.discard_pile[-1].rank} "
"or pickup the pile by typing 'p'.")
            raise ValueError(error_msg)

        # Now the move is valid; remove and process the card.
        played_card = current_source.pop(selected_index)
        game.discard_pile.append(played_card)

        effect = get_card_effect(played_card.rank)
        if effect:
            effect.apply(game)

        self._refill_hand(game.deck)
        return played_card

    def _refill_hand(self, deck):
        if self.hand and len(self.hand) < 3 and deck.cards:
            while len(self.hand) < 3 and deck.cards:
                self.hand.append(deck.cards.pop())

    def get_name(self):
        # Must be implemented in subclasses.
        raise NotImplementedError

    def _select_card(self) -> int:
        # Must be implemented in subclasses.
        raise NotImplementedError

    def _is_valid_move(self, card, discard_pile):
        """Basic validation (extend for special cards later)"""
        if not discard_pile:
            return True
        return card.value >= discard_pile[-1].value

    def draw(self, deck):
        """Draw a card from the deck"""
        if deck:
            self.hand.append(deck.pop())

    def pickup_discard_pile(self, discard_pile):
        """Pick up the entire discard pile"""
        self.hand.extend(discard_pile)
        discard_pile.clear()

    # Accessors for testability
    def get_face_down_cards(self):
        return self.face_down_cards.copy()

    def get_face_up_cards(self):
        return self.face_up_cards.copy()

    def get_hand(self):
        return self.hand.copy()


class HumanPlayer(Player):
    def __init__(self, input_fn=input, output_fn=print):
        """
        :param input_fn: Function to handle input (default is the built-in input)
        :param output_fn: Function to handle output (default is the built-in print)
        """
        super().__init__(output_fn=output_fn)
        self.input_fn = input_fn

    def _select_card(self) -> int:
        while True:
            if self.current_source is self.hand:
                source_name = "hand"
                visible = [str(c) for c in self.current_source]
            elif self.current_source is self.face_up_cards:
                source_name = "face-up cards"
                visible = [str(c) for c in self.current_source]
            else:
                source_name = "face-down cards"
                visible = ["???" for _ in self.current_source]

            self.output_fn(f"Select from {source_name}: {visible}")
            user_input = self.input_fn("Enter card index (0-based): ")
            try:
                choice = int(user_input)
                if 0 <= choice < len(self.current_source):
                    return choice
                else:
                    self.output_fn(
                        f"Invalid index. Please enter a number between 0 and {len(self.current_source) - 1}."
                    )
            except ValueError:
                self.output_fn("Invalid input. Please enter a number.")

    def get_name(self):
        if not self.name:
            self.name = self.input_fn("Enter your name: ")
        return self.name


class AIPlayer(Player):
    def __init__(self, output_fn=print):
        super().__init__(output_fn=output_fn)
        self._names = [
            "Alice", "Bob", "Charlie", "Diana", "Eve",
            "Frank", "Grace", "Hank", "Ivy", "Jack"
        ]

    def get_name(self) -> str:
        """Generate a random name for the AI player."""
        if not self.name:  # Only generate once.
            self.name = random.choice(self._names)
        return self.name

    def _select_card(self) -> int:
        """Improved AI with basic validation"""
        if not self.current_source:
            raise ValueError("No cards available to play")
            
        # Find the first valid card.
        for idx, card in enumerate(self.current_source):
            if self._is_valid_move(card, []):  # Pass empty discard pile for now.
                return idx
        raise ValueError("No valid moves available")
    
    def get_visible_state(self):
        state = (
            f"Hand: {['???' for _ in self.hand]}\n\n"
            f"Face Up: {[str(c) for c in self.face_up_cards]}\n\n"
            f"Face Down: {['???' for _ in self.face_down_cards]}"
        )
        return state
