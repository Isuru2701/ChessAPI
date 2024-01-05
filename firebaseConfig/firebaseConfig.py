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
            cert = json.loads(cert)
            cred = credentials.Certificate(cert)
            try:
                app = firebase_admin.initialize_app(cred, {
                    "databaseURL": self.__url
                })
            except ValueError:
                print("VALUE_ERROR: Database .__init__ app instance already exists or something else went wrong")

        except IOError:
            print("IOError: Database .__init__ Config file not found")

    def getLastGameId(self) -> int:
        """
        Fetches the last GAME ID. Increment this by 1 to get the game ID for a new game.
        :return: last game ID
        """
        try:
            # Make a new game index.
            games = db.reference("games").get()


            # Convert 'id' to int, filtering out invalid entries
            try:
                ids = [int(game['id']) for game in games if
                   game is not None and 'id' in game and isinstance(game['id'], (int, str))]
            except:
                ids = []

            # Check if the ids list is empty
            if not ids:
                print('First game')
                return 0

            return max(ids)

        except exceptions.FirebaseError:
            print('FIREBASE_ERROR Database getLastGameId()')
            return 0

    def initialize(self, id, token, elo, sn):

        try:
            print(id)
            self.__game = db.reference("games").child(str(id))
            self.__game.child("id").set(id)
            self.__game.child("elo").set(elo)
            self.__game.child("token").set(token)
            self.__game.child("board").set("")
            if sn is None: # store the robot's sn as well  | we need to handle the case when sn is None
                self.__game.child("robot").set("") 
            else:
                self.__game.child("robot").set(sn)  
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
            return Game(game["elo"], str(game["board"]))

        return None

    def updateGame(self, id, token, gamefen):
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
                    currentTime - lastOnlineTime) < 1200.00 and currentStatus == "standby"):  # adjust seconds for 5.00 to increase accuracy
                db.reference("robots").child(str(sn)).update({"game": None}) # If on standby, clear previously tied game IDs
                return "available"
            elif db.reference("robots").child(str(sn)).child('status').get() == 'staged':
                return "robot is staged for a match"
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

        robots = db.reference("stagingArea").get()
        print(robots)
        if robots is not None:
            # ids = [int(robot['robot']) for robot in robots if
            #        robot is not None and 'robot' in robot and isinstance(robot['robot'], (int, str))]
            #

            ids = []
            for robot in robots:
                print("robot: ", robot)
                ids.append(int(robot))
                print(ids)

            if isinstance(ids, list):
                print("here ",ids)
                return ids  # If it's already a list, return as is
            else:
                ids = [ids]
                print("in else", ids)
                return ids
        else:
            return None

    def getRobotJson(self, sn):
        print(db.reference("stagingArea").child(str(sn)).get())
        return db.reference("stagingArea").child(str(sn)).get()
