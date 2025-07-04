from piece import Piece
import pandas as pd

class Rook(Piece):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)

    def get_possible_moves(self):
        x, y = self.location
        moves = []

        # Para a direita
        for dx in range(x + 1, 8):
            moves.append((dx, y))
        # Para a esquerda
        for dx in range(x - 1, -1, -1):
            moves.append((dx, y))
        # Para baixo
        for dy in range(y + 1, 8):
            moves.append((x, dy))
        # Para cima
        for dy in range(y - 1, -1, -1):
            moves.append((x, dy))

        self.possible_moves = (moves, [])
        
    def get_moves(self):
        return [(1,0), (-1,0), (0,1), (0,-1)]

    def move(self, target: tuple[int, int], board: pd.DataFrame):
        super().move(target, board)
        print("Ocorreu um movimento")

    # @timer
    def set_legal_moves(self, board):
        directions = self.get_moves()
        x, y = self.location
        legal_moves = ([], [])

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                next_pos = board.iloc[ny, nx]
                if not isinstance(next_pos, Piece):
                    legal_moves[0].append((nx, ny))
                else:
                    if self.get_team() != next_pos.get_team():
                        legal_moves[1].append((nx, ny))  # pode capturar
                    break  # encontrou qualquer peça, para nessa direção
                nx += dx
                ny += dy

        self.legal_moves = legal_moves
        return legal_moves
    
    def __str__(self):
        return "R" # "bP" if self.direction == 1 else "wP"
        
