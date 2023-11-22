import chess
from flask import Flask, request, session
import json

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

    id, token = db.initialize(elo)
    game = Game(int(elo))

    return json.dumps(
        {
            "id" : id,
            "token": token,
            "elo": elo

        }
    )

@app.route('/api/', methods=["POST"])
def move():
    db = Database()
    if db.exists(request.form["id"], request.form["token"]):
        move = request.form["move"]
        game =


def verify(id, token):
    """id and token verified with firebase"""
    db = Database()
    return db.exists(id, token)


if __name__ == '__main__':
    app.run(debug=True)
