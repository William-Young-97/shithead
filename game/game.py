from typing import List
from game.deck import Deck
from game.player import Player, HumanPlayer, AIPlayer
from game.card import Card

class Game:
    def __init__(self, num_players: int = 2, input_fn=input, output_fn=print):
        self.deck = Deck()
        self.discard_pile: List[Card] = []
        self.players: List[Player] = []
        self.current_player_index = 0
        self.input_fn = input_fn
        self.output_fn = output_fn
        self._initialize_players(num_players, input_fn, output_fn)
    
    def _initialize_players(self, num_players: int, input_fn, output_fn):
        # Create a HumanPlayer with the provided input/output functions.
        self.players.append(HumanPlayer(input_fn=input_fn, output_fn=output_fn))
        for _ in range(num_players - 1):
            self.players.append(AIPlayer(output_fn=output_fn))
        
        for player in self.players:
            output_fn(f"Player {player.get_name()} has joined the game!")
    
    def start(self):
        self.deck.shuffle()
        self._deal_cards()
        self._start_game_loop()
    
    def _start_game_loop(self):
        winner = None
        while not (winner := self._check_win_condition()):
            self._play_turn()
        self.output_fn(f"Game over! {winner.get_name()} wins!")

    def _deal_cards(self):
        for player in self.players:
            for _ in range(3):
                player.face_down_cards.append(self.deck.cards.pop())
            for _ in range(3):
                player.face_up_cards.append(self.deck.cards.pop())
            for _ in range(3):
                player.hand.append(self.deck.cards.pop())

    def _play_turn(self):
        player = self.players[self.current_player_index]
        self.output_fn(f"\n--- {player.name}'s turn ---")
        self.output_fn(f"deck remaining: {len(self.deck.cards)}\n")
        self.output_fn(player.get_visible_state())
        self.output_fn(f"----------------------------")
        if self.discard_pile:
            self.output_fn(f"Discard pile top card: {self.discard_pile[-1]}")
        else:
            self.output_fn("Discard pile is empty.")

        self.output_fn(f"----------------------------")

        try:
            player.select_action(self)
            if self.discard_pile:
                self.output_fn(f"Played card: {self.discard_pile[-1]}")
            else:
                self.output_fn("No card was played.")
            self._next_player()
        except ValueError as e:
            self.output_fn(f"Invalid move: {e}")


    def _next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def _check_win_condition(self):
        for player in self.players:
            if not player.hand and not player.face_up_cards and not player.face_down_cards:
                return player
        return None


    # helper
    def get_players(self):
        return self.players