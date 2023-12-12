# Chess API
A python flask web API that enables the robots to play chess with a human physically
All logical processing and game-handling is done by the API.

# Events
The API depends on events to communicate with the robots.
The events are as listed below:

- Standby
  - Robot is online and ready to play
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

