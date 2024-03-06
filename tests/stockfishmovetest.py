import unittest
from Game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        # Create a Game instance with Elo 1200 for testing
        self.game = Game(1200)

    def tearDown(self):
        # Close the engine after each test
        self.game.destroy()

    def test_legal_move(self):
        # Test for a legal move
        self.assertTrue(self.game.isLegalMove("e2e4"))

    def test_illegal_move(self):
        # Test for an illegal move
        self.assertFalse(self.game.isLegalMove("e2e5"))

    def test_capture(self):
        # Test for a move resulting in a capture
        self.assertTrue(self.game.isCapture("e2e4"))
        self.game.makeMove("e2e4")
        self.assertTrue(self.game.isCapture("d7d5"))
        self.game.makeMove("d7d5")
        self.assertTrue(self.game.isCapture("e4d5"))

    def test_non_capture(self):
        # Test for a move not resulting in a capture
        self.assertFalse(self.game.isCapture("e2e4"))
        self.game.makeMove("e2e4")
        self.assertFalse(self.game.isCapture("d7d5"))

    def test_stockfish_move(self):
        # Test the AI's move generation
        move = self.game.stockfishMove()
        self.assertTrue(self.game.isLegalMove(move))
        self.assertTrue(self.game.isCapture(move))
        self.game.makeMove(move)
        self.assertEqual(self.game.checkForGameOver(), "NOT_OVER")

    def test_game_over(self):
        # Test for game over conditions (stalemate, checkmate)
        # Test for stalemate
        self.game.setBoard("8/8/8/8/5k2/8/4K3/8 w - - 0 1")
        self.assertEqual(self.game.checkForGameOver(), "STALEMATE")

        # Test for checkmate
        self.game.setBoard("8/8/8/8/5k2/8/4K3/q7 w - - 0 1")
        self.assertEqual(self.game.checkForGameOver(), "CHECKMATE")


if __name__ == '__main__':
    unittest.main()
