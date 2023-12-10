import firebase_admin
from firebase_admin import credentials, db, exceptions
import secrets
from Game import Game
import time
import os
import json


class Database:

    def __init__(self):
        self.__game = None  # a reference to the database's entry
        self.__url = "https://chess-13669-default-rtdb.asia-southeast1.firebasedatabase.app/"

        # passing credentials as an environment variable
        try:
            cert = os.getenv("FIREBASE_CONFIG")
            print(cert)
            cert = json.loads(cert)
            print(cert)
            cred = credentials.Certificate(cert)
            try:
                firebase_admin.initialize_app(cred, {
                    "databaseURL": self.__url
                })
            except ValueError:
                print("An error occurred. Are you connected to the internet?")

        except IOError:
            print("Config file not found or is invalid. Please check your directory again")

    def getLastGameId(self) -> int:
        """
        Fetches the last GAME ID. Increment this by 1 to get the game ID for a new game.
        :return: last game ID
        """
        try:
            # Make a new game index.
            games = db.reference("games").get()

            # Convert 'id' to int, filtering out invalid entries
            ids = [int(game['id']) for game in games if
                   game is not None and 'id' in game and isinstance(game['id'], (int, str))]

            # Check if the ids list is empty
            if not ids:
                print('No valid games found')
                return 0

            return max(ids)

        except exceptions.FirebaseError:
            print('An error occurred. Are you connected to the internet?')
            return 0

    def initialize(self, id, token, elo, sn):

        try:
            print(id)
            self.__game = db.reference("games").child(str(id))
            self.__game.child("id").set(id)
            self.__game.child("elo").set(elo)
            self.__game.child("token").set(token)
            self.__game.child("board").set("")
            self.__game.child("robot").set(sn)  # store the robot's sn as well

        except exceptions.FirebaseError:
            return "An error occurred. database.initialize()"

    def writeMove(self, move, board):
        """
        Writes the move to the database
        :param move: Send the move as a SAN string (e.g. e4, Nf3, etc.)
        :param board: Send the board representation as a FEN string
        :return:
        """
        self.__game.child("moves").child().set(move)
        self.__game.child("board").set(board)

    def exists(self, id, token):
        games = db.reference("games").get()
        ids = [int(game['id']) for game in games if
               game is not None and 'id' in game and isinstance(game['id'], (int, str))]
        id = int(id)
        if id in ids:
            details = db.reference("games").child(str(id)).get()
            if token == details["token"]:
                return True

        return False

    def loadBoard(self, id, token) -> str:
        """

        :param id:
        :param token:
        :return: board's FEN
        """

        if self.exists(id, token):
            return str(db.reference("games").child(str(id)).child("board").get())

    def writeBoard(self, id, token, board) -> bool:
        """

        :param id:
        :param token:
        :param board: board representation as FEN
        :return: True if successful, False if failed
        """
        if self.exists(id, token):
            db.reference("games").child(str(id)).child("board").set(board)
            return True
        return False

    def loadGame(self, id, token) -> Game | None:
        """
        Load the Game from the database
        :param id:
        :param token:
        :return: Game if present, None if not
        """

        if self.exists(id, token):
            game = db.reference("games").child(str(id)).get()
            return {"elo": game["elo"], "board": str(game["board"])}

        return None

    def updateGame(self, id, token, gamefen, move):
        """
        Updates the game in the database
        :param id:
        :param token:
        :param game:
        :return:
        """
        if self.exists(id, token):
            self.__game = db.reference("games").child(str(id))
            self.__game.child("board").set(str(gamefen))

    def updateRobotStatus(self, sn, status):
        """
        update robotSerialNumber Online status in database
        with current time
        """
        last_request_time = time.time()

        db.reference("robots").child(str(sn)).update({"lastOnline": str(last_request_time)})
        db.reference("robots").child(str(sn)).update({"status": str(status)})

    def checkRobotOnline(self, sn):
        """
        validate the RobotSerialNumber is Online, if Not set it Offline and return status[online\offline]
        STATES: STANDBY, PLAYING, OFFLINE
        """
        currentTime = time.time()
        lastOnlineTime = db.reference("robots").child(sn).child("lastOnline").get()
        currentStatus = db.reference("robots").child(sn).child("status").get()
        if lastOnlineTime is not None:
            lastOnlineTime = float(lastOnlineTime)
            if ((
                    currentTime - lastOnlineTime) < 120.00 and currentStatus == "standby"):  # adjust seconds for 5.00 to increase accuracy
                db.reference("robots").child(str(sn)).update({"game": None}) # If on standby, clear previously tied game IDs
                return "available"
            else:
                # set offline
                db.reference("robots").child(str(sn)).update({"status": str("offline")})
                return "offline or in use"
        else:
            # no such robot serial saved in firebase
            return "offline : Robot Not found"

    def getRobotStatus(self, sn):
        """
        get robot status from firebase
        """
        return db.reference("robots").child(sn).child("status").get()

    def setRobotGame(self, sn, id):
        """
        set robot game in firebase. Establishes sort of a foreign key between game <-> robot
        IMPORTANT: Call this method after a game ends with id=None to clear the old game.
        :param id: game id
        :return:
        """

        db.reference("robots").child(str(sn)).update({"game": str(id)})

    def getRobotGame(self, sn):
        """
        get robot game from firebase
        """
        return db.reference("robots").child(sn).child("game").get()

    def stageRobot(self,sn, json):

        """
        if a robot is requested for a game, add them to the staging area with the initial json
        :param sn:
        :return:
        """
        db.reference("stagingArea").child(str(sn)).set(json)


    def destageRobot(self, sn):

        db.reference("stagingArea").child(str(sn)).delete()

    def getStagedRobots(self):

        return db.reference("stagingArea").get()

    def getRobotJson(self, sn):
        return db.reference("robots").child(str(sn)).get()
