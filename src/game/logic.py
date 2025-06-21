import pygame
from timing import timer
from piece import Piece
import const as con 

class GamingLogic():
        def __init__(self) -> None:
            pass
        @timer
        def flip_board(self):

            # checar se já esta virada
            if self.board_is_fliped == False:
                self.board_is_fliped = True
            else:
                self.board_is_fliped = False

            self.board = self.board.iloc[::-1]
            self.board = self.board[self.board.columns[::-1]]

        def handle_click(self, pos):
            # Convert pixel position to board coordinates
            col = pos[0] // con.SQUARE_SIZE
            row = pos[1] // con.SQUARE_SIZE

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

        def moving_logic(self):
            board_row, board_col = self.handle_click(pygame.mouse.get_pos())
            piece: Piece | Literal["_"] = self.board.iloc[board_row, board_col] # type: ignore

            # Se nenhuma peça está selecionada, selecione se for sua peça
            if self.selected_piece is None:
                if piece == "_":
                    return
                
                if (piece.get_team() == "white" and self.white_to_move) or (piece.get_team() == "black" and not self.white_to_move):
                    self.selected_piece = piece
                    self.legal_moves = piece.set_legal_moves(self.board)
            # Se já tem uma peça selecionada, tente mover
            else:
                if (board_col, board_row) in self.legal_moves[0] or (board_col, board_row) in self.legal_moves[1]:# type: ignore
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
                    self.legal_moves = piece.set_legal_moves(self.board)

                # Se clicou em quadrado inválido ou peça adversária fora dos movimentos válidos, limpa a seleção
                else:
                    self.selected_piece = None
                    self.legal_moves = ([], [])
            print("Selected_piece: ", self.selected_piece)
            print("piece: ", piece)