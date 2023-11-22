import firebase_admin
from firebase_admin import credentials, db, exceptions
import secrets


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
            id = max(ids) + 1
            return id

        except exceptions.FirebaseError:
            print('first game')
            return 0

    def getLastMoveId(self, id, token) -> int:
        """
        fetches the last GAME ID. Increment this by 1 to get the game ID for a new game.
        :return: last game ID
        """
        try:
            # make a new game index.
            if self.exists(id, token):
                moves = db.reference("games").child(str(id)).child("moves").get()
                ids = [move for move in moves]
                return max(ids)
            else:
                raise

        except exceptions.FirebaseError:
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
            return

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