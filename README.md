# Chess API
A python flask web API that enables the robots to play chess with a human physically
All logical processing and game-handling is done by the API.

# Events
The API depends on events to communicate with the robots.
The events are as listed below:

- Standby
  - Robot is online and ready to play
  - Robot staged
  - Robot is offline or in use

- Start Game
  - Player is White
  - Player is Black

- Make Moves

- Game Over
  - Player Checkmates
  - Robot Checkmates
  - Stalemate
  - Player Resigns

The endpoints and handling of each event is explained below

> Note!
> Parameters inside [ ] are optional, and only one of them can be used at a time

# Standby
This event is triggered when the robot is online and ready to play.

The robot sends a POST request to the API with the following payload:
endpoint: `/api/robots/` | method: `POST`
```json
{
  "sn": 1
}
```

If the Robot is NOT STAGED for a game, the API responds with a 200 OK and the robot is added to the list of available robots.

If the Robot is STAGED for a game, the initial json payload generated while initializing is sent. This is stored in Firebase until the robot replies.

# Start Game
This event is triggered when the player starts a game.

endpoint: `/api/games/` | method: `POST`
```json
{
  "sn": 1,
  "elo": 1200,
  "player": ["black", "white"]
}
```

The API responds with a 200 OK and the robot is added to the list of staged robots.
return to the UI if SUCCESS
```json
{
  "id": 1,
  "token": "sbnsivnsidnvsiv",
  "elo": 1200,
  "player": ["BLACK", "WHITE"]
}
```

if FAILURE
```json
{
  "error": "Robot not available"
}
```

json payload staged for the robot: 
- if player is WHITE:
```json
{
  "id": 1,
  "token": "sbnsivnsidnvsiv",
  "elo": 1200,
  "player": "WHITE",
  "move" : null
}
```
- if player is BLACK:
```json
{
  "id": 1,
  "token": "sbnsivnsidnvsiv",
  "elo": 1200,
  "player": "BLACK",
  "move" : "e2e4"
}
```

# Make Moves
This event is triggered when the player makes a move.

endpoint: `/api/games/play` | method: `POST`
```json
{
  "id": 0,
  "token": 0,
  "move": "e2e4"
}
```
RETURNS
```json
{
  "result": "AI_MOVE",
  "move": "e7e5"
}
```

If illegal move RETURNS
```json
{
  "illegal": true
}
```

where move is the AI's move
"result" will be explained later in the Game Over section.

# Game Over
This event is triggered when the game is over.
In states where game over is declared. the json payload defined in `Make Moves` will change accordingly. 
- Player Checkmates
```json
{
  "result": "CHECKMATE",
  "move": null
}
```
- Robot Checkmates
```json
{
  "result": "CHECKMATE",
  "move": "e7e5"
}
```

> Note!
> If it's a robot checkmate, the robot has to make the move. And therefore the winner must be identified by whether move is null or not.

- Stalemate
```json
{
  "result": "STALEMATE",
  "move": null
}
```

- Player Resigns
endpoint: `/api/games/{id}/resign` | method: `POST`
```json
{
  "id": 0,
  "token": 0
}
```
RETURNS
```json
{
  "result": "RESIGN",
  "move": null
}
```

# Get Board
Access this endpoint with your UI to fetch the current board
endpoint: `/api/games/{id}/board` | method: `GET`
RETURNS `FEN` string