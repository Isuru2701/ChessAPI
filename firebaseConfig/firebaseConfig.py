import firebase_admin
from firebase_admin import credentials, db, exceptions
import secrets
from Game import Game
import time

class Database:

    def __init__(self):
        self.__game = None #a reference to the database's entry
        self.__url = "https://chess-13669-default-rtdb.asia-southeast1.firebasedatabase.app/"

        # Make an app in firebaseConfig > add realtime database > service accounts > generate new private key
        # Add the json file to the same directory as this file and rename it to "firebaseconfig.json"
        # This file isn't pushed to GitHub for security reasons.
        try:
            cred = credentials.Certificate(r"firebaseConfig/firebaseconfig.json")
            try:
                firebase_admin.initialize_app(cred, {
                    "databaseURL": self.__url
                })
            except ValueError:
                print("An error occurred. Are you connected to the internet?")

        except IOError | ValueError:
            print("Config file not found or is invalid. Please check your directory again")


    def getLastGameId(self) -> int:
        """
        fetches the last GAME ID. Increment this by 1 to get the game ID for a new game.
        :return: last game ID
        """
        try:
            # make a new game index.
            games = db.reference("games").get()
            ids = [game['id'] for game in games]
            return max(ids)

        except exceptions.FirebaseError:
            print('first game')
            return 0

    def getLastMoveId(self, id, token) -> int:
        """
        fetches the last MOVE ID. Increment this by 1 to get the move ID for a new move.
        :return: last game ID
        """
        try:
            # make a new game index.
            if self.exists(id, token):
                moves = db.reference("games").child(str(id)).child("moves").get()
                ids = [move for move in moves]
                return max(ids)

        except:
            print('first move')
            return 0



    def initialize(self, id, token, elo):

        try:
            print(id)
            self.__game = db.reference("games").child(str(id))
            self.__game.child("id").set(id)
            self.__game.child("elo").set(elo)
            self.__game.child("token").set(token)
            self.__game.child("board").set("")

        except exceptions.FirebaseError:
            return "An error occurred. Are you connected to the internet?"

    def writeMove(self, move, board):
        """
        Writes the move to the database
        :param move: Send the move as a SAN string (e.g. e4, Nf3, etc.)
        :param board: Send the board representation as a FEN string
        :return:
        """
        self.__game.child("moves").child().set(move)
        self.__game.child("board").set(board)
        self.__moveId += 1

    def exists(self, id, token):

        ids = [game["id"] for game in db.reference("games").get()]
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
            return Game(game["elo"], game["board"])

        return None

    def updateGame(self, id, token, game, move):
        """
        Updates the game in the database
        :param id:
        :param token:
        :param game:
        :return:
        """
        if self.exists(id, token):
            self.__game = db.reference("games").child(str(game.getId()))
        self.__game.child("board").set(game.getBoard())
        self.__game.child("moves").child(str(self.getLastMoveId(id, token)+1)).set(move)

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
        """
        currentTime = time.time()
        lastOnlineTime = db.reference("robots").child(sn).child("lastOnline").get()

        if lastOnlineTime is not None:
            lastOnlineTime = float(lastOnlineTime)
            if ((currentTime - lastOnlineTime)  < 20.00): #adjust seconds for 5.00 to increase accuracy
                return "online"
            else:
                #set offline
                db.reference("robots").child(str(sn)).update({"status": str("offline")})
                return "offline"
        else: 
            #no such robot serial saved in firebase
            return "offline"    
            
