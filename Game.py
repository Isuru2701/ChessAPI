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

    def makeMove(self):
        """user makes move"""

    def stockfishMove(self) -> str:
        """stockfish AI makes move and sends back a from-square-to-square"""


