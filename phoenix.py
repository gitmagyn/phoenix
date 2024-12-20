
import chess
import chess.pgn
import chess.polyglot
import time

from values import *

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def store(self, b_hash, depth, eval, flag, move):
        self.table[b_hash] = (depth, eval, flag, move)

    def lookup(self, b_hash, depth):
        if b_hash in self.table:
            s_depth, eval, flag, move = self.table[b_hash]
            if s_depth >= depth:
                return eval, flag, move
        return None

t_table = TranspositionTable()

def b_hash(board):
    return (board.fen(), board.turn, board.castling_rights,
            board.ep_square, board.halfmove_clock, board.fullmove_number)

def evaluate_board(board, depth):

    if board.is_checkmate():
        return (-10000 + depth) if board.turn == chess.WHITE else (10000 - depth)
    elif board.is_stalemate():
        return 0

    evaluation = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_value = material.get(piece.piece_type, 0)
            _, pst = tables[piece.piece_type][piece.color]
            piece_position_value = pst[square]
            if piece.color == chess.WHITE:
                evaluation += piece_value + piece_position_value
            else:
                evaluation -= piece_value + piece_position_value

    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    for square in center_squares:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                evaluation += 0.5
            else:
                evaluation -= 0.5

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            if piece.color == chess.WHITE:
                evaluation += 0.1 if square not in [chess.B1, chess.G1] else -0.1
            else:
                evaluation -= 0.1 if square not in [chess.B8, chess.G8] else 0.1

    evaluation += pawn_structure(board)

    evaluation += king_safety(board, chess.WHITE)
    evaluation -= king_safety(board, chess.BLACK)

    evaluation += open_file_control(board, chess.WHITE)
    evaluation -= open_file_control(board, chess.BLACK)
    
    return evaluation

def open_file_control(board, color):
    evaluation = 0
    for file in range(8):
        is_open = True
        for rank in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                is_open = False
                break
        if is_open:
            rook_or_queen = [board.piece_at(chess.square(file, rank)) for rank in range(8)]
            if any(piece for piece in rook_or_queen if piece and piece.color == color and piece.piece_type in [chess.ROOK, chess.QUEEN]):
                evaluation += 0.3
    return evaluation

def pawn_structure(board):
    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.PAWN:
            evaluation += pawn_ss(board, square, piece.color)
    return evaluation

def pawn_ss(board, square, color):
    evaluation = 0
    file = chess.square_file(square)
    rank = chess.square_rank(square)

    # Peão isolado
    if ((file == 0 or not any(board.piece_at(chess.square(file - 1, r)) == chess.PAWN and board.piece_at(chess.square(file - 1, r)).color == color for r in range(8))) and
        (file == 7 or not any(board.piece_at(chess.square(file + 1, r)) == chess.PAWN and board.piece_at(chess.square(file + 1, r)).color == color for r in range(8)))):
        evaluation -= 0.5
    
    # Peão dobrado
    if sum(1 for r in range(8) if board.piece_at(chess.square(file, r)) == chess.PAWN and board.piece_at(chess.square(file, r)).color == color) > 1:
        evaluation -= 0.5

    # Peão passado
    if is_pawn_passed(board, square, color):
        evaluation += 0.7

    return evaluation

def is_pawn_passed(board, square, color):
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    direction = 1 if color == chess.WHITE else -1

    for r in range(rank + direction, 8 if color == chess.WHITE else -1, direction):
        for f in range(max(0, file - 1), min(7, file + 1) + 1):
            if board.piece_at(chess.square(f, r)) == chess.PAWN and board.piece_at(chess.square(f, r)).color != color:
                return False
    return True

def king_safety(board, color):
    evaluation = 0
    king_square = board.king(color)
    king_file = chess.square_file(king_square)
    king_rank = chess.square_rank(king_square)
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for direction in directions:
        for i in range(1, 3):
            file = king_file + direction[0] * i
            rank = king_rank + direction[1] * i
            if 0 <= file < 8 and 0 <= rank < 8:
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                if piece and piece.color != color:
                    evaluation -= piece_threat_value(piece)
    return evaluation

def piece_threat_value(piece):
    if piece.piece_type == chess.QUEEN:
        return 9
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type in [chess.BISHOP, chess.KNIGHT]:
        return 3
    return 1

def order_moves(board):
    def move_score(move):
        piece = board.piece_at(move.to_square)
        if piece is None:
            return (False, 0)
        return (True, piece.piece_type)
    moves = list(board.legal_moves)
    moves.sort(key=move_score, reverse=True)
    return moves

nodes = 0

def minimax(board, depth, alpha, beta, maximizing_player, log):
    global nodes
    nodes += 1

    bl_hash = b_hash(board)
    tt_entry = t_table.lookup(bl_hash, depth)
    if tt_entry:
        tt_eval, tt_flag, tt_move = tt_entry
        if tt_flag == "exact":
            return tt_eval, tt_move
        elif tt_flag == "lowerbound" and tt_eval > alpha:
            alpha = tt_eval
        elif tt_flag == "upperbound" and tt_eval < beta:
            beta = tt_eval
        if alpha >= beta:
            return tt_eval, tt_move

    if depth == 0 or board.is_game_over():
        return evaluate_board(board, depth), None

    best_move = None
    if maximizing_player:
        max_eval = -float('inf')
        for move in order_moves(board):
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False, log)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Poda Beta
        log.append((depth, best_move.uci(), max_eval))
        t_table.store(bl_hash, depth, max_eval, "exact", best_move)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in order_moves(board):
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True, log)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Poda Alpha
        log.append((depth, best_move.uci(), min_eval))
        t_table.store(bl_hash, depth, min_eval, "exact", best_move)
        return min_eval, best_move

def best_minimax(board, max_depth):
    global nodes
    log = []
    best_move = None

    nodes = 0
    for depth in range(1, max_depth + 1):
        eval, best_move = minimax(board, depth, -float('inf'), float('inf'), board.turn == chess.WHITE, log)
        eval = int(eval * 10)
        print(f"info depth {depth} nodes {nodes} nps {nodes} score cp {eval} pv {best_move.uci()}")

    print(f"info nodes {nodes}")
    eval = int(eval * 10)
    print(f"info score cp {eval} depth {max_depth}")

    return best_move

import base64
from binbase64 import *
import tempfile

def get_phoenix_bin_file():
    decoded = base64.b64decode(PHOENIX_BIN_BASE64)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as temp_file:
        temp_file.write(decoded)
        temp_file.seek(0)
        return temp_file.name

def best_movep(board):
    phoenix_path = get_phoenix_bin_file()
    with chess.polyglot.open_reader(phoenix_path) as reader:
        try:
            entry = reader.find(board)
            return entry.move
        except IndexError:
            return None
        
# ESTÁ EM BETA TEST
def difval():
    num_pieces = sum(1 for square in chess.SQUARES if board.piece_at(square) is not None)
    legal_moves = len(list(board.legal_moves))
    threats = 0
    forced_moves = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.color != board.turn:
            if board.is_attacked_by(board.turn, square):
                threats += 1
            for move in board.legal_moves:
                if move.to_square == square and board.is_checkmate():
                    forced_moves += 1
    phase_factor = 0.8
    difficulty_score = ((num_pieces / 32) * 5 + (legal_moves / 20) * 3 + (threats / 5) * 7 + (forced_moves / 5) * 5) / 5
    difficulty_score *= phase_factor
    difficulty_score = max(0, min(5, difficulty_score))
    return round(difficulty_score, 5)

def gameconfig():    
    total_pieces = 0
    total_value = 0
    queens = 0
    rooks = 0
    knights = 0
    bishops = 0

    for piece in board.piece_map().values():
        total_pieces += 1
        total_value += material.get(piece.piece_type, 0)
        if piece.piece_type == chess.QUEEN:
            queens += 1
        elif piece.piece_type == chess.ROOK:
            rooks += 1
        elif piece.piece_type == chess.KNIGHT:
            knights += 1
        elif piece.piece_type == chess.BISHOP:
            bishops += 1

    if total_pieces <= 10 or total_value <= 200:
        print("info preview endgame")
        return "endgame"
    elif queens < 2 and (rooks < 2 or knights + bishops < 2):
        print("info preview endgame")
        return "endgame"
    else:
        print("info preview midgame")
        return "midgame"

def calculate_depth(rem_time, increment, moveleft=40, position_complexity=1.0):
    position_complexity = difval()
    print(f"info preview dif {position_complexity}")
    moveleft = 80 - moveleft
    buffer_time = rem_time * 0.02
    safetime = rem_time - buffer_time
    if safetime < 0:
        safetime = rem_time
    timepmove = (safetime / moveleft + increment) * position_complexity

    print(timepmove)
    
    x = gameconfig()

    if x == "midgame":    
        if timepmove <= 50:
            depth = 4
        elif (rem_time + increment) <= 0.1:
            depth = 2
        elif (rem_time + increment) <= 0.5:
            depth = 3
        else:
            depth = 5
        if position_complexity > 2.2 and (rem_time + increment) >= 60:
            depth += 1
        print(f"info preview depth {depth}")
        return depth
    elif x == "endgame":
        if timepmove <= 30:
            depth = 4
        elif (rem_time + increment) <= 0.1:
            depth = 3
        else:
            depth = 5
        if position_complexity > 2.2 and (rem_time + increment) >= 60:
            depth += 1
        print(f"info preview depth {depth}")
        return depth

board = chess.Board()
moves = []
invalidmoves = []
options = {
    "Hash": 128,
    "Ponder": False,
}

# you can use CPython, but it is recommended to use PyPy
print("PyPy OK")

while True:
    inp = input().strip()
    
    if inp == "uci":
        print("id name Phoenix 3.1")
        print("id author magyn")
        print("uciok")
    
    elif inp == "isready":
        print("readyok")
        
    elif inp.startswith("setoption"):
        parts = inp.split(" ")
        if len(parts) >= 4:
            option_name = parts[2]
            option_value = " ".join(parts[4:])
            if option_name.lower() == "move" and parts[3].lower() == "overhead":
                options["Move Overhead"] = option_value
                print(f"info string Move Overhead set to {option_value}")
            elif option_name.lower() == "threads":
                options["Threads"] = option_value
                print(f"info string Threads set to {option_value}")
            elif option_name.lower() == "hash":
                options["Hash"] = option_value
                print(f"info string Hash set to {option_value}")
            else:
                options[option_name] = option_value
        else:
            print("info string Invalid setoption format")
    
    elif inp == "ucinewgame":
        board = chess.Board()
        moves = []
        invalidmoves = []
    
    elif inp.startswith("position startpos"):
        board = chess.Board()
        moves = []
        invalidmoves = []
        if "moves" in inp:
            moves = inp.split("moves")[1].strip().split(" ")
            for move in moves:
                try:
                    board.push_uci(move)
                except ValueError:
                    pass
    
    elif inp.startswith("position fen"):
        fen_position = inp[len("position fen"):].strip()
        try:
            board.set_fen(fen_position)
            moves = []
            invalidmoves = []
        except ValueError:
            pass

    elif len(inp) == 4 and inp[0].isalpha() and inp[1].isdigit() and inp[2].isalpha() and inp[3].isdigit():
        try:
            board.push_uci(inp)
            moves.append(inp)
        except ValueError:
            print(f"Invalid move: {inp}")
            invalidmoves.append(inp)
    
    elif inp.startswith("go"):
        parts = inp.split()
        wtime = btime = 300000
        winc = binc = 1000
        
        for i in range(len(parts)):
            if parts[i] == "wtime":
                wtime = int(parts[i + 1])
            elif parts[i] == "btime":
                btime = int(parts[i + 1])
            elif parts[i] == "winc":
                winc = int(parts[i + 1])
            elif parts[i] == "binc":
                binc = int(parts[i + 1])

        if not board.is_game_over():
            timer = wtime / 1000 if board.turn == chess.WHITE else btime / 1000
            inc = winc / 1000 if board.turn == chess.WHITE else binc / 1000

            depth = calculate_depth(timer, inc)

            for i in range(len(parts)):
                if parts[i] == "depth":
                    depth = int(parts[i + 1])

            best_move = best_movep(board)    # with polyglot book
            #best_move = None                # no polyglot book
            if not best_move:
                best_move = best_minimax(board, depth)
            if best_move:
                try:
                    board.push(best_move)
                    moves.append(best_move.uci())
                    invalidmoves = []
                    print(f"bestmove {best_move.uci()}")
                except ValueError:
                    pass
                    invalidmoves.append(best_move)
        else:
            pass
    
    elif inp == "stop":
        print("search stopped")
    
    elif inp == "quit":
        break
