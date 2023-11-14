"""
Object for handling the game
"""
import chess
import chess.engine

class Game:
    """
    Represents the game
    Uses stockfish engine
    """
    def __init__(self, elo):
        self.__elo = elo
        self.__stockfish = r"stockfish/stockfish-windows-x86-64-avx2.exe"
        self.__playerMoves = []
        self.__aiMoves = []
        self.__board = chess.Board()
        self.__engine = chess.engine.SimpleEngine.popen_uci(r"stockfish\stockfish-windows-x86-64-avx2.exe")

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


