from flask import Flask, request, session
import json
import secrets
#from flask_cors import CORS


#custom libraries
from Game import Game
from firebaseConfig.firebaseConfig import Database


app = Flask(__name__)   

#CORS(app)

@app.route('/api/games/',  methods=["POST"])
def start():
    """
    Initialize a game
    Validate SerialNumber
    Set SerialNumber Robot Status for gaming
    Setup Firebase, generate ID, generate token
    Return id, token, and elo
    :return:
    """
    global last_request_time
    db = Database()

    # Assume the request contains JSON data
    data = request.get_json()

    """============== Validations =============="""
    # Validate serial number: is the robot online?
    sn = data.get('sn')
    if sn:
        if db.checkRobotOnline(str(sn)) != "available":
            # Return current ID and token for monitoring the current game
            return db.checkRobotOnline(str(sn))  # This returns an error message

    # Else: start a normal app game (app vs engine)
    elo = data.get('elo')
    if elo is None or not str(elo).isnumeric():
        elo = 1200  # Default elo

    player = data.get('player')
    if player is not None:
        # Generate ID
        id = db.getLastGameId() + 1
        print(id)
        # Generate token
        token = secrets.token_hex(16)
        db.initialize(id, token, elo)
        if player == "white":
            return json.dumps(
                {
                    "id": id,
                    "token": token,
                    "elo": elo,
                    "move": "send your first move to api/games/play"
                }
            )
        elif player == "black":
            NewGame = Game(elo, board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")#initialize the fen
            move = NewGame.makeMove()
            print(NewGame.getBoard())
            db.updateGame(id, token, NewGame.getBoard())
            return json.dumps(
                {
                    "id": id,
                    "token": token,
                    "elo": elo,
                    "move": move
                }
            )
    else:
        return "please select player color"
    """========================================="""


@app.route('/api/games/play', methods=["POST"]) #confirmly gets a move in request object
def move():
    """
    Make user move and make AI's move.
    If the game is over by move, return winner.
    If not, return AI move.
    """

    data = request.get_json()  # Get JSON data from the request

    # Assuming your JSON payload has keys: "id", "token", "move"
    game_id = data.get("id")
    token = data.get("token")
    user_move = data.get("move")

    db = Database()
    game = db.loadGame(game_id, token)  # Loading game from database using id and token
    # Set up Game object, passing the elo with board situation
    currentGame = Game(int(game["elo"]), str(game["board"]))
    ai_move = currentGame.makeMove(user_move)  # Updating the game instance
    db.updateGame(game_id, token, currentGame.getBoard())  #Updating the database

    # Check for game over
    if currentGame.checkForGameOver() == "CHECKMATE":
        return json.dumps({"result": "PLAYER_WINS"})

    # if the game isnt over, return ai move in a json object
    return json.dumps({"result": "AI_MOVE", "move": ai_move})

@app.route('/api/games/board/monitor', methods=["POST"])
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
    app.run(debug=True)
