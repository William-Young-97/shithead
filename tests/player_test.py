from game.player import Player

def test_init():
    player = Player()
    
    assert isinstance(player, Player)
    assert player.face_down_cards == []
    assert player.face_up_cards == []
    assert player.hand == []

