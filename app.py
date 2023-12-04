
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
    validate serialNumber 
    set SerialNumber Robot Status for gaming
    setup firebase, generate ID, generate token
    return id, token, and elo
    :return:
    """
    global last_request_time
    db = Database()
    elo = request.args.get('elo')
    sn = request.args.get('sn')
    player = request.args.get('player')

    """============== validations =============="""
    # validate serial number .. is robot online ? 
    if sn is not None:
        if db.checkRobotOnline(str(sn)) != "online":
            return "Robot offline please try again!"
    #else : start a normal app game
    
    if elo is None or not elo.isnumeric():
        elo = 1200 # default elo

    if player is not None:
        proceedOperations = 1 #TODO: delete this line and do proceedings of flag
    else:
        return "please select player color"         
    """========================================="""

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
    pass


@app.route('/api/games/board', methods=["POST"])
def getBoard():
    db = Database()
    game = db.loadGame(request.form["id"], request.form["token"])
    if game is not None:
        return game.getBoard()

    return "Game not found"
 

@app.route('/api/robots', methods=["POST"])
def get_robot_status():
    # Ensure the request has a json object
    if not request.is_json:
        return "Invalid JSON request", 400

    json_data = request.get_json()
    db = Database()
    sn = json_data["sn"]
    status = json_data["status"]

    db.updateRobotStatus(sn, status)
    return "robot updated Successfull"


if __name__ == '__main__':
    app.run(debug=True, load_dotenv=True)
