from game.game import Game

def test_init():
    game = Game()
    assert isinstance(game, Game)
    