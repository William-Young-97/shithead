from game.deck import Deck
from game.card import Card
from game.player import Player
from game.game import Game

def test_complete_game_flow():
    deck = deck()
    game = Game(deck, num_players=2)
    game.start()

    while not game.winner:
        current_player = game.current_player
        playable_cards = current_player.get_playable_cards(game.pile)
        if playable_cards:
            # given this relies on user input would have to mock it
            game.current_player.play_card()
        else:
            game.current_player.pickup_pile()
    
    assert game.winner is not None
    # also assert winners has no cards in any slot