from firebaseConfig.firebaseConfig import Database
db = Database()

staged_robots = db.getStagedRobots()
print(staged_robots)