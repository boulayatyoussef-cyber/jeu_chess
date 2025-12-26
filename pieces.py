class Piece:
    def __init__(self, color, row, col, name):
        self.color, self.row, self.col, self.name = color, row, col, name
    def is_on_board(self, r, c): return 0 <= r < 8 and 0 <= c < 8

class Pawn(Piece):
    def get_valid_moves(self, board):
        moves = []
        dir = -1 if self.color == "w" else 1
        if self.is_on_board(self.row + dir, self.col) and board[self.row + dir][self.col] is None:
            moves.append((self.row + dir, self.col))
            if (self.color == "w" and self.row == 6) or (self.color == "b" and self.row == 1):
                if board[self.row + 2 * dir][self.col] is None: moves.append((self.row + 2 * dir, self.col))
        for dc in [-1, 1]:
            nr, nc = self.row + dir, self.col + dc
            if self.is_on_board(nr, nc) and board[nr][nc] and board[nr][nc].color != self.color:
                moves.append((nr, nc))
        return moves

class Knight(Piece):
    def get_valid_moves(self, board):
        moves = []
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            nr, nc = self.row + dr, self.col + dc
            if self.is_on_board(nr, nc) and (board[nr][nc] is None or board[nr][nc].color != self.color):
                moves.append((nr, nc))
        return moves

class SlidingPiece(Piece):
    def get_moves(self, board, dirs):
        moves = []
        for dr, dc in dirs:
            for i in range(1, 8):
                nr, nc = self.row + dr*i, self.col + dc*i
                if not self.is_on_board(nr, nc): break
                if board[nr][nc] is None: moves.append((nr, nc))
                elif board[nr][nc].color != self.color:
                    moves.append((nr, nc)); break
                else: break
        return moves

class Rook(SlidingPiece):
    def get_valid_moves(self, board): return self.get_moves(board, [(0,1),(0,-1),(1,0),(-1,0)])
class Bishop(SlidingPiece):
    def get_valid_moves(self, board): return self.get_moves(board, [(1,1),(1,-1),(-1,1),(-1,-1)])
class Queen(SlidingPiece):
    def get_valid_moves(self, board): return self.get_moves(board, [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)])
class King(Piece):
    def get_valid_moves(self, board):
        moves = []
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0: continue
                nr, nc = self.row + dr, self.col + dc
                if self.is_on_board(nr, nc) and (board[nr][nc] is None or board[nr][nc].color != self.color):
                    moves.append((nr, nc))
        return moves
