from piece import Piece
import pandas as pd

class Hourse(Piece):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)

    def get_possible_moves(self):
        x, y = self.location
        moves = self.get_moves()

        for i, move in enumerate(moves):
            moves[i] = (move[0]+x, move[1]+y) 

        self.possible_moves = (moves, [])
        
    def get_moves(self):
        return [(2,1), (2,-1), (-2,1), (-2,-1), (-1,2), (1,2), (1,-2), (-1,-2)]

    def move(self, target: tuple[int, int], board: pd.DataFrame):
        super().move(target, board)
        print("Ocorreu um movimento")

    # @timer
    def set_legal_moves(self, board):
        all_moves = self.possible_moves
        legal_moves = ([], [])

        for move in all_moves[0]:
            x, y = move

            if (y >= board.shape[0] or y < 0) or (x >= board.shape[1] or x < 0):
                continue
            
            next_pos = board.iloc[y, x]
            if not isinstance(next_pos, Piece):
                legal_moves[0].append((x, y))
            else:
                if self.get_team() != next_pos.get_team():
                    legal_moves[1].append((x, y))  # pode capturar

        self.legal_moves = legal_moves
        return legal_moves
    
    def __str__(self):
        return "H"