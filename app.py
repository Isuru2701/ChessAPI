from flask import Flask, request, session
import json
import secrets
from flask_cors import CORS

# custom libraries
from Game import Game
from firebaseConfig.firebaseConfig import Database

app = Flask(__name__)

CORS(app)


@app.route('/api/games', methods=["POST"])
def start():
    """
    Initialize a game
    Validate SerialNumber
    Set SerialNumber Robot Status for gaming
    Setup Firebase, generate ID, generate token
    Return id, token, and elo
    :return:
    """
    global last_request_time #TODO: is this needed? remove it if it isn't
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

        # setup robot for match
        if db.getRobotStatus(str(sn)) == "standby":
            db.updateRobotStatus(str(sn), "staged")

    else:
        sn = None #allow for web-client to web-client play

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
        db.initialize(id, token, elo, sn)
        if player == "white":
            reply = {
                "id": id,
                "token": token,
                "elo": elo,
                "robot": sn,
                "move": None
            }

            if sn:
                # if a robot is selected, add this json to the staging area instead
                db.stageRobot(sn, reply)

            return json.dumps(reply)

        elif player == "black":
            NewGame = Game(elo)  # initialize the fen
            move = NewGame.stockfishMove()
            print(NewGame.getBoard())
            db.updateGame(id, token, NewGame.getBoard())
            reply = {
                "id": id,
                "token": token,
                "elo": elo,
                "robot": sn,
                "move": move
            }

            if sn:
                db.stageRobot(sn, reply)

            return json.dumps(reply) #return payload as well cuz the UI service needs the id and token as well

    else:
        return "please select player color"
    """========================================="""


@app.route('/api/games/play', methods=["POST"])  # gets a move in request object
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
    sn = data.get("sn") # needed to update robot status if game over

    db = Database()
    game = db.loadGame(game_id, token)  # Loading game from database using id and token
    # Set up Game object, passing the elo with board situation
    currentGame = Game(int(game["elo"]), str(game["board"]))

    result = currentGame.makeMove(user_move)
    db.updateGame(game_id, token, currentGame.getBoard())

    if result == "ILLEGAL_MOVE":
        return "ILLEGAL_MOVE"

    #Check if the move the user made led to a checkmate against the robot
    if currentGame.checkForGameOver() == "CHECKMATE":
        # if game over, reset robot to standby state
        db.updateRobotStatus(sn, 'standby')
        db.destageRobot(sn)
        return json.dumps({"result": "CHECKMATE", "move":None})



    ai_move = currentGame.stockfishMove()
    db.updateGame(game_id, token, currentGame.getBoard())  # Updating the database

    # Check for game over by the move the AI made
    if currentGame.checkForGameOver() == "CHECKMATE":
        # if game over, reset robot to standby state
        db.updateRobotStatus(sn, 'standby')
        db.destageRobot(sn)
        return json.dumps({"result": "CHECKMATE", "move":ai_move})

    # if the game isn't over, return AI move in a json object
    return json.dumps({"result": "AI_MOVE", "move": ai_move})


@app.route('/api/games/board', methods=["POST"])
def getBoard():

    data = request.get_json()
    id = data.get('id')
    token = data.get('token')

    db = Database()

    game = db.loadGame(id, token)
    if game is not None:
        return game.getBoard()

    return "Game not found"


@app.route('/api/robots', methods=["POST"])
def ping():
    """
    Robots send requests to this endpoint periodically to indicate that they are online
    :return:
    """

    # Ensure the request has a json object
    if not request.is_json:
        return "Invalid JSON request", 400

    json_data = request.get_json()
    db = Database()
    sn = json_data["sn"]

    # check if robot is asked for a match yet
    stagedBots = db.getStagedRobots()
    print("staged: ", stagedBots)
    if stagedBots is not None:
        if sn in db.getStagedRobots():


            # bot has accepted game. set bot to playing
            db.updateRobotStatus(sn, "playing")

            return db.getRobotJson(sn)




    db.updateRobotStatus(sn, "standby")
    return "ACK"  # Acknowledgement OK


#TODO: add endpoint for reset


if __name__ == '__main__':
    app.run(debug=True)
