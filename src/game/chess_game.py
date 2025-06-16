import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Literal, Optional
from themes.skins import Skins
from timing import timer
from game import *
from piece import Piece
from pawn import Pawn
from rook import Rook
from logic import GamingLogic
import pandas as pd
import pygame
import sys
import os
from copy import deepcopy
from time import sleep

print(os.getcwd())

# chess game
class ChessGame(GamingLogic):

    def __init__(self):
        self.running = True
        self.screen: pygame.Surface
        self.board = pd.DataFrame()
        self.legal_moves: tuple[list[tuple[int, int]], list[tuple[int, int]]] = ([],[])
        self.white_to_move = True
        self.selected_piece: Optional[Piece] = None
        self.history_of_moves = [] #TODO
        self.board_is_fliped = False
        self.piece_order = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] # Set up pieces (simplified representation)
         
    # @timer
    def initialize_board(self):
        # Initialize 8x8 board with pieces in starting position
        self.board = pd.DataFrame(None, index=[str(i) for i in range(8, 0, -1)], columns=list('abcdefgh'))
        # Black pieces
        # self.board.loc['8'] = [f'b{p}' for p in self.piece_order]
        self.board.loc['7'] = [Pawn(x=column, y=1, direction=1) for column in range(self.board.shape[1])]

        # White pieces
        self.board.loc['2'] = [Pawn(x=column, y=6, direction=-1) for column in range(self.board.shape[1])]
        self.board.loc['1', "a"] = Rook(x=0, y=0, direction=-1) #type: ignore

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

                if not isinstance(piece, Piece):
                    continue

                font = pygame.font.Font(None, 42)
                if piece.get_team() == "white":
                    text = font.render(str(piece), True, WHITE)
                elif piece.get_team() == "black":
                    text = font.render(str(piece), True, BLACK)
                else:
                    print(f"Invalid piece string: {piece}")
                    break
                self.screen.blit(text, (col * SQUARE_SIZE + 30, row * SQUARE_SIZE + 30)) 
    # @timer
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Chess Game')
        self.initialize_board()
    
    def update_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.moving_logic()

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

