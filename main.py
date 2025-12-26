import pygame, sys
from board import Board
from ai import minimax

WIDTH, HEIGHT = 600, 680
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def choose_mode():
    WIN.fill((50, 50, 50))
    f = pygame.font.SysFont("arial", 35)
    r1 = WIN.blit(f.render("1. Joueur vs Joueur", True, (255,255,255)), (150, 200))
    r2 = WIN.blit(f.render("2. Joueur vs IA", True, (255,255,255)), (150, 300))
    pygame.display.update()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if r1.collidepoint(e.pos): return "PVP"
                if r2.collidepoint(e.pos): return "AI"

def main():
    mode = choose_mode()
    board = Board()
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        if mode == "AI" and board.current_turn == "b":
            _, move = minimax(board, 2, -10000, 10000, True)
            if move: board.move_piece(board.board[move[0].row][move[0].col], move[1][0], move[1][1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < 600: board.select(y // 75, x // 75)
                elif 120 <= x <= 220 and y > 610: board.undo()
        WIN.fill((30, 30, 30))
        board.draw(WIN)
        pygame.draw.rect(WIN, (100,100,100), (120, 620, 90, 40))
        WIN.blit(pygame.font.SysFont("arial", 20).render("UNDO", True, (255,255,255)), (135, 630))
        pygame.display.update()

if __name__ == "__main__":
    main()
