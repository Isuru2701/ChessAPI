import chess
from flask import Flask, request, session
import json
import secrets

#custom libraries
from Game import Game
from firebaseConfig.firebaseConfig import Database



app = Flask(__name__)

@app.route('/api/games/')
def start():

    """
    initialize a game
    setup firebase, generate ID, generate token
    return id, token, and elo
    :return:
    """

    db = Database()
    elo = request.args.get('elo')
    if elo is None or not elo.isnumeric():
        elo = 1200 # default elo

    # generate ID
    id = db.getLastGameId() + 1

    # generate token
    token = secrets.token_hex(16)

    db.initialize(id, token, elo)

    return json.dumps(
        {
            "id" : id,
            "token": token,
            "elo": elo

        }
    )

@app.route('/api/games/', methods=["POST"])
def move():
    db = Database()

    if db.exists(request.form["id"], request.form["token"]):
        game = db.loadGame(request.form["id"], request.form["token"])
        if game is not None:
            if game.isLegalMove(request.form["move"]):
                game.makeMove(request.form["move"])
                db.updateGame(request.form["id"], request.form["token"], game, request.form["move"])
                return game.getBoard()
            else:
                return "Illegal move"



@app.route('/api/games/board', methods=["POST"])
def getBoard():
    db = Database()
    game = db.loadGame(request.form["id"], request.form["token"])
    if game is not None:
        return game.getBoard()

    return "Game not found"


if __name__ == '__main__':
    app.run(debug=True)
