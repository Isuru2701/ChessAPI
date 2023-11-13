import firebase_admin
from firebase_admin import credentials, db


# Make an app in firebase > add realtime database > service accounts > generate new private key
# Add the json file to the same directory as this file and rename it to "firebaseconfig.json"
cred = credentials.Certificate("firebaseconfig.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://chess-13669-default-rtdb.asia-southeast1.firebasedatabase.app/"
})
