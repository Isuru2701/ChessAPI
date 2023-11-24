"""
Object for handling the game
"""
import chess
import chess.engine
class Game:
    """
    Represents the game
    Uses stockfish engine
    Communicates with the engine via The Universal chess interface (UCI) and XBoard protocol
    """
    def __init__(self, elo, board=""):
        self.__elo = elo
        self.__stockfish = r"stockfish/stockfish-windows-x86-64-avx2.exe"
        self.__playerMoves = []
        self.__aiMoves = []
        self.__board = chess.Board()
        self.__engine = chess.engine.SimpleEngine.popen_uci(r"stockfish\stockfish-windows-x86-64-avx2.exe")
        self.__game_over = False
        self.__isPlayerTurn = True

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
    def getMoves(self):
        """
        Get the moves of the game
        :return: player moves and ai moves as arrays
        """
        return self.__playerMoves, self.__aiMoves


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

    def makeMove(self, moveStr):
        """user makes move"""

        if not self.__game_over:
            if self.__isPlayerTurn:
                if self.isLegalMove(moveStr):
                    self.__board.push_san(moveStr)
                    self.__playerMoves.append(moveStr)
                    self.__playerMoves.append(moveStr)
                    ##AI's Turn next
                    self.__isPlayerTurn = False
                    return "OK"

            return "NOT_YOUR_TURN"

        return "GAME_OVER"


    def stockfishMove(self) -> str:
        """stockfish AI makes move and sends back a from-square-to-square"""
        result = self.__engine.play(self.__board, chess.engine.Limit(time=4.0))
        move = result.move
        self.__board.push(move)
        # Back to the user
        self.__aiMoves.append(move.uci())
        self.__isPlayerTurn = True

        if self.__board.is_kingside_castling(move):
            return "O-O"
        elif self.__board.is_queenside_castling(move):
            return "O-O-O"

        return move.uci()


    def checkForGameOver(self) -> bool:
        """Game over logic: check for
         - Checkmate
         - Stalemate
         - Draw
         - Resignation
         """
        if self.__board.is_checkmate():
            self.__game_over = True

        return self.__game_over

    def getBoard(self):
        return self.__board.fen()

    def setBoard(self, fenStr):
        self.__board.set_board_fen(fenStr)