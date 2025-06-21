from logic import GamingLogic
from timing import timer
from piece import Piece
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from queen import Queen
from king import King
from hourse import Hourse
import const as con


from typing import Literal, Optional
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from themes.skins import Skins

import pygame

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
        self.board.loc['8', "a"] = Rook(x=0, y=0, direction=1) #type: ignore
        self.board.loc['8', "b"] = Hourse(x=1, y=0, direction=1) #type: ignore
        self.board.loc['8', "c"] = Bishop(x=2, y=0, direction=1) #type: ignore
        self.board.loc['8', "d"] = Queen(x=3, y=0, direction=1) #type: ignore
        self.board.loc['8', "e"] = King(x=4, y=0, direction=1) #type: ignore
        self.board.loc['8', "f"] = Bishop(x=5, y=0, direction=1) #type: ignore
        self.board.loc['8', "g"] = Hourse(x=6, y=0, direction=1) #type: ignore
        self.board.loc['8', "h"] = Rook(x=7, y=0, direction=1) #type: ignore

        # White pieces
        self.board.loc['2'] = [Pawn(x=column, y=6, direction=-1) for column in range(self.board.shape[1])]
        self.board.loc['1', "a"] = Rook(x=0, y=7, direction=-1) #type: ignore
        self.board.loc['1', "b"] = Hourse(x=1, y=7, direction=-1) #type: ignore
        self.board.loc['1', "c"] = Bishop(x=2, y=7, direction=-1) #type: ignore
        self.board.loc['1', "d"] = Queen(x=3, y=7, direction=-1) #type: ignore
        self.board.loc['1', "e"] = King(x=4, y=7, direction=-1) #type: ignore
        self.board.loc['1', "f"] = Bishop(x=5, y=7, direction=-1) #type: ignore
        self.board.loc['1', "g"] = Hourse(x=6, y=7, direction=-1) #type: ignore
        self.board.loc['1', "h"] = Rook(x=7, y=7, direction=-1) #type: ignore

        # trocando nan para '_'
        self.board = self.board.fillna("_")
    
    def draw_board(self):
        # Skin setup
        skin = Skins()
        WHITE, BLACK, LIGHT_SQUARE, DARK_SQUARE = skin.default_skin()

        # Draw chess board with alternating colors
        for row in range(con.BOARD_SIZE):
            for col in range(con.BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(self.screen, 
                                 color, 
                                 (col * con.SQUARE_SIZE, row * con.SQUARE_SIZE, con.SQUARE_SIZE, con.SQUARE_SIZE)
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
                self.screen.blit(text, (col * con.SQUARE_SIZE + 30, row * con.SQUARE_SIZE + 30)) 
    # @timer
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((con.WINDOW_SIZE, con.WINDOW_SIZE))
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
                center = (col * con.SQUARE_SIZE + con.SQUARE_SIZE // 2,
                        row * con.SQUARE_SIZE + con.SQUARE_SIZE // 2)
                pygame.draw.circle(self.screen, color="lightblue", center=center, radius=10)

            for move in self.legal_moves[1]:
                col, row = move
                center = (col * con.SQUARE_SIZE + con.SQUARE_SIZE // 2,
                        row * con.SQUARE_SIZE + con.SQUARE_SIZE // 2)
                pygame.draw.circle(self.screen, color="firebrick", center=center, radius=10)
        
        pygame.display.flip()

