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
    def __init__(self, elo):
        self.__elo = elo
        self.__stockfish = r"stockfish/stockfish-windows-x86-64-avx2.exe"
        self.__playerMoves = []
        self.__aiMoves = []
        self.__board = chess.Board()
        self.__engine = chess.engine.SimpleEngine.popen_uci(r"stockfish\stockfish-windows-x86-64-avx2.exe")

        # refer to the following paper for skill level to elo comparison http://web.ist.utl.pt/diogo.ferreira/papers/ferreira13impact.pdf Page 11
        self.__engine.configure({"UCI_LimitStrength": True,"min": 100, "UCI_Elo": self.__elo })
        print(self.__engine.options)
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


