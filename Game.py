"""
Object for handling the game
"""
import chess

class Game:

    def __init__(self, elo):
        self.__elo = elo
        self.__stockfish = r"stockfish/stockfish-windows-x86-64-avx2.exe"
        self.__playerMoves = []
        self.__aiMoves = []
        self.__board = chess.Board()
        engine = chess.engine.SimpleEngine.popen_uci(r"stockfish\stockfish-windows-x86-64-avx2.exe")


