from game.player import Player

def test_init():
    player = Player()
    assert isinstance(player, Player)