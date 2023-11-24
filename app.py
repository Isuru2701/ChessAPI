import chess
from flask import Flask, request, session
import json
import secrets

#custom libraries
from Game import Game
from firebaseConfig.firebaseConfig import Database



app = Flask(__name__)

@app.route('/api/')
def start():


    db = Database()
    elo = request.args.get('elo')
    if elo is None or not elo.isnumeric():
        elo = 1200 ##default elo

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

@app.route('/api/game/', methods=["POST"])
def getBoard():
    db = Database()
    game = db.loadGame(request.form["id"], request.form["token"])
    if game is not None:
        return game.getBoard()

    return "Game not found"

@app.route('/api/', methods=["POST"])
def move():
    db = Database()

    if db.exists(request.form["id"], request.form["token"]):
        game = db.loadGame(request.form["id"], request.form["token"])
        if game is not None:
            if game.isLegalMove(request.form["move"]):
                game.makeMove(request.form["move"])
                db.updateGame(game)
                return game.getBoard()
            else:
                return "Illegal move"



if __name__ == '__main__':
    app.run(debug=True)
