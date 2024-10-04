import chess

pawnblack = 0b0000000011111111000000000000000000000000000000001111111100000000
pawnwhite = 0b0000000000000000000000000000000011111111000000000000000000000000
knightblack = 0b0100000000000000000000000000000000000000000000000000000000000010
knightwhite = 0b0000000000000000000000000000000000000000000000000000000000001001
bishopblack = 0b0010000000000000000000000000000000000000000000000000000000000100
bishopwhite = 0b0000000000000000000000000000000000000000000000000000000000000010
rookblack = 0b1000000000000000000000000000000000000000000000000000000000001000
rookwhite = 0b0000000000000000000000000000000000000000000000000000000000000001
queenblack = 0b0000000000000000000000000000000000000000000000000000000000000000
queenwhite = 0b0000000000000000000000000000000000000000000000000000000000000000
kingblack = 0b0000000000000000000000000000000000000000000000000000000000000000
kingwhite = 0b0000000000000000000000000000000000000000000000000000000000000000

material = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 35,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 0
}

PST_PAWN_WHITE = [
    0, 0, 0, 0, 0, 0, 0, 0, 
    -1, -1, -2, -2, -2, -2, -1, -1, 
    1, 0, 0, 0, 0, 0, 0, 1, 
    0.5, 0.5, 0.5, 1, 1, 0.5, 0.5, 0.5, 
    0, 0.5, 1, 1.5, 1.5, 1, 0.5, 0, 
    0.3, 1, 2, 2.5, 2.5, 2, 1, 0.3, 
    1, 2, 3, 4, 4, 3, 2, 1, 
    0, 0, 0, 0, 0, 0, 0, 0
]

PST_PAWN_BLACK = PST_PAWN_WHITE[::-1]

PST_KNIGHT_WHITE = [
    -5, -4, -3, -3, -3, -3, -4, -5, 
    -4, -2, 0, 0.5, 0.5, 0, -2, -4, 
    -3, 0, 1, 1.5, 1.5, 1, 0, -3, 
    -3, 0.5, 1.5, 1, 1, 1.5, 0.5, -3, 
    -3, 0.5, 1.5, 1, 1, 1.5, 0.5, -3, 
    -3, 0.5, 1.5, 1.5, 1.5, 1, 0.5, -3, 
    -4, -2, 0, 0.5, 0.5, 0, -2, -4, 
    -5, -4, -3, -3, -3, -3, -4, -5
]

PST_KNIGHT_BLACK = PST_KNIGHT_WHITE[::-1]

PST_BISHOP_WHITE = [
    -2, -1, -1, -1, -1, -1, -1, -2, 
    -1, 0, 0, 0, 0, 0, 0, -1, 
    -0.5, 0, 0.5, 1, 1, 0.5, 0, -0.5, 
    -0.5, 0.5, 1, 1.5, 1.5, 1, 0.5, -0.5, 
    -0.5, 0.5, 1, 1.5, 1.5, 1, 0.5, -0.5, 
    -0.5, 0, 0.5, 1, 1, 0.5, 0, -0.5, 
    -1, 0, 0, 0, 0, 0, 0, -1, 
    -2, -1, -1, -1, -1, -1, -1, -2
]

PST_BISHOP_BLACK = PST_BISHOP_WHITE[::-1]

PST_ROOK_WHITE = [
    0, 0, 0, 0, 0, 0, 0, 0, 
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 
    0, 0, 0, 0.5, 0.5, 0, 0, 0, 
    0, 0, 0, 0.5, 0.5, 0, 0, 0, 
    0, 0, 0, 0.5, 0.5, 0, 0, 0, 
    0, 0, 0, 0.5, 0.5, 0, 0, 0, 
    1, 1, 1, 1, 1, 1, 1, 1, 
    0, 0, 0, 0, 0, 0, 0, 0
]

PST_ROOK_BLACK = PST_ROOK_WHITE[::-1]

PST_QUEEN_WHITE = [
    0, 0, 0, 0, 0, 0, 0, 0, 
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 
    0, 0, 0, 0.5, 0.5, 0, 0, 0, 
    0, 0, 0, 0.5, 0.5, 0, 0, 0, 
    0, 0, 0, 0.5, 0.5, 0, 0, 0, 
    0, 0, 0, 0.5, 0.5, 0, 0, 0, 
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 
    0, 0, 0, 0, 0, 0, 0, 0
]

PST_QUEEN_BLACK = PST_QUEEN_WHITE[::-1]

PST_KING_WHITE_MIDGAME = [
    -3, -4, -4, -5, -5, -4, -4, -3, 
    -3, -4, -4, -5, -5, -4, -4, -3, 
    -3, -4, -4, -5, -5, -4, -4, -3, 
    -3, -4, -4, -5, -5, -4, -4, -3, 
    -2, -3, -3, -4, -4, -3, -3, -2, 
    -1, -2, -2, -2, -2, -2, -2, -1, 
    1, 2, 2, 2, 2, 2, 2, 1, 
    2, 3, 1, 0, 0, 1, 3, 2
]

PST_KING_BLACK_MIDGAME = PST_KING_WHITE_MIDGAME[::-1]

PST_KING_WHITE_ENDGAME = [
    -2, -1, -1, -1, -1, -1, -1, -2, 
    -1, 2, 2, 2, 2, 2, 2, -1, 
    -1, 2, 3, 3, 3, 3, 2, -1, 
    -1, 2, 3, 4, 4, 3, 2, -1, 
    -1, 2, 3, 4, 4, 3, 2, -1, 
    -1, 2, 3, 3, 3, 3, 2, -1, 
    -1, 2, 2, 2, 2, 2, 2, -1, 
    -2, -1, -1, -1, -1, -1, -1, -2
]

PST_KING_BLACK_ENDGAME = PST_KING_WHITE_ENDGAME[::-1]

kingwhite_midgame = PST_KING_WHITE_MIDGAME
kingwhite_endgame = PST_KING_WHITE_ENDGAME
kingblack_midgame = PST_KING_BLACK_MIDGAME
kingblack_endgame = PST_KING_BLACK_ENDGAME

tables = {
    chess.PAWN: {chess.WHITE: (pawnwhite, PST_PAWN_WHITE), chess.BLACK: (pawnblack, PST_PAWN_BLACK)},
    chess.KNIGHT: {chess.WHITE: (knightwhite, PST_KNIGHT_WHITE), chess.BLACK: (knightblack, PST_KNIGHT_BLACK)},
    chess.BISHOP: {chess.WHITE: (bishopwhite, PST_BISHOP_WHITE), chess.BLACK: (bishopblack, PST_BISHOP_BLACK)},
    chess.ROOK: {chess.WHITE: (rookwhite, PST_ROOK_WHITE), chess.BLACK: (rookblack, PST_ROOK_BLACK)},
    chess.QUEEN: {chess.WHITE: (queenwhite, PST_QUEEN_WHITE), chess.BLACK: (queenblack, PST_QUEEN_BLACK)},
    chess.KING: {
        chess.WHITE: (kingwhite_midgame, PST_KING_WHITE_MIDGAME), 
        chess.BLACK: (kingblack_midgame, PST_KING_BLACK_MIDGAME),
        "endgame_white": (kingwhite_endgame, PST_KING_WHITE_ENDGAME),
        "endgame_black": (kingblack_endgame, PST_KING_BLACK_ENDGAME)
    }
}
