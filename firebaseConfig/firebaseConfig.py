import firebase_admin
from firebase_admin import credentials, db
import secrets


class Database:

    def __init__(self):
        self.__game = None
        self.__url = "https://chess-13669-default-rtdb.asia-southeast1.firebasedatabase.app/"
        self.__id = 0
        self.__token = ""
        self.__moveId = 0

        cred = credentials.Certificate("firebaseConfig/firebaseconfig.json")

        firebase_admin.initialize_app(cred, {
            "databaseURL": self.__url
        })

    def initialize(self):
        # Make an app in firebaseConfig > add realtime database > service accounts > generate new private key
        # Add the json file to the same directory as this file and rename it to "firebaseconfig.json"

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
        self.__game.child("token").set(self.__token)

        return self.__id, self.__token

    def writeMove(self, move):
        self.__game.child("moves").child(self.__moveId).set(move)
        self.__moveId += 1

