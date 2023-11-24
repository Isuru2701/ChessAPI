from Game import Game
from firebaseConfig.firebaseConfig import Database
def test_get_moves():
    game = Game(1000)


def test_exists():
    db = Database()
    print(db.exists(2, "999898"))


def test_loadgame():
    db = Database()
    game = db.loadGame(2, "999898")