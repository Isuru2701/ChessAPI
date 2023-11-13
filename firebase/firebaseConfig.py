import firebase_admin
from firebase_admin import credentials, db



cred = credentials.Certificate("chess-d400d-firebase-adminsdk-j6xcq-00e9c7244a.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://chess-13669-default-rtdb.asia-southeast1.firebasedatabase.app/"
})
