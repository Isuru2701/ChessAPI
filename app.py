import chess
from flask import Flask, request, g
import json

#custom libraries
from Game import Game
from firebaseConfig.firebaseConfig import Record



app = Flask(__name__)



@app.route('/api/')
def start():  # put application's code here
    db = Record()
    elo = request.args.get('elo')
    if elo is None or not elo.isnumeric():
        elo = 1200 ##default elo

    id, token = db.initialize(elo)
    game = Game(int(elo))

    return json.dumps(
        {
            "id" : id,
            "elo": elo,
            "token" : token
        }
    )

@app.route('/api/', methods=["POST"])
def move():
    pass


def verify(id, token):
    """id and token verified with firebase"""
    db = Record()
    return db.exists(id, token)


if __name__ == '__main__':
    app.run(debug=True)
