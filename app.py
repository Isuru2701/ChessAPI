import chess
from flask import Flask, request
import json

#custom libraries
from Game import Game
from firebaseConfig.firebaseConfig import Database



app = Flask(__name__)

db = Database()

@app.route('/api/')
def start():  # put application's code here
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


def verify(json):
    """extract the id and token from the json and verify with firebase"""
    pass



if __name__ == '__main__':
    app.run(debug=True)
