import copy
from utils import VALUES

def evaluate(board_obj):
    score = 0
    for r in range(8):
        for c in range(8):
            p = board_obj.board[r][c]
            if p:
                v = VALUES.get(p.name.split("_")[1], 0)
                score += v if p.color == "b" else -v
    return score

def get_all_moves(board_obj, color):
    moves = []
    for r in range(8):
        for c in range(8):
            p = board_obj.board[r][c]
            if p and p.color == color:
                for m in p.get_valid_moves(board_obj.board): moves.append((p, m))
    return moves

def minimax(board_obj, depth, alpha, beta, maximizing):
    if depth == 0: return evaluate(board_obj), None
    moves = get_all_moves(board_obj, "b" if maximizing else "w")
    if not moves: return evaluate(board_obj), None
    best_move = None
    if maximizing:
        max_ev = -float('inf')
        for piece, (tr, tc) in moves:
            old_r, old_c, cap = piece.row, piece.col, board_obj.board[tr][tc]
            board_obj.board[old_r][old_c] = None
            piece.row, piece.col, board_obj.board[tr][tc] = tr, tc, piece
            ev, _ = minimax(board_obj, depth-1, alpha, beta, False)
            board_obj.board[tr][tc], piece.row, piece.col, board_obj.board[old_r][old_c] = cap, old_r, old_c, piece
            if ev > max_ev: max_ev, best_move = ev, (piece, (tr, tc))
            alpha = max(alpha, ev)
            if beta <= alpha: break
        return max_ev, best_move
    else:
        min_ev = float('inf')
        for piece, (tr, tc) in moves:
            old_r, old_c, cap = piece.row, piece.col, board_obj.board[tr][tc]
            board_obj.board[old_r][old_c] = None
            piece.row, piece.col, board_obj.board[tr][tc] = tr, tc, piece
            ev, _ = minimax(board_obj, depth-1, alpha, beta, True)
            board_obj.board[tr][tc], piece.row, piece.col, board_obj.board[old_r][old_c] = cap, old_r, old_c, piece
            if ev < min_ev: min_ev, best_move = ev, (piece, (tr, tc))
            beta = min(beta, ev)
            if beta <= alpha: break
        return min_ev, best_move
