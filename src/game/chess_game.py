import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Literal, Optional
from themes.skins import Skins
from timing import timer
from game import *
from piece import Piece
from pawn import Pawn
import pandas as pd
import pygame
import sys
import os
from copy import deepcopy
from time import sleep

print(os.getcwd())

# chess game
class ChessGame:
    def __init__(self):
        self.running = True
        self.screen: pygame.Surface
        self.board = pd.DataFrame()
        self.legal_moves: tuple[list[tuple[int, int]], list[tuple[int, int]]] = ([],[])
        self.white_to_move = True
        self.moving = False
        self.selected_piece: Optional[Piece] = None
        self.history_of_moves = [] #TODO
        self.piece_already_selected = False
        self.selected_coords = ()
        self.last_piece = ""
        self.last_coords = ()
        self.board_is_fliped = False
        self.piece_order = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] # Set up pieces (simplified representation)
        
    @timer
    def initialize_board(self):
        # Initialize 8x8 board with pieces in starting position
        self.board = pd.DataFrame(None, index=[str(i) for i in range(8, 0, -1)], columns=list('abcdefgh'))
        # Black pieces
        # self.board.loc['8'] = [f'b{p}' for p in self.piece_order]
        self.board.loc['7'] = [Pawn(x=column, y=1, direction=1) for column in range(self.board.shape[1])]

        # White pieces
        self.board.loc['2'] = [Pawn(x=column, y=6, direction=-1) for column in range(self.board.shape[1])]
        # self.board.loc['1'] = [f'w{p}' for p in self.piece_order]

        # trocando nan para '_'
        self.board = self.board.fillna("_")
    
    def draw_board(self):
        # Skin setup
        skin = Skins()
        WHITE, BLACK, LIGHT_SQUARE, DARK_SQUARE = skin.default_skin()

        # Draw chess board with alternating colors
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(self.screen, 
                                 color, 
                                 (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                                 )
                
                # Draw pieces
                piece = self.board.iloc[row, col]
                if isinstance(piece, Piece):
                    font = pygame.font.Font(None, 42)
                    if piece.get_team() == "white":
                        text = font.render(str(piece), True, WHITE)
                    elif piece.get_team() == "black":
                        text = font.render(str(piece), True, BLACK)
                    else:
                        print(f"Invalid piece string: {piece}")
                        break
                    self.screen.blit(text, (col * SQUARE_SIZE + 30, row * SQUARE_SIZE + 30))
    
    @timer
    def flip_board(self):

        # checar se já esta virada
        if self.board_is_fliped == False:
            self.board_is_fliped = True
        else:
            self.board_is_fliped = False

        self.board = self.board.iloc[::-1]
        self.board = self.board[self.board.columns[::-1]]
    
    @timer
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Chess Game')
        self.initialize_board()
    
    def handle_click(self, pos):
        # Convert pixel position to board coordinates
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if not self.board_is_fliped:
            board_row = int(row)
            board_col = int(col)
            ui_row = 8 - board_row      # linha de exibição: 1 (baixo) a 8 (cima)
            ui_col = board_col + 1      # coluna de exibição: 1 a 8
        else:
            board_row = 7 - int(row)
            board_col = 7 - int(col)
            ui_row = board_row + 1      # linha de exibição: 1 a 8
            ui_col = 8 - board_col      # coluna de exibição: 8 a 1

        # print(f"l-c (UI): {ui_row} - {ui_col}")
        # print(f"índice da matriz: {board_row} - {board_col}")
        # print(f"Obj clicado {self.board.iloc[board_row, board_col]}")

        return board_row, board_col
    
    @timer
    def set_legal_moves(self, piece: Piece):
        all_moves = piece.possible_moves
        legal_moves = ([], [])
        # print("all:", all_moves)
    
        # Possible normal moves
        for move in all_moves[0]:
            x = move[0]
            y = move[1]
            
            if (y >= self.board.shape[0] or y < 0) or (x >= self.board.shape[1] or x < 0):
                continue

            next_p = self.board.iloc[y, x]
            if not isinstance(next_p, Piece):
                legal_moves[0].append(move)

        # Possible atk moves
        for move in all_moves[1]:
            x = move[0]
            y = move[1]
            
            if (y >= self.board.shape[0] or y < 0) or (x >= self.board.shape[1] or x < 0):
                continue

            next_p = self.board.iloc[y, x]
            if isinstance(next_p, Piece):
                if piece.get_team() != next_p.get_team():
                    legal_moves[1].append(move)

        # print("legal:", legal_moves)

        self.legal_moves = legal_moves

    def update_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:

                board_row, board_col = self.handle_click(pygame.mouse.get_pos())
                piece: Piece | Literal["_"] = self.board.iloc[board_row, board_col] # type: ignore

                # Se nenhuma peça está selecionada, selecione se for sua peça
                if self.selected_piece is None:
                    if piece == "_":
                        return
                    
                    if (piece.get_team() == "white" and self.white_to_move) or (piece.get_team() == "black" and not self.white_to_move):
                        self.selected_piece = piece
                        self.set_legal_moves(piece)
                # Se já tem uma peça selecionada, tente mover
                else:
                    if (board_col, board_row) in self.legal_moves[0] or (board_col, board_row) in self.legal_moves[1]:
                        self.selected_piece.move(target=(board_col, board_row), board=self.board)
                        self.white_to_move = not self.white_to_move
                        self.selected_piece = None
                        self.legal_moves = ([], [])

                    # Se clicou em outra peça própria, troca a seleção
                    elif isinstance(piece, Piece) and (
                        (piece.get_team() == "white" and self.white_to_move) or
                        (piece.get_team() == "black" and not self.white_to_move)
                    ):
                        self.selected_piece = piece
                        self.set_legal_moves(piece)

                    # Se clicou em quadrado inválido ou peça adversária fora dos movimentos válidos, limpa a seleção
                    else:
                        self.selected_piece = None
                        self.legal_moves = ([], [])

                # print("Movimentos legais: ", self.legal_moves)
                # print("Selected_piece: ", self.selected_piece)
                # print("Selected_coords: ", self.selected_coords)
                # print("piece: ", piece)

            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_f:
                        self.flip_board()
                    case pygame.K_b:
                        print(self.board)
                    case pygame.K_c:
                        os.system("clear")
                    case pygame.K_0:
                        print(self.selected_piece.location) #type: ignore
                    case pygame.K_h:
                        print(f"HISTORY: {self.history_of_moves}")
                
        self.screen.fill((255, 255, 255))
        self.draw_board()

        if isinstance(self.selected_piece, Piece): #type: ignore
            for move in self.legal_moves[0]:
                col, row = move
                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(self.screen, color="lightblue", center=center, radius=10)

            for move in self.legal_moves[1]:
                col, row = move
                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(self.screen, color="firebrick", center=center, radius=10)
        
        pygame.display.flip()

    def run(self):
        self.setup()
        while self.running:
            self.update_loop()
        pygame.quit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()




