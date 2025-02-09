from game.game_controller import GameController
from game.player import HumanPlayer
from game.card import Card

# Helper: Fake input sequence that returns predetermined responses.
def fake_input_sequence(responses):
    responses_iter = iter(responses)
    def inner(prompt):
        return str(next(responses_iter))
    return inner

# Helper: Output capturer as a callable object.
class OutputCapture:
    def __init__(self):
        self.messages = []
    def __call__(self, message):
        self.messages.append(message)
    def get(self):
        return self.messages

# Test for _format_source.
def test_format_source():
    # Create a list of sample cards.
    cards = [Card("A", "Spades", 14), Card("K", "Hearts", 13)]
    # Create a dummy controller (the game parameter isn't used in _format_source).
    controller = GameController(game=None)
    formatted = controller._format_source(cards)
    expected = [str(card) for card in cards]
    assert formatted == expected

# Test that prompt_player_action returns 'p' when the user types 'p'
def test_prompt_player_action_pickup():
    # Create a dummy HumanPlayer with a non-empty hand.
    player = HumanPlayer(input_fn=fake_input_sequence(["p"]), output_fn=lambda x: None)
    player.hand = [Card("5", "Clubs", 5)]
    # Create a dummy controller.
    controller = GameController(game=None, input_fn=fake_input_sequence(["p"]), output_fn=lambda x: None)
    result = controller.prompt_player_action(player)
    assert result == 'p'

# Test that prompt_player_action returns a valid integer index when the input is numeric.
def test_prompt_player_action_valid():
    player = HumanPlayer(input_fn=fake_input_sequence(["0"]), output_fn=lambda x: None)
    player.hand = [Card("5", "Clubs", 5)]
    controller = GameController(game=None, input_fn=fake_input_sequence(["0"]), output_fn=lambda x: None)
    result = controller.prompt_player_action(player)
    assert result == 0

# Test that prompt_player_action reprompts on invalid input, then returns a valid selection.
def test_prompt_player_action_invalid_then_valid():
    out_cap = OutputCapture()
    # The input sequence: first invalid ("abc"), then valid ("1").
    player = HumanPlayer(input_fn=fake_input_sequence(["abc", "1"]), output_fn=out_cap)
    # Ensure the player has at least two cards in hand.
    player.hand = [Card("5", "Clubs", 5), Card("K", "Hearts", 13)]
    controller = GameController(game=None, input_fn=fake_input_sequence(["abc", "1"]), output_fn=out_cap)
    result = controller.prompt_player_action(player)
    assert result == 1
    messages = out_cap.get()
    # Verify that at least one message mentions invalid input.
    assert any("Invalid input" in msg for msg in messages)

# Test that run() outputs a welcome message and calls the game's start() method.
class DummyGame:
    def __init__(self):
        self.started = False
    def start(self):
        self.started = True

def test_run_calls_game_start():
    dummy_game = DummyGame()
    out_cap = OutputCapture()
    # No input is needed for this test.
    controller = GameController(dummy_game, input_fn=fake_input_sequence([]), output_fn=out_cap)
    controller.run()
    messages = out_cap.get()
    # Check that the first message is the welcome message.
    assert messages[0] == "Welcome to the game!"
    # Ensure that the game's start method was called.
    assert dummy_game.started is True
