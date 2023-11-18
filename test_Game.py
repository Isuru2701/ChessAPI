from Game import Game
from firebaseConfig.firebaseConfig import Record
def test_get_moves():
    game = Game(1000)


def test_exists():
    db = Record()
    print(db.exists(2, "999898"))