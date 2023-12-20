"""
Object for handling the game
"""
import sys
import chess
import chess.engine
import os
class Game:
    """
    Represents the game
    Uses stockfish engine
    Communicates with the engine via The Universal chess interface (UCI) and XBoard protocol
    """
    def __init__(self, elo, board=""):
        self.__elo = elo
        self.__stockfish = r"stockfish/stockfish-windows-x86-64-avx2.exe"
        if board == "":
            self.__board = chess.Board()
        else:
            self.__board = chess.Board(board)
        self.__engine = chess.engine.SimpleEngine.popen_uci( os.path.join("stockfish", "stockfish-windows-x86-64-avx2.exe"))

        # refer to the following for skill level to elo mapping https://lichess.org/forum/general-chess-discussion/elo-of-lichess-ais?page=1
        if elo < 800:
            self.__engine.configure({"UCI_LimitStrength": True, "Skill level": 0})
        elif elo < 900:
            self.__engine.configure({"UCI_LimitStrength": True, "Skill level": 2})
        elif elo < 1000:
            self.__engine.configure({"UCI_LimitStrength": True, "Skill level": 3})
        elif elo < 1200:
            self.__engine.configure({"UCI_LimitStrength": True, "Skill level": 4})
        elif elo < 1700:
            self.__engine.configure({"UCI_LimitStrength": True, "Skill level": 5})
        elif elo < 1900:
            self.__engine.configure({"UCI_LimitStrength": True, "Skill level": 6})
        elif elo < 2000:
            self.__engine.configure({"UCI_LimitStrength": True, "Skill level": 7})
        else:
            self.__engine.configure({"UCI_LimitStrength": True, "Skill level": 10})

    def destroy(self):
        """
        kills the engine
        """
        self.__engine.quit()

    def isLegalMove(self, move) -> bool:
        """Check if the move is legal
            return: True if legal, False otherwise
        """
        return move in self.__board.legal_moves

    def makeMove(self, moveStr=None) -> str:
        """User makes a move

        :param moveStr: Move in SAN format
        :return: AI's move in SAN format or game result
        """
        if moveStr is not None:
            user_move = chess.Move.from_uci(moveStr)
            if not self.isLegalMove(user_move):
                return "ILLEGAL_MOVE"
            self.__board.push(user_move)


    def stockfishMove(self) -> str:
        """stockfish AI makes move and sends back a from-square-to-square"""
        result = self.__engine.play(self.__board, chess.engine.Limit(time=2.0))
        move = result.move
        self.__board.push(move)

        if self.__board.is_kingside_castling(move):
            return "O-O"
        elif self.__board.is_queenside_castling(move):
            return "O-O-O"

        #if self.checkForGameOver():
            #return "AI_WINS"   -- correctly handle this validation later
        return move.uci()




    def checkForGameOver(self) -> str:
        """Game over logic: check for
         - Checkmate
         - Stalemate
         - Draw
         - Resignation
         """
        if self.__board.is_stalemate():
            return "STALEMATE"

        if self.__board.is_checkmate():
            return "CHECKMATE"

        else:
            return "NOT_OVER"

    def getBoard(self):
        return self.__board.fen()

    def setBoard(self, fenStr):
        self.__board.set_board_fen(fenStr)


if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script_name.py elo move")
        sys.exit(1)

    # Extract Elo and move from command-line arguments
    elo = int(sys.argv[1])
    move = sys.argv[2]

    # Create a Game instance with the specified Elo
    game = Game(elo)

    # Make the move and get the AI's response
    ai_response = game.makeMove(move)

    # Print the result
    print(f"AI's response: {ai_response}")

    # Close the engine
    game.destroy()