from abc import ABC, abstractmethod
from typing import Literal
import pandas as pd

class Piece(ABC):
    def __init__(self, x, y, direction):
        super().__init__()
        self.location = (x, y)
        self.possible_moves = ([],[])
        self.direction: Literal[1, -1] = direction
        self.get_possible_moves()

    def move(self, target: tuple[int, int], board: pd.DataFrame):

        board.iloc[self.location[1], self.location[0]] = "_"
        board.iloc[target[1], target[0]] = self # type: ignore
        self.location = target

        self.get_possible_moves()
    
    def get_team(self):
        return "black" if self.direction == 1 else "white"

    @abstractmethod
    def get_possible_moves(self): # seta self.valid_moves
        pass

    @abstractmethod
    def get_moves(self): # retorna movimento cru das pecas
        pass

    @abstractmethod
    def __str__(self):
        pass
    
    

