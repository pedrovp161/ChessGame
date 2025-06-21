from piece import Piece
import pandas as pd

class Pawn(Piece):
    def __init__(self, x, y, direction):
        self.moved = False
        super().__init__(x, y, direction)

    def get_possible_moves(self):
        all_moves = self.get_moves()
        x = self.location[0]
        y = self.location[1]
        
        for i, move in enumerate(all_moves[0]):
            all_moves[0][i] = (move[0]+x, move[1]+y)
        
        for i, move in enumerate(all_moves[1]):
            all_moves[1][i] = (move[0]+x, move[1]+y)
        
        self.possible_moves = all_moves
        
    def get_moves(self):
        if self.moved:
            return (
                [(0, self.direction)],
                [(1, self.direction), (-1, self.direction)]
            )
        
        return (
            [(0, self.direction), (0, self.direction*2)],
            [(1, self.direction), (-1, self.direction)]
        )

    def move(self, target: tuple[int, int], board: pd.DataFrame):
        super().move(target, board)

    # @timer
    def set_legal_moves(self, board: pd.DataFrame):
        all_moves = self.possible_moves
        legal_moves = ([], [])
        # print("all:", all_moves)
    
        # Possible normal moves
        for move in all_moves[0]:
            x = move[0]
            y = move[1]
            
            if (y >= board.shape[0] or y < 0) or (x >= board.shape[1] or x < 0):
                continue

            next_pos = board.iloc[y, x]
            if not isinstance(next_pos, Piece):
                legal_moves[0].append(move)

        # check blockage
        if legal_moves[0] and all_moves[0]:
            if min(legal_moves[0][0]) != min(all_moves[0][0]):
                legal_moves[0].clear()

        # Possible atk moves
        for move in all_moves[1]:
            x = move[0]
            y = move[1]
            
            if (y >= board.shape[0] or y < 0) or (x >= board.shape[1] or x < 0):
                continue

            next_pos = board.iloc[y, x]
            if isinstance(next_pos, Piece):
                if self.get_team() != next_pos.get_team():
                    legal_moves[1].append(move)

        # print("legal:", legal_moves)
        self.legal_moves = legal_moves

        return legal_moves
    
    def __str__(self):
        return "P" # "bP" if self.direction == 1 else "wP"
        
