# CHESS API
A python-flask-based stockfish api that gives the best move for the corresponding user move in a chess game

```mermaid
    graph LR
    a[User move] --> b((stockfish processing)) --> c[AI move]

```

 ## Endpoints

###  GET /
    RETURNS a chess board to make moves online

> Note
> Parameters inside [ ] are optional, and only one of them can be used at a time

### POST /api/robots/
Update robot availability

```json
{
  "sn": 1,
  "online": true,
  "status": ["STANDBY", "PLAYING"]
}
```

RETURNS
`200 OK`


###  POST /api/games/
    initializes the game. With difficulty set to the `elo` level
    default elo is 1200
```json
{
  "sn": 1,
  "elo": 1200,
  "player": ["BLACK", "WHITE"]
}
```


SENDS TO ROBOT
```json
{
  "id": 1,
  "token": "sbnsivnsidnvsiv",
  "elo": 1200,
  "player": ["BLACK", "WHITE"],
  "move" : [null, "e2e4"]
}
```

RETURNS TO MOBILE APP
```json
{
  "id": 1,
  "token": "sbnsivnsidnvsiv",
  "elo": 1200,
  "player": [
    "BLACK",
    "WHITE"
  ]
}
```
IF robot is not available
```json
{
  "error": "Robot not available"
}
```

    RETURNS game id and token "id", "token"

Use the id and token to access your game

### POST /api/games/{move}
    make user move in the game. Uses the from-square to-square format. Returns AI move.
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
  "id": 0,
  "token": 0,
  "move": "e2e4",
  "best_move": "e7e5"
}
```
If illegal move RETURNS
```json
{
  "id": 0,
  "token": 0,
  "illegal": true
}
```

### GET /api/games/{id}
    GET the current state of the game

RETURNS
```json
{
  "id": 0,
  "token": 0,
  "state": "playing",
  "board": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
}
```
### PUT /api/games/{id}/resign
    resign the game

```json
{
  "id": 0,
  "token": 0
}
```
RETURNS
```json
{
    "id": 0,
    "token": 0,
    "state": "resigned"
}
```