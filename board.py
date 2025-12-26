import pygame
import copy
from pieces import *

class Board:
    def __init__(self):
        self.square_size = 75
        self.board = [[None]*8 for _ in range(8)]
        self.history = []
        self.current_turn = "w"
        self.selected_piece = None
        self.valid_moves_to_draw = []
        self.last_move = None # Stocke ((r_dep, c_dep), (r_arr, c_arr))
        self.piece_text = {"pawn":"P", "rook":"R", "knight":"N", "bishop":"B", "queen":"Q", "king":"K"}
        self.setup_board()

    def setup_board(self):
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        names = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for i, cls in enumerate(order):
            self.board[0][i] = cls("b", 0, i, f"b_{names[i]}")
            self.board[7][i] = cls("w", 7, i, f"w_{names[i]}")
        for i in range(8):
            self.board[1][i], self.board[6][i] = Pawn("b", 1, i, "b_pawn"), Pawn("w", 6, i, "w_pawn")

    def draw(self, win):
        font = pygame.font.SysFont("arial", 40, bold=True)
        for r in range(8):
            for c in range(8):
                # Couleurs de base
                color = (235, 235, 208) if (r + c) % 2 == 0 else (119, 148, 85)
                
                # Couleur si c'est le dernier coup joué (Jaune clair)
                if self.last_move and ((r, c) == self.last_move[0] or (r, c) == self.last_move[1]):
                    color = (247, 247, 105) if (r + c) % 2 == 0 else (218, 218, 70)

                pygame.draw.rect(win, color, (c*75, r*75, 75, 75))
                
                p = self.board[r][c]
                if p:
                    char = self.piece_text[p.name.split("_")[1]]
                    txt_col = (255, 255, 255) if p.color == "w" else (0, 0, 0)
                    surf = font.render(char, True, txt_col)
                    win.blit(surf, surf.get_rect(center=(c*75+37, r*75+37)))

        # Points pour les mouvements possibles
        for move in self.valid_moves_to_draw:
            pygame.draw.circle(win, (100, 100, 100), (move[1]*75+37, move[0]*75+37), 10)
        
        # Bordure pour la pièce sélectionnée
        if self.selected_piece:
            pygame.draw.rect(win, (186, 202, 43), (self.selected_piece.col*75, self.selected_piece.row*75, 75, 75), 4)

    def select(self, r, c):
        piece = self.board[r][c]
        if piece and piece.color == self.current_turn:
            self.selected_piece = piece
            self.valid_moves_to_draw = piece.get_valid_moves(self.board)
            return False
        elif self.selected_piece:
            if (r, c) in self.selected_piece.get_valid_moves(self.board):
                self.move_piece(self.selected_piece, r, c)
                self.selected_piece, self.valid_moves_to_draw = None, []
                return True
            self.selected_piece, self.valid_moves_to_draw = None, []
        return False

    def move_piece(self, piece, r, c):
        self.history.append(copy.deepcopy(self.board))
        self.last_move = ((piece.row, piece.col), (r, c)) # Enregistrer le coup
        self.board[piece.row][piece.col] = None
        piece.row, piece.col = r, c
        self.board[r][c] = piece
        self.current_turn = "b" if self.current_turn == "w" else "w"

    def undo(self):
        if self.history:
            self.board = self.history.pop()
            self.current_turn = "w" if self.current_turn == "b" else "b"
            self.last_move = None
