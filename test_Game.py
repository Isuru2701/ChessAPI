import chess
import chess.engine

def main():
    print("Welcome to Console Chess!")
    print("Enter moves in the format 'fromSquare toSquare'.")
    print("Example: e2e4")
    print("Enter 'q' to quit.\n")

    initial_fen = "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R"
    board = chess.Board(initial_fen)
    
    engine = chess.engine.SimpleEngine.popen_uci(r"stockfish\stockfish-windows-x86-64-avx2.exe")
    set_skill_level(engine, 2)

    is_player_turn = True
    is_game_over = False

    while not is_game_over:
        move = ""
        if is_player_turn:
            move = input("Player's turn: ")
            if move == 'q':
                break
            if not is_valid_move(board, move):
                print("Illegal move!")
                continue
        else:
            move = get_engine_move(engine, board)
            print("Engine's turn:", move)

            if not is_valid_move(board, move):
                print("Engine made an invalid move:", move)
                continue

        parsed_move = chess.Move.from_uci(move)
        moved_piece = get_piece_symbol(board.piece_type_at(parsed_move.from_square))
        cut_piece = get_piece_symbol(board.piece_type_at(parsed_move.to_square)) if board.is_capture(parsed_move) else "0"
        move_with_info = f"{move}m={moved_piece},c={cut_piece}"

        # Output the moves so far
        print(move_with_info)

        # Make the move on the board
        board.push(parsed_move)

        # Print the updated FEN string
        print("Updated FEN:", board.fen())

        move_history = list(board.move_stack)

        # Print the move history
        for movements in move_history:
            print(movements.uci())

        # Check for game end conditions (e.g., checkmate, stalemate, etc.)
        if board.is_checkmate():
            print("Checkmate!")
            if is_player_turn:
                print("Player wins!")
            else:
                print("Engine wins!")
            is_game_over = True
        elif board.is_stalemate():
            print("Stalemate! It's a draw.")
            is_game_over = True

        is_player_turn = not is_player_turn

    print("\nGame ended.")
    engine.quit()

def is_valid_move(board, move):
    try:
        parsed_move = board.parse_san(move)
        return parsed_move in board.legal_moves
    except ValueError:
        return False

def get_engine_move(engine, board):
    result = engine.play(board, chess.engine.Limit(time=4.0))
    move = result.move
    return move.uci()

def set_skill_level(engine, level):
    engine.configure({"UCI_LimitStrength": True, "Skill level": level})

def get_piece_symbol(piece_type):
    if piece_type == chess.PAWN:
        return "p"
    elif piece_type == chess.BISHOP:
        return "b"
    elif piece_type == chess.KNIGHT:
        return "n"
    elif piece_type == chess.KING:
        return "k"
    elif piece_type == chess.QUEEN:
        return "q"
    elif piece_type == chess.ROOK:
        return "r"

if __name__ == "__main__":
    main()
