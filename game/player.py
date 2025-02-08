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

    def select_action(self, game):
        current_source = self.current_source
        if not current_source:
            raise ValueError("No cards available to play")

        choice = self._select_card_or_pickup(game)
        if choice == 'p':
            self.pickup_discard_pile(game)
        else:
            self._play_card(game, choice)

    def _play_card(self, game, choice):
        current_source = self.current_source
        self._validate_choice(current_source, choice)
        candidate = current_source[choice]

        # Reveal face-down card if applicable.
        if current_source is self.face_down_cards:
            self.output_fn(f"Revealed face-down card: {candidate}")

        # Special handling for 2's.
        if candidate.rank == "2":
            return self._handle_two(game, choice)

        # Validate normal moves.
        if not get_card_effect(candidate.rank):
            self._validate_normal_move(game, candidate)

        # Process the card and apply any effect.
        played_card = current_source.pop(choice)
        game.discard_pile.append(played_card)
        _ = self._apply_effect_if_any(game, candidate)

        self._refill_hand(game.deck)
        return played_card

    def _refill_hand(self, deck):
        if self.hand and len(self.hand) < 3 and deck.cards:
            while len(self.hand) < 3 and deck.cards:
                self.hand.append(deck.cards.pop())

    def get_name(self):
        # Must be implemented in subclasses.
        raise NotImplementedError

    def _select_card_or_pickup(self, game) -> int:
        # Must be implemented in subclasses.
        raise NotImplementedError

    def draw(self, deck):
        """Draw a card from the deck"""
        if deck:
            self.hand.append(deck.pop())

    def pickup_discard_pile(self, game):
        """Pick up the entire discard pile"""
        self.hand.extend(game.discard_pile)
        game._clear_discard_pile()
        self.output_fn(f"{self.name} picked up the discard pile!")

    # Accessors for testability
    def get_face_down_cards(self):
        return self.face_down_cards.copy()

    def get_face_up_cards(self):
        return self.face_up_cards.copy()

    def get_hand(self):
        return self.hand.copy()

    def _validate_choice(self, current_source, choice):
        if current_source is None or len(current_source) == 0:
            raise ValueError("No cards available to play")
        if choice < 0 or choice >= len(current_source):
            raise ValueError("Invalid selection index.")

    def _handle_two(self, game, choice):
        """Handles the logic when a '2' is played."""
        current_source = self.current_source
        played_two = current_source.pop(choice)
        game.discard_pile.append(played_two)
        self.output_fn(f"Played card: {str(game.get_actual_top_card())}")
        # If playing the two empties all sources, return it immediately.
        if not self.hand and not self.face_up_cards and not self.face_down_cards:
            return played_two
        # Otherwise, prompt the user again and recursively play the next card.
        new_choice = self._select_card_or_pickup(game)
        return self._play_card(game, new_choice)

    def _validate_normal_move(self, game, candidate):
        """Checks for invalid moves based on the current game state."""
        if not game.is_reversed and game.discard_pile and candidate.value < game.get_effective_top_card().value:
            error_msg = (
                f"Invalid move: Please play a special card, a number equal or higher than the "
                f"{game.get_effective_top_card().rank} or pickup the pile by typing 'p'."
            )
            raise ValueError(error_msg)
        if game.is_reversed and game.discard_pile and candidate.value > game.get_effective_top_card().value:
            error_msg = (
                f"Invalid move: Please play a special card, a number equal or lower than the "
                f"{game.get_effective_top_card().rank} or pickup the pile by typing 'p'."
            )
            raise ValueError(error_msg)

    def _apply_effect_if_any(self, game, candidate):
        """Retrieves and applies any special effect for the candidate card."""
        effect = get_card_effect(candidate.rank)
        if effect:
            effect.apply(game)
            # For a '3', if there's a dynamic representation, use it.
            if candidate.rank == "3" and hasattr(effect, "as_string"):
                self.output_fn(effect.as_string(game))
            else:
                self.output_fn(str(effect))
        return effect


class HumanPlayer(Player):
    def __init__(self, input_fn=input, output_fn=print):
        """
        :param input_fn: Function to handle input (default is the built-in input)
        :param output_fn: Function to handle output (default is the built-in print)
        """
        super().__init__(output_fn=output_fn)
        self.input_fn = input_fn

    def _select_card_or_pickup(self, game) -> int:
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
            user_input = self.input_fn("Enter card index (0-based) or type 'p' to pickup: ")
            if user_input.lower() == 'p':
                return 'p'
            try:
                choice = int(user_input)
                if 0 <= choice < len(self.current_source):
                    return choice
                else:
                    self.output_fn(
                        f"Invalid index. Please enter a number between 0 and {len(self.current_source) - 1}."
                        "or type 'p' to pickup the discard pile."
                    )
            except ValueError:
                self.output_fn("Invalid input. Please enter a number or p to pickup.")

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

    def _select_card_or_pickup(self, game):
        if not self.current_source:
            raise ValueError("No cards available to play")
        
        # Iterate over available cards in the current source.
        for idx, card in enumerate(self.current_source):
            try:
                # Attempt to validate the move for this card.
                self._validate_normal_move(game, card)
                # If no exception is raised, then this card is valid.
                return idx
            except ValueError:
                # If the move is invalid, skip this card.
                continue
        # If no card passes validation, return 'p' to indicate a pickup.
        return 'p'

    
    def get_visible_state(self):
        state = (
            f"Hand: {['???' for _ in self.hand]}\n\n"
            f"Face Up: {[str(c) for c in self.face_up_cards]}\n\n"
            f"Face Down: {['???' for _ in self.face_down_cards]}"
        )
        return state