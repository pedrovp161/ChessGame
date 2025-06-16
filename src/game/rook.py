from piece import Piece
import pandas as pd

class Rook(Piece):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)

    def get_possible_moves(self):
        all_moves = self.get_moves()
        x = self.location[0]
        y = self.location[1]
        
        if all_moves[0]:
            for i, move in enumerate(all_moves[0]):
                if isinstance(move, tuple) and len(move) == 1:
                    all_moves[0][i] = (move[0]+x, move[1]+y)
        
        if all_moves[1]:
            for i, move in enumerate(all_moves[1]):
                if isinstance(move, tuple) and len(move) == 1:
                    all_moves[1][i] = (move[0]+x, move[1]+y)# type:ignore
        
        self.possible_moves = all_moves
        
    def get_moves(self):
        return (
            [(0, self.direction), (1, 0), (-1, 0), (0, -self.direction)],
            [(), ()]
        )

    def move(self, target: tuple[int, int], board: pd.DataFrame):
        super().move(target, board)
        print("Ocorreu um movimento")

    # @timer
    def set_legal_moves(self, board):
        possible_moves = self.possible_moves
        legal_moves = ([], [])
        # print("all:", all_moves)
    
        # Possible normal moves
        for move in possible_moves[0]:
            x = move[0]
            y = move[1]
            
            if (y >= board.shape[0] or y < 0) or (x >= board.shape[1] or x < 0):
                continue

            next_pos = board.iloc[y, x]
            if not isinstance(next_pos, Piece):
                legal_moves[0].append(move)

        # Possible atk moves
        if len(possible_moves[1]) != 0:
            
            print("legal:", legal_moves)
            self.legal_moves = legal_moves

            return legal_moves
        
        for move in possible_moves[1]:
            x = move[0] # type: ignore
            y = move[1] # type: ignore
            
            if (y >= board.shape[0] or y < 0) or (x >= board.shape[1] or x < 0):
                continue

            next_pos = board.iloc[y, x]
            if isinstance(next_pos, Piece):
                if self.get_team() != next_pos.get_team():
                    legal_moves[1].append(move)

        print("legal:", legal_moves)
        self.legal_moves = legal_moves

        return legal_moves
    
    def __str__(self):
        return "R" # "bP" if self.direction == 1 else "wP"
        
