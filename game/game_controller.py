class GameController:
    def __init__(self, game, input_fn=input, output_fn=print):
        self.game = game
        self.input_fn = input_fn
        self.output_fn = output_fn

    def run(self):
        # Optionally, perform any initial UI setup.
        self.output_fn("Welcome to the game!")
        # Start the game (or your game loop).
        self.game.start()

    def prompt_player_action(self, player):
        # Here, you would call a version of select_action that doesn't do the prompting itself,
        # but instead returns a candidate move.
        # For example:
        current_source = player.current_source
        if not current_source:
            raise ValueError("No cards available to play")
        # Instead of having the player ask for input, have the controller do it:
        self.output_fn(f"Available cards: {self._format_source(current_source)}")
        raw = self.input_fn("Enter card index (0-based) or 'p' to pickup: ")
        if raw.lower() == 'p':
            return 'p'
        try:
            choice = int(raw)
            return choice
        except ValueError:
            self.output_fn("Invalid input. Try again.")
            return self.prompt_player_action(player)

    def _format_source(self, source):
        # A helper method to format the list of cards for display.
        return [str(card) for card in source]
