import chess
import chess.pgn
import chess.polyglot
import os
import time

pawnblack = [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5, 0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5, 0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0, 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5, 1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0, 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0, 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
pawnwhite = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -1.0, -1.0, -2.0, 0.0, 0.0, -2.0, -1.0, -1.0, 0.0, 0.0, 0.0, -2.5, -2.5, 0.0, 0.0, 0.0, -0.0, -0.0, -0.0, -2.0, -2.0, -0.0, -0.0, -0.0, -0.5, 0.5, 1.0, -0.0, -0.0, 1.0, 0.5, -0.5, -0.5, -1.0, -1.0, 2.0, 2.0, -1.0, -1.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
knightblack = [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0, -4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0, -3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0, -3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0, -3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0, -3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0, -4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0, -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
knightwhite = [5.0, 4.0, 3.0, 3.0, 3.0, 3.0, 4.0, 5.0, 4.0, 2.0, 0.0, -0.0, -0.0, 0.0, 2.0, 4.0, 3.0, -0.5, -1.0, -1.5, -1.5, -1.0, -0.5, 3.0, 3.0, -0.5, -1.5, -2.0, -2.0, -1.5, -0.5, 3.0, 3.0, -0.5, -1.5, -2.0, -2.0, -1.5, -0.5, 3.0, 3.0, -0.5, -1.0, -1.5, -1.5, -1.0, -0.5, 3.0, 4.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.0, 5.0, 4.0, 3.0, 3.0, 3.0, 3.0, 4.0, 5.0]
bishopblack = [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0, 1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0, -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0, -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0, -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0, -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0, 1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5,  1.0, -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
bishopwhite = [2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0, -1.0, -1.0, -1.0, -1.0, 0.0, 1.0, 1.0, -0.0, -1.0, -1.0, -1.0, -1.0, -0.0, 1.0, 1.0, 0.0, -0.5, -1.0, -1.0, -0.5, 0.0, 1.0, 1.0, -0.0, -0.5, -1.0, -1.0, -0.5, -0.0, 1.0, -1.0, -0.0, 0.0, 0.0, 0.0, 0.0, -0.0, -1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0]
rookblack = [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
rookwhite = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0, -0.0, -0.0, -0.5, -0.5, -0.0, -0.0, -0.0, 0.0, 0.0, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0, -0.0, 0.0, 0.0, 0.0]
queenblack = [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0, 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
queenwhite = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0, -0.0, -0.0, -0.5, -0.5, -0.0, -0.0, -0.0, 0.0, 0.0, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0, -0.0, 0.0, 0.0, 0.0]
kingblack = [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0,  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0, -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0, -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0, -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0, -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0, -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0, -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0]
kingwhite = [3.0, 4.0, 4.0, 0.0, 0.0, 4.0, 4.0, 3.0, 3.0, 4.0, 0.0, 0.0, 0.0, 0.0, 4.0, 3.0, 3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0, 3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0, 2.0, 3.0, 3.0, 4.0, 4.0, 3.0, 3.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, -2.0, -2.0, -0.0, -0.0, -0.0, -0.0, -2.0, -2.0, -2.0, -3.0, -1.0, -0.0, -0.0, -1.0, -3.0, -2.0]

tables = {
    chess.PAWN: {chess.WHITE: pawnwhite, chess.BLACK: pawnblack},
    chess.KNIGHT: {chess.WHITE: knightwhite, chess.BLACK: knightblack},
    chess.BISHOP: {chess.WHITE: bishopwhite, chess.BLACK: bishopblack},
    chess.ROOK: {chess.WHITE: rookwhite, chess.BLACK: rookblack},
    chess.QUEEN: {chess.WHITE: queenwhite, chess.BLACK: queenblack},
    chess.KING: {chess.WHITE: kingwhite, chess.BLACK: kingblack}
}

material = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 35,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 0
}

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

def evaluate_board(board):
    evaluation = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_value = material.get(piece.piece_type, 0)
            piece_positionv = tables[piece.piece_type][piece.color][square]
            if piece.color == chess.WHITE:
                evaluation += piece_value + piece_positionv
            else:
                evaluation -= piece_value + piece_positionv

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
            if piece.color == chess.WHITE and square not in [chess.B1, chess.G1]:
                evaluation += 0.1
            elif piece.color == chess.BLACK and square not in [chess.B8, chess.G8]:
                evaluation -= 0.1

    evaluation += pawn_structure(board)
    evaluation += king_safety(board, chess.WHITE)
    evaluation -= king_safety(board, chess.BLACK)

    return evaluation

def pawn_ss(board, square, color):
    evaluation = 0
    file = chess.square_file(square)
    rank = chess.square_rank(square)

    if ((file == 0 or not any(board.piece_at(chess.square(file - 1, r)) == chess.PAWN and board.piece_at(chess.square(file - 1, r)).color == color for r in range(8))) and
        (file == 7 or not any(board.piece_at(chess.square(file + 1, r)) == chess.PAWN and board.piece_at(chess.square(file + 1, r)).color == color for r in range(8)))):
        evaluation -= 0.5
    
    if sum(1 for r in range(8) if board.piece_at(chess.square(file, r)) == chess.PAWN and board.piece_at(chess.square(file, r)).color == color) > 1:
        evaluation -= 0.5
    
    if rank > 0 and rank < 7:
        if color == chess.WHITE:
            if ((file > 0 and board.piece_at(chess.square(file - 1, rank + 1)) == chess.PAWN and board.piece_at(chess.square(file - 1, rank + 1)).color == color) or
                (file < 7 and board.piece_at(chess.square(file + 1, rank + 1)) == chess.PAWN and board.piece_at(chess.square(file + 1, rank + 1)).color == color)):
                pass
            else:
                evaluation -= 0.5
        else:
            if ((file > 0 and board.piece_at(chess.square(file - 1, rank - 1)) == chess.PAWN and board.piece_at(chess.square(file - 1, rank - 1)).color == color) or
                (file < 7 and board.piece_at(chess.square(file + 1, rank - 1)) == chess.PAWN and board.piece_at(chess.square(file + 1, rank - 1)).color == color)):
                pass
            else:
                evaluation -= 0.5

    return evaluation

def pawn_structure(board):
    evaluation = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.PAWN:
            evaluation += pawn_ss(board, square, piece.color)

    return evaluation

def king_safety(board, color):
    evaluation = 0
    king_square = board.king(color)
    king_file = chess.square_file(king_square)
    king_rank = chess.square_rank(king_square)
    
    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (-1, -1), (1, -1), (-1, 1)
    ]

    for direction in directions:
        for i in range(1, 3):
            file = king_file + direction[0] * i
            rank = king_rank + direction[1] * i
            if 0 <= file < 8 and 0 <= rank < 8:
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                if piece and piece.color != color:
                    if piece.piece_type == chess.QUEEN:
                        evaluation -= 9
                    elif piece.piece_type == chess.ROOK:
                        evaluation -= 5
                    elif piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT:
                        evaluation -= 3

    return evaluation

def order_moves(board):
    def move_score(move):
        piece = board.piece_at(move.to_square)
        if piece is None:
            return (False, 0)
        return (True, piece.piece_type)
    moves = list(board.legal_moves)
    moves.sort(key=move_score, reverse=True)
    return moves

def minimax(board, depth, alpha, beta, maximizing_player, log, start_time, max_time):
    b_hash = b_hash(board)
    tt_entry = t_table.lookup(b_hash, depth)
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

    if depth == 0 or board.is_game_over() or time.time() - start_time > max_time:
        return evaluate_board(board), None

    best_move = None
    if maximizing_player:
        max_eval = -float('inf')
        for move in order_moves(board):
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False, log, start_time, max_time)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        log.append((depth, best_move.uci(), max_eval))
        flag = "exact"
        if max_eval <= alpha:
            flag = "upperbound"
        elif max_eval >= beta:
            flag = "lowerbound"
        t_table.store(b_hash, depth, max_eval, flag, best_move)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in order_moves(board):
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True, log, start_time, max_time)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        log.append((depth, best_move.uci(), min_eval))
        flag = "exact"
        if min_eval <= alpha:
            flag = "upperbound"
        elif min_eval >= beta:
            flag = "lowerbound"
        t_table.store(b_hash, depth, min_eval, flag, best_move)
        return min_eval, best_move

def best_minimax(board, max_time):
    log = []
    depth = 1
    starttime = time.time()
    best_move = None
    best_moves_pd = {}

    while True:
        eval, best_move = minimax(board, depth, -float('inf'), float('inf'), board.turn == chess.WHITE, log, starttime, max_time)
        if time.time() - starttime > max_time:
            break
        best_moves_pd[depth] = best_move
        print(f"info depth {depth} score cp {eval} pv {best_move.uci()}")
        depth += 1

    if depth > 1 and (time.time() - starttime > max_time):
        best_move = best_moves_pd[depth - 1]
    
    print("info depth {0}".format(depth - 1))

    return best_move

def best_movep(board):
    if os.path.exists("phoenix.bin"):
        with chess.polyglot.open_reader("phoenix.bin") as reader:
            try:
                entry = reader.find(board)
                return entry.move
            except IndexError:
                return None
    return None

def get_timea(rem_time, increment, moveleft=40):
    buffer_time = 5
    safetime = rem_time - buffer_time
    if safetime < 0:
        safetime = rem_time

    timepmove = safetime / moveleft + increment
    return max(1, timepmove)

board = chess.Board()
moves = []
invalidmoves = []
options = {
    "Hash": 128,
    "Ponder": False,
}

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
            option_value = parts[4]
            options[option_name] = option_value
    
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
                    moves.append(move)
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
    
    elif inp.startswith("go"):
        parts = inp.split()
        wtime = btime = winc = binc = 0
        
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
            rem_time = wtime / 1000 if board.turn == chess.WHITE else btime / 1000
            increment = winc / 1000 if board.turn == chess.WHITE else binc / 1000

            max_time = get_timea(rem_time, increment)
            
            best_move = best_movep(board)
            if not best_move:
                best_move = best_minimax(board, max_time)
            
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