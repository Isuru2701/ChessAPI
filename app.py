import chess
from flask import Flask, request

from Game import Game
from firebaseConfig.firebaseConfig import Database
import json

app = Flask(__name__)

db = Database()

@app.route('/api/')
def start():  # put application's code here
    elo = request.args.get('elo')
    id, token = db.initialize(elo)

    return json.dumps(
        {
            "id" : id,
            "elo": elo,
            "token" : token
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
