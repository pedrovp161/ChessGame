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
        self.moved = True
        super().move(target, board)
        print("##############")
        
    
    def __str__(self):
        return "P"#"bP" if self.direction == 1 else "wP"
        
