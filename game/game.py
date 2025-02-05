from typing import List
from game.deck import Deck
from game.player import Player, HumanPlayer, AIPlayer
from game.card import Card

class Game:
    def __init__(self, num_players: int = 2):
        self.deck = Deck()
        self.discard_pile: List[Card] = []
        self.players: List[Player] = []
        self.current_player_index = 0
        self._initialize_players(num_players)
    
    def _initialize_players(self, num_players: int):
        self.players.append(HumanPlayer())
        for _ in range(num_players - 1):
            self.players.append(AIPlayer())
        
        for player in self.players:
            print(f"Player {player.get_name()} has joined the game!")
    
    def start(self):
        self.deck.shuffle()
        self._deal_cards()
        self._start_game_loop()
    
    def _start_game_loop(self):
        while not self._check_win_condition():
            self._play_turn()
            self._next_player()

        print(f"Game over! {self.players[self.current_player_index]} wins!")

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
        print(f"\n--- {player.name}'s turn ---")

        if self.discard_pile:
            print(f"Discard pile top card: {self.discard_pile[-1]}")
        else:
            print("Discard pile is empty.")
    
        try:
            # Attempt to play a card
            player.play_card(self.discard_pile, self.deck)
            print(f"Played card: {self.discard_pile[-1]}")
        except ValueError as e:
            # Handle invalid moves or no cards
            print(f"Invalid move: {e}")
            self._handle_no_valid_moves(player)

    def _handle_no_valid_moves(self, player: Player):
        if not self.discard_pile:
            print("Cannot pick up an empty discard pile. Drawing a card instead.")
            player.draw(self.deck.cards)
        else:
            print("Picking up the discard pile.")
            player.pickup_discard_pile(self.discard_pile)

    def _next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def _check_win_condition(self) -> bool:
        for player in self.players:
            if not player.hand and not player.face_up_cards and not player.face_down_cards:
                return True
        return False

    # helper
    def get_players(self):
        return self.players