import chess
from flask import Flask
from firebaseConfig.firebaseConfig import Database
import json

app = Flask(__name__)

db = Database()

@app.route('/api/')
def start():  # put application's code here
    id, token = db.initialize()

    return json.dumps(
        {
            "id" : id,
            "token" : token
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
