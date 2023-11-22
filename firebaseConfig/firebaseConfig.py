import firebase_admin
from firebase_admin import credentials, db
import secrets


class Record:

    def __init__(self):
        self.__game = None #a reference to the database's entry
        self.__url = "https://chess-13669-default-rtdb.asia-southeast1.firebasedatabase.app/"
        self.__id = 0
        self.__token = ""
        self.__moveId = 0

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




    def initialize(self, elo):

        try:
            # make a new game index.
            games = db.reference("games").get()
            ids = [game['id'] for game in games]
            self.__id = max(ids) + 1

        except:
            print('first game')

        print(self.__id)
        self.__game = db.reference("games").child(str(self.__id))
        self.__token = secrets.token_hex(16)
        self.__game.child("id").set(self.__id)
        self.__game.child("elo").set(elo)
        self.__game.child("token").set(self.__token)
        self.__game.child("board").set("")

        return self.__id, self.__token

    def writeMove(self, move, board):
        """
        Writes the move to the database
        :param move: Send the move as a SAN string (e.g. e4, Nf3, etc.)
        :param board: Send the board representation as a FEN string
        :return:
        """
        self.__game.child("moves").child(self.__moveId).set(move)
        self.__game.child("board").set(board)
        self.__moveId += 1

    def exists(self, id, token):

        ids = [game["id"] for game in db.reference("games").get()]
        if id in ids:
            details = db.reference("games").child(str(id)).get()
            if token == details["token"]:
                return True

        return False
